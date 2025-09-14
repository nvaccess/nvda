# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by kernel32.dll, and supporting data structures and enumerations."""

from ctypes import (
	WINFUNCTYPE,
	Structure,
	c_void_p,
	c_byte,
	c_wchar,
	c_wchar_p,
	windll,
	POINTER,
	c_size_t,
	c_int,
	c_uint,
	c_long,
	c_short,
	c_ushort,
	HRESULT,
)
from ctypes.wintypes import (
	DWORD,
	WORD,
	USHORT,
	LONG,
	PULONG,
	SMALL_RECT,
	UINT,
	HANDLE,
	HMODULE,
	LPCWSTR,
	BOOL,
	LPVOID,
	HGLOBAL,
	HWND,
	LCID,
	LPWSTR,
	LARGE_INTEGER,
	WCHAR,
)
from serial.win32 import LPOVERLAPPED
from .advapi32 import SECURITY_ATTRIBUTES

ULONG_PTR = c_size_t


__all__ = (
	"GetModuleHandle",
	"GetModuleFileName",
	"LoadLibraryEx",
	"FreeLibrary",
	"CloseHandle",
	"ReleaseMutex",
	"WaitForSingleObject",
	"OpenProcess",
	"VirtualAllocEx",
	"VirtualFreeEx",
	"ReadProcessMemory",
	"WriteProcessMemory",
	"GlobalAlloc",
	"GlobalFree",
	"GlobalLock",
	"GlobalUnlock",
	"GetCurrentProcess",
	"SetUnhandledExceptionFilter",
	"GetCurrentThreadId",
	"OpenThread",
	"QueueUserAPC",
	"CreateEvent",
	"CreateMutex",
	"CreateWaitableTimer",
	"SetEvent",
	"ResetEvent",
	"SetWaitableTimer",
	"CancelWaitableTimer",
	"WaitForMultipleObjects",
	"SleepEx",
	"SetThreadExecutionState",
	"ReadFileEx",
	"WriteFile",
	"GetOverlappedResult",
	"CancelIoEx",
	"WaitCommEvent",
	"CopyFile",
	"GetLocaleInfo",
	"LocaleNameToLCID",
	"GetUserDefaultUILanguage",
	"AttachConsole",
	"FreeConsole",
	"GetConsoleWindow",
	"GetConsoleProcessList",
	"GetConsoleScreenBufferInfo",
	"GetConsoleSelectionInfo",
	"ReadConsoleOutputCharacter",
	"ReadConsoleOutput",
	"SetConsoleCtrlHandler",
	"GetModuleHandleEx",
	"GetPackageFullName",
	"QueryFullProcessImageName",
	"IsWow64Process",
	"IsWow64Process2",
	"GetProcessInformation",
	"RegisterApplicationRestart",
	"GetLastError",
	"GetStdHandle",
	"CreateFile",
	"GetSystemPowerStatus",
	"GetThreadLocale",
	"Wow64DisableWow64FsRedirection",
	"Wow64RevertWow64FsRedirection",
	"FileTimeToSystemTime",
	"SystemTimeToTzSpecificLocalTime",
	"GetDateFormatEx",
	"GetTimeFormatEx",
	"WaitForSingleObjectEx",
	"SetProcessShutdownParameters",
	"GetExitCodeProcess",
	"TerminateProcess",
	"GetDriveType",
	"CreatePipe",
	"DuplicateHandle",
	"MoveFileEx",
	"LCIDToLocaleName",
	"GetACP",
)


dll = windll.kernel32

GetModuleHandle = dll.GetModuleHandleW
"""
Retrieves a module handle for the specified module, which must have been loaded by the calling process.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulehandlew
"""
GetModuleHandle.argtypes = (c_wchar_p,)
GetModuleHandle.restype = HMODULE

GetModuleFileName = dll.GetModuleFileNameW
"""
Retrieves the fully qualified path for the file that contains the specified module, which must have been loaded by the current process.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulefilenamew
"""
GetModuleFileName.argtypes = (HANDLE, c_wchar_p, DWORD)
GetModuleFileName.restype = DWORD

LoadLibraryEx = dll.LoadLibraryExW
"""
Loads the specified module into the address space of the calling process.
The specified module may cause other modules to be loaded.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibraryexw
"""
LoadLibraryEx.argtypes = (
	LPCWSTR,  # lpLibFileName
	HANDLE,  # hFile
	DWORD,  # dwFlags
)
LoadLibraryEx.restype = HMODULE

FreeLibrary = dll.FreeLibrary
"""
Frees the loaded module and decrements its reference count.
If the reference count reaches zero, the module is unloaded from the address space of the calling process.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-freelibrary
"""
FreeLibrary.argtypes = (HMODULE,)
FreeLibrary.restype = BOOL

CloseHandle = dll.CloseHandle
"""
Closes an open object handle. The handle must have been created by the calling process.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle
"""
CloseHandle.argtypes = (HANDLE,)
CloseHandle.restype = BOOL

ReleaseMutex = dll.ReleaseMutex
"""
Releases ownership of the specified mutex object. The calling thread must have owned the mutex object.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-releasemutex
"""
ReleaseMutex.argtypes = (HANDLE,)
ReleaseMutex.restype = BOOL

WaitForSingleObject = dll.WaitForSingleObject
"""
Waits until the specified object is in the signaled state or the time-out interval elapses.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject
"""
WaitForSingleObject.argtypes = (
	HANDLE,  # hHandle
	DWORD,  # dwMilliseconds
)
WaitForSingleObject.restype = DWORD

