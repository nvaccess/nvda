//inputLangChange.c
//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence
//See the file Copying for details.

#include <windows.h>
#include "nvdaHelperRemote.h"
#include "nvdaControllerInternal.h"
#include "inputLangChange.h"

LRESULT CALLBACK inputLangChange_callWndProcHook(int code, WPARAM wParam, LPARAM lParam) {
	static int lastInputLangChange=0;
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if((pcwp->message==WM_INPUTLANGCHANGE)&&(pcwp->lParam!=lastInputLangChange)) {
		wchar_t* buf=(wchar_t*)malloc(sizeof(wchar_t)*1024);
		GetKeyboardLayoutName(buf);
		nvdaControllerInternal_inputLangChangeNotify(GetCurrentThreadId(),pcwp->lParam,buf);
		free(buf);
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
