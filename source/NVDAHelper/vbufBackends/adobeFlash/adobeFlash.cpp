#include <sstream>
#include <cassert>
#include <map>
#include <windows.h>
#include <oleacc.h>
#include <remote/nvdaHelperRemote.h>
#include <vbufBase/backend.h>
#include "adobeFlash.h"

using namespace std;

void AdobeFlashVBufBackend_t::renderThread_initialize() {
	registerWinEventHook(renderThread_winEventProcHook);
	VBufBackend_t::renderThread_initialize();
}

void AdobeFlashVBufBackend_t::renderThread_terminate() {
	unregisterWinEventHook(renderThread_winEventProcHook);
	VBufBackend_t::renderThread_terminate();
}

void CALLBACK AdobeFlashVBufBackend_t::renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	switch(eventID) {
		case EVENT_OBJECT_REORDER:
		case EVENT_OBJECT_NAMECHANGE:
		case EVENT_OBJECT_VALUECHANGE:
		case EVENT_OBJECT_STATECHANGE:
		break;
		default:
		return;
	}

	int docHandle=(int)hwnd;
	int ID=childID;
	VBufBackend_t* backend=NULL;
	for(VBufBackendSet_t::iterator i=runningBackends.begin();i!=runningBackends.end();i++) {
		HWND rootWindow=(HWND)((*i)->rootDocHandle);
		if(rootWindow==hwnd) {
			backend=(*i);
		}
	}
	if(!backend) {
		return;
	}
	VBufStorage_controlFieldNode_t* node=backend->getControlFieldNodeWithIdentifier(docHandle,ID);
	if(!node) {
		return;
	}
	backend->invalidateSubtree(node);
}

VBufStorage_fieldNode_t* AdobeFlashVBufBackend_t::renderControlContent(VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode, int docHandle, IAccessible* pacc, long accChildID) {
	assert(buffer);

	int res;
	//all IAccessible methods take a variant for childID, get one ready
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=accChildID;

VBufStorage_fieldNode_t* tempNode=NULL;

int id=accChildID;

	//Make sure that we don't already know about this object -- protect from loops
	if(buffer->getControlFieldNodeWithIdentifier(docHandle,id)!=NULL) {
		return NULL;
	}

	//Add this node to the buffer
	parentNode=buffer->addControlFieldNode(parentNode,previousNode,docHandle,id,TRUE);
	assert(parentNode); //new node must have been created
	previousNode=NULL;

	wostringstream s;

	// Get role with accRole
	long role = 0;
	VARIANT varRole;
	VariantInit(&varRole);
	if((res=pacc->get_accRole(varChild,&varRole))!=S_OK) {
		s<<0;
	} else if(varRole.vt==VT_BSTR) {
		s << varRole.bstrVal;
	} else if(varRole.vt==VT_I4) {
		s << varRole.lVal;
		role = varRole.lVal;
	}
	parentNode->addAttribute(L"IAccessible::role",s.str());
	VariantClear(&varRole);

	// Get states with accState
	VARIANT varState;
	VariantInit(&varState);
	if((res=pacc->get_accState(varChild,&varState))!=S_OK) {
		varState.vt=VT_I4;
		varState.lVal=0;
	}
	int states=varState.lVal;
	VariantClear(&varState);
	//Add each state that is on, as an attrib
	for(int i=0;i<32;i++) {
		int state=1<<i;
		if(state&states) {
			s.str(L"");
			s<<L"IAccessible::state_"<<state;
			parentNode->addAttribute(s.str(),L"1");
		}
	}

	BSTR tempBstr=NULL;
	wstring name;
	wstring value;
	wstring content;

	if ((res = pacc->get_accName(varChild, &tempBstr)) == S_OK) {
		name = tempBstr;
		SysFreeString(tempBstr);
	}
	if ((res = pacc->get_accValue(varChild, &tempBstr)) == S_OK) {
		value = tempBstr;
		SysFreeString(tempBstr);
	}
	if(!value.empty()) {
		content=value;
	} else if(role!=ROLE_SYSTEM_TEXT&&!name.empty()) {
		content=name;
	} else if (states & STATE_SYSTEM_FOCUSABLE) {
		// This node is focusable, but contains no text.
		// Therefore, add it with a space so that the user can get to it.
		content = L" ";
	}

	if (!content.empty()) {
		if (tempNode = buffer->addTextFieldNode(parentNode, previousNode, content)) {
			previousNode=tempNode;
		}
	}

	return parentNode;
}

void AdobeFlashVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode) {
	DWORD res=0;
	//Get an IAccessible by sending WM_GETOBJECT directly to bypass any proxying, to speed things up.
	if(SendMessageTimeout((HWND)docHandle,WM_GETOBJECT,0,OBJID_CLIENT,SMTO_ABORTIFHUNG,2000,&res)==0||res==0) {
		//Failed to send message or window does not support IAccessible
		return;
	}
	IAccessible* pacc=NULL;
	if(ObjectFromLresult(res,IID_IAccessible,0,(void**)&pacc)!=S_OK) {
		//Could not get the IAccessible pointer from the WM_GETOBJECT result
		return;
	}
	assert(pacc); //must get a valid IAccessible object
	if(ID==0) {
		VBufStorage_controlFieldNode_t* parentNode=buffer->addControlFieldNode(NULL,NULL,docHandle,ID,TRUE);
		parentNode->addAttribute(L"IAccessible::role",L"10");
		VBufStorage_fieldNode_t* previousNode=NULL;
		long childCount=0;
		pacc->get_accChildCount(&childCount);
		map<pair<pair<long,long>,long>,long> childIDsByLocation;
		VARIANT varChild;
		varChild.vt=VT_I4;
		HRESULT hRes;
		for(int i=1;i<1000&&childIDsByLocation.size()<childCount;++i) {
			IDispatch* childDisp=NULL;
			varChild.lVal=i;
			hRes=pacc->get_accChild(varChild,&childDisp);
			if(hRes==S_OK) {
				childDisp->Release();
				long left=0, top=0, width=0, height=0;
				if(pacc->accLocation(&left,&top,&width,&height,varChild)!=S_OK) {
					left=top=width=height=0;
				}
				childIDsByLocation[make_pair(make_pair(top+(height/2),left+(width/2)),i)]=i;
			}
		} 
		for(map<pair<pair<long,long>,long>,long>::iterator i=childIDsByLocation.begin();i!=childIDsByLocation.end();++i) {
			previousNode=this->renderControlContent(buffer,parentNode,previousNode,docHandle,pacc,i->second);
		}
	} else {
		this->renderControlContent(buffer,NULL,NULL,docHandle,pacc,ID);
	}
	pacc->Release();
}

AdobeFlashVBufBackend_t::AdobeFlashVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID) {
}

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID) {
	VBufBackend_t* backend=new AdobeFlashVBufBackend_t(docHandle,ID);
	return backend;
}
