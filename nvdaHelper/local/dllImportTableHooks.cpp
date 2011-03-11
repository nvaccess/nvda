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
#include <shlwapi.h>
#include <psapi.h>

using namespace std;

DllImportTableHooks::DllImportTableHooks(HMODULE targetModuleArg): targetModule(targetModuleArg) {
}

BOOL DllImportTableHooks::hookFunctions() {
	char moduleName[MAX_PATH];
	GetModuleFileNameA(this->targetModule,moduleName,MAX_PATH);
	PathStripPathA(moduleName);
	printf("_hookFunctionsOnModule: called for %s\n",moduleName);
	UINT_PTR  imageBaseAddress=(UINT_PTR)this->targetModule;
	if(!imageBaseAddress) {
		fprintf(stderr,"_hookFunctionsOnModule: could not locate base address of %s, returning false\n",moduleName); 
		return FALSE;
	}
	UINT_PTR impDescRVA=((IMAGE_NT_HEADERS*)(imageBaseAddress+((IMAGE_DOS_HEADER*)imageBaseAddress)->e_lfanew))->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress;
	if(impDescRVA==0) {
		printf("_hookFunctionsOnModule: %s has no import table, nothing to do, returning true\n",moduleName);
		return TRUE;
	}
	printf("_hookFunctionsOnModule: %s import table at address 0X%X\n",moduleName,imageBaseAddress+impDescRVA);
	for(IMAGE_IMPORT_DESCRIPTOR* pImpDesc=(IMAGE_IMPORT_DESCRIPTOR*)(imageBaseAddress+impDescRVA);pImpDesc->Name!=0;pImpDesc++) {
		char* curModuleName=(char*)(imageBaseAddress+pImpDesc->Name);
		moduleNameToFuncToFunc_t::const_iterator i=this->hookRequests.find(curModuleName);
		if(i!=this->hookRequests.end()) {
			printf("_hookFunctionsOnModule: import table for %s: module section for %s: looking for functions to hook\n",moduleName,curModuleName); 
			for(IMAGE_THUNK_DATA* pThunk=(IMAGE_THUNK_DATA*)(imageBaseAddress+(pImpDesc->FirstThunk));pThunk->u1.Function!=0;pThunk++) {
				void* funcAddress=(void*)(pThunk->u1.Function);
				funcToFunc_t::const_iterator j=i->second.find(funcAddress);
				if(j!=i->second.end()) {
					printf("_hookFunctionsOnModule: import table for %s: module section for %s: function at address 0X%X found , changing thunk to use function at address 0X%X\n",moduleName,curModuleName,pThunk->u1.Function,j->second);
					this->hookedFunctions[funcAddress]=pThunk;
					DWORD oldProtect;
					VirtualProtect(pThunk,sizeof(IMAGE_THUNK_DATA),PAGE_READWRITE,&oldProtect);
					pThunk->u1.Function=(UINT_PTR)(j->second);
					VirtualProtect(pThunk,sizeof(IMAGE_THUNK_DATA),oldProtect,&oldProtect);
				}
			}
		} else {
			printf("_hookFunctionsOnModule: import table for %s: module section for %s: no requested hooks\n",moduleName,curModuleName);
		}
	}
	printf("_hookFunctionsOnModule: successfully walked %s's import table, returning true\n",moduleName); 
	return TRUE;
}

void* DllImportTableHooks::requestFunctionHook(const char* moduleName, const char* functionName, void* newHookProc) {
	HMODULE moduleHandle=GetModuleHandleA(moduleName);
	if(!moduleHandle) {
		fprintf(stderr,"apiHook_requestFunctionHook: module %s not loaded\n");
		return NULL;
	}
	void* realFunc=GetProcAddress(moduleHandle,functionName);
	if(!realFunc) {
		fprintf(stderr,"apiHook_requestFunctionHook: function %s does not exist in module %s\n",functionName,moduleName);
		return NULL;
	}
	printf("apiHook_requestFunctionHook: requesting to hook function %s at address 0X%X in module %s at address 0X%X with  new function at address 0X%X\n",functionName,realFunc,moduleName,moduleHandle,newHookProc);
	funcToFunc_t& funcToFunc=this->hookRequests[moduleName];
	funcToFunc_t::iterator i=funcToFunc.find(realFunc);
	void* oldFunc=NULL;
	if(i!=funcToFunc.end()) {
		oldFunc=i->second;
		printf("api_requestHookFunction: hook already exists for function at address 0X%X, setting new hook and returning old one\n",realFunc);
		i->second=newHookProc;
	} else {
		oldFunc=realFunc;
		printf("apiHook_requestFunctionHook: no existing hook for function at address 0X%X, setting hook and returning real function\n",realFunc);
		funcToFunc[realFunc]=newHookProc;
	}
	return oldFunc;
}

BOOL DllImportTableHooks::unhookFunctions() {
	printf("apiHook_unhookFunctions: unhooking all functions\n");
	if(this->hookedFunctions.size()==0) {
		printf("apiHook_unhookFunctions: no functions hooked, returnning true\n");
		return TRUE;
	}
	printf("apiHook_unhookFunctions: unhooking functions on module at address 0X%X\n",targetModule);
	for(funcToThunk_t::iterator i=this->hookedFunctions.begin();i!=this->hookedFunctions.end();i++) {
		printf("apiHook_unhookFunctions: restoring thunk at address 0X%X back to original function at address 0X%X\n",i->second,i->first);
		DWORD oldProtect;
		VirtualProtect(i->second,sizeof(IMAGE_THUNK_DATA),PAGE_READWRITE,&oldProtect);
		i->second->u1.Function=(UINT_PTR)i->first;
		VirtualProtect(i->second,sizeof(IMAGE_THUNK_DATA),oldProtect,&oldProtect);
	}
	this->hookRequests.clear();
	this->hookedFunctions.clear();
	return TRUE;
}
