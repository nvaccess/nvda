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
#include <cstdio>
#include <sstream>
#include <windows.h>
#include "vbufRemote.h"
#include "displayModelRemote.h"
#include "rpcSrv.h"

RPC_IF_HANDLE availableInterfaces[]={
	displayModelRemote_DisplayModel_v1_0_s_ifspec,
	VBufRemote_VBuf_v2_0_s_ifspec,
};

//memory allocation functions

void* __RPC_USER midl_user_allocate(size_t size) {
	return malloc(size);
}

void __RPC_USER midl_user_free(void* p) {
	free(p);
}

void rpcSrv_inProcess_initialize() {
	RPC_STATUS status;
	//Set the protocol
	std::wostringstream endPoint;
	endPoint<<L"nvdaHelperRemote_"<<GetCurrentProcessId();
	status=RpcServerUseProtseqEp((RPC_WSTR)L"ncalrpc",RPC_C_PROTSEQ_MAX_REQS_DEFAULT,(RPC_WSTR)(endPoint.str().c_str()),NULL);
	assert(status==RPC_S_OK||status==RPC_S_DUPLICATE_ENDPOINT);
	//Register the interfaces
	for(int i=0;i<ARRAYSIZE(availableInterfaces);i++) {
		status=RpcServerRegisterIfEx(availableInterfaces[i],NULL,NULL,RPC_IF_AUTOLISTEN,RPC_C_LISTEN_MAX_CALLS_DEFAULT,NULL);
		assert(status==RPC_S_OK);
	}
}

void rpcSrv_inProcess_terminate() {
	RPC_STATUS status;
	for(int i=0;i<ARRAYSIZE(availableInterfaces);i++) {
		status=RpcServerUnregisterIfEx(availableInterfaces[i],NULL,1);
		assert(status==RPC_S_OK);
	}
}
