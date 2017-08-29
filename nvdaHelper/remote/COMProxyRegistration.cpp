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
#include <string>
#include <locale>
#include <codecvt>
#include <vector>
#define WIN32_LEAN_AND_MEAN 
#define CINTERFACE
#include <windows.h>
#include <objbase.h>
#include <rpcproxy.h>
#include <common/log.h>
#include "dllmain.h"
#include "COMProxyRegistration.h"

using namespace std;

typedef void(RPC_ENTRY *LPFNGETPROXYDLLINFO)(ProxyFileInfo***, CLSID**);

const wchar_t* StringCLSID_StandardMarshaler=L"{00020424-0000-0000-C000-000000000046}";

COMProxyRegistration_t* registerCOMProxy(wchar_t* dllPath) {
	LOG_DEBUG(L"Registering proxy "<<dllPath);
	int res;
	// Fetch the CLSID for the standard marshaler which will be used to unregister PS CLSIDs later
	CLSID clsid_standardMarshaler;
	if((res=IIDFromString(StringCLSID_StandardMarshaler,&clsid_standardMarshaler))!=S_OK) {
		LOG_ERROR(L"Could not get clsid for standard marshaler");
		return nullptr;
	}
	// Generate a new unique CLSID to use for class object registration
	CLSID regClsid={0};
	if((res=CoCreateGuid(&regClsid))!=S_OK) {
		LOG_ERROR(L"Unable to generate registration CLSID");
		return nullptr;
	}
	// load the proxy dll
	wchar_t absDllPath[MAX_PATH]={0};
	wsprintf(absDllPath,L"%s\\%s",dllDirectory,dllPath);
	HMODULE dllHandle=LoadLibrary(absDllPath);
	if(dllHandle==NULL) {
		LOG_ERROR(L"LoadLibrary failed for "<<dllPath);
		return nullptr;
	}
	// look up the GetProxyDllInfo function on the proxy dll 
	LPFNGETPROXYDLLINFO Dll_GetProxyDllInfo=(LPFNGETPROXYDLLINFO)GetProcAddress(dllHandle,"GetProxyDllInfo");
	if(Dll_GetProxyDllInfo==NULL) {
		LOG_ERROR(L"GetProxyDllInfo function not found in "<<dllPath);
		FreeLibrary(dllHandle);
		return nullptr;
	}
	// Fetch the proxy information from the dll (interface IIDs and the proxy stub CLSID)
	CLSID* pProxyClsid=NULL;
	ProxyFileInfo** pProxyInfo=NULL;
	Dll_GetProxyDllInfo(&pProxyInfo,&pProxyClsid);
	if(!pProxyClsid||!pProxyInfo) {
		LOG_ERROR(L"Could not fetch proxy information from "<<dllPath);
		FreeLibrary(dllHandle);
		return nullptr;
	}
	// Create and activate an activation context using the manifest in the proxy dll 
	// to temporarily register the proxy dll's class object
	ACTCTX actCtx={0};
	actCtx.cbSize=sizeof(actCtx);
	actCtx.dwFlags=ACTCTX_FLAG_HMODULE_VALID|ACTCTX_FLAG_RESOURCE_NAME_VALID;
	actCtx.lpResourceName=MAKEINTRESOURCE(2);
	actCtx.hModule=dllHandle;
	HANDLE hActCtx=CreateActCtx(&actCtx);
	if(hActCtx==NULL) {
		LOG_ERROR(L"Could not create activation context for "<<dllPath);
		FreeLibrary(dllHandle);
		return nullptr;
	}
	ULONG_PTR actCtxCookie;
	if(!ActivateActCtx(hActCtx,&actCtxCookie)) {
		LOG_ERROR(L"Error activating activation context for "<<dllPath);
		ReleaseActCtx(hActCtx);
		FreeLibrary(dllHandle);
		return nullptr;
	}
	// Fetch the class object (which will come from the proxy dll)
	IUnknown* ClassObjPunk=NULL;
	res=CoGetClassObject(*pProxyClsid,CLSCTX_INPROC_SERVER,nullptr,IID_IUnknown,(void**)&ClassObjPunk);
	// From here we no longer need the activation context
	DeactivateActCtx(0,actCtxCookie);
	ReleaseActCtx(hActCtx);
	if(res!=S_OK) {
		LOG_ERROR(L"Error fetching class object for "<<dllPath<<L", code "<<res);
		FreeLibrary(dllHandle);
		return nullptr;
	}
	// Re-register the class object with COM now that the activation context is gone.
	// Keeping the class object available to COM, with COM also handling the life time of the proxy dll now
	DWORD dwCookie;
	res=CoRegisterClassObject(regClsid,ClassObjPunk,CLSCTX_INPROC_SERVER,REGCLS_MULTIPLEUSE,&dwCookie);
	ClassObjPunk->lpVtbl->Release(ClassObjPunk);
	if(res!=S_OK) {
		LOG_ERROR(L"Error registering class object for "<<dllPath<<L", code "<<res);
		FreeLibrary(dllHandle);
		return nullptr;
	}
	COMProxyRegistration_t* reg= new COMProxyRegistration_t();
	reg->dllPath=dllPath;
	reg->classObjectRegistrationCookie=dwCookie;
	// For all interfaces the proxy dll supports, register its CLSID as their proxy stub CLSID
	ProxyFileInfo** tempInfoPtr=pProxyInfo;
	while(*tempInfoPtr) {
		ProxyFileInfo& fileInfo=**tempInfoPtr;
		for(unsigned short idx=0;idx<fileInfo.TableSize;++idx) {
			IID iid=*(fileInfo.pStubVtblList[idx]->header.piid);
			CLSID clsidBackup={0};
			wstring_convert<codecvt_utf8_utf16<wchar_t>> converter;
			wstring name=converter.from_bytes(fileInfo.pNamesArray[idx]);
			// Fetch the old CLSID for this interface if one is set, so we can replace it on deregistration.
			// If not set, then we'll use the standard marshaler clsid on deregistration.
			if((res=CoGetPSClsid(iid,&clsidBackup))!=S_OK) {
				clsidBackup=clsid_standardMarshaler;
			} else {
				LOG_DEBUG(L"Backed up existing clsid for interface "<<name);
			}
			if((res=CoRegisterPSClsid(iid,regClsid))!=S_OK) {
				LOG_ERROR(L"Unable to register interface "<<name<<L" with proxy stub "<<dllPath<<L", code "<<res);
				continue;
			}
		reg->psClsidBackups.push_back({name,iid,clsidBackup});
		LOG_DEBUG(L"Registered interface "<<name);
		}
		++tempInfoPtr;
	}
	// We can now safely free the proxy dll. COM will keep it loaded or re-load it if needed
	FreeLibrary(dllHandle);
	LOG_DEBUG(L"Done registering proxy "<<dllPath);
	return reg;
}

bool unregisterCOMProxy(COMProxyRegistration_t* reg) {
	if(!reg) return false;
	HRESULT res;
	LOG_DEBUG(L"Unregistering proxy "<<(reg->dllPath));
	for(auto& backup: reg->psClsidBackups) {
		if((res=CoRegisterPSClsid(backup.iid,backup.clsid))!=S_OK) {
			LOG_ERROR(L"Error registering backup PSClsid for interface "<<(backup.name)<<L" from "<<(reg->dllPath)<<L", code "<<res);
		}
		LOG_DEBUG(L"Unregistered interface "<<(backup.name));
	}
	if((res=CoRevokeClassObject((DWORD)(reg->classObjectRegistrationCookie)))!=S_OK) {
		LOG_ERROR(L"Error unregistering class object from "<<(reg->dllPath)<<L", code "<<res);
	}
	LOG_DEBUG(L"Done unregistering proxy "<<(reg->dllPath));
	delete reg;
	return true;
}

