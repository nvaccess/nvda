# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions exported by kernel32.dll, and supporting data structures and enumerations."""

from ctypes import (
	c_wchar_p,
	windll,
)
from ctypes.wintypes import (
	DWORD,
	HANDLE,
	HMODULE,
	LPCWSTR,
	BOOL,
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

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulefilenamew
"""
GetModuleFileName.argtypes = (HANDLE, c_wchar_p, DWORD)
GetModuleFileName.restype = DWORD

LoadLibraryEx = dll.LoadLibraryExW
"""
Loads the specified module into the address space of the calling process. The specified module may cause other modules to be loaded.

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
Frees the loaded module and decrements its reference count. If the reference count reaches zero, the module is unloaded from the address space of the calling process.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-freelibrary
"""
FreeLibrary.argtypes = (HMODULE,)
FreeLibrary.restype = BOOL
