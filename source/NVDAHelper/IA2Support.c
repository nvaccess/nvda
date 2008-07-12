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

#define ia2InterfaceCount 12

#pragma data_seg(".hookManagerShared")
BOOL isIA2Initialized=FALSE;
wchar_t IA2DllPath[256]={0};
//This array can hold items containing a clsid to be registered, and the old proxy stub clsid for that clsid that may have been pointed to 
//Both values are NULL Iids (all zeros) by default 
IID ia2ClsidArray[ia2InterfaceCount][2]={0};
#pragma data_seg()
#pragma comment(linker, "/section:.hookManagerShared,rws")

#define IAccessible2ProxyIID IID_IAccessible2

BOOL isIA2Installed=FALSE;
HANDLE IA2DllHandle=0;
DWORD IA2RegCooky=0;
IUnknown* IA2DllPunk=NULL;

void installIA2Support() {
	LPFNGETCLASSOBJECT IA2Dll_DllGetClassObject;
	int i;
	if(isIA2Installed) return;
	IA2DllHandle=CoLoadLibrary(IA2DllPath,TRUE);
	if(IA2DllHandle==0) return;
	IA2Dll_DllGetClassObject=(LPFNGETCLASSOBJECT)GetProcAddress(IA2DllHandle,"DllGetClassObject");
	IA2Dll_DllGetClassObject(&IAccessible2ProxyIID,&IID_IUnknown,(LPVOID*)&IA2DllPunk);
	CoRegisterClassObject(&IAccessible2ProxyIID,IA2DllPunk,CLSCTX_LOCAL_SERVER,REGCLS_MULTIPLEUSE,(LPDWORD)&IA2RegCooky);
	for(i=0;i<ia2InterfaceCount;i++) {
		CoGetPSClsid(&(ia2ClsidArray[i][0]),&(ia2ClsidArray[i][1]));
		CoRegisterPSClsid(&(ia2ClsidArray[i][0]),&IAccessible2ProxyIID);
	}
	isIA2Installed=TRUE;
}

void uninstallIA2Support() {
	int i;
	if(IA2DllHandle!=0) {
	for(i=0;i<ia2InterfaceCount;i++) {
			CoRegisterPSClsid(&(ia2ClsidArray[i][0]),&(ia2ClsidArray[i][1]));
		}
		CoRevokeClassObject(IA2RegCooky);
		CoFreeUnusedLibrariesEx(0,0);
		IA2DllHandle=0;
		isIA2Installed=FALSE;
	}
}

void IA2Support_initialize() {
	int count=0;
	GetFullPathName(L"lib/IAccessible2Proxy.dll",256,IA2DllPath,NULL);
	//Initialize the IAccessible2 Iids
	ia2ClsidArray[count++][0]=IID_IAccessible2;
	ia2ClsidArray[count++][0]=IID_IAccessibleAction;
	ia2ClsidArray[count++][0]=IID_IAccessibleApplication;
	ia2ClsidArray[count++][0]=IID_IAccessibleComponent;
	ia2ClsidArray[count++][0]=IID_IAccessibleEditableText;
	ia2ClsidArray[count++][0]=IID_IAccessibleHyperlink;
	ia2ClsidArray[count++][0]=IID_IAccessibleHypertext;
	ia2ClsidArray[count++][0]=IID_IAccessibleImage;
	ia2ClsidArray[count++][0]=IID_IAccessibleRelation;
	ia2ClsidArray[count++][0]=IID_IAccessibleTable;
	ia2ClsidArray[count++][0]=IID_IAccessibleText;
	ia2ClsidArray[count++][0]=IID_IAccessibleValue;
	isIA2Initialized=TRUE;
	installIA2Support();
}
