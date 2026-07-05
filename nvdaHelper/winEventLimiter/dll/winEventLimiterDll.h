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

#include <eventData.h>
#include <eventNotifier.h>

// The flush/event retrieval/setAlwaysAllowed functions below are not thread safe with
// respect to each other: NVDA calls them all from its main thread.
// winEventLimiter_addEvent and winEventLimiter_getConsoleThreadID are thread safe.
extern "C" {

// Starts receiving and limiting winEvents.
// One hook is registered per entry of eventIds (which is copied before returning).
// Returns 0 on success, -1 if already started, -2 if no hook could be registered,
// -3 on invalid arguments, -4 if the pump's shutdown event could not be created,
// -5 on an internal failure (the module is left reset, like the other error paths).
int winEventLimiter_start(
	NotifyCB_T notifyOfNewEventsCallback,
	IN const DWORD* eventIds,
	IN unsigned int eventIdCount
);

int winEventLimiter_stop();

// Adds an event to the same input buffer as hooked winEvents, preserving their shared
// insertion order before limiting. The event time is captured by this function.
// Returns 0 on success, -1 if the limiter is not running.
int winEventLimiter_addEvent(
	IN DWORD idEvent,
	IN HWND hwnd,
	IN LONG idObject,
	IN LONG idChild,
	IN DWORD dwEventThread
);

// Snapshots the limited events for fetching.
// Returns 1 if the flush was deferred because a foreground change is still settling
// (#3831), or a destroy arrived after the client's destroy snapshot: nothing was
// flushed, another pump has already been requested via the notify callback, and the
// client should hold its whole cycle. Returns 0 otherwise.
int winEventLimiter_flushEvents();

unsigned int winEventLimiter_getEventCount();

unsigned int winEventLimiter_getEvents(
	IN unsigned int eventIndex,
	IN unsigned int maxEvents,
	OUT EventData * data
);

// Snapshots the pending destroy events for fetching, independently of the regular flush:
// processing a destroy may correct the client's focus, so the client should flush and
// process destroys before deciding this cycle's focused object and flushing the regular
// events.
void winEventLimiter_flushDestroyEvents();

// Destroy events snapshotted by the last winEventLimiter_flushDestroyEvents. They are
// delivered raw (no OBJID_CLIENT remap, no invalid window drop; see EventLimiterThread)
// and are never gated by the foreground defer.
unsigned int winEventLimiter_getDestroyEventCount();

unsigned int winEventLimiter_getDestroyEvents(
	IN unsigned int eventIndex,
	IN unsigned int maxEvents,
	OUT EventData * data
);

// Whether a destroy event has been discarded, or its ordering relative to regular
// events could not be preserved at the defer cap, since the last call. Reading clears
// the flag.
int winEventLimiter_takeLostDestroys();

// #11520: Exempts events for the given object from the per thread limit.
// All zeros clears the exemption.
// Returns 0 on success, -1 if the limiter is not running.
int winEventLimiter_setAlwaysAllowedObject(
	IN HWND hwnd,
	IN LONG idObject,
	IN LONG idChild
);

// #10554: The thread a ConsoleWindowClass window was really created in
// (as recorded from its winEvents), or 0 if unknown or not running.
DWORD winEventLimiter_getConsoleThreadID(IN HWND hwnd);

}
