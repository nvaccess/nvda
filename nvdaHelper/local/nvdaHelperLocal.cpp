/*
A part of NonVisual Desktop Access (NVDA)
Copyright (C) 2008-2023 NV Access Limited
This file may be used under the terms of the GNU General Public License, version 2 or later.
For more details see: https://www.gnu.org/licenses/gpl-2.0.html
*/

#include <cstdio>
#include <sstream>
#include <algorithm>
#include <rpc.h>
#include <sddl.h>
#include <common/log.h>
#include <common/apiHook.h>
#include <local/nvdaControllerInternal.h>
#include "nvdaHelperLocal.h"
#include "dllImportTableHooks.h"
#include "rpcsrv.h"

decltype(&SendMessageW) real_SendMessageW = nullptr;
decltype(&SendMessageTimeoutW) real_SendMessageTimeoutW = nullptr;
decltype(&OpenClipboard) real_OpenClipboard = nullptr;


handle_t createRemoteBindingHandle(wchar_t* uuidString) {
	RPC_STATUS rpcStatus;
	RPC_WSTR stringBinding;
	if((rpcStatus=RpcStringBindingCompose((RPC_WSTR)uuidString,(RPC_WSTR)L"ncalrpc",NULL,NULL,NULL,&stringBinding))!=RPC_S_OK) {
		LOG_ERROR(L"RpcStringBindingCompose failed with status "<<rpcStatus);
		return NULL;
	}
	handle_t bindingHandle;
	if((rpcStatus=RpcBindingFromStringBinding(stringBinding,&bindingHandle))!=RPC_S_OK) {
		LOG_ERROR(L"RpcBindingFromStringBinding failed with status "<<rpcStatus);
		return NULL;
	}
	PSECURITY_DESCRIPTOR psd = nullptr;
	ULONG size;
	if (!ConvertStringSecurityDescriptorToSecurityDescriptor(L"D:(A;;GA;;;wd)(A;;GA;;;AC)", SDDL_REVISION_1, &psd, &size)) {
		LOG_ERROR(L"ConvertStringSecurityDescriptorToSecurityDescriptor failed");
		return NULL;
	}
	RPC_SECURITY_QOS_V5_W securityQos = {5, 0, 0, 0, 0, nullptr, nullptr, 0, psd};
	if ((rpcStatus = RpcBindingSetAuthInfoEx(
		bindingHandle, nullptr, RPC_C_AUTHN_LEVEL_DEFAULT, RPC_C_AUTHN_DEFAULT, nullptr, 0,
		(RPC_SECURITY_QOS*)&securityQos)
	) != RPC_S_OK) {
		LOG_ERROR(L"RpcBindingSetAuthInfoEx failed with status " << rpcStatus);
		return NULL;
	}
	return bindingHandle;
}

const UINT CANCELSENDMESSAGE_CHECK_INTERVAL = 400;
DWORD mainThreadId = 0;
HANDLE cancelCallEvent = NULL;
void(__stdcall *_notifySendMessageCancelled)() = NULL;

LRESULT cancellableSendMessageTimeout(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam, UINT fuFlags, UINT uTimeout, PDWORD_PTR lpdwResult) {
	if (!hwnd) {
		// Return as early as possible when no hwnd is given.
		SetLastError(ERROR_INVALID_WINDOW_HANDLE);
		return 0;
	}

	DWORD currentThreadId = GetCurrentThreadId();
	if (GetWindowThreadProcessId(hwnd, NULL) == currentThreadId) {
		// We're sending a message to the current thread, so just forward the call.
		return real_SendMessageTimeoutW(hwnd, Msg, wParam, lParam, fuFlags, uTimeout, lpdwResult);
	}

	if (WaitForSingleObject(cancelCallEvent, 0) == WAIT_OBJECT_0) {
		// Already cancelled, so don't bother going any further.
		SetLastError(ERROR_CANCELLED);
		return 0;
	}
	if (Msg < WM_APP || Msg > 0xBFFF) {
		// Message in the range 0x8000 through 0xBFFF are available for applications to use as private messages.
		// Setting the SMTO_ABORTIFHUNG for these messages is known to cause problems, for example with SAPI5 (#15082)
		fuFlags |= SMTO_ABORTIFHUNG;
	}
	fuFlags &= ~SMTO_NOTIMEOUTIFNOTHUNG;

	if (uTimeout > 10000) {
		uTimeout = 10000;
	}
	// SMTO_ABORTIFHUNG only aborts if the window is already hung,
	// not if the window hangs while sending.
	LRESULT ret = 0;
	for (UINT remainingTimeout = uTimeout; remainingTimeout > 0; remainingTimeout -= (remainingTimeout > CANCELSENDMESSAGE_CHECK_INTERVAL) ? CANCELSENDMESSAGE_CHECK_INTERVAL : remainingTimeout) {
		if (WaitForSingleObject(cancelCallEvent, 0) == WAIT_OBJECT_0) {
			// Note that cancellation is based on whether the *main* thread is alive.
			if (_notifySendMessageCancelled) {
				_notifySendMessageCancelled();
			}
			SetLastError(ERROR_CANCELLED);
			return 0;
		}
		if ((ret = real_SendMessageTimeoutW(hwnd, Msg, wParam, lParam, fuFlags, std::min(remainingTimeout, CANCELSENDMESSAGE_CHECK_INTERVAL), lpdwResult)) != 0 || GetLastError() != ERROR_TIMEOUT) {
			// Success or error other than timeout.
			return ret;
		}
	}
	// Timeout.
	return ret;
}

