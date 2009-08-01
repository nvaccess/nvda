//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence

#ifndef HOOKREGISTRATION_H
#define HOOKREGISTRATION_H

#include <windows.h>

#define DLLEXPORT extern "C" __declspec(dllexport)

//Win event registration

/**
 * Registers a callback function to be called with in future win events fired for the calling thread
 * @param procHook the callback function which should be called
 * @return true if the hook was registered, false otherwise.
 */
DLLEXPORT bool registerWinEventHook(WINEVENTPROC hookProc);

/**
 * Unregisters a previously registered callback function for a win event for the calling thread
 * @param hookProc the callback function to be unregistered
 * @return True if it was unregistered, false otherwize.
 */
DLLEXPORT bool unregisterWinEventHook(WINEVENTPROC hookProc);

//Windows hook registration

/**
 * Registers a callback function to be called with in future windows hooks fired for the calling thread with the given hook type
 * @param hookType the type of windows hook (WH_CALLWNDPROC, WH_GETMESSAGE)
 * @param procHook the callback function which should be called
 * @return true if the hook was registered, false otherwise.
 */
DLLEXPORT bool registerWindowsHook(int hookType, HOOKPROC hookProc);

/**
 * Unregisters a previously registered callback function for a windows hook for the calling thread with the given hook type
 * @param hookType the type of windows hook
 * @param hookProc the callback function to be unregistered
 * @return True if it was unregistered, false otherwize.
 */
DLLEXPORT bool unregisterWindowsHook(int hookType, HOOKPROC hookProc);

#endif
