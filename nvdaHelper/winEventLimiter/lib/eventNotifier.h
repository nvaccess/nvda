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
#include <functional>
#include <mutex>
#include <atomic>

// #14928: The int argument is non-zero when the new events include a focus event,
// so the client can pump immediately rather than after a delay.
using NotifyCB_T = void(int);

class EventNotifier {
public:
	EventNotifier(std::function<NotifyCB_T> notifyCB);

	void NotifyClientOfNewEvents(bool includesFocusEvent);

	void ResetNotify();

	void Invalidate();
private:
	std::function<NotifyCB_T> m_notifyCB;
	std::mutex m_eventCBMutex;
	std::atomic<bool> m_hasBeenNotified;
	std::atomic<bool> m_hasNotifiedFocus;
	bool m_commsValid;
};