LRESULT WINAPI fake_SendMessageW(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam) {
	DWORD_PTR result = 0;
	cancellableSendMessageTimeout(hwnd, Msg, wParam, lParam, 0, 60000, &result);
	return (LRESULT)result;
}

LRESULT WINAPI fake_SendMessageTimeoutW(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam, UINT fuFlags, UINT uTimeout, PDWORD_PTR lpdwResult) {
	return cancellableSendMessageTimeout(hwnd, Msg, wParam, lParam, fuFlags, uTimeout, lpdwResult);
}

//A replacement OpenClipboard function to disable the use of the clipboard in a secure mode NVDA process
//Simply returns false without calling the original OpenClipboard
BOOL WINAPI fake_OpenClipboard(HWND hwndOwner) {
	return false;
}

void nvdaHelperLocal_initialize(bool secureMode) {
	startServer();
	mainThreadId = GetCurrentThreadId();
	cancelCallEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
	// Begin API hooking transaction
	apiHook_beginTransaction();
	// Hook SendMessageW and SendMessageTimeoutW to ensure that
	// we can cancel such calls when they would otherwise freeze NVDA's process.
	apiHook_hookFunction_safe(SendMessageW, fake_SendMessageW, &real_SendMessageW);
	apiHook_hookFunction_safe(SendMessageTimeoutW, fake_SendMessageTimeoutW, &real_SendMessageTimeoutW);
	// For secure mode NVDA process, hook OpenClipboard to disable usage of the clipboard
	if (secureMode) {
		apiHook_hookFunction_safe(OpenClipboard, fake_OpenClipboard, &real_OpenClipboard);
	}
	// Enable all registered API hooks by committing the transaction
	apiHook_commitTransaction();
}

void nvdaHelperLocal_terminate() {
	// Unregister and terminate API hooks
	apiHook_terminate();
	CloseHandle(cancelCallEvent);
	stopServer();
}

void logMessage(int level, const wchar_t* msg) {
	nvdaControllerInternal_logMessage(level,0,msg);
}

typedef struct {
	wchar_t wantedClass[256];
	BOOL checkVisible;
	HWND foundWindow;
	wchar_t tempClass[256];
} _fwct_info;

BOOL CALLBACK _fwct_enumThreadWindowsProc(HWND hwnd, LPARAM lParam) {
	_fwct_info* info=(_fwct_info*)lParam;
	if(!(info->checkVisible)||IsWindowVisible(hwnd)) {
		GetClassName(hwnd,info->tempClass,ARRAYSIZE(info->tempClass));
		if(wcscmp(info->tempClass,info->wantedClass)==0) {
			info->foundWindow=hwnd;
			return FALSE;
		}
	}
	EnumChildWindows(hwnd,_fwct_enumThreadWindowsProc,lParam);
	return !(info->foundWindow);
}

HWND findWindowWithClassInThread(long threadID, wchar_t* windowClassName,BOOL checkVisible) {
	_fwct_info info={0};
	info.checkVisible=checkVisible;
	wcscpy(info.wantedClass,windowClassName);
	EnumThreadWindows(threadID,_fwct_enumThreadWindowsProc,(LPARAM)&info);
	return info.foundWindow;
}
