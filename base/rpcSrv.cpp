#include <cstdio>
#include <sstream>
#include <windows.h>
#include <remoteApi/remoteApi.h>

//Special cleanup method for VBufRemote when client is lost
void __RPC_USER VBufRemote_bufferHandle_t_rundown(VBufRemote_bufferHandle_t buffer) {
	VBufRemote_destroyBuffer(&buffer);
}

RPC_STATUS startServer() {
	RPC_STATUS status;
	//Set the protocol
	std::ostringstream endPoint;
	endPoint<<"nvVBufSrv_"<<GetCurrentProcessId();
	if((status=RpcServerUseProtseqEp((RPC_CSTR)"ncalrpc",RPC_C_PROTSEQ_MAX_REQS_DEFAULT,(RPC_CSTR)(endPoint.str().c_str()),NULL))!=RPC_S_OK) {
		fprintf(stderr,"Error setting protocol\n");
		return status;
	}
	//Register the interfaces
	printf("Registering interface...\n");
	if((status=RpcServerRegisterIfEx(VBufRemote_VBufRemote_v2_0_s_ifspec,NULL,NULL,RPC_IF_AUTOLISTEN,RPC_C_LISTEN_MAX_CALLS_DEFAULT,NULL))!=RPC_S_OK) {
		fprintf(stderr,"Error registering interface, code 0X%X\n",status);
		return status;
	}
	printf("done\n");
/*
	//Start listening
	printf("starting server\n");
	if((status=RpcServerListen(1,RPC_C_LISTEN_MAX_CALLS_DEFAULT,TRUE))!=RPC_S_OK) {
		fprintf(stderr,"Error starting, code 0X%X\n",status);
		return status;
	}
	CreateThread(NULL,0,(LPTHREAD_START_ROUTINE)RpcMgmtWaitServerListen,NULL,0,NULL);
*/
	return status;
}

void stopServer() {
	printf("unregistering interface...\n");
	RpcServerUnregisterIf(VBufRemote_VBufRemote_v2_0_s_ifspec,NULL,1);
	printf("Done\n");
}

//dll initialization and termination
//Starts and stops the server
#pragma comment(linker,"/entry:_DllMainCRTStartup@12")
BOOL DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		startServer();
	} else if(reason==DLL_PROCESS_DETACH) {
		stopServer();
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
