#define UNICODE
 #include <set>
 #include <cassert>
#include <windows.h>
#include <base/base.h>
#include <oleacc.h>
#include <AcrobatAccess/AcrobatAccess.h>
#include "adobeAcrobat.h"

using namespace std;

typedef std::set<VBufBackend_t*> VBufBackendSet_t;

HINSTANCE backendLibHandle=NULL;

#pragma comment(linker,"/entry:_DllMainCRTStartup@12")
BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		backendLibHandle=hModule;
	}
	return TRUE;
}

UINT wmMainThreadSetup=0;
UINT wmMainThreadTerminate=0;
VBufBackendSet_t backends;
HWINEVENTHOOK winEventHookID;

IAccessible* IAccessibleFromIdentifier(int docHandle, int ID) {
	int res;
	IAccessible* pacc=NULL;
	VARIANT varChild;
	DEBUG_MSG(L"Calling AccessibleObjectFromEvent");
	if((res=AccessibleObjectFromEvent((HWND)docHandle,OBJID_CLIENT,ID,&pacc,&varChild))!=S_OK) {
		DEBUG_MSG(L"AccessibleObjectFromEvent returned "<<res);
		return NULL;
	}
	DEBUG_MSG(L"Got IAccessible at "<<pacc);
	VariantClear(&varChild);
	return pacc;
}

long getAccID(IAccessible* pacc) {
	int res;
	IServiceProvider* pserv=NULL;
	IAccID* paccID = NULL;
	long ID;

	DEBUG_MSG(L"calling IAccessible::QueryInterface with IID_IServiceProvider");
	if((res=pacc->QueryInterface(IID_IServiceProvider,(void**)(&pserv)))!=S_OK) {
		DEBUG_MSG(L"IAccessible::QueryInterface returned "<<res);
		return 0;
	}  
	DEBUG_MSG(L"IServiceProvider at "<<pserv);
	DEBUG_MSG(L"calling IServiceProvider::QueryService for IAccID");
	if((res=pserv->QueryService(SID_AccID,IID_IAccID,(void**)(&paccID)))!=S_OK) {
		DEBUG_MSG(L"IServiceProvider::QueryService returned "<<res);
		return 0;
	} 
	DEBUG_MSG(L"IAccID at "<<paccID);
	DEBUG_MSG(L"releasingIServiceProvider");
	pserv->Release();

	DEBUG_MSG(L"Calling get_accID");
	if((res=paccID->get_accID((long*)(&ID)))!=S_OK) {
		DEBUG_MSG(L"paccID->get_accID returned "<<res);
		ID = 0;
	}

	DEBUG_MSG("Releasing IAccID");
	paccID->Release();

	return ID;
}

