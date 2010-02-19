#ifndef NVDAHELPER_COMMON_WINIPCUTILS_H
#define NVDAHELPER_COMMON_WINIPCUTILS_H

#ifdef __cplusplus
extern "C" {
#endif
 
#include <wchar.h>

/**
 * Calculates the port string that NVDA's ncallrpc endpoint should use, so that it is local to the current Windows session and desktop.
 * @param buf address of allocated memory that could hold cch characters where the port string should be written to.
 * @param cch the size of buf in characters
 * @param fullAddress if True the full ncalrpc address will be fetched, false only the port is fetched.
 */
int getNVDAControllerNcalrpcEndpointString(wchar_t* buf, int cch, BOOL fullAddress);

#ifdef __cplusplus
}
#endif

#endif
 