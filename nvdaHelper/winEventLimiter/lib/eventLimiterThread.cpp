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
#include "eventLimiterThread.h"

#include <algorithm>
#include <utility>

#include "eventDoubleBuffer.h"
#include "eventNotifier.h"
#include "utils.h"
#include "internalConstants.h"

namespace {

bool isEventIn(const DWORD idEvent, const std::vector<DWORD>& eventIds) {
	return std::find(eventIds.cbegin(), eventIds.cend(), idEvent) != eventIds.cend();
}

}  // namespace

EventLimiterThread::EventLimiterThread(
	EventNotifier& eventNotifier,
	EventDoubleBuffer& buffer
)
	: m_in(buffer)
	, m_eventNotifier(eventNotifier)
	, m_continue(true)
{
	m_thread = std::thread([this]() {
		_pushThroughEventLimiter();
	});
}

EventLimiterThread::~EventLimiterThread() {
	// Safety net so destruction without a prior Stop() cannot std::terminate on a joinable
	// thread. Joining here during DLL_PROCESS_DETACH could deadlock on the loader lock;
	// the supported teardown remains winEventLimiter_stop() before unload.
	Stop();
}

void EventLimiterThread::Stop() {
	m_continue = false;
	m_in.ReleaseBlockingSwap();
	if (m_thread.joinable()) {
		m_thread.join();
	}
}

// Main loop for this thread
void
EventLimiterThread::_pushThroughEventLimiter() {
	m_in.MakeSwapBlock(); // block until new events available
	while (m_continue) {
		m_in.SwapEventBuffers();
		m_classNameCacheHwnd = nullptr;
		bool shouldNotify = false;
		bool addedFocusEvent = false;
		for (auto& e : m_in.Read()) {
			if (e.idEvent == EVENT_OBJECT_DESTROY) {
				// Diverted before _preprocessEvent, deliberately raw: NVDA's
				// processDestroyWinEvent needs the original objectID (#2695), and the
				// invalid window drop must not apply to a window that is being destroyed.
				std::scoped_lock destroyLock(m_destroyEventsMutex);
				if (m_destroyEvents.size() >= MAX_BUFFERED_DESTROY_EVENTS) {
					m_destroyEvents.erase(
						m_destroyEvents.begin(),
						m_destroyEvents.begin()
							+ static_cast<std::ptrdiff_t>(MAX_BUFFERED_DESTROY_EVENTS / 2)
					);
					m_lostDestroys = true;
				}
				m_destroyEvents.push_back(e);
				shouldNotify = true;
				continue;
			}
			if (!e.bypassesPreprocessing && !_preprocessEvent(e)) continue;
			// #3831: Track must be atomic with FlushEventLimiter's defer check (both under
			// m_eventLimiterMutex), so a foreground event can never be flushed before it
			// was set for deferral.
			std::unique_lock lock(m_eventLimiterMutex);
			if (!e.bypassesPreprocessing) {
				m_deferredTracker.Track(e);
			}
			auto wasEventAdded = m_eventLimiter.AddEvent(e);
			shouldNotify = wasEventAdded || shouldNotify;
			// #14928: focus events should be pumped immediately rather than after a
			// delay
			addedFocusEvent = addedFocusEvent
				|| (wasEventAdded && e.idEvent == EVENT_OBJECT_FOCUS);
		}
		if (shouldNotify) {
			m_eventNotifier.NotifyClientOfNewEvents(addedFocusEvent);
		}
	}
}

