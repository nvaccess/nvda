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

#include <cassert>
#include <iostream>
#include <set>
#include <windows.h>
#include <libMinHook/MinHook.h>
#include "common/log.h"
#include "apiHook.h"

using namespace std;

typedef multiset<HMODULE> moduleSet_t;
typedef set<void*> functionSet_t;

moduleSet_t g_hookedModules;
functionSet_t g_hookedFunctions;
 
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
		FreeLibrary(moduleHandle);
		return NULL;
	}
	if((res=MH_EnableHook(realFunc))!=MH_OK) {
		LOG_ERROR("MH_EnableHook failed with " << res);
		FreeLibrary(moduleHandle);
		return NULL;
	}
	g_hookedModules.insert(moduleHandle);
	g_hookedFunctions.insert(realFunc);
	LOG_DEBUG("successfully hooked function " << functionName << " in module " << moduleName << " with hook procedure at address 0X" << std::hex << newHookProc << ", returning true");
	return origFunc;
}

BOOL apiHook_inProcess_terminate() {
	int res;
	for(functionSet_t::iterator i=g_hookedFunctions.begin();i!=g_hookedFunctions.end();++i) {
		res=MH_DisableHook(*i);
		assert(res==MH_OK);
	}
	g_hookedFunctions.clear();
	//Give enough time for all hook functions to complete.
	Sleep(250);
	res=MH_Uninitialize();
	assert(res==MH_OK);
	for(moduleSet_t::iterator i=g_hookedModules.begin();i!=g_hookedModules.end();i++) {
		FreeLibrary(*i);
	}
	g_hookedModules.clear();
	return TRUE;
}
