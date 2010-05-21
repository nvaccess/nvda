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
#include "nvdaControllerInternal.h"

#define __STR2WSTR(x) L##x
#define _STR2WSTR(x) __STR2WSTR(x)

#define _LOG_MSG(level,message) {\
	std::wostringstream* s = new std::wostringstream;\
	(*s)<<message;\
	nvdaControllerInternal_logMessage(GetCurrentProcessId(),GetCurrentThreadId(),level,_STR2WSTR(__FILE__),_STR2WSTR(__FUNCTION__),__LINE__,s->str().c_str());\
	delete s;\
}

#define loglevel_none 60
#define loglevel_critical 50
#define LOGLEVEL_ERROR 40
#define LOGLEVEL_WARNING 30
#define LOGLEVEL_INFO 20
#define LOGLEVEL_DEBUGWARNING 15
#define LOGLEVEL_DEBUG 10

#ifndef LOGLEVEL
#define LOGLEVEL LOGLEVEL_NONE
#endif

#if LOGLEVEL <= LOGLEVEL_CRITICAL
#define LOG_CRITICAL(message) _LOG_MSG(LOGLEVEL_CRITICAL,message)
 #else
#define LOG_CRITICAL(message)
#endif

#if LOGLEVEL <= LOGLEVEL_ERROR
#define LOG_ERROR(message) _LOG_MSG(LOGLEVEL_ERROR,message)
 #else
#define LOG_ERROR(message)
#endif

#if LOGLEVEL <= LOGLEVEL_WARNING
#define LOG_WARNING(message) _LOG_MSG(LOGLEVEL_WARNING,message)
 #else
#define LOG_WARNING(message)
#endif

#if LOGLEVEL <= LOGLEVEL_INFO
#define LOG_INFO(message) _LOG_MSG(LOGLEVEL_INFO,message)
 #else
#define LOG_INFO(message)
#endif

#if LOGLEVEL <= LOGLEVEL_DEBUGWARNING
#define LOG_DEBUGWARNING(message) _LOG_MSG(LOGLEVEL_DEBUGWARNING,message)
 #else
#define LOG_DEBUGWARNING(message)
#endif

#if LOGLEVEL <= LOGLEVEL_DEBUG
#define LOG_DEBUG(message) _LOG_MSG(LOGLEVEL_DEBUG,message)
 #else
#define LOG_DEBUG(message)
#endif

#endif
