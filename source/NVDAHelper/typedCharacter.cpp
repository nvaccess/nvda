//typedCharacter.c
//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence
//See the file Copying for details.

#define UNICODE
#include <windows.h>
#include <wchar.h>
#include "hookRegistration.h"
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

void typedCharacter_inThread_initialize() {
	registerWindowsHook(WH_GETMESSAGE,typedCharacter_getMessageHook);
}

void typedCharacter_inThread_terminate() {
	unregisterWindowsHook(WH_GETMESSAGE,typedCharacter_getMessageHook);
}
