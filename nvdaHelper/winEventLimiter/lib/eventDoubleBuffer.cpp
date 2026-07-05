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
#include "eventDoubleBuffer.h"

#include <utility>

EventDoubleBuffer::EventDoubleBuffer()
	: m_doubleBuffer()
	, m_writeBuffer(&m_doubleBuffer[0])
	, m_readBuffer(&m_doubleBuffer[1])
	, m_swapMutex()
	, m_onWriteCond()
	, m_shouldWaitToSwapBuffers(false)
	, m_lostDestroys(false)
{
	constexpr unsigned int INITIAL_BUFF_SIZE = 200u;
	m_readBuffer->reserve(INITIAL_BUFF_SIZE);
	m_writeBuffer->reserve(INITIAL_BUFF_SIZE);
}

void EventDoubleBuffer::ReleaseBlockingSwap() {
	{ // scope of lock
		// The flag must be cleared while holding m_swapMutex: a waiter that has evaluated
		// its predicate but not yet blocked would otherwise miss this notification and
		// sleep forever (with no further Write to wake it during shutdown).
		std::scoped_lock lock(m_swapMutex);
		m_shouldWaitToSwapBuffers = false;
	} // end lock
	m_onWriteCond.notify_all();
}

void EventDoubleBuffer::MakeSwapBlock() {
	std::scoped_lock lock(m_swapMutex);
	m_shouldWaitToSwapBuffers = true;
}

void EventDoubleBuffer::SwapEventBuffers() {
	m_readBuffer->clear();
	{ // scope of lock
		std::unique_lock lock(m_swapMutex);
		// to prevent churn, only swap if the writeBuffer has items
		const bool waitForEvents = m_shouldWaitToSwapBuffers && m_writeBuffer->empty();
		if (waitForEvents) {
			m_onWriteCond.wait(
				lock,
				[this]() {
					return _isReadyToSwap();
				}
			);
		}
		if (!m_writeBuffer->empty()) {
			std::swap(m_writeBuffer, m_readBuffer);
		}
	} // end lock
}

void EventDoubleBuffer::Write(const EventData & e) {
	{// scope of lock
		std::unique_lock lock(m_swapMutex);
		if (m_writeBuffer->size() >= MAX_BUFFERED_EVENTS) {
			_dropOldestExpendableEvents();
		}
		m_writeBuffer->emplace_back(e); // e invalidated
	} // end lock
	m_onWriteCond.notify_all();
}

// Caller must hold m_swapMutex.
void EventDoubleBuffer::_dropOldestExpendableEvents() {
	// A sustained event flood has left the limiter thread too far behind for old generic
	// events to remain useful. The trim therefore drops generic and raw menu events
	// before focus, foreground, and destroy events. Losing these preferred events could
	// leave NVDA with stale focus or miss a destroy correction.
	// If there are too few expendable events to reach the target size, the trim must also
	// drop preferred events. Otherwise, a flood of preferred events would keep the buffer
	// above the overflow threshold, causing every subsequent write to scan and rebuild an
	// ever-growing buffer without reducing it.
	// Dropped destroy events are recoverable: TakeLostDestroys tells the client to treat
	// every window as potentially destroyed.
	const auto target = MAX_BUFFERED_EVENTS / 2;
	const auto toDrop = m_writeBuffer->size() - target;
	auto dropBudget = eventBufferLimits::CalculateDropBudget(
		m_writeBuffer->cbegin(),
		m_writeBuffer->cend(),
		toDrop,
		[this](const EventData& e) { return !_isProtectedFromOverflow(e); }
	);
	EventBuffer kept;
	kept.reserve(target);
	for (const auto& e : *m_writeBuffer) {
		if (dropBudget.ShouldDrop(!_isProtectedFromOverflow(e))) {
			if (e.idEvent == EVENT_OBJECT_DESTROY) {
				m_lostDestroys = true;
			}
			continue;
		}
		kept.push_back(e);
	}
	*m_writeBuffer = std::move(kept);
}

bool EventDoubleBuffer::TakeLostDestroys() {
	std::scoped_lock lock(m_swapMutex);
	return std::exchange(m_lostDestroys, false);
}

EventBuffer & EventDoubleBuffer::Read() {
	return *m_readBuffer;
}

void EventDoubleBuffer::SetAlwaysAllowedObject(HWND hwnd, LONG idObject, LONG idChild) {
	std::scoped_lock lock(m_swapMutex);
	if (hwnd == nullptr && idObject == 0 && idChild == 0) {
		m_alwaysAllowedObject.reset();
		return;
	}
	m_alwaysAllowedObject = AlwaysAllowedObject{ hwnd, idObject, idChild };
}

bool EventDoubleBuffer::_isProtectedFromOverflow(const EventData& e) const {
	// #2695: Focus and foreground events feed the limiter's focus cache (which, like the Python
	// limiter, never silently drops them), and destroy events are diverted for NVDA's
	// cache eviction and focus correction. The overflow trim prefers consuming generic
	// events so these survive to reach those protections. Raw menu events remain
	// expendable because the limiter coalesces them later; protecting the entire raw
	// flood could otherwise displace a focus event before it reaches the limiter.
	if (e.idEvent == EVENT_OBJECT_FOCUS
		|| e.idEvent == EVENT_SYSTEM_FOREGROUND
		|| e.idEvent == EVENT_OBJECT_DESTROY
	) {
		return true;
	}
	// #11520: events for the always allowed (focused) object must survive too, or they
	// would be lost before WinEventLimiter's exemption could see them.
	if (!m_alwaysAllowedObject.has_value()) {
		return false;
	}
	const auto& allowed = m_alwaysAllowedObject.value();
	// Events here are raw; apply the same objectID remap the limiter thread's
	// preprocessing will (window objectIDs become OBJID_CLIENT), so this comparison
	// matches what WinEventLimiter::_matchesAlwaysAllowed would later see.
	const LONG idObject = (e.idObject == 0 && e.idChild == 0) ? OBJID_CLIENT : e.idObject;
	return e.hwnd == allowed.hwnd
		&& idObject == allowed.idObject
		&& e.idChild == allowed.idChild;
}

bool EventDoubleBuffer::_isReadyToSwap() {
	const auto hasEvents = false == m_writeBuffer->empty();
	return hasEvents
		|| false == m_shouldWaitToSwapBuffers;
}
