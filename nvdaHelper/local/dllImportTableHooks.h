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

#include <string>
#include <set>
#include <map>
#include <windows.h>

#ifndef _DLLIMPORTTABLEHOOKS_H
#define _DLLIMPORTTABLEHOOKS_H

#ifdef __CPLUSCPLUS
extern "C" {
#endif

typedef std::map<void*,void*> funcToFunc_t;
typedef std::map<std::string,funcToFunc_t> moduleNameToFuncToFunc_t;
typedef std::map<void*,IMAGE_THUNK_DATA*> funcToThunk_t;

class DllImportTableHooks {
	public:

	DllImportTableHooks(HMODULE targetModule);

	/**
	 * Requests that the given function from the given module should be hooked with the given hook procedure. Note that hooking does not automatically take place when this function is called, so this function can be called many times before the actual hooking can be done in bulk with apiHooks_hookFunctions. 
	 * @param moduleName the name of the module the function you wish to hook is located in.
	 * @param functionName the name of the function you wish to hook.
	 * @param newHookProc the function you wish  to be called instead of the original one.
	 * @return the address of the original function. You could use this to call the origianl function from with in your replacement.
	 */ 
	void* requestFunctionHook(const char* moduleName, const char* functionName, void* newHookProc);

	/**
	 * Hooks all the functions requested with requestFunctionHook.
	 * @return true if it succeeded, false otherwize.
	 */
	BOOL hookFunctions();

	/**
	 * Unhooks any functions previously hooked.
	 */
	BOOL unhookFunctions();

	const HMODULE targetModule;

	private:
	moduleNameToFuncToFunc_t hookRequests;
	funcToThunk_t hookedFunctions;

};

/**
 * Hooks a single imported function in a dll. Uses the DllImportTableHook class.
 * @param targetDll the name of the dll who has imported the function to be hooked.
* @param importDll the name of the dll containing the function imported.
* @param functionName The name of the function to be hooked.
* @param newFunction the function to be called instead.
* @return an opaque pointer to the DllImportTableHook class instance that hooked the function.
*/
void* dllImportTableHooks_hookSingle(char* targetDll, char* importDll, char* functionName, void* newFunction);

/**
 * Unhooks a previously hooked function hooked by dllImportTableHooks_hookSingle.
 * @param hook The opaque pointer returned from a ccessful call to dllImportTableHooks_hookSingle.
 */
void dllImportTableHooks_unhookSingle(void* hook);


#ifdef __CPLUSCPLUS
extern "C" {
#endif

#endif