VBufStorage_fieldNode_t* fillVBuf(int docHandle, IAccessible* pacc, VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode) {
	int res;
	DEBUG_MSG(L"Entered fillVBuf, with pacc at "<<pacc<<L", parentNode at "<<parentNode<<L", previousNode "<<previousNode);
	assert(buffer); //buffer can't be NULL
	assert(!parentNode||buffer->isNodeInBuffer(parentNode)); //parent node must be in buffer
	assert(!previousNode||buffer->isNodeInBuffer(previousNode)); //Previous node must be in buffer
	VBufStorage_fieldNode_t* tempNode;

	//all IAccessible methods take a variant for childID, get one ready
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=0;

	// GET ID
	int ID = getAccID(pacc);

	//Make sure that we don't already know about this object -- protect from loops
	/*if(buffer->getControlFieldNodeWithIdentifier(docHandle,ID)!=NULL) {
		DEBUG_MSG(L"A node with this docHandle and ID already exists, returning NULL");
		pacc->Release();
		return NULL;
	}*/

	//Add this node to the buffer
	DEBUG_MSG(L"Adding Node to buffer");
	parentNode=buffer->addControlFieldNode(parentNode,previousNode,docHandle,ID,TRUE);
	assert(parentNode); //new node must have been created
	previousNode=NULL;
	DEBUG_MSG(L"Added  node at "<<parentNode);

	// Get role with accRole
	DEBUG_MSG(L"Get role with accRole");
	{
		wostringstream s;
		VARIANT varRole;
		VariantInit(&varRole);
		if((res=pacc->get_accRole(varChild,&varRole))!=S_OK) {
			DEBUG_MSG(L"accRole returned code "<<res);
			s<<0;
		} else if(varRole.vt==VT_BSTR) {
			DEBUG_MSG(L"Got role string of " << varRole.bstrVal);
			s << varRole.bstrVal;
		} else if(varRole.vt==VT_I4) {
			DEBUG_MSG(L"Got role of " << varRole.lVal);
			s << varRole.lVal;
		}
		parentNode->addAttribute(L"IAccessible::role",s.str().c_str());
		VariantClear(&varRole);
	}

	// Get states with accState
	DEBUG_MSG(L"get states with IAccessible::get_accState");
	varChild.lVal=0;
	VARIANT varState;
	VariantInit(&varState);
	if((res=pacc->get_accState(varChild,&varState))!=S_OK) {
		DEBUG_MSG(L"pacc->get_accState returned "<<res);
		varState.vt=VT_I4;
		varState.lVal=0;
	}
	int states=varState.lVal;
	VariantClear(&varState);
	DEBUG_MSG(L"states is "<<states);
	//Add each state that is on, as an attrib
	for(int i=0;i<32;i++) {
		int state=1<<i;
		if(state&states) {
			wostringstream nameStream;
			nameStream<<L"IAccessible::state_"<<state;
			parentNode->addAttribute(nameStream.str().c_str(),L"1");
		}
	}

	//Get the child count
	int childCount=0;
	DEBUG_MSG(L"get childCount with IAccessible::get_accChildCount");
	if((res=pacc->get_accChildCount((long*)(&childCount)))!=S_OK) {
		DEBUG_MSG(L"pacc->get_accChildCount returned "<<res);
		childCount=0;
	}
	DEBUG_MSG(L"childCount is "<<childCount);

	// Iterate through the children.
	if (childCount > 0) {
		DEBUG_MSG(L"Allocate memory to hold children");
		VARIANT* varChildren;
		if((varChildren=(VARIANT*)malloc(sizeof(VARIANT)*childCount))==NULL) {
			DEBUG_MSG(L"Error allocating varChildren memory");
			return NULL;
		}
		DEBUG_MSG(L"Fetch children with AccessibleChildren");
		if((res=AccessibleChildren(pacc,0,childCount,varChildren,(long*)(&childCount)))!=S_OK) {
			DEBUG_MSG(L"AccessibleChildren returned "<<res);
			childCount=0;
		}
		DEBUG_MSG(L"got "<<childCount<<L" children");
		for(int i=0;i<childCount;i++) {
			DEBUG_MSG(L"child "<<i);
			if(varChildren[i].vt==VT_DISPATCH) {
				DEBUG_MSG(L"QueryInterface dispatch child to IID_IAccesible");
				IAccessible* childPacc;
				if((res=varChildren[i].pdispVal->QueryInterface(IID_IAccessible,(void**)(&childPacc)))!=S_OK) {
					DEBUG_MSG(L"varChildren["<<i<<L"].pdispVal->QueryInterface to IID_iAccessible returned "<<res);
					continue;
				}
				DEBUG_MSG(L"calling filVBuf with child object ");
				if((tempNode=fillVBuf(docHandle,childPacc,buffer,parentNode,previousNode))!=NULL) {
					previousNode=tempNode;
				} else {
					DEBUG_MSG(L"Error in calling fillVBuf");
				}
				DEBUG_MSG(L"releasing child IDispatch object");
			}
			VariantClear(&(varChildren[i]));
		}
		DEBUG_MSG(L"Freeing memory holding children");
		free(varChildren);
	} else {

		// Get the value (text) with accValue
		BSTR value=NULL;
		if((res=pacc->get_accValue(varChild,&value))!=S_OK) {
			DEBUG_MSG(L"IAccessible::get_accValue returned "<<res);
			value=NULL;
		}
		if(value!=NULL&&SysStringLen(value)==0) {
			SysFreeString(value);
			value=NULL;
		}
		if (value != NULL) {
			if((tempNode=buffer->addTextFieldNode(parentNode,previousNode,value))!=NULL) {
				previousNode=tempNode;
			}
		}
	}

	DEBUG_MSG(L"Returning node at "<<parentNode);
	return parentNode;
}

