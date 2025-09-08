/*
A part of NonVisual Desktop Access (NVDA)
This file is covered by the GNU General Public License.
See the file COPYING for more details.
Copyright (C) 2025 NV Access Limited
*/
#include <windows.h>
#include <dbghelp.h>
#include <string>

/**
 * @brief Writes a crash dump to the specified path.
 *
 * This function creates a minidump file at the given path containing information about the current process state.
 * It is typically called from an unhandled exception filter.
 *
 * @param dumpPath The path to write the crash dump file.
 * @param pExceptionPointers Exception pointers provided by the UnhandledExceptionFilter.
 * @return true if the dump was written successfully, false otherwise.
 */
bool writeCrashDump(const wchar_t* dumpPath, EXCEPTION_POINTERS* pExceptionPointers) {
	HANDLE hFile = CreateFileW(
		dumpPath,
		GENERIC_WRITE,
		0,
		nullptr,
		CREATE_ALWAYS,
		FILE_ATTRIBUTE_NORMAL,
		nullptr
	);
	if (hFile == INVALID_HANDLE_VALUE) {
		return false;
	}

	MINIDUMP_EXCEPTION_INFORMATION mdei;
	mdei.ThreadId = GetCurrentThreadId();
	mdei.ExceptionPointers = pExceptionPointers;
	mdei.ClientPointers = FALSE;

	// Write a small minidump
	bool res = MiniDumpWriteDump(
		GetCurrentProcess(),
		GetCurrentProcessId(),
		hFile,
		MiniDumpNormal,
		&mdei,
		nullptr,
		nullptr
	);
	CloseHandle(hFile);
	return res;
}
