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
#include "eventBufferLimits.h"
#include "eventData.h"
#include <map>
#include <optional>
#include <unordered_map>

struct cachedEvent;
using VecSize_t = std::vector<cachedEvent>::size_type;

class WinEventLimiter
{
public:
	WinEventLimiter();
	bool AddEvent(EventData& e);
	EventBuffer Flush();
	// #11520: Exempts events for the given object from the per thread limit;
	// All zeros clears the exemption.
	void SetAlwaysAllowedObject(HWND hwnd, LONG idObject, LONG idChild);
	VecSize_t GetMaxBufferSize(); // Used for diagnostics

	~WinEventLimiter();

	static const int MAX_FOCUS_ITEMS;
	static const int MAX_EVENTS_FOR_THREAD;
	static constexpr VecSize_t MAX_BUFFERED_EVENTS =
		eventBufferLimits::MAX_BUFFERED_EVENTS;

private:
	std::vector<cachedEvent> m_events;
	// The index in m_events of the single valid entry for each event identity, giving constant-time
	// duplicate and equivalent-event invalidation.
	std::unordered_map<EventData, VecSize_t, EventDataHasher> m_liveEventIndices;
	std::vector<VecSize_t> m_focusEventIndices;
	std::optional<VecSize_t> m_lastMenuEvent;
	std::optional<AlwaysAllowedObject> m_alwaysAllowedObject;
	EventBuffer::size_type m_validEventCount;
	VecSize_t m_maxBufferSize;

	void _addFocusEvent(VecSize_t index);
	// keepIdentity skips the m_liveEventIndices erase; the caller repoints the entry.
	void _invalidateEventAt(VecSize_t index, bool keepIdentity = false);
	void _invalidateMatching(const EventData & e);
	void _invalidateEquivEvent(const EventData & e, const DWORD eventID);
	void _applyThreadLimit();
	bool _isExemptFromThreadLimit(VecSize_t index) const;
	bool _matchesAlwaysAllowed(const EventData & e) const;
	void _compact();
	void _reset();
	bool _preFilter(const EventData & e);
};
