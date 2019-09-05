#pragma once
#include "stdafx.h"
#include <functional>
#include "eventData.h"
#include <mutex>
#include <atomic>

using NotifyCB_T = void();
using DestroyEventCB_T = void(EventData*);

class EventNotifier {
public:
	EventNotifier(
		std::function<NotifyCB_T> notifyCB,
		std::function<DestroyEventCB_T> destroyEvntCB
	);

	void NotifyClientOfNewEvents();

	void ResetNotify();

	void NotifyClientOfDestroyEvent(EventData& e);

	void Invalidate();
private:
	std::function<NotifyCB_T> m_notifyCB;
	std::mutex m_eventCBMutex;
	std::function<DestroyEventCB_T> m_destroyEvntCB;
	std::mutex m_destroyEventCBMutex;
	std::atomic<bool> m_hasBeenNotified;
	std::atomic<bool> m_commsValid;
};



