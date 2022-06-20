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

#include <local/nvdaController.h>

error_status_t(__stdcall *_nvdaController_speakText)(const wchar_t*);
error_status_t __stdcall nvdaController_speakText(const wchar_t* text) {
	return _nvdaController_speakText(text);
}

error_status_t(__stdcall *_nvdaController_cancelSpeech)();
error_status_t __stdcall nvdaController_cancelSpeech() {
	return _nvdaController_cancelSpeech();
}

error_status_t(__stdcall *_nvdaController_brailleMessage)(const wchar_t*);
error_status_t __stdcall nvdaController_brailleMessage(const wchar_t* text) {
	return _nvdaController_brailleMessage(text);
}

error_status_t __stdcall nvdaController_testIfRunning() {
	return 0;
}
