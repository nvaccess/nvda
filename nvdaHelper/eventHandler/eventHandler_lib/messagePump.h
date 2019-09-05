#pragma once
#include "stdafx.h"
#include <thread>
#include <atomic>
#include <future>

#include "eventData.h"

class EventNotifier;
class WriteBuffer;

class MessagePumpThread {
public:
	static std::shared_ptr<MessagePumpThread>
		GetInstance(EventNotifier& eventNotifier, WriteBuffer& buffer);

	int Start();

	int Stop();
private:
	// static vars
	static std::shared_ptr<MessagePumpThread> s_instance;
	static HWINEVENTHOOK s_winEventHook;
	static void CALLBACK _sHandleWinEvent(
		HWINEVENTHOOK hook, DWORD idEvent, HWND hwnd,
		LONG idObject, LONG idChild,
		DWORD dwEventThread, DWORD dwmsEventTime
	);

	// member vars
	std::atomic<bool> m_shouldContinuePump;
	EventNotifier& m_eventNotifier;
	WriteBuffer& m_buffer;
	std::thread m_thread;
	bool m_cooinit;

	MessagePumpThread(
		EventNotifier& eventNotifier,
		WriteBuffer& doubleBuffer
	);

	int _start();

	void _initialise(std::promise<int> initResult);

	// Initializes COM and sets up the idEvent hook.
	int _initializeMSAA();

	void _doBlockingMessagePump();

	void _handleWinEvent(EventData& e);

	int _stop();

	// Unhooks the idEvent and shuts down COM.
	int _shutdownMSAA();
};
