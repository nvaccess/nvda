//nvdaHelper.cpp
//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence
//See the file Copying for details.
 
#include <cstdio>
#include <cassert>
#include <list>
#include <set>
#include <map>
#include <windows.h>
#include <shlwapi.h>
#include "rpcSrv.h"
#include "inputLangChange.h"
#include "typedCharacter.h"
#include "IA2Support.h"
#include "ia2LiveRegions.h"
#include "nvdaController.h"
#include "nvdaControllerInternal.h"
#include <common/winIPCUtils.h>
#include <common/log.h>
#include "apiHook.h"
#include "gdiHooks.h"
#include "nvdaHelperRemote.h"

using namespace std;

typedef map<WINEVENTPROC,size_t> winEventHookRegistry_t;
typedef map<HOOKPROC,size_t> windowsHookRegistry_t;

#pragma data_seg(".remoteShared")
	wchar_t dllDirectory[MAX_PATH]={0};
#pragma data_seg()
#pragma comment(linker, "/section:.remoteShared,rws")

BOOL isInitialized=FALSE;
HINSTANCE moduleHandle;
BOOL inProcess_wasInitializedOnce=false;
BOOL inProcess_isRunning=false;
winEventHookRegistry_t inProcess_registeredWinEventHooks;
windowsHookRegistry_t inProcess_registeredCallWndProcWindowsHooks;
windowsHookRegistry_t inProcess_registeredGetMessageWindowsHooks;
DWORD desktopProcessID=0;

void inProcess_initialize() {
	#ifndef NDEBUG
	Beep(220,35);
	#endif
	assert(!inProcess_isRunning);
	assert(!inProcess_wasInitializedOnce);
	rpcSrv_inProcess_initialize();
	IA2Support_inProcess_initialize();
	ia2LiveRegions_inProcess_initialize();
	typedCharacter_inProcess_initialize();
	inputLangChange_inProcess_initialize();
	if (apiHook_inProcess_initialize()) {
		gdiHooks_inProcess_initialize();
	}
	inProcess_isRunning=inProcess_wasInitializedOnce=true;
}

void inProcess_terminate() {
	assert(inProcess_isRunning);
	assert(inProcess_wasInitializedOnce);
	apiHook_inProcess_terminate();
	gdiHooks_inProcess_terminate();
	inputLangChange_inProcess_terminate();
	typedCharacter_inProcess_terminate();
	ia2LiveRegions_inProcess_terminate();
	IA2Support_inProcess_terminate();
	rpcSrv_inProcess_terminate();
	inProcess_isRunning=false;
	#ifndef NDEBUG
	Beep(440,35);
	#endif
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
		assert(i->second==1);
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
		assert(i->second==1);
		r->erase(i);
	}
	return true;
}

BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if((reason==DLL_PROCESS_ATTACH)&&(moduleHandle==NULL)) {
		moduleHandle=hModule;
		GetWindowThreadProcessId(GetDesktopWindow(),&desktopProcessID);
		wchar_t endpointString[64];
		getNVDAControllerNcalrpcEndpointString(endpointString,64,TRUE);
		RpcBindingFromStringBinding((RPC_WSTR)endpointString,&nvdaControllerBindingHandle);
		RpcBindingFromStringBinding((RPC_WSTR)endpointString,&nvdaControllerInternalBindingHandle);
	} else if(reason==DLL_PROCESS_DETACH) {
	if(inProcess_isRunning) inProcess_terminate();
	RpcBindingFree(&nvdaControllerBindingHandle);
	RpcBindingFree(&nvdaControllerInternalBindingHandle);
	}
	return TRUE;
}

