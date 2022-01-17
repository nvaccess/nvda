/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2011-2016 NV Access Limited
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
#include <atlcomcli.h>
#include <oleacc.h>
#include <ia2.h>
#include <remote/nvdaHelperRemote.h>
#include <common/log.h>
#include <common/ia2utils.h>
#include <vbufBase/backend.h>
#include "webKit.h"

using namespace std;

CComPtr<IAccessible2> IAccessible2FromIdentifier(int docHandle, int id) {
	CComPtr<IAccessible> acc = nullptr;
	CComVariant varChild;
	// WebKit returns a positive value for uniqueID,
	// but we need to pass a negative value when retrieving objects.
	id = -id;
	if (AccessibleObjectFromEvent((HWND)UlongToHandle(docHandle), OBJID_CLIENT, id, &acc, &varChild) != S_OK) {
		return nullptr;
	}
	if (varChild.lVal != CHILDID_SELF) {
		// IAccessible2 can't be implemented on a simple child,
		// so this object is invalid.
		return nullptr;
	}
	CComQIPtr<IServiceProvider> serv = acc;
	if (!serv) {
		return nullptr;
	}
	CComPtr<IAccessible2> pacc2;
	serv->QueryService(IID_IAccessible, IID_IAccessible2, (void**)&pacc2);
	return pacc2;
}

VBufStorage_fieldNode_t* WebKitVBufBackend_t::fillVBuf(int docHandle, IAccessible2* pacc, VBufStorage_buffer_t* buffer,
	VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode
) {
	nhAssert(buffer);

	//all IAccessible methods take a variant for childID, get one ready
	CComVariant varChild(CHILDID_SELF);

	// Get role with accRole
	CComVariant varRole;
	pacc->get_accRole(varChild, &varRole);

	if (varRole.vt == VT_I4 && varRole.lVal == ROLE_SYSTEM_COLUMN) {
		// WebKit provides both row and column representations for tables,
		// duplicating the table cells.
		// We never want the column representation.
		return NULL;
	}

	int id;
	if(pacc->get_uniqueID((long*)&id) != S_OK)
		return NULL;

	//Make sure that we don't already know about this object -- protect from loops
	if(buffer->getControlFieldNodeWithIdentifier(docHandle,id)!=NULL) {
		return NULL;
	}

	//Add this node to the buffer
	parentNode = buffer->addControlFieldNode(parentNode, previousNode,
		docHandle, id, true);
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

	// Get states with accState
	CComVariant varState;
	pacc->get_accState(varChild,&varState);
	int states=varState.lVal;
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
		auto [varChildren, accChildrenRes] = getAccessibleChildren(pacc, 0, childCount);
		if (S_OK == accChildrenRes) {
			for (CComVariant& child : varChildren) {
				if (VT_DISPATCH != child.vt) {
					continue;
				}
				CComQIPtr<IAccessible2> childPacc(child.pdispVal);
				if (!childPacc) {
					continue;
				}
				if ((tempNode = this->fillVBuf(docHandle, childPacc, buffer, parentNode, previousNode)) != NULL) {
					previousNode = tempNode;
				}
			}
		}
	} else {

		// No children, so fetch content from this leaf node.
		CComBSTR tempBstr;
		wstring content;

		if ((role != ROLE_SYSTEM_TEXT || !(states & STATE_SYSTEM_FOCUSABLE)) && role != ROLE_SYSTEM_COMBOBOX
				&& pacc->get_accName(varChild, &tempBstr) == S_OK && tempBstr) {
			content = tempBstr;
		} 
		tempBstr.Empty();
		if (content.empty()&&pacc->get_accValue(varChild, &tempBstr) == S_OK && tempBstr) {
			content = tempBstr;
		}
		tempBstr.Empty();
		if (content.empty()&&pacc->get_accDescription(varChild, &tempBstr) == S_OK && tempBstr) {
			if(wcsncmp(tempBstr,L"Description: ",13)==0) {
				content=&tempBstr[13];
			}
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
		case EVENT_OBJECT_REORDER:
			break;
		default:
			return;
	}

	WebKitVBufBackend_t* backend = NULL;
	for (VBufBackendSet_t::iterator it = runningBackends.begin(); it != runningBackends.end(); ++it) {
		HWND rootWindow = (HWND)UlongToHandle((*it)->rootDocHandle);
		if (hwnd == rootWindow || IsChild(rootWindow, hwnd)) {
			backend = static_cast<WebKitVBufBackend_t*>(*it);
			break;
		}
	}
	if (!backend)
		return;
	int docHandle = HandleToUlong(hwnd);
	// WebKit returns positive values for uniqueID, but fires events with negative ids.
	// Therefore, flip the sign on childID.
	VBufStorage_controlFieldNode_t* node = backend->getControlFieldNodeWithIdentifier(docHandle, -childID);
	if (!node)
		return;
	backend->invalidateSubtree(node);
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
	CComPtr<IAccessible2> pacc = IAccessible2FromIdentifier(docHandle,ID);
	nhAssert(pacc); //must get a valid IAccessible object
	this->fillVBuf(docHandle, pacc, buffer, NULL, NULL);
}

WebKitVBufBackend_t::WebKitVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID) {
}

VBufBackend_t* WebKitVBufBackend_t_createInstance(int docHandle, int ID) {
	VBufBackend_t* backend=new WebKitVBufBackend_t(docHandle,ID);
	return backend;
}
