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
#include "deferredForegroundWindowHandler.h"

void DeferredForegroundWindowEventHandler::Track(EventData & e) {
	if (e.idEvent == EVENT_SYSTEM_FOREGROUND) {
		// #3831: Event handling can be deferred if Windows takes a while to change the foreground window.
		// See pumpAll for details.
		m_deferUntilForegroundWindow = { e.hwnd, 0 };
	}
}

bool DeferredForegroundWindowEventHandler::ShouldDeferEvents()
{
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
