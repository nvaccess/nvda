//Copyright (c) 2009-2010 Aleksey Sadovoy <lex@progger.ru>
//This file is covered by the GNU General Public Licence

#ifndef WINEventFILTER_H
#define WINEventFILTER_H
#include "nvdaHelperRemote.h"

#pragma pack(push)
#pragma pack(4)
struct winEvent_t {
	DWORD event;
	DWORD window;
	LONG objectID;
	LONG childID;
	DWORD thread;
	winEvent_t(DWORD _event=0, DWORD _window=0, LONG _objectID=0, LONG _childID=0, DWORD _thread=0):
		event(_event),window(_window),objectID(_objectID),childID(_childID),thread(_thread) { }
	bool operator< (const winEvent_t& other) const {
		return memcmp(this,&other,sizeof(winEvent_t))<0;
	}
};
#pragma pack(pop)

bool winEventFilter_initialize();
void winEventFilter_terminate();
void winEventFilter_inProcess_initialize();
void winEventFilter_inProcess_terminate();
DLLEXPORT int getWinEvents(winEvent_t* arr, unsigned arrLength);

#endif