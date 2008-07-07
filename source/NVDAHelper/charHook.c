//charHook.c
//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence
//See the file Copying for details.
 
#define UNICODE
#include <windows.h>
#include "charHook.h"

#pragma data_seg(".shared")
HHOOK getMessageHookID=0;
HHOOK callWndProcHookID=0;
#pragma data_seg()
#pragma comment(linker, "/section:.shared,rws")

HINSTANCE moduleHandle;
BOOL isInitialized=FALSE;

#pragma comment(linker,"/entry:_DllMainCRTStartup@12")
BOOL DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if((reason==DLL_PROCESS_ATTACH)&&(moduleHandle==NULL)) {
		moduleHandle=hModule;
	}
	return TRUE;
}

LRESULT CALLBACK getMessageHook(int code, WPARAM wParam, LPARAM lParam) {
	MSG* pmsg=(MSG*)lParam;
	if(code<0) {
		return CallNextHookEx(getMessageHookID,code,wParam,lParam);
	}
	hook_typedCharacter(pmsg->hwnd,pmsg->message,pmsg->wParam,pmsg->lParam);
	return CallNextHookEx(getMessageHookID,code,wParam,lParam);
}

LRESULT CALLBACK callWndProcHook(int code, WPARAM wParam,LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if(code<0) {
		return CallNextHookEx(callWndProcHookID,code,wParam,lParam);
	}
	hook_inputLangChange(pcwp->hwnd,pcwp->message,pcwp->wParam,pcwp->lParam);
	return CallNextHookEx(callWndProcHookID,code,wParam,lParam);
}

int initialize() {
	if(isInitialized) {
		fprintf(stderr,"Already initialized\n");
		return -1;
	}
	if((getMessageHookID=SetWindowsHookEx(WH_GETMESSAGE,(HOOKPROC)getMessageHook,moduleHandle,0))<=0) {
		fprintf(stderr,"Error registering window message hook\n");
		return -1;
	}
	if((callWndProcHookID=SetWindowsHookEx(WH_CALLWNDPROC,(HOOKPROC)callWndProcHook,moduleHandle,0))<=0) {
		fprintf(stderr,"Error registering window message hook\n");
		return -1;
	}
	isInitialized=TRUE;
	return 0;
}

void terminate() {
	if(isInitialized) {
		UnhookWindowsHookEx(getMessageHookID);
		UnhookWindowsHookEx(callWndProcHookID);
		isInitialized=FALSE;
	}
}
