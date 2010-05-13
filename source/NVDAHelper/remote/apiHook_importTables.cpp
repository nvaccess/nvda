#include <cstdio>
#include <string>
#include <set>
#include <map>
#include <string.h>
#include <windows.h>
#include "apiHook.h"
#include <shlwapi.h>
#include <psapi.h>

using namespace std;

typedef map<void*,void*> funcToFunc_t;
typedef map<string,funcToFunc_t> moduleNameToFuncToFunc_t;
typedef map<void*,IMAGE_THUNK_DATA*> funcToThunk_t;
typedef map<HMODULE,funcToThunk_t> moduleToFuncToThunk_t;

moduleNameToFuncToFunc_t g_hookRequests;
moduleToFuncToThunk_t g_hookedFunctions;

BOOL _hookFunctionsOnModule(HMODULE moduleHandle, const moduleNameToFuncToFunc_t& hookRequests, moduleToFuncToThunk_t& hookedFunctions) {
	char moduleName[MAX_PATH];
	GetModuleFileNameA(moduleHandle,moduleName,MAX_PATH);
	PathStripPathA(moduleName);
	printf("_hookFunctionsOnModule: called for %s\n",moduleName);
	UINT_PTR  imageBaseAddress=(UINT_PTR)moduleHandle;
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
		moduleNameToFuncToFunc_t::const_iterator i=hookRequests.find(curModuleName);
		if(i!=hookRequests.end()) {
			printf("_hookFunctionsOnModule: import table for %s: module section for %s: looking for functions to hook\n",moduleName,curModuleName); 
			for(IMAGE_THUNK_DATA* pThunk=(IMAGE_THUNK_DATA*)(imageBaseAddress+(pImpDesc->FirstThunk));pThunk->u1.Function!=0;pThunk++) {
			void* funcAddress=(void*)(pThunk->u1.Function);
			funcToFunc_t::const_iterator j=i->second.find(funcAddress);
				if(j!=i->second.end()) {
					printf("_hookFunctionsOnModule: import table for %s: module section for %s: function at address 0X%X found , changing thunk to use function at address 0X%X\n",moduleName,curModuleName,pThunk->u1.Function,j->second);
					hookedFunctions[moduleHandle][funcAddress]=pThunk;
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

void _forgetHookedFunctionsOnModule(HMODULE moduleHandle, moduleToFuncToThunk_t& hookedFunctions) {
	moduleToFuncToThunk_t::iterator i=hookedFunctions.find(moduleHandle);
	if(i!=hookedFunctions.end()) {
		printf("_forgetHookedFunctionsOnModule: functions are hooked on module at address 0X%X, forgetting about them\n",moduleHandle);
		g_hookedFunctions.erase(i);
	} else {
		printf("_forgetHookedFunctionsOnModule: no functions hooked on module at address 0X%X\n",moduleHandle);
	}
}

typedef HMODULE(WINAPI *LoadLibraryA_funcType)(char*);
LoadLibraryA_funcType real_LoadLibraryA=NULL;
HMODULE WINAPI fake_LoadLibraryA(char* moduleName) {
	printf("fake_LoadLibraryA: called for module %s\n",moduleName);
	HMODULE existingModuleHandle=GetModuleHandleA(moduleName);
	HMODULE moduleHandle=real_LoadLibraryA(moduleName);
	printf("fake_LoadLibraryA: real LoadLibraryA returned module at address 0X%X\n",moduleHandle);
	if(moduleHandle) {
		if(!existingModuleHandle) {
			printf("fake_LoadLibraryA: new module\n");
			g_hookedFunctions.erase(moduleHandle);
			_hookFunctionsOnModule(moduleHandle,g_hookRequests,g_hookedFunctions);
		} else {
			printf("fake_LoadLibraryA: module was already loaded\n");
		}
	}
	return moduleHandle;
}

typedef HMODULE(WINAPI *LoadLibraryW_funcType)(wchar_t*);
LoadLibraryW_funcType real_LoadLibraryW=NULL;
HMODULE WINAPI fake_LoadLibraryW(wchar_t* moduleName) {
	wprintf(L"fake_LoadLibraryW: called for module %s\n",moduleName);
	HMODULE existingModuleHandle=GetModuleHandleW(moduleName);
	HMODULE moduleHandle=real_LoadLibraryW(moduleName);
	printf("fake_LoadLibraryW: real LoadLibraryW returned module at address 0X%X\n",moduleHandle);
	if(moduleHandle) {
		if(!existingModuleHandle) {
			printf("fake_LoadLibraryW: new module\n");
			g_hookedFunctions.erase(moduleHandle);
			_hookFunctionsOnModule(moduleHandle,g_hookRequests,g_hookedFunctions);
		} else {
			printf("fake_LoadLibraryW: module was already loaded\n");
		}
	}
	return moduleHandle;
}

BOOL apiHook_hookFunctions() {
	printf("apiHook_hookFunctions: called\n");
	if(g_hookRequests.size()==0) {
		fprintf(stderr,"apiHook_hookFunctions: no requested functions to hook, returnning true\n");
		return TRUE;
	}
	if((real_LoadLibraryA=(LoadLibraryA_funcType)apiHook_requestFunctionHook("KERNEL32.dll","LoadLibraryA",fake_LoadLibraryA))==NULL) {
		fprintf(stderr,"apiHook_hookFunctions: could not request hook for LoadLibraryA in kernel32, returnning false\n");
		return FALSE;
	}
	if((real_LoadLibraryW=(LoadLibraryW_funcType)apiHook_requestFunctionHook("KERNEL32.dll","LoadLibraryW",fake_LoadLibraryW))==NULL) {
		fprintf(stderr,"apiHook_hookFunctions: could not request hook for LoadLibraryW in kernel32, returnning false\n");
		return FALSE;
	}
	HANDLE curProcess=GetCurrentProcess();
	HMODULE moduleList[1024];
	DWORD dwSizeNeeded;
	if(EnumProcessModules(curProcess,moduleList,1024,&dwSizeNeeded)==0) {
		fprintf(stderr,"apiHook_hookFunctions: error fetching list of all loaded modules, returning false\n");
		return FALSE;
	}
	int moduleCount=dwSizeNeeded/sizeof(HMODULE);
	for(int i=0;i<moduleCount;i++) {
		if(!_hookFunctionsOnModule(moduleList[i],g_hookRequests,g_hookedFunctions)) {
			fprintf(stderr,"apiHook_hookFunctions: error modifying import table for module at address 0X%X, returning false\n",moduleList[i]);
			return FALSE;
		}
	}
	printf("apiHook_hookFunctions: done\n");
	return TRUE;
}

void* apiHook_requestFunctionHook(const char* moduleName, const char* functionName, void* newHookProc) {
	if(g_hookedFunctions.size()>0) {
		fprintf(stderr,"apiHook_requestFunctionHook: functions are currently being hooked, returnning false\n");
		return FALSE;
	}
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
	funcToFunc_t& funcToFunc=g_hookRequests[moduleName];
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

BOOL apiHook_unhookFunctions() {
	printf("apiHook_unhookFunctions: unhooking all functions\n");
	if(g_hookedFunctions.size()==0) {
		printf("apiHook_unhookFunctions: no functions hooked, returnning true\n");
		return TRUE;
	}
	HANDLE curProcess=GetCurrentProcess();
	HMODULE moduleList[1024];
	DWORD dwSizeNeeded;
	if(EnumProcessModules(curProcess,moduleList,1024,&dwSizeNeeded)==0) {
		fprintf(stderr,"apiHook_unhookFunctions: error fetching list of all loaded modules, returning false\n");
		return FALSE;
	}
	int moduleCount=dwSizeNeeded/sizeof(HMODULE);
	for(int index=0;index<moduleCount;index++) {
		moduleToFuncToThunk_t::iterator i=g_hookedFunctions.find(moduleList[index]);
		if(i!=g_hookedFunctions.end()) {
			printf("apiHook_unhookFunctions: unhooking functions on module at address 0X%X\n",i->first);
			for(funcToThunk_t::iterator j=i->second.begin();j!=i->second.end();j++) {
				printf("apiHook_unhookFunctions: restoring thunk at address 0X%X back to original function at address 0X%X\n",j->second,j->first);
				DWORD oldProtect;
				VirtualProtect(j->second,sizeof(IMAGE_THUNK_DATA),PAGE_READWRITE,&oldProtect);
				j->second->u1.Function=(UINT_PTR)j->first;
				VirtualProtect(j->second,sizeof(IMAGE_THUNK_DATA),oldProtect,&oldProtect);
			}
		}
	}
	g_hookRequests.clear();
	g_hookedFunctions.clear();
	return TRUE;
}
