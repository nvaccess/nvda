/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2011 NV Access Inc
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
#include <common/log.h>
#include <vbufBase/backend.h>
#include "webKit.h"

using namespace std;

const UINT WM_LRESULT_FROM_IACCESSIBLE = RegisterWindowMessage(L"VBufBackend_lresultFromIAccessible");
const UINT WM_IACCESSIBLE_FROM_CHILDID = RegisterWindowMessage(L"VBufBackend_IAccessibleFromChildID");

IAccessible* IAccessibleFromIdentifier(int docHandle, int ID) {
	// We want to bypass oleacc proxying,
	// so retrieve the IAccessible directly rather than using AccessibleObjectFromEvent.
	LRESULT lres;
	if (!(lres = SendMessage((HWND)docHandle, WM_GETOBJECT, 0, OBJID_CLIENT)))
		return NULL;
	IAccessible* root = NULL;
	if (ObjectFromLresult(lres, IID_IAccessible, 0, (void**)&root) != S_OK)
		return NULL;
	VARIANT varChild;
	varChild.vt = VT_I4;
	varChild.lVal = ID;
	IDispatch* childDisp;
	HRESULT hres = root->get_accChild(varChild, &childDisp);
	root->Release();
	if (hres != S_OK)
		return NULL;
	IAccessible* childAcc;
	hres = childDisp->QueryInterface(IID_IAccessible, (void**)&childAcc);
	childDisp->Release();
	if (hres != S_OK)
		return NULL;
	return childAcc;
}

class WebKitVBufStorage_controlFieldNode_t: public VBufStorage_controlFieldNode_t {
	public:
	WebKitVBufStorage_controlFieldNode_t(int docHandle, int ID, bool isBlock, IAccessible* accessibleObj, WebKitVBufBackend_t* backend): VBufStorage_controlFieldNode_t(docHandle, ID, isBlock) {
		this->accessibleObj = accessibleObj;
		this->backend = backend;
		backend->accessiblesToNodes[accessibleObj] = this;
	}

	~WebKitVBufStorage_controlFieldNode_t() {
		if (accessibleObj) {
			backend->accessiblesToNodes.erase(accessibleObj);
			accessibleObj->Release();
		}
	}

	protected:
	IAccessible* accessibleObj;
	WebKitVBufBackend_t* backend;
	friend class WebKitVBufBackend_t;
};

