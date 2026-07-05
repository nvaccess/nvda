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
#include "eventNotifier.h"

EventNotifier::EventNotifier(std::function<NotifyCB_T> notifyCB)
	: m_notifyCB(notifyCB)
	, m_hasBeenNotified(false)
	, m_hasNotifiedFocus(false)
	// Start valid so the callback fires until Invalidate() is called.
	, m_commsValid(true)
{}

void EventNotifier::NotifyClientOfNewEvents(bool includesFocusEvent) {
	// don't allow the CB to be invalidated while calling.
	std::scoped_lock lock(m_eventCBMutex);
	// #14928: Notify at most once until the client flushes. A focus event still upgrades an
	// already delivered notification once, so the client can upgrade a pending delayed
	// pump to an immediate one.
	bool shouldNotify = !m_hasBeenNotified.exchange(true);
	if (includesFocusEvent && !m_hasNotifiedFocus.exchange(true)) {
		shouldNotify = true;
	}
	if (m_commsValid && m_notifyCB && shouldNotify) {
		m_notifyCB(includesFocusEvent ? 1 : 0);
	}
}

void EventNotifier::ResetNotify() {
	m_hasBeenNotified = false;
	m_hasNotifiedFocus = false;
}

void EventNotifier::Invalidate() {
	std::scoped_lock lock(m_eventCBMutex);
	m_commsValid = false;
}
