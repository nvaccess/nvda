#include "stdafx.h"

#include <set>
#include "winEventLimiter.h"
#include "utils.h"
#include "internalConstants.h"

const int WinEventLimiter::MAX_EVENTS_FOR_THREAD = 10;
const int WinEventLimiter::MAX_FOCUS_EVENTS = 4;

struct cachedEvent {
	EventData event;
	bool valid;
};

WinEventLimiter::WinEventLimiter()
	: m_events()
	, m_focusEventIndices()
	, m_lastMenuEvent()
	, m_threadEventIndexes()
	, m_validEventCount(0)
	, m_maxBufferSize(0)
{
}

WinEventLimiter::~WinEventLimiter() {
}

bool WinEventLimiter::_preFilter(const EventData& e) {
	if (e.idEvent == EVENT_OBJECT_FOCUS
		&& _in(e.idObject, MENU_OBJECTS) && e.idChild == 0) {
		// This is a focus event on a menu bar itself, which is just silly.Ignore it.
		return false;
	}
	const auto itr = std::find_if(
		m_events.begin(), m_events.end(),
		[&e](const cachedEvent& existing) {
			// This does not compare the time of the event,
			// multiple events at different times only adds more unncessary work for NVDA
			return existing.valid && existing.event == e;
	});
	if(itr != m_events.end()){
		return false;
	}
	return true;
}

void WinEventLimiter::_addFocusEvent(VecSize_t index) {
	m_focusEventIndices.push_back(index);
	const auto numFocusEvents = m_focusEventIndices.size();
	if (numFocusEvents > MAX_FOCUS_EVENTS) {
		const auto oldestFocusEventIndex = m_focusEventIndices.front();
		auto& oldestFocusEvent = m_events[oldestFocusEventIndex];
		_invalidateCachedEvent(oldestFocusEvent);
		m_focusEventIndices.erase(m_focusEventIndices.begin());
	}
}

void WinEventLimiter::_invalidateAnyMatchingFocusEvent(const EventData& e) {
	// use erase remove idiom, piggy back and invalidate cached events.
	auto& indices = m_focusEventIndices;
	const auto removeItr = std::remove_if(
		indices.begin(), indices.end(), [&e, this](auto index) {
			auto& existing = m_events[index];
			if (existing.event == e) {
				_invalidateCachedEvent(existing);
				return true;
			}
			return false;
		});
	m_focusEventIndices.erase(removeItr, indices.end());
}

void WinEventLimiter::_invalidateCachedEvent(cachedEvent & e) {
	if (e.valid) {
		e.valid = false;
		--m_validEventCount;
	}
}

bool WinEventLimiter::AddEvent(EventData& e) {
	if (!_preFilter(e)) {
		return false;
	}
	const auto index = m_events.size();
	m_events.push_back(cachedEvent({ e, true }));
	++m_validEventCount;

	auto& eventsForThread = m_threadEventIndexes[e.dwEventThread];
	eventsForThread.push_back(index);
	if (eventsForThread.size() > MAX_EVENTS_FOR_THREAD) {
		auto indexOfOldestEventForThread = eventsForThread.front();
		eventsForThread.erase(eventsForThread.begin());
		auto& oldestEventForThread = m_events[indexOfOldestEventForThread];
		_invalidateCachedEvent(oldestEventForThread);
	}

	if (e.idEvent == EVENT_OBJECT_FOCUS) {
		_addFocusEvent(index);
		return true;
	}
	else if (e.idEvent == EVENT_SYSTEM_FOREGROUND) {
		EventData equivFocusEvent = e;
		equivFocusEvent.idEvent = EVENT_OBJECT_FOCUS;
		_invalidateAnyMatchingFocusEvent(equivFocusEvent);
		_addFocusEvent(index);
	}
	else if (e.idEvent == EVENT_OBJECT_SHOW) {
		EventData equivHideEvent = e;
		equivHideEvent.idEvent = EVENT_OBJECT_HIDE;
		for(auto& existing : m_events) {
			if (existing.event == e) {
				_invalidateCachedEvent(existing);
			}
		}
	}
	else if (e.idEvent == EVENT_OBJECT_HIDE) {
		EventData equivHideEvent = e;
		equivHideEvent.idEvent = EVENT_OBJECT_SHOW;
		for (auto& existing : m_events) {
			if (existing.event == e) {
				_invalidateCachedEvent(existing);
			}
		}
	}
	else if (_in(e.idEvent, MENU_EVENTIDS)) {
		if (m_lastMenuEvent.has_value()) {
			auto& existing = m_events[m_lastMenuEvent.value()];
			_invalidateCachedEvent(existing);
		}
		m_lastMenuEvent = index;
	}
	return true;
}

void WinEventLimiter::_reset() {
	m_maxBufferSize = std::max(m_maxBufferSize, m_events.size());
	m_lastMenuEvent.reset();
	m_events.clear();
	m_focusEventIndices.clear();
	m_threadEventIndexes.clear();
	m_validEventCount = 0;
}

EventBuffer WinEventLimiter::Flush() {
	EventBuffer ret;
	ret.reserve(m_validEventCount);

	for (auto& e : m_events) {
		if (e.valid) {
			ret.push_back(e.event);
		}
	}
	_reset();
	return ret;
}

VecSize_t WinEventLimiter::GetMaxBufferSize()
{
	return m_maxBufferSize;
}

