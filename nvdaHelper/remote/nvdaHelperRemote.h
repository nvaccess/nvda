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

#ifndef NVDAHELPERREMOTE_H
#define NVDAHELPERREMOTE_H

#include <windows.h>

//Initialization and termination

/**
 * Initializes nvdaHelperRemote, and allows it to inject in to processes.
 * @param secureMode 1 specifies that the NVDA process initializing NVDAHelper is in secure mode
 */
BOOL injection_initialize(int secureMode);

/**
 * Terminates nvdaHelperRemote, allowing it to uninject from any processes.
 */ 
BOOL injection_terminate();

//Win event registration

/**
 * Registers a callback function to be called with in future win events for this process.
 * @param procHook the callback function which should be called
 * @return true if the hook was registered, false otherwise.
 */
bool registerWinEventHook(WINEVENTPROC hookProc);

/**
 * Unregisters a previously registered callback function for a win event for this process.
 * It may be possible for the winEvent hook to fire one more time after unregistration if the unregistration happens within a winEvent hook.
 * @param hookProc the callback function to be unregistered
 * @return True if it was unregistered, false otherwize.
 */
bool unregisterWinEventHook(WINEVENTPROC hookProc);

//Windows hook registration

/**
 * Registers a callback function to be called with in future windows hooks fired for this process.
 * @param hookType the type of windows hook (WH_CALLWNDPROC, WH_GETMESSAGE)
 * @param procHook the callback function which should be called
 * @return true if the hook was registered, false otherwise.
 */
bool registerWindowsHook(int hookType, HOOKPROC hookProc);

/**
 * Unregisters a previously registered callback function for a windows hook for this process.
 * It may be possible for the windows hook to fire one more time after unregistration if the unregistration happens within a windows hook.
 * @param hookType the type of windows hook
 * @param hookProc the callback function to be unregistered
 * @return True if it was unregistered, false otherwize.
 */
bool unregisterWindowsHook(int hookType, HOOKPROC hookProc);

// The handle for NVDA's inproc manager thread
extern HANDLE inprocMgrThreadHandle;

// Flushes any remaining log messages to NVDA.
// This should only be called from the NVDA inproc manager thread as it blocks while sending to NVDA.
void log_flushQueue();

#endif
