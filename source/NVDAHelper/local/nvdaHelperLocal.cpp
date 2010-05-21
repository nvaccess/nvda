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
#include "nvdaHelperLocal.h"

handle_t createConnection(int processID) {
	RPC_STATUS rpcStatus;
	std::wostringstream addr;
	addr<<L"ncalrpc:[nvdaHelperRemote_"<<processID<<L"]";
	handle_t bindingHandle;
	if((rpcStatus=RpcBindingFromStringBinding((RPC_WSTR)(addr.str().c_str()),&bindingHandle))!=RPC_S_OK) {
		fprintf(stderr,"Error creating binding handle from string binding, rpc code 0X%X\n",rpcStatus);
		return NULL;
	} 
	return bindingHandle;
}

void destroyConnection(handle_t bindingHandle) {
	RpcBindingFree(&bindingHandle);
}
