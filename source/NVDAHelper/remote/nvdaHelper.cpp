//nvdaHelper.cpp
//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence
//See the file Copying for details.
 
#define UNICODE
#include <cstdio>
#include <set>
#include <map>
#include <windows.h>
#include "inputLangChange.h"
#include "typedCharacter.h"
#include "IA2Support.h"
#include "hookRegistration.h"
#include "nvdaHelper.h"

using namespace std;

typedef multimap<int,WINEVENTPROC> winEventHookRegistry_t;
typedef multimap<int,HOOKPROC> windowsHookRegistry_t;

HINSTANCE moduleHandle;
BOOL isInitialized=false;
BOOL inProcess_isInitialized=false;
set<int> inProcess_initializedThreads;
winEventHookRegistry_t inProcess_registeredWinEventHooks;
windowsHookRegistry_t inProcess_registeredCallWndProcWindowsHooks;
windowsHookRegistry_t inProcess_registeredGetMessageWindowsHooks;
HHOOK getMessageHookID=0;
HHOOK callWndProcHookID=0;
HWINEVENTHOOK winEventHookID=0; 
DWORD desktopProcessID=0;

void inThread_initialize() {
	Beep(880,35);
	inProcess_initializedThreads.insert(GetCurrentThreadId());
	typedCharacter_inThread_initialize();
	inputLangChange_inThread_initialize();
}

void inThread_terminate() {
	inputLangChange_inThread_terminate();
	typedCharacter_inThread_terminate();
	int threadID=GetCurrentThreadId();
	inProcess_initializedThreads.erase(threadID);
	inProcess_registeredWinEventHooks.erase(threadID);
	inProcess_registeredCallWndProcWindowsHooks.erase(threadID);
	inProcess_registeredGetMessageWindowsHooks.erase(threadID);
	Beep(1760,35);
}

void inProcess_initialize() {
	Beep(220,35);
	IA2Support_inProcess_initialize();
	inThread_initialize();
	inProcess_isInitialized=true;
}

void inProcess_terminate() {
	inThread_terminate();
	IA2Support_inProcess_terminate();
	inProcess_isInitialized=false;
	Beep(440,35);
}

bool registerWinEventHook(WINEVENTPROC hookProc) {
	inProcess_registeredWinEventHooks.insert(winEventHookRegistry_t::value_type(GetCurrentThreadId(),hookProc));
	return true;
}

bool unregisterWinEventHook(WINEVENTPROC hookProc) {
	winEventHookRegistry_t::iterator i=inProcess_registeredWinEventHooks.find(GetCurrentThreadId());
	if(i==inProcess_registeredWinEventHooks.end()) return false;
	inProcess_registeredWinEventHooks.erase(i);
return true;
}

bool registerWindowsHook(int hookType, HOOKPROC hookProc) {
	windowsHookRegistry_t* r=NULL;
	if(hookType==WH_GETMESSAGE) {
		r=&inProcess_registeredGetMessageWindowsHooks;
	} else if(hookType==WH_CALLWNDPROC) {
		r=&inProcess_registeredCallWndProcWindowsHooks;
	}
	if(r==NULL) return false;
	r->insert(windowsHookRegistry_t::value_type(GetCurrentThreadId(),hookProc));
	return true;
}

bool unregisterWindowsHook(int hookType, HOOKPROC hookProc) {
	windowsHookRegistry_t* r=NULL;
	if(hookType==WH_GETMESSAGE) {
		r=&inProcess_registeredGetMessageWindowsHooks;
	} else if(hookType==WH_CALLWNDPROC) {
		r=&inProcess_registeredCallWndProcWindowsHooks;
	}
	if(r==NULL) return false;
	r->erase(GetCurrentThreadId());
	return true;
}

