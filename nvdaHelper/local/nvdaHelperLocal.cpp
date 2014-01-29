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
#include <set>
#include <rpc.h>
#include <sddl.h>
#include <common/log.h>
#include "nvdaControllerInternal.h"
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

const UINT CANCELSENDMESSAGE_CHECK_INTERVAL = 1000;
DWORD mainThreadId = 0;
HANDLE cancelSendMessageEvent = NULL;
void(__stdcall *_notifySendMessageCancelled)() = NULL;
struct BgSendMessageData {
	HANDLE completeEvent;
	HANDLE execEvent;
	HWND hwnd;
	DWORD threadId;
	UINT Msg;
	WPARAM wParam;
	LPARAM lParam;
	UINT fuFlags;
	UINT uTimeout;
	DWORD dwResult;
	DWORD error;
};
BgSendMessageData* bgSendMessageData = NULL;
std::set<DWORD> unresponsiveThreads;
CRITICAL_SECTION unresponsiveThreadsLock;

DWORD WINAPI bgMessageThreadProc(LPVOID param) {
	BgSendMessageData* data = (BgSendMessageData*)param;
	// This thread keeps handling SendMessages until it is abandoned.
	do {
		// The main thread shouldn't bother sending messages to this thread
		// until it has responded to the current message.
		EnterCriticalSection(&unresponsiveThreadsLock);
		unresponsiveThreads.insert(data->threadId);
		LeaveCriticalSection(&unresponsiveThreadsLock);
		// Even though this is a background thread, we still want a timeout
		// to minimise the cancelled messages that hit unresponsive threads.
		// Keep sending this message until the timeout elapses.
		LRESULT ret;
		for (UINT remainingTimeout = data->uTimeout; remainingTimeout > 0; remainingTimeout -= (remainingTimeout > CANCELSENDMESSAGE_CHECK_INTERVAL) ? CANCELSENDMESSAGE_CHECK_INTERVAL : remainingTimeout) {
			if (WaitForSingleObject(data->execEvent, 0) == WAIT_OBJECT_0)
				break; // Cancelled.
			if ((ret = SendMessageTimeoutW(data->hwnd, data->Msg, data->wParam, data->lParam, data->fuFlags, min(remainingTimeout, CANCELSENDMESSAGE_CHECK_INTERVAL), &data->dwResult)) != 0) {
				// Success.
				data->error = 0;
				break;
			} else {
				data->error = GetLastError();
				if (data->error != ERROR_TIMEOUT) {
					// Error other than timeout.
					break;
				}
			}
		}
		EnterCriticalSection(&unresponsiveThreadsLock);
		unresponsiveThreads.erase(data->threadId);
		LeaveCriticalSection(&unresponsiveThreadsLock);
		// Tell the main thread that we're done with this message.
		SetEvent(data->completeEvent);
		// Wait for the next message or abandonment.
		WaitForSingleObject(data->execEvent, INFINITE);
		ResetEvent(data->execEvent);
	} while (data->hwnd);
	// If data->hwnd is NULL, this thread has been abandoned.
	CloseHandle(data->execEvent);
	CloseHandle(data->completeEvent);
	delete data;
	return 0;
}

LRESULT cancellableSendMessageTimeout(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam, UINT fuFlags, UINT uTimeout, PDWORD_PTR lpdwResult) {
	fuFlags |= SMTO_ABORTIFHUNG;
	fuFlags &= ~SMTO_NOTIMEOUTIFNOTHUNG;
	DWORD windowThreadId = GetWindowThreadProcessId(hwnd, NULL);

	if (windowThreadId == mainThreadId || GetCurrentThreadId() != mainThreadId) {
		// We're sending a message to our own thread
		// or we're sending from a thread other than the main thread.
		// We can't do cancellation in this case,
		// but at least shorten the timeout for other threads.
		return SendMessageTimeoutW(hwnd, Msg, wParam, lParam, fuFlags, min(uTimeout, 10000), lpdwResult);
	}

	if (unresponsiveThreads.find(windowThreadId) != unresponsiveThreads.end()) {
		// The target thread is unresponsive.
		SetLastError(ERROR_CANCELLED);
		return 0;
	}

	bool newThread = !bgSendMessageData;
	if (newThread)
		bgSendMessageData = new BgSendMessageData;
	bgSendMessageData->hwnd = hwnd;
	bgSendMessageData->threadId = windowThreadId;
	bgSendMessageData->Msg = Msg;
	bgSendMessageData->wParam = wParam;
	bgSendMessageData->lParam = lParam;
	bgSendMessageData->fuFlags = fuFlags;
	bgSendMessageData->uTimeout = uTimeout;
	bgSendMessageData->dwResult = 0;
	if (newThread) {
		// Create a new SendMessage thread.
		bgSendMessageData->execEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
		bgSendMessageData->completeEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
		HANDLE thread = CreateThread(NULL, 0, bgMessageThreadProc, (LPVOID)bgSendMessageData, 0, NULL);
		CloseHandle(thread);
	} else {
		// Tell the existing SendMessage thread to send this message.
		SetEvent(bgSendMessageData->execEvent);
	}

	HANDLE waitHandles[] = {bgSendMessageData->completeEvent, cancelSendMessageEvent};
	DWORD waitIndex = 0;
	CoWaitForMultipleHandles(0, INFINITE, 2, waitHandles, &waitIndex);
	if (waitIndex == 1) {
		// Cancelled. Abandon the thread.
		bgSendMessageData->hwnd = NULL;
		SetEvent(bgSendMessageData->execEvent);
		bgSendMessageData = NULL;
		SetLastError(ERROR_CANCELLED);
		if (_notifySendMessageCancelled)
			_notifySendMessageCancelled();
		return 0;
	}

	// Got a result.
	if (bgSendMessageData->error != 0) {
		SetLastError(bgSendMessageData->error);
		return 0;
	}
	*lpdwResult = bgSendMessageData->dwResult;
	return 1;
}

void cancelSendMessage() {
	SetEvent(cancelSendMessageEvent);
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
	startServer();
	mainThreadId = GetCurrentThreadId();
	cancelSendMessageEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
	InitializeCriticalSection(&unresponsiveThreadsLock);
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
	if (bgSendMessageData) {
		// Terminate the background SendMessage thread.
		bgSendMessageData->hwnd = NULL;
		SetEvent(bgSendMessageData->execEvent);
	}
	CloseHandle(cancelSendMessageEvent);
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
