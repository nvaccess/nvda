//typedCharacter.c
//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence
//See the file Copying for details.

#define UNICODE
#include <windows.h>
#include <wchar.h>
#include "charHook.h"

HWND charWindow=0;
wchar_t lastCharacter=0;

void hook_typedCharacter(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam) {
	if(message==WM_KEYDOWN) {
		charWindow=hwnd;
		lastCharacter=0;
	} else if((charWindow!=0)&&(message==WM_CHAR)&&(hwnd==charWindow)&&(wParam!=lastCharacter)) { 
		NotifyWinEvent(EVENT_TYPEDCHARACTER,hwnd,wParam,lParam);
		lastCharacter=wParam;
	}
}
