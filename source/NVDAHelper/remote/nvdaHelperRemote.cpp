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
	BOOL isInitialized=FALSE;
#pragma data_seg()
#pragma comment(linker, "/section:.remoteShared,rws")

HINSTANCE moduleHandle;
BOOL inProcess_wasInitializedOnce=false;
BOOL inProcess_isRunning=false;
winEventHookRegistry_t inProcess_registeredWinEventHooks;
windowsHookRegistry_t inProcess_registeredCallWndProcWindowsHooks;
windowsHookRegistry_t inProcess_registeredGetMessageWindowsHooks;
HHOOK getMessageHookID=0;
HHOOK callWndProcHookID=0;
HWINEVENTHOOK winEventHookID=0; 
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

BOOL DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if((reason==DLL_PROCESS_ATTACH)&&(moduleHandle==NULL)) {
		moduleHandle=hModule;
		GetWindowThreadProcessId(GetDesktopWindow(),&desktopProcessID);
		wchar_t endpointString[64];
		getNVDAControllerNcalrpcEndpointString(endpointString,64,TRUE);
		RpcBindingFromStringBinding((RPC_WSTR)endpointString,&nvdaControllerBindingHandle);
		RpcBindingFromStringBinding((RPC_WSTR)endpointString,&nvdaControllerInternalBindingHandle);
		if(isInitialized) LOG_INFO(L"process attach");
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
	if((getMessageHookID=SetWindowsHookEx(WH_GETMESSAGE,(HOOKPROC)getMessageHook,moduleHandle,0))==0) {
		MessageBox(NULL,L"Error registering getMessage Windows hook",L"nvdaHelperRemote (nvdaHelper_initialize)",0);
		return -1;
	}
	if((callWndProcHookID=SetWindowsHookEx(WH_CALLWNDPROC,(HOOKPROC)callWndProcHook,moduleHandle,0))==0) {
		MessageBox(NULL,L"Error registering callWndProc Windows hook",L"nvdaHelperRemote (nvdaHelper_initialize)",0);
		return -1;
	}
	if((winEventHookID=SetWinEventHook(0,0xFFFFFFFF,moduleHandle,(WINEVENTPROC)winEventHook,0,0,WINEVENT_INCONTEXT))==0) {
		MessageBox(NULL,L"Error registering winEvent hook",L"nvdaHelperRemote (nvdaHelper_initialize)",0);
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
