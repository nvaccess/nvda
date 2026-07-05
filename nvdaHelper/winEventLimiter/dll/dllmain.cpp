/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2019-2026 NV Access Limited, Bill Dengler
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2.0, as published by
the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

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

#include <memory>
#include <mutex>
#include <utility>
#include <vector>

#include "winEventLimiterDll.h"
#include <eventNotifier.h>
#include <eventDoubleBuffer.h>
#include <eventLimiterThread.h>
#include <messagePump.h>
#include <utils.h>

// These holders are reset on winEventLimiter_stop. Keeping the empty holders
// alive at process exit avoids running thread-owning destructors under the loader lock
// when a host terminates without calling winEventLimiter_stop.
std::unique_ptr<EventDoubleBuffer>& g_doubleBuffer =
	*new std::unique_ptr<EventDoubleBuffer>();
std::unique_ptr<EventLimiterThread>& g_limiterThread =
	*new std::unique_ptr<EventLimiterThread>();
std::unique_ptr<EventNotifier>& g_eventNotifier =
	*new std::unique_ptr<EventNotifier>();
EventBuffer g_out;
EventBuffer g_destroyOut;

namespace {

std::mutex g_stateMutex;
bool g_acceptsAddedEvents = false;

// Tear down all module state so that a future winEventLimiter_start starts from scratch.
// Only call once both threads have been stopped (or never started).
void _resetGlobals() {
	// MessagePumpThread's own singleton reference is its single owner.
	MessagePumpThread::ResetInstance();
	{
		std::scoped_lock lock(g_stateMutex);
		g_limiterThread.reset();
		g_acceptsAddedEvents = false;
		g_doubleBuffer.reset();
	}
	g_eventNotifier.reset();
	g_out.clear();
	g_destroyOut.clear();
}

unsigned int _copyEvents(
	const EventBuffer& source,
	unsigned int eventIndex,
	unsigned int maxEvents,
	EventData* data
) {
	auto eventsReturned = 0u;
	for (auto vecIndex = eventIndex;
		vecIndex < source.size() && eventsReturned < maxEvents;
		++vecIndex, ++eventsReturned
		) {
		data[eventsReturned] = source[vecIndex];
	}
	return eventsReturned;
}

}  // namespace

int winEventLimiter_start(
	NotifyCB_T notifyOfNewEventsCallback,
	IN const DWORD* eventIds,
	IN unsigned int eventIdCount
) {
	if (MessagePumpThread::GetExistingInstance()) {
		return -1; // No consideration has been given to multiple messagePumps.
	}
	if (eventIds == nullptr || eventIdCount == 0) {
		return -3;
	}
	int result;
	try {
		std::vector<DWORD> eventIdsToHook(eventIds, eventIds + eventIdCount);
		g_doubleBuffer = std::make_unique<EventDoubleBuffer>();
		g_eventNotifier = std::make_unique<EventNotifier>(
			std::function<NotifyCB_T>(notifyOfNewEventsCallback)
			);
		{
			std::scoped_lock lock(g_stateMutex);
			g_limiterThread = std::make_unique<EventLimiterThread>(*g_eventNotifier, *g_doubleBuffer);
		}
		WriteBuffer& buf = *g_doubleBuffer;
		auto messagePump = MessagePumpThread::GetInstance(buf, std::move(eventIdsToHook));
		result = messagePump->Start();
	}
	catch (...) {
		// E.g. a std::thread that could not start. Unwinding into ctypes would surface
		// as SEH and skip the cleanup below, stranding whatever was already created.
		result = -5;
	}
	if (result != 0) {
		// Leave the process clean so the caller can fall back to in-process hooking.
		// The pump thread was already joined by the failed Start.
		if (g_eventNotifier) {
			g_eventNotifier->Invalidate();
		}
		if (g_limiterThread) {
			g_limiterThread->Stop();
		}
		_resetGlobals();
	}
	else {
		std::scoped_lock lock(g_stateMutex);
		g_acceptsAddedEvents = true;
	}
	return result;
}

int winEventLimiter_stop() {
	auto ret = 0;
	{
		std::scoped_lock lock(g_stateMutex);
		g_acceptsAddedEvents = false;
	}
	// Block the callback first, so the client never gets called back mid-teardown.
	if (g_eventNotifier) {
		g_eventNotifier->Invalidate();
	}
	auto messagePump = MessagePumpThread::GetExistingInstance();
	if (!messagePump) {
		ret |= 1;
	}
	else {
		messagePump->Stop();
	}
	if (!g_limiterThread) {
		ret |= 2;
	}
	else {
		g_limiterThread->Stop();
	}
	_resetGlobals();
	return ret;
}

int winEventLimiter_addEvent(
	IN DWORD idEvent,
	IN HWND hwnd,
	IN LONG idObject,
	IN LONG idChild,
	IN DWORD dwEventThread
) {
	std::scoped_lock lock(g_stateMutex);
	if (!g_acceptsAddedEvents || !g_doubleBuffer) {
		return -1;
	}
	const EventData event{
		idEvent,
		hwnd,
		idObject,
		idChild,
		dwEventThread,
		GetTickCount(),
		true, // Match direct insertion into the in-process limiter.
	};
	g_doubleBuffer->Write(event);
	return 0;
}

int winEventLimiter_flushEvents() {
	if (!g_limiterThread) {
		g_out.clear();
		return 0;
	}
	bool deferred = false;
	g_out = g_limiterThread->FlushEventLimiter(deferred);
	return deferred ? 1 : 0;
}

unsigned int
winEventLimiter_getEventCount() {
	return static_cast<unsigned int>(g_out.size());
}

unsigned int
winEventLimiter_getEvents(
	IN unsigned int eventIndex,
	IN unsigned int maxEvents,
	OUT EventData * data
) {
	return _copyEvents(g_out, eventIndex, maxEvents, data);
}

void winEventLimiter_flushDestroyEvents() {
	if (!g_limiterThread) {
		g_destroyOut.clear();
		return;
	}
	g_destroyOut = g_limiterThread->TakeDestroyEvents();
}

unsigned int
winEventLimiter_getDestroyEventCount() {
	return static_cast<unsigned int>(g_destroyOut.size());
}

unsigned int
winEventLimiter_getDestroyEvents(
	IN unsigned int eventIndex,
	IN unsigned int maxEvents,
	OUT EventData * data
) {
	return _copyEvents(g_destroyOut, eventIndex, maxEvents, data);
}

int winEventLimiter_takeLostDestroys() {
	bool lost = false;
	if (g_doubleBuffer) {
		lost |= g_doubleBuffer->TakeLostDestroys();
	}
	if (g_limiterThread) {
		lost |= g_limiterThread->TakeLostDestroys();
	}
	return lost ? 1 : 0;
}

int winEventLimiter_setAlwaysAllowedObject(
	IN HWND hwnd,
	IN LONG idObject,
	IN LONG idChild
) {
	if (!g_limiterThread) {
		return -1;
	}
	g_limiterThread->SetAlwaysAllowedObject(hwnd, idObject, idChild);
	return 0;
}

DWORD winEventLimiter_getConsoleThreadID(IN HWND hwnd) {
	std::scoped_lock lock(g_stateMutex);
	if (!g_limiterThread) {
		return 0;
	}
	return g_limiterThread->GetConsoleThreadID(hwnd);
}
