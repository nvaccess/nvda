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
 * Warning, this function has no safety checks, you should usually use the apiHook_hookFunction_safe macro
 * @param realFunction the name of the function you wish to hook.
 * @param fakeFunction the function you wish  to be called instead of the original one.
 * @param targetPointerRef Pointer to the target pointer to which the detour will be attached.
 */ 
bool apiHook_hookFunction(void* realFunction, void* fakeFunction, void** targetPointerRef);

 /**
 * a helper template used internally by apiHook_hookFunction_safe
 */
template<typename funcType> bool _apiHook_hookFunction_tpl(funcType realFunction, funcType fakeFunction, funcType* targetPointerRef) { return apiHook_hookFunction((void*)realFunction,(void*)fakeFunction,(void**)targetPointerRef); }

/**
 * Safely hooks a given function from a given module with a given fake function.
 * @param realFunction the name of the function you wish to hook.
 * @param fakeFunction the function you wish  to be called instead of the original one.
 * @param targetPointerRef Pointer to the target pointer to which the detour will be attached.
 */ 
#define apiHook_hookFunction_safe(realFunction,fakeFunction, targetPointerRef) _apiHook_hookFunction_tpl(realFunction,fakeFunction,targetPointerRef)
 
/**
 * Commits an API hooking transaction.
 */
bool apiHook_commitTransaction();

/**
 * unhooks all functions previously hooked with apiHook_hookFunction and terminates API hooking subsystem.
 */
bool apiHook_terminate();

#endif
