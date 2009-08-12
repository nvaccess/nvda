#include <cstdio>
#include <cassert>
#include <windows.h>
#include <remote/nvdaHelperRemote.h>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR cmdline, int flags) {
	int res=0;
	Beep(440,100);
	res=nvdaHelper_initialize();
	assert(res==0); //nvdaHelper_initialize
	// Wait for input or EOF.
	getc(stdin);
	res=nvdaHelper_terminate();
	assert(res==0); //nvdaHelper_terminate
	Beep(880,100);
	return 0;
}
