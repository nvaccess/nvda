//winEventFilter.cpp
//Copyright (C) 2009 Aleksey Sadovoy <lex@progger.ru>
//This file is covered by the GNU General Public Licence
//See the file Copying for details.

#include <algorithm>
#include <wchar.h>
#include <stdio.h>
#include <windows.h>
#include "nvdaHelperRemote.h"
#include "winEventFilter.h"

using namespace std;

const wchar_t winEventFilterSharedMem[]=L"Local\\NVDA_winEventFilterMem";
const unsigned sharedMemSize=1024*16;
const DWORD readyFlag=3492830629; //Some random value

#pragma pack(push)
#pragma pack(4)
struct winEventRecord_t {
	DWORD event;
	HWND window;
	LONG objectID;
	LONG childID;
	DWORD thread;
	LONG readyFlag;
};
const unsigned bufLength=(sharedMemSize-sizeof(LONG))/sizeof(winEventRecord_t); //Don't forget to update when sharedInfo_t changes!!!
struct sharedInfo_t {
	LONG eventWritten;
	winEventRecord_t events[bufLength];
};
#pragma pack(pop)

HANDLE hMapFile=0;
sharedInfo_t* pBuf=NULL;


bool winEventFilter_initialize() {
	hMapFile = CreateFileMapping(INVALID_HANDLE_VALUE,NULL,PAGE_READWRITE,0,sharedMemSize,winEventFilterSharedMem);
	if (!hMapFile) {
		fprintf(stderr,"Error: Could not create file mapping object (%d).\n",GetLastError());
		return false;
	}
	pBuf=(sharedInfo_t*)MapViewOfFile(hMapFile,FILE_MAP_ALL_ACCESS,0,0,sharedMemSize);
	if (!pBuf) {
		fprintf(stderr,"Error: MapVievOfFile failed (%d).\n",GetLastError());
		return false;
	}
	//Initialize an event record counter with NULL
	pBuf->eventWritten=0;
	return true;
}

void winEventFilter_terminate() {
	if (pBuf) UnmapViewOfFile((void*)pBuf);
	CloseHandle(hMapFile);
	hMapFile=0;
}

void winEventFilter_inProcess_initialize() {
	if (hMapFile) return; //already initialized
	//Open an already created file mapping
	hMapFile=OpenFileMapping(FILE_MAP_ALL_ACCESS,false,winEventFilterSharedMem);
	if (!hMapFile) {
		fprintf(stderr,"Error: Could not open file mapping object (%d).\n",GetLastError());
		return;
	}
	pBuf=(sharedInfo_t*)MapViewOfFile(hMapFile,FILE_MAP_ALL_ACCESS,0,0,sharedMemSize);
	if (!pBuf) {
		fprintf(stderr,"Error: MapVievOfFile failed (%d).\n",GetLastError());
		return;
	}
	//registerWinEventHook(winEventFilterHook);
}

void winEventFilter_inProcess_terminate() {
	//unregisterWinEventHook(winEventFilterHook);
	winEventFilter_terminate();
}

void CALLBACK winEventFilterHook(HWINEVENTHOOK hookID, DWORD eventID, HWND window, long objectID, long childID, DWORD threadID, DWORD time) {
	if (!pBuf) return;
	try {
		//Ignore all object IDs from alert onwards (sound, nativeom etc) as we don't support them
		if ((objectID<=OBJID_ALERT) ||
		//Also ignore all locationChange events except ones for the caret
		(eventID==EVENT_OBJECT_LOCATIONCHANGE && objectID!=OBJID_CARET)) 
			return;
		//Change window objIDs to client objIDs for better reporting of objects
		if ((objectID==0) && (childID==0)) objectID=OBJID_CLIENT;
		//Ignore events with invalid window handles
		bool isWindow=window?IsWindow(window) : false;
		if (!window || (!isWindow && (eventID == EVENT_SYSTEM_SWITCHSTART || eventID==EVENT_SYSTEM_SWITCHEND || eventID==EVENT_SYSTEM_MENUEND || eventID==EVENT_SYSTEM_MENUPOPUPEND)))
			window=GetDesktopWindow();
		else if (!isWindow) 
			return;
		wchar_t* buf=new wchar_t[256]; //Todo: really need to use one of excelent smart ptrs from the boost library here
		if (childID<0) {
			while (window && !(bool)(GetWindowLong(window,GWL_STYLE)&WS_POPUP)) {
				GetClassName(window,buf,255);
				if (wcscmp(buf,L"MozillaWindowClass")==0) window=GetAncestor(window,GA_PARENT);
				else break;
			}
		}
		GetClassName(window,buf,255);
		//At the moment we can't handle show, hide or reorder events on Mozilla Firefox Location bar,as there are just too many of them
		//Ignore show, hide and reorder on MozillaDropShadowWindowClass windows.
		if (equal(buf,buf+7,L"Mozilla") && childID<0 && (eventID==EVENT_OBJECT_SHOW || eventID==EVENT_OBJECT_HIDE || eventID==EVENT_OBJECT_REORDER)) {
			//Mozilla Gecko can sometimes fire win events on a catch-all window which isn't really the real window
			//Move up the ancestry to find the real mozilla Window and use that
			GetClassName(window,buf,255); //Strange, may be GetParent is forgoten here? just getting the ClassName second time
			if (wcscmp(buf,L"MozillaDropShadowWindowClass")==0) {
				delete []buf;
				return;
			}
		}
		//We never want to see foreground events for the Program Manager or Shell (task bar) 
		if (eventID==EVENT_SYSTEM_FOREGROUND && (wcscmp(buf,L"Progman")==0 || wcscmp(buf,L"Shell_TrayWnd")==0)) {
			delete []buf;
			return;
		}
		delete []buf;
		LONG offset=(InterlockedIncrement(&pBuf->eventWritten)-1) % bufLength; //We have a circular array
		//Get a reference to our struct
		winEventRecord_t& r=pBuf->events[offset];
		r.event=eventID;
		r.window=window;
		r.objectID=objectID;
		r.childID = childID;
		r.thread=threadID;
		InterlockedExchange(&r.readyFlag,readyFlag);
	} catch(...) {
		//Temporary, just play a beep
		Beep(440,35);
	}
}

//Client part
LONG eventReadCount=0; //how many events we've processed

int getWinEvents(winEvent_t* arr, unsigned arrLength) {
	if (!arr) return -1;
	if (pBuf->eventWritten-eventReadCount>bufLength) { //we are late. Skip some events
		eventReadCount+=pBuf->eventWritten-eventReadCount-bufLength;
	}
	unsigned totalEvents=min(arrLength,pBuf->eventWritten-eventReadCount); //How many to read
	totalEvents=min(totalEvents,bufLength);
	for (unsigned i=0; i<totalEvents; i++) {
		if (pBuf->events[eventReadCount%bufLength].readyFlag!=readyFlag) { //Yet unfinished data! Stopping
			return i;
		}
		memcpy(&arr[i],&pBuf->events[eventReadCount%bufLength],sizeof(winEvent_t));
		InterlockedExchange(&pBuf->events[eventReadCount%bufLength].readyFlag,0);
		eventReadCount++;
	}
	return totalEvents;
}
