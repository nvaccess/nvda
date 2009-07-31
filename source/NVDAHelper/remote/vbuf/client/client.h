#ifndef VIRTUALBUFFER_CLIENT_H
#define VIRTUALBUFFER_CLIENT_H

#include <remoteApi/remoteApi.h>

#define DLLEXPORT extern "C" __declspec(dllexport)

DLLEXPORT handle_t VBufClient_connect(int processID);
DLLEXPORT void VBufClient_disconnect(handle_t bindingHandle);

#endif
