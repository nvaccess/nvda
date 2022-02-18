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
#include <map>
#define WIN32_LEAN_AND_MEAN 
#include <windows.h>
#include <shlwapi.h>
#include <sddl.h>
#include <common/log.h>
#include "apiHook.h"
#include <remote/nvdaController.h>
#include <remote/nvdaControllerInternal.h>
#include <common/lock.h>
#include <common/winIPCUtils.h>
#include "dllmain.h"
#include "nvdaHelperRemote.h"
#include "inProcess.h"
#include "rpcSrv.h"

using namespace std;

typedef HHOOK(WINAPI *SetWindowsHookEx_funcType)(int,HOOKPROC,HINSTANCE,DWORD);

HINSTANCE dllHandle=NULL;
wchar_t dllDirectory[MAX_PATH];
wchar_t desktopSpecificNamespace[64];
LockableObject inprocThreadsLock;
HANDLE inprocMgrThreadHandle=NULL;
HWINEVENTHOOK inprocWinEventHookID=0;
map<long,HHOOK> callWndProcHooksByThread;
map<long,HHOOK> getMessageHooksByThread;
long tlsIndex_inThreadInjectionID=0;
bool isProcessExiting=false;
bool isSecureModeNVDAProcess=false;
SetWindowsHookEx_funcType real_SetWindowsHookExA=NULL;

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
		} else getMessageHooksByThread.insert(make_pair(threadID,tempHook));
		if((tempHook=SetWindowsHookEx(WH_CALLWNDPROC,inProcess_callWndProcHook,dllHandle,threadID))==0) {
			LOG_DEBUGWARNING(L"SetWindowsHookEx with WH_CALLWNDPROC failed, GetLastError returned "<<GetLastError());
		} else callWndProcHooksByThread.insert(make_pair(threadID,tempHook));
	}
	inprocThreadsLock.release();
	//Call the winEvent callback for the in-process subsystems.
	inProcess_winEventCallback(hookID,eventID,hwnd,objectID,childID,threadID,time);
}

//An implementation of SetWindowsHookExA that ensures that our W hooks always happen before other peoples' A hooks
HHOOK WINAPI fake_SetWindowsHookExA(int IdHook, HOOKPROC lpfn, HINSTANCE hMod, DWORD dwThreadId) {
	//Call the real SetWindowsHookExA
	HHOOK res=real_SetWindowsHookExA(IdHook,lpfn,hMod,dwThreadId);
	//We only go on if the real call did not fail and this is a thread-specific hook
	if(!res||!dwThreadId) return res;
	//Find our correct hooksByThread map and hookProc
	//based on the hook type.
	//If not supported then don't do anything more
	map<long,HHOOK>* hooksByThread=NULL;
	HOOKPROC ourHookProc=NULL;
	switch(IdHook) {
		case WH_GETMESSAGE:
		hooksByThread=&getMessageHooksByThread;
		ourHookProc=inProcess_getMessageHook;
		break;
		case WH_CALLWNDPROC:
		hooksByThread=&callWndProcHooksByThread;
		ourHookProc=inProcess_callWndProcHook;
		break;
		default:
		return res;
	}
	//See if we have previously hooked this thread ourselves.
	//If not then do nothing more.
	inprocThreadsLock.acquire();
	map<long,HHOOK>::iterator i=hooksByThread->find(dwThreadId);
	if(i!=hooksByThread->end()) {
		//Unhook our previous hook for this thread and rehook it again, placing our hook before the non-NVDA hook just registered 
		if(UnhookWindowsHookEx(i->second)) {
			i->second=SetWindowsHookEx(IdHook,ourHookProc,NULL,dwThreadId);
		} else {
			i->second=0;
		}
		if(i->second==0) {
			hooksByThread->erase(i);
		}
	}
	inprocThreadsLock.release();
	return res;
}

//Unregisters any current windows hooks
void killRunningWindowsHooks() {
	for(map<long,HHOOK>::iterator i=getMessageHooksByThread.begin();i!=getMessageHooksByThread.end();) {
		UnhookWindowsHookEx(i->second);
		getMessageHooksByThread.erase(i++);
	}
	for(map<long,HHOOK>::iterator i=callWndProcHooksByThread.begin();i!=callWndProcHooksByThread.end();) {
		UnhookWindowsHookEx(i->second);
		callWndProcHooksByThread.erase(i++);
	}
}

//A replacement OpenClipboard function to disable the use of the clipboard in a secure mode NVDA process
//Simply returns false without calling the original OpenClipboard
typedef BOOL(WINAPI *OpenClipboard_funcType)(HWND);
OpenClipboard_funcType real_OpenClipboard=NULL;
BOOL WINAPI fake_OpenClipboard(HWND hwndOwner) {
	return false;
}

