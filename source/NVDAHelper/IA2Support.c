//IA2Support.c
//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence
//See the file Copying for details.
#define UNICODE

#include <wchar.h>
#include <windows.h>
#include <objbase.h>
#include "ia2.h"
#include "IA2Support.h"

#pragma data_seg(".hookManagerShared")
BOOL isIA2Initialized=FALSE;
wchar_t IA2DllPath[256]={0};
#pragma data_seg()
#pragma comment(linker, "/section:.hookManagerShared,rws")

#define IAccessible2ProxyIID IID_IAccessible2

BOOL isIA2Installed=FALSE;
HANDLE IA2DllHandle=0;
DWORD IA2RegCooky=0;
IUnknown* IA2DllPunk=NULL;

BOOL checkForIA2() {
	CLSID proxyIid;
	CLSID NULLIid;
	memset(&NULLIid,0,sizeof(CLSID));
	return (CoGetPSClsid(&IID_IAccessible2,&proxyIid)==S_OK)&&!IsEqualCLSID(&proxyIid,&NULLIid);
}

void installIA2Support() {
	LPFNGETCLASSOBJECT IA2Dll_DllGetClassObject;
	if(isIA2Installed) return;
	if(!checkForIA2()) {
		IA2DllHandle=CoLoadLibrary(IA2DllPath,TRUE);
		if(IA2DllHandle==0) return;
		IA2Dll_DllGetClassObject=(LPFNGETCLASSOBJECT)GetProcAddress(IA2DllHandle,"DllGetClassObject");
		IA2Dll_DllGetClassObject(&IAccessible2ProxyIID,&IID_IUnknown,(LPVOID*)&IA2DllPunk);
		CoRegisterClassObject(&IAccessible2ProxyIID,IA2DllPunk,CLSCTX_LOCAL_SERVER,REGCLS_MULTIPLEUSE,(LPDWORD)&IA2RegCooky);
		CoRegisterPSClsid(&IID_IAccessible2,&IAccessible2ProxyIID);
		CoRegisterPSClsid(&IID_IAccessibleAction,&IAccessible2ProxyIID);
		CoRegisterPSClsid(&IID_IAccessibleApplication,&IAccessible2ProxyIID);
		CoRegisterPSClsid(&IID_IAccessibleComponent,&IAccessible2ProxyIID);
		CoRegisterPSClsid(&IID_IAccessibleEditableText,&IAccessible2ProxyIID);
		CoRegisterPSClsid(&IID_IAccessibleHyperlink,&IAccessible2ProxyIID);
		CoRegisterPSClsid(&IID_IAccessibleHypertext,&IAccessible2ProxyIID);
		CoRegisterPSClsid(&IID_IAccessibleImage,&IAccessible2ProxyIID);
		CoRegisterPSClsid(&IID_IAccessibleRelation,&IAccessible2ProxyIID);
		CoRegisterPSClsid(&IID_IAccessibleTable,&IAccessible2ProxyIID);
		CoRegisterPSClsid(&IID_IAccessibleText,&IAccessible2ProxyIID);
		CoRegisterPSClsid(&IID_IAccessibleValue,&IAccessible2ProxyIID);
	}
	isIA2Installed=TRUE;
}

void uninstallIA2Support() {
	CLSID NULLIid;
	memset(&NULLIid,0,sizeof(CLSID));
	if(IA2DllHandle!=0) {
		CoRegisterPSClsid(&IID_IAccessible2,&NULLIid);
		CoRegisterPSClsid(&IID_IAccessibleAction,&NULLIid);
		CoRegisterPSClsid(&IID_IAccessibleApplication,&NULLIid);
		CoRegisterPSClsid(&IID_IAccessibleComponent,&NULLIid);
		CoRegisterPSClsid(&IID_IAccessibleEditableText,&NULLIid);
		CoRegisterPSClsid(&IID_IAccessibleHypertext,&NULLIid);
		CoRegisterPSClsid(&IID_IAccessibleImage,&NULLIid);
		CoRegisterPSClsid(&IID_IAccessibleRelation,&NULLIid);
		CoRegisterPSClsid(&IID_IAccessibleTable,&NULLIid);
		CoRegisterPSClsid(&IID_IAccessibleText,&NULLIid);
		CoRegisterPSClsid(&IID_IAccessibleValue,&NULLIid);
		CoRevokeClassObject(IA2RegCooky);
		CoFreeUnusedLibrariesEx(0,0);
		IA2DllHandle=0;
		isIA2Installed=FALSE;
	}
}

void IA2Support_initialize() {
	GetFullPathName(L"lib/IAccessible2Proxy.dll",256,IA2DllPath,NULL);
	isIA2Initialized=TRUE;
}