void CALLBACK mainThreadWinEventCallback(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
}

void mainThreadSetup(VBufBackend_t* backend) {
	int processID=GetCurrentProcessId();
	int threadID=GetCurrentThreadId();
	DEBUG_MSG(L"process ID "<<processID<<L", thread ID "<<threadID);
	backends.insert(backend);
	if (backends.size() == 1) {
		DEBUG_MSG(L"Registering win event callback");
		winEventHookID=SetWinEventHook(EVENT_MIN,0xffffffff,backendLibHandle,(WINEVENTPROC)mainThreadWinEventCallback,processID,threadID,WINEVENT_INCONTEXT);
		assert(winEventHookID!=0); //winEventHookID must be non-0
		DEBUG_MSG(L"Registered win event callback, with ID "<<winEventHookID);
	}
	VBufStorage_buffer_t* storageBuffer=backend->getStorageBuffer();
	storageBuffer->lock.acquire();
	//Render buffer
	IAccessible* pacc=IAccessibleFromIdentifier(backend->getRootDocHandle(),backend->getRootID());
	assert(pacc); //must get a valid IAccessible object
	fillVBuf(backend->getRootDocHandle(),pacc,storageBuffer,NULL,NULL);
	pacc->Release();
	storageBuffer->lock.release();
	Beep(220,70);
}

LRESULT CALLBACK mainThreadCallWndProcHook(int code, WPARAM wParam,LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if((code==HC_ACTION)&&(pcwp->message==wmMainThreadSetup)) {
		mainThreadSetup((VBufBackend_t*)(pcwp->wParam));
	}
	return CallNextHookEx(0,code,wParam,lParam);
}

AdobeAcrobatVBufBackend_t::AdobeAcrobatVBufBackend_t(int docHandle, int ID, VBufStorage_buffer_t* storageBuffer): VBufBackend_t(docHandle,ID,storageBuffer) {
	int res;
	DEBUG_MSG(L"Initializing Adobe Acrobat backend");
	if(!wmMainThreadSetup) wmMainThreadSetup=RegisterWindowMessage(L"VBufBackend_adobeAcrobat_mainThreadSetup");
	if(!wmMainThreadTerminate) wmMainThreadTerminate=RegisterWindowMessage(L"VBufBackend_adobeAcrobat_mainThreadTerminate");
	DEBUG_MSG(L"wmMainThreadSetup message: "<<wmMainThreadSetup<<L", wmMainThreadTerminate message: "<<wmMainThreadTerminate);
	DEBUG_MSG(L"Setting hook");
	HWND rootWindow=(HWND)rootDocHandle;
	rootThreadID=GetWindowThreadProcessId(rootWindow,NULL);
	HHOOK mainThreadCallWndProcHookID=SetWindowsHookEx(WH_CALLWNDPROC,(HOOKPROC)mainThreadCallWndProcHook,backendLibHandle,rootThreadID);
	assert(mainThreadCallWndProcHookID!=0); //valid hooks are not 0
	DEBUG_MSG(L"Hook set with ID "<<mainThreadCallWndProcHookID);
	DEBUG_MSG(L"Sending wmMainThreadSetup to window, docHandle "<<rootDocHandle<<L", ID "<<rootID<<L", backend "<<this);
	SendMessage(rootWindow,wmMainThreadSetup,(WPARAM)this,0);
	DEBUG_MSG(L"Message sent");
	DEBUG_MSG(L"Removing hook");
	res=UnhookWindowsHookEx(mainThreadCallWndProcHookID);
	assert(res!=0); //unHookWindowsHookEx must return non-0
	DEBUG_MSG(L"Gecko backend initialized");
}

AdobeAcrobatVBufBackend_t::~AdobeAcrobatVBufBackend_t() {
}

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID, VBufStorage_buffer_t* storageBuffer) {
	VBufBackend_t* backend=new AdobeAcrobatVBufBackend_t(docHandle,ID,storageBuffer);
	DEBUG_MSG(L"Created new backend at "<<backend);
	return backend;
}