OpenProcess = dll.OpenProcess
"""
Opens an existing local process object.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess
"""
OpenProcess.argtypes = (
	DWORD,  # dwDesiredAccess
	BOOL,  # bInheritHandle
	DWORD,  # dwProcessId
)
OpenProcess.restype = HANDLE

VirtualAllocEx = dll.VirtualAllocEx
"""
Allocates memory in the virtual address space of a specified process.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex
"""
VirtualAllocEx.argtypes = (
	HANDLE,  # hProcess
	LPVOID,  # lpAddress
	c_size_t,  # dwSize
	DWORD,  # flAllocationType
	DWORD,  # flProtect
)
VirtualAllocEx.restype = LPVOID

VirtualFreeEx = dll.VirtualFreeEx
"""
Frees or releases a region of memory within the virtual address space of a specified process.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualfreeex
"""
VirtualFreeEx.argtypes = (
	HANDLE,  # hProcess
	LPVOID,  # lpAddress
	c_size_t,  # dwSize
	DWORD,  # dwFreeType
)
VirtualFreeEx.restype = BOOL

ReadProcessMemory = dll.ReadProcessMemory
"""
Reads data from the memory of a specified process.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-readprocessmemory
"""
ReadProcessMemory.argtypes = (
	HANDLE,  # hProcess
	LPVOID,  # lpBaseAddress
	LPVOID,  # lpBuffer
	c_size_t,  # nSize
	POINTER(c_size_t),  # lpNumberOfBytesRead
)
ReadProcessMemory.restype = BOOL

WriteProcessMemory = dll.WriteProcessMemory
"""
Writes data to an area of memory in a specified process.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory
"""
WriteProcessMemory.argtypes = (
	HANDLE,  # hProcess
	LPVOID,  # lpBaseAddress
	LPVOID,  # lpBuffer
	c_size_t,  # nSize
	POINTER(c_size_t),  # lpNumberOfBytesWritten
)
WriteProcessMemory.restype = BOOL

DuplicateHandle = dll.DuplicateHandle
"""
Duplicates an object handle.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-duplicatehandle
"""
DuplicateHandle.argtypes = (
	HANDLE,  # hSourceProcessHandle
	HANDLE,  # hSourceHandle
	HANDLE,  # hTargetProcessHandle
	POINTER(HANDLE),  # lpTargetHandle
	DWORD,  # dwDesiredAccess
	BOOL,  # bInheritHandle
	DWORD,  # dwOptions
)
DuplicateHandle.restype = BOOL

GlobalAlloc = dll.GlobalAlloc
"""
Allocates global memory and returns a handle to the allocated memory.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globalalloc
"""
GlobalAlloc.argtypes = (
	UINT,  # uFlags
	c_size_t,  # dwBytes
)
GlobalAlloc.restype = HGLOBAL


GlobalFree = dll.GlobalFree
"""
Frees the specified global memory object and invalidates its handle.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globalfree
"""
GlobalFree.argtypes = (
	HGLOBAL,  # hMem
)
GlobalFree.restype = HGLOBAL

GlobalLock = dll.GlobalLock
"""
Locks a global memory object and returns a pointer to the first byte of the object's memory block.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globallock
"""
GlobalLock.argtypes = (
	HGLOBAL,  # hMem
)
GlobalLock.restype = LPVOID

GlobalUnlock = dll.GlobalUnlock
"""
Unlocks a global memory object, allowing it to be accessed by other processes.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globalunlock
"""
GlobalUnlock.argtypes = (
	HGLOBAL,  # hMem
)
GlobalUnlock.restype = BOOL

GetCurrentProcess = dll.GetCurrentProcess
"""
Retrieves a pseudo handle for the current process.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getcurrentprocess
"""
GetCurrentProcess.argtypes = ()
GetCurrentProcess.restype = HANDLE

UnhandledExceptionFilter = WINFUNCTYPE(
	c_void_p,  # lpTopLevelExceptionFilter: The pointer to the old unhandled exception filter function.
	c_void_p,  # lpTopLevelExceptionFilter: A pointer to the new unhandled exception filter function.
)

SetUnhandledExceptionFilter = dll.SetUnhandledExceptionFilter
"""
Sets a new unhandled exception filter function for the current process.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-setunhandledexceptionfilter
"""
SetUnhandledExceptionFilter.argtypes = (
	UnhandledExceptionFilter,  # lpTopLevelExceptionFilter: A pointer to the new unhandled exception filter function.
)
SetUnhandledExceptionFilter.restype = UnhandledExceptionFilter


GetCurrentThreadId = dll.GetCurrentThreadId
"""
Retrieves the thread identifier of the calling thread.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getcurrentthreadid
"""
GetCurrentThreadId.argtypes = ()
GetCurrentThreadId.restype = DWORD


OpenThread = dll.OpenThread
"""
Opens an existing thread object.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openthread
"""
OpenThread.argtypes = (
	DWORD,  # dwDesiredAccess
	BOOL,  # bInheritHandle
	DWORD,  # dwThreadId
)
OpenThread.restype = HANDLE


PAPCFUNC = WINFUNCTYPE(None, ULONG_PTR)
"""
An application-defined completion routine. Specify this address when calling the QueueUserAPC function.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winnt/nc-winnt-papcfunc
"""


QueueUserAPC = dll.QueueUserAPC
"""
Adds a user-mode asynchronous procedure call (APC) object to the APC queue of the specified thread.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-queueuserapc
"""
QueueUserAPC.argtypes = (
	PAPCFUNC,  # pfnAPC: A pointer to the application-supplied APC function
	HANDLE,  # hThread: A handle to the thread
	ULONG_PTR,  # dwData: A single value that is passed to the APC function
)
QueueUserAPC.restype = BOOL


