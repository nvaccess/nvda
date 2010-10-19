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
#include <sstream>
#include "nvdaHelperLocal.h"
#include "dllImportTableHooks.h"

DllImportTableHooks* oleaccHooks;

handle_t createConnection(int processID) {
	RPC_STATUS rpcStatus;
	std::wostringstream addr;
	addr<<L"ncalrpc:[nvdaHelperRemote_"<<processID<<L"]";
	handle_t bindingHandle;
	if((rpcStatus=RpcBindingFromStringBinding((RPC_WSTR)(addr.str().c_str()),&bindingHandle))!=RPC_S_OK) {
		fprintf(stderr,"Error creating binding handle from string binding, rpc code 0X%X\n",rpcStatus);
		return NULL;
	} 
	return bindingHandle;
}

void destroyConnection(handle_t bindingHandle) {
	RpcBindingFree(&bindingHandle);
}

LRESULT WINAPI fake_SendMessageW(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam) {
	DWORD_PTR result;
	if (SendMessageTimeoutW(hwnd, Msg, wParam, lParam, SMTO_ABORTIFHUNG, 1000, &result) == 0 && GetLastError() == ERROR_TIMEOUT) {
		Beep(880,50);
		RaiseException(ERROR_TIMEOUT, EXCEPTION_NONCONTINUABLE, 0, NULL);
	}
	return (LRESULT)result;
}

LRESULT WINAPI fake_SendMessageTimeoutW(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam, UINT fuFlags, UINT uTimeout, PDWORD_PTR lpdwResult) {
	if (uTimeout > 2000)
		uTimeout = 2000;
	return SendMessageTimeoutW(hwnd, Msg, wParam, lParam, fuFlags, uTimeout, lpdwResult);
}

void nvdaHelperLocal_initialize() {
	// TODO: Should we call startServer() here instead of making the caller call it separately?
	HMODULE oleacc = LoadLibraryA("oleacc.dll");
	if (!oleacc)
		return;
	oleaccHooks = new DllImportTableHooks(oleacc);
	oleaccHooks->requestFunctionHook("USER32.dll", "SendMessageW", fake_SendMessageW);
	oleaccHooks->requestFunctionHook("USER32.dll", "SendMessageTimeoutW", fake_SendMessageTimeoutW);
	oleaccHooks->hookFunctions();
}

void nvdaHelperLocal_terminate() {
	oleaccHooks->unhookFunctions();
	FreeLibrary(oleaccHooks->targetModule);
	delete oleaccHooks;
	oleaccHooks = NULL;
}