//GetMessage hook callback
LRESULT CALLBACK getMessageHook(int code, WPARAM wParam, LPARAM lParam) {
	if(code<0) {
		return CallNextHookEx(0,code,wParam,lParam);
	}
	if(inProcess_isRunning) {
		//Hookprocs may unregister or register hooks themselves, so we must copy the hookprocs before executing
		list<windowsHookRegistry_t::key_type> hookProcList;
		for(windowsHookRegistry_t::iterator i=inProcess_registeredGetMessageWindowsHooks.begin();i!=inProcess_registeredGetMessageWindowsHooks.end();i++) {
			hookProcList.push_back(i->first);
		}
		for(list<windowsHookRegistry_t::key_type>::iterator j=hookProcList.begin();j!=hookProcList.end();j++) {
			(*j)(code,wParam,lParam);
		}
	}
	return CallNextHookEx(0,code,wParam,lParam);
}

//callWndProc hook callback
LRESULT CALLBACK callWndProcHook(int code, WPARAM wParam,LPARAM lParam) {
	if(code<0) {
		return CallNextHookEx(0,code,wParam,lParam);
	}
	if(inProcess_isRunning) {
		//Hookprocs may unregister or register hooks themselves, so we must copy the hookprocs before executing
		list<windowsHookRegistry_t::key_type> hookProcList;
		for(windowsHookRegistry_t::iterator i=inProcess_registeredCallWndProcWindowsHooks.begin();i!=inProcess_registeredCallWndProcWindowsHooks.end();i++) {
			hookProcList.push_back(i->first);
		}
		for(list<windowsHookRegistry_t::key_type>::iterator j=hookProcList.begin();j!=hookProcList.end();j++) {
			(*j)(code,wParam,lParam);
		}
	}
	return CallNextHookEx(0,code,wParam,lParam);
}

//winEvent callback
void CALLBACK winEventHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	//We are not at all interested in out-of-context winEvents, even if they were accidental.
	if(threadID!=GetCurrentThreadId()) return;
	if(!inProcess_wasInitializedOnce) {
		assert(!inProcess_isRunning);
		DWORD curProcessID=0;
		if(eventID==EVENT_SYSTEM_FOREGROUND||eventID==EVENT_OBJECT_FOCUS) {
			GetWindowThreadProcessId(hwnd,&curProcessID);
			if(curProcessID!=desktopProcessID) {
				inProcess_initialize();
			}
		}
	} 
	if(inProcess_isRunning) {
		//Hookprocs may unregister or register hooks themselves, so we must copy the hookprocs before executing
		list<winEventHookRegistry_t::key_type> hookProcList;
		for(winEventHookRegistry_t::iterator i=inProcess_registeredWinEventHooks.begin();i!=inProcess_registeredWinEventHooks.end();i++) {
			hookProcList.push_back(i->first);
		}
		for(list<winEventHookRegistry_t::key_type>::iterator j=hookProcList.begin();j!=hookProcList.end();j++) {
			(*j)(hookID, eventID, hwnd, objectID, childID, threadID, time);
		}
	}
}

