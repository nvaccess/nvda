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
#include <detours/src/detours.h>
#include <remote/nvdaControllerInternal.h>
#include <common/log.h>
#include "dllmain.h"
#include "apiHook.h"

using namespace std;

typedef set<pair<void**, void*>> functionSet_t;

functionSet_t g_hookedFunctions;

bool apiHook_beginTransaction() {
	LOG_DEBUG("Initializing an API hook transaction");
	auto res = DetourTransactionBegin();
	if (res != NO_ERROR) {
		LOG_ERROR("DetourTransactionBegin failed with " << res);
		return false;
	}
	res = DetourUpdateThread(GetCurrentThread());
	if (res != NO_ERROR) {
		LOG_ERROR("DetourUpdateThread failed with " << res);
		DetourTransactionAbort();
		return false;
	}
	return true;
}

bool apiHook_hookFunction(void* realFunction, void* fakeFunction, void** targetPointerRef) {
	if (targetPointerRef == nullptr) {
		return false;
	}
	*targetPointerRef = realFunction;
	LOG_DEBUG("requesting to hook function at address 0X" << std::hex << realFunction << " with  new function at address 0X" << fakeFunction);
	auto res = DetourAttach(targetPointerRef, fakeFunction);
	if(res != NO_ERROR) {
		LOG_ERROR("DetourAttach for function at address 0X" << std::hex << realFunction << " with  new function at address 0X" << fakeFunction << " failed with " << res);
		return false;
	}
	g_hookedFunctions.insert(make_pair(targetPointerRef, fakeFunction));
	LOG_DEBUG("successfully hooked function at address 0X" << std::hex << realFunction << " with  new function at address 0X" << fakeFunction << ", new pointer will be written to variable at address 0X" << std::hex << targetPointerRef << " add transaction commit time");
	return true;
}

bool apiHook_commitTransaction() {
	LOG_DEBUG("About to commit an API hook transaction");
	void** failedPointerRef = nullptr;
	auto res = DetourTransactionCommitEx(&failedPointerRef);
	if (res != NO_ERROR) {
		LOG_ERROR("DetourTransactionCommit failed with " << res << " due to variable at address 0X" << std::hex << failedPointerRef << " that should hold a function pointer");
		return false;
	} 
	LOG_DEBUG("DetourTransactionCommit succeeded");
	return TRUE;
}

bool apiHook_terminate() {
	auto res = apiHook_beginTransaction();
	if (!res) {
		return false;
	}
	long detourRes = NO_ERROR;
	for (const auto& iter : g_hookedFunctions) {
		void** pointerRec = iter.first;
		void* fakeFunc = iter.second;
		LOG_DEBUG("Detaching function hook at address 0X" << std::hex << *pointerRec << " with hook procedure at address 0X" << std::hex << fakeFunc);
		detourRes = DetourDetach(pointerRec, fakeFunc);
		if (detourRes != NO_ERROR) {
			LOG_ERROR("Error detaching function hook at address 0X" << std::hex << *pointerRec << " with hook procedure at address 0X" << std::hex << fakeFunc);
		}
	}
	res = apiHook_commitTransaction();
	if (!res) {
		return false;
	}
	g_hookedFunctions.clear();
	return TRUE;
}
