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

#include <cstdio>
#include <cwchar>
#define WIN32_LEAN_AND_MEAN 
#include <windows.h>
#include <objbase.h>
#include <ia2.h>
#include "nvdaControllerInternal.h"
#include <common/log.h>
#include "nvdaHelperRemote.h"
#include "dllmain.h"
#include "inProcess.h"
#include "nvdaInProcUtils.h"
#include "COMProxyRegistration.h"
#include "IA2Support.h"

using namespace std;

#define APPLICATION_USER_MODEL_ID_MAX_LENGTH 131
typedef LONG(WINAPI *GetCurrentApplicationUserModelId_funcType)(UINT32*,PWSTR);
typedef ULONG(*LPFNDLLCANUNLOADNOW)();

bool isIA2Installed=FALSE;
COMProxyRegistration_t* IA2ProxyRegistration;
COMProxyRegistration_t* ISimpleDOMProxyRegistration;
HANDLE IA2UIThreadHandle=NULL;
DWORD IA2UIThreadID=0;
HANDLE IA2UIThreadUninstalledEvent=NULL;
UINT wm_uninstallIA2Support=0;
bool isIA2Initialized=FALSE;
bool isIA2SupportDisabled=false;

bool installIA2Support() {
	if(isIA2Installed) return FALSE;
	APTTYPE appType;
	APTTYPEQUALIFIER aptQualifier;
	HRESULT res;
	if((res=CoGetApartmentType(&appType,&aptQualifier))!=S_OK) {
		if(res!=CO_E_NOTINITIALIZED) {
			LOG_ERROR(L"Error getting apartment type, code "<<res);
		}
		return false;
	}
	IA2ProxyRegistration=registerCOMProxy(L"IAccessible2Proxy.dll");
	if(!IA2ProxyRegistration) {
		LOG_ERROR(L"Error registering IAccessible2 proxy");
	}
		ISimpleDOMProxyRegistration=registerCOMProxy(L"ISimpleDOM.dll");
	if(!ISimpleDOMProxyRegistration) {
		LOG_ERROR(L"Error registering ISimpleDOM proxy");
	}
	isIA2Installed=TRUE;
	return isIA2Installed;
}

bool uninstallIA2Support() {
	if(!isIA2Installed) return false;
	if(ISimpleDOMProxyRegistration&&!unregisterCOMProxy(ISimpleDOMProxyRegistration)) {
		LOG_ERROR(L"Error unregistering ISimpleDOM proxy");
	} else {
		ISimpleDOMProxyRegistration=nullptr;
	}
	if(IA2ProxyRegistration&&!unregisterCOMProxy(IA2ProxyRegistration)) {
		LOG_ERROR(L"Error unregistering IAccessible2 proxy");
	} else {
		IA2ProxyRegistration=nullptr;
	}
	isIA2Installed=FALSE;
	return TRUE;
}

void CALLBACK IA2Support_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) { 
	if (eventID != EVENT_SYSTEM_FOREGROUND && eventID != EVENT_OBJECT_FOCUS)
		return;
	if (installIA2Support()) {
		IA2UIThreadHandle=OpenThread(SYNCHRONIZE,false,threadID);
		IA2UIThreadID=threadID;
		// IA2 support successfully installed, so this hook isn't needed anymore.
		unregisterWinEventHook(IA2Support_winEventProcHook);
	}
}

LRESULT CALLBACK IA2Support_uninstallerHook(int code, WPARAM wParam, LPARAM lParam) {
	MSG* pmsg=(MSG*)lParam;
	if(pmsg->message==wm_uninstallIA2Support) {
		uninstallIA2Support();
		SetEvent(IA2UIThreadUninstalledEvent);
	}
	return 0;
}

