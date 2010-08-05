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

#include <string>
#include <sstream>
#include <set>
#include <windows.h>
#include <shlwapi.h>
#include <common/log.h>
#include "ia2Support.h"
#include "apiHook.h"
#include "nvdaController.h"
#include "nvdaControllerInternal.h"
#include <common/lock.h>
#include <common/winIPCUtils.h>
#include "dllmain.h"
#include "nvdaHelperRemote.h"
#include "inProcess.h"

using namespace std;

HINSTANCE dllHandle=NULL;
wchar_t dllDirectory[MAX_PATH];
wchar_t desktopSpecificNamespace[64];
LockableObject inprocThreadsLock;
HANDLE inprocMgrThreadHandle=NULL;
HWINEVENTHOOK inprocWinEventHookID=0;
set<HHOOK> inprocCurrentWindowsHooks;
long tlsIndex_inThreadInjectionID=0;

//Code executed in-process

//General in-process winEvent callback
//Used for all possible winEvents in this process
void CALLBACK inproc_winEventCallback(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	if(hookID==0) return;
	//We are not at all interested in out-of-context winEvents, even if they were accidental.
	if(threadID!=GetCurrentThreadId()) return;
	//Set windows hooks for this thread if we havn't done so already
	inprocThreadsLock.acquire();
	if((HWINEVENTHOOK)TlsGetValue(tlsIndex_inThreadInjectionID)!=hookID) {
		TlsSetValue(tlsIndex_inThreadInjectionID,(LPVOID)hookID);
		HHOOK tempHook;
		if((tempHook=SetWindowsHookEx(WH_GETMESSAGE,inProcess_getMessageHook,dllHandle,threadID))==0) {
			LOG_DEBUGWARNING(L"SetWindowsHookEx with WH_GETMESSAGE failed, GetLastError returned "<<GetLastError());
		} else inprocCurrentWindowsHooks.insert(tempHook);
		if((tempHook=SetWindowsHookEx(WH_CALLWNDPROC,inProcess_callWndProcHook,dllHandle,threadID))==0) {
			LOG_DEBUGWARNING(L"SetWindowsHookEx with WH_CALLWNDPROC failed, GetLastError returned "<<GetLastError());
		} else inprocCurrentWindowsHooks.insert(tempHook);
	}
	inprocThreadsLock.release();
	//Call the winEvent callback for the in-process subsystems.
	inProcess_winEventCallback(hookID,eventID,hwnd,objectID,childID,threadID,time);
}

//Unregisters any current windows hooks
void killRunningWindowsHooks() {
	for(set<HHOOK>::iterator i=inprocCurrentWindowsHooks.begin();i!=inprocCurrentWindowsHooks.end();++i) {
		UnhookWindowsHookEx(*i);
	}
}

//A thread function that runs while  NVDA is injected in a process.
//Note that a mutex is used to make sure that there is never more than one copy of this thread in a given process at any given time.
//I.e. Another copy of NVDA is started  while the first is still running.
DWORD WINAPI inprocMgrThreadFunc(LPVOID data) {
	//Create a label for the mutex with the processID encoded so that it only affects this process.
	wostringstream mutexNameStream;
	mutexNameStream<<L"NVDAHelperRemote_inprocMgrThread_"<<GetCurrentProcessId();
	//Create/open the mutex and wait to gain access.
	HANDLE threadMutex=CreateMutex(NULL,FALSE,mutexNameStream.str().c_str()); 
	if(!threadMutex) {
		LOG_ERROR(L"CreateMutex failed, GetLastError returned "<<GetLastError());
		return 0;
	}
	WaitForSingleObject(threadMutex,INFINITE);
	//Stop this dll from unloading while this function is running
	assert(dllHandle);
	HINSTANCE tempHandle=NULL;
	if(!GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS,(LPCTSTR)dllHandle,&tempHandle)) {
		LOG_ERROR(L"GetModuleHandleEx failed, GetLastError returned "<<GetLastError());
		return 0;
	}
	assert(dllHandle==tempHandle);
	//Try to open handles to both the injectionDone event and NVDA's process handle
		HANDLE waitHandles[2]={0};
	long nvdaProcessID=0;
	nvdaControllerInternal_getNVDAProcessID(&nvdaProcessID);
	if(nvdaProcessID>0) {
		waitHandles[0]=OpenProcess(SYNCHRONIZE,FALSE,nvdaProcessID);
		wstringstream s;
		s<<L"nvdaHelperRemote_injectionDoneEvent_"<<desktopSpecificNamespace;
		waitHandles[1]=OpenEvent(SYNCHRONIZE,FALSE,s.str().c_str());
	}
	//As long as we have successfully retreaved handles for NVDA's process and the event, then go on and initialize, wait and terminate.
	if(waitHandles[0]&&waitHandles[1]) {
		//Register for all winEvents in this process.
		inprocWinEventHookID=SetWinEventHook(0,0XFFFFFFFF,dllHandle,inproc_winEventCallback,GetCurrentProcessId(),0,WINEVENT_INCONTEXT);
		if(inprocWinEventHookID==0) {
			LOG_ERROR(L"SetWinEventHook failed");
		}
		//Initialize API hooking
		apiHook_initialize();
		//Initialize in-process subsystems
		inProcess_initialize();
		//Enable all registered API hooks
		apiHook_enableHooks();
		//Notify injection_winEventCallback (who started our thread) that we're past initialization
		SetEvent((HANDLE)data);
		//Wait till either the injection done event is set, or NVDA's process dies
		#ifndef NDEBUG
		Beep(660,75);
		#endif
		WaitForMultipleObjects(2,waitHandles,FALSE,INFINITE);
		assert(inprocMgrThreadHandle);
		inprocThreadsLock.acquire();
		CloseHandle(inprocMgrThreadHandle);
		inprocMgrThreadHandle=NULL;
		inprocThreadsLock.release();
		#ifndef NDEBUG
		Beep(1320,75);
		#endif
		//Unregister and terminate API hooks
		apiHook_terminate();
		//Terminate all in-process subsystems.
		inProcess_terminate();
		//Unregister winEvents for this process
		if(inprocWinEventHookID) { 
			UnhookWinEvent(inprocWinEventHookID);
			inprocWinEventHookID=0;
		}
		//Unregister any windows hooks registered so far
		killRunningWindowsHooks();
	} else {
		assert(inprocMgrThreadHandle);
		inprocThreadsLock.acquire();
		CloseHandle(inprocMgrThreadHandle);
		inprocMgrThreadHandle=NULL;
		inprocThreadsLock.release();
	}
	if(waitHandles[0]) CloseHandle(waitHandles[0]);
	if(waitHandles[1]) CloseHandle(waitHandles[1]);
	//Release and close the thread mutex
	ReleaseMutex(threadMutex);
	CloseHandle(threadMutex);
	//Allow this dll to unload if necessary, and exit the thread.
	FreeLibraryAndExitThread(dllHandle,0);
	return 0;
}

