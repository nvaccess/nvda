#define UNICODE
#include <cstdio>
#include <cassert>
#include <map>
#include <sstream>
#include <windows.h>
#include <remoteApi/remoteApi.h>
#include "client.h"

#define VBufClientLibName L"VBufClient.dll"
#define VBufBaseLibName L"VBufBase.dll"

typedef struct {
	int processID;
	HANDLE processHandle;
	HMODULE VBufLibHandle;
} remoteServerInfo_t;

std::map<handle_t,remoteServerInfo_t> remoteServerMap;

HINSTANCE VBufClientLibHandle=0;

#pragma comment(linker,"/entry:_DllMainCRTStartup@12")
BOOL DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		VBufClientLibHandle=hModule;
	}
	return TRUE;
}

handle_t VBufClient_connect(int processID) {
	RPC_STATUS rpcStatus;
	std::wostringstream addr;
	addr<<L"ncalrpc:[nvVBufSrv_"<<processID<<L"]";
	handle_t bindingHandle;
	if((rpcStatus=RpcBindingFromStringBinding((RPC_WSTR)(addr.str().c_str()),&bindingHandle))!=RPC_S_OK) {
		fprintf(stderr,"Error creating binding handle from string binding, rpc code 0X%X\n",rpcStatus);
		return NULL;
	} 
	HANDLE processHandle=OpenProcess(PROCESS_CREATE_THREAD|PROCESS_QUERY_INFORMATION|PROCESS_VM_READ|PROCESS_VM_WRITE|PROCESS_VM_OPERATION,FALSE,processID);
	if(processHandle==0) {
		fprintf(stderr,"Error opening remote process\n");
		RpcBindingFree(&bindingHandle);
		return NULL;
	}
	wchar_t VBufLibPath[1024];
	assert(VBufClientLibHandle); //we need a valid handle for current dll
	int i=GetModuleFileName(VBufClientLibHandle,VBufLibPath,1024);
	assert(i>0); //size of path must be greater than 0
	wcscpy(VBufLibPath+(i-wcslen(VBufClientLibName)),VBufBaseLibName);
	void* remoteVBufLibPath=VirtualAllocEx(processHandle,NULL,sizeof(VBufLibPath),MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE);
	if(remoteVBufLibPath==NULL) {
		fprintf(stderr,"Could not allocate remoteVBufLibPath\n");
		CloseHandle(processHandle);
		RpcBindingFree(&bindingHandle);
		return NULL;
	}
	if(WriteProcessMemory(processHandle,remoteVBufLibPath,VBufLibPath,sizeof(VBufLibPath),NULL)==0) {
		fprintf(stderr,"Error writing VBufLibPath to remote process\n");
		VirtualFreeEx(processHandle,remoteVBufLibPath,0,MEM_RELEASE);
		CloseHandle(processHandle);
		RpcBindingFree(&bindingHandle);
		return NULL;
	}
	HANDLE remoteThread=CreateRemoteThread(processHandle,NULL,0,(LPTHREAD_START_ROUTINE)LoadLibrary,remoteVBufLibPath,0,NULL);
	if(remoteThread==0) {
		fprintf(stderr,"Could not create remote thread\n");
		VirtualFreeEx(processHandle,remoteVBufLibPath,0,MEM_RELEASE);
		CloseHandle(processHandle);
		RpcBindingFree(&bindingHandle);
		return NULL;
	}
	if(WaitForSingleObject(remoteThread,1000)!=0) {
		fprintf(stderr,"Error waiting for remote thread to complete\n");
		VirtualFreeEx(processHandle,remoteVBufLibPath,0,MEM_RELEASE);
		CloseHandle(processHandle);
		RpcBindingFree(&bindingHandle);
		return NULL;
	}
	HMODULE VBufLibHandle;
	if(GetExitCodeThread(remoteThread,(LPDWORD)&VBufLibHandle)==0) {
		fprintf(stderr,"Could not get remote thread exit code\n");
		VirtualFreeEx(processHandle,remoteVBufLibPath,0,MEM_RELEASE);
		CloseHandle(processHandle);
		RpcBindingFree(&bindingHandle);
		return NULL;
	}
	VirtualFreeEx(processHandle,remoteVBufLibPath,0,MEM_RELEASE);
	remoteServerInfo_t info;
	info.processID=processID;
	info.processHandle=processHandle;
	info.VBufLibHandle=VBufLibHandle;
	remoteServerMap[bindingHandle]=info;
	return bindingHandle;
}

void VBufClient_disconnect(handle_t bindingHandle) {
	if(remoteServerMap.count(bindingHandle)==0) {
		fprintf(stderr,"Unknown binding handle\n");
		return;
	}
	remoteServerInfo_t info=remoteServerMap[bindingHandle];
	remoteServerMap.erase(bindingHandle);
	WaitForSingleObject(CreateRemoteThread(info.processHandle,NULL,0,(LPTHREAD_START_ROUTINE)FreeLibrary,info.VBufLibHandle,0,NULL),1000);
	CloseHandle(info.processHandle);
	RpcBindingFree(&bindingHandle);
}

//memory allocation functions

void* __RPC_USER midl_user_allocate(size_t size) {
	return malloc(size);
}

void __RPC_USER midl_user_free(void* p) {
	free(p);
}

