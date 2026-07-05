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

#include <algorithm>
#include <limits>
#include <set>
#include "winEventLimiter.h"
#include "utils.h"
#include "internalConstants.h"

// Flood protection: only the newest MAX_EVENTS_FOR_THREAD generic winEvents per source
// thread survive a flush.
// Complex web documents (e.g. Google applications in Firefox) and
// applications starting up can flood NVDA with far more show/hide/nameChange winEvents
// than it could ever usefully process, freezing NVDA for many seconds.
// Focus and foreground events, and the surviving menu event, are not counted.
const int WinEventLimiter::MAX_EVENTS_FOR_THREAD = 10;
// The number of focus changed events allowed to be queued; if more are added then the
// oldest focus event is removed to make space.
const int WinEventLimiter::MAX_FOCUS_ITEMS = 4;
struct cachedEvent {
	EventData event;
	bool valid;
};

WinEventLimiter::WinEventLimiter()
	: m_events()
	, m_liveEventIndices()
	, m_focusEventIndices()
	, m_lastMenuEvent()
	, m_validEventCount(0)
	, m_maxBufferSize(0)
{
}

WinEventLimiter::~WinEventLimiter() {
}

bool WinEventLimiter::_preFilter(const EventData& e) {
	const bool isMenuObject = std::find(
		MENU_OBJECTS.cbegin(), MENU_OBJECTS.cend(), e.idObject
	) != MENU_OBJECTS.cend();
	if (e.idEvent == EVENT_OBJECT_FOCUS
		&& isMenuObject && e.idChild == 0) {
		// This is a focus event on a menu bar itself, which is just silly. Ignore it.
		return false;
	}
	return true;
}

void WinEventLimiter::_invalidateMatching(const EventData& e) {
	// At most one valid entry can match: duplicates are invalidated when added.
	const auto itr = m_liveEventIndices.find(e);
	if (itr != m_liveEventIndices.end()) {
		_invalidateEventAt(itr->second);
	}
}

void WinEventLimiter::_addFocusEvent(VecSize_t index) {
	m_focusEventIndices.push_back(index);
	const auto numFocusEvents = m_focusEventIndices.size();
	if (numFocusEvents > MAX_FOCUS_ITEMS) {
		const auto oldestFocusEventIndex = m_focusEventIndices.front();
		if (m_events[oldestFocusEventIndex].event.idEvent == EVENT_SYSTEM_FOREGROUND) {
			// Like the Python limiter, where a foreground event lives in both the focus and
			// generic caches, eviction from the focus cache demotes it to a generic event
			// (now subject to the per thread limit) rather than dropping it: an application
			// switch must still be announced after a burst of rejected focus events.
			m_focusEventIndices.erase(m_focusEventIndices.begin());
		}
		else {
			// Also erases the index from m_focusEventIndices.
			_invalidateEventAt(oldestFocusEventIndex);
		}
	}
}

void WinEventLimiter::_invalidateEventAt(VecSize_t index, bool keepIdentity) {
	auto& cached = m_events[index];
	if (!cached.valid) {
		return;
	}
	cached.valid = false;
	--m_validEventCount;
	if (!keepIdentity) {
		m_liveEventIndices.erase(cached.event);
	}
	// Keep focus and menu in sync, so stale entries can never consume the
	// MAX_FOCUS_ITEMS budget (evicting still valid focus events) or exempt a dead index
	// from the per thread limit.
	const auto focusItr = std::find(
		m_focusEventIndices.begin(), m_focusEventIndices.end(), index
	);
	if (focusItr != m_focusEventIndices.end()) {
		m_focusEventIndices.erase(focusItr);
	}
	if (m_lastMenuEvent == index) {
		m_lastMenuEvent.reset();
	}
}

void WinEventLimiter::_invalidateEquivEvent(const EventData& e, const DWORD eventID){
	EventData equivEvent = e;
	equivEvent.idEvent = eventID;
	_invalidateMatching(equivEvent);
}

