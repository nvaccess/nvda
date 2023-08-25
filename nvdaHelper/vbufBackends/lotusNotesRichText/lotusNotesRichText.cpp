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
#include <map>
#include <windows.h>
#include <oleacc.h>
#include <common/log.h>
#include <common/ia2utils.h>
#include <remote/nvdaHelperRemote.h>
#include <vbufBase/backend.h>
#include "lotusNotesRichText.h"

using namespace std;

void lotusNotesRichTextVBufBackend_t::renderThread_initialize() {
	registerWinEventHook(renderThread_winEventProcHook);
	VBufBackend_t::renderThread_initialize();
}

void lotusNotesRichTextVBufBackend_t::renderThread_terminate() {
	unregisterWinEventHook(renderThread_winEventProcHook);
	VBufBackend_t::renderThread_terminate();
}

void CALLBACK lotusNotesRichTextVBufBackend_t::renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	switch(eventID) {
		case EVENT_OBJECT_REORDER:
		case EVENT_OBJECT_NAMECHANGE:
		case EVENT_OBJECT_VALUECHANGE:
		case EVENT_OBJECT_STATECHANGE:
		break;
		default:
		return;
	}

	int docHandle=HandleToUlong(hwnd);
	int ID=childID;
	VBufBackend_t* backend=NULL;
	for(VBufBackendSet_t::iterator i=runningBackends.begin();i!=runningBackends.end();++i) {
		HWND rootWindow=(HWND)UlongToHandle(((*i)->rootDocHandle));
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

VBufStorage_fieldNode_t* lotusNotesRichTextVBufBackend_t::renderControlContent(VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode, int docHandle, IAccessible* pacc, long accChildID) {
	nhAssert(buffer);

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
	VARIANT varState;
	VariantInit(&varState);
	if((res=pacc->get_accState(varChild,&varState))!=S_OK) {
		varState.vt=VT_I4;
		varState.lVal=0;
	}
	int states=varState.lVal;
	VariantClear(&varState);
	//Add each state that is on, as an attrib
	for(int i=0;i<32;++i) {
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
	} else { 
		content = L" ";
	}
	if (!content.empty()) {
		if (tempNode = buffer->addTextFieldNode(parentNode, previousNode, content)) {
			previousNode=tempNode;
		}
	}

	return parentNode;
}

void lotusNotesRichTextVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode) {
	DWORD_PTR res=0;
	//Get an IAccessible by sending WM_GETOBJECT directly to bypass any proxying, to speed things up.
	if(SendMessageTimeout((HWND)UlongToHandle(docHandle),WM_GETOBJECT,0,OBJID_CLIENT,SMTO_ABORTIFHUNG,2000,&res)==0||res==0) {
		//Failed to send message or window does not support IAccessible
		return;
	}
	IAccessible* pacc=NULL;
	if(ObjectFromLresult(res,IID_IAccessible,0,(void**)&pacc)!=S_OK) {
		//Could not get the IAccessible pointer from the WM_GETOBJECT result
		return;
	}
	nhAssert(pacc); //must get a valid IAccessible object
	if(ID==0) {
		VBufStorage_controlFieldNode_t* parentNode=buffer->addControlFieldNode(NULL,NULL,docHandle,ID,TRUE);
		parentNode->addAttribute(L"IAccessible::role",L"10");
		VBufStorage_fieldNode_t* previousNode=NULL;
		long childCount=0;
		pacc->get_accChildCount(&childCount);

		auto [varChildren, hres] = getAccessibleChildren(pacc, 0, childCount);
		for(CComVariant& child : varChildren) {
			if(VT_I4 == child.vt) {
				previousNode = this->renderControlContent(
					buffer,
					parentNode,
					previousNode,
					docHandle,
					pacc,
					child.lVal
				);
			}
		}
	} else {
		this->renderControlContent(buffer,NULL,NULL,docHandle,pacc,ID);
	}
	pacc->Release();
}

lotusNotesRichTextVBufBackend_t::lotusNotesRichTextVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID) {
}

VBufBackend_t* lotusNotesRichTextVBufBackend_t_createInstance(int docHandle, int ID) {
	VBufBackend_t* backend=new lotusNotesRichTextVBufBackend_t(docHandle,ID);
	return backend;
}
