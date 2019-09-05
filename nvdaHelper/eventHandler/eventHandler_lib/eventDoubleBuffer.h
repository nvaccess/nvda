#pragma once
#include "stdafx.h"
#include <functional>
#include <thread>
#include <atomic>
#include <mutex>
#include <future>
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

private:
	std::vector<EventBuffer> m_doubleBuffer;
	EventBuffer* m_writeBuffer;
	EventBuffer* m_readBuffer;
	std::mutex m_swapMutex;
	std::condition_variable_any m_onWriteCond;
	using size_t = std::vector<EventBuffer>::size_type;
	size_t m_maxReadBufferSize;
	std::atomic<bool> m_shouldWaitToSwapBuffers;

	bool _isReadyToSwap();
};