bool WinEventLimiter::AddEvent(EventData& e) {
	if (!_preFilter(e)) {
		return false;
	}
	// Only one event per specific object is kept at a time, though a duplicate pushes it
	// further forward in time (the old copy is dropped and the new one appended).
	// Equality does not compare the time of the event; multiple events for the same object
	// at different times would only add more unnecessary work for NVDA.
	const auto index = m_events.size();
	m_events.push_back(cachedEvent({ e, true }));
	++m_validEventCount;
	// try_emplace resolves fresh and duplicate identities with one hash of the key,
	// where find + erase + insert would hash it three times per duplicate.
	const auto [itr, inserted] = m_liveEventIndices.try_emplace(e, index);
	if (!inserted) {
		_invalidateEventAt(itr->second, true /*keepIdentity*/);
		itr->second = index;
	}

	switch (e.idEvent) {
	case EVENT_OBJECT_FOCUS:
		_addFocusEvent(index);
		break;
	case EVENT_SYSTEM_FOREGROUND:
		// An equivalent queued focus event is superseded by this foreground event.
		_invalidateEquivEvent(e, EVENT_OBJECT_FOCUS);
		_addFocusEvent(index);
		break;
	case EVENT_OBJECT_SHOW: _invalidateEquivEvent(e, EVENT_OBJECT_HIDE);
		break;
	case EVENT_OBJECT_HIDE: _invalidateEquivEvent(e, EVENT_OBJECT_SHOW);
		break;
	default:
		const bool isMenuEvent = std::find(
			MENU_EVENTIDS.cbegin(), MENU_EVENTIDS.cend(), e.idEvent
		) != MENU_EVENTIDS.cend();
		if (isMenuEvent) {
			if (m_lastMenuEvent.has_value()) {
				// Also resets m_lastMenuEvent.
				_invalidateEventAt(m_lastMenuEvent.value());
			}
			m_lastMenuEvent = index;
		}
	}
	if (m_events.size() >= MAX_BUFFERED_EVENTS) {
		_compact();
	}
	return true;
}

void WinEventLimiter::SetAlwaysAllowedObject(HWND hwnd, LONG idObject, LONG idChild) {
	if (hwnd == nullptr && idObject == 0 && idChild == 0) {
		m_alwaysAllowedObject.reset();
		return;
	}
	m_alwaysAllowedObject = AlwaysAllowedObject{ hwnd, idObject, idChild };
}

bool WinEventLimiter::_matchesAlwaysAllowed(const EventData& e) const {
	if (!m_alwaysAllowedObject.has_value()) {
		return false;
	}
	const auto& allowed = m_alwaysAllowedObject.value();
	// Like the Python limiter, the event ID and thread are deliberately not compared:
	// any kind of event for the allowed object is exempt, whichever thread raised it.
	return e.hwnd == allowed.hwnd
		&& e.idObject == allowed.idObject
		&& e.idChild == allowed.idChild;
}

