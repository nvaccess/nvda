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

#ifndef NVDAHELPER_NEWMINHOOK_H
#define NVDAHELPER_NEWMINHOOK_H

#include <libMinHook/minHook.h>

//Some new batch calls
MH_STATUS MH_EnableAllHooks();
MH_STATUS MH_DisableAllHooks();

//function pointer typedefs for all minHook functions for use with getProcAddress
typedef MH_STATUS(WINAPI *MH_Initialize_funcType)();
typedef MH_STATUS(WINAPI *MH_Uninitialize_funcType)();
typedef MH_STATUS(WINAPI *MH_CreateHook_funcType)(void*,void*,void**);
typedef MH_STATUS(WINAPI *MH_EnableHook_funcType)(void*);
typedef MH_STATUS(WINAPI *MH_DisableHook_funcType)(void*);
typedef MH_STATUS(*MH_EnableAllHooks_funcType)();
typedef MH_STATUS(*MH_DisableAllHooks_funcType)();

#endif
