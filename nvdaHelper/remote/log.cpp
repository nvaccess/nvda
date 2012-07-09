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

#include <crtdbg.h>
#include "nvdaControllerInternal.h"
#include <common/log.h>

void logMessage(int level, const wchar_t* msg) {
	if(level>LOGLEVEL_DEBUG) nvdaControllerInternal_logMessage(level,GetCurrentProcessId(),msg);
	OutputDebugString(msg);
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

