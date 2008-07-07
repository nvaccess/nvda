//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence

#ifndef TYPEDCHARACTER_H
#define TYPEDCHARACTER_H

#include <windows.h>
#include <wchar.h>

//Event IDs
#define EVENT_TYPEDCHARACTER 0x1000

//Private functions
void hook_typedCharacter(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);

#endif