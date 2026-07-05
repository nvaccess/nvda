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
#include "messagePump.h"

#include <utility>

#include "eventDoubleBuffer.h"


// Deliberately retain the empty holder until process exit. A normal stop resets the
// contained pump; avoiding a static shared_ptr destructor prevents thread teardown
// under the loader lock if the host exits without calling winEventLimiter_stop.
std::shared_ptr<MessagePumpThread>& MessagePumpThread::s_instance =
	*new std::shared_ptr<MessagePumpThread>();


std::shared_ptr<MessagePumpThread>
MessagePumpThread::GetInstance(WriteBuffer & buffer, std::vector<DWORD> eventIds) {
	if (!s_instance) {
		s_instance = std::shared_ptr<MessagePumpThread>(
			new MessagePumpThread(buffer, std::move(eventIds))
		);
	}
	return s_instance;
}

std::shared_ptr<MessagePumpThread> MessagePumpThread::GetExistingInstance() {
	return s_instance;
}

void MessagePumpThread::ResetInstance() {
	s_instance.reset();
}

MessagePumpThread::MessagePumpThread(WriteBuffer& doubleBuffer, std::vector<DWORD> eventIds)
	: m_shouldContinuePump(false)
	, m_stopRequested(false)
	, m_buffer(doubleBuffer)
	, m_eventIds(std::move(eventIds))
	, m_thread()
	, m_coInit(false)
	, m_stopEvent(CreateEventW(nullptr, TRUE, FALSE, nullptr))
{ }

inline int MessagePumpThread::_start() {
	// Not in thread
	if (m_stopEvent == nullptr || !ResetEvent(m_stopEvent)) {
		return -4;
	}
	m_stopRequested = false;
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
	const auto result = futureResult.get();
	if (result != 0) {
		// Initialisation failed: the pump loop never runs, so the thread is already exiting.
		m_thread.join();
	}
	return result;
}

inline int MessagePumpThread::_stop() {
	// Not in thread.
	m_stopRequested = true;
	m_shouldContinuePump = false; // stop the message pump
	if (!m_thread.joinable()) {
		// Never started, or already joined by a failed _start().
		return 0;
	}
	SetEvent(m_stopEvent);
	m_thread.join();
	return 0;
}


inline void MessagePumpThread::_doBlockingMessagePump() {
	MSG msg = { 0 };
	while (m_shouldContinuePump) {
		const DWORD waitResult = MsgWaitForMultipleObjectsEx(
			1,
			&m_stopEvent,
			INFINITE,
			QS_ALLINPUT,
			MWMO_INPUTAVAILABLE
		);
		if (waitResult == WAIT_OBJECT_0) {
			break;
		}
		if (waitResult != WAIT_OBJECT_0 + 1) {
			// A transient wait failure must not silently remove all hooks. Yield before
			// retrying so a persistent failure cannot create a busy loop.
			Sleep(10);
			continue;
		}
		while (m_shouldContinuePump && PeekMessageW(&msg, nullptr, 0, 0, PM_REMOVE)) {
			if (msg.message == WM_QUIT) {
				continue;
			}
			TranslateMessage(&msg);
			DispatchMessageW(&msg);
		}
	}
}

inline void MessagePumpThread::_unhookWinEvents() {
	for (const HWINEVENTHOOK hook : m_winEventHooks) {
		UnhookWinEvent(hook);
	}
	m_winEventHooks.clear();
}

// Unhooks the winEvents and shuts down COM.
inline int MessagePumpThread::_shutdownMSAA() {
	_unhookWinEvents();
	if (m_coInit) {
		CoUninitialize();
		m_coInit = false;
	}
	return 0;
}

inline void MessagePumpThread::_initialise(std::promise<int> initResult) {
	auto res = _initializeMSAA();
	if (res == 0) {
		// Must be set before fulfilling the promise: once the caller observes success,
		// a concurrent _stop() must not race with this write.
		m_shouldContinuePump = true;
	}
	initResult.set_value(res);
}

// Initializes COM and sets up the winEvent hooks.

inline int MessagePumpThread::_initializeMSAA()
{
	const HRESULT hr = CoInitializeEx(
		nullptr,
		COINIT_MULTITHREADED | COINIT_SPEED_OVER_MEMORY
	);
	// S_FALSE (already initialized) still requires a balancing CoUninitialize.
	// On RPC_E_CHANGED_MODE the apartment is usable but not ours to uninitialize.
	m_coInit = SUCCEEDED(hr);
	// One hook per event ID, like NVDA's in-process registration: Windows then only
	// delivers the requested events, so no per-event acceptance filtering is needed.
	m_winEventHooks.reserve(m_eventIds.size());
	bool hookRegistrationFailed = false;
	for (const auto eventId : m_eventIds) {
		const auto hook = SetWinEventHook(
			eventId, eventId, // Range of events: just this one.
			nullptr, // Handle to DLL.
			MessagePumpThread::_sHandleWinEvent, // The callback.
			0, 0, // Process and thread IDs of interest (0 = all)
			WINEVENT_OUTOFCONTEXT // Flags.
		);
		if (hook) {
			m_winEventHooks.push_back(hook);
		}
		else {
			hookRegistrationFailed = true;
		}
	}
	const bool noHooksRegistered = m_winEventHooks.empty();
	if (noHooksRegistered || hookRegistrationFailed) {
		_unhookWinEvents();
		if (m_coInit) {
			CoUninitialize();
			m_coInit = false;
		}
		return -2;
	}
	return 0;
}

inline void MessagePumpThread::_handleWinEvent(EventData & e) {
	/*
		Note, this function must be re-entrant and thread safe.
		Multiple calls to this may happen simultaneously.
		Keep this logic aligned with Python internalWinEventHandler.winEventCallback.
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
	// Destroy events also travel through the buffer (the limiter thread diverts them to a
	// separate fetch queue), so this thread never blocks on the client's runtime (GIL).
	m_buffer.Write(e);
}

int MessagePumpThread::Start() {
	return _start();
}

int MessagePumpThread::Stop() {
	return _stop();
}

MessagePumpThread::~MessagePumpThread() {
	// Safety net so destruction without a prior Stop() cannot std::terminate on a joinable
	// thread. Joining here during DLL_PROCESS_DETACH could deadlock on the loader lock;
	// the supported teardown remains winEventLimiter_stop() before unload.
	_stop();
	if (m_stopEvent != nullptr) {
		CloseHandle(m_stopEvent);
		m_stopEvent = nullptr;
	}
}

void MessagePumpThread::_sHandleWinEvent(
	HWINEVENTHOOK hook, DWORD idEvent,
	HWND hwnd, LONG idObject,
	LONG idChild, DWORD dwEventThread,
	DWORD dwmsEventTime
) {
	/*
		Note, this function must be re-entrant and thread safe.
		Multiple calls to this may happen simultaneously.
	*/
	// Copy the singleton reference. Teardown resets s_instance only after the pump thread
	// (and with it these hooks) has been stopped, but be defensive anyway.
	const auto instance = s_instance;
	if (!instance) {
		return;
	}
	if (instance->m_stopRequested) {
		// Out-of-context callbacks are dispatched on the pump thread while it retrieves
		// messages. Unhook here so an event flood cannot keep that retrieval call alive
		// indefinitely after the stop event has been signalled.
		instance->_unhookWinEvents();
		return;
	}
	EventData e{
		idEvent, hwnd,
		idObject, idChild,
		dwEventThread, dwmsEventTime
	};
	instance->_handleWinEvent(e);
}
