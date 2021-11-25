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
#include <DbgHelp.h>
#include <remote/nvdaControllerInternal.h>
#include <common/log.h>
#include <remote/vbufRemote.h>
#include <remote/displayModelRemote.h>
#include <remote/NvdaInProcUtils.h>
#include <remote/nvdaControllerInternal.h>
#include "rpcSrv.h"

typedef RPC_STATUS(RPC_ENTRY *RpcServerRegisterIf3_functype)(RPC_IF_HANDLE,UUID __RPC_FAR*,RPC_MGR_EPV __RPC_FAR*,unsigned int,unsigned int,unsigned int,RPC_IF_CALLBACK_FN __RPC_FAR*,void __RPC_FAR*);

RPC_IF_HANDLE availableInterfaces[]={
	nvdaInProcUtils_NvdaInProcUtils_v1_0_s_ifspec,
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

HANDLE nvdaUnregisteredEvent=NULL;
RPC_BINDING_VECTOR* bindingVector;
UUID nvdaInprocUuid;

RPC_STATUS rpcSrv_initialize() {
	nvdaUnregisteredEvent=CreateEvent(NULL,TRUE,true,NULL);
	RPC_STATUS status;
	//Set the protocol
	status=RpcServerUseProtseq((RPC_WSTR)L"ncalrpc",RPC_C_PROTSEQ_MAX_REQS_DEFAULT,NULL);
	//We can ignore the error where the endpoint is already set
	if(status!=RPC_S_OK&&status!=RPC_S_DUPLICATE_ENDPOINT) {
		LOG_ERROR(L"Unable to use RPC endPoint. RPC error "<<status); 
		return status;
	}
	if((status=RpcServerInqBindings(&bindingVector))!=RPC_S_OK) {
		LOG_ERROR(L"RpcServerInqBindings failed with status "<<status);
		return status;
	}
	UuidCreate(&nvdaInprocUuid);
	UUID_VECTOR nvdaInprocUuidVector={1,&nvdaInprocUuid};
	//Register the interfaces
	for(int i=0;i<ARRAYSIZE(availableInterfaces);++i) {
		if((status=RpcServerRegisterIfEx(availableInterfaces[i],NULL,NULL,RPC_IF_AUTOLISTEN,RPC_C_LISTEN_MAX_CALLS_DEFAULT,NULL))!=RPC_S_OK) {
			LOG_ERROR(L"RpcServerRegisterIfEx for interface at index "<<i<<L" failed with status "<<status);
			continue;
		}
		if((status=RpcEpRegister(availableInterfaces[i],bindingVector,&nvdaInprocUuidVector,(RPC_WSTR)L"NVDAHelperRemote interface"))!=RPC_S_OK) {
			LOG_ERROR(L"RpcEpRegister failed for interface at index "<<i<<L" with status "<<status);
			continue;
		}
	}
	RPC_WSTR uuidString;
	UuidToString(&nvdaInprocUuid,&uuidString);
	RpcBindingSetObject(nvdaControllerInternalBindingHandle,&nvdaInprocUuid);
	if((status=nvdaControllerInternal_requestRegistration((wchar_t*)uuidString))!=RPC_S_OK) {
		LOG_ERROR(L"nvdaControllerInternal_requestRegistration failed with status "<<status);
	}
	RpcStringFree(&uuidString);
	return status;
}

void rpcSrv_terminate() {
	RPC_STATUS status;
	CloseHandle(nvdaUnregisteredEvent);
	nvdaUnregisteredEvent=NULL;
	UUID_VECTOR nvdaInprocUuidVector={1,&nvdaInprocUuid};
	for(int i=0;i<ARRAYSIZE(availableInterfaces);++i) {
		if((status=RpcEpUnregister(availableInterfaces[i],bindingVector,&nvdaInprocUuidVector))!=RPC_S_OK) {
			LOG_ERROR(L"RpcEpUnregister failed for interface at index "<<i<<L" with status "<<status);
		}
		if((status=RpcServerUnregisterIfEx(availableInterfaces[i],NULL,1))!=RPC_S_OK) {
			LOG_ERROR(L"RpcServerUnregisterIfEx for interface at index "<<i<<L" failed with status "<<status);
		}
	}
	RpcBindingVectorFree(&bindingVector);
}

error_status_t nvdaInProcUtils_registerNVDAProcess(handle_t bindingHandle, nvdaRegistrationHandle_t* registrationHandle) {
	ResetEvent(nvdaUnregisteredEvent);
	*registrationHandle=&nvdaUnregisteredEvent;
	return RPC_S_OK;
}

error_status_t nvdaInProcUtils_unregisterNVDAProcess(nvdaRegistrationHandle_t* registrationHandle) {
	SetEvent(nvdaUnregisteredEvent);
	*registrationHandle=NULL;
	return RPC_S_OK;
}

void __RPC_USER nvdaRegistrationHandle_t_rundown(nvdaRegistrationHandle_t registrationHandle) {
	nvdaInProcUtils_unregisterNVDAProcess(&registrationHandle);
}

error_status_t nvdaInProcUtils_getActiveObject(handle_t bindingHandle, const wchar_t* progid, IUnknown** ppUnknown) {
	if(!progid) {
		LOG_DEBUGWARNING(L"NULL progid");
		return E_FAIL;
	}
	IID clsid;
	HRESULT res=CLSIDFromString(progid,&clsid);
	if(res!=NOERROR) {
		LOG_DEBUGWARNING(L"CLSIDFromString for "<<progid<<L" returned "<<res);
		return res;
	}
	return GetActiveObject(clsid,NULL,ppUnknown);
}

std::wstring minidumpPath;

LONG WINAPI crashHandler(LPEXCEPTION_POINTERS exceptionInfo) {
	HANDLE mdf = CreateFile(minidumpPath.c_str(), GENERIC_WRITE, 0, NULL,
		CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	if (mdf == INVALID_HANDLE_VALUE)
		return EXCEPTION_CONTINUE_SEARCH;
	MINIDUMP_EXCEPTION_INFORMATION mdExc;
	mdExc.ThreadId = GetCurrentThreadId();
	mdExc.ExceptionPointers = exceptionInfo;
	mdExc.ClientPointers = FALSE;
	MiniDumpWriteDump(
		GetCurrentProcess(), GetCurrentProcessId(),
		mdf,
		MiniDumpNormal,
		&mdExc, NULL, NULL);
	CloseHandle(mdf);
	return EXCEPTION_CONTINUE_SEARCH;
}

error_status_t nvdaInProcUtils_dumpOnCrash(handle_t bindingHandle, const wchar_t* path) {
	if (!path)
		return E_FAIL;
	minidumpPath = path;
	SetUnhandledExceptionFilter(crashHandler);
	return S_OK;
}
