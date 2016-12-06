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
 
#include <cstdio>
#include <list>
#include <set>
#include <map>
#define WIN32_LEAN_AND_MEAN 
#include <windows.h>
#include "winword.h"
#include "inputLangChange.h"
#include "typedCharacter.h"
#include "tsf.h"
#include "ime.h"
#include "IA2Support.h"
#include "ia2LiveRegions.h"
#include <common/log.h>
#include "gdiHooks.h"
#include "nvdaHelperRemote.h"
#include "inProcess.h"

using namespace std;

typedef map<WINEVENTPROC,size_t> winEventHookRegistry_t;
typedef map<HOOKPROC,size_t> windowsHookRegistry_t;

winEventHookRegistry_t inProcess_registeredWinEventHooks;
windowsHookRegistry_t inProcess_registeredCallWndProcWindowsHooks;
windowsHookRegistry_t inProcess_registeredGetMessageWindowsHooks;

UINT wm_execInWindow;

void inProcess_initialize() {
	wm_execInWindow=RegisterWindowMessage(L"nvdaHelper_execInWindow");
	IA2Support_inProcess_initialize();
	ia2LiveRegions_inProcess_initialize();
	typedCharacter_inProcess_initialize();
	inputLangChange_inProcess_initialize();
	TSF_inProcess_initialize();
	IME_inProcess_initialize();
	winword_inProcess_initialize();
	gdiHooks_inProcess_initialize();
}

void inProcess_terminate() {
	gdiHooks_inProcess_terminate();
	IME_inProcess_terminate();
	TSF_inProcess_terminate();
	winword_inProcess_terminate();
	inputLangChange_inProcess_terminate();
	typedCharacter_inProcess_terminate();
	ia2LiveRegions_inProcess_terminate();
	IA2Support_inProcess_terminate();
}

bool registerWinEventHook(WINEVENTPROC hookProc) {
	inProcess_registeredWinEventHooks[hookProc]+=1;
	return true;
}

bool unregisterWinEventHook(WINEVENTPROC hookProc) {
	winEventHookRegistry_t::iterator i=inProcess_registeredWinEventHooks.find(hookProc);
	if(i==inProcess_registeredWinEventHooks.end()) return false;
	if(i->second>1) {
		i->second-=1;
	} else {
		nhAssert(i->second==1);
		inProcess_registeredWinEventHooks.erase(i);
	}
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
	(*r)[hookProc]+=1;
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
	windowsHookRegistry_t::iterator i=r->find(hookProc);
	if(i==r->end()) return false;
	if(i->second>1) {
		i->second-=1;
	} else {
		nhAssert(i->second==1);
		r->erase(i);
	}
	return true;
}

//GetMessage hook callback
LRESULT CALLBACK inProcess_getMessageHook(int code, WPARAM wParam, LPARAM lParam) {
	if(code<0||wParam==PM_NOREMOVE) {
		return CallNextHookEx(0,code,wParam,lParam);
	}
	//Hookprocs may unregister or register hooks themselves, so we must copy the hookprocs before executing
	windowsHookRegistry_t hookProcs=inProcess_registeredGetMessageWindowsHooks;
	for(windowsHookRegistry_t::iterator i=hookProcs.begin();i!=hookProcs.end();++i) {
		i->first(code,wParam,lParam);
	}
	return CallNextHookEx(0,code,wParam,lParam);
}

//callWndProc hook callback
LRESULT CALLBACK inProcess_callWndProcHook(int code, WPARAM wParam,LPARAM lParam) {
	if(code<0) {
		return CallNextHookEx(0,code,wParam,lParam);
	}
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if(pcwp->message==wm_execInWindow) {
		execInWindow_funcType* func=(execInWindow_funcType*)(pcwp->wParam);
		void* data=(void*)(pcwp->lParam);
		if(func) (*func)(data);
		return 0;
	}
	//Hookprocs may unregister or register hooks themselves, so we must copy the hookprocs before executing
	windowsHookRegistry_t hookProcs=inProcess_registeredCallWndProcWindowsHooks;
	for(windowsHookRegistry_t::iterator i=hookProcs.begin();i!=hookProcs.end();++i) {
		i->first(code,wParam,lParam);
	}
	return CallNextHookEx(0,code,wParam,lParam);
}

//winEvent callback
void CALLBACK inProcess_winEventCallback(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	//We are not at all interested in out-of-context winEvents, even if they were accidental.
	if(threadID!=GetCurrentThreadId()) return;
	//Hookprocs may unregister or register hooks themselves, so we must copy the hookprocs before executing
	winEventHookRegistry_t hookProcs=inProcess_registeredWinEventHooks;
	for(winEventHookRegistry_t::iterator i=hookProcs.begin();i!=hookProcs.end();++i) {
		i->first(hookID, eventID, hwnd, objectID, childID, threadID, time);
	}
}

void execInWindow(HWND hwnd, execInWindow_funcType func,void* data) {
	// Using SendMessage here causes outgoing cross-process COM calls to fail with RPC_E_CANTCALLOUT_ININPUTSYNCCALL,
	// which breaks us for Firefox multi-process. See Mozilla bug 1297549 comments 14 and 18.
	// Use SendMessageCallback instead.
	SENDASYNCPROC callback = [] (HWND hwnd, UINT msg, ULONG_PTR data, LRESULT result) {
		// Signal the waiting message loop to exit.
		PostQuitMessage(0);
	};
	if (!SendMessageCallback(hwnd,wm_execInWindow,(WPARAM)&func,(LPARAM)data, callback, NULL))
		return;
	MSG msg;
	// Wait in a message loop until the callback fires and sends WM_QUIT.
	// We also abort the loop if WaitMessage fails for some reason.
	while (GetMessage(&msg, NULL, WM_QUIT, WM_QUIT) > 0);
}
