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

#ifndef _APIHOOK_H
#define _APIHOOK_H

#ifdef __CPLUSCPLUS
extern "C" {
#endif

/**
 * Initializes API hooking subsystem.
 * @return success flag
 */ 
bool apiHook_initialize();

/**
 * Requests that the given function from the given module should be hooked with the given hook procedure. 
 * @param moduleName the name of the module the function you wish to hook is located in.
 * @param functionName the name of the function you wish to hook.
 * @param newHookProc the function you wish  to be called instead of the original one.
 * @return the address of the original function. You could use this to call the origianl function from with in your replacement.
 */ 
void* apiHook_hookFunction(const char* moduleName, const char* functionName, void* newHookProc);

/**
 * Actually hooks all requested hook functions.
 */
	BOOL apiHook_enableHooks();

/**
 * unhooks all functions previously hooked with apiHook_hookFunction and terminates API hooking subsystem.
 */
BOOL apiHook_terminate();

#ifdef __CPLUSCPLUS
extern "C" {
#endif

#endif
