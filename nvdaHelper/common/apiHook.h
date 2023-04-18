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

/**
 * Initializes an API hooking transaction.
 * @return success flag
 */ 
bool apiHook_beginTransaction();

/**
 * Requests that the given function from the given module should be hooked with the given hook procedure. 
 * Warning, this function has no safety checks, you should usually use the apiHook_hookFunction_safe template
 * @param realFunction the function you wish to hook.
 * @param fakeFunction the function you wish  to be called instead of the original one.
 * @param targetPointerRef Pointer variable that will contain a pointer to the original function after hooking. This is used to unhook.
 */ 
bool apiHook_hookFunction(void* realFunction, void* fakeFunction, void** targetPointerRef);

/**
 * Safely hooks a given function from a given module with a given fake function.
 * This is a safer wrapper around apiHook_hookFunction that ensures that the real and fake function have matching signatures.
 * @param realFunction the function you wish to hook.
 * @param fakeFunction the function you wish  to be called instead of the original one.
 * @param targetPointerRef Pointer variable that will contain a pointer to the original function after hooking. This is used to unhook.
*/ 
template<typename funcType>
bool apiHook_hookFunction_safe(funcType realFunction, funcType fakeFunction, funcType* targetPointerRef) {
	return apiHook_hookFunction(
		reinterpret_cast<void*>(realFunction),
		reinterpret_cast<void*>(fakeFunction),
		reinterpret_cast<void**>(targetPointerRef)
	);
}

/**
 * Commits an API hooking transaction.
 */
bool apiHook_commitTransaction();

/**
 * unhooks all functions previously hooked with apiHook_hookFunction and terminates API hooking subsystem.
 */
bool apiHook_terminate();

#endif
