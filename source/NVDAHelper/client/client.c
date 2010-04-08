#include <windows.h>
#include "nvdaController.h"
#include <common/winIPCUtils.h>

void* __RPC_USER midl_user_allocate(size_t size) {
	return malloc(size);
}

void __RPC_USER midl_user_free(void* p) {
	free(p);
}

BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		wchar_t* endpointString=(wchar_t*)malloc(sizeof(wchar_t)*64);
		getNVDAControllerNcalrpcEndpointString(endpointString,64,TRUE);
		RpcBindingFromStringBinding((RPC_WSTR)endpointString,&nvdaControllerBindingHandle);
		free(endpointString);
	} else if(reason==DLL_PROCESS_DETACH) {
		RpcBindingFree(&nvdaControllerBindingHandle);
	}
	return TRUE;
}
