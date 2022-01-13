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
#include <rpc.h>
#include <sddl.h>
#include <local/nvdaController.h>
#include <local/nvdaControllerInternal.h>
#include <common/winIPCUtils.h>
#include <common/log.h>
#include "rpcSrv.h"

using namespace std;

typedef RPC_STATUS(RPC_ENTRY *RpcServerRegisterIf3_functype)(RPC_IF_HANDLE,UUID __RPC_FAR*,RPC_MGR_EPV __RPC_FAR*,unsigned int,unsigned int,unsigned int,RPC_IF_CALLBACK_FN __RPC_FAR*,void __RPC_FAR*);

RPC_IF_HANDLE availableInterfaces[]={
	nvdaController_NvdaController_v1_0_s_ifspec,
	nvdaControllerInternal_NvdaControllerInternal_v1_0_s_ifspec
};


//memory allocation functions

void* __RPC_USER midl_user_allocate(size_t size) {
	return malloc(size);
}

void __RPC_USER midl_user_free(void* p) {
	free(p);
}

RPC_STATUS startServer() {
	RPC_STATUS status;
	wchar_t desktopSpecificNamespace[64];
	generateDesktopSpecificNamespace(desktopSpecificNamespace,ARRAYSIZE(desktopSpecificNamespace));
	wstring endpointString=L"NvdaCtlr.";
	endpointString+=desktopSpecificNamespace;
	//On Windows 8 the new rpcServerRegisterIf3 must be used along with a security descriptor allowing appContainer access
	HANDLE rpcrt4Handle=GetModuleHandle(L"rpcrt4.dll");
	RpcServerRegisterIf3_functype RpcServerRegisterIf3=(RpcServerRegisterIf3_functype)GetProcAddress((HMODULE)rpcrt4Handle,"RpcServerRegisterIf3");
	PSECURITY_DESCRIPTOR psd=NULL;
	ULONG size;
	if(RpcServerRegisterIf3) {
		if(!ConvertStringSecurityDescriptorToSecurityDescriptor(L"D:(A;;GA;;;wd)(A;;GA;;;AC)",SDDL_REVISION_1,&psd,&size)||!psd) {
			LOG_ERROR(L"ConvertStringSecurityDescriptorToSecurityDescriptor failed, GetLastError is "<<GetLastError());
			return -1;
		}
	}
	status=RpcServerUseProtseqEp((RPC_WSTR)L"ncalrpc",RPC_C_PROTSEQ_MAX_REQS_DEFAULT,(RPC_WSTR)(endpointString.c_str()),psd);
	//We can ignore the error where the endpoint is already set
	if(status!=RPC_S_OK&&status!=RPC_S_DUPLICATE_ENDPOINT) {
		LOG_ERROR(L"RpcUseProtSeqEp failed with status "<<status);
		return status;
	}
	//Register the interfaces
	if(RpcServerRegisterIf3) { //Windows 8
		for(int i=0;i<ARRAYSIZE(availableInterfaces);i++) {
			if((status=RpcServerRegisterIf3(availableInterfaces[i],NULL,NULL,RPC_IF_AUTOLISTEN|RPC_IF_ALLOW_CALLBACKS_WITH_NO_AUTH,RPC_C_LISTEN_MAX_CALLS_DEFAULT,0,NULL,psd))!=RPC_S_OK) {
				LOG_ERROR(L"RpcServerRegisterIf3 failed to register interface at index "<<i<<L", status "<<status);
				return status;
			}
		}
	} else { // Pre Windows 8
		for(int i=0;i<ARRAYSIZE(availableInterfaces);i++) {
			if((status=RpcServerRegisterIfEx(availableInterfaces[i],NULL,NULL,RPC_IF_AUTOLISTEN,RPC_C_LISTEN_MAX_CALLS_DEFAULT,NULL))!=RPC_S_OK) {
				LOG_ERROR(L"RpcServerRegisterIf failed to register interface at index "<<i<<L", status "<<status);
				return status;
			}
		}
	}
	LocalFree(psd);
	return status;
}

RPC_STATUS stopServer() {
	RPC_STATUS status;
	for(int i=0;i<ARRAYSIZE(availableInterfaces);i++) {
		if((status=RpcServerUnregisterIf(availableInterfaces[i],NULL,1))!=RPC_S_OK) {
			LOG_ERROR(L"RpcServerUnregisterIf failed to unregister interface at index "<<i<<L", status "<<status);
			return status;
		}
	}
	return status;
}
