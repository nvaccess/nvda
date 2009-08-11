//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence

#ifndef NVDAHELPERREMOTE_H
#define NVDAHELPERREMOTE_H

#include <windows.h>

#define DLLEXPORT extern "C" __declspec(dllexport)

//The directory name where this dll is situated
extern wchar_t dllDirectory[MAX_PATH];

//Exported functions
DLLEXPORT int nvdaHelper_initialize();
DLLEXPORT int nvdaHelper_terminate();

//Win event registration

/**
 * Registers a callback function to be called with in future win events for this process.
 * @param procHook the callback function which should be called
 * @return true if the hook was registered, false otherwise.
 */
DLLEXPORT bool registerWinEventHook(WINEVENTPROC hookProc);

/**
 * Unregisters a previously registered callback function for a win event for this process.
 * It may be possible for the winEvent hook to fire one more time after unregistration if the unregistration happens within a winEvent hook.
 * @param hookProc the callback function to be unregistered
 * @return True if it was unregistered, false otherwize.
 */
DLLEXPORT bool unregisterWinEventHook(WINEVENTPROC hookProc);

//Windows hook registration

/**
 * Registers a callback function to be called with in future windows hooks fired for this process.
 * @param hookType the type of windows hook (WH_CALLWNDPROC, WH_GETMESSAGE)
 * @param procHook the callback function which should be called
 * @return true if the hook was registered, false otherwise.
 */
DLLEXPORT bool registerWindowsHook(int hookType, HOOKPROC hookProc);

/**
 * Unregisters a previously registered callback function for a windows hook for this process.
 * It may be possible for the windows hook to fire one more time after unregistration if the unregistration happens within a windows hook.
 * @param hookType the type of windows hook
 * @param hookProc the callback function to be unregistered
 * @return True if it was unregistered, false otherwize.
 */
DLLEXPORT bool unregisterWindowsHook(int hookType, HOOKPROC hookProc);

#endif