CreateEvent = dll.CreateEventW
"""
Creates or opens a named or unnamed event object.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createeventw
"""
CreateEvent.argtypes = (
	POINTER(SECURITY_ATTRIBUTES),  # lpEventAttributes: A pointer to a SECURITY_ATTRIBUTES structure
	BOOL,  # bManualReset: If TRUE, the function creates a manual-reset event object
	BOOL,  # bInitialState: If TRUE, the initial state of the event object is signaled
	LPCWSTR,  # lpName: The name of the event object
)
CreateEvent.restype = HANDLE


CreateMutex = dll.CreateMutexW
"""
Creates or opens a named or unnamed mutex object.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createmutexw
"""
CreateMutex.argtypes = (
	POINTER(SECURITY_ATTRIBUTES),  # lpMutexAttributes: A pointer to a SECURITY_ATTRIBUTES structure
	BOOL,  # bInitialOwner: If TRUE, the calling thread requests immediate ownership
	LPCWSTR,  # lpName: The name of the mutex object
)
CreateMutex.restype = HANDLE


CreateWaitableTimer = dll.CreateWaitableTimerW
CreateWaitableTimerW = dll.CreateWaitableTimerW
"""
Creates or opens a waitable timer object.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createwaitabletimerw
"""
CreateWaitableTimer.argtypes = (
	POINTER(SECURITY_ATTRIBUTES),  # lpTimerAttributes: A pointer to a SECURITY_ATTRIBUTES structure
	BOOL,  # bManualReset: If TRUE, the function creates a manual-reset notification timer
	LPCWSTR,  # lpTimerName: The name of the timer object
)
CreateWaitableTimer.restype = HANDLE


SetEvent = dll.SetEvent
"""
Sets the specified event object to the signaled state.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-setevent
"""
SetEvent.argtypes = (
	HANDLE,  # hEvent: A handle to the event object
)
SetEvent.restype = BOOL


ResetEvent = dll.ResetEvent
"""
Sets the specified event object to the nonsignaled state.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-resetevent
"""
ResetEvent.argtypes = (
	HANDLE,  # hEvent: A handle to the event object
)
ResetEvent.restype = BOOL


PTIMERAPCROUTINE = WINFUNCTYPE(
	None,
	LPVOID,  # lpArgToCompletionRoutine: The argument to be passed to the completion routine
	# DWORD,  # dwTimerLowValue: The low-order part of the time-out value
	# DWORD,  # dwTimerHighValue: The high-order part of the time-out
)
"""
An application-defined timer completion routine. Specify this address when calling the SetWaitableTimer function.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nc-synchapi-ptimerapcroutine
"""

SetWaitableTimer = dll.SetWaitableTimer
"""
Activates the specified waitable timer.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-setwaitabletimer
"""
SetWaitableTimer.argtypes = (
	HANDLE,  # hTimer: A handle to the timer object
	POINTER(LARGE_INTEGER),  # lpDueTime: A pointer to a LARGE_INTEGER structure
	c_int,  # lPeriod: The period of the timer, in milliseconds
	c_void_p,  # pfnCompletionRoutine: An optional pointer to the completion routine
	LPVOID,  # lpArgToCompletionRoutine: A single value passed to the completion routine
	BOOL,  # fResume: If TRUE, restores a system in suspended power conservation mode
)
SetWaitableTimer.restype = BOOL


CancelWaitableTimer = dll.CancelWaitableTimer
"""
Sets the specified waitable timer to the inactive state.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-cancelwaitabletimer
"""
CancelWaitableTimer.argtypes = (
	HANDLE,  # hTimer: A handle to the timer object
)
CancelWaitableTimer.restype = BOOL


WaitForMultipleObjects = dll.WaitForMultipleObjects
"""
Waits until one or all of the specified objects are in the signaled state or the time-out interval elapses.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitformultipleobjects
"""
WaitForMultipleObjects.argtypes = (
	DWORD,  # nCount: The number of object handles in the array
	POINTER(HANDLE),  # lpHandles: An array of object handles
	BOOL,  # bWaitAll: If TRUE, the function returns when all objects are signaled
	DWORD,  # dwMilliseconds: The time-out interval, in milliseconds
)
WaitForMultipleObjects.restype = DWORD


SleepEx = dll.SleepEx
"""
Suspends the current thread until the specified condition is met.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-sleepex
"""
SleepEx.argtypes = (
	DWORD,  # dwMilliseconds: The time interval for which execution is to be suspended
	BOOL,  # bAlertable: If TRUE, the function returns when an APC is queued
)
SleepEx.restype = DWORD


SetThreadExecutionState = dll.SetThreadExecutionState
"""
Enables an application to inform the system that it is in use.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate
"""
SetThreadExecutionState.argtypes = (
	DWORD,  # esFlags: The execution state flags
)
SetThreadExecutionState.restype = DWORD


LpoverlappedCompletionRoutine = WINFUNCTYPE(
	None,
	DWORD,  # dwErrorCode: The completion code
	DWORD,  # dwNumberOfBytesTransfered: The number of bytes transferred
	LPOVERLAPPED,  # lpOverlapped: A pointer to the OVERLAPPED structure
)
"""
An application-defined completion routine used with the ReadFileEx and WriteFileEx functions.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/minwinbase/nc-minwinbase-lpoverlapped_completion_routine
"""


