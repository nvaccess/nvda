/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2010-2013 NV Access Limited
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
#include <initguid.h>
#include <oleacc.h>
#include <common/log.h>
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
	if (this->accPropServices)
		this->accPropServices->Release();
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
	int ID=(childID==CHILDID_SELF&&objectID>0)?objectID:childID;
	for(VBufBackendSet_t::iterator i=runningBackends.begin();i!=runningBackends.end();++i) {
		AdobeFlashVBufBackend_t* backend=NULL;
		HWND rootWindow=(HWND)((*i)->rootDocHandle);
		if(rootWindow!=hwnd)
			continue;
		backend=static_cast<AdobeFlashVBufBackend_t*>(*i);
		VBufStorage_controlFieldNode_t* node=backend->getControlFieldNodeWithIdentifier(docHandle,ID);
		if(node)
			backend->invalidateSubtree(node);
		if(!backend->isWindowless) {
			// If this is not windowless, there can only be one backend with this docHandle,
			// so stop searching.
			break;
		}
	}
}

VBufStorage_fieldNode_t* AdobeFlashVBufBackend_t::renderControlContent(VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode, int docHandle, int id, IAccessible* pacc) {
	nhAssert(buffer);

	HRESULT res;
	//all IAccessible methods take a variant for childID, get one ready
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=CHILDID_SELF;

	VBufStorage_fieldNode_t* tempNode=NULL;

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

long AdobeFlashVBufBackend_t::getAccId(IAccessible* acc) {
	IAccIdentity* accId = NULL;
	if (acc->QueryInterface(IID_IAccIdentity, (void**)&accId) != S_OK || !accId)
		return -1;
	BYTE* idString=NULL;
	DWORD idLen=0;
	HRESULT res;
	res = accId->GetIdentityString(CHILDID_SELF, &idString, &idLen);
	accId->Release();
	if (res != S_OK || !idString)
		return -1;
	if (!this->accPropServices) {
		// Only retrieve this the first time it's needed.
		if (CoCreateInstance(CLSID_AccPropServices, NULL, CLSCTX_SERVER, IID_IAccPropServices, (void**)&this->accPropServices) != S_OK) {
			CoTaskMemFree(idString);
			return -1;
		}
	}
	HWND hwnd;
	DWORD objId;
	DWORD childId;
	res = this->accPropServices->DecomposeHwndIdentityString(idString, idLen, &hwnd, &objId, &childId);
	CoTaskMemFree(idString);
	if (res != S_OK)
		return -1;
	return objId;
}

void AdobeFlashVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode) {
	if (!oldNode) {
		// This is the initial render.
		WCHAR* wclass = (WCHAR*)malloc(sizeof(WCHAR) * 256);
		if (!wclass)
			return;
		if (GetClassName((HWND)docHandle, wclass, 256) == 0) {
			free(wclass);
			return;
		}
		this->isWindowless = wcscmp(wclass, L"Internet Explorer_Server") == 0;
		free(wclass);
	}

	DWORD_PTR res=0;
	//Get an IAccessible by sending WM_GETOBJECT directly to bypass any proxying, to speed things up.
	if (SendMessageTimeout((HWND)docHandle, WM_GETOBJECT, 0, isWindowless ? ID : OBJID_CLIENT, SMTO_ABORTIFHUNG, 2000, &res) == 0 || res == 0) {
		//Failed to send message or window does not support IAccessible
		return;
	}
	IAccessible* pacc=NULL;
	if(ObjectFromLresult(res,IID_IAccessible,0,(void**)&pacc)!=S_OK) {
		//Could not get the IAccessible pointer from the WM_GETOBJECT result
		return;
	}
	nhAssert(pacc); //must get a valid IAccessible object
	HRESULT hres;
	VARIANT varChild;
	varChild.vt=VT_I4;
	IAccessible* childAcc;
	if (ID != CHILDID_SELF && !this->isWindowless) {
		// We have the root accessible, but a specific child has been requested.
		varChild.lVal = ID;
		IDispatch* childDisp = NULL;
		hres = pacc->get_accChild(varChild, &childDisp);
		pacc->Release();
		if (hres != S_OK || !childDisp)
			return;
		childAcc = NULL;
		hres = childDisp->QueryInterface(IID_IAccessible, (void**)&childAcc);
		childDisp->Release();
		if (hres != S_OK || !childAcc)
			return;
		pacc = childAcc;
	}

	if (!oldNode || ID == this->rootID) {
		// This is the root node.
		VBufStorage_controlFieldNode_t* parentNode=buffer->addControlFieldNode(NULL,NULL,docHandle,ID,TRUE);
		parentNode->addAttribute(L"IAccessible::role",L"10");
		VBufStorage_fieldNode_t* previousNode=NULL;
		long childCount=0;
		pacc->get_accChildCount(&childCount);

		if (this->getAccId(pacc) != -1) {
			// We can get IDs from accessibles.
			VARIANT* varChildren;
			if (!(varChildren = (VARIANT*)malloc(sizeof(VARIANT) * childCount)))
				return;
			if (FAILED(AccessibleChildren(pacc, 0, childCount, varChildren, &childCount)))
				childCount = 0;
			for (long i = 0; i < childCount; ++i) {
				if (varChildren[i].vt != VT_DISPATCH || !varChildren[i].pdispVal) {
					VariantClear(&(varChildren[i]));
					continue;
				}
				childAcc = NULL;
				hres = varChildren[i].pdispVal->QueryInterface(IID_IAccessible, (void**)&childAcc);
				VariantClear(&(varChildren[i]));
				if (hres != S_OK)
					continue;
				int childId = getAccId(childAcc);
				previousNode = this->renderControlContent(buffer, parentNode, previousNode, docHandle, childId, childAcc);
				childAcc->Release();
			}
			free(varChildren);

		} else {
			// We can't get IDs from accessibles.
			// The only way to get IDs is to just try them sequentially.
			// accessiblesByLocation maps ((x, y), id) to (accessible, id).
			// This allows us to order by location and, where that is the same, ID.
			// We need this because added children always have larger IDs,
			// even if they were inserted between two other children.
			map<pair<pair<long, long>, long>, pair<IAccessible*, long>> accessiblesByLocation;
			// Keep going until we have childCount children.
			for(int i=1;i<1000&&static_cast<long>(accessiblesByLocation.size())<childCount;++i) {
				IDispatch* childDisp=NULL;
				varChild.lVal=i;
				if (pacc->get_accChild(varChild, &childDisp) != S_OK || !childDisp)
					continue;
				childAcc = NULL;
				hres = childDisp->QueryInterface(IID_IAccessible, (void**)&childAcc);
				childDisp->Release();
				if (hres != S_OK || !childAcc)
					continue;
				long left=0, top=0, width=0, height=0;
				varChild.lVal = CHILDID_SELF;
				if (childAcc->accLocation(&left, &top, &width, &height, varChild) != S_OK)
					left=top=width=height=0;
				accessiblesByLocation[make_pair(make_pair(top + height / 2, left + width / 2), i)] = make_pair(childAcc, i);
			}
			for (map<pair<pair<long, long>, long>, pair<IAccessible*, long>>::iterator i = accessiblesByLocation.begin(); i != accessiblesByLocation.end(); ++i) {
				previousNode = this->renderControlContent(buffer, parentNode, previousNode, docHandle, i->second.second, i->second.first);
				i->second.first->Release();
			}
		}

	} else {
		// This is a child that is being re-rendered.
		this->renderControlContent(buffer, NULL, NULL, docHandle, ID, pacc);
	}

	pacc->Release();
}

AdobeFlashVBufBackend_t::AdobeFlashVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID), accPropServices(NULL) {
}

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID) {
	VBufBackend_t* backend=new AdobeFlashVBufBackend_t(docHandle,ID);
	return backend;
}

BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		_CrtSetReportHookW2(_CRT_RPTHOOK_INSTALL,(_CRT_REPORT_HOOKW)NVDALogCrtReportHook);
	}
	return true;
}