//winEvent callback to inject in-process
//Only used for foreground/focus winEvents
void CALLBACK injection_winEventCallback(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	//We are not at all interested in out-of-context winEvents, even if they were accidental.
	if(threadID!=GetCurrentThreadId()) return;
	BOOL threadCreated=FALSE;
	HANDLE waitHandles[2]={0};
	//Gain exclusive access to all the inproc thread variables for the rest of this function.
	inprocThreadsLock.acquire();
	if(inprocMgrThreadHandle&&WaitForSingleObject(inprocMgrThreadHandle,0)==0) {
		LOG_ERROR(L"inproc manager thread died prematuraly");
		CloseHandle(inprocMgrThreadHandle);
		inprocMgrThreadHandle=NULL;
	}
	if(!inprocMgrThreadHandle) {
		//Create an event which will be used for the inproc manager thread to notify us that its successfully past initialization.
		waitHandles[0]=CreateEvent(NULL,TRUE,FALSE,NULL);
		if(waitHandles[0]) {
			//Create the inproc manager thread, passing the event as an argument.
			inprocMgrThreadHandle=waitHandles[1]=CreateThread(NULL,0,inprocMgrThreadFunc,(LPVOID)(waitHandles[0]),0,NULL);
			if(waitHandles[1]) {
				threadCreated=TRUE;
			} else { //CreateThread returned NULL
				LOG_ERROR(L"Error creating inproc manager thread, GetLastError returned "<<GetLastError());
			}
		} else { //CreateEvent returned NULL
			LOG_ERROR(L"Error creating inproc manager thread initialization done event, GetLastError returned "<<GetLastError());
		}
	}
	inprocThreadsLock.release();
	if(threadCreated) {
		//Wait until the event is set (the thread is past initialization) or until the thread dies.
		WaitForMultipleObjects(2,waitHandles,FALSE,1000);
		//Forward this winEvent to the general in-process winEvent callback if necessary, so it sees this initial event.
		inproc_winEventCallback(inprocWinEventHookID,eventID,hwnd,objectID,childID,threadID,time);
	}
	//Close the event handle, but not the thread handle as the thread itself will do that.
	if(waitHandles[0]) CloseHandle(waitHandles[0]);
}

//Code for launcher process

