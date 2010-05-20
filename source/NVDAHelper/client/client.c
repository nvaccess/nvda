/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2010 NVDA contributers.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License version 2.1, as published by
the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
*/

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
