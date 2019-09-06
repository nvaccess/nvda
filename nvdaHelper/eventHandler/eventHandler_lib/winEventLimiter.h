#pragma once
#include "stdafx.h"
#include "eventData.h"
#include <map>
#include <optional>

struct cachedEvent;
using VecSize_t = std::vector<cachedEvent>::size_type;

class WinEventLimiter
{
public:
	WinEventLimiter();
	bool AddEvent(EventData& e);
	EventBuffer Flush();
	VecSize_t GetMaxBufferSize(); // Used for diagnostics
	
	~WinEventLimiter();

	static const int MAX_FOCUS_EVENTS;
	static const int MAX_EVENTS_FOR_THREAD;

private:
	std::vector<cachedEvent> m_events;
	std::vector<VecSize_t> m_focusEventIndices;
	std::optional<VecSize_t> m_lastMenuEvent;
	std::map<DWORD, std::vector<VecSize_t>> m_threadEventIndexes;
	EventBuffer::size_type m_validEventCount;
	VecSize_t m_maxBufferSize;
	
	void _addFocusEvent(VecSize_t index);
	void _invalidateAnyMatchingFocusEvent(const EventData & e);
	void _invalidateCachedEvent(cachedEvent & e);
	void _invalidateEquivEvent(const EventData & e, const DWORD eventID);
	void _reset();
	bool _preFilter(const EventData & e);
};