void IA2Support_inProcess_initialize() {
	if (isIA2Installed||isIA2SupportDisabled)
		return;
	// #5417: disable IAccessible2 support for suspendable processes to work around a deadlock in NVDAHelperRemote (specifically seen in Win10 searchUI)
	HMODULE kernel32Handle=LoadLibrary(L"kernel32.dll");
	if(!kernel32Handle) {
		LOG_ERROR(L"Can't load kernel32.dll");
		return; 
	}
	GetCurrentApplicationUserModelId_funcType GetCurrentApplicationUserModelId_fp=(GetCurrentApplicationUserModelId_funcType)GetProcAddress(kernel32Handle,"GetCurrentApplicationUserModelId");
	if(GetCurrentApplicationUserModelId_fp) {
		UINT32 bufSize=APPLICATION_USER_MODEL_ID_MAX_LENGTH+1;
		wchar_t* buf=(wchar_t*)malloc(bufSize*sizeof(wchar_t));
		LONG res=GetCurrentApplicationUserModelId_fp(&bufSize,buf);
		if(res==ERROR_SUCCESS) {
			isIA2SupportDisabled=true;
			LOG_DEBUGWARNING(L"disabling IA2 support");
		} else if(res==ERROR_INSUFFICIENT_BUFFER) {
			LOG_ERROR(L"string not long enough");
		}
		free(buf);
	}
	FreeLibrary(kernel32Handle);
	if(isIA2SupportDisabled) return;
	// Try to install IA2 support on focus/foreground changes.
	// This hook will be unregistered by the callback once IA2 support is successfully installed.
	registerWinEventHook(IA2Support_winEventProcHook);
}

void IA2Support_inProcess_terminate() {
	// This will do nothing if the hook isn't registered.
	unregisterWinEventHook(IA2Support_winEventProcHook);
	if(!isIA2Installed||!IA2UIThreadHandle) {
		return;
	}
	//Check if the UI thread is still alive, if not there's nothing for us to do
	if(WaitForSingleObject(IA2UIThreadHandle,0)==0) {
		return;
	}
	//Instruct the UI thread to uninstall IA2
	IA2UIThreadUninstalledEvent=CreateEvent(NULL,true,false,NULL);
	registerWindowsHook(WH_GETMESSAGE,IA2Support_uninstallerHook);
	wm_uninstallIA2Support=RegisterWindowMessage(L"wm_uninstallIA2Support");
	PostThreadMessage(IA2UIThreadID,wm_uninstallIA2Support,0,0);
	HANDLE waitHandles[2]={IA2UIThreadUninstalledEvent,IA2UIThreadHandle};
	int res=WaitForMultipleObjects(2,waitHandles,false,10000);
	if(res!=WAIT_OBJECT_0&&res!=WAIT_OBJECT_0+1) {
		LOG_DEBUGWARNING(L"WaitForMultipleObjects returned "<<res);
	}
	unregisterWindowsHook(WH_GETMESSAGE,IA2Support_uninstallerHook);
	CloseHandle(IA2UIThreadUninstalledEvent);
	CloseHandle(IA2UIThreadHandle);
}

const long FINDCONTENTDESCENDANT_FIRST=0;
const long FINDCONTENTDESCENDANT_CARET=1;
const long FINDCONTENTDESCENDANT_LAST=2;
const long FINDCONTENTDESCENDANT_SELECTIONSTART=3;
const long FINDCONTENTDESCENDANT_SELECTIONEND=4;