ReadFileEx = dll.ReadFileEx
"""
Reads data from the specified file or input/output (I/O) device.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-readfileex
"""
ReadFileEx.argtypes = (
	HANDLE,  # hFile: A handle to the file or I/O device
	LPVOID,  # lpBuffer: A pointer to the buffer that receives the data
	DWORD,  # nNumberOfBytesToRead: The maximum number of bytes to be read
	LPOVERLAPPED,  # lpOverlapped: A pointer to an OVERLAPPED structure
	LpoverlappedCompletionRoutine,  # lpCompletionRoutine: A pointer to the completion routine
)
ReadFileEx.restype = BOOL


WriteFile = dll.WriteFile
"""
Writes data to the specified file or input/output (I/O) device.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile
"""
WriteFile.argtypes = (
	HANDLE,  # hFile: A handle to the file or I/O device
	c_void_p,  # lpBuffer: A pointer to the buffer containing the data
	DWORD,  # nNumberOfBytesToWrite: The number of bytes to be written
	POINTER(
		DWORD,
	),  # lpNumberOfBytesWritten: A pointer to the variable that receives the number of bytes written
	LPOVERLAPPED,  # lpOverlapped: A pointer to an OVERLAPPED structure
)
WriteFile.restype = BOOL


GetOverlappedResult = dll.GetOverlappedResult
"""
Retrieves the results of an overlapped operation on the specified file, named pipe, or communications device.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-getoverlappedresult
"""
GetOverlappedResult.argtypes = (
	HANDLE,  # hFile: A handle to the file, named pipe, or communications device
	LPOVERLAPPED,  # lpOverlapped: A pointer to an OVERLAPPED structure
	POINTER(
		DWORD,
	),  # lpNumberOfBytesTransferred: A pointer to a variable that receives the number of bytes transferred
	BOOL,  # bWait: If TRUE, the function does not return until the operation has been completed
)
GetOverlappedResult.restype = BOOL


CancelIoEx = dll.CancelIoEx
"""
Marks any outstanding I/O operations for the specified file handle as canceled.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-cancelioex
"""
CancelIoEx.argtypes = (
	HANDLE,  # hFile: A handle to the file
	LPOVERLAPPED,  # lpOverlapped: A pointer to an OVERLAPPED structure
)
CancelIoEx.restype = BOOL


WaitCommEvent = dll.WaitCommEvent
"""
Waits for an event to occur for a specified communications device.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-waitcommevent
"""
WaitCommEvent.argtypes = (
	HANDLE,  # hFile: A handle to the communications device
	POINTER(DWORD),  # lpEvtMask: A pointer to a variable that receives a mask indicating the type of event
	LPOVERLAPPED,  # lpOverlapped: A pointer to an OVERLAPPED structure
)
WaitCommEvent.restype = BOOL


CopyFile = dll.CopyFileW
"""
Copies an existing file to a new file.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-copyfilew
"""
CopyFile.argtypes = (
	LPCWSTR,  # lpExistingFileName: The name of an existing file
	LPCWSTR,  # lpNewFileName: The name of the new file
	BOOL,  # bFailIfExists: If TRUE, the function fails if the new file already exists
)
CopyFile.restype = BOOL


GetLocaleInfo = dll.GetLocaleInfoW
"""
Retrieves information about a locale specified by identifier.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getlocaleinfow
"""
GetLocaleInfo.argtypes = (
	LCID,  # Locale: The locale identifier for which to retrieve information
	DWORD,  # LCType: The locale information to retrieve
	LPWSTR,  # lpLCData: Pointer to a buffer in which this function retrieves the requested data
	c_int,  # cchData: Size, in characters, of the data buffer
)
GetLocaleInfo.restype = c_int


LocaleNameToLCID = dll.LocaleNameToLCID
"""
Converts a locale name to a locale identifier.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-localenametolcid
"""
LocaleNameToLCID.argtypes = (
	LPCWSTR,  # lpName: Pointer to a null-terminated string representing a locale name
	DWORD,  # dwFlags: Flags controlling the operation
)
LocaleNameToLCID.restype = LCID


GetUserDefaultUILanguage = dll.GetUserDefaultUILanguage
"""
Retrieves the language identifier for the user UI language for the current user.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getuserdefaultuilanguage
"""
GetUserDefaultUILanguage.argtypes = ()
GetUserDefaultUILanguage.restype = c_int


AttachConsole = dll.AttachConsole
"""
Attaches the calling process to the console of the specified process.

.. seealso::
	https://learn.microsoft.com/en-us/windows/console/attachconsole
"""
AttachConsole.argtypes = (
	DWORD,  # dwProcessId: The identifier of the process whose console is to be attached
)
AttachConsole.restype = BOOL


FreeConsole = dll.FreeConsole
"""
Detaches the calling process from its console.

.. seealso::
	https://learn.microsoft.com/en-us/windows/console/freeconsole
"""
FreeConsole.argtypes = ()
FreeConsole.restype = BOOL


GetConsoleWindow = dll.GetConsoleWindow
"""
Retrieves the window handle used by the console associated with the calling process.

.. seealso::
	https://learn.microsoft.com/en-us/windows/console/getconsolewindow
"""
GetConsoleWindow.argtypes = ()
GetConsoleWindow.restype = HWND


GetConsoleProcessList = dll.GetConsoleProcessList
"""
Retrieves a list of the processes attached to the current console.

.. seealso::
	https://learn.microsoft.com/en-us/windows/console/getconsoleprocesslist
"""
GetConsoleProcessList.argtypes = (
	POINTER(DWORD),  # lpdwProcessList: A pointer to a buffer that receives the list of process identifiers
	DWORD,  # dwProcessCount: The maximum number of process identifiers that can be stored
)
GetConsoleProcessList.restype = DWORD


