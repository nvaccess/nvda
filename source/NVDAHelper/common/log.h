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

#ifdef LOGGING
#define LOG_DEBUG(messageArg) _LOG_MSG(L"debug",messageArg)
#define LOG_WARN(messageArg) _LOG_MSG(L"debugWarning",messageArg)
#else
#define LOG_DEBUG(messageArg)
#define LOG_WARN(messageArg)
#endif

#endif