//A thread function that runs while  NVDA is injected in a process.
//Note that a mutex is used to make sure that there is never more than one copy of this thread in a given process at any given time.
//I.e. Another copy of NVDA is started  while the first is still running.
DWORD WINAPI inprocMgrThreadFunc(LPVOID data) {
	HANDLE threadMutex=NULL;
	//Create a label for the mutex with the processID encoded so that it only affects this process.
	{
		wostringstream mutexNameStream;
		mutexNameStream<<L"NVDAHelperRemote_inprocMgrThread_"<<GetCurrentProcessId();
		//Create/open the mutex and wait to gain access.
		threadMutex=CreateMutex(NULL,FALSE,mutexNameStream.str().c_str()); 
	}
	if(!threadMutex) {
		LOG_ERROR(L"CreateMutex failed, GetLastError returned "<<GetLastError());
		return 0;
	}
	WaitForSingleObject(threadMutex,INFINITE);
	//Stop this dll from unloading while this function is running
	nhAssert(dllHandle);
	HINSTANCE tempHandle=NULL;
	if(!GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS,(LPCTSTR)dllHandle,&tempHandle)) {
		LOG_ERROR(L"GetModuleHandleEx failed, GetLastError returned "<<GetLastError());
		ReleaseMutex(threadMutex);
		return 0;
	}
	nhAssert(dllHandle==tempHandle);
	// Flush any log messages from other threads queued before the manager thread was started. 
	log_flushQueue();
	//Register for all winEvents in this process.
	inprocWinEventHookID=SetWinEventHook(EVENT_MIN,EVENT_MAX,dllHandle,inproc_winEventCallback,GetCurrentProcessId(),0,WINEVENT_INCONTEXT);
	if(inprocWinEventHookID==0) {
		LOG_ERROR(L"SetWinEventHook failed");
	}

	// Begin API hooking transaction
	apiHook_beginTransaction();
	// Hook SetWindowsHookExA so that we can juggle hooks around a bit.
	// Fixes #2411
	apiHook_hookFunction_safe(SetWindowsHookExA, fake_SetWindowsHookExA, &real_SetWindowsHookExA);
	// For secure mode NVDA process, hook OpenClipboard to disable usage of the clipboard
	if (isSecureModeNVDAProcess) {
		apiHook_hookFunction_safe(OpenClipboard, fake_OpenClipboard, &real_OpenClipboard);
	}
	// Initialize in-process subsystems
	inProcess_initialize();
	// Enable all registered API hooks by committing the transaction
	apiHook_commitTransaction();
	// Initialize our rpc server interfaces and request registration with NVDA
	rpcSrv_initialize();
	// Notify injection_winEventCallback (who started our thread) that we're past initialization
	SetEvent((HANDLE)data);
	// Wait until nvda unregisters
	#ifndef NDEBUG
	Beep(660,75);
	#endif
	// Even though we only registered for in-context winEvents, we may still receive some out-of-context events; e.g. console events.
	// Therefore, we must have a message loop.
	// Otherwise, any out-of-context events will cause major lag which increases over time.
	// We must also wait in an alertable state so that any APC functions queued to this thread by other NVDAHelper code will be executed.
	while(true) {
		const long handleCount = 1;
		const long WAIT_PENDING_MESSAGES = WAIT_OBJECT_0 + handleCount;
		DWORD res = MsgWaitForMultipleObjectsEx(
			handleCount,
			&nvdaUnregisteredEvent,
			INFINITE,
			QS_ALLINPUT,
			MWMO_ALERTABLE // wait in an alert state so queued APC functions are executed.
		);
		if(res == WAIT_PENDING_MESSAGES) {
			// Consume and handle all pending messages.
			MSG msg;
			while(PeekMessage(&msg, nullptr, 0, 0, PM_REMOVE)) {
				TranslateMessage(&msg);
				DispatchMessage(&msg);
			}
			continue;
		} else if(res == WAIT_IO_COMPLETION) {
			// Woke for a queued APC function. Keep going.
			continue;
		}
		// anything else (the registrationEvent was set, there was an error) means we need to stop.
		break;
	}
	nhAssert(inprocMgrThreadHandle);
	inprocThreadsLock.acquire();
	CloseHandle(inprocMgrThreadHandle);
	inprocMgrThreadHandle=NULL;
	inprocThreadsLock.release();
	#ifndef NDEBUG
	Beep(1320,75);
	#endif
	// Terminate our RPC server interfaces
	rpcSrv_terminate();
	// Unregister and terminate API hooks
	apiHook_terminate();
	// Terminate all in-process subsystems.
	inProcess_terminate();
	// Unregister any windows hooks registered so far
	killRunningWindowsHooks();
	// Unregister inproc winEvent callback
	UnhookWinEvent(inprocWinEventHookID);
	inprocWinEventHookID=0;
	// Flush any remaining log messages to NVDA
	log_flushQueue();
	// Release and close the thread mutex
	ReleaseMutex(threadMutex);
	CloseHandle(threadMutex);
	// Allow this dll to unload if necessary, and exit the thread.
	FreeLibraryAndExitThread(dllHandle,0);
	return 0;
}

