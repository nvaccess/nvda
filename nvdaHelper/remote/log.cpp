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
#include <crtdbg.h>
#include "nvdaControllerInternal.h"
#include "nvdaHelperRemote.h"
#include <common/log.h>

std::deque<std::tuple<int, std::wstring>> logQueue;

// Fetch a  maximum number of messages from the log queue
// and send them onto NvDA via rpc.
void __stdcall log_flushQueue(ULONG_PTR maxCount) {
	while(!logQueue.empty()) {
		if(maxCount < 1) break;
		{
			auto& [level, msg] = logQueue.front();
			nvdaControllerInternal_logMessage(level, GetCurrentProcessId(), msg.c_str());
		}
		logQueue.pop_front();
		--maxCount;
	}
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
		// The message is queued to NVDA's inproc manager thread to be logged from there.
		logQueue.emplace_back(level, msg);
		QueueUserAPC(log_flushQueue, inprocMgrThreadHandle, 1);
	} else {
		// The message is being logged from NVDA's inproc manager thread.
		// Log to NVDA via rpc directly.
	// But first flush any pending log messages from other threads to ensure they are kept in the right order
	log_flushQueue(logQueue.size());
		nvdaControllerInternal_logMessage(level,GetCurrentProcessId(),msg);
	}
}

void log_terminate() {
	// Send any remaining messages in the queue to NVDA
	log_flushQueue(logQueue.size());
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

