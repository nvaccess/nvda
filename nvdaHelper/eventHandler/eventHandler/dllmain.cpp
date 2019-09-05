// dllmain.cpp : Defines the entry point for the DLL application.
#include "stdafx.h"

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
};

#include <optional>
#include <thread>
#include <future>
#include <condition_variable>
#include <atomic>
#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>

#include "eventHandlerDll.h"
#include <eventNotifier.h>
#include <eventDoubleBuffer.h>
#include <eventLimiterThread.h>
#include <messagePump.h>
#include <utils.h>

std::shared_ptr<MessagePumpThread> g_messagePump;
std::unique_ptr<EventDoubleBuffer> g_doubleBuffer;
std::unique_ptr<EventLimiterThread> g_limiterThread;
std::unique_ptr<EventNotifier> g_eventNotifier;
EventBuffer g_out;

int RegisterAndPump_Async(
	NotifyCB_T notifyOfNewEventsCallback,
	DestroyEventCB_T notifyOfDestroyEventCallback
) {
	if (g_messagePump) {
		return -1; // No consideration has been given to multiple messagePumps.
	}
	g_doubleBuffer = std::make_unique<EventDoubleBuffer>();
	g_eventNotifier = std::make_unique<EventNotifier>(
		std::function<NotifyCB_T>(notifyOfNewEventsCallback),
		std::function<DestroyEventCB_T>(notifyOfDestroyEventCallback)
		);
	g_limiterThread = std::make_unique<EventLimiterThread>(*g_eventNotifier, *g_doubleBuffer);
	WriteBuffer& buf = *g_doubleBuffer;
	g_messagePump = MessagePumpThread::GetInstance(*g_eventNotifier, buf);
	auto result = g_messagePump->Start();
	return result;
}

int RegisterAndPump_Join() {
	auto ret = 0u;
	if (!g_messagePump) {
		ret &= 1;
	}
	else {
		g_messagePump->Stop();
	}
	if (!g_limiterThread) {
		ret &= 2;
	}
	else {
		g_limiterThread->Stop();
	}
	return ret;
}

void FlushEvents() {
	g_out = g_limiterThread->FlushEventLimiter();
}

unsigned int
GetEventCount() {
	return static_cast<unsigned int>(g_out.size());
}

unsigned int
GetEvents(
	IN unsigned int eventIndex,
	IN unsigned int maxEvents,
	OUT EventData * data
) {
	auto eventsReturned = 0u;
	for (auto vecIndex = eventIndex;
		vecIndex < g_out.size() && eventsReturned < maxEvents;
		++vecIndex, ++eventsReturned
		) {
		data[eventsReturned] = g_out[vecIndex];
	}
	return eventsReturned;
}


void PrintEvent(unsigned int eventIndex) {
	EventData e;
	std::stringstream sstream;
	auto constexpr MAX_EVENTS = 1u;
	const auto gotCount = GetEvents(eventIndex, MAX_EVENTS, &e);
	if (0u < gotCount && gotCount <= MAX_EVENTS) {
		const auto eName = getEventName(e.idEvent);
		sstream << std::hex << std::showbase <<
			" eventID: " << e.idEvent <<
			" eventName: " << eName <<
			" hwnd: " << e.hwnd <<
			" idObject: " << e.idObject <<
			" idChild: " << e.idChild <<
			" eventThread: " << e.dwEventThread <<
			" eventTime: " << e.dwmsEventTime
			<< '\n';
	}
	else {
		const auto eCount = GetEventCount();
		sstream << "failed to get event at index: " << eventIndex << " from outBuffer with size: " << eCount << '\n';
	}
	std::cout << sstream.str();
}
