#include <iostream>
#include <set>
#include <windows.h>
#include <libMinHook/MinHook.h>
#include "common/log.h"
#include "apiHook.h"

using namespace std;

typedef multiset<HMODULE> moduleSet_t;

moduleSet_t g_hookedModules;

bool apiHook_inProcess_initialize() {
	LOG_DEBUG("calling MH_Initialize");
	int res;
	if ((res=MH_Initialize())!=MH_OK) {
		LOG_ERROR("MH_CreateHook failed with " << res);
		return false;
	} 
	else return true;
}

void* apiHook_hookFunction(const char* moduleName, const char* functionName, void* newHookProc) {
	HMODULE moduleHandle=LoadLibraryA(moduleName);
	if(!moduleHandle) {
		LOG_ERROR("module " << moduleName << " not loaded");
		return NULL;
	}
	void* realFunc=GetProcAddress(moduleHandle,functionName);
	if(!realFunc) {
		LOG_ERROR("function " << functionName << " does not exist in module " << moduleName);
		FreeLibrary(moduleHandle);
		return NULL;
	}
	LOG_DEBUG("requesting to hook function " << functionName << " at address 0X" << std::hex << realFunc << " in module " << moduleName << " at address 0X" << moduleHandle << " with  new function at address 0X" << newHookProc);
	void* origFunc;
	int res;
	if((res=MH_CreateHook(realFunc,newHookProc,&origFunc))!=MH_OK) {
		LOG_ERROR("MH_CreateHook failed with " << res);
		return NULL;
	}
	if((res=MH_EnableHook(realFunc))!=MH_OK) {
		LOG_ERROR("MH_EnableHook failed with " << res);
		return NULL;
	}
	g_hookedModules.insert(moduleHandle);
	LOG_DEBUG("successfully hooked function " << functionName << " in module " << moduleName << " with hook procedure at address 0X" << std::hex << newHookProc << ", returning true");
	return origFunc;
}

BOOL apiHook_inProcess_terminate() {
	int res;
	if ((res=MH_Uninitialize())!=MH_OK) 
		LOG_ERROR("MH_Uninitialize failed with " << res);
	for(moduleSet_t::iterator i=g_hookedModules.begin();i!=g_hookedModules.end();i++) {
		FreeLibrary(*i);
	}
	g_hookedModules.clear();
	return TRUE;
}