#pragma comment(linker,"/entry:_DllMainCRTStartup@12")
BOOL DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if((reason==DLL_PROCESS_ATTACH)&&(moduleHandle==NULL)) {
		moduleHandle=hModule;
		GetWindowThreadProcessId(GetDesktopWindow(),&desktopProcessID);
	} else if(reason==DLL_THREAD_DETACH) {
		if(inProcess_initializedThreads.count(GetCurrentThreadId())>0) inThread_terminate();
	} else if(reason==DLL_PROCESS_DETACH) {
	if(inProcess_isInitialized) inProcess_terminate();
	}
	return TRUE;
}

//GetMessage hook callback
LRESULT CALLBACK getMessageHook(int code, WPARAM wParam, LPARAM lParam) {
	if(code<0) {
		return CallNextHookEx(0,code,wParam,lParam);
	}
	pair<windowsHookRegistry_t::iterator,windowsHookRegistry_t::iterator> range=inProcess_registeredGetMessageWindowsHooks.equal_range(GetCurrentThreadId());
	for(windowsHookRegistry_t:: iterator i=range.first;i!=range.second;i++) {
		i->second(code,wParam,lParam);
	}
	return CallNextHookEx(0,code,wParam,lParam);
}

//callWndProc hook callback
LRESULT CALLBACK callWndProcHook(int code, WPARAM wParam,LPARAM lParam) {
	if(code<0) {
		return CallNextHookEx(0,code,wParam,lParam);
	}
	pair<windowsHookRegistry_t::iterator,windowsHookRegistry_t::iterator> range=inProcess_registeredCallWndProcWindowsHooks.equal_range(GetCurrentThreadId());
	for(windowsHookRegistry_t:: iterator i=range.first;i!=range.second;i++) {
		i->second(code,wParam,lParam);
	}
	return CallNextHookEx(0,code,wParam,lParam);
}

//winEvent callback
void winEventHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	DWORD curProcessID=0;
	int curThreadID=GetCurrentThreadId();
	if(eventID==EVENT_SYSTEM_FOREGROUND||eventID==EVENT_OBJECT_FOCUS) {
		GetWindowThreadProcessId(hwnd,&curProcessID);
		if(curProcessID!=desktopProcessID) {
			if(!inProcess_isInitialized) inProcess_initialize();
			if(inProcess_initializedThreads.count(curThreadID)==0) inThread_initialize();
		}
	}
	pair<winEventHookRegistry_t::iterator,winEventHookRegistry_t::iterator> range=inProcess_registeredWinEventHooks.equal_range(curThreadID);
	for(winEventHookRegistry_t:: iterator i=range.first;i!=range.second;i++) {
		i->second(hookID, eventID, hwnd, objectID, childID, threadID, time);
	}
}

int nvdaHelper_initialize() {
	if(isInitialized) {
		fprintf(stderr,"Already initialized\n");
		return -1;
	}
	if(!IA2Support_initialize()) {
		fprintf(stderr,"Error initializing IA2 support\n");
		return -1;
	}
	if((getMessageHookID=SetWindowsHookEx(WH_GETMESSAGE,(HOOKPROC)getMessageHook,moduleHandle,0))==0) {
		fprintf(stderr,"Error registering window message hook\n");
		return -1;
	}
	if((callWndProcHookID=SetWindowsHookEx(WH_CALLWNDPROC,(HOOKPROC)callWndProcHook,moduleHandle,0))==0) {
		fprintf(stderr,"Error registering window message hook\n");
		return -1;
	}
	if((winEventHookID=SetWinEventHook(0,0xFFFFFFFF,moduleHandle,(WINEVENTPROC)winEventHook,0,0,WINEVENT_INCONTEXT|WINEVENT_SKIPOWNPROCESS))==0) {
		fprintf(stderr,"Error registering winEvent hook\n");
		return -1;
	}
	isInitialized=TRUE;
	return 0;
}

int nvdaHelper_terminate() {
	if(!isInitialized) {
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
	if(!IA2Support_terminate()) {
		fprintf(stderr,"Error terminating IA2 support");
		return -1;
	}
	isInitialized=FALSE;
	return 0;
}
