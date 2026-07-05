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
#include <optional>
#include "eventData.h"

// #3831: After a foreground winEvent is fired, GetForegroundWindow() can take a short
// while to actually return the new foreground window. Defer flushing events for up to
// this many pumps until the OS agrees the tracked window is in the foreground, giving it
// time to update. (Sometimes foreground events fire when the foreground never changes,
// hence the cap.) Mirrors internalWinEventHandler._shouldGetEvents in NVDA's in-process
// implementation.
constexpr unsigned int MAX_FOREGROUND_DEFERS = 2;

// Not internally synchronized: both callers already hold EventLimiterThread's
// m_eventLimiterMutex, which #3831 requires anyway (Track must be atomic with the
// defer check).
class DeferredForegroundWindowEventHandler {

public:
	struct DeferUntilHwndForeground {
		HWND hwnd;
		unsigned int deferCount;
	};

	void Track(EventData& e);

	bool ShouldDeferEvents();

private:
	std::optional<DeferUntilHwndForeground> m_deferUntilForegroundWindow;
};
