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
#include "nvdaHelperRemote.h"
#include "nvdaControllerInternal.h"
#include "inputLangChange.h"

LRESULT CALLBACK inputLangChange_callWndProcHook(int code, WPARAM wParam, LPARAM lParam) {
	static int lastInputLangChange=0;
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if((pcwp->message==WM_INPUTLANGCHANGE)&&(pcwp->lParam!=lastInputLangChange)) {
		wchar_t buf[KL_NAMELENGTH];
		GetKeyboardLayoutName(buf);
		nvdaControllerInternal_inputLangChangeNotify(GetCurrentThreadId(),pcwp->lParam,buf);
		lastInputLangChange=pcwp->lParam;
	}
	return 0;
}

void inputLangChange_inProcess_initialize() {
	registerWindowsHook(WH_CALLWNDPROC,inputLangChange_callWndProcHook);
}

void inputLangChange_inProcess_terminate() {
	unregisterWindowsHook(WH_CALLWNDPROC,inputLangChange_callWndProcHook);
}
