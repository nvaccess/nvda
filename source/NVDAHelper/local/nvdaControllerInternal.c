#include <windows.h>
#include "nvdaControllerInternal.h"

__declspec(dllexport) error_status_t(__stdcall *_nvdaControllerInternal_inputLangChangeNotify)(const long, const unsigned long, const wchar_t*);
error_status_t __stdcall nvdaControllerInternal_inputLangChangeNotify(const long threadID, const unsigned long hkl, const wchar_t* layoutString) {
	return _nvdaControllerInternal_inputLangChangeNotify(threadID,hkl,layoutString);
}

__declspec(dllexport) error_status_t(__stdcall *_nvdaControllerInternal_logMessage)(const long, const long, const wchar_t*, const wchar_t*, const wchar_t*, const long, const wchar_t*);
error_status_t __stdcall nvdaControllerInternal_logMessage(const long processID, const long threadID, const wchar_t* level, const wchar_t* fileName, const wchar_t* funcName, const long lineNo, const wchar_t* message) {
	return _nvdaControllerInternal_logMessage(processID,threadID,level,fileName,funcName,lineNo,message);
}
