/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2019-2026 NV Access Limited, Bill Dengler
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2.0, as published by
the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

// Precompiled header for the winEventLimiter static library.
// WIN32_LEAN_AND_MEAN and NOMINMAX must be defined before <windows.h> is first included,
// so every translation unit includes this header first.

#pragma once

#define WIN32_LEAN_AND_MEAN             // Exclude rarely-used stuff from Windows headers
#ifndef NOMINMAX
#define NOMINMAX  // Use std::min / std::max
#endif
#include <windows.h>

#include <winuser.h>  // winEvent and OBJID constants, SetWinEventHook
#include <objbase.h>  // CoInitializeEx
