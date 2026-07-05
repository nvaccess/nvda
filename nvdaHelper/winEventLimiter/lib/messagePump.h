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
#include <thread>
#include <atomic>
#include <future>
#include <memory>
#include <vector>

#include "eventData.h"

class WriteBuffer;

class MessagePumpThread {
public:
	// Creates (or returns) the singleton pump, which hooks each of the given winEvent IDs.
	static std::shared_ptr<MessagePumpThread> GetInstance(
		WriteBuffer& buffer,
		std::vector<DWORD> eventIds
	);

	// The current instance, or null if none; never creates one.
	static std::shared_ptr<MessagePumpThread> GetExistingInstance();

	// Drops the singleton reference so a future GetInstance creates a fresh pump.
	// Only call once the pump has been stopped (or failed to start).
	static void ResetInstance();

	int Start();

	int Stop();

	~MessagePumpThread();
private:
	// static vars
	static std::shared_ptr<MessagePumpThread>& s_instance;
	static void CALLBACK _sHandleWinEvent(
		HWINEVENTHOOK hook, DWORD idEvent, HWND hwnd,
		LONG idObject, LONG idChild,
		DWORD dwEventThread, DWORD dwmsEventTime
	);

	// member vars
	std::atomic<bool> m_shouldContinuePump;
	std::atomic<bool> m_stopRequested;
	WriteBuffer& m_buffer;
	const std::vector<DWORD> m_eventIds;
	std::vector<HWINEVENTHOOK> m_winEventHooks;
	std::thread m_thread;
	bool m_coInit;
	HANDLE m_stopEvent;

	MessagePumpThread(WriteBuffer& doubleBuffer, std::vector<DWORD> eventIds);

	int _start();

	void _initialise(std::promise<int> initResult);

	// Initializes COM and sets up the idEvent hook.
	int _initializeMSAA();

	void _doBlockingMessagePump();

	void _handleWinEvent(EventData& e);

	int _stop();

	// Must run on the pump thread, which registered the hooks.
	void _unhookWinEvents();

	// Unhooks the idEvent and shuts down COM.
	int _shutdownMSAA();
};