//This function is run in its own thread.
//This thread is needed to icealate the hook callbacks from the rest of NVDA
//As some incontext callbacks may be called out of context due to 32/64 bit boundaries, and or security issues.
//We don't want them clogging up NVDA's main message queue.
DWORD WINAPI outprocMgrThreadFunc(LPVOID data) {
	HWINEVENTHOOK winEventHookFocusID=0; 
	HWINEVENTHOOK winEventHookForegroundID=0; 
//Register focus/foreground winEvents
	if((winEventHookFocusID=SetWinEventHook(EVENT_OBJECT_FOCUS,EVENT_OBJECT_FOCUS,dllHandle,injection_winEventCallback,0,0,WINEVENT_INCONTEXT))==0) {
		MessageBox(NULL,L"Error registering focus winEvent hook",L"nvdaHelperRemote (outprocMgrThreadFunc)",0);
		return 0;
	}
	if((winEventHookForegroundID=SetWinEventHook(EVENT_SYSTEM_FOREGROUND,EVENT_SYSTEM_FOREGROUND,dllHandle,injection_winEventCallback,0,0,WINEVENT_INCONTEXT))==0) {
		MessageBox(NULL,L"Error registering foreground winEvent hook",L"nvdaHelperRemote (outprocMgrThreadFunc)",0);
		return 0;
	}
	//Standard message loop
	MSG msg;
	while(GetMessage(&msg,NULL,0,0)) {
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}
	if(UnhookWinEvent(winEventHookFocusID)==FALSE) {
		MessageBox(NULL,L"Error unregistering focus winEvent hook",L"nvdaHelperRemote (outprocMgrThreadFunc)",0);
	}
	if(UnhookWinEvent(winEventHookForegroundID)==FALSE) {
		MessageBox(NULL,L"Error unregistering foreground winEvent hook",L"nvdaHelperRemote (outprocMgrThreadFunc)",0);
	}
	return 0;
}

HANDLE outprocMgrThreadHandle=NULL;
DWORD outprocMgrThreadID=0;
BOOL outprocInitialized=FALSE;
HANDLE injectionDoneEvent=NULL;

BOOL injection_initialize() {
	if(outprocInitialized) {
		MessageBox(NULL,L"Already initialized",L"nvdaHelperRemote (injection_initialize)",0);
		return FALSE;
	}
	assert(dllHandle);
	if(!IA2Support_initialize()) {
		MessageBox(NULL,L"Error initializing IA2 support",L"nvdaHelperRemote (injection_initialize)",0);
		return FALSE;
	}
	assert(!injectionDoneEvent);
	{
		wstringstream s;
		s<<L"nvdaHelperRemote_injectionDoneEvent_"<<desktopSpecificNamespace;
		injectionDoneEvent=CreateEvent(NULL,TRUE,FALSE,s.str().c_str());
	}
	assert(injectionDoneEvent);
	ResetEvent(injectionDoneEvent);
	outprocMgrThreadHandle=CreateThread(NULL,0,outprocMgrThreadFunc,NULL,0,&outprocMgrThreadID);
	outprocInitialized=TRUE;
	return TRUE;
}

BOOL injection_terminate() {
	if(!outprocInitialized) {
		MessageBox(NULL,L"Error not initialized yet",L"nvdaHelperRemote (injection_terminate)",0);
		return FALSE;
	}
	PostThreadMessage(outprocMgrThreadID,WM_QUIT,0,0);
	if(WaitForSingleObject(outprocMgrThreadHandle,1000)!=0) {
		MessageBox(NULL,L"Error waiting for local thread to die, already dead or not responding.",L"nvdaHelperRemote (injection_terminate)",0);
	}
	outprocMgrThreadHandle=NULL;
	outprocMgrThreadID=0;
	if(!IA2Support_terminate()) {
		MessageBox(NULL,L"Error terminating IA2 support",L"nvdaHelperRemote (injection_terminate)",0);
		return FALSE;
	}
	assert(injectionDoneEvent);
	SetEvent(injectionDoneEvent);
	CloseHandle(injectionDoneEvent);
	injectionDoneEvent=NULL;
	outprocInitialized=FALSE;
	return TRUE;
}

//Common code to in-process and out-of-process

BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		#ifndef NDEBUG
		Beep(220,75);
		#endif
		tlsIndex_inThreadInjectionID=TlsAlloc();
		dllHandle=hModule;
		GetModuleFileName(dllHandle,dllDirectory,MAX_PATH);
		PathRemoveFileSpec(dllDirectory);
		generateDesktopSpecificNamespace(desktopSpecificNamespace,ARRAYSIZE(desktopSpecificNamespace));
		//Initialize some needed RPC binding handles.
		wstringstream s;
		s<<L"ncalrpc:[NvdaCtlr."<<desktopSpecificNamespace<<L"]";
		RpcBindingFromStringBinding((RPC_WSTR)(s.str().c_str()),&nvdaControllerBindingHandle);
		RpcBindingFromStringBinding((RPC_WSTR)(s.str().c_str()),&nvdaControllerInternalBindingHandle);
	} else if(reason==DLL_PROCESS_DETACH) {
		#ifndef NDEBUG
		Beep(1760,75);
		#endif
	//cleanup some RPC binding handles
	RpcBindingFree(&nvdaControllerBindingHandle);
	RpcBindingFree(&nvdaControllerInternalBindingHandle);
		if(lpReserved) { // process is terminating
			//If the inproc manager thread was killed off due to process termination then at least unregister hooks
			if(inprocMgrThreadHandle) {
				#ifndef NDEBUG
				Beep(2500,75);
				#endif
				//Unregister and terminate API hooks
				apiHook_terminate();
				//Unregister any current windows hooks
				killRunningWindowsHooks();
			}
		} else { //The dll is being unloaded from this process
			TlsFree(tlsIndex_inThreadInjectionID);
		}
	}
	return TRUE;
}