bool EventLimiterThread::_preprocessEvent(EventData& e) {
	// Keep this filter chain aligned with internalWinEventHandler.winEventCallback.
	// Change window objIDs to client objIDs for better reporting of objects
	if (e.idObject == 0 && e.idChild == 0) {
		e.idObject = OBJID_CLIENT;
	}
	// Ignore events with invalid window handles
	// TODO: this logic can be cleaned up, e should be const.
	bool isWnd = IsWindow(e.hwnd);
	if (e.hwnd == nullptr || (!isWnd && isEventIn(e.idEvent, VALID_EVENTS_FOR_NON_WINDOWS))) {
		e.hwnd = GetDesktopWindow();
	}
	else if (!isWnd) {
		return false;
	}

	if (e.hwnd != m_classNameCacheHwnd) {
		m_classNameCache = _getClassName(e.hwnd);
		m_classNameCacheHwnd = e.hwnd;
	}
	const std::wstring& windowClassName = m_classNameCache;

	// #11818: Excel produces UI Automation events which are proxied by Windows into MSAA
	// winEvents. In certain builds of Excel 2016, responding to these can freeze NVDA
	// for several seconds. NVDA doesn't need these MSAA events for its Excel support,
	// so just ignore them early.
	if (windowClassName == L"EXCEL7" && e.idObject > 0) {
		return false;
	}

	if (windowClassName == L"ConsoleWindowClass") {
		// #10554: Windows forces the reported thread of console windows to match the
		// thread of the first attached process, but NVDA needs the thread the window
		// was really created in (inside conhost), e.g. to speak typed characters in
		// the correct language. winEvents always carry the true thread ID, so record
		// it here; NVDA fetches it via winEventLimiter_getConsoleThreadID.
		std::scoped_lock lock(m_consoleThreadIDsMutex);
		m_consoleThreadIDs[e.hwnd] = e.dwEventThread;
	}

	// Modern IME candidate list windows fire menu events which confuse us
	// and can't be used properly in conjunction with input composition support.
	if (windowClassName == L"Microsoft.IME.UIManager.CandidateWindow.Host"
		&& isEventIn(e.idEvent, MENU_EVENTIDS)
		) {
		return false;
	}

	// We never want to see foreground events for the Program Manager or Shell(task bar)
	if (e.idEvent == EVENT_SYSTEM_FOREGROUND
		&& UNWANTED_FOREGROUND_EVENTS.end() != std::find(UNWANTED_FOREGROUND_EVENTS.begin(), UNWANTED_FOREGROUND_EVENTS.end(), windowClassName)
		) {
		return false;
	}

	if (windowClassName == L"MSNHiddenWindowClass") {
		// HACK : Events get fired by this window in Windows Live Messenger 2009 when it starts.
		// If we send a WM_NULL to this window at this point(which happens in accessibleObjectFromEvent), Messenger will silently exit(#677).
		// Therefore, completely ignore these events, which is useless to us anyway.
		return false;
	}
	return true;
}

DWORD EventLimiterThread::GetConsoleThreadID(HWND hwnd) {
	std::scoped_lock lock(m_consoleThreadIDsMutex);
	const auto itr = m_consoleThreadIDs.find(hwnd);
	return itr != m_consoleThreadIDs.end() ? itr->second : 0;
}


void EventLimiterThread::SetAlwaysAllowedObject(HWND hwnd, LONG idObject, LONG idChild) {
	{ // scope of lock
		std::unique_lock lock(m_eventLimiterMutex);
		m_eventLimiter.SetAlwaysAllowedObject(hwnd, idObject, idChild);
	} // end lock
	// The double buffer prefers keeping this object's events when its overflow trim
	// runs; it takes its own leaf mutex, never nested with m_eventLimiterMutex.
	m_in.SetAlwaysAllowedObject(hwnd, idObject, idChild);
}

EventBuffer
EventLimiterThread::FlushEventLimiter(bool& deferred) {
	m_eventNotifier.ResetNotify();

	deferred = false;
	bool hasPendingDestroyEvents = false;
	EventBuffer out;
	{ // scope of lock
		// The destroy check and regular flush must be atomic. The limiter thread
		// processes its input in order, so holding both locks ensures that a destroy
		// cannot be queued while a later regular event enters this flush.
		std::scoped_lock lock(m_eventLimiterMutex, m_destroyEventsMutex);
		const bool shouldDeferForForeground = m_deferredTracker.ShouldDeferEvents();
		hasPendingDestroyEvents = !m_destroyEvents.empty();
		const bool shouldDeferForDestroy = hasPendingDestroyEvents
			&& m_destroyDefers < MAX_FOREGROUND_DEFERS;
		m_destroyDefers = shouldDeferForDestroy ? m_destroyDefers + 1 : 0;
		deferred = shouldDeferForForeground || shouldDeferForDestroy;
		if (!deferred) {
			if (hasPendingDestroyEvents) {
				// A continuous stream of late destroys must not starve regular events,
				// but those events may refer to an object whose destroy is still pending.
				// Escalate to whole-cache recovery before allowing the capped flush.
				m_lostDestroys = true;
			}
			out = m_eventLimiter.Flush();
		}
	} // end lock
	if (deferred || hasPendingDestroyEvents) {
		// A late destroy still needs another pump when the defer cap lets regular
		// events through. Otherwise ResetNotify can consume its only notification.
		// The callback may call into Python, so it must run outside any lock.
		m_eventNotifier.NotifyClientOfNewEvents(false);
	}
	return out;
}

EventBuffer
EventLimiterThread::TakeDestroyEvents() {
	std::scoped_lock lock(m_destroyEventsMutex);
	return std::exchange(m_destroyEvents, EventBuffer());
}

bool EventLimiterThread::TakeLostDestroys() {
	std::scoped_lock lock(m_destroyEventsMutex);
	return std::exchange(m_lostDestroys, false);
}
