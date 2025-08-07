// Copyright(C) 2006-2023 NV Access Limited, Leonard de Ruijter
// This file is covered by the GNU Lesser General Public License, version 2.1.
// See the file license.txt for more details.

#define UNICODE
#include <windows.h>
#include <stdio.h>
#include "nvdaController.h"

error_status_t __stdcall onMarkReached(const wchar_t*  name) {
	wprintf(L"Reached SSML mark with name %s\n", name);
	return ERROR_SUCCESS;
}

int main(int argc, char *argv[]) {
	long res = nvdaController_testIfRunning();
	if (res != 0) {
		MessageBox(0, L"Error communicating with NVDA", L"Error", 0);
		return 1;
	}
	for (int i = 0; i < 4; i++) {
		nvdaController_speakText(L"This is a test speech message");
		nvdaController_brailleMessage(L"This is a test braille message");
		Sleep(1000);
	}
	wchar_t* ssml = (
		L"<speak>"
		L"This is one sentence. "
		L"<mark name=\"test\" />"
		L"<prosody pitch=\"200%\">This sentence is pronounced with higher pitch.</prosody>"
		L"<mark name=\"test2\" />"
		L"This is a third sentence. "
		L"<mark name=\"test3\" />"
		L"This is a fourth sentence. We will stay silent for a second after this one."
		L"<break time=\"1000ms\" />"
		L"<mark name=\"test4\" />"
		L"This is a fifth sentence. "
		L"<mark name=\"test5\" />"
		L"</speak>"
	);
	nvdaController_setOnSsmlMarkReachedCallback(&onMarkReached);
	nvdaController_speakSsml(ssml, SYMBOL_LEVEL_UNCHANGED,  SPEECH_PRIORITY_NORMAL, FALSE);
	nvdaController_setOnSsmlMarkReachedCallback(NULL);
	nvdaController_brailleMessage(L"Test completed!");
	return 0;
}
