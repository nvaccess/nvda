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
