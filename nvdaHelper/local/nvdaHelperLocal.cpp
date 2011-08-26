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
#include <algorithm>
#include "nvdaHelperLocal.h"
#include "dllImportTableHooks.h"

DllImportTableHooks* oleaccHooks;
DllImportTableHooks* uiaCoreHooks;

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

bool shouldCancelSendMessage;
const UINT CANCELSENDMESSAGE_CHECK_INTERVAL = 400;

void(__stdcall *_notifySendMessageCancelled)();

LRESULT cancellableSendMessageTimeout(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam, UINT fuFlags, UINT uTimeout, PDWORD_PTR lpdwResult) {
	fuFlags |= SMTO_BLOCK | SMTO_ABORTIFHUNG;
	fuFlags &= ~SMTO_NOTIMEOUTIFNOTHUNG;
	shouldCancelSendMessage = false;
	LRESULT ret;
	for (UINT remainingTimeout = uTimeout; remainingTimeout > 0; remainingTimeout -= (remainingTimeout > CANCELSENDMESSAGE_CHECK_INTERVAL) ? CANCELSENDMESSAGE_CHECK_INTERVAL : remainingTimeout) {
		if (shouldCancelSendMessage) {
			_notifySendMessageCancelled();
			SetLastError(ERROR_CANCELLED);
			return 0;
		}
		if ((ret = SendMessageTimeoutW(hwnd, Msg, wParam, lParam, fuFlags, min(remainingTimeout, CANCELSENDMESSAGE_CHECK_INTERVAL), lpdwResult)) != 0 || GetLastError() != ERROR_TIMEOUT) {
			// Success or error other than timeout.
			return ret;
		}
	}
	// Timeout.
	SetLastError(ERROR_TIMEOUT);
	return 0;
}

void cancelSendMessage() {
	shouldCancelSendMessage = true;
}

LRESULT WINAPI fake_SendMessageW(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam) {
	DWORD_PTR result;
	cancellableSendMessageTimeout(hwnd, Msg, wParam, lParam, 0, 60000, &result);
	return (LRESULT)result;
}

LRESULT WINAPI fake_SendMessageTimeoutW(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam, UINT fuFlags, UINT uTimeout, PDWORD_PTR lpdwResult) {
	return cancellableSendMessageTimeout(hwnd, Msg, wParam, lParam, fuFlags, uTimeout, lpdwResult);
}

void nvdaHelperLocal_initialize() {
	// TODO: Should we call startServer() here instead of making the caller call it separately?
	HMODULE oleacc = LoadLibraryA("oleacc.dll");
	if (!oleacc)
		return;
	HMODULE uiaCore = LoadLibraryA("UIAutomationCore.dll");
	if (!uiaCore) {
		FreeLibrary(oleacc);
		return;
	}
	oleaccHooks = new DllImportTableHooks(oleacc);
	oleaccHooks->requestFunctionHook("USER32.dll", "SendMessageW", fake_SendMessageW);
	oleaccHooks->requestFunctionHook("USER32.dll", "SendMessageTimeoutW", fake_SendMessageTimeoutW);
	uiaCoreHooks = new DllImportTableHooks(uiaCore);
	uiaCoreHooks->requestFunctionHook("USER32.dll", "SendMessageW", fake_SendMessageW);
	uiaCoreHooks->requestFunctionHook("USER32.dll", "SendMessageTimeoutW", fake_SendMessageTimeoutW);
	oleaccHooks->hookFunctions();
	uiaCoreHooks->hookFunctions();
}

void nvdaHelperLocal_terminate() {
	oleaccHooks->unhookFunctions();
	uiaCoreHooks->unhookFunctions();
	FreeLibrary(oleaccHooks->targetModule);
	FreeLibrary(uiaCoreHooks->targetModule);
	delete oleaccHooks;
	oleaccHooks = NULL;
	delete uiaCoreHooks;
	uiaCoreHooks = NULL;
}
