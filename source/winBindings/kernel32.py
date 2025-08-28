# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by kernel32.dll, and supporting data structures and enumerations."""

from ctypes import (
	WINFUNCTYPE,
	c_void_p,
	c_wchar_p,
	windll,
	POINTER,
	c_size_t,
)
from ctypes.wintypes import (
	DWORD,
	UINT,
	HANDLE,
	HMODULE,
	LPCWSTR,
	BOOL,
	LPVOID,
	HGLOBAL,
)

__all__ = (
	"GetModuleHandle",
	"GetModuleFileName",
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
