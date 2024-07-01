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

#ifndef NVDAHELPER_LOG_H
#define NVDAHELPER_LOG_H

#include <string>
#include <sstream>
#include <common/lock.h>

#define nhAssert _ASSERTE

void logMessage(int level, const wchar_t* msg);

int NVDALogCrtReportHook(int reportType, const wchar_t* msg, int* returnVal);

#define LOGLEVEL_NONE 60
#define LOGLEVEL_CRITICAL 50
#define LOGLEVEL_ERROR 40
#define LOGLEVEL_WARNING 30
#define LOGLEVEL_INFO 20
#define LOGLEVEL_DEBUGWARNING 15
#define LOGLEVEL_DEBUG 10

#define __STR2WSTR(x) L##x
#define _STR2WSTR(x) __STR2WSTR(x)

static std::wostringstream _logStringStream;
static LockableObject _logLock;

#define _LOG_MSG_MACRO(level,message) {\
	_logLock.acquire();\
	_logStringStream.str(L"");\
	_logStringStream<<L"Thread "<<GetCurrentThreadId()<<L", "<<_STR2WSTR(__FILE__)<<L", "<<_STR2WSTR(__FUNCTION__)<<L", "<<__LINE__<<L":"<<std::endl<<message<<std::endl;\
	logMessage(level,_logStringStream.str().c_str());\
	_logLock.release();\
}

#ifndef LOGLEVEL
#define LOGLEVEL LOGLEVEL_NONE
#endif

#if LOGLEVEL <= LOGLEVEL_CRITICAL
#define LOG_CRITICAL(message) _LOG_MSG_MACRO(LOGLEVEL_CRITICAL,message)
 #else
#define LOG_CRITICAL(message)
#endif

#if LOGLEVEL <= LOGLEVEL_ERROR
#define LOG_ERROR(message) _LOG_MSG_MACRO(LOGLEVEL_ERROR,message)
 #else
#define LOG_ERROR(message)
#endif

#if LOGLEVEL <= LOGLEVEL_WARNING
#define LOG_WARNING(message) _LOG_MSG_MACRO(LOGLEVEL_WARNING,message)
 #else
#define LOG_WARNING(message)
#endif

#if LOGLEVEL <= LOGLEVEL_INFO
#define LOG_INFO(message) _LOG_MSG_MACRO(LOGLEVEL_INFO,message)
 #else
#define LOG_INFO(message)
#endif

#if LOGLEVEL <= LOGLEVEL_DEBUGWARNING
#define LOG_DEBUGWARNING(message) _LOG_MSG_MACRO(LOGLEVEL_DEBUGWARNING,message)
 #else
#define LOG_DEBUGWARNING(message)
#endif

#if LOGLEVEL <= LOGLEVEL_DEBUG
#define LOG_DEBUG(message) _LOG_MSG_MACRO(LOGLEVEL_DEBUG,message)
 #else
#define LOG_DEBUG(message)
#endif

#endif
