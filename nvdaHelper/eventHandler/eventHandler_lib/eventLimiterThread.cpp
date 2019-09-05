#include "stdafx.h"
#include "eventLimiterThread.h"
#include "eventDoubleBuffer.h"
#include "eventNotifier.h"
#include "utils.h"
#include "internalConstants.h"

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

EventLimiterThread::~EventLimiterThread(){}

void EventLimiterThread::Stop() {
	m_continue = false;
	m_in.ReleaseBlockingSwap();
	m_thread.join();
}

bool _preprocessEvent(EventData& e);

// Main loop for this thread
void
EventLimiterThread::_pushThroughEventLimiter() {
	m_in.MakeSwapBlock(); // don't spin, block until new events available.
	while (m_continue) {
		m_in.SwapEventBuffers();
		bool shouldNotify = false;
		for (auto& e : m_in.Read()) {
			if (!_preprocessEvent(e)) continue;
			m_deferredTracker.Track(e);
			std::unique_lock lock(m_eventLimiterMutex);
			auto wasEventAdded = m_eventLimiter.AddEvent(e);
			shouldNotify = wasEventAdded || shouldNotify;
		}
		if (shouldNotify) {
			m_eventNotifier.NotifyClientOfNewEvents();
		}
	}
}

bool _preprocessEvent(EventData& e) {
	// Change window objIDs to client objIDs for better reporting of objects
	if (e.idObject == 0 && e.idChild == 0) {
		e.idObject = OBJID_CLIENT;
	}
	// Ignore events with invalid window handles
	// TODO: this logic can be cleaned up, e should be const.
	bool isWnd = IsWindow(e.hwnd);
	if (e.hwnd == nullptr || (!isWnd && _in(e.idEvent, VALID_EVENTS_FOR_NON_WINDOWS))) {
		e.hwnd = GetDesktopWindow();
	}
	else if (!isWnd) {
		return false;
	}

	if (e.idChild < 0) {
		auto tempWindow = e.hwnd;
		while (tempWindow
			&& !bool(_getWindowStyle(tempWindow) & WS_POPUP)
			&& _getClassName(tempWindow) == L"MozillaWindowClass"
			) {
			tempWindow = GetAncestor(tempWindow, GA_PARENT);
			if (tempWindow
				&& _startsWith(_getClassName(tempWindow), MOZILLA)
				) {
				e.hwnd = tempWindow;
			}
		}
	}

	auto windowClassName = _getClassName(e.hwnd);
	// Modern IME candidate list windows fire menu events which confuse us
	// and can't be used properly in conjunction with input composition support.
	if (windowClassName == L"Microsoft.IME.UIManager.CandidateWindow.Host"
		&& _in(e.idEvent, MENU_EVENTIDS)
		) {
		return false;
	}

	// At the moment we can't handle show, hide or reorder events on 
	// Mozilla Firefox Location bar,as there are just too many of them
	// Ignore show, hide and reorder on MozillaDropShadowWindowClass windows.
	if (_startsWith(windowClassName, MOZILLA)
		&& _in(e.idEvent, HIDE_SHOW_REORDER)
		&& e.idChild < 0
		) {
		// Mozilla Gecko can sometimes fire win events on a catch - all window 
		// which isn't really the real window
		// Move up the ancestry to find the real mozilla Window and use that
		if (windowClassName == L"MozillaDropShadowWindowClass") {
			return false;
		}
	}

	// We never want to see foreground events for the Program Manager or Shell(task bar)
	if (e.idEvent == EVENT_SYSTEM_FOREGROUND
		&& UNWANTED_FORGROUND_EVENTS.end() != std::find(UNWANTED_FORGROUND_EVENTS.begin(), UNWANTED_FORGROUND_EVENTS.end(), windowClassName)
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


EventBuffer
EventLimiterThread::FlushEventLimiter() {
	m_eventNotifier.ResetNotify();

	if (m_deferredTracker.ShouldDeferEvents()) {
		m_eventNotifier.NotifyClientOfNewEvents();
		return EventBuffer();
	}

	std::unique_lock lock(m_eventLimiterMutex);
	auto&& out = m_eventLimiter.Flush();
	m_maxOutBufferSize = std::max(m_maxOutBufferSize, out.size());
	return out;
}
