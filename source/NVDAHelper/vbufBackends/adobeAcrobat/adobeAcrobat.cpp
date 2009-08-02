/**
 * backends/adobeAcrobat/adobeAcrobat.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007-2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#define UNICODE
 #include <set>
 #include <sstream>
 #include <cassert>
#include <windows.h>
#include <oleacc.h>
#include <AcrobatAccess/AcrobatAccess.h>
#include <vbufBase/backend.h>
#include <vbufBase/debug.h>
#include "adobeAcrobat.h"

using namespace std;

typedef std::set<VBufBackend_t*> VBufBackendSet_t;

HINSTANCE backendLibHandle=NULL;
UINT wmMainThreadSetup=0;
UINT wmMainThreadTerminate=0;
VBufBackendSet_t backends;
HWINEVENTHOOK winEventHookID;
UINT_PTR mainThreadTimerID=0;

#pragma comment(linker,"/entry:_DllMainCRTStartup@12")
BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		backendLibHandle=hModule;
		wmMainThreadSetup=RegisterWindowMessage(L"VBufBackend_adobeAcrobat_mainThreadSetup");
		wmMainThreadTerminate=RegisterWindowMessage(L"VBufBackend_adobeAcrobat_mainThreadTerminate");
		DEBUG_MSG(L"wmMainThreadSetup message: "<<wmMainThreadSetup<<L", wmMainThreadTerminate message: "<<wmMainThreadTerminate);
	}
	return TRUE;
}

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

long getAccID(IServiceProvider* servprov) {
	int res;
	IAccID* paccID = NULL;
	long ID;

	DEBUG_MSG(L"calling IServiceProvider::QueryService for IAccID");
	if((res=servprov->QueryService(SID_AccID,IID_IAccID,(void**)(&paccID)))!=S_OK) {
		DEBUG_MSG(L"IServiceProvider::QueryService returned "<<res);
		return 0;
	} 
	DEBUG_MSG(L"IAccID at "<<paccID);

	DEBUG_MSG(L"Calling get_accID");
	if((res=paccID->get_accID((long*)(&ID)))!=S_OK) {
		DEBUG_MSG(L"paccID->get_accID returned "<<res);
		ID = 0;
	}

	DEBUG_MSG("Releasing IAccID");
	paccID->Release();

	return ID;
}

IPDDomNode* getPDDomNode(VARIANT& varChild, IServiceProvider* servprov) {
	int res;
	IGetPDDomNode* pget = NULL;
	IPDDomNode* domNode = NULL;

	DEBUG_MSG(L"calling IServiceProvider::QueryService for IGetPDDomNode");
	if((res=servprov->QueryService(SID_GetPDDomNode,IID_IGetPDDomNode,(void**)(&pget)))!=S_OK) {
		DEBUG_MSG(L"IServiceProvider::QueryService returned "<<res);
		return NULL;
	} 
	DEBUG_MSG(L"IGetPDDomNode at "<<pget);

	DEBUG_MSG(L"Calling get_PDDomNode");
	if((res=pget->get_PDDomNode(varChild, &domNode))!=S_OK) {
		DEBUG_MSG(L"pget->get_PDDomNode returned "<<res);
		domNode = NULL;
	}

	DEBUG_MSG("Releasing IGetPDDomNode");
	pget->Release();

	return domNode;
}

VBufStorage_fieldNode_t* fillVBuf(int docHandle, IAccessible* pacc, VBufStorage_buffer_t* buffer,
	VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode,
	int indexInParent=0, long tableID=0, int rowNumber=0
) {
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

	IServiceProvider* servprov = NULL;
	DEBUG_MSG(L"calling IAccessible::QueryInterface with IID_IServiceProvider");
	if((res=pacc->QueryInterface(IID_IServiceProvider,(void**)(&servprov)))!=S_OK) {
		DEBUG_MSG(L"IAccessible::QueryInterface returned "<<res);
		return NULL;
	}  
	DEBUG_MSG(L"IServiceProvider at "<<servprov);

	// GET ID
	int ID = getAccID(servprov);
	assert(ID);

	//Make sure that we don't already know about this object -- protect from loops
	if(buffer->getControlFieldNodeWithIdentifier(docHandle,ID)!=NULL) {
		DEBUG_MSG(L"A node with this docHandle and ID already exists, returning NULL");
		servprov->Release();
		return NULL;
	}

	//Add this node to the buffer
	DEBUG_MSG(L"Adding Node to buffer");
	parentNode=buffer->addControlFieldNode(parentNode,previousNode,docHandle,ID,TRUE);
	assert(parentNode); //new node must have been created
	previousNode=NULL;
	DEBUG_MSG(L"Added  node at "<<parentNode);

	// Get role with accRole
	long role = 0;
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
			role = varRole.lVal;
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

	IPDDomNode* domNode = getPDDomNode(varChild, servprov);

	IPDDomElement* domElement = NULL;
	DEBUG_MSG(L"Trying to get IPDDomElement");
	if (domNode && (res = domNode->QueryInterface(IID_IPDDomElement, (void**)(&domElement))) != S_OK) {
		DEBUG_MSG(L"QueryInterface to IPDDomElement returned " << res);
		domElement = NULL;
	}

	// Get stdName.
	if (domElement) {
		BSTR stdName;
		if ((res = domElement->GetStdName(&stdName)) != S_OK) {
			DEBUG_MSG(L"IPDDomElement::GetStdName returned " << res);
			stdName = NULL;
		}
		if (stdName) {
			parentNode->addAttribute(L"acrobat::stdname", stdName);
			SysFreeString(stdName);
			stdName = NULL;
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

	// Handle table information.
	if (role == ROLE_SYSTEM_TABLE) {
		DEBUG_MSG(L"This is a table, adding table-id attribute");
		wostringstream s;
		s << ID;
		parentNode->addAttribute(L"table-id", s.str());
		tableID = ID;
	} else if (role == ROLE_SYSTEM_ROW) {
		DEBUG_MSG(L"This is a table row, setting rowNumber");
		rowNumber = indexInParent + 1;
	} else if (role == ROLE_SYSTEM_CELL || role == ROLE_SYSTEM_COLUMNHEADER) {
		DEBUG_MSG(L"This is a table cell, adding attributes");
		wostringstream s;
		s << tableID;
		parentNode->addAttribute(L"table-id", s.str());
		s.str(L"");
		s << ((role == ROLE_SYSTEM_COLUMNHEADER) ? 0 : rowNumber);
		parentNode->addAttribute(L"table-rownumber", s.str());
		s.str(L"");
		// The parent is a row, so indexInParent is the column number.
		s << indexInParent + 1;
		parentNode->addAttribute(L"table-columnnumber", s.str());
	}

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
				IAccessible* childPacc=NULL;
				if((res=varChildren[i].pdispVal->QueryInterface(IID_IAccessible,(void**)(&childPacc)))!=S_OK) {
					DEBUG_MSG(L"varChildren["<<i<<L"].pdispVal->QueryInterface to IID_iAccessible returned "<<res);
					childPacc=NULL;
				}
				if(childPacc) {
					DEBUG_MSG(L"calling filVBuf with child object ");
					if((tempNode=fillVBuf(docHandle,childPacc,buffer,parentNode,previousNode,i,tableID,rowNumber))!=NULL) {
						previousNode=tempNode;
					} else {
						DEBUG_MSG(L"Error in calling fillVBuf");
					}
					DEBUG_MSG(L"releasing child IAccessible object");
					childPacc->Release();
				}
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

		// Where accValue isn't useful, use the name instead.
		if(!value && (res=pacc->get_accName(varChild,&value))!=S_OK) {
			DEBUG_MSG(L"IAccessible::get_accName returned "<<res);
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
			SysFreeString(value);
			value = NULL;
		} else if (STATE_SYSTEM_FOCUSABLE & states) {
			// This node is focusable, but contains no text.
			// Therefore, add it with a space so that the user can get to it.
			if((tempNode=buffer->addTextFieldNode(parentNode,previousNode,L" "))!=NULL) {
				previousNode=tempNode;
			}
		}
	}

	if (domElement) {
		DEBUG_MSG(L"Releasing IPDDomElement");
		domElement->Release();
	}
	if (domNode) {
		DEBUG_MSG(L"Releasing IPDDomNode");
		domNode->Release();
	}
	DEBUG_MSG(L"Releasing IServiceProvider");
	servprov->Release();

	DEBUG_MSG(L"Returning node at "<<parentNode);
	return parentNode;
}

void CALLBACK mainThreadTimerProc(HWND hwnd, UINT msg, UINT_PTR timerID, DWORD time) {
	KillTimer(0,mainThreadTimerID);
	mainThreadTimerID=0;
	DEBUG_MSG(L"Updating "<<backends.size()<<L" backends");
	for(VBufBackendSet_t::iterator i=backends.begin();i!=backends.end();i++) {
		DEBUG_MSG(L"Updating backend at "<<(*i));
		(*i)->update();
	}
	DEBUG_MSG(L"All updated");
}

void CALLBACK mainThreadWinEventCallback(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	if (eventID != EVENT_OBJECT_STATECHANGE && eventID != EVENT_OBJECT_VALUECHANGE)
		return;
	if (eventID == EVENT_OBJECT_VALUECHANGE && childID == CHILDID_SELF) {
		// This indicates that a new document or page replaces this one.
		// The client will ditch this buffer and create a new one, so there's no point rendering it here.
		return;
	}

	DEBUG_MSG(L"winEvent for window "<<hwnd);

	int docHandle=(int)hwnd;
	int ID=childID;
	VBufBackend_t* backend=NULL;
	DEBUG_MSG(L"Searching for backend in collection of "<<backends.size()<<L" running backends");
	for(VBufBackendSet_t::iterator i=backends.begin();i!=backends.end();i++) {
		HWND rootWindow=(HWND)((*i)->getRootDocHandle());
		DEBUG_MSG(L"Comparing backend's root window "<<rootWindow<<L" with window "<<hwnd);
		if(rootWindow==hwnd) {
			backend=(*i);
		}
	}
	if(!backend) {
		DEBUG_MSG(L"No matching backend found");
		return;
	}
	DEBUG_MSG(L"found active backend for this window at "<<backend);

	VBufStorage_buffer_t* buffer=backend;
	VBufStorage_controlFieldNode_t* node=buffer->getControlFieldNodeWithIdentifier(docHandle,ID);
	if(!node) {
		DEBUG_MSG(L"No nodes to use, returning");
		return;
	}

	backend->invalidateSubtree(node);

	if(mainThreadTimerID==0) {
		mainThreadTimerID=SetTimer(0,0,250,mainThreadTimerProc);
		DEBUG_MSG(L"Set timer for update with ID of "<<mainThreadTimerID);
	}
}

void mainThreadSetup(VBufBackend_t* backend) {
	if (!winEventHookID && backends.size() > 0) {
		int processID=GetCurrentProcessId();
		int threadID=GetCurrentThreadId();
		DEBUG_MSG(L"process ID "<<processID<<L", thread ID "<<threadID);
		DEBUG_MSG(L"Registering win event callback");
		winEventHookID=SetWinEventHook(EVENT_MIN,0xffffffff,backendLibHandle,(WINEVENTPROC)mainThreadWinEventCallback,processID,threadID,WINEVENT_INCONTEXT);
		assert(winEventHookID!=0); //winEventHookID must be non-0
		DEBUG_MSG(L"Registered win event callback, with ID "<<winEventHookID);
	}
	backend->update();
	#ifdef DEBUG
	Beep(220,70);
	#endif
}

LRESULT CALLBACK mainThreadCallWndProcHook(int code, WPARAM wParam,LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if((code==HC_ACTION)&&(pcwp->message==wmMainThreadSetup)) {
		mainThreadSetup((VBufBackend_t*)(pcwp->wParam));
	}
	return CallNextHookEx(0,code,wParam,lParam);
}

void mainThreadTerminate(VBufBackend_t* backend) {
	if (winEventHookID && backends.size() == 0) {
		DEBUG_MSG(L"No backends, unhooking winEvent");
		UnhookWinEvent(winEventHookID);
		winEventHookID = 0;
	}
	if (mainThreadTimerID) {
		KillTimer(0, mainThreadTimerID);
	}
	#ifdef DEBUG
	Beep(880,70);
	#endif
}

LRESULT CALLBACK mainThreadGetMessageHook(int code, WPARAM wParam,LPARAM lParam) {
	MSG* pmsg=(MSG*)lParam;
	if((code==HC_ACTION)&&(pmsg->message==wmMainThreadTerminate)) {
		mainThreadTerminate((VBufBackend_t*)(pmsg->wParam));
		DEBUG_MSG(L"Removing hook");
		int res=UnhookWindowsHookEx((HHOOK)(pmsg->lParam));
		assert(res!=0); //unHookWindowsHookEx must return non-0
	}
	return CallNextHookEx(0,code,wParam,lParam);
}

void AdobeAcrobatVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode) {
	DEBUG_MSG(L"Rendering from docHandle "<<docHandle<<L", ID "<<ID<<L", in to buffer at "<<buffer);
	IAccessible* pacc=IAccessibleFromIdentifier(docHandle,ID);
	assert(pacc); //must get a valid IAccessible object
	fillVBuf(docHandle,pacc,buffer,NULL,NULL);
	pacc->Release();
	DEBUG_MSG(L"Rendering done");
}

AdobeAcrobatVBufBackend_t::AdobeAcrobatVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID) {
	int res;
	DEBUG_MSG(L"Initializing Adobe Acrobat backend");
	backends.insert(this);
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
	DEBUG_MSG(L"Adobe Acrobat backend initialized");
}

AdobeAcrobatVBufBackend_t::~AdobeAcrobatVBufBackend_t() {
	int res;
	DEBUG_MSG(L"adobeAcrobat backend being destroied");
	backends.erase(this);
	DEBUG_MSG(L"Setting hook");
	HHOOK mainThreadGetMessageHookID=SetWindowsHookEx(WH_GETMESSAGE,(HOOKPROC)mainThreadGetMessageHook,backendLibHandle,rootThreadID);
	assert(mainThreadGetMessageHookID!=0); //valid hooks are not 0
	DEBUG_MSG(L"Hook set with ID "<<mainThreadGetMessageHookID);
	DEBUG_MSG(L"Sending wmMainThreadTerminate to thread "<<rootThreadID<<", docHandle "<<rootDocHandle<<L", ID "<<rootID<<L", backend "<<this);
	PostThreadMessage(rootThreadID,wmMainThreadTerminate,(WPARAM)this,(LPARAM)mainThreadGetMessageHookID);
	DEBUG_MSG(L"Message sent");
	DEBUG_MSG(L"Adobe Acrobat backend terminated");
}

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID) {
	VBufBackend_t* backend=new AdobeAcrobatVBufBackend_t(docHandle,ID);
	DEBUG_MSG(L"Created new backend at "<<backend);
	return backend;
}
