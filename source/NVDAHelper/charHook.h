//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence

#ifndef CHARHOOK_H
#define CHARHOOK_H

#include <windows.h>
#include <wchar.h>

//Event IDs
#define EVENT_TYPEDCHARACTER 0x1000
#define EVENT_INPUTLANGCHANGE 0x1001

//Private functions
void hook_typedCharacter(HWND hwnd, UINT msg, WPARAM wParam, LPARAM LParam);
void hook_inputLangChange(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);

#define DLLEXPORT __declspec(dllexport)

//Exported functions
DLLEXPORT int initialize();
DLLEXPORT void terminate();

#endif