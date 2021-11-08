/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2008-2014 NV Access Limited.
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
#include <set>
#include <rpc.h>
#include <sddl.h>
#include <common/log.h>
#include <local/nvdaControllerInternal.h>
#include "nvdaHelperLocal.h"
#include "dllImportTableHooks.h"
#include "rpcsrv.h"

DllImportTableHooks* oleaccHooks = NULL;
DllImportTableHooks* uiaCoreHooks = NULL;

typedef struct _RPC_SECURITY_QOS_V5_W {
  unsigned long Version;
  unsigned long Capabilities;
  unsigned long IdentityTracking;
  unsigned long ImpersonationType;
  unsigned long AdditionalSecurityInfoType;
  union 
      {
      RPC_HTTP_TRANSPORT_CREDENTIALS_W *HttpCredentials;
      } u;
  void *Sid;
  unsigned int EffectiveOnly;
  void *ServerSecurityDescriptor;
} RPC_SECURITY_QOS_V5_W, *PRPC_SECURITY_QOS_V5_W;

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
	//On Windows 8 we must allow AppContainer servers to communicate back to us
	//Detect Windows 8 by looking for RpcServerRegisterIf3
	HANDLE rpcrt4Handle=GetModuleHandle(L"rpcrt4.dll");
	if(rpcrt4Handle&&GetProcAddress((HMODULE)rpcrt4Handle,"RpcServerRegisterIf3")) {
		PSECURITY_DESCRIPTOR psd=NULL;
		ULONG size;
		if(!ConvertStringSecurityDescriptorToSecurityDescriptor(L"D:(A;;GA;;;wd)(A;;GA;;;AC)",SDDL_REVISION_1,&psd,&size)) {
			LOG_ERROR(L"ConvertStringSecurityDescriptorToSecurityDescriptor failed");
			return NULL;
		}
		RPC_SECURITY_QOS_V5_W securityQos={5,0,0,0,0,NULL,NULL,0,psd};
		if((rpcStatus=RpcBindingSetAuthInfoEx(bindingHandle,NULL,RPC_C_AUTHN_LEVEL_DEFAULT,RPC_C_AUTHN_DEFAULT,NULL,0,(RPC_SECURITY_QOS*)&securityQos))!=RPC_S_OK) {
			LOG_ERROR(L"RpcBindingSetAuthInfoEx failed with status "<<rpcStatus);
			return NULL;
		}
	}
	return bindingHandle;
}

const UINT CANCELSENDMESSAGE_CHECK_INTERVAL = 400;
DWORD mainThreadId = 0;
HANDLE cancelCallEvent = NULL;
void(__stdcall *_notifySendMessageCancelled)() = NULL;
struct BgSendMessageData {
	HANDLE completeEvent;
	HANDLE execEvent;
	bool isActive;
	HWND hwnd;
	UINT Msg;
	WPARAM wParam;
	LPARAM lParam;
	UINT fuFlags;
	UINT uTimeout;
	DWORD_PTR dwResult;
	DWORD error;
} bgSendMessageData;

DWORD WINAPI bgSendMessageThreadProc(LPVOID param) {
	// Keep handling messages until terminated.
	for ( ; ; ) {
		// Wait for the next message or abandonment.
		WaitForSingleObject(bgSendMessageData.execEvent, INFINITE);
		if (!bgSendMessageData.hwnd)
			break; // Terminated.
		bgSendMessageData.fuFlags |= SMTO_BLOCK;
		// Keep sending this message until the timeout elapses.
		for (UINT remainingTimeout = bgSendMessageData.uTimeout; remainingTimeout > 0; remainingTimeout -= (remainingTimeout > CANCELSENDMESSAGE_CHECK_INTERVAL) ? CANCELSENDMESSAGE_CHECK_INTERVAL : remainingTimeout) {
			if (WaitForSingleObject(cancelCallEvent, 0) == WAIT_OBJECT_0) {
				// Cancellation has been requested.
				bgSendMessageData.error = ERROR_CANCELLED;
				break;
			}
			if (SendMessageTimeoutW(bgSendMessageData.hwnd, bgSendMessageData.Msg, bgSendMessageData.wParam, bgSendMessageData.lParam, bgSendMessageData.fuFlags, min(remainingTimeout, CANCELSENDMESSAGE_CHECK_INTERVAL), &bgSendMessageData.dwResult) != 0) {
				// Success.
				bgSendMessageData.error = 0;
				break;
			} else {
				bgSendMessageData.error = GetLastError();
				if (bgSendMessageData.error != ERROR_TIMEOUT) {
					// Error other than timeout.
					break;
				}
			}
		}
		// Tell the main thread that we're done with this message.
		SetEvent(bgSendMessageData.completeEvent);
	}
	CloseHandle(bgSendMessageData.execEvent);
	CloseHandle(bgSendMessageData.completeEvent);
	return 0;
}

LRESULT cancellableSendMessageTimeout(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam, UINT fuFlags, UINT uTimeout, PDWORD_PTR lpdwResult) {
	if (!hwnd) {
		// We use HWND NULL to signal that the background thread should die,
		// so we must return before then.
		// We may as well do it as early as possible.
		SetLastError(ERROR_INVALID_WINDOW_HANDLE);
		return 0;
	}

	if (WaitForSingleObject(cancelCallEvent, 0) == WAIT_OBJECT_0) {
		// Already cancelled, so don't bother going any further.
		SetLastError(ERROR_CANCELLED);
		return 0;
	}

	fuFlags |= SMTO_ABORTIFHUNG;
	fuFlags &= ~SMTO_NOTIMEOUTIFNOTHUNG;

	DWORD currentThreadId = GetCurrentThreadId();
	if (currentThreadId == mainThreadId && GetWindowThreadProcessId(hwnd, NULL) == mainThreadId) {
		// We're sending a message to our own thread, so just forward the call.
		return SendMessageTimeoutW(hwnd, Msg, wParam, lParam, fuFlags, uTimeout, lpdwResult);
	}

	if (currentThreadId != mainThreadId) {
		// We're sending from a thread other than the main thread.
		// We don't want to use a background thread in this case,
		// but we can still improve things.
		if (uTimeout > 10000)
			uTimeout = 10000;
		// SMTO_ABORTIFHUNG only aborts if the window is already hung,
		// not if the window hangs while sending.
		LRESULT ret = 0;
		for (UINT remainingTimeout = uTimeout; remainingTimeout > 0; remainingTimeout -= (remainingTimeout > CANCELSENDMESSAGE_CHECK_INTERVAL) ? CANCELSENDMESSAGE_CHECK_INTERVAL : remainingTimeout) {
			if (WaitForSingleObject(cancelCallEvent, 0) == WAIT_OBJECT_0) {
				// Note that cancellation is based on whether the *main* thread is alive.
				if (_notifySendMessageCancelled)
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
		return ret;
	}

	if (bgSendMessageData.isActive) {
		// We can't handle reentrancy.
		SetLastError(ERROR_CANCELLED);
		return 0;
	}

	// #3825: SendMessageTimeout can block until the window responds in some cases despite the timeout,
	// so use a background thread to send messages.
	bgSendMessageData.hwnd = hwnd;
	bgSendMessageData.Msg = Msg;
	bgSendMessageData.wParam = wParam;
	bgSendMessageData.lParam = lParam;
	bgSendMessageData.fuFlags = fuFlags;
	bgSendMessageData.uTimeout = uTimeout;
	bgSendMessageData.dwResult = 0;
	bgSendMessageData.isActive = true;
	// Notify the background thread to send the message.
	SetEvent(bgSendMessageData.execEvent);

	// Wait for the background thread to send the message.
	// It will cancel if appropriate.
	// This function must not return while the SendMessage is in progress,
	// as the caller might free memory used by the message.
	DWORD waitIndex = 0;
	if (fuFlags & SMTO_BLOCK) {
		WaitForSingleObject(bgSendMessageData.completeEvent, INFINITE);
	} else {
		// We need to pump nonqueued messages while waiting.
		// MsgWaitForMultipleObjects can wake for nonqueued messages,
		// but we'd have to manage the actual pump ourselves.
		// CoWaitForMultipleHandles does exactly what we need.
		CoWaitForMultipleHandles(0, INFINITE, 1, &bgSendMessageData.completeEvent, &waitIndex);
	}
	bgSendMessageData.isActive = false;

	// Handle the result.
	if (bgSendMessageData.error != 0) {
		if (bgSendMessageData.error == ERROR_CANCELLED && _notifySendMessageCancelled)
			_notifySendMessageCancelled();
		SetLastError(bgSendMessageData.error);
		return 0;
	}
	*lpdwResult = bgSendMessageData.dwResult;
	return 1;
}

LRESULT WINAPI fake_SendMessageW(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam) {
	DWORD_PTR result = 0;
	cancellableSendMessageTimeout(hwnd, Msg, wParam, lParam, 0, 60000, &result);
	return (LRESULT)result;
}

LRESULT WINAPI fake_SendMessageTimeoutW(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam, UINT fuFlags, UINT uTimeout, PDWORD_PTR lpdwResult) {
	return cancellableSendMessageTimeout(hwnd, Msg, wParam, lParam, fuFlags, uTimeout, lpdwResult);
}

void nvdaHelperLocal_initialize() {
	startServer();
	mainThreadId = GetCurrentThreadId();
	cancelCallEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
	bgSendMessageData.execEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
	bgSendMessageData.completeEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
	bgSendMessageData.isActive = false;
	CloseHandle(CreateThread(NULL, 0, bgSendMessageThreadProc, NULL, 0, NULL));
	HMODULE oleacc = LoadLibraryA("oleacc.dll");
	if (!oleacc)
		return;
	oleaccHooks = new DllImportTableHooks(oleacc);
	oleaccHooks->requestFunctionHook("USER32.dll", "SendMessageW", fake_SendMessageW);
	oleaccHooks->requestFunctionHook("USER32.dll", "SendMessageTimeoutW", fake_SendMessageTimeoutW);
	oleaccHooks->hookFunctions();
	HMODULE uiaCore = LoadLibraryA("UIAutomationCore.dll");
	// It is not an error if UIA isn't present.
	if (uiaCore) {
		uiaCoreHooks = new DllImportTableHooks(uiaCore);
		uiaCoreHooks->requestFunctionHook("USER32.dll", "SendMessageW", fake_SendMessageW);
		uiaCoreHooks->requestFunctionHook("USER32.dll", "SendMessageTimeoutW", fake_SendMessageTimeoutW);
		uiaCoreHooks->hookFunctions();
	}
}

void nvdaHelperLocal_terminate() {
	if (uiaCoreHooks) {
		uiaCoreHooks->unhookFunctions();
		FreeLibrary(uiaCoreHooks->targetModule);
		delete uiaCoreHooks;
		uiaCoreHooks = NULL;
	}
	if (oleaccHooks) {
		oleaccHooks->unhookFunctions();
		FreeLibrary(oleaccHooks->targetModule);
		delete oleaccHooks;
		oleaccHooks = NULL;
	}
	// Terminate the background SendMessage thread.
	bgSendMessageData.hwnd = NULL;
	SetEvent(bgSendMessageData.execEvent);
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
