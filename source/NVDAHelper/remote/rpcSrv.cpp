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

RPC_STATUS startServer() {
	RPC_STATUS status;
	//Set the protocol
	std::wostringstream endPoint;
	endPoint<<L"nvdaHelperRemote_"<<GetCurrentProcessId();
	status=RpcServerUseProtseqEp((RPC_WSTR)L"ncalrpc",RPC_C_PROTSEQ_MAX_REQS_DEFAULT,(RPC_WSTR)(endPoint.str().c_str()),NULL);
	//We can ignore the error where the endpoint is already set
	if(status!=RPC_S_OK&&status!=RPC_S_DUPLICATE_ENDPOINT) {
		fprintf(stderr,"Error setting protocol\n");
		return status;
	}
	//Register the interfaces
	for(int i=0;i<ARRAYSIZE(availableInterfaces);i++) {
		if((status=RpcServerRegisterIf(availableInterfaces[i],NULL,NULL))!=RPC_S_OK) {
			return status;
		}
	}
	if((status=RpcServerRegisterIf(VBufRemote_VBuf_v2_0_s_ifspec,NULL,NULL))!=RPC_S_OK) {
		fprintf(stderr,"Error registering interface, code 0X%X\n",status);
		return status;
	}
	printf("done\n");
	//Start listening
	printf("starting server\n");
	if((status=RpcServerListen(1,RPC_C_LISTEN_MAX_CALLS_DEFAULT,TRUE))!=RPC_S_OK) {
		fprintf(stderr,"Error starting, code 0X%X\n",status);
		return status;
	}
	CreateThread(NULL,0,(LPTHREAD_START_ROUTINE)RpcMgmtWaitServerListen,NULL,0,NULL);
	return status;
}

RPC_STATUS stopServer() {
	RPC_STATUS status;
	printf("unregistering interface...\n");
	for(int i=0;i<ARRAYSIZE(availableInterfaces);i++) {
		if((status=RpcServerUnregisterIf(availableInterfaces[i],NULL,1))!=RPC_S_OK) {
			return status;
		}
	}
	return RpcMgmtStopServerListening(NULL); 
}

void rpcSrv_inProcess_initialize() {
	startServer();
}

void rpcSrv_inProcess_terminate() {
	stopServer();
}

