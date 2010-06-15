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
#include <cassert>
#include <cwchar>
#include <windows.h>
#include <objbase.h>
#include <ia2.h>
#include "nvdaControllerInternal.h"
#include <common/log.h>
#include "nvdaHelperRemote.h"
#include "dllmain.h"
#include "IA2Support.h"

typedef ULONG(*LPFNDLLCANUNLOADNOW)();

#pragma data_seg(".ia2SupportShared")
wchar_t IA2DllPath[MAX_PATH]={0};
IID ia2Iids[]={
	IID_IAccessible2,
	IID_IAccessibleAction,
	IID_IAccessibleApplication,
	IID_IAccessibleComponent,
	IID_IAccessibleEditableText,
	IID_IAccessibleHyperlink,
	IID_IAccessibleHypertext,
	IID_IAccessibleImage,
	IID_IAccessibleRelation,
	IID_IAccessibleTable,
	IID_IAccessibleText,
	IID_IAccessibleValue,
};
#pragma data_seg()
#pragma comment(linker, "/section:.ia2SupportShared,rws")

#define IAccessible2ProxyIID IID_IAccessible2

IID _ia2PSClsidBackups[ARRAYSIZE(ia2Iids)]={0};
BOOL isIA2Installed=FALSE;
HINSTANCE IA2DllHandle=0;
DWORD IA2RegCooky=0;
BOOL isIA2Initialized=FALSE;

BOOL installIA2Support() {
	LPFNGETCLASSOBJECT IA2Dll_DllGetClassObject;
	int i;
	int res;
	if(isIA2Installed) return TRUE;
	if((IA2DllHandle=CoLoadLibrary(IA2DllPath,FALSE))==NULL) {
		LOG_ERROR(L"CoLoadLibrary failed");
		return FALSE;
	}
	IA2Dll_DllGetClassObject=(LPFNGETCLASSOBJECT)GetProcAddress(static_cast<HMODULE>(IA2DllHandle),"DllGetClassObject");
	assert(IA2Dll_DllGetClassObject); //IAccessible2 proxy dll must have this function
	IUnknown* ia2ClassObjPunk=NULL;
	if((res=IA2Dll_DllGetClassObject(IAccessible2ProxyIID,IID_IUnknown,(LPVOID*)&ia2ClassObjPunk))!=S_OK) {
		LOG_ERROR(L"Error calling DllGetClassObject, code "<<res);
		CoFreeLibrary(IA2DllHandle);
		IA2DllHandle=0;
		return FALSE;
	}
	if((res=CoRegisterClassObject(IAccessible2ProxyIID,ia2ClassObjPunk,CLSCTX_INPROC_SERVER,REGCLS_MULTIPLEUSE,(LPDWORD)&IA2RegCooky))!=S_OK) {
		LOG_DEBUGWARNING(L"Error registering class object, code "<<res);
		ia2ClassObjPunk->Release();
		CoFreeLibrary(IA2DllHandle);
		IA2DllHandle=0;
		return FALSE;
	}
	ia2ClassObjPunk->Release();
	for(i=0;i<ARRAYSIZE(ia2Iids);++i) {
		CoGetPSClsid(ia2Iids[i],&(_ia2PSClsidBackups[i]));
		CoRegisterPSClsid(ia2Iids[i],IAccessible2ProxyIID);
	}
	isIA2Installed=TRUE;
	return TRUE;
}

BOOL uninstallIA2Support() {
	int i;
	LPFNDLLCANUNLOADNOW IA2Dll_DllCanUnloadNow;
	if(isIA2Installed) {
	for(i=0;i<ARRAYSIZE(ia2Iids);++i) {
			CoRegisterPSClsid(ia2Iids[i],_ia2PSClsidBackups[i]);
		}
		CoRevokeClassObject(IA2RegCooky);
		IA2Dll_DllCanUnloadNow=(LPFNDLLCANUNLOADNOW)GetProcAddress(static_cast<HMODULE>(IA2DllHandle),"DllCanUnloadNow");
		assert(IA2Dll_DllCanUnloadNow); //IAccessible2 proxy dll must have this function
		if(IA2Dll_DllCanUnloadNow()==S_OK) {
			CoFreeLibrary(IA2DllHandle);
		}
		IA2DllHandle=0;
		isIA2Installed=FALSE;
	}
	return TRUE;
}

BOOL IA2Support_initialize() {
	assert(!isIA2Initialized);
	wsprintf(IA2DllPath,L"%s\\IAccessible2Proxy.dll",dllDirectory);
	isIA2Initialized=TRUE;
	installIA2Support();
	return TRUE;
}

BOOL IA2Support_terminate() {
	assert(isIA2Initialized);
	uninstallIA2Support();
	return TRUE;
}

void CALLBACK IA2Support_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) { 
	if (eventID != EVENT_SYSTEM_FOREGROUND && eventID != EVENT_OBJECT_FOCUS)
		return;
	if (installIA2Support()) {
		// IA2 support successfully installed, so this hook isn't needed anymore.
		unregisterWinEventHook(IA2Support_winEventProcHook);
	}
}

void IA2Support_inProcess_initialize() {
	// Try to install IA2 support on focus/foreground changes.
	// This hook will be unregistered by the callback once IA2 support is successfully installed.
	registerWinEventHook(IA2Support_winEventProcHook);
}

void IA2Support_inProcess_terminate() {
	// This will do nothing if the hook isn't registered.
	unregisterWinEventHook(IA2Support_winEventProcHook);
	uninstallIA2Support();
}
