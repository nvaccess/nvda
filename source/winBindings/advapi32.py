# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by advapi32.dll, and supporting data structures and enumerations."""

from ctypes import (
	sizeof,
	Structure,
	POINTER,
	windll,
	c_void_p,
	c_byte,
)
from ctypes.wintypes import (
	BOOL,
	DWORD,
	WORD,
	HANDLE,
	HKEY,
	LONG,
	LPCWSTR,
	LPWSTR,
	LPVOID,
)

__all__ = (
	"OpenProcessToken",
	"RegCloseKey",
	"RegOpenKeyEx",
	"RegQueryValueEx",
	"CreateProcessAsUser",
	"GetTokenInformation",
)


dll = windll.advapi32


OpenProcessToken = dll.OpenProcessToken
"""
Opens the access token associated with a process.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocesstoken
"""
OpenProcessToken.argtypes = (
	HANDLE,  # ProcessHandle
	DWORD,  # DesiredAccess
	POINTER(HANDLE),  # TokenHandle
)
OpenProcessToken.restype = BOOL

RegCloseKey = dll.RegCloseKey
"""
Closes a handle to the specified registry key.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regclosekey
"""
RegCloseKey.argtypes = (
	HKEY,  # hKey
)
RegCloseKey.restype = LONG

RegOpenKeyEx = dll.RegOpenKeyExW
"""
Opens the specified registry key.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regopenkeyexw
"""
RegOpenKeyEx.argtypes = (
	HKEY,  # hKey
	LPCWSTR,  # lpSubKey
	DWORD,  # ulOptions
	DWORD,  # samDesired
	POINTER(HKEY),  # phkResult
)
RegOpenKeyEx.restype = LONG

RegQueryValueEx = dll.RegQueryValueExW
"""
Retrieves the type and data for a specified value name associated with an open registry key.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regqueryvalueexw
"""
RegQueryValueEx.argtypes = (
	HKEY,  # hKey
	LPCWSTR,  # lpValueName
	POINTER(DWORD),  # lpReserved
	POINTER(DWORD),  # lpType
	c_void_p,  # lpData
	POINTER(DWORD),  # lpcbData
)
RegQueryValueEx.restype = LONG


class STARTUPINFOW(Structure):
	"""
	Specifies the window station, desktop, standard handles, and appearance of the main window for a process at creation time.

	..seealso:
		https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfow
	"""

	_fields_ = (
		("cb", DWORD),
		("lpReserved", LPWSTR),
		("lpDesktop", LPWSTR),
		("lpTitle", LPWSTR),
		("dwX", DWORD),
		("dwY", DWORD),
		("dwXSize", DWORD),
		("dwYSize", DWORD),
		("dwXCountChars", DWORD),
		("dwYCountChars", DWORD),
		("dwFillAttribute", DWORD),
		("dwFlags", DWORD),
		("wShowWindow", WORD),
		("cbReserved2", WORD),
		("lpReserved2", POINTER(c_byte)),
		("hSTDInput", HANDLE),
		("hSTDOutput", HANDLE),
		("hSTDError", HANDLE),
	)

	def __init__(self, **kwargs):
		super(STARTUPINFOW, self).__init__(cb=sizeof(self), **kwargs)


STARTUPINFO = STARTUPINFOW


class PROCESS_INFORMATION(Structure):
	"""
	Contains information about a newly created process and its primary thread.

	..seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-process_information
	"""

	_fields_ = (
		("hProcess", HANDLE),
		("hThread", HANDLE),
		("dwProcessID", DWORD),
		("dwThreadID", DWORD),
	)


class SECURITY_ATTRIBUTES(Structure):
	"""
	Contains the security descriptor for an object and specifies whether the handle retrieved by specifying this structure is inheritable.

	..seealso::
		https://learn.microsoft.com/en-us/previous-versions/windows/desktop/legacy/aa379560(v=vs.85)
	"""

	_fields_ = (
		("nLength", DWORD),
		("lpSecurityDescriptor", LPVOID),
		("bInheritHandle", BOOL),
	)


CreateProcessAsUser = dll.CreateProcessAsUserW
"""
Creates a new process and its primary thread. The new process runs in the security context of the user represented by the specified token.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasuserw
"""
CreateProcessAsUser.argtypes = (
	HANDLE,  # hToken
	LPCWSTR,  # lpApplicationName
	LPWSTR,  # lpCommandLine
	POINTER(SECURITY_ATTRIBUTES),  # lpProcessAttributes
	POINTER(SECURITY_ATTRIBUTES),  # lpThreadAttributes
	BOOL,  # bInheritHandles
	DWORD,  # dwCreationFlags
	LPVOID,  # lpEnvironment
	LPCWSTR,  # lpCurrentDirectory
	POINTER(STARTUPINFOW),  # lpStartupInfo
	POINTER(PROCESS_INFORMATION),  # lpProcessInformation
)
CreateProcessAsUser.restype = BOOL

GetTokenInformation = dll.GetTokenInformation
"""
Retrieves a specified type of information about an access token.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-gettokeninformation
"""
GetTokenInformation.argtypes = (
	HANDLE,  # TokenHandle
	DWORD,  # TOKEN_INFORMATION_CLASS
	LPVOID,  # TokenInformation
	DWORD,  # TokenInformationLength
	POINTER(DWORD),  # ReturnLength
)
GetTokenInformation.restype = BOOL
