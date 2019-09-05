#pragma once
#include "stdafx.h"
#include <thread>
#include <atomic>
#include <mutex>
#include "winEventLimiter.h"
#include "deferredForegroundWindowHandler.h"

class EventNotifier;
class EventDoubleBuffer;

class EventLimiterThread
{
public:
	EventLimiterThread(EventNotifier& eventNotifier, EventDoubleBuffer& buffer);
	~EventLimiterThread();

	void Stop();

	// Prepares m_out for fetching events from NVDA
	EventBuffer FlushEventLimiter();
private:
	EventDoubleBuffer& m_in;
	EventNotifier& m_eventNotifier;
	DeferredForegourndWindowEventHandler m_deferredTracker;
	WinEventLimiter m_eventLimiter;
	std::mutex m_eventLimiterMutex;
	std::atomic<bool> m_continue;
	std::thread m_thread;
	using size_t = EventBuffer::size_type;
	size_t m_maxOutBufferSize = 0;

	// Main thread loop
	// - Swaps the read/write buffers in EventDoubleBuffer
	// - Takes events from the read buffer feeding to the WinEventLimiter
	void _pushThroughEventLimiter();
};

