/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright (C) 2017  NV Access Limited.
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
#include <vector>
#include <map>
#include <mutex>
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

typedef struct {
	bool hadOriginalProxy;
	CLSID originalProxyClsid;
	std::wstring dllPath;
	std::wstring interfaceName;
	long threadId;
	CLSID proxyClsidRegistered;
} InterfaceProxyBackup_t;

std::map<std::wstring, InterfaceProxyBackup_t> interfaceProxyBackups;
std::map<std::wstring, CLSID> dllProxyClsidCache;
std::mutex comProxyRegistrationMutex;

std::wstring guidToString(const GUID& guid) {
	OLECHAR* guidString = nullptr;
	HRESULT res = StringFromCLSID(guid, &guidString);
	if (FAILED(res) || !guidString) {
		LOG_ERROR(L"StringFromCLSID failed, code "<<res);
		return L"";
	}
	std::wstring result(guidString);
	CoTaskMemFree(guidString);
	return result;
}

GUID stringToGuid(const std::wstring& guidString) {
	GUID guid = GUID_NULL;
	HRESULT res = CLSIDFromString(guidString.c_str(), &guid);
	if (FAILED(res)) {
		LOG_ERROR(L"CLSIDFromString failed for '"<<guidString<<L"', code "<<res);
		return GUID_NULL;
	}
	return guid;
}

bool generateOrFetchUniqueClsidForProxyDll(const std::wstring& dllPath, CLSID* outClsid) {
	std::lock_guard<std::mutex> lock(comProxyRegistrationMutex);
	auto it = dllProxyClsidCache.find(dllPath);
	if (it != dllProxyClsidCache.end()) {
		*outClsid = it->second;
		auto cachedClsidString = guidToString(it->second);
		LOG_DEBUG(L"Reusing cached proxy CLSID "<<cachedClsidString <<L" for dll "<<dllPath);
		return true;
	}
	// generate a new CLSID for this dll and cache it so that we can reuse the same CLSID for all interfaces in the same dll and also for later unregistration
	HRESULT res = CoCreateGuid(outClsid);
	if (res != S_OK) {
		LOG_ERROR(L"Failed to generate CLSID for proxy dll "<<dllPath<<L", code "<<res);
		return false;
	}
	dllProxyClsidCache[dllPath] = *outClsid;
	return true;
}

bool registerInterfaceProxy(std::wstring interfaceName, std::wstring dllPath, IID iid, CLSID clsid) {
	HRESULT res;
	auto iidString = guidToString(iid);
	auto clsidString = guidToString(clsid);
	InterfaceProxyBackup_t backup = {0};
	std::lock_guard<std::mutex> lock(comProxyRegistrationMutex);
	auto it = interfaceProxyBackups.find(iidString);
	if (it != interfaceProxyBackups.end()) {
		if (dllPath != it->second.dllPath) {
			LOG_ERROR(L"Interface "<<interfaceName<<L" ("<<iidString<<L") already has a backup from a different dll ("<<it->second.dllPath<<L"), this may indicate a problem");
			return false;
		}
		if (clsid != it->second.proxyClsidRegistered) {
			LOG_ERROR(L"Interface "<<interfaceName<<L" ("<<iidString<<L") already has a backup with a different registered proxy CLSID ("<<guidToString(it->second.proxyClsidRegistered)<<L") than the one we are trying to register ("<<clsidString<<L"), this may indicate a problem");
			return false;
		}
		LOG_DEBUG(L"Interface "<<iidString<<L" already  backed up by thread "<<it->second.threadId<<L" for dll "<<it->second.dllPath);
		return true;
	}
	res = CoGetPSClsid(iid,&backup.originalProxyClsid);
	if(res!=S_OK) {
		LOG_DEBUG(L"Interface "<<iidString<<L" does not have an already registered proxy CLSID");
		backup.hadOriginalProxy = false;
	} else {
		backup.hadOriginalProxy = true;
	}
	backup.interfaceName = interfaceName;
	backup.dllPath = dllPath;
	backup.proxyClsidRegistered = clsid;
	backup.threadId = GetCurrentThreadId();
	res = CoRegisterPSClsid(iid, clsid);
	if(res!=S_OK) {
		LOG_ERROR(L"Unable to register interface iid "<<iidString<<L" with proxy CLSID "<<clsidString<<L", code "<<res);
		return false;
	}
	interfaceProxyBackups[iidString] = backup;
	LOG_DEBUG(L"Registered proxy CLSID "<<clsidString<<L" for interface "<<interfaceName<<L" ("<<iidString<<L") for dll "<<dllPath);
	return true;
}