class COORD(Structure):  # noqa: F405
	_fields_ = [
		("x", c_short),  # noqa: F405
		("y", c_short),  # noqa: F405
	]


class CONSOLE_SCREEN_BUFFER_INFO(Structure):
	_fields_ = [
		("dwSize", COORD),
		("dwCursorPosition", COORD),
		("wAttributes", WORD),
		("srWindow", SMALL_RECT),
		("dwMaximumWindowSize", COORD),
	]


class CONSOLE_SELECTION_INFO(Structure):
	_fields_ = [
		("dwFlags", DWORD),
		("dwSelectionAnchor", COORD),
		("srSelection", SMALL_RECT),
	]


class CHAR_INFO(Structure):
	_fields_ = [
		(
			"Char",
			c_wchar,
		),  # union of char and wchar_t isn't needed since we deal only with unicode  # noqa: F405
		("Attributes", WORD),
	]


PHANDLER_ROUTINE = WINFUNCTYPE(
	BOOL,
	DWORD,  # dwCtrlType: The type of control signal received
)


GetConsoleScreenBufferInfo = dll.GetConsoleScreenBufferInfo
"""
Retrieves information about the specified console screen buffer.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wincon/nf-wincon-getconsolescreenbufferinfo
"""
GetConsoleScreenBufferInfo.argtypes = (
	HANDLE,  # hConsoleOutput: A handle to the console screen buffer
	POINTER(
		CONSOLE_SCREEN_BUFFER_INFO,
	),  # lpConsoleScreenBufferInfo: A pointer to a CONSOLE_SCREEN_BUFFER_INFO structure
)
GetConsoleScreenBufferInfo.restype = BOOL


GetConsoleSelectionInfo = dll.GetConsoleSelectionInfo
"""
Retrieves information about the current console selection.

.. seealso::
	https://learn.microsoft.com/en-us/windows/console/getconsoleselectioninfo
"""
GetConsoleSelectionInfo.argtypes = (
	POINTER(
		CONSOLE_SELECTION_INFO,
	),  # lpConsoleSelectionInfo: A pointer to a CONSOLE_SELECTION_INFO structure
)
GetConsoleSelectionInfo.restype = BOOL


ReadConsoleOutputCharacter = dll.ReadConsoleOutputCharacterW
"""
Copies a number of characters from consecutive cells of a console screen buffer.

.. seealso::
	https://learn.microsoft.com/en-us/windows/console/readconsoleoutputcharacter
"""
ReadConsoleOutputCharacter.argtypes = (
	HANDLE,  # hConsoleOutput: A handle to the console screen buffer
	LPWSTR,  # lpCharacter: A pointer to a buffer that receives the characters
	DWORD,  # nLength: The number of characters to be read
	COORD,  # dwReadCoord: A COORD structure that specifies the coordinates of the first cell
	POINTER(
		DWORD,
	),  # lpNumberOfCharsRead: A pointer to a variable that receives the actual number of characters read
)
ReadConsoleOutputCharacter.restype = BOOL


ReadConsoleOutput = dll.ReadConsoleOutputW
"""
Reads character and color attribute data from a rectangular block of character cells in a console screen buffer.

.. seealso::
	https://learn.microsoft.com/en-us/windows/console/readconsoleoutput
"""
ReadConsoleOutput.argtypes = (
	HANDLE,  # hConsoleOutput: A handle to the console screen buffer
	POINTER(
		CHAR_INFO,
	),  # lpBuffer: A pointer to the destination buffer that receives the character and attribute data
	COORD,  # dwBufferSize: A COORD structure that specifies the size of the lpBuffer parameter
	COORD,  # dwBufferCoord: A COORD structure that specifies the coordinates of the upper-left cell
	POINTER(SMALL_RECT),  # lpReadRegion: A pointer to a SMALL_RECT structure
)
ReadConsoleOutput.restype = BOOL


SetConsoleCtrlHandler = dll.SetConsoleCtrlHandler
"""
Adds or removes an application-defined HandlerRoutine function from the list of handler functions.

.. seealso::
	https://learn.microsoft.com/en-us/windows/console/setconsolectrlhandler
"""
SetConsoleCtrlHandler.argtypes = (
	PHANDLER_ROUTINE,  # HandlerRoutine: A pointer to the application-defined HandlerRoutine function
	BOOL,  # Add: If TRUE, the handler is added; if FALSE, the handler is removed
)
SetConsoleCtrlHandler.restype = BOOL


GetModuleHandleEx = dll.GetModuleHandleExW
"""
Retrieves a module handle for the specified module and increments the module's reference count.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulehandleexw
"""
GetModuleHandleEx.argtypes = (
	DWORD,  # dwFlags: Flags to control the operation
	LPCWSTR,  # lpModuleName: The name of the loaded module
	POINTER(HMODULE),  # phModule: A pointer to a variable that receives a handle to the specified module
)
GetModuleHandleEx.restype = BOOL


GetPackageFullName = dll.GetPackageFullName
"""
Gets the package full name for the specified process.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/appmodel/nf-appmodel-getpackagefullname
"""
GetPackageFullName.argtypes = (
	HANDLE,  # hProcess: A handle to the process
	POINTER(c_uint),  # packageFullNameLength: On input, the size of the packageFullName buffer
	LPWSTR,  # packageFullName: The package full name
)
GetPackageFullName.restype = LONG


GetCurrentPackageFullName = dll.GetCurrentPackageFullName
"""
Retrieves the package full name for the current process.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/appmodel/nf-appmodel-getcurrentpackagefullname
"""
GetCurrentPackageFullName.argtypes = (
	POINTER(c_uint),  # packageFullNameLength: On input, the size of the packageFullName buffer
	LPWSTR,  # packageFullName: The package full name
)
GetCurrentPackageFullName.restype = LONG


