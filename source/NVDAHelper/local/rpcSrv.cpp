#include <cstdio>
#include <sstream>
#include <windows.h>
#include <interfaces/nvdaController/nvdaController.h>
#include "rpcSrv.h"

//memory allocation functions

void* __RPC_USER midl_user_allocate(size_t size) {
	return malloc(size);
}

void __RPC_USER midl_user_free(void* p) {
	free(p);
}

RPC_STATUS startServer() {
	RPC_STATUS status;
	//Set the protocol
	status=RpcServerUseProtseqEp((RPC_WSTR)L"ncalrpc",RPC_C_PROTSEQ_MAX_REQS_DEFAULT,(RPC_WSTR)L"nvdaController",NULL);
	//We can ignore the error where the endpoint is already set
	if(status!=RPC_S_OK&&status!=RPC_S_DUPLICATE_ENDPOINT) {
		return status;
	}
	//Register the interfaces
	if((status=RpcServerRegisterIf(nvdaController_NvdaController_v1_0_s_ifspec,NULL,NULL))!=RPC_S_OK) {
		return status;
	}
	//Start listening
	if((status=RpcServerListen(1,RPC_C_LISTEN_MAX_CALLS_DEFAULT,TRUE))!=RPC_S_OK) {
		return status;
	}
	CreateThread(NULL,0,(LPTHREAD_START_ROUTINE)RpcMgmtWaitServerListen,NULL,0,NULL);
	return status;
}

RPC_STATUS stopServer() {
	RPC_STATUS status;
	if((status=RpcServerUnregisterIf(nvdaController_NvdaController_v1_0_s_ifspec,NULL,1))!=RPC_S_OK) {
		return status;
	}
	return RpcMgmtStopServerListening(NULL); 
}