//This function is used to hook windows hooks and winEvents, pump messages, and then unhook windows hooks and winEvents.
//This function is run in its own thread.
//This thread is needed to icealate the hook callbacks from the rest of NVDA
//As some incontext callbacks may be called out of context due to 32/64 bit boundaries, and or security issues.
//We don't want them clogging up NVDA's main message queue.
void _nvdaHelper_localThreadFunc() {
	HHOOK getMessageHookID=0;
	HHOOK callWndProcHookID=0;
	HWINEVENTHOOK winEventHookLowID=0; 
	HWINEVENTHOOK winEventHookHighID=0; 
	if((getMessageHookID=SetWindowsHookEx(WH_GETMESSAGE,(HOOKPROC)getMessageHook,moduleHandle,0))==0) {
		MessageBox(NULL,L"Error registering getMessage Windows hook",L"nvdaHelperRemote (_nvdaHelper_localThreadFunc)",0);
	}
	if((callWndProcHookID=SetWindowsHookEx(WH_CALLWNDPROC,(HOOKPROC)callWndProcHook,moduleHandle,0))==0) {
		MessageBox(NULL,L"Error registering callWndProc Windows hook",L"nvdaHelperRemote (_nvdaHelper_localThreadFunc)",0);
	}
	//Register winEvent hooks in two separate calls,
	//Skipping the Windows console winEvent range (0x4001-0x40ff) as these are always out-of-context.
	if((winEventHookLowID=SetWinEventHook(0,0x4000,moduleHandle,(WINEVENTPROC)winEventHook,0,0,WINEVENT_INCONTEXT))==0) {
		MessageBox(NULL,L"Error registering low winEvent hooks",L"nvdaHelperRemote (_nvdaHelper_localThreadFunc)",0);
	}
	if((winEventHookHighID=SetWinEventHook(0x4100,0xffffffff,moduleHandle,(WINEVENTPROC)winEventHook,0,0,WINEVENT_INCONTEXT))==0) {
		MessageBox(NULL,L"Error registering high winEvent hooks",L"nvdaHelperRemote (_nvdaHelper_localThreadFunc)",0);
	}
	MSG msg;
	while(GetMessage(&msg,NULL,0,0)) {
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}
	if(UnhookWindowsHookEx(getMessageHookID)==0) {
		MessageBox(NULL,L"Error unregistering getMessage hook",L"nvdaHelperRemote (_nvdaHelper_localThreadFunc)",0);
	}
	if(UnhookWindowsHookEx(callWndProcHookID)==0) {
		MessageBox(NULL,L"Error unregistering callWndProc hook",L"nvdaHelperRemote (_nvdaHelper_localThreadFunc)",0);
	}
	if(UnhookWinEvent(winEventHookLowID)==FALSE) {
		MessageBox(NULL,L"Error unregistering low winEvent hooks",L"nvdaHelperRemote (_nvdaHelper_localThreadFunc)",0);
	}
	if(UnhookWinEvent(winEventHookHighID)==FALSE) {
		MessageBox(NULL,L"Error unregistering high winEvent hooks",L"nvdaHelperRemote (_nvdaHelper_localThreadFunc)",0);
	}
}

HANDLE _nvdaHelper_localThreadHandle=NULL;
DWORD _nvdaHelper_localThreadID=0;

int nvdaHelper_initialize() {
	if(isInitialized) {
		MessageBox(NULL,L"Already initialized",L"nvdaHelperRemote (nvdaHelper_initialize)",0);
		return -1;
	}
	//Find the directory name of this dll
	assert(moduleHandle);
	GetModuleFileName(moduleHandle,dllDirectory,MAX_PATH);
	PathRemoveFileSpec(dllDirectory);
	if(!IA2Support_initialize()) {
		MessageBox(NULL,L"Error initializing IA2 support",L"nvdaHelperRemote (nvdaHelper_initialize)",0);
		return -1;
	}
	_nvdaHelper_localThreadHandle=CreateThread(NULL,0,(LPTHREAD_START_ROUTINE)_nvdaHelper_localThreadFunc,NULL,0,&_nvdaHelper_localThreadID);
	isInitialized=TRUE;
	return 0;
}

int nvdaHelper_terminate() {
	if(!isInitialized) {
		MessageBox(NULL,L"Error not initialized yet",L"nvdaHelperRemote (nvdaHelper_terminate)",0);
		return -1;
	}
	PostThreadMessage(_nvdaHelper_localThreadID,WM_QUIT,0,0);
	if(WaitForSingleObject(_nvdaHelper_localThreadHandle,1000)!=0) {
		MessageBox(NULL,L"Error waiting for local thread to die, already dead or not responding.",L"nvdaHelperRemote (nvdaHelper_terminate)",0);
	}
	_nvdaHelper_localThreadHandle=NULL;
	_nvdaHelper_localThreadID=0;
	if(!IA2Support_terminate()) {
		MessageBox(NULL,L"Error terminating IA2 support",L"nvdaHelperRemote (nvdaHelper_terminate)",0);
		return -1;
	}
	isInitialized=FALSE;
	return 0;
}
