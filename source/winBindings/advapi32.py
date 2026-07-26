# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by advapi32.dll, and supporting data structures and enumerations."""

from ctypes import (
	WINFUNCTYPE,
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
	PDWORD,
	WORD,
	HANDLE,
	HKEY,
	LONG,
	LPCWSTR,
	LPWSTR,
	LPVOID,
)
from enum import IntEnum, IntFlag, StrEnum

__all__ = (
	"OpenProcessToken",
	"RegCloseKey",
	"RegDeleteTree",
	"RegOpenKeyEx",
	"RegQueryValueEx",
	"CreateProcessAsUser",
	"GetTokenInformation",
)


dll = windll.advapi32


class TokenAccessRight(IntEnum):
	"""
	The specific access rights for access tokens.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/secauthz/access-rights-for-access-token-objects
	"""

	QUERY = 0x0008
	"""TOKEN_QUERY: Required to query an access token."""
	ADJUST_PRIVILEGES = 0x0020
	"""TOKEN_ADJUST_PRIVILEGES: Required to enable or disable the privileges in an access token."""


OpenProcessToken = WINFUNCTYPE(None)(("OpenProcessToken", dll))
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

RegCloseKey = WINFUNCTYPE(None)(("RegCloseKey", dll))
"""
Closes a handle to the specified registry key.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regclosekey
"""
RegCloseKey.argtypes = (
	HKEY,  # hKey
)
RegCloseKey.restype = LONG

RegDeleteTree = WINFUNCTYPE(None)(("RegDeleteTreeW", dll))
"""
Deletes a subkey and all its descendants.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-RegDeleteTree

.. note::
	This function can be replaced with ``winreg.DeleteTree`` in python 3.14.
	https://github.com/python/cpython/pull/138388
"""
RegDeleteTree.argtypes = (
	HKEY,  # hKey
	LPCWSTR,  # lpSubKey
)
RegDeleteTree.restype = LONG

RegOpenKeyEx = WINFUNCTYPE(None)(("RegOpenKeyExW", dll))
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

RegQueryValueEx = WINFUNCTYPE(None)(("RegQueryValueExW", dll))
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


CreateProcessAsUser = WINFUNCTYPE(None)(("CreateProcessAsUserW", dll))
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


class TOKEN_INFORMATION_CLASS(IntEnum):
	"""
	Specifies the type of information being assigned to or retrieved from an access token.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-token_information_class
	"""

	ELEVATION_TYPE = 18
	"""The buffer receives a TOKEN_ELEVATION_TYPE value that specifies the elevation level of the token."""


class TOKEN_ELEVATION_TYPE(IntEnum):
	"""
	Indicates the elevation type of an access token.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-token_elevation_type
	"""

	DEFAULT = 1
	"""The token does not have a linked token."""

	FULL = 2
	"""The token is an elevated token."""

	LIMITED = 3
	"""The token is a limited token."""


GetTokenInformation = WINFUNCTYPE(None)(("GetTokenInformation", dll))
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


class SE_PRIVILEGE(IntFlag):
	"""Possible attributes of privilege in a TOKEN_PRIVILEGES structure."""

	ENABLED_BY_DEFAULT = 0x00000001
	"""SE_PRIVILEGE_ENABLED_BY_DEFAULT: The privilege is enabled by default."""
	ENABLED = 0x00000002
	"""SE_PRIVILEGE_ENABLED: The privilege is enabled."""
	REMOVED = 0x00000004
	"""SE_PRIVILEGE_REMOVED: Used to remove a privilege."""
	USED_FOR_ACCESS = 0x80000000
	"""SE_PRIVILEGE_USED_FOR_ACCESS: The privilege was used to gain access to an object or service."""


class LUID(Structure):
	"""Describes a local identifier for an adapter.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-luid
	"""

	_fields_ = (
		("LowPart", DWORD),
		("HighPart", LONG),
	)


PLUID = POINTER(LUID)


class LUID_AND_ATTRIBUTES(Structure):
	"""Represents a locally unique identifier (LUID) and its attributes.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-luid_and_attributes
	"""

	_fields_ = (
		("Luid", LUID),
		("Attributes", DWORD),
	)


class TOKEN_PRIVILEGES(Structure):
	"""Contains information about a set of privileges for an access token.

	.. warning::
		To create this array with more than one element, you must allocate sufficient memory for the structure to take into account additional elements.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_privileges
	"""

	_fields_ = (
		("PrivilegeCount", DWORD),
		("Privileges", LUID_AND_ATTRIBUTES * 1),
	)


PTOKEN_PRIVILEGES = POINTER(TOKEN_PRIVILEGES)

AdjustTokenPrivileges = WINFUNCTYPE(None)(("AdjustTokenPrivileges", dll))
"""Enables, disables or removes privileges in an access token.

.. note::
	Enabling or disabling privileges in an access token requires TOKEN_ADJUST_PRIVILEGES access.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-adjusttokenprivileges
"""
AdjustTokenPrivileges.restype = BOOL
AdjustTokenPrivileges.argtypes = (
	HANDLE,  # TokenHandle: A handle to the access token that contains the privileges to be modified.
	BOOL,  # DisableAllPrivileges: Specifies whether to disable all of the token's privileges, or modify them based on the NewState parameter.
	PTOKEN_PRIVILEGES,  # NewState: Specifies an array of privileges and their attributes. Only used if DisableAllPrivileges is FALSE.
	DWORD,  # BufferLength: The size, in bytes, of the buffer pointed to by the PreviousState parameter.
	PTOKEN_PRIVILEGES,  # PreviousState: Optional pointer to a buffer to be filled with the the previous state of any privileges that were modified.
	PDWORD,  # ReturnLength: Optional pointer to a variable that receives the required size, in bytes, of the buffer pointed to by the PreviousState parameter.
)


class PrivilegeName(StrEnum):
	"""Privilege constants for use with the LookupPrivilegeValue function.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/secauthz/privilege-constants
	"""

	SHUTDOWN = "SeShutdownPrivilege"
	"""SE_SHUTDOWN_NAME: Required to shut down a local system."""


LookupPrivilegeValue = WINFUNCTYPE(None)(("LookupPrivilegeValueW", dll))
LookupPrivilegeValue.restype = BOOL
LookupPrivilegeValue.argtypes = (
	LPCWSTR,  # lpSystemName: The name of the system on which the privilege name is retrieved, or null to find the privilege name on the local system.
	LPCWSTR,  # lpName: The name of the privilege, as defined in Winnt.h.
	PLUID,  # lpLuid: Receives the LUID by which the privilege is known on the specified system.
)
