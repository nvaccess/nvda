#define UNICODE
#include <windows.h>
#include "nvdaController.h"

int main(int argc, char* argv[]) {
	long res=nvdaController_testIfRunning();
	if(res!=0) {
		MessageBox(0,L"Error communicating with NVDA",L"Error",0);
		return 1;
	}
	nvdaController_speakText(L"This is a test speech message");
	nvdaController_brailleMessage(L"This is a test braille message");
	Sleep(1000);
	nvdaController_speakText(L"Test completed!");
	nvdaController_brailleMessage(L"Test completed!");
return 0;
}