QueryFullProcessImageName = dll.QueryFullProcessImageNameW
"""
Retrieves the full name of the executable image for the specified process.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-queryfullprocessimagenamew
"""
QueryFullProcessImageName.argtypes = (
	HANDLE,  # hProcess: A handle to the process
	DWORD,  # dwFlags: Flags that control the operation
	LPWSTR,  # lpExeName: The path to the executable image
	POINTER(DWORD),  # lpdwSize: On input, specifies the size of the lpExeName buffer
)
QueryFullProcessImageName.restype = BOOL


IsWow64Process = dll.IsWow64Process
"""
Determines whether the specified process is running under WOW64.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wow64apiset/nf-wow64apiset-iswow64process
"""
IsWow64Process.argtypes = (
	HANDLE,  # hProcess: A handle to the process
	POINTER(
		BOOL,
	),  # Wow64Process: A pointer to a value that is set to TRUE if the process is running under WOW64
)
IsWow64Process.restype = BOOL


IsWow64Process2 = dll.IsWow64Process2
"""
Determines whether the specified process is running under WOW64; also returns additional machine process information.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wow64apiset/nf-wow64apiset-iswow64process2
"""
IsWow64Process2.argtypes = (
	HANDLE,  # hProcess: A handle to the process
	POINTER(c_ushort),  # pProcessMachine: On success, returns a pointer to the machine architecture
	POINTER(c_ushort),  # pNativeMachine: On success, returns a pointer to the native machine architecture
)
IsWow64Process2.restype = BOOL


class _PROCESS_MACHINE_INFORMATION(Structure):
	_fields_ = [
		("ProcessMachine", USHORT),
		("Res0", USHORT),
		("MachineAttributes", DWORD),
	]


GetProcessInformation = dll.GetProcessInformation
"""
Retrieves information about the specified process.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocessinformation
"""
GetProcessInformation.argtypes = (
	HANDLE,  # hProcess: A handle to the process
	DWORD,  # ProcessInformationClass: The type of process information to be retrieved
	POINTER(
		_PROCESS_MACHINE_INFORMATION
	),  # ProcessInformation: A pointer to a buffer to receive the process information
	DWORD,  # ProcessInformationLength: The size of the buffer pointed to by the ProcessInformation parameter
)
GetProcessInformation.restype = BOOL


CreateToolhelp32Snapshot = dll.CreateToolhelp32Snapshot
"""
Takes a snapshot of the specified processes, as well as the heaps, modules, and threads used by these processes.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot
"""
CreateToolhelp32Snapshot.argtypes = (
	DWORD,  # dwFlags: The portions of the system to be included in the snapshot
	DWORD,  # th32ProcessID: The process identifier of the process to be included in the snapshot
)
CreateToolhelp32Snapshot.restype = HANDLE


class PROCESSENTRY32W(Structure):
	"""See https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-processentry32w"""

	_fields_ = [
		("dwSize", DWORD),
		("cntUsage", DWORD),
		("th32ProcessID", DWORD),
		("th32DefaultHeapID", PULONG),
		("th32ModuleID", DWORD),
		("cntThreads", DWORD),
		("th32ParentProcessID", DWORD),
		("pcPriClassBase", c_long),
		("dwFlags", DWORD),
		("szExeFile", c_wchar * 260),
	]


Process32First = dll.Process32FirstW
"""
Retrieves information about the first process encountered in a system snapshot.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-process32firstw
"""
Process32First.argtypes = (
	HANDLE,  # hSnapshot: A handle to the snapshot returned from CreateToolhelp32Snapshot
	POINTER(PROCESSENTRY32W),  # lppe: A pointer to a PROCESSENTRY32 structure
)
Process32First.restype = BOOL

Process32Next = dll.Process32NextW
"""
Retrieves information about the next process recorded in a system snapshot.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-process32nextw
"""
Process32Next.argtypes = (
	HANDLE,  # hSnapshot: A handle to the snapshot returned from CreateToolhelp32Snapshot
	POINTER(PROCESSENTRY32W),  # lppe: A pointer to a PROCESSENTRY32 structure
)
Process32Next.restype = BOOL


RegisterApplicationRestart = dll.RegisterApplicationRestart
"""
Registers the active instance of an application for restart.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-registerapplicationrestart
"""
RegisterApplicationRestart.argtypes = (
	LPCWSTR,  # pwzCommandline: A pointer to a Unicode string that specifies the command line arguments
	DWORD,  # dwFlags: Flags that control restart operations
)
RegisterApplicationRestart.restype = HRESULT


GetLastError = dll.GetLastError
"""
Retrieves the calling thread's last-error code value.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror
"""
GetLastError.argtypes = ()
GetLastError.restype = DWORD


GetStdHandle = dll.GetStdHandle
"""
Retrieves a handle to the specified standard device.

.. seealso::
	https://learn.microsoft.com/en-us/windows/console/getstdhandle
"""
GetStdHandle.argtypes = (
	DWORD,  # nStdHandle: The standard device
)
GetStdHandle.restype = HANDLE


