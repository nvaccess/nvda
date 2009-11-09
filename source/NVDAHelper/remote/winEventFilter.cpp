//winEventFilter.cpp
//Copyright (C) 2009 Aleksey Sadovoy <lex@progger.ru>
//This file is covered by the GNU General Public Licence
//See the file Copying for details.

#include <algorithm>
#include <map>
#include <queue>
#include <wchar.h>
#include <stdio.h>
#include <boost/noncopyable.hpp>
#include <boost/foreach.hpp>
#include <windows.h>
#include <ia2/ia2.h>
#include "nvdaHelperRemote.h"
#include "winEventFilter.h"

using namespace std;

const wchar_t winEventFilterSharedMem[]=L"Local\\NVDA_winEventFilterMem";
const unsigned sharedMemSize=1024*16;
const DWORD readyFlag=3492830629; //Some random value

#pragma pack(push)
#pragma pack(4)
struct winEventRecord_t: public winEvent_t {
	/*DWORD event;
	HWND window;
	LONG objectID;
	LONG childID;
	DWORD thread;*/
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
vector<HWINEVENTHOOK> winEventHookIDs;
DWORD allowedWinEventIDs[]={EVENT_SYSTEM_DESKTOPSWITCH,EVENT_SYSTEM_FOREGROUND,EVENT_SYSTEM_ALERT,EVENT_SYSTEM_MENUSTART,EVENT_SYSTEM_MENUEND,EVENT_SYSTEM_MENUPOPUPSTART,EVENT_SYSTEM_MENUPOPUPEND,EVENT_SYSTEM_SCROLLINGSTART,EVENT_SYSTEM_SWITCHEND,EVENT_OBJECT_FOCUS,EVENT_OBJECT_SHOW,EVENT_OBJECT_DESTROY,EVENT_OBJECT_HIDE,EVENT_OBJECT_DESCRIPTIONCHANGE,EVENT_OBJECT_LOCATIONCHANGE,EVENT_OBJECT_NAMECHANGE,EVENT_OBJECT_SELECTION,EVENT_OBJECT_SELECTIONADD,EVENT_OBJECT_SELECTIONREMOVE,EVENT_OBJECT_SELECTIONWITHIN,EVENT_OBJECT_STATECHANGE,EVENT_OBJECT_VALUECHANGE,IA2_EVENT_TEXT_CARET_MOVED,IA2_EVENT_DOCUMENT_LOAD_COMPLETE,IA2_EVENT_OBJECT_ATTRIBUTE_CHANGED};

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
}

void winEventFilter_inProcess_terminate() {
	if (pBuf) UnmapViewOfFile((void*)pBuf);
	CloseHandle(hMapFile);
	hMapFile=0;
}

