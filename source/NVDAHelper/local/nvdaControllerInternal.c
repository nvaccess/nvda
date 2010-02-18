#include <windows.h>
#include "nvdaControllerInternal.h"

__declspec(dllexport) error_status_t(__stdcall *_nvdaControllerInternal_inputLangChangeNotify)(const long, const unsigned long, const wchar_t*);
error_status_t __stdcall nvdaControllerInternal_inputLangChangeNotify(const long threadID, const unsigned long hkl, const wchar_t* layoutString) {
	return _nvdaControllerInternal_inputLangChangeNotify(threadID,hkl,layoutString);
}
