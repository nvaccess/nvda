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
#include <rpc.h>
#include <sddl.h>
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
		fprintf(stderr,"RpcStringBindingCompose failed, rpc code 0X%X\n",rpcStatus);
		return NULL;
	}
	handle_t bindingHandle;
	if((rpcStatus=RpcBindingFromStringBinding(stringBinding,&bindingHandle))!=RPC_S_OK) {
		fprintf(stderr,"Error creating binding handle from string binding, rpc code 0X%X\n",rpcStatus);
		return NULL;
	} 
	PSECURITY_DESCRIPTOR psd=NULL;
	ULONG size;
	if(!ConvertStringSecurityDescriptorToSecurityDescriptor(L"D:(A;;GA;;;wd)(A;;GA;;;AC)",SDDL_REVISION_1,&psd,&size)) {
		return NULL;
	}
	RPC_SECURITY_QOS_V5_W securityQos={5,0,0,0,0,NULL,NULL,0,psd};
	if(RpcBindingSetAuthInfoEx(bindingHandle,NULL,RPC_C_AUTHN_LEVEL_DEFAULT,RPC_C_AUTHN_DEFAULT,NULL,0,(RPC_SECURITY_QOS*)&securityQos)!=RPC_S_OK) {
		return NULL;
	}
	return bindingHandle;
}

bool shouldCancelSendMessage;
const UINT CANCELSENDMESSAGE_CHECK_INTERVAL = 400;

void(__stdcall *_notifySendMessageCancelled)() = NULL;

LRESULT cancellableSendMessageTimeout(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam, UINT fuFlags, UINT uTimeout, PDWORD_PTR lpdwResult) {
	fuFlags |= SMTO_BLOCK | SMTO_ABORTIFHUNG;
	fuFlags &= ~SMTO_NOTIMEOUTIFNOTHUNG;
	shouldCancelSendMessage = false;
	LRESULT ret;
	for (UINT remainingTimeout = uTimeout; remainingTimeout > 0; remainingTimeout -= (remainingTimeout > CANCELSENDMESSAGE_CHECK_INTERVAL) ? CANCELSENDMESSAGE_CHECK_INTERVAL : remainingTimeout) {
		if (shouldCancelSendMessage) {
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
	startServer();
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
	stopServer();
}