CreateFile = dll.CreateFileW
"""
Creates or opens a file or I/O device.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew
"""
CreateFile.argtypes = (
	LPCWSTR,  # lpFileName: The name of the file or device to be created or opened
	DWORD,  # dwDesiredAccess: The requested access to the file or device
	DWORD,  # dwShareMode: The requested sharing mode of the file or device
	POINTER(SECURITY_ATTRIBUTES),  # lpSecurityAttributes: A pointer to a SECURITY_ATTRIBUTES structure
	DWORD,  # dwCreationDisposition: An action to take on a file or device that exists or does not exist
	DWORD,  # dwFlagsAndAttributes: The file or device attributes and flags
	HANDLE,  # hTemplateFile: A valid handle to a template file with the GENERIC_READ access right
)
CreateFile.restype = HANDLE


class SYSTEM_POWER_STATUS(Structure):
	# https://docs.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-system_power_status
	_fields_ = [
		("ACLineStatus", c_byte),
		("BatteryFlag", c_byte),
		("BatteryLifePercent", c_byte),
		("Reserved1", c_byte),
		("BatteryLifeTime", DWORD),
		("BatteryFullLiveTime", DWORD),
	]


GetSystemPowerStatus = dll.GetSystemPowerStatus
"""
Retrieves the power status of the system.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getsystempowerstatus
"""
GetSystemPowerStatus.argtypes = (
	c_void_p,  # lpSystemPowerStatus: A pointer to a SYSTEM_POWER_STATUS structure
)
GetSystemPowerStatus.restype = BOOL


GetThreadLocale = dll.GetThreadLocale
"""
Returns the locale identifier for the current thread.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getthreadlocale
"""
GetThreadLocale.argtypes = ()
GetThreadLocale.restype = LCID


Wow64DisableWow64FsRedirection = dll.Wow64DisableWow64FsRedirection
"""
Disables file system redirection for the calling thread.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wow64apiset/nf-wow64apiset-wow64disablewow64fsredirection
"""
Wow64DisableWow64FsRedirection.argtypes = (
	c_void_p,  # OldValue: The WOW64 file system redirection value
)
Wow64DisableWow64FsRedirection.restype = BOOL


Wow64RevertWow64FsRedirection = dll.Wow64RevertWow64FsRedirection
"""
Restores file system redirection for the calling thread.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wow64apiset/nf-wow64apiset-wow64revertwow64fsredirection
"""
Wow64RevertWow64FsRedirection.argtypes = (
	LPVOID,  # OldValue: The WOW64 file system redirection value
)
Wow64RevertWow64FsRedirection.restype = BOOL


class SYSTEMTIME(Structure):
	_fields_ = (
		("wYear", WORD),
		("wMonth", WORD),
		("wDayOfWeek", WORD),
		("wDay", WORD),
		("wHour", WORD),
		("wMinute", WORD),
		("wSecond", WORD),
		("wMilliseconds", WORD),
	)


class FILETIME(Structure):
	_fields_ = (
		("dwLowDateTime", DWORD),
		("dwHighDateTime", DWORD),
	)


FileTimeToSystemTime = dll.FileTimeToSystemTime
"""
Converts a file time to system time format.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/timezoneapi/nf-timezoneapi-filetimetosystemtime
"""
FileTimeToSystemTime.argtypes = (
	POINTER(FILETIME),  # lpFileTime: A pointer to a FILETIME structure
	POINTER(SYSTEMTIME),  # lpSystemTime: A pointer to a SYSTEMTIME structure
)
FileTimeToSystemTime.restype = BOOL


class TIME_ZONE_INFORMATION(Structure):
	_fields_ = (
		("Bias", LONG),
		("StandardName", WCHAR * 32),
		("StandardDate", SYSTEMTIME),
		("StandardBias", LONG),
		("DaylightName", WCHAR * 32),
		("DaylightDate", SYSTEMTIME),
		("DaylightBias", LONG),
	)


SystemTimeToTzSpecificLocalTime = dll.SystemTimeToTzSpecificLocalTime
"""
Converts a time in Coordinated Universal Time (UTC) to a specified time zone's corresponding local time.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/timezoneapi/nf-timezoneapi-systemtimetotzspecificlocaltime
"""
SystemTimeToTzSpecificLocalTime.argtypes = (
	POINTER(TIME_ZONE_INFORMATION),  # lpTimeZoneInformation: A pointer to a TIME_ZONE_INFORMATION structure
	POINTER(SYSTEMTIME),  # lpUniversalTime: A pointer to a SYSTEMTIME structure
	POINTER(SYSTEMTIME),  # lpLocalTime: A pointer to a SYSTEMTIME structure
)
SystemTimeToTzSpecificLocalTime.restype = BOOL


GetDateFormatEx = dll.GetDateFormatEx
"""
Formats a date as a date string for a locale specified by name.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/datetimeapi/nf-datetimeapi-getdateformatex
"""
GetDateFormatEx.argtypes = (
	LPCWSTR,  # lpLocaleName: Pointer to a locale name
	DWORD,  # dwFlags: Flags specifying various function options
	POINTER(SYSTEMTIME),  # lpDate: Pointer to a SYSTEMTIME structure
	LPCWSTR,  # lpFormat: Pointer to a format picture string
	LPWSTR,  # lpDateStr: Pointer to a buffer to receive the formatted date string
	c_int,  # cchDate: Size, in characters, of the lpDateStr buffer
	LPCWSTR,  # lpCalendar: Reserved; must be NULL
)
GetDateFormatEx.restype = c_int


GetTimeFormatEx = dll.GetTimeFormatEx
"""
Formats time as a time string for a locale specified by name.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/datetimeapi/nf-datetimeapi-gettimeformatex
"""
GetTimeFormatEx.argtypes = (
	LPCWSTR,  # lpLocaleName: Pointer to a locale name
	DWORD,  # dwFlags: Flags specifying various function options
	POINTER(SYSTEMTIME),  # lpTime: Pointer to a SYSTEMTIME structure
	LPCWSTR,  # lpFormat: Pointer to a format picture string
	LPWSTR,  # lpTimeStr: Pointer to a buffer to receive the formatted time string
	c_int,  # cchTime: Size, in characters, of the lpTimeStr buffer
)
GetTimeFormatEx.restype = c_int