bool initInprocManagerThreadIfNeeded() {
	bool threadCreated=FALSE;
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
		WaitForMultipleObjects(2,waitHandles,FALSE,10000);
	}
	//Close the event handle, but not the thread handle as the thread itself will do that.
	if(waitHandles[0]) CloseHandle(waitHandles[0]);
	return threadCreated;
}

//winEvent callback to inject in-process
//Only used for foreground/focus winEvents
void CALLBACK injection_winEventCallback(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	if(isProcessExiting) {
		// We shouldn't do anything at all if the process is exiting.
		// Doing so will probably cause a crash.
		return;
	}
	//We are not at all interested in out-of-context winEvents, even if they were accidental.
	if(threadID!=GetCurrentThreadId()) return;
	if(initInprocManagerThreadIfNeeded()) {
		//Forward this winEvent to the general in-process winEvent callback if necessary, so it sees this initial event.
		inproc_winEventCallback(inprocWinEventHookID,eventID,hwnd,objectID,childID,threadID,time);
	}
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

/**
 * Initializes the out-of-process code for NVDAHelper 
 * @param secureMode 1 specifies that NVDA is running in seucre mode, 0 says not.
 */ 
BOOL injection_initialize(int secureMode) {
	if(secureMode) isSecureModeNVDAProcess=true;
	if(outprocInitialized) {
		MessageBox(NULL,L"Already initialized",L"nvdaHelperRemote (injection_initialize)",0);
		return FALSE;
	}
	nhAssert(dllHandle);
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
	outprocInitialized=FALSE;
	return TRUE;
}

//Common code to in-process and out-of-process

BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		_CrtSetReportHookW2(_CRT_RPTHOOK_INSTALL,(_CRT_REPORT_HOOKW)NVDALogCrtReportHook);
		#ifndef NDEBUG
		Beep(220,75);
		#endif
		tlsIndex_inThreadInjectionID=TlsAlloc();
		dllHandle=hModule;
		GetModuleFileName(dllHandle,dllDirectory,MAX_PATH);
		PathRemoveFileSpec(dllDirectory);
		generateDesktopSpecificNamespace(desktopSpecificNamespace,ARRAYSIZE(desktopSpecificNamespace));
		//Initialize some needed RPC binding handles.
		wstring endpoint=L"NvdaCtlr.";
		endpoint+=desktopSpecificNamespace;
		RPC_WSTR stringBinding;
		RpcStringBindingCompose(NULL,(RPC_WSTR)L"ncalrpc",NULL,(RPC_WSTR)(endpoint.c_str()),NULL,&stringBinding);
		RpcBindingFromStringBinding(stringBinding,&nvdaControllerBindingHandle);
		RpcBindingFromStringBinding(stringBinding,&nvdaControllerInternalBindingHandle);
		RpcStringFree(&stringBinding);
	} else if(reason==DLL_PROCESS_DETACH) {
		#ifndef NDEBUG
		Beep(1760,75);
		#endif
		if(lpReserved) { // process is terminating
			isProcessExiting=true;
			//If the inproc manager thread was killed off due to process termination then at least unregister hooks
			if(inprocMgrThreadHandle) {
				#ifndef NDEBUG
				Beep(2500,75);
				#endif
				//Unregister and terminate API hooks
				apiHook_terminate();
				//Unregister any current windows hooks
				killRunningWindowsHooks();
				//Unregister winEvents for this process
				if(inprocWinEventHookID) { 
					UnhookWinEvent(inprocWinEventHookID);
					inprocWinEventHookID=0;
				}
			}
		} else { //The dll is being unloaded from this process
			TlsFree(tlsIndex_inThreadInjectionID);
			//cleanup some RPC binding handles
			RpcBindingFree(&nvdaControllerBindingHandle);
			RpcBindingFree(&nvdaControllerInternalBindingHandle);
		}
	} else if(reason==DLL_THREAD_DETACH) {
		long threadID=GetCurrentThreadId();
		getMessageHooksByThread.erase(threadID);
		callWndProcHooksByThread.erase(threadID);
	}
	return TRUE;
}
