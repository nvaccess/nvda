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

#include <windows.h>
#include "nvdaControllerInternal.h"

error_status_t __stdcall nvdaControllerInternal_getNVDAProcessID(long* pProcessID) {
	*pProcessID=GetCurrentProcessId();
	return RPC_S_OK;
}

__declspec(dllexport) error_status_t(__stdcall *_nvdaControllerInternal_inputLangChangeNotify)(const long, const unsigned long, const wchar_t*);
error_status_t __stdcall nvdaControllerInternal_inputLangChangeNotify(const long threadID, const unsigned long hkl, const wchar_t* layoutString) {
	return _nvdaControllerInternal_inputLangChangeNotify(threadID,hkl,layoutString);
}

__declspec(dllexport) error_status_t(__stdcall *_nvdaControllerInternal_logMessage)(const long, const long, const long, const wchar_t*, const wchar_t*, const long, const wchar_t*);
error_status_t __stdcall nvdaControllerInternal_logMessage(const long processID, const long threadID, const long level, const wchar_t* fileName, const wchar_t* funcName, const long lineNo, const wchar_t* message) {
	return _nvdaControllerInternal_logMessage(processID,threadID,level,fileName,funcName,lineNo,message);
}
