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

#ifndef INPUTLANGCHANGE_H
#define INPUTLANGCHANGE_H

#include <windows.h>
#include <wchar.h>

//Event IDs
#define EVENT_INPUTLANGCHANGE 0x1001

void inputLangChange_inProcess_initialize();
void inputLangChange_inProcess_terminate();

#endif
