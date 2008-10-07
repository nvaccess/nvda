#include <stdio.h>
#include "NVDAControler.h"

#define DLLEXPORT __declspec(dllexport)

//function pointers
DLLEXPORT void(*fp_getNVDAVersionString)(unsigned char**) = NULL;
DLLEXPORT inprocWorkerHandle_t(*fp_registerInprocWorker)(int, unsigned char*)=NULL;
DLLEXPORT void(*fp_unregisterInprocWorker)(inprocWorkerHandle_t)=NULL;
DLLEXPORT int(*fp_executeAppModuleEvent)(int,unsigned char*)=NULL;

//Implementation of methods 

void NVDAControler_getNVDAVersionString(unsigned char** version) {
	fp_getNVDAVersionString(version);
}

inprocWorkerHandle_t NVDAControler_registerInprocWorker(int processID, unsigned char* address) {
	return fp_registerInprocWorker(processID,address);
}

 void NVDAControler_unregisterInprocWorker(inprocWorkerHandle_t* inprocWorkerHandle) {
	inprocWorkerHandle_t_rundown(*inprocWorkerHandle);
	*inprocWorkerHandle=NULL;
}

int NVDAControler_executeAppModuleEvent(int processID, unsigned char* event) {
	return fp_executeAppModuleEvent(processID,event);
}

//Special cleanup method when client is lost

void __RPC_USER inprocWorkerHandle_t_rundown(inprocWorkerHandle_t inprocWorkerHandle) {
	fp_unregisterInprocWorker(inprocWorkerHandle);
}
  
//Server management functions

DLLEXPORT RPC_STATUS runServer() {
	RPC_STATUS status;
	//Set the protocol
	if((status=RpcServerUseProtseqEp("ncalrpc",RPC_C_PROTSEQ_MAX_REQS_DEFAULT,"NVDAControler",NULL))!=RPC_S_OK) {
		fprintf(stderr,"Error setting protocol\n");
		return status;
	}
	//Register the appModuleHelper interface
	if((status=RpcServerRegisterIf(NVDAControler_NVDAControler_v1_0_s_ifspec,NULL,NULL))!=RPC_S_OK) {
		fprintf(stderr,"Error registering interface, code 0X%X\n",status);
		return status;
	}
	//Start listening
	if((status=RpcServerListen(1,RPC_C_LISTEN_MAX_CALLS_DEFAULT,FALSE))!=RPC_S_OK) {
		fprintf(stderr,"Error listening, code 0X%X\n",status);
		return status;
	}
	return status;
}

DLLEXPORT RPC_STATUS stopServer() {
	return RpcMgmtStopServerListening(NULL); 
}

//memory allocation functions

void* __RPC_USER midl_user_allocate(size_t size) {
	return malloc(size);
}

void __RPC_USER midl_user_free(void* p) {
	free(p);
}
