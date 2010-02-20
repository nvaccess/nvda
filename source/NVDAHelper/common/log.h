#ifndef NVDAHELPER_LOG_H
#define NVDAHELPER_LOG_H

#include <string>
#include <sstream>

#define __STR2WSTR(x) L##x
#define _STR2WSTR(x) __STR2WSTR(x)

#define _LOG_MSG(level,message) {\
	std::wostringstream* s = new std::wostringstream;\
	(*s)<<message;\
	nvdaControllerInternal_logMessage(GetCurrentProcessId(),GetCurrentThreadId(),level,_STR2WSTR(__FILE__),_STR2WSTR(__FUNCTION__),__LINE__,s->str().c_str());\
	delete s;\
}

#define LOGLEVEL_NONE 0
#define LOGLEVEL_ERROR 10 
#define LOGLEVEL_WARNING 20
#define LOGLEVEL_INFO 30
#define LOGLEVEL_DEBUGWARNING 40
#define LOGLEVEL_DEBUG 50

#ifndef LOGLEVEL
#define LOGLEVEL LOGLEVEL_NONE
#endif

#if LOGLEVEL >= LOGLEVEL_ERROR
#define LOG_ERROR(message) _LOG_MSG(L"error",message)
 #else
#define LOG_ERROR(message)
#endif

#if LOGLEVEL >= LOGLEVEL_WARNING
#define LOG_WARNING(message) _LOG_MSG(L"warning",message)
 #else
#define LOG_WARNING(message)
#endif

#if LOGLEVEL >= LOGLEVEL_INFO
#define LOG_INFO(message) _LOG_MSG(L"info",message)
 #else
#define LOG_INFO(message)
#endif

#if LOGLEVEL >= LOGLEVEL_DEBUGWARNING
#define LOG_DEBUGWARNING(message) _LOG_MSG(L"debugWarning",message)
 #else
#define LOG_DEBUGWARNING(message)
#endif

#if LOGLEVEL >= LOGLEVEL_DEBUG
#define LOG_DEBUG(message) _LOG_MSG(L"debug",message)
 #else
#define LOG_DEBUG(message)
#endif

#endif
