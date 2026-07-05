/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2026 Bill Dengler
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

#include <algorithm>

#include "eventData.h"

namespace eventBufferLimits {

// All queues use the same bound so an event flood has a consistent retention policy
// at every stage of the external limiter pipeline.
inline constexpr EventBuffer::size_type MAX_BUFFERED_EVENTS = 2000;

class EventDropBudget {
public:
	EventDropBudget(
		EventBuffer::size_type expendableEvents,
		EventBuffer::size_type preferredEvents
	)
		: m_expendableEvents(expendableEvents)
		, m_preferredEvents(preferredEvents)
	{
	}

	bool ShouldDrop(bool isExpendable) {
		EventBuffer::size_type& budget = isExpendable
			? m_expendableEvents
			: m_preferredEvents;
		if (budget == 0) {
			return false;
		}
		--budget;
		return true;
	}

private:
	EventBuffer::size_type m_expendableEvents;
	EventBuffer::size_type m_preferredEvents;
};

template<typename Iterator, typename IsExpendable>
EventDropBudget CalculateDropBudget(
	Iterator first,
	Iterator last,
	EventBuffer::size_type eventsToDrop,
	IsExpendable isExpendable
) {
	const EventBuffer::size_type expendableCount = static_cast<EventBuffer::size_type>(
		std::count_if(first, last, isExpendable)
	);
	const EventBuffer::size_type expendableToDrop = std::min(
		expendableCount,
		eventsToDrop
	);
	return EventDropBudget(
		expendableToDrop,
		eventsToDrop - expendableToDrop
	);
}

}  // namespace eventBufferLimits
