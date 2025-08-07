/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2010 NVDA contributers.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License version 2.1, as published by
the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
*/

#ifndef NVDAHELPER_COMMON_WINIPCUTILS_H
#define NVDAHELPER_COMMON_WINIPCUTILS_H

#ifdef __cplusplus
extern "C" {
#endif

#include <wchar.h>

/**
 * Generates a string that can be used as part of the name for events and rpc endpoints etc that will localize it to the current session/desktop.
 * @param buf address of allocated memory that could hold cch characters where the port string should be written to.
 * @param cch the size of buf in characters
 */
size_t generateDesktopSpecificNamespace(wchar_t* buf, size_t cch);

#ifdef __cplusplus
}
#endif

#endif
