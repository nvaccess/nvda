#include <io.h>
#include <windows.h>

int access(const char* path, int mode) {
	return GetFileAttributes(path);
}