VBufStorage_fieldNode_t* WebKitVBufBackend_t::fillVBuf(int docHandle, IAccessible* pacc, VBufStorage_buffer_t* buffer,
	VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode
) {
	nhAssert(buffer);

	//all IAccessible methods take a variant for childID, get one ready
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=0;

	// Get role with accRole
	VARIANT varRole;
	VariantInit(&varRole);
	pacc->get_accRole(varChild, &varRole);

	if (varRole.vt == VT_I4 && varRole.lVal == ROLE_SYSTEM_COLUMN) {
		// WebKit provides both row and column representations for tables,
		// duplicating the table cells.
		// We never want the column representation.
		return NULL;
	}
	// varRole is still needed. It will be cleaned up later.

	int id = ++idCounter;
	//Make sure that we don't already know about this object -- protect from loops
	if(buffer->getControlFieldNodeWithIdentifier(docHandle,id)!=NULL) {
		VariantClear(&varRole);
		pacc->Release();
		return NULL;
	}

	//Add this node to the buffer
	parentNode = buffer->addControlFieldNode(parentNode, previousNode, 
		new WebKitVBufStorage_controlFieldNode_t(docHandle, id, true, pacc, this));
	nhAssert(parentNode); //new node must have been created
	previousNode=NULL;
	VBufStorage_fieldNode_t* tempNode;

	wostringstream s;

	long role = 0;
	if(varRole.vt==VT_EMPTY) {
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
	if(pacc->get_accState(varChild,&varState)!=S_OK) {
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
	if (role == ROLE_SYSTEM_COMBOBOX
		|| (role == ROLE_SYSTEM_LIST && !(states & STATE_SYSTEM_READONLY))
		// Editable text fields sometimes have children with no content.
		|| (role == ROLE_SYSTEM_TEXT && states & STATE_SYSTEM_FOCUSABLE)
	) {
		// We don't want this node's children.
		childCount=0;
	} else
		pacc->get_accChildCount(&childCount);

	// Iterate through the children.
	if (childCount > 0) {
		VARIANT* varChildren;
		if((varChildren=(VARIANT*)malloc(sizeof(VARIANT)*childCount))==NULL) {
			return NULL;
		}
		if(AccessibleChildren(pacc,0,childCount,varChildren,(long*)(&childCount))!=S_OK) {
			childCount=0;
		}
		for(int i=0;i<childCount;i++) {
			if(varChildren[i].vt==VT_DISPATCH) {
				IAccessible* childPacc=NULL;
				if(varChildren[i].pdispVal->QueryInterface(IID_IAccessible,(void**)(&childPacc))!=S_OK) {
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

		// No children, so fetch content from this leaf node.
		BSTR tempBstr = NULL;
		wstring content;

		if ((role != ROLE_SYSTEM_TEXT || !(states & STATE_SYSTEM_FOCUSABLE)) && role != ROLE_SYSTEM_COMBOBOX
				&& pacc->get_accName(varChild, &tempBstr) == S_OK && tempBstr) {
			content = tempBstr;
			SysFreeString(tempBstr);
		} 
		if (content.empty()&&pacc->get_accValue(varChild, &tempBstr) == S_OK && tempBstr) {
			content = tempBstr;
			SysFreeString(tempBstr);
		}
		if (content.empty()&&pacc->get_accDescription(varChild, &tempBstr) == S_OK && tempBstr) {
			if(wcsncmp(tempBstr,L"Description: ",13)==0) {
				content=&tempBstr[13];
			}
			SysFreeString(tempBstr);
		}
		if (content.empty() && states & STATE_SYSTEM_FOCUSABLE) {
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

void CALLBACK WebKitVBufBackend_t::renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	switch (eventID) {
		case EVENT_OBJECT_VALUECHANGE:
		case EVENT_OBJECT_STATECHANGE:
			break;
		default:
			return;
	}

	WebKitVBufBackend_t* backend = NULL;
	for (VBufBackendSet_t::iterator it = runningBackends.begin(); it != runningBackends.end(); ++it) {
		HWND rootWindow = (HWND)(*it)->rootDocHandle;
		if (hwnd == rootWindow || IsChild(rootWindow, hwnd)) {
			backend = static_cast<WebKitVBufBackend_t*>(*it);
			break;
		}
	}
	if (!backend)
		return;

	IAccessible* acc = IAccessibleFromIdentifier((int)hwnd, childID);
	if (!acc)
		return;
	acc->Release();
	map<IAccessible*, WebKitVBufStorage_controlFieldNode_t*>::const_iterator it;
	if ((it = backend->accessiblesToNodes.find(acc)) == backend->accessiblesToNodes.end())
		return;
	backend->invalidateSubtree(it->second);
}

void WebKitVBufBackend_t::renderThread_initialize() {
	registerWinEventHook(renderThread_winEventProcHook);
	VBufBackend_t::renderThread_initialize();
}

void WebKitVBufBackend_t::renderThread_terminate() {
	unregisterWinEventHook(renderThread_winEventProcHook);
	VBufBackend_t::renderThread_terminate();
}

void WebKitVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode) {
	IAccessible* pacc = NULL;
	if (oldNode) {
		pacc = static_cast<WebKitVBufStorage_controlFieldNode_t*>(oldNode)->accessibleObj;
		// This accessible will now be used by a new node,
		// so make sure the old node doesn't clean it up.
		static_cast<WebKitVBufStorage_controlFieldNode_t*>(oldNode)->accessibleObj = NULL;
	} else
		pacc = IAccessibleFromIdentifier(docHandle,ID);
	nhAssert(pacc); //must get a valid IAccessible object
	this->fillVBuf(docHandle, pacc, buffer, NULL, NULL);
	// pacc will be released later.
}

WebKitVBufBackend_t::WebKitVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID), idCounter(-1) {
}

LRESULT CALLBACK callWndProcHook(int code, WPARAM wParam,LPARAM lParam) {
	CWPSTRUCT* pcwp = (CWPSTRUCT*)lParam;
	if (pcwp->message == WM_LRESULT_FROM_IACCESSIBLE) {
		*(LRESULT*)pcwp->lParam = LresultFromObject(IID_IAccessible, 0,
			(IUnknown*)pcwp->wParam);
	} else if (pcwp->message == WM_IACCESSIBLE_FROM_CHILDID) {
		IAccessible* acc = IAccessibleFromIdentifier((int)pcwp->hwnd, (int)pcwp->wParam);
		if (acc) {
			acc->Release();
		}
		*(IAccessible**) pcwp->lParam = acc;
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
	// LResultFromObject always returns a 32 bit value.
	return (int)res;
}

VBufStorage_controlFieldNode_t* WebKitVBufBackend_t::getNodeForNativeHandle(int nativeHandle) {
	IAccessible* acc;
	// This method will be called in an RPC thread.
	// IAccessibleFromIdentifier must be called in the thread in which the object was created.
	registerWindowsHook(WH_CALLWNDPROC, callWndProcHook);
	SendMessage((HWND)rootDocHandle, WM_IACCESSIBLE_FROM_CHILDID,
		(WPARAM)nativeHandle, (LPARAM)&acc);
	unregisterWindowsHook(WH_CALLWNDPROC, callWndProcHook);
	if (!acc)
		return NULL;
	map<IAccessible*, WebKitVBufStorage_controlFieldNode_t*>::const_iterator it;
	if ((it = accessiblesToNodes.find(acc)) == accessiblesToNodes.end())
		return NULL;
	return it->second;
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
