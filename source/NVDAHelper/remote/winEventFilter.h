//Copyright (c) 2009 Aleksey Sadovoy <lex@progger.ru>
//This file is covered by the GNU General Public Licence

#ifndef WINEventFILTER_H
#define WINEventFILTER_H
#include "nvdaHelperRemote.h"

#pragma pack(push)
#pragma pack(4)
struct winEvent_t {
	DWORD event;
	HWND window;
	LONG objectID;
	LONG childID;
	DWORD thread;
};
#pragma pack(pop)

void CALLBACK winEventFilterHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time);
bool winEventFilter_initialize();
void winEventFilter_terminate();
void winEventFilter_inProcess_initialize();
void winEventFilter_inProcess_terminate();
DLLEXPORT int getWinEvents(winEvent_t* arr, unsigned arrLength);

#endif