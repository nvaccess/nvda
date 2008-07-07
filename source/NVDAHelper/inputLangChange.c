//inputLangChange.c
//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence
//See the file Copying for details.

#define UNICODE
#include <windows.h>
#include "charHook.h"

int lastInputLangChange=0;

void hook_inputLangChange(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam) {
	if((message==WM_INPUTLANGCHANGE)&&(lParam!=lastInputLangChange)) {
		NotifyWinEvent(EVENT_INPUTLANGCHANGE,hwnd,wParam,lParam);
		lastInputLangChange=lParam;
	}
}
