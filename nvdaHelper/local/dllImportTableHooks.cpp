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
#include <string.h>
#include "dllImportTableHooks.h"
#include <common\log.h>
#include <shlwapi.h>
#include <psapi.h>

using namespace std;

DllImportTableHooks::DllImportTableHooks(HMODULE targetModuleArg): targetModule(targetModuleArg) {
}

BOOL DllImportTableHooks::hookFunctions() {
	char moduleName[MAX_PATH];
	GetModuleFileNameA(this->targetModule,moduleName,MAX_PATH);
	PathStripPathA(moduleName);
	LOG_DEBUG(L"_hookFunctionsOnModule: called for " << moduleName << endl);
	UINT_PTR  imageBaseAddress=(UINT_PTR)this->targetModule;
	if(!imageBaseAddress) {
		LOG_ERROR(L"_hookFunctionsOnModule: could not locate base address of " << moduleName << L" returning false" << endl);
		return FALSE;
	}
	UINT_PTR impDescRVA=((IMAGE_NT_HEADERS*)(imageBaseAddress+((IMAGE_DOS_HEADER*)imageBaseAddress)->e_lfanew))->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress;
	if(impDescRVA==0) {
		LOG_DEBUG(L"_hookFunctionsOnModule: " << moduleName << L" has no import table, nothing to do, returning true" << endl);
		return TRUE;
	}
	LOG_DEBUG(L"_hookFunctionsOnModule: " << moduleName << L" import table at address 0X" << imageBaseAddress+impDescRVA << endl);
	for(IMAGE_IMPORT_DESCRIPTOR* pImpDesc=(IMAGE_IMPORT_DESCRIPTOR*)(imageBaseAddress+impDescRVA);pImpDesc->Name!=0;pImpDesc++) {
		char* curModuleName=(char*)(imageBaseAddress+pImpDesc->Name);
		moduleNameToFuncToFunc_t::const_iterator i=this->hookRequests.find(curModuleName);
		if(i!=this->hookRequests.end()) {
			LOG_DEBUG(L"_hookFunctionsOnModule: import table for " << moduleName << L": module section for " << curModuleName << L": looking for functions to hook\n");
			for(IMAGE_THUNK_DATA* pThunk=(IMAGE_THUNK_DATA*)(imageBaseAddress+(pImpDesc->FirstThunk));pThunk->u1.Function!=0;pThunk++) {
				void* funcAddress=(void*)(pThunk->u1.Function);
				funcToFunc_t::const_iterator j=i->second.find(funcAddress);
				if(j!=i->second.end()) {
					LOG_DEBUG(L"_hookFunctionsOnModule: import table for " << moduleName << L": module section for " << curModuleName << L": function at address 0X" << (VOID*)pThunk->u1.Function << L" found , changing thunk to use function at address 0X" << j->second << L"\n");
					this->hookedFunctions[funcAddress]=pThunk;
					DWORD oldProtect;
					VirtualProtect(pThunk,sizeof(IMAGE_THUNK_DATA),PAGE_READWRITE,&oldProtect);
					pThunk->u1.Function=(UINT_PTR)(j->second);
					VirtualProtect(pThunk,sizeof(IMAGE_THUNK_DATA),oldProtect,&oldProtect);
				}
			}
		} else {
			LOG_DEBUG(L"_hookFunctionsOnModule: import table for " << moduleName << L": module section for " << curModuleName << L": no requested hooks\n");
		}
	}
	LOG_DEBUG(L"_hookFunctionsOnModule: successfully walked " << moduleName << L"'s import table, returning true\n");
	return TRUE;
}

void* DllImportTableHooks::requestFunctionHook(const char* moduleName, const char* functionName, void* newHookProc) {
	if (!moduleName) {
		LOG_ERROR(L"apiHook_requestFunctionHook: nullptr given for moduleName\n");
		return nullptr;
	}
	HMODULE moduleHandle=GetModuleHandleA(moduleName);
	if(!moduleHandle) {
		LOG_ERROR(L"apiHook_requestFunctionHook: module " << moduleName << L" not loaded\n");
		return NULL;
	}
	void* realFunc=GetProcAddress(moduleHandle,functionName);
	if(!realFunc) {
		LOG_ERROR(L"apiHook_requestFunctionHook: function " << functionName << L" does not exist in module " << moduleName << L"\n");
		return NULL;
	}
	LOG_DEBUG(L"apiHook_requestFunctionHook: requesting to hook function " << functionName << L" at address 0X" << realFunc << L" in module " << moduleName << L" at address 0X" << moduleHandle << L" with new function at address 0X" << newHookProc << L"\n");
	funcToFunc_t& funcToFunc=this->hookRequests[moduleName];
	funcToFunc_t::iterator i=funcToFunc.find(realFunc);
	void* oldFunc=NULL;
	if(i!=funcToFunc.end()) {
		oldFunc=i->second;
		LOG_DEBUG(L"api_requestHookFunction: hook already exists for function at address 0X" << realFunc << L", setting new hook and returning old one\n");
		i->second=newHookProc;
	} else {
		oldFunc=realFunc;
		LOG_DEBUG(L"apiHook_requestFunctionHook: no existing hook for function at address 0X" << realFunc << L", setting hook and returning real function\n");
		funcToFunc[realFunc]=newHookProc;
	}
	return oldFunc;
}

BOOL DllImportTableHooks::unhookFunctions() {
	LOG_DEBUG(L"apiHook_unhookFunctions: unhooking all functions\n");
	if(this->hookedFunctions.size()==0) {
		LOG_DEBUG(L"apiHook_unhookFunctions: no functions hooked, returning true\n");
		return TRUE;
	}
	LOG_DEBUG(L"apiHook_unhookFunctions: unhooking functions on module at address 0X" << targetModule << L"\n");
	for(funcToThunk_t::iterator i=this->hookedFunctions.begin();i!=this->hookedFunctions.end();++i) {
		LOG_DEBUG(L"apiHook_unhookFunctions: restoring thunk at address 0X" << i->second << L" back to original function at address 0X" << i->first << L"\n");
		DWORD oldProtect;
		VirtualProtect(i->second,sizeof(IMAGE_THUNK_DATA),PAGE_READWRITE,&oldProtect);
		i->second->u1.Function=(UINT_PTR)i->first;
		VirtualProtect(i->second,sizeof(IMAGE_THUNK_DATA),oldProtect,&oldProtect);
	}
	this->hookRequests.clear();
	this->hookedFunctions.clear();
	return TRUE;
}

void* dllImportTableHooks_hookSingle(char* targetDll, char* importDll, char* funcName, void* newFunction) {
	HMODULE targetHandle=LoadLibraryA(targetDll);
	if(!targetHandle) return NULL;
	DllImportTableHooks* hooks=new DllImportTableHooks(targetHandle);
	hooks->requestFunctionHook(importDll,funcName,newFunction);
	hooks->hookFunctions();
	return (void*)hooks;
}

void dllImportTableHooks_unhookSingle(void* hook) {
	DllImportTableHooks* hooks=(DllImportTableHooks*)hook;
	hooks->unhookFunctions();
	FreeLibrary(hooks->targetModule);
	delete hooks;
}
