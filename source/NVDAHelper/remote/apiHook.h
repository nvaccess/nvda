#ifndef _APIHOOK_H
#define _APIHOOK_H

#ifdef __CPLUSCPLUS
extern "C" {
#endif

/**
 * Initializes hooking subsystem.
 * @return success flag
 */ 
bool apiHook_init();

/**
 * Requests that the given function from the given module should be hooked with the given hook procedure. 
 * @param moduleName the name of the module the function you wish to hook is located in.
 * @param functionName the name of the function you wish to hook.
 * @param newHookProc the function you wish  to be called instead of the original one.
 * @return the address of the original function. You could use this to call the origianl function from with in your replacement.
 */ 
void* apiHook_hookFunction(const char* moduleName, const char* functionName, void* newHookProc);

/**
 * unhooks all functions previously hooked with apiHook_hookFunction.
 */
BOOL apiHook_unhookFunctions();

#ifdef __CPLUSCPLUS
extern "C" {
#endif

#endif
