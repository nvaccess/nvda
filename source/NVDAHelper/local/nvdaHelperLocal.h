#ifndef NVDAHELPERLOCAL_H
#define NVDAHELPERLOCAL_H
#include <windows.h>

#define DLLEXPORT extern "C" __declspec(dllexport)

DLLEXPORT handle_t createConnection(int processID);
DLLEXPORT void destroyConnection(handle_t bindingHandle);

#endif
