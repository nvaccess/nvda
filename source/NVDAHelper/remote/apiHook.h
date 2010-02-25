#ifndef _APIHOOK_H
#define _APIHOOK_H

#ifdef __CPLUSCPLUS
extern "C" {
#endif

/**
 * Requests that the given function from the given module should be hooked with the given hook procedure. Note that hooking does not automatically take place when this function is called, so this function can be called many times before the actual hooking can be done in bulk with apiHooks_hookFunctions. 
 * @param moduleName the name of the module the function you wish to hook is located in.
 * @param functionName the name of the function you wish to hook.
 * @param newHookProc the function you wish  to be called instead of the original one.
 * @return the address of the original function. You could use this to call the origianl function from with in your replacement.
 */ 
void* apiHook_requestFunctionHook(const char* moduleName, const char* functionName, void* newHookProc);

/**
 * Hooks all the functions requested with apiHooks_requestFunctionHook.
 * @return true if it succeeded, false otherwize.
 */
BOOL apiHook_hookFunctions();

/**
 * Unhooks any functions previously hooked.
 */
BOOL apiHook_unhookFunctions();

#ifdef __CPLUSCPLUS
extern "C" {
#endif

#endif
