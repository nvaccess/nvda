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
#include <array>
#include <condition_variable>
#include <mutex>
#include <optional>
#include "eventBufferLimits.h"
#include "eventData.h"

class WriteBuffer {
public:
	virtual ~WriteBuffer() {}
	virtual void Write(const EventData& e) = 0;
};

class EventDoubleBuffer : public WriteBuffer {
public:
	EventDoubleBuffer();

	void ReleaseBlockingSwap();

	void MakeSwapBlock();

	void SwapEventBuffers();

	void Write(const EventData& e) override;

	EventBuffer& Read();

	// #11520: The focused object, whose events the overflow trim prefers to keep;
	// all zeros clears it. Thread safe.
	void SetAlwaysAllowedObject(HWND hwnd, LONG idObject, LONG idChild);

	// Whether the overflow trim has discarded any destroy events since the last call;
	// reading clears the flag. The client must then treat every window as potentially
	// destroyed, since cache eviction can no longer rely on per window destroy events.
	// Thread safe.
	bool TakeLostDestroys();

	// WinEvents can arrive faster than the limiter thread drains them; the write buffer
	// must not grow without bound (the in-process implementation was implicitly bounded
	// by the OS limit on the hooking thread's message queue). On reaching this size, the
	// buffer is shrunk to half, discarding the oldest generic and raw menu events first;
	// focus, foreground, destroy, and focused-object events are only dropped when the
	// expendable events cannot cover the excess (destroy loss is then reported via
	// TakeLostDestroys).
	static constexpr EventBuffer::size_type MAX_BUFFERED_EVENTS =
		eventBufferLimits::MAX_BUFFERED_EVENTS;

private:
	std::array<EventBuffer, 2> m_doubleBuffer;
	EventBuffer* m_writeBuffer;
	EventBuffer* m_readBuffer;
	std::mutex m_swapMutex;
	std::condition_variable_any m_onWriteCond;
	// Guarded by m_swapMutex (see ReleaseBlockingSwap for why a bare atomic is not enough).
	bool m_shouldWaitToSwapBuffers;
	// Guarded by m_swapMutex.
	bool m_lostDestroys;
	// Guarded by m_swapMutex.
	std::optional<AlwaysAllowedObject> m_alwaysAllowedObject;

	bool _isReadyToSwap();

	// Shrinks the write buffer to half of MAX_BUFFERED_EVENTS, oldest and generic events
	// first. Caller must hold m_swapMutex.
	void _dropOldestExpendableEvents();

	// Whether the trim must prefer keeping this event. Caller must hold m_swapMutex.
	bool _isProtectedFromOverflow(const EventData& e) const;
};
