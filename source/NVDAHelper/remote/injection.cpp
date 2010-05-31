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
#include "ia2Support.h"
#include "nvdaController.h"
#include "nvdaControllerInternal.h"
#include <common/lock.h>
#include <common/winIPCUtils.h>
#include "dllmain.h"
#include "nvdaHelperRemote.h"
#include "inProcess.h"

using namespace std;

#pragma data_seg(".injectionShared")
long dllInjectionID=0;
#pragma data_seg()
#pragma comment(linker, "/section:.injectionShared,rws")

HINSTANCE dllHandle=NULL;
wchar_t dllDirectory[MAX_PATH];
LockableObject inprocThreadsLock;
long inprocInjectionID=0;
set<HHOOK> inprocCurrentWindowsHooks;
long tlsIndex_inThreadInjectionID=0;

//Code executed in-process

//General in-process winEvent callback
//Used for all possible winEvents in this process
void CALLBACK inproc_winEventCallback(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	//We are not at all interested in out-of-context winEvents, even if they were accidental.
	if(threadID!=GetCurrentThreadId()) return;
	//Set windows hooks for this thread if we havn't done so already
	inprocThreadsLock.acquire();
	if((long)TlsGetValue(tlsIndex_inThreadInjectionID)!=inprocInjectionID) {
		TlsSetValue(tlsIndex_inThreadInjectionID,(LPVOID)inprocInjectionID);
		HHOOK tempHook;
		if((tempHook=SetWindowsHookEx(WH_GETMESSAGE,inProcess_getMessageHook,dllHandle,threadID))==0) {
			MessageBox(NULL,L"Error registering getMessage Windows hook",L"nvdaHelperRemote (inproc_winEventCallback)",0);
		} else inprocCurrentWindowsHooks.insert(tempHook);
		if((tempHook=SetWindowsHookEx(WH_CALLWNDPROC,inProcess_callWndProcHook,dllHandle,threadID))==0) {
			MessageBox(NULL,L"Error registering callWndProc Windows hook",L"nvdaHelperRemote (inproc_winEventCallback)",0);
		} else inprocCurrentWindowsHooks.insert(tempHook);
	}
	inprocThreadsLock.release();
	//Call the winEvent callback for the in-process subsystems.
	inProcess_winEventCallback(hookID,eventID,hwnd,objectID,childID,threadID,time);
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
	assert(threadMutex);
	WaitForSingleObject(threadMutex,INFINITE);
	//Stop this dll from unloading while this function is running
	GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS,(LPCTSTR)dllHandle,&dllHandle);
	assert(dllHandle);
	//Initialize some needed RPC binding handles.
	wchar_t endpointString[64];
	getNVDAControllerNcalrpcEndpointString(endpointString,64,TRUE);
	RpcBindingFromStringBinding((RPC_WSTR)endpointString,&nvdaControllerBindingHandle);
	RpcBindingFromStringBinding((RPC_WSTR)endpointString,&nvdaControllerInternalBindingHandle);
	//Try to open handles to both the injectionDone event and NVDA's process handle
		HANDLE waitHandles[2]={0};
	long nvdaProcessID=0;
	nvdaControllerInternal_getNVDAProcessID(&nvdaProcessID);
	if(nvdaProcessID>0) {
		waitHandles[0]=OpenProcess(SYNCHRONIZE,FALSE,nvdaProcessID);
		waitHandles[1]=OpenEvent(SYNCHRONIZE,FALSE,L"nvdaHelperRemote_injectionDoneEvent");
	}
	//As long as we have successfully retreaved handles for NVDA's process and the event, then go on and initialize, wait and terminate.
	if(waitHandles[0]&&waitHandles[1]) {
		//Register for all winEvents in this process.
		HWINEVENTHOOK winEventHookID=SetWinEventHook(0,0XFFFFFFFF,dllHandle,inproc_winEventCallback,GetCurrentProcessId(),0,WINEVENT_INCONTEXT);
		assert(winEventHookID);
		//Initialize in-process subsystems
		inProcess_initialize();
		//Notify injection_winEventCallback (who started our thread) that we're past initialization
		SetEvent((HANDLE)data);
		//Wait till either the injection done event is set, or NVDA's process dies
		Beep(660,75);
		WaitForMultipleObjects(2,waitHandles,FALSE,INFINITE);
		Beep(1320,75);
		//Terminate all in-process subsystems.
		inProcess_terminate();
		//Unregister winEvents for this process
		UnhookWinEvent(winEventHookID);
		//Unregister any windows hooks registered so far
		inprocThreadsLock.acquire();
		//for(auto i=inprocCurrentWindowsHooks.cbegin();i!=inprocCurrentWindowsHooks.cend();++i) {
		for(set<HHOOK>::iterator i=inprocCurrentWindowsHooks.begin();i!=inprocCurrentWindowsHooks.end();++i) {
			UnhookWindowsHookEx(*i);
		}
		inprocCurrentWindowsHooks.clear();
		inprocThreadsLock.release();
	}
	if(waitHandles[0]) CloseHandle(waitHandles[0]);
	if(waitHandles[1]) CloseHandle(waitHandles[1]);
	//cleanup some RPC binding handles
	RpcBindingFree(&nvdaControllerBindingHandle);
	RpcBindingFree(&nvdaControllerInternalBindingHandle);
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
	HANDLE waitHandles[2]={0};
	BOOL threadCreated=FALSE;
	//Gain exclusive access to all the inproc thread variables for the rest of this function.
	inprocThreadsLock.acquire();
	if(inprocInjectionID!=dllInjectionID) {
		inprocInjectionID=dllInjectionID;
		//Create an event which will be used for the inproc manager thread to notify us that its successfully past initialization.
		waitHandles[0]=CreateEvent(NULL,TRUE,FALSE,NULL);
		assert(waitHandles[0]);
		//Create the inproc manager thread, passing the event as an argument.
		waitHandles[1]=CreateThread(NULL,0,inprocMgrThreadFunc,(LPVOID)(waitHandles[0]),0,NULL);
		assert(waitHandles[1]);
		threadCreated=TRUE;
	}
	inprocThreadsLock.release();
	if(threadCreated) {
		//Wait until the event is set (the thread is past initialization) or until the thread dies.
		WaitForMultipleObjects(2,waitHandles,FALSE,1000);
		//Cleanup the handles
		CloseHandle(waitHandles[0]);
		CloseHandle(waitHandles[1]);
		//Forward this winEvent to the general in-process winEvent callback if necessary, so it sees this initial event.
		inproc_winEventCallback(hookID,eventID,hwnd,objectID,childID,threadID,time);
	}
}

//Code for launcher process

//This function is run in its own thread.
//This thread is needed to icealate the hook callbacks from the rest of NVDA
//As some incontext callbacks may be called out of context due to 32/64 bit boundaries, and or security issues.
//We don't want them clogging up NVDA's main message queue.
DWORD WINAPI outprocMgrThreadFunc(LPVOID data) {
	InterlockedIncrement(&dllInjectionID);
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
	assert(!injectionDoneEvent);
	if(!IA2Support_initialize()) {
		MessageBox(NULL,L"Error initializing IA2 support",L"nvdaHelperRemote (injection_initialize)",0);
		return FALSE;
	}
	injectionDoneEvent=CreateEvent(NULL,TRUE,FALSE,L"nvdaHelperRemote_injectionDoneEvent");
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
		Beep(220,75);
		tlsIndex_inThreadInjectionID=TlsAlloc();
		dllHandle=hModule;
		GetModuleFileName(dllHandle,dllDirectory,MAX_PATH);
		PathRemoveFileSpec(dllDirectory);
	} else if(reason==DLL_PROCESS_DETACH) {
		Beep(1760,75);
		TlsFree(tlsIndex_inThreadInjectionID);
	}
	return TRUE;
}
