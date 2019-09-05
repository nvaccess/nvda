#include "stdafx.h"
#include "deferredForegroundWindowHandler.h"

void DeferredForegourndWindowEventHandler::Track(EventData & e) {
	if (e.idEvent == EVENT_SYSTEM_FOREGROUND) {
		// #3831: Event handling can be deferred if Windows takes a while to change the foreground window.
		// See pumpAll for details.
		std::scoped_lock lock(m_deferMutex);
		m_deferUntilForegroundWindow = { e.hwnd, 0 };
	}
}

bool DeferredForegourndWindowEventHandler::ShouldDeferEvents()
{
	std::scoped_lock lock(m_deferMutex);
	auto& deferForHwnd = m_deferUntilForegroundWindow;
	if (deferForHwnd.has_value()) {
		// #3831: Sometimes, a foreground event is fired,
		// but GetForegroundWindow() takes a short while to return this new foreground.
		const bool canDeferAgain = deferForHwnd->deferCount < MAX_FOREGROUND_DEFERS;
		const bool isWindowInForeground = GetForegroundWindow() == deferForHwnd->hwnd;

		if (canDeferAgain && !isWindowInForeground) {
			++deferForHwnd->deferCount;
			return true;
		}
		else {
			// Either the foreground window is now correct
			// or we've already had the maximum number of defers.
			// (Sometimes, foreground events are fired even when the foreground hasn't actually changed.)
			deferForHwnd.reset();
			return false;
		}
	}
	return false;
}
