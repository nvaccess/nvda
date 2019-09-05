#include "stdafx.h"
#include "messagePump.h"

#include "eventDoubleBuffer.h"
#include "eventNotifier.h"
#include "utils.h"
#include "internalConstants.h"


HWINEVENTHOOK MessagePumpThread::s_winEventHook = nullptr;
std::shared_ptr<MessagePumpThread> MessagePumpThread::s_instance;


std::shared_ptr<MessagePumpThread>
MessagePumpThread::GetInstance(EventNotifier & eventNotifier, WriteBuffer & buffer) {
	if (!s_instance) {
		s_instance = std::shared_ptr<MessagePumpThread>(new MessagePumpThread(eventNotifier, buffer));
	}
	return s_instance;
}

MessagePumpThread::MessagePumpThread(
	EventNotifier& eventNotifier,
	WriteBuffer& doubleBuffer
)
	: m_shouldContinuePump(false)
	, m_eventNotifier(eventNotifier)
	, m_buffer(doubleBuffer)
	, m_thread()
	, m_cooinit(false)
{ }

inline int MessagePumpThread::_start() {
	// Not in thread
	std::promise<int> resultPromise;
	std::future<int> futureResult = resultPromise.get_future();
	m_thread = std::thread(
		[this, &resultPromise]() {
			_initialise(std::move(resultPromise)); // resultPromise no longer valid after here.
			_doBlockingMessagePump(); // Blocks until _stop() is called
			_shutdownMSAA();
		}
	);
	futureResult.wait();
	return futureResult.get();
}

inline int MessagePumpThread::_stop() {
	// Not in thread.
	m_shouldContinuePump = false; // stop the message pump
	// send another message to ensure that message pump is not 
	// blocked on GetMessage
	auto threadHandle = static_cast<HANDLE>(m_thread.native_handle());
	DWORD threadId = ::GetThreadId(threadHandle);
	PostThreadMessage(threadId, WM_APP + 1, 0, 0);
	m_thread.join();
	return 0;
}


inline void MessagePumpThread::_doBlockingMessagePump() {
	bool pumpStillValid = true;
	MSG msg = { 0 };
	while (pumpStillValid && m_shouldContinuePump) {
		const auto res = GetMessage (
			&msg, // _Out_ LPMSG lpMsg
			nullptr, // _In_opt_ HWND hWnd
			0u, // _In_ UINT wMsgFilterMin
			0u  // _In_ UINT wMsgFilterMax
		);
		if (0 < res) {
			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
		else {
			pumpStillValid = false;
		}
	}
}

// Unhooks the idEvent and shuts down COM.
inline int MessagePumpThread::_shutdownMSAA() {
	if (s_winEventHook) {
		UnhookWinEvent(s_winEventHook);
	}
	if (m_cooinit) {
		CoUninitialize();
	}
	return 0;
}

inline void MessagePumpThread::_initialise(std::promise<int> initResult) {
	auto res = _initializeMSAA();
	initResult.set_value(res);
	m_shouldContinuePump = true;
}

// Initializes COM and sets up the idEvent hook.

inline int MessagePumpThread::_initializeMSAA()
{
	auto res = CoInitializeEx(
		nullptr,
		COINIT_MULTITHREADED | COINIT_SPEED_OVER_MEMORY
	);
	m_cooinit = true;
	s_winEventHook = SetWinEventHook(
		//EVENT_MIN, EVENT_MAX, // Range of events
		EVENT_IDS_TO_ACCEPT.front(), EVENT_IDS_TO_ACCEPT.back(),
		nullptr, // Handle to DLL.
		MessagePumpThread::_sHandleWinEvent, // The callback.
		0, 0, // Process and thread IDs of interest (0 = all)
		WINEVENT_OUTOFCONTEXT // Flags.
	);
	if (!s_winEventHook) {
		return -2;
	}
	return 0;
}

inline void MessagePumpThread::_handleWinEvent(EventData & e) {
	/*
		Note, this function must be re-entrant and thread safe.
		Multiple calls to this may happen simultaniously.
	*/
	// Ignore all object IDs from alert onwards(sound, nativeom etc) as we don't support them
	if (e.idObject <= OBJID_ALERT) {
		return;
	}
	// Ignore all locationChange events except ones for the caret
	if (e.idEvent == EVENT_OBJECT_LOCATIONCHANGE
		&& e.idObject != OBJID_CARET) {
		return;
	}
	// Early exit for destroy objects, NVDA should be notified as early as possible.
	if (e.idEvent == EVENT_OBJECT_DESTROY) {
		m_eventNotifier.NotifyClientOfDestroyEvent(e);
		return;
	}
	m_buffer.Write(e);
}

int MessagePumpThread::Start() {
	return _start();
}

int MessagePumpThread::Stop() {
	return _stop();
}

void MessagePumpThread::_sHandleWinEvent(
	HWINEVENTHOOK hook, DWORD idEvent,
	HWND hwnd, LONG idObject,
	LONG idChild, DWORD dwEventThread,
	DWORD dwmsEventTime
) {
	/*
		Note, this function must be re-entrant and thread safe.
		Multiple calls to this may happen simultaniously.
	*/
	if (!_in(idEvent, EVENT_IDS_TO_ACCEPT)) {
		return;
	}
	EventData e{
		idEvent, hwnd,
		idObject, idChild,
		dwEventThread, dwmsEventTime
	};
	s_instance->_handleWinEvent(e);
}



