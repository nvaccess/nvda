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

#pragma once
#include "stdafx.h"
#include <thread>
#include <atomic>
#include <map>
#include <mutex>
#include <string>
#include "eventBufferLimits.h"
#include "winEventLimiter.h"
#include "deferredForegroundWindowHandler.h"

class EventNotifier;
class EventDoubleBuffer;

class EventLimiterThread
{
public:
	EventLimiterThread(EventNotifier& eventNotifier, EventDoubleBuffer& buffer);
	~EventLimiterThread();

	void Stop();

	// Prepares m_out for fetching events from NVDA.
	// deferred is set when a foreground change is still settling (#3831), or when a
	// destroy arrived after this cycle's TakeDestroyEvents: nothing was flushed, and
	// another pump has already been requested via the notifier, so the client can hold
	// its whole cycle and process the destroy before later regular events.
	EventBuffer FlushEventLimiter(bool& deferred);

	// Hands over the destroy events collected since the last call, so NVDA can process
	// them before this cycle's other events. Independent of the foreground defer.
	EventBuffer TakeDestroyEvents();

	// If NVDA's core stalls and stops fetching, the destroy queue must not grow without
	// bound; on reaching this size, the oldest half is discarded and the loss is
	// reported via TakeLostDestroys.
	static constexpr EventBuffer::size_type MAX_BUFFERED_DESTROY_EVENTS =
		eventBufferLimits::MAX_BUFFERED_EVENTS;

	// Whether the destroy queue has discarded an event, or a pending destroy reached the
	// regular-event defer cap, since the last call; reading clears the flag. The client
	// must then treat every window as potentially destroyed, since cache eviction can no
	// longer rely on per-window destroy ordering.
	bool TakeLostDestroys();

	// Thread safe access to WinEventLimiter::SetAlwaysAllowedObject.
	void SetAlwaysAllowedObject(HWND hwnd, LONG idObject, LONG idChild);

	// #10554: The thread a ConsoleWindowClass window was really created in
	// (as recorded from its winEvents), or 0 if unknown.
	DWORD GetConsoleThreadID(HWND hwnd);
private:
	EventDoubleBuffer& m_in;
	EventNotifier& m_eventNotifier;
	DeferredForegroundWindowEventHandler m_deferredTracker;
	WinEventLimiter m_eventLimiter;
	std::mutex m_eventLimiterMutex;
	EventBuffer m_destroyEvents;
	std::mutex m_destroyEventsMutex;
	// Guarded by m_destroyEventsMutex.
	bool m_lostDestroys = false;
	unsigned int m_destroyDefers = 0;
	std::map<HWND, DWORD> m_consoleThreadIDs;
	std::mutex m_consoleThreadIDsMutex;
	// One-entry cache for _preprocessEvent's GetClassNameW calls: floods are typically
	// bursts from one window. Limiter thread only; reset each batch (HWND reuse).
	HWND m_classNameCacheHwnd = nullptr;
	std::wstring m_classNameCache;
	std::atomic<bool> m_continue;
	std::thread m_thread;

	// Main thread loop
	// - Swaps the read/write buffers in EventDoubleBuffer
	// - Takes events from the read buffer feeding to the WinEventLimiter
	void _pushThroughEventLimiter();

	// Filters and transforms an event before it enters the limiter
	// Returns false if the event should be dropped.
	bool _preprocessEvent(EventData& e);
};
