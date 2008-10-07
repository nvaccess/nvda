#include <stdio.h>
#include <windows.h>
#include "NVDAControler.h"
#include "NVDAControlClient.h"

int getNVDAVersionString(char** version) {
	RpcTryExcept {
		NVDAControler_getNVDAVersionString(version);
	} RpcExcept(1) {
		return FALSE;
	} RpcEndExcept; 
	return TRUE;
}

int executeAppModuleEvent(const char* event) {
	int res;
	int processID=GetCurrentProcessId();
	RpcTryExcept {
		res=NVDAControler_executeAppModuleEvent(processID,event);
	} RpcExcept(1) {
		return FALSE;
	} RpcEndExcept;
	return res;
}

inprocWorkerHandle_t registerInprocWorker(const char* address) {
	inprocWorkerHandle_t handle;
	int processID=GetCurrentProcessId();
	RpcTryExcept {
		handle=NVDAControler_registerInprocWorker(processID,address);
	} RpcExcept(1) {
		return NULL;
	} RpcEndExcept;
	return handle;
}

void unregisterInprocWorker(inprocWorkerHandle_t handle) {
	RpcTryExcept {
		NVDAControler_unregisterInprocWorker(&handle);
	} RpcExcept(1) {
	} RpcEndExcept;
}

//dll initialization and termination
//Points implicit bindings to the interfaces on the server
#pragma comment(linker,"/entry:_DllMainCRTStartup@12")
BOOL DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	RPC_STATUS status;
	if(reason==DLL_PROCESS_ATTACH) {
		if((status=RpcBindingFromStringBinding("ncalrpc:[NVDAControler]",&bindingHandle_NVDAControler))!=RPC_S_OK) {
			fprintf(stderr,"error calling RpcBindingFromStringBinding, code 0X%X\n",status);
			return FALSE;
		}
	} else if(reason==DLL_PROCESS_DETACH) {
		RpcBindingFree(bindingHandle_NVDAControler);
	}
	return TRUE;
}

//memory allocation functions

void* __RPC_USER midl_user_allocate(size_t size) {
	return malloc(size);
}

void __RPC_USER midl_user_free(void* p) {
	free(p);
}