bool findContentDescendant(IAccessible2* pacc2, long what, long* descendantID, long* descendantOffset) {
	bool foundDescendant=false;
	IAccessibleText* paccText=NULL;
	pacc2->QueryInterface(IID_IAccessibleText,(void**)&paccText);
	if(paccText) {
		long offset=-1;
		switch(what) {
			case FINDCONTENTDESCENDANT_FIRST:
				offset=0;
				break;
			case FINDCONTENTDESCENDANT_CARET:
				paccText->get_caretOffset(&offset);
				break;
			case FINDCONTENTDESCENDANT_LAST:
				paccText->get_nCharacters(&offset);
				// If there is no text, last is still valid but should just use 0.
				if (offset > 0)
					--offset;
				break;
			case FINDCONTENTDESCENDANT_SELECTIONSTART:
			case FINDCONTENTDESCENDANT_SELECTIONEND:
				long nSelections=0;
				paccText->get_nSelections(&nSelections);
				if(nSelections==0) {
					offset=-1;
				} else {
					long startOffset=0;
					long endOffset=0;
					paccText->get_selection(0,&startOffset,&endOffset);
					offset=(what==FINDCONTENTDESCENDANT_SELECTIONSTART)?startOffset:endOffset-1;
				}
				break;
		}
		paccText->Release();
		if(offset==-1) return false; 
		IAccessibleHypertext* paccHypertext=NULL;
		pacc2->QueryInterface(IID_IAccessibleHypertext,(void**)&paccHypertext);
		if(paccHypertext) {
			long hi=-1;
			paccHypertext->get_hyperlinkIndex(offset,&hi);
			IAccessibleHyperlink* paccHyperlink=NULL;
			if(hi>=0) {
				paccHypertext->get_hyperlink(hi,&paccHyperlink);
			}
			paccHypertext->Release();
			if(paccHyperlink) {
				IAccessible2* pacc2Child=NULL;
				paccHyperlink->QueryInterface(IID_IAccessible2,(void**)&pacc2Child);
				paccHyperlink->Release();
				if(pacc2Child) {
					foundDescendant=findContentDescendant(pacc2Child,what,descendantID,descendantOffset);
					if(!foundDescendant&&what==FINDCONTENTDESCENDANT_CARET) {
						foundDescendant=findContentDescendant(pacc2Child,FINDCONTENTDESCENDANT_FIRST,descendantID,descendantOffset);
					}
					pacc2Child->Release();
				}
			}
		}
		if(!foundDescendant) {
			pacc2->get_uniqueID(descendantID);
			*descendantOffset=offset;
			foundDescendant=true;
		}
	} else {
		long childCount=0;
		pacc2->get_accChildCount(&childCount);
		VARIANT varChild;
		varChild.vt=VT_I4;
		for(int i=1;i<=childCount;++i) {
			varChild.lVal=(what==FINDCONTENTDESCENDANT_LAST||what==FINDCONTENTDESCENDANT_SELECTIONEND)?(childCount-(i-1)):i;
			IDispatch* pdispatchChild=NULL;
			pacc2->get_accChild(varChild,&pdispatchChild);
			if(!pdispatchChild) continue;
			IAccessible2* pacc2Child=NULL;
			pdispatchChild->QueryInterface(IID_IAccessible2,(void**)&pacc2Child);
			pdispatchChild->Release();
			if(!pacc2Child) continue;
			foundDescendant=findContentDescendant(pacc2Child,what,descendantID,descendantOffset);
			pacc2Child->Release();
			if(foundDescendant) break;
		}
	}
	return foundDescendant;
}

error_status_t nvdaInProcUtils_IA2Text_findContentDescendant(handle_t bindingHandle, const unsigned long windowHandle, long parentID, long what, long* descendantID, long* descendantOffset) {
	HWND hwnd=(HWND)UlongToHandle(windowHandle);
	auto func=[&] {
		IAccessible* pacc=NULL;
		VARIANT varChild;
		AccessibleObjectFromEvent((HWND)hwnd,OBJID_CLIENT,parentID,&pacc,&varChild);
		if(!pacc) return;
		IAccessible2* pacc2=NULL;
		IServiceProvider* pserv=NULL;
		pacc->QueryInterface(IID_IServiceProvider,(void**)&pserv);
		pacc->Release();
		if(!pserv) return; 
		pserv->QueryService(IID_IAccessible,IID_IAccessible2,(void**)&pacc2);
		pserv->Release();
		if(!pacc2) return;
		findContentDescendant(pacc2,what,descendantID,descendantOffset);
		pacc2->Release();
	};
	if(!execInThread(GetWindowThreadProcessId(hwnd,NULL),func)) {
			LOG_DEBUGWARNING(L"Could not execute findContentDescendant in UI thread");
	}
	return 0;
}
