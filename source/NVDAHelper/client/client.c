#include <windows.h>
#include <interfaces/nvdaController/nvdaController.h>

void* __RPC_USER midl_user_allocate(size_t size) {
	return malloc(size);
}

void __RPC_USER midl_user_free(void* p) {
	free(p);
}

BOOL DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		RpcBindingFromStringBinding((RPC_WSTR)L"ncalrpc:[nvdaController]",&nvdaControllerBindingHandle);
	} else if(reason==DLL_PROCESS_DETACH) {
		RpcBindingFree(&nvdaControllerBindingHandle);
	}
	return TRUE;
}
