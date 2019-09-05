#pragma once

#include <eventNotifier.h>

int RegisterAndPump_Async(
	NotifyCB_T notifyOfNewEventsCallback,
	DestroyEventCB_T notifyOfDestroyEventCallback
);

int RegisterAndPump_Join();

void FlushEvents();

unsigned int GetEventCount();

unsigned int GetEvents(
	IN unsigned int eventIndex,
	IN unsigned int maxEvents,
	OUT EventData * data
);

void PrintEvent(unsigned int eventIndex);