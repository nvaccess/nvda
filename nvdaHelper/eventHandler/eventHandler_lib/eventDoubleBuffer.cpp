#include "stdafx.h"
#include "eventDoubleBuffer.h"

EventDoubleBuffer::EventDoubleBuffer()
	: m_doubleBuffer(2)
	, m_writeBuffer(&m_doubleBuffer[0])
	, m_readBuffer(&m_doubleBuffer[1])
	, m_swapMutex()
	, m_onWriteCond()
	, m_maxReadBufferSize(0u)
	, m_shouldWaitToSwapBuffers(false)
{
	constexpr unsigned int INITIAL_BUFF_SIZE = 200u;
	m_readBuffer->reserve(INITIAL_BUFF_SIZE);
	m_writeBuffer->reserve(INITIAL_BUFF_SIZE);
}

void EventDoubleBuffer::ReleaseBlockingSwap() {
	m_shouldWaitToSwapBuffers = false;
	m_onWriteCond.notify_all();
}

void EventDoubleBuffer::MakeSwapBlock() {
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
			m_maxReadBufferSize = std::max(m_maxReadBufferSize, m_readBuffer->size());
		}
	} // end lock
}

void EventDoubleBuffer::Write(const EventData & e) {
	{// scope of lock
		std::unique_lock lock(m_swapMutex);
		m_writeBuffer->emplace_back(e); // e invalidated
	} // end lock
	m_onWriteCond.notify_all();
}

EventBuffer & EventDoubleBuffer::Read() {
	return *m_readBuffer;
}

bool EventDoubleBuffer::_isReadyToSwap() {
	const auto hasEvents = false == m_writeBuffer->empty();
	return hasEvents
		|| false == m_shouldWaitToSwapBuffers;
}
