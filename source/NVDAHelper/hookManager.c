//hookManager.c
//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence
//See the file Copying for details.
 
#define UNICODE
#include <windows.h>
#include "inputLangChange.h"
#include "typedCharacter.h"
#include "IA2Support.h"
#include "hookManager.h"

#pragma data_seg(".hookManagerShared")
HHOOK getMessageHookID=0;
HHOOK callWndProcHookID=0;
HWINEVENTHOOK winEventHookID=0; 
int initialProcessID=0;
int desktopProcessID=0;
int shellProcessID=0;
#pragma data_seg()
#pragma comment(linker, "/section:.hookManagerShared,rws")

HINSTANCE moduleHandle;
BOOL isManagerInitialized=FALSE;

#pragma comment(linker,"/entry:_DllMainCRTStartup@12")
BOOL DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if((reason==DLL_PROCESS_ATTACH)&&(moduleHandle==NULL)) {
		moduleHandle=hModule;
	} else if(reason==DLL_PROCESS_DETACH) {
		if(isIA2Initialized) uninstallIA2Support();
	}
	return TRUE;
}

//GetMessage hook callback
LRESULT CALLBACK getMessageHook(int code, WPARAM wParam, LPARAM lParam) {
	MSG* pmsg=(MSG*)lParam;
	if(code<0) {
		return CallNextHookEx(getMessageHookID,code,wParam,lParam);
	}
	hook_typedCharacter(pmsg->hwnd,pmsg->message,pmsg->wParam,pmsg->lParam);
	return CallNextHookEx(getMessageHookID,code,wParam,lParam);
}

//callWndProc hook callback
LRESULT CALLBACK callWndProcHook(int code, WPARAM wParam,LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if(code<0) {
		return CallNextHookEx(callWndProcHookID,code,wParam,lParam);
	}
	hook_inputLangChange(pcwp->hwnd,pcwp->message,pcwp->wParam,pcwp->lParam);
	return CallNextHookEx(callWndProcHookID,code,wParam,lParam);
}

//winEvent callback
void winEventHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	int curProcessID=0;
	if(eventID==EVENT_SYSTEM_FOREGROUND||eventID==EVENT_OBJECT_FOCUS) {
		GetWindowThreadProcessId(hwnd,&curProcessID);
		if(isIA2Initialized&&curProcessID!=initialProcessID&&curProcessID!=desktopProcessID&&curProcessID!=shellProcessID) installIA2Support();
	}
}

int initialize() {
	if(isManagerInitialized) {
		fprintf(stderr,"Already initialized\n");
		return -1;
	}
	initialProcessID=GetCurrentProcessId();
	GetWindowThreadProcessId(GetDesktopWindow(),&desktopProcessID);
	GetWindowThreadProcessId(GetShellWindow(),&shellProcessID);
	IA2Support_initialize();
	if((getMessageHookID=SetWindowsHookEx(WH_GETMESSAGE,(HOOKPROC)getMessageHook,moduleHandle,0))==0) {
		fprintf(stderr,"Error registering window message hook\n");
		return -1;
	}
	if((callWndProcHookID=SetWindowsHookEx(WH_CALLWNDPROC,(HOOKPROC)callWndProcHook,moduleHandle,0))==0) {
		fprintf(stderr,"Error registering window message hook\n");
		return -1;
	}
	if((winEventHookID=SetWinEventHook(0,0xFFFFFFFF,moduleHandle,(WINEVENTPROC)winEventHook,0,0,WINEVENT_INCONTEXT|WINEVENT_SKIPOWNPROCESS))==0) {
		fprintf(stderr,"Error registering foregorund winEvent hook\n");
		return -1;
	}
	isManagerInitialized=TRUE;
	return 0;
}

int terminate() {
	if(!isManagerInitialized) {
		fprintf(stderr,"Error: not initialized yet\n");
		return -1;
	}
	if(UnhookWindowsHookEx(getMessageHookID)==0) {
		fprintf(stderr,"Error unhooking getMessage hook\n");
		return -1;
	}
	if(UnhookWindowsHookEx(callWndProcHookID)==0) {
		fprintf(stderr,"Error unhooking callWndProc hook\n");
		return -1;
	}
	if(UnhookWinEvent(winEventHookID)==FALSE) {
		fprintf(stderr,"Error unregistering foreground winEvent\n");
		return -1;
	}
	isManagerInitialized=FALSE;
	return 0;
}
