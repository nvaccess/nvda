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

#include <windows.h>
#include <wchar.h>
#include "nvdaHelperRemote.h"
#include "typedCharacter.h"

LRESULT CALLBACK typedCharacter_getMessageHook(int code, WPARAM wParam, LPARAM lParam) {
	static HWND charWindow=0;
	static wchar_t lastCharacter=0;
	MSG* pmsg=(MSG*)lParam;
	if(pmsg->message==WM_KEYDOWN) {
		charWindow=pmsg->hwnd;
		lastCharacter=0;
	} else if((charWindow!=0)&&(pmsg->message==WM_CHAR)&&(pmsg->hwnd==charWindow)&&(pmsg->wParam!=lastCharacter)) { 
		NotifyWinEvent(EVENT_TYPEDCHARACTER,pmsg->hwnd,pmsg->wParam,pmsg->lParam);
		lastCharacter=pmsg->wParam;
	}
	return 0;
}

void typedCharacter_inProcess_initialize() {
	registerWindowsHook(WH_GETMESSAGE,typedCharacter_getMessageHook);
}

void typedCharacter_inProcess_terminate() {
	unregisterWindowsHook(WH_GETMESSAGE,typedCharacter_getMessageHook);
}
