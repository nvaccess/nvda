#include <cstdio>
#include <windows.h>
#include <remote/nvdaHelperRemote.h>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR cmdline, int flags) {
	Beep(440,100);
	nvdaHelper_initialize();
	// Wait for input or EOF.
	getc(stdin);
	nvdaHelper_terminate();
	Beep(880,100);
	return 0;
}
