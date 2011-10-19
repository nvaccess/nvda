/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2010 NVDA contributers.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <sstream>
#include <windows.h>
#include <oleacc.h>
#include <remote/nvdaHelperRemote.h>
#include <remote/log.h>
#include <vbufBase/backend.h>
#include "webKit.h"

using namespace std;

const UINT WM_LRESULT_FROM_IACCESSIBLE = RegisterWindowMessage(L"VBufBackend_lresultFromIAccessible");

int idCounter = 0;

IAccessible* IAccessibleFromIdentifier(int docHandle, int ID) {
	int res;
	IAccessible* pacc=NULL;
	VARIANT varChild;
	if((res=AccessibleObjectFromEvent((HWND)docHandle,OBJID_CLIENT,ID,&pacc,&varChild))!=S_OK) {
		return NULL;
	}
	VariantClear(&varChild);
	return pacc;
}

class WebKitVBufStorage_controlFieldNode_t: public VBufStorage_controlFieldNode_t {
	public:
	WebKitVBufStorage_controlFieldNode_t(int docHandle, int ID, bool isBlock, IAccessible* accessibleObj): VBufStorage_controlFieldNode_t(docHandle, ID, isBlock) {
		this->accessibleObj = accessibleObj;
	}

	~WebKitVBufStorage_controlFieldNode_t() {
		this->accessibleObj->Release();
	}

	protected:
	IAccessible* accessibleObj;
	friend class WebKitVBufBackend_t;
};

VBufStorage_fieldNode_t* WebKitVBufBackend_t::fillVBuf(int docHandle, IAccessible* pacc, VBufStorage_buffer_t* buffer,
	VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode
) {
	nhAssert(buffer);

	int res;
	VBufStorage_fieldNode_t* tempNode;
	//all IAccessible methods take a variant for childID, get one ready
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=0;

	int id = ++idCounter;
	//Make sure that we don't already know about this object -- protect from loops
	if(buffer->getControlFieldNodeWithIdentifier(docHandle,id)!=NULL) {
		pacc->Release();
		return NULL;
	}

	//Add this node to the buffer
	parentNode = buffer->addControlFieldNode(parentNode, previousNode, 
		new WebKitVBufStorage_controlFieldNode_t(docHandle, id, true, pacc));
	nhAssert(parentNode); //new node must have been created
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
	varChild.lVal=0;
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

	//Get the child count
	long childCount=0;
	if((res=pacc->get_accChildCount(&childCount))!=S_OK) {
		childCount=0;
	}

	// Iterate through the children.
	if (childCount > 0) {
		VARIANT* varChildren;
		if((varChildren=(VARIANT*)malloc(sizeof(VARIANT)*childCount))==NULL) {
			return NULL;
		}
		if((res=AccessibleChildren(pacc,0,childCount,varChildren,(long*)(&childCount)))!=S_OK) {
			childCount=0;
		}
		for(int i=0;i<childCount;i++) {
			if(varChildren[i].vt==VT_DISPATCH) {
				IAccessible* childPacc=NULL;
				if((res=varChildren[i].pdispVal->QueryInterface(IID_IAccessible,(void**)(&childPacc)))!=S_OK) {
					childPacc=NULL;
				}
				if(childPacc) {
					if((tempNode=this->fillVBuf(docHandle,childPacc,buffer,parentNode,previousNode))!=NULL) {
						previousNode=tempNode;
					}
				}
			}
			VariantClear(&(varChildren[i]));
		}
		free(varChildren);
	} else {

		// No children, so this is a text leaf node.
		BSTR tempBstr = NULL;
		wstring content;

		if ((res = pacc->get_accName(varChild, &tempBstr)) == S_OK) {
			content = tempBstr;
			SysFreeString(tempBstr);
		} else if ((res = pacc->get_accValue(varChild, &tempBstr)) == S_OK) {
			content = tempBstr;
			SysFreeString(tempBstr);
		} else if (states & STATE_SYSTEM_FOCUSABLE) {
			// This node is focusable, but contains no text.
			// Therefore, add it with a space so that the user can get to it.
			content = L" ";
		}

		if (!content.empty()) {
			if (tempNode = buffer->addTextFieldNode(parentNode, previousNode, content))
				previousNode=tempNode;
		}
	}

	return parentNode;
}

void WebKitVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode) {
	IAccessible* pacc=IAccessibleFromIdentifier(docHandle,ID);
	nhAssert(pacc); //must get a valid IAccessible object
	this->fillVBuf(docHandle,pacc,buffer,NULL,NULL);
}

WebKitVBufBackend_t::WebKitVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID) {
}

LRESULT CALLBACK callWndProcHook(int code, WPARAM wParam,LPARAM lParam) {
	CWPSTRUCT* pcwp = (CWPSTRUCT*)lParam;
	if (pcwp->message == WM_LRESULT_FROM_IACCESSIBLE) {
		*(LRESULT*)pcwp->lParam = LresultFromObject(IID_IAccessible, 0,
			(IUnknown*)pcwp->wParam);
	}
	return 0;
}

int WebKitVBufBackend_t::getNativeHandleForNode(VBufStorage_controlFieldNode_t* node) {
	if (!this->isNodeInBuffer(node))
		return 0;
	LRESULT res = 0;
	// This method will be called in an RPC thread.
		// LresultFromObject must be called in the thread in which the object was created.
	registerWindowsHook(WH_CALLWNDPROC, callWndProcHook);
	SendMessage((HWND)rootDocHandle, WM_LRESULT_FROM_IACCESSIBLE,
		(WPARAM)static_cast<WebKitVBufStorage_controlFieldNode_t*>(node)->accessibleObj, (LPARAM)&res);
	unregisterWindowsHook(WH_CALLWNDPROC, callWndProcHook);
	if (res <= 0)
		return 0;
	return res;
}

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID) {
	VBufBackend_t* backend=new WebKitVBufBackend_t(docHandle,ID);
	return backend;
}

BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		_CrtSetReportHookW2(_CRT_RPTHOOK_INSTALL,(_CRT_REPORT_HOOKW)NVDALogCrtReportHook);
	}
	return true;
}
