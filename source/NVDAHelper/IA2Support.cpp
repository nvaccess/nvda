//IA2Support.cpp
//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence
//See the file Copying for details.
#define UNICODE

#include <cstdio>
#include <cassert>
#include <cwchar>
#include <windows.h>
#include <objbase.h>
#include "ia2.h"
#include "IA2Support.h"

typedef ULONG(*LPFNDLLCANUNLOADNOW)();

#pragma data_seg(".hookManagerShared")
BOOL isIA2Initialized=FALSE;
wchar_t IA2DllPath[256]={0};
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
#pragma comment(linker, "/section:.hookManagerShared,rws")

#define IAccessible2ProxyIID IID_IAccessible2

IID _ia2PSClsidBackups[ARRAYSIZE(ia2Iids)]={0};
BOOL isIA2Installed=FALSE;
HINSTANCE IA2DllHandle=0;
DWORD IA2RegCooky=0;

BOOL installIA2Support() {
	LPFNGETCLASSOBJECT IA2Dll_DllGetClassObject;
	int i;
	int res;
	if(isIA2Installed) return TRUE;
	if((IA2DllHandle=CoLoadLibrary(IA2DllPath,FALSE))==NULL) {
		fprintf(stderr,"Error loading IAccessible2 proxy dll\n");
		return FALSE;
	}
	IA2Dll_DllGetClassObject=(LPFNGETCLASSOBJECT)GetProcAddress(static_cast<HMODULE>(IA2DllHandle),"DllGetClassObject");
	assert(IA2Dll_DllGetClassObject); //IAccessible2 proxy dll must have this function
	IUnknown* ia2ClassObjPunk=NULL;
	if((res=IA2Dll_DllGetClassObject(IAccessible2ProxyIID,IID_IUnknown,(LPVOID*)&ia2ClassObjPunk))!=S_OK) {
		fprintf(stderr,"Error calling DllGetClassObject, code %d\n",res);
		CoFreeLibrary(IA2DllHandle);
		IA2DllHandle=0;
		return FALSE;
	}
	if((res=CoRegisterClassObject(IAccessible2ProxyIID,ia2ClassObjPunk,CLSCTX_INPROC_SERVER,REGCLS_MULTIPLEUSE,(LPDWORD)&IA2RegCooky))!=S_OK) {
		fprintf(stderr,"Error registering class object, code %d\n",res);
		ia2ClassObjPunk->Release();
		CoFreeLibrary(IA2DllHandle);
		IA2DllHandle=0;
		return FALSE;
	}
	ia2ClassObjPunk->Release();
	for(i=0;i<ARRAYSIZE(ia2Iids);i++) {
		CoGetPSClsid(ia2Iids[i],&(_ia2PSClsidBackups[i]));
		CoRegisterPSClsid(ia2Iids[i],IAccessible2ProxyIID);
	}
	isIA2Installed=TRUE;
	return TRUE;
}

BOOL uninstallIA2Support() {
	int i;
	int res;
	LPFNDLLCANUNLOADNOW IA2Dll_DllCanUnloadNow;
	if(isIA2Installed) {
	for(i=0;i<ARRAYSIZE(ia2Iids);i++) {
			CoRegisterPSClsid(ia2Iids[i],_ia2PSClsidBackups[i]);
		}
		CoRevokeClassObject(IA2RegCooky);
		IA2Dll_DllCanUnloadNow=(LPFNDLLCANUNLOADNOW)GetProcAddress(static_cast<HMODULE>(IA2DllHandle),"DllCanUnloadNow");
		assert(IA2Dll_DllCanUnloadNow); //IAccessible2 proxy dll must have this function
		if(IA2Dll_DllCanUnloadNow()==S_OK) {
			CoFreeLibrary(IA2DllHandle);
		} else {
			Beep(550,50);
		}
		IA2DllHandle=0;
		isIA2Installed=FALSE;
	}
	return TRUE;
}

BOOL IA2Support_initialize() {
	int count=0;
	if(!isIA2Initialized) {
		GetFullPathName(L"lib/IAccessible2Proxy.dll",256,IA2DllPath,NULL);
		isIA2Initialized=TRUE;
	}
	if(!installIA2Support()) {
		fprintf(stderr,"Error installing IA2 support\n");
		return FALSE;
	}
	return TRUE;
}

BOOL IA2Support_terminate() {
	if(!uninstallIA2Support()) {
		fprintf(stderr,"Error uninstalling IA2 support\n");
		return FALSE;
	}
	return TRUE;
}
