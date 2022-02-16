/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2010 NVDA contributers.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <string>
#include <queue>
#include <mutex>
#include <crtdbg.h>
#include <remote/nvdaControllerInternal.h>
#include "nvdaHelperRemote.h"
#include <common/log.h>

std::deque<std::tuple<int, std::wstring>> logQueue;
std::mutex logQueueLock;

// Forward declare an APC function for flushing the log queue. 
void __stdcall log_flushQueue_apcFunc(ULONG_PTR data);

// Fetch all available messages from the queue
// and send them onto NvDA via rpc.
void log_flushQueue() {
	// Ensure this is never called from outside the manager thread.
	if(!inprocMgrThreadHandle) {
		// the manager thread does not yet exist.
		// just ignore the call as once it does exist it will flush itself.
		return;
	} else if(GetCurrentThreadId() != GetThreadId(inprocMgrThreadHandle)) {
		// call it correctly in the manager thread with APC.
		QueueUserAPC(log_flushQueue_apcFunc, inprocMgrThreadHandle, 0);
		return;
	}
	std::deque<std::tuple<int, std::wstring>> tempQueue;
	{
		std::lock_guard lock{logQueueLock};
		tempQueue.swap(logQueue);
	}
	for(auto& [level, msg] : tempQueue) {
		nvdaControllerInternal_logMessage(level, GetCurrentProcessId(), msg.c_str());
	}
}

void __stdcall log_flushQueue_apcFunc(ULONG_PTR data) {
	log_flushQueue();
}

void logMessage(int level, const wchar_t* msg) {
	// Always log to any connected debugger 
	OutputDebugString(msg);
	if(
		!inprocMgrThreadHandle
		|| GetCurrentThreadId() != GetThreadId(inprocMgrThreadHandle)
	) {
		// either the NVDA inproc manager thread is not yet running,
		// Or this message is being logged from outside NVDA's inproc manager thread.
		// So as to not block any app threads,
		// The message is queued for later fetching by  NVDA's inproc manager thread
		{
			std::lock_guard lock{logQueueLock};
			logQueue.emplace_back(level, msg);
		}
		if(inprocMgrThreadHandle) {
			QueueUserAPC(log_flushQueue_apcFunc, inprocMgrThreadHandle, 0);
		}
	} else {
		// The message is being logged from NVDA's inproc manager thread.
		// Log to NVDA via rpc directly.
		// But first flush any pending log messages from other threads to ensure they are kept in the right order
		log_flushQueue();
		nvdaControllerInternal_logMessage(level,GetCurrentProcessId(),msg);
	}
}

int NVDALogCrtReportHook(int reportType,const wchar_t *message,int *returnValue) {
	bool doDebugBreak=false;
	int level=LOGLEVEL_WARNING;
	if(reportType==_CRT_ERROR) {
		level=LOGLEVEL_ERROR;
		doDebugBreak=true;
	} else if(reportType==_CRT_ASSERT) {
		level=LOGLEVEL_CRITICAL;
		doDebugBreak=true;
	}
	logMessage(level,message);
	if(doDebugBreak&&IsDebuggerPresent()) {
		_CrtDbgBreak();
	}
	*returnValue=0;
	return true;
}
