#ifndef NVDACONTROLCLIENT_H
#define NVDACONTROLCLIENT_H

#ifdef __cplusplus
extern "C"{
#endif 

#include "NVDAControler.h"

#define DLLEXPORT __declspec(dllexport)

/**
 * Retreaves the version from the currently running NVDA
 * @param version memory to receive the pointer that will point to the version string
 * @return true if the version was retreaved, false otherwize.
 */
DLLEXPORT int getNVDAVersionString(char** version);

/**
 * Executes an event on the appModule in NVDA representing this process.
 * @param event a python expression representing the event and arguments to execute
 * @return true if the event was received ok by NVDA, false otherwize.
 */
DLLEXPORT int executeAppModuleEvent(const char* event);

/**
 * Registers this process in NVDA as having an inprocWorker at the given address.
 * @param address the address of the inproc worker's rpc server.
 * @return a handle which can be later used to unregister the inproc worker.
 */
DLLEXPORT inprocWorkerHandle_t registerInprocWorker(const char* address);

/**
 * Unregisters a previously registered inproc worker.
 * @param a handle previously received when registering this inproc worker
 */
DLLEXPORT void unregisterInprocWorker(inprocWorkerHandle_t inprocWorkerHandle);
 
#ifdef __cplusplus
}
#endif

#endif

