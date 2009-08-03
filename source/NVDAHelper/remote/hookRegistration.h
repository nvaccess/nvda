//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence

#ifndef HOOKREGISTRATION_H
#define HOOKREGISTRATION_H

#include <windows.h>

#define DLLEXPORT extern "C" __declspec(dllexport)

//Win event registration

/**
 * Registers a callback function to be called with in future win events fired for the given thread  
 * @param procHook the callback function which should be called
 * @param threadID the id of the thread the winEvent is for, if not given its the current thread.
 * @return true if the hook was registered, false otherwise.
 */
DLLEXPORT bool registerWinEventHook(WINEVENTPROC hookProc, int threadID=0);

/**
 * Unregisters a previously registered callback function for a win event for the given thread 
 * @param hookProc the callback function to be unregistered
 * @param threadID the ID of the thread the winEvent is for. If not given its the current thread.
 * @return True if it was unregistered, false otherwize.
 */
DLLEXPORT bool unregisterWinEventHook(WINEVENTPROC hookProc, int threadID=0);

//Windows hook registration

/**
 * Registers a callback function to be called with in future windows hooks fired for the given thread with the given hook type
 * @param hookType the type of windows hook (WH_CALLWNDPROC, WH_GETMESSAGE)
 * @param procHook the callback function which should be called
 * @param threadID the ID of the thread the hook should be called for, if not given its the current thread. 
 * @return true if the hook was registered, false otherwise.
 */
DLLEXPORT bool registerWindowsHook(int hookType, HOOKPROC hookProc, int threadID=0);

/**
 * Unregisters a previously registered callback function for a windows hook for the given thread with the given hook type
 * @param hookType the type of windows hook
 * @param hookProc the callback function to be unregistered
 * @param the ID of the thread the hook is for, if not given its the current thread.
 * @return True if it was unregistered, false otherwize.
 */
DLLEXPORT bool unregisterWindowsHook(int hookType, HOOKPROC hookProc, int threadID=0);

#endif