WaitForSingleObjectEx = dll.WaitForSingleObjectEx
"""
Waits until the specified object is in the signaled state, an I/O completion routine or APC is queued, or the time-out interval elapses.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobjectex
"""
WaitForSingleObjectEx.argtypes = (
	HANDLE,  # hHandle: A handle to the object
	DWORD,  # dwMilliseconds: The time-out interval, in milliseconds
	BOOL,  # bAlertable: If TRUE, the function returns when the system queues an APC
)
WaitForSingleObjectEx.restype = DWORD


SetProcessShutdownParameters = dll.SetProcessShutdownParameters
"""
Sets shutdown parameters for the currently calling process.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setprocessshutdownparameters
"""
SetProcessShutdownParameters.argtypes = (
	DWORD,  # dwLevel: The shutdown priority for the process relative to other processes
	DWORD,  # dwFlags: This parameter can be the following value
)
SetProcessShutdownParameters.restype = BOOL


GetExitCodeProcess = dll.GetExitCodeProcess
"""
Retrieves the termination status of the specified process.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getexitcodeprocess
"""
GetExitCodeProcess.argtypes = (
	HANDLE,  # hProcess: A handle to the process
	POINTER(DWORD),  # lpExitCode: A pointer to a variable to receive the process termination status
)
GetExitCodeProcess.restype = BOOL


TerminateProcess = dll.TerminateProcess
"""
Terminates the specified process and all of its threads.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess
"""
TerminateProcess.argtypes = (
	HANDLE,  # hProcess: A handle to the process to be terminated
	UINT,  # uExitCode: The exit code to be used by the process and threads terminated as a result of this call
)
TerminateProcess.restype = BOOL


GetDriveType = dll.GetDriveTypeW
"""
Determines whether a disk drive is a removable, fixed, CD-ROM, RAM disk, or network drive.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getdrivetypew
"""
GetDriveType.argtypes = (
	LPCWSTR,  # lpRootPathName: The root directory of the disk to be examined
)
GetDriveType.restype = UINT


CreatePipe = dll.CreatePipe
"""
Creates an anonymous pipe and returns handles to the read and write ends of the pipe.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-createpipe
"""
CreatePipe.argtypes = (
	POINTER(HANDLE),  # hReadPipe: A pointer to a variable that receives the read handle for the pipe
	POINTER(HANDLE),  # hWritePipe: A pointer to a variable that receives the write handle for the pipe
	POINTER(SECURITY_ATTRIBUTES),  # lpPipeAttributes: A pointer to a SECURITY_ATTRIBUTES structure
	DWORD,  # nSize: The size of the buffer for the pipe, in bytes
)
CreatePipe.restype = BOOL


MoveFileEx = dll.MoveFileExW
"""
Moves an existing file or directory, including its children, with various move options.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw
"""
MoveFileEx.argtypes = (
	LPCWSTR,  # lpExistingFileName: The current name of the file or directory
	LPCWSTR,  # lpNewFileName: The new name for the file or directory
	DWORD,  # dwFlags: This parameter can be one or more of the following values
)
MoveFileEx.restype = BOOL


LCIDToLocaleName = dll.LCIDToLocaleName
"""
Converts a locale identifier to a locale name.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-lcidtolocalename
"""
LCIDToLocaleName.argtypes = (
	LCID,  # Locale: The locale identifier to convert
	LPWSTR,  # lpName: Pointer to a buffer in which this function retrieves the locale name
	c_int,  # cchName: Size, in characters, of the locale name buffer
	DWORD,  # dwFlags: Flags controlling the operation
)
LCIDToLocaleName.restype = c_int


GetLocaleInfoEx = dll.GetLocaleInfoEx
"""
Retrieves information about a locale specified by name.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getlocaleinfoex
"""
GetLocaleInfoEx.argtypes = (
	LPCWSTR,  # lpLocaleName: Pointer to a locale name
	DWORD,  # LCType: The locale information to retrieve
	LPWSTR,  # lpLCData: Pointer to a buffer in which this function retrieves the requested data
	c_int,  # cchData: Size, in characters, of the data buffer
)
GetLocaleInfoEx.restype = c_int


GetACP = dll.GetACP
"""
Retrieves the current Windows ANSI code page identifier.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getacp
"""
GetACP.argtypes = ()
GetACP.restype = UINT

SetThreadLocale = dll.SetThreadLocale
"""
Sets the locale identifier for the current thread.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-setthreadlocale
"""
SetThreadLocale.argtypes = (
	LCID,  # Locale: The locale identifier to be set for the current thread
)
SetThreadLocale.restype = BOOL


GetApplicationUserModelId = dll.GetApplicationUserModelId
"""
Retrieves the application user model ID for the specified process.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/appmodel/nf-appmodel-getapplicationusermodelid
"""
GetApplicationUserModelId.argtypes = (
	HANDLE,  # hProcess: A handle to the process
	POINTER(DWORD),  # AppUserModelIDLength: On input, the size of the AppUserModelID buffer
	LPWSTR,  # AppUserModelID: The application user model ID string
)
GetApplicationUserModelId.restype = LONG

GetOEMCP = dll.GetOEMCP
"""
Retrieves the current OEM code page identifier.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getoemcp
"""
GetOEMCP.argtypes = ()
GetOEMCP.restype = UINT