void CALLBACK winEventFilterHook(HWINEVENTHOOK hookID, DWORD eventID, HWND window, long objectID, long childID, DWORD threadID, DWORD time) {
	if (!pBuf) return;
	try {
		//Ignore all object IDs from alert onwards (sound, nativeom etc) as we don't support them
		if ((objectID<=OBJID_ALERT) ||
		//Also ignore all locationChange events except ones for the caret
		(eventID==EVENT_OBJECT_LOCATIONCHANGE && objectID!=OBJID_CARET) ||
		(eventID==EVENT_OBJECT_FOCUS && (objectID == OBJID_SYSMENU || objectID==OBJID_MENU) && childID==0) //This is a focus event on a menu bar itself, which is just silly. Ignore it
			) return;
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
	struct orderedWinEvent_t: public winEvent_t {
		long int count;
		orderedWinEvent_t(DWORD _event=0, HWND _window=0, LONG _objectID=0, LONG _childID=0, DWORD _thread=0,long int _count=-1):
		winEvent_t(_event,_window,_objectID,_childID,_thread),count(_count) { }
		bool operator<(const orderedWinEvent_t& other) const { return count<other.count; }
	};
bool _eventCmp(const orderedWinEvent_t* a, const orderedWinEvent_t* b) { return a->count < b->count; }
class OrderedWinEventLimiter: public boost::noncopyable {
	static const unsigned MAX_WINEVENTS_PER_THREAD=10;
	typedef map<winEvent_t,long> winEventMap_t;
	winEventMap_t focusEventCache,genericEventCache;
	orderedWinEvent_t lastMenuEvent;
	unsigned maxFocusItems;
	typedef priority_queue<orderedWinEvent_t/**,vector<orderedWinEvent_t*>,bool(*)(const orderedWinEvent_t*, const orderedWinEvent_t*)*/> eventQueue_t;
	eventQueue_t eventQueue;

	public:
	OrderedWinEventLimiter(const unsigned aMaxFocusItems=3):maxFocusItems(aMaxFocusItems)/*,eventQueue(_eventCmp)*/ { }
	//Returns number of events added (negative values mean that an event was removed instead)
	int addEvent(const winEvent_t& ev) {
		//seems as we add foreground events twice, both to the focusEventCache and genericEventCache
		//so we need to track this to be able to return number of events added
		unsigned result=0;
		//Filtering events for UIA windows is not implemented yet
		switch (ev.event) {
			case EVENT_OBJECT_FOCUS:
			//We do not need a focus event on an object if we already got a foreground event for it
			if (focusEventCache.count(winEvent_t(EVENT_SYSTEM_FOREGROUND,ev.window,ev.objectID,ev.childID,ev.thread))) return 0;
			focusEventCache[ev]=eventReadCount;
			return 1;
			break; //Never goes here
			case EVENT_SYSTEM_FOREGROUND:
			result=1;
			result-=focusEventCache.erase(winEvent_t(EVENT_OBJECT_FOCUS,ev.window,ev.objectID,ev.childID,ev.thread));
			focusEventCache[ev]=eventReadCount;
			return result;
			break;
			case EVENT_OBJECT_SHOW:
			if (genericEventCache.erase(winEvent_t(EVENT_OBJECT_HIDE,ev.window,ev.objectID,ev.childID,ev.thread))) return -1;
			break;
			case EVENT_OBJECT_HIDE:
			if (genericEventCache.erase(winEvent_t(EVENT_OBJECT_SHOW,ev.window,ev.objectID,ev.childID,ev.thread))) return -1;
			break;
			case EVENT_OBJECT_DESTROY:
			if (genericEventCache.erase(winEvent_t(EVENT_OBJECT_CREATE,ev.window,ev.objectID,ev.childID,ev.thread))) return -1;
			break;
			case EVENT_SYSTEM_MENUSTART:
			case EVENT_SYSTEM_MENUEND:
			case EVENT_SYSTEM_MENUPOPUPSTART:
			case EVENT_SYSTEM_MENUPOPUPEND:
			memcpy(&lastMenuEvent,&ev,sizeof(winEvent_t));
			lastMenuEvent.count=eventReadCount;
			return 1;
			break;
		}
		genericEventCache[ev]=eventReadCount;
		return 1+result; 
	}

	//returns number of events added to the arr. Arr must always have enough size
	unsigned flushEvents(winEvent_t arr[]) {
		if (lastMenuEvent.count!=-1) eventQueue.push(lastMenuEvent);
		//Move generic events to array, converting from winEvent_t to orderedWinEvent_t
		vector<orderedWinEvent_t> genericEventArray;
		genericEventArray.reserve(genericEventCache.size());
		BOOST_FOREACH (winEventMap_t::value_type i, genericEventCache)
			genericEventArray.push_back(orderedWinEvent_t(i.first.event,i.first.window,i.first.objectID,i.first.childID,i.first.thread,i.second));
		genericEventCache.clear();
		sort(genericEventArray.begin(),genericEventArray.end());
		//Limit them by thread
		map<DWORD,long> threadCounters;
		BOOST_REVERSE_FOREACH (orderedWinEvent_t i,genericEventArray) {
			long& threadCount=threadCounters[i.thread];
			if (threadCount>MAX_WINEVENTS_PER_THREAD) continue;
			eventQueue.push(i);
			threadCount++;
		}
		//now copy the focus events
		vector<orderedWinEvent_t> focusEventArray;
		focusEventArray.reserve(focusEventCache.size());
		BOOST_FOREACH (winEventMap_t::value_type i, focusEventCache) 
			focusEventArray.push_back(orderedWinEvent_t(i.first.event,i.first.window,i.first.objectID,i.first.childID,i.first.thread,i.second));
		focusEventCache.clear();
		sort(focusEventArray.begin(),focusEventArray.end());
		//add only last maxFocusItems into queue
		for (vector<orderedWinEvent_t>::reverse_iterator i=focusEventArray.rbegin(); i!=focusEventArray.rbegin()+min(focusEventArray.size(),maxFocusItems); ++i)
			eventQueue.push(*i);
		//now eventQueue contains a sorted list of pointers
		//Copy events to arr
		int queueSize=eventQueue.size();
		for (int i=queueSize-1; i>=0; --i) {
			arr[i]=eventQueue.top();
			eventQueue.pop();
		}
	lastMenuEvent.count=-1; //mark as empty
	return queueSize;
	}
};

OrderedWinEventLimiter* eventLimiter=NULL;

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
	if (!eventLimiter) eventLimiter = new OrderedWinEventLimiter();
	BOOST_FOREACH (DWORD eventID, allowedWinEventIDs) {
		HWINEVENTHOOK hookID=SetWinEventHook(eventID,eventID,moduleHandle,winEventFilterHook,0,0,WINEVENT_INCONTEXT);
		winEventHookIDs.push_back(hookID);
	}
	return true;
}

void winEventFilter_terminate() {
	if (pBuf) UnmapViewOfFile((void*)pBuf);
	CloseHandle(hMapFile);
	hMapFile=0;
	if (eventLimiter) {
		delete eventLimiter;
		eventLimiter=NULL;
	}
	BOOST_FOREACH(HWINEVENTHOOK hookID, winEventHookIDs) 
		UnhookWinEvent(hookID);
	winEventHookIDs.clear();
}

int getWinEvents(winEvent_t* arr, unsigned arrLength) {
	if (!arr) return -1;
	if (pBuf->eventWritten-eventReadCount>bufLength) { //we are late. Skip some events
		eventReadCount+=pBuf->eventWritten-eventReadCount-bufLength;
	}
	unsigned maxEvents=min(bufLength,pBuf->eventWritten-eventReadCount); //How many to read
	unsigned eventsTotal=0; //How many events was actually added to the limiter
	for (unsigned i=0; i<maxEvents; i++) {
		if (pBuf->events[eventReadCount%bufLength].readyFlag!=readyFlag) { //Yet unfinished data! Stopping
			break;
		}
		eventsTotal+=eventLimiter->addEvent(pBuf->events[eventReadCount%bufLength]);
		InterlockedExchange(&pBuf->events[eventReadCount%bufLength].readyFlag,0);
		eventReadCount++;
		if (eventsTotal>=arrLength) break;
	}
	return eventLimiter->flushEvents(arr);
}
