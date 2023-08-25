/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2018 NV Access Limited, rui Batista, Google LLC.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <local/nvdaControllerInternal.h>

error_status_t(__stdcall *_nvdaControllerInternal_requestRegistration)(const wchar_t*);
error_status_t __stdcall nvdaControllerInternal_requestRegistration(const wchar_t* uuidString) {
	return _nvdaControllerInternal_requestRegistration(uuidString);
}

error_status_t(__stdcall *_nvdaControllerInternal_inputLangChangeNotify)(const long, const unsigned long, const wchar_t*);
error_status_t __stdcall nvdaControllerInternal_inputLangChangeNotify(const long threadID, const unsigned long hkl, const wchar_t* layoutString) {
	return _nvdaControllerInternal_inputLangChangeNotify(threadID,hkl,layoutString);
}

error_status_t(__stdcall *_nvdaControllerInternal_typedCharacterNotify)(const wchar_t); 
error_status_t __stdcall nvdaControllerInternal_typedCharacterNotify(const wchar_t ch) {
	return _nvdaControllerInternal_typedCharacterNotify(ch);
}


error_status_t(__stdcall *_nvdaControllerInternal_logMessage)(const long, const long, const wchar_t*);
error_status_t __stdcall nvdaControllerInternal_logMessage(const long level, const long processID, const wchar_t* message) {
	return _nvdaControllerInternal_logMessage(level,processID,message);
}

error_status_t(__stdcall *_nvdaControllerInternal_displayModelTextChangeNotify)(const long, const long, const long, const long, const long);
error_status_t __stdcall nvdaControllerInternal_displayModelTextChangeNotify(const long hwnd, const long left, const long top, const long right, const long bottom) { 
	return _nvdaControllerInternal_displayModelTextChangeNotify(hwnd,left,top,right,bottom);
}

error_status_t(__stdcall *_nvdaControllerInternal_inputCompositionUpdate)(const wchar_t*, const int, const int, const int);
error_status_t __stdcall nvdaControllerInternal_inputCompositionUpdate(const wchar_t* compositionString, const int selectionStart, const int selectionEnd, const int isReading) {
	return _nvdaControllerInternal_inputCompositionUpdate(compositionString,selectionStart,selectionEnd,isReading);
}

error_status_t(__stdcall *_nvdaControllerInternal_inputCandidateListUpdate)(const wchar_t*, const long, const wchar_t*);
error_status_t __stdcall nvdaControllerInternal_inputCandidateListUpdate(const wchar_t* candidates, const long selectionIndex, const wchar_t* inputMethod) {
	return _nvdaControllerInternal_inputCandidateListUpdate(candidates,selectionIndex,inputMethod);
}

error_status_t(__stdcall *_nvdaControllerInternal_IMEOpenStatusUpdate)(const long);
error_status_t __stdcall nvdaControllerInternal_IMEOpenStatusUpdate(const long opened) {
	return _nvdaControllerInternal_IMEOpenStatusUpdate(opened);
}

error_status_t(__stdcall *_nvdaControllerInternal_inputConversionModeUpdate)(const long, const long, const unsigned long);
error_status_t __stdcall nvdaControllerInternal_inputConversionModeUpdate(const long oldFlags, const long newFlags, const unsigned long lcid) {
	return _nvdaControllerInternal_inputConversionModeUpdate(oldFlags,newFlags,lcid);
}

error_status_t(__stdcall *_nvdaControllerInternal_vbufChangeNotify)(const int, const int);
error_status_t __stdcall nvdaControllerInternal_vbufChangeNotify(const int rootDocHandle, const int rootID) {
	return _nvdaControllerInternal_vbufChangeNotify(rootDocHandle,rootID);
}

error_status_t(__stdcall *_nvdaControllerInternal_installAddonPackageFromPath)(const wchar_t *);
error_status_t __stdcall nvdaControllerInternal_installAddonPackageFromPath(const wchar_t *addonPath) {
	return _nvdaControllerInternal_installAddonPackageFromPath(addonPath);
}

error_status_t(__stdcall *_nvdaControllerInternal_drawFocusRectNotify)(const long, const long, const long, const long, const long);
error_status_t __stdcall nvdaControllerInternal_drawFocusRectNotify(const long hwnd, const long left, const long top, const long right, const long bottom) { 
	return _nvdaControllerInternal_drawFocusRectNotify(hwnd,left,top,right,bottom);
}

error_status_t(__stdcall *_nvdaControllerInternal_reportLiveRegion)(const wchar_t*, const wchar_t*);
error_status_t __stdcall nvdaControllerInternal_reportLiveRegion(const wchar_t* text, const wchar_t* politeness) {
	return _nvdaControllerInternal_reportLiveRegion(text, politeness);
}

error_status_t(__stdcall *_nvdaControllerInternal_openConfigDirectory)();
error_status_t __stdcall nvdaControllerInternal_openConfigDirectory() {
	return _nvdaControllerInternal_openConfigDirectory();
}
