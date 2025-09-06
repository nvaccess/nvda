# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by shell32.dll, and supporting data structures and enumerations."""

from ctypes import (
	POINTER,
	sizeof,
	Structure,
	c_long,
	c_int,
	c_uint,
	c_void_p,
	c_wchar_p,
	windll,
)
from ctypes.wintypes import (
	LPCVOID,
	ULONG,
	BOOL,
	HANDLE,
	LPVOID,
	DWORD,
	HINSTANCE,
	HKEY,
	HWND,
	INT,
	LPCWSTR,
)
from comtypes import (
	GUID,
	HRESULT,
)


dll = windll.shell32


IsUserAnAdmin = dll.IsUserAnAdmin
"""
Tests whether the current user is a member of the Administrator's group.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/shlobj_core/nf-shlobj_core-isuseranadmin
"""
IsUserAnAdmin.restype = BOOL
IsUserAnAdmin.argtypes = ()

SHGetKnownFolderPath = dll.SHGetKnownFolderPath
"""
Retrieves the full path of a known folder identified by the folder's KNOWNFOLDERID.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/shlobj_core/nf-shlobj_core-shgetknownfolderpath
"""
SHGetKnownFolderPath.restype = HRESULT
SHGetKnownFolderPath.argtypes = (
	POINTER(GUID),  # rfid: Reference to the KNOWNFOLDERID that identifies the folder
	DWORD,  # dwFlags: Flags that specify special retrieval options
	HANDLE,  # hToken: Access token that represents a particular user (can be NULL)
	POINTER(c_wchar_p),  # ppszPath: Address of a pointer to a null-terminated Unicode string
)

ShellExecute = dll.ShellExecuteW
"""
Performs an operation on a specified file.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecutew
"""
ShellExecute.restype = c_void_p  # Returns HINSTANCE (handle)
ShellExecute.argtypes = (
	HWND,  # hwnd: Handle to the parent window
	LPCWSTR,  # lpOperation: String that specifies the operation to perform (can be NULL)
	LPCWSTR,  # lpFile: String that specifies the file or object on which to execute
	LPCWSTR,  # lpParameters: String that specifies the parameters to be passed (can be NULL)
	LPCWSTR,  # lpDirectory: String that specifies the default directory (can be NULL)
	INT,  # nShowCmd: Flags that specify how an application is to be displayed
)


class SHELLEXECUTEINFOW(Structure):
	"""
	Contains information used by ShellExecuteEx.

	..seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/shellapi/ns-shellapi-shellexecuteinfow
	"""

	_fields_ = (
		("cbSize", DWORD),
		("fMask", ULONG),
		("hwnd", HWND),
		("lpVerb", LPCWSTR),
		("lpFile", LPCWSTR),
		("lpParameters", LPCWSTR),
		("lpDirectory", LPCWSTR),
		("nShow", c_int),
		("hInstApp", HINSTANCE),
		("lpIDList", LPVOID),
		("lpClass", LPCWSTR),
		("hkeyClass", HKEY),
		("dwHotKey", DWORD),
		("hIconOrMonitor", HANDLE),
		("hProcess", HANDLE),
	)

	def __init__(self, **kwargs):
		super(SHELLEXECUTEINFOW, self).__init__(cbSize=sizeof(self), **kwargs)


SHELLEXECUTEINFO = SHELLEXECUTEINFOW

ShellExecuteEx = dll.ShellExecuteExW
"""
Performs an operation on a specified file with extended options.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecuteexw
"""
ShellExecuteEx.restype = BOOL
ShellExecuteEx.argtypes = (
	POINTER(SHELLEXECUTEINFOW),  # pExecInfo: Pointer to a SHELLEXECUTEINFO structure
)

SHChangeNotify = dll.SHChangeNotify
"""
Notifies the system of an event that an application has performed.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/shlobj_core/nf-shlobj_core-shchangenotify
"""
SHChangeNotify.restype = None
SHChangeNotify.argtypes = (
	c_long,  # wEventId: Describes the event that has occurred
	c_uint,  # uFlags: Flags that indicate the meaning of the dwItem1 and dwItem2 parameters
	LPCVOID,  # dwItem1: Optional first item identifier
	LPCVOID,  # dwItem2: Optional second item identifier
)