void WinEventLimiter::_compact() {
	// Shrink the buffer to at most half of MAX_BUFFERED_EVENTS. Invalidated entries (mostly
	// superseded duplicates) are removed first; only if the buffer is still too large are
	// the oldest valid events dropped, generic ones first. Focus class events and the
	// surviving menu event are never dropped (their own limits bound them). Events for the
	// always allowed (focused) object are preferred survivors (#11520), but only while the
	// generic events can cover the excess: deduplication keeps one entry per distinct
	// event ID and thread, so the focused object alone can overflow the cap, and the cap
	// must stay absolute or the buffer would grow without bound while recompacting on
	// every add.
	m_maxBufferSize = std::max(m_maxBufferSize, m_events.size());
	const auto keepCount = MAX_BUFFERED_EVENTS / 2;
	const auto totalToDrop = m_validEventCount > keepCount ? m_validEventCount - keepCount : 0;
	eventBufferLimits::EventDropBudget dropBudget = eventBufferLimits::CalculateDropBudget(
		m_events.cbegin(),
		m_events.cend(),
		totalToDrop,
		[this](const cachedEvent& cached) {
			if (!cached.valid || _matchesAlwaysAllowed(cached.event)) {
				return false;
			}
			const VecSize_t index = static_cast<VecSize_t>(&cached - m_events.data());
			return !_isExemptFromThreadLimit(index);
		}
	);
	std::vector<cachedEvent> keptEvents;
	keptEvents.reserve(std::min(m_validEventCount, keepCount));
	constexpr auto DROPPED = std::numeric_limits<VecSize_t>::max();
	std::vector<VecSize_t> indexRemap(m_events.size(), DROPPED);
	for (VecSize_t index = 0; index < m_events.size(); ++index) {
		const auto& cached = m_events[index];
		if (!cached.valid) {
			continue;
		}
		if (!_isExemptFromThreadLimit(index)
			&& dropBudget.ShouldDrop(!_matchesAlwaysAllowed(cached.event))
		) {
			continue;
		}
		indexRemap[index] = keptEvents.size();
		keptEvents.push_back(cached);
	}
	m_events = std::move(keptEvents);
	m_liveEventIndices.clear();
	for (VecSize_t index = 0; index < m_events.size(); ++index) {
		m_liveEventIndices[m_events[index].event] = index;
	}
	std::vector<VecSize_t> rebasedFocusIndices;
	rebasedFocusIndices.reserve(m_focusEventIndices.size());
	for (const auto index : m_focusEventIndices) {
		if (indexRemap[index] != DROPPED) {
			rebasedFocusIndices.push_back(indexRemap[index]);
		}
	}
	m_focusEventIndices = std::move(rebasedFocusIndices);
	if (m_lastMenuEvent.has_value()) {
		const auto remapped = indexRemap[m_lastMenuEvent.value()];
		if (remapped != DROPPED) {
			m_lastMenuEvent = remapped;
		}
		else {
			m_lastMenuEvent.reset();
		}
	}
	// The compaction loop omitted every invalid entry.
	m_validEventCount = m_events.size();
}

void WinEventLimiter::_reset() {
	m_maxBufferSize = std::max(m_maxBufferSize, m_events.size());
	m_lastMenuEvent.reset();
	m_events.clear();
	m_liveEventIndices.clear();
	m_focusEventIndices.clear();
	m_validEventCount = 0;
}

bool WinEventLimiter::_isExemptFromThreadLimit(VecSize_t index) const {
	// Focus class events and the surviving menu event are limited by their own
	// mechanisms (MAX_FOCUS_ITEMS and m_lastMenuEvent) and are never counted
	// towards the per-thread limit.
	if (m_lastMenuEvent.has_value() && m_lastMenuEvent.value() == index) {
		return true;
	}
	return std::find(
		m_focusEventIndices.cbegin(), m_focusEventIndices.cend(), index
	) != m_focusEventIndices.cend();
}

void WinEventLimiter::_applyThreadLimit() {
	// Walk newest to oldest, keeping only the newest MAX_EVENTS_FOR_THREAD generic
	// events per source thread.
	std::map<DWORD, int> perThreadCounts;
	for (auto index = m_events.size(); index-- > 0; ) {
		auto& cached = m_events[index];
		if (!cached.valid || _isExemptFromThreadLimit(index)) {
			continue;
		}
		auto& count = perThreadCounts[cached.event.dwEventThread];
		++count;
		if (count > MAX_EVENTS_FOR_THREAD && !_matchesAlwaysAllowed(cached.event)) {
			// #11520: events for the always allowed (focused) object are never
			// dropped by the per thread limit.
			_invalidateEventAt(index);
		}
	}
}

EventBuffer WinEventLimiter::Flush() {
	_applyThreadLimit();
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
