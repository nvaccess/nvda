#include "stdafx.h"
#include "eventNotifier.h"

EventNotifier::EventNotifier(std::function<NotifyCB_T> notifyCB, std::function<DestroyEventCB_T> destroyEvntCB)
	: m_notifyCB(notifyCB)
	, m_destroyEvntCB(destroyEvntCB)
	, m_hasBeenNotified(false)
{}

void EventNotifier::NotifyClientOfNewEvents() {
	// don't allow the CB to be invalidated while calling.
	std::scoped_lock lock(m_eventCBMutex);
	auto isAlreadyNotified = m_hasBeenNotified.exchange(true);
	if (m_commsValid && m_notifyCB && !isAlreadyNotified) {
		m_notifyCB();
	}
}

void EventNotifier::ResetNotify() {
	m_hasBeenNotified = false;
}

void EventNotifier::NotifyClientOfDestroyEvent(EventData & e) {
	// only one call to notify at a time
	// we also don't want the callback to be invalidated while calling.
	std::scoped_lock lock(m_destroyEventCBMutex);
	if (m_commsValid && m_destroyEvntCB) {
		m_destroyEvntCB(&e);
	}
}

void EventNotifier::Invalidate() {
	std::scoped_lock lock(m_destroyEventCBMutex, m_eventCBMutex);
	m_commsValid = false;
}
