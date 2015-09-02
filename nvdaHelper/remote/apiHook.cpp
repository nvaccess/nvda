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

#include <iostream>
#include <set>
#define WIN32_LEAN_AND_MEAN 
#include <windows.h>
#include <delayimp.h>
#include <minhook/include/minhook.h>
#include "nvdaControllerInternal.h"
#include <common/log.h>
#include "dllmain.h"
#include "apiHook.h"

using namespace std;

typedef multiset<HMODULE> moduleSet_t;
typedef set<void*> functionSet_t;

moduleSet_t g_hookedModules;
functionSet_t g_hookedFunctions;
HMODULE minhookLibHandle=NULL;
bool error_setNHFP=false;

//function pointer typedefs for all minHook functions for use with getProcAddress
typedef MH_STATUS(WINAPI *MH_Initialize_funcType)();
typedef MH_STATUS(WINAPI *MH_Uninitialize_funcType)();
typedef MH_STATUS(WINAPI *MH_CreateHook_funcType)(void*,void*,void**);
typedef MH_STATUS(WINAPI *MH_EnableHook_funcType)(void*);
typedef MH_STATUS(WINAPI *MH_DisableHook_funcType)(void*);

#define defMHFP(funcName) funcName##_funcType funcName##_fp=NULL

#define setMHFP(funcName) {\
	funcName##_fp=(funcName##_funcType)GetProcAddress(minhookLibHandle,#funcName);\
	if(!funcName##_fp) {\
		error_setNHFP=true;\
		LOG_ERROR(L"Error setting minHook function pointer "<<L#funcName);\
	}\
}

defMHFP(MH_Initialize);
defMHFP(MH_Uninitialize);
defMHFP(MH_CreateHook);
defMHFP(MH_EnableHook);
defMHFP(MH_DisableHook);

 bool apiHook_initialize() {
	LOG_DEBUG("calling MH_Initialize");
	int res;
	wstring dllPath=dllDirectory;
	dllPath+=L"\\minhook.dll";
	if((minhookLibHandle=LoadLibrary(dllPath.c_str()))==NULL) {
		LOG_ERROR(L"LoadLibrary failed to load "<<dllPath);
		return false;
	}
	error_setNHFP=false;
	setMHFP(MH_Initialize);
	setMHFP(MH_Uninitialize);
	setMHFP(MH_CreateHook);
	setMHFP(MH_EnableHook);
	setMHFP(MH_DisableHook);
	if(error_setNHFP) {
		LOG_ERROR(L"Error setting minHook function pointers");
		FreeLibrary(minhookLibHandle);
		minhookLibHandle=NULL;
		return false;
	}
	if ((res=MH_Initialize_fp())!=MH_OK) {
		LOG_ERROR("MH_CreateHook failed with " << res);
		FreeLibrary(minhookLibHandle);
		minhookLibHandle=NULL;
		return false;
	} 
	else return true;
}

void* apiHook_hookFunction(const char* moduleName, const char* functionName, void* newHookProc) {
	if(!minhookLibHandle) {
		LOG_ERROR(L"apiHooks not initialized");
		return NULL;
	}
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
	if((res=MH_CreateHook_fp(realFunc,newHookProc,&origFunc))!=MH_OK) {
		LOG_ERROR("MH_CreateHook failed with " << res);
		FreeLibrary(moduleHandle);
		return NULL;
	}
	g_hookedModules.insert(moduleHandle);
	g_hookedFunctions.insert(realFunc);
	LOG_DEBUG("successfully hooked function " << functionName << " in module " << moduleName << " with hook procedure at address 0X" << std::hex << newHookProc << ", returning true");
	return origFunc;
}

bool apiHook_enableHooks() {
	int res;
	if(!minhookLibHandle) {
		LOG_ERROR(L"apiHooks not initialized");
		return false;
	}
	res=MH_EnableHook_fp(MH_ALL_HOOKS);
	nhAssert(res==MH_OK);
	return TRUE;
}

bool apiHook_terminate() {
	int res;
	//If the process is exiting then minHook will have already removed all hooks and unloaded
	if(isProcessExiting) return true;
	if(!minhookLibHandle) {
		LOG_ERROR(L"apiHooks not initialized");
		return false;
	}
	res=MH_DisableHook_fp(MH_ALL_HOOKS);
	nhAssert(res==MH_OK);
	g_hookedFunctions.clear();
	//Give enough time for all hook functions to complete.
	Sleep(250);
	res=MH_Uninitialize_fp();
	nhAssert(res==MH_OK);
	for(moduleSet_t::iterator i=g_hookedModules.begin();i!=g_hookedModules.end();++i) {
		FreeLibrary(*i);
	}
	g_hookedModules.clear();
	FreeLibrary(minhookLibHandle);
	minhookLibHandle=NULL;
	return TRUE;
}