COMProxyRegistration_t* registerCOMProxy(const wchar_t* dllPath) {
	LOG_DEBUG(L"Registering proxy "<<dllPath);
	CLSID proxyClsidForRegistration;
	if (!generateOrFetchUniqueClsidForProxyDll(dllPath, &proxyClsidForRegistration)) {
		LOG_ERROR(L"Failed to generate or fetch proxy CLSID for "<<dllPath);
		return nullptr;
	}
	auto proxyClsidString = guidToString(proxyClsidForRegistration);
	HRESULT res;
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
	// to temporarily register the proxy dll's class object.
	// We do this instead of calling DllGetClassObject, so that Windows manages the loading and unloading of the proxy dll itself.
	ACTCTX actCtx={0};
	actCtx.cbSize=sizeof(actCtx);
	actCtx.dwFlags=ACTCTX_FLAG_HMODULE_VALID|ACTCTX_FLAG_RESOURCE_NAME_VALID;
	// The resource ID for a dll must be 2.
	// See the linker's /manifest argument stating where the manifest is placed in a dll: https://docs.microsoft.com/en-gb/cpp/build/reference/manifest-create-side-by-side-assembly-manifest
	actCtx.lpResourceName=MAKEINTRESOURCE(2);
	actCtx.hModule=dllHandle;
	HANDLE hActCtx=CreateActCtx(&actCtx);
	if (hActCtx == INVALID_HANDLE_VALUE) {
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
	res = CoRegisterClassObject(
		proxyClsidForRegistration,
		ClassObjPunk,
		CLSCTX_INPROC_SERVER,
		REGCLS_MULTIPLEUSE,
		&dwCookie
	);
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
	// pProxyInfo is a pointer to a list of ProxyFileInfo pointers. The last of them being NULL to denote the end of the list.
	// There is no official documentation on this, but
	// in dlldata.c generated by MIDL (E.g. for IAccessible2, ia2_data.c), you can see:
	// PROXYFILE_LIST_START, followed by REFERENCE_PROXY_FILE(IA2), followed by PROXYFILE_LIST_END.
	// In RPCProxy.h from the Windows SDK, PROXYFILE_LIST_START declairs an unsized array of ProxyFileInfo pointers, REFERENCE_PROXY_FILE fills in each   ProxyFileInfo pointer, and PROXYFILE_LIST_END places a final 0 to terminate the list.
	// The reason it is a list is that multiple IDLs may be compiled into one proxy, and each IDL file gets its own ProxyFileInfo and therefore its own call to REFERENCE_PROXY_FILE
	// Also see a similar implementation in Mozilla Gecko:
	// https://hg.mozilla.org/mozilla-central/raw-file/1b4c59eef820b46eb0037aca68f83a15088db45f/ipc/mscom/Registration.cpp
	ProxyFileInfo** tempInfoPtr=pProxyInfo;
	while(*tempInfoPtr) {
		ProxyFileInfo& fileInfo=**tempInfoPtr;
		for(unsigned short idx=0;idx<fileInfo.TableSize;++idx) {
			IID iid=*(fileInfo.pStubVtblList[idx]->header.piid);
			auto iidString = guidToString(iid);
			const auto pName = fileInfo.pNamesArray[idx];
			const int nameLength=MultiByteToWideChar(
				CP_UTF8,  // Code Page for conversion
				0,  // DWFlags
				pName,  // lpMultiByteStr - string to convert
				-1,  // cbMultiByte - size (bytes of pName). -1 means process whole string and pName must be null terminated.
				nullptr,  // lpWideCharStr -  don't fetch anything this time
				0 // cchWideChar - character count of lpWideCharStr. When 0, lpWideCharStr is not used, just return number of characters after conversion (including null character).
			);
			if (0 == nameLength) {
				LOG_ERROR(L"Unable to  get name length for MultiByteToWideChar conversion for entry "<<idx<<L" in ProxyFileInfo, error "<<GetLastError());
				continue;
			}
			wstring name(nameLength,L'\0');
			const int charsConverted= MultiByteToWideChar(
				CP_UTF8,  // Code Page for conversion
				0,  // DWFlags
				pName,  // lpMultiByteStr - string to convert
				-1,  // cbMultiByte - size (bytes of pName). -1 means process whole string and pName must be null terminated.
				name.data(),  // lpWideCharStr
				nameLength  // cchWideChar
			);
			if (0 == charsConverted) {
				LOG_ERROR(L"Unable to perform MultiByteToWideChar conversion for entry "<<idx<<L" in ProxyFileInfo, error "<<GetLastError());
				continue;
			}
			const auto indexOfFirstNull = name.find_first_of(L'\0');
			if(wstring::npos != indexOfFirstNull) {
				name.resize(indexOfFirstNull );
			}
			if (!registerInterfaceProxy(name, dllPath, iid, proxyClsidForRegistration)) {
				LOG_ERROR(L"Failed to register proxy for interface "<<name<<L" ("<<iidString<<L") with CLSID "<<proxyClsidString<<L" for dll "<<dllPath);
				continue;
			}
			reg->registeredInterfaces[name] = iid;
		}
		++tempInfoPtr;
	}
	LOG_DEBUG(L"Done registering proxy "<<dllPath);
	// We can now safely free the proxy dll. COM will keep it loaded or re-load it if needed
	FreeLibrary(dllHandle);
	return reg;
}

bool unregisterCOMProxy(COMProxyRegistration_t* reg) {
	if(!reg) return false;
	HRESULT res;
	LOG_DEBUG(L"Unregistering proxy "<<(reg->dllPath));
	res=CoRevokeClassObject((DWORD)(reg->classObjectRegistrationCookie));
	if(res!=S_OK) {
		LOG_ERROR(L"Error unregistering class object from "<<(reg->dllPath)<<L", code "<<res);
	}
	// For all interfaces the proxy dll supports, if we changed their proxy CLSID, restore the original one
	for (const auto& entry: reg->registeredInterfaces) {
		unregisterInterfaceProxy(entry.second);
	}
	auto it = dllProxyClsidCache.find(reg->dllPath);
	if (it != dllProxyClsidCache.end()) {
		LOG_DEBUG(L"Removing cached proxy CLSID "<<guidToString(it->second)<<L" for dll "<<reg->dllPath);
		dllProxyClsidCache.erase(it);
	}
	LOG_DEBUG(L"Done unregistering proxy "<<(reg->dllPath));
	delete reg;
	return true;
}

bool unregisterInterfaceProxy(IID iid) {
	std::lock_guard<std::mutex> lock(comProxyRegistrationMutex);
	auto iidString = guidToString(iid);
	auto it = interfaceProxyBackups.find(iidString);
	if (it == interfaceProxyBackups.end()) {
		LOG_DEBUG(L"No backup found for interface "<<iidString<<L", nothing to restore");
		return true;
	}
	if (!it->second.hadOriginalProxy) {
		LOG_DEBUG(L"Interface " << iidString << L" had no original proxy CLSID; leaving current registration unchanged");
		interfaceProxyBackups.erase(it);
		return true;
	}
	HRESULT res = CoRegisterPSClsid(iid, it->second.originalProxyClsid);
	if (res != S_OK) {
		LOG_ERROR(L"Unable to restore proxy CLSID for interface " << iidString << L" to " << guidToString(it->second.originalProxyClsid) << L", code "<< res);
		return false;
	}
	LOG_DEBUG(L"Restored proxy CLSID " << guidToString(it->second.originalProxyClsid) << L" for interface " << iidString);
	interfaceProxyBackups.erase(it);
	return true;
}

void clearCOMProxyRegistrationCache() {
	std::lock_guard<std::mutex> lock(comProxyRegistrationMutex);
	if (!dllProxyClsidCache.empty()) {
		LOG_ERROR(L"COM proxy registration cache is not empty at time of clearing. This may indicate a leak of COM proxy registrations. Cached entries: ");
		for (const auto& entry: dllProxyClsidCache) {
			LOG_ERROR(L"Cached CLSID "<<guidToString(entry.second)<<L" for dll "<<entry.first);
		}
	}
	dllProxyClsidCache.clear();
}

void clearInterfaceProxyBackups() {
	std::lock_guard<std::mutex> lock(comProxyRegistrationMutex);
	if (!interfaceProxyBackups.empty()) {
		LOG_ERROR(L"Interface proxy backup cache is not empty at time of clearing. This may indicate that some interface proxy registrations were not properly unregistered. Cached entries: ");
		for (const auto& entry: interfaceProxyBackups) {
			LOG_ERROR(L"Cached backup for interface "<<entry.first<<L", had original proxy: "<<entry.second.hadOriginalProxy<<L", original proxy CLSID: "<<guidToString(entry.second.originalProxyClsid));
		}
	}
	interfaceProxyBackups.clear();
}
