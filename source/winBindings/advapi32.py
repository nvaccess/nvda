# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
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
	WORD,
	HANDLE,
	HKEY,
	LONG,
	LPCWSTR,
	LPWSTR,
	LPVOID,
)
from .winnt import (
	SECURITY_ATTRIBUTES,
	STARTUPINFOW,
	STARTUPINFO,
	PROCESS_INFORMATION,
	SID_AND_ATTRIBUTES,
	LUID_AND_ATTRIBUTES,
)


__all__ = (
	"OpenProcessToken",
	"RegCloseKey",
	"RegDeleteTree",
	"RegOpenKeyEx",
	"RegQueryValueEx",
	"CreateProcessAsUser",
	"GetTokenInformation",
	"SetTokenInformation",  # added export
	"ConvertStringSidToSid",
	"ConvertSidToStringSid",
	"CreateWellKnownSid",  # added export
)


dll = windll.advapi32


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

CreateProcessWithToken = WINFUNCTYPE(None)(("CreateProcessWithTokenW", dll))
"""
Creates a new process and its primary thread. The new process runs in the security context of the user represented by the specified token.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithtokenw
"""
CreateProcessWithToken.argtypes = (
	HANDLE,  # hToken
	DWORD,  # dwLogonFlags
	LPCWSTR,  # lpApplicationName
	LPWSTR,  # lpCommandLine
	DWORD,  # dwCreationFlags
	LPVOID,  # lpEnvironment
	LPCWSTR,  # lpCurrentDirectory
	POINTER(STARTUPINFOW),  # lpStartupInfo
	POINTER(PROCESS_INFORMATION),  # lpProcessInformation
)
CreateProcessWithToken.restype = BOOL

LogonUser = WINFUNCTYPE(None)(("LogonUserW", dll))
"""
Attempts to log a user on to the local computer.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-logonuserw
"""
LogonUser.argtypes = (
	LPCWSTR,  # lpszUsername
	LPCWSTR,  # lpszDomain
	LPCWSTR,  # lpszPassword
	DWORD,    # dwLogonType
	DWORD,    # dwLogonProvider
	POINTER(HANDLE),  # phToken
)
LogonUser.restype = BOOL

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

SetTokenInformation = WINFUNCTYPE(None)(("SetTokenInformation", dll))
"""
Sets specified types of information for an access token.
.. seealso:: https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-settokeninformation
"""
SetTokenInformation.argtypes = (
	HANDLE,  # TokenHandle
	DWORD,   # TOKEN_INFORMATION_CLASS
	LPVOID,  # TokenInformation
	DWORD,   # TokenInformationLength
)
SetTokenInformation.restype = BOOL

DuplicateTokenEx = WINFUNCTYPE(None)(("DuplicateTokenEx", dll))
"""
Creates a new access token that duplicates an existing token.
.. seealso:: https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-duplicatetokenex
"""
DuplicateTokenEx.argtypes = (
	HANDLE,  # hExistingToken
	DWORD,   # dwDesiredAccess
	POINTER(SECURITY_ATTRIBUTES),  # lpTokenAttributes
	DWORD,   # ImpersonationLevel (SECURITY_IMPERSONATION_LEVEL)
	DWORD,   # TokenType (TOKEN_TYPE)
	POINTER(HANDLE),  # phNewToken
)
DuplicateTokenEx.restype = BOOL

PSID = LPVOID

# Add ConvertStringSidToSid and ConvertSidToStringSid bindings
ConvertStringSidToSid = WINFUNCTYPE(None)(("ConvertStringSidToSidW", dll))
"""
Converts a string-format security identifier (SID) into a valid SID structure.
.. seealso:: https://learn.microsoft.com/en-us/windows/win32/api/sddl/nf-sddl-convertstringsidtosisw
"""
# LPCWSTR StringSid, PSID *Sid
ConvertStringSidToSid.argtypes = (
	LPCWSTR,            # StringSid
	POINTER(PSID ),    # Sid (PSID*) -> pointer to allocated PSID
)
ConvertStringSidToSid.restype = BOOL

ConvertSidToStringSid = WINFUNCTYPE(None)(("ConvertSidToStringSidW", dll))
"""
Converts a valid SID to a string-format SID.
.. seealso:: https://learn.microsoft.com/en-us/windows/win32/api/sddl/nf-sddl-convertsidtostringsidw
"""
# PSID Sid, LPWSTR *StringSid
ConvertSidToStringSid.argtypes = (
	PSID ,             # Sid (PSID)
	POINTER(LPWSTR),    # StringSid (LPWSTR*)
)
ConvertSidToStringSid.restype = BOOL

# Add CreateWellKnownSid binding
CreateWellKnownSid = WINFUNCTYPE(None)(("CreateWellKnownSid", dll))
"""
Creates a well-known security identifier (SID).
.. seealso:: https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-createwellknownsid
"""
CreateWellKnownSid.argtypes = (
	DWORD,        # WellKnownSidType
	PSID,         # DomainSid (PSID) or NULL
	PSID,         # pSid (buffer to receive SID)
	POINTER(DWORD),  # cbSid (in/out buffer size)
)
CreateWellKnownSid.restype = BOOL


CreateRestrictedToken = WINFUNCTYPE(None)(("CreateRestrictedToken", dll))
"""
Creates a restricted token by disabling SIDs, deleting privileges, and adding restricted SIDs.
.. seealso:: https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-createrestrictedtoken
"""
CreateRestrictedToken.argtypes = (
	HANDLE,  # ExistingTokenHandle
	DWORD,   # Flags
	DWORD,   # DisableSidCount
	POINTER(SID_AND_ATTRIBUTES),  # SidsToDisable (PSID_AND_ATTRIBUTES)
	DWORD,   # DeletePrivilegeCount
	POINTER(LUID_AND_ATTRIBUTES),  # PrivilegesToDelete (PLUID_AND_ATTRIBUTES)
	DWORD,   # RestrictedSidCount
	POINTER(SID_AND_ATTRIBUTES),  # SidsToRestrict (PSID_AND_ATTRIBUTES)
	POINTER(HANDLE),  # NewToken (PHANDLE)
)
CreateRestrictedToken.restype = BOOL

FreeSid = WINFUNCTYPE(None)(("FreeSid", dll))
"""
Frees a security identifier (SID).
.. seealso:: https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-freesid
"""
FreeSid.argtypes = (
	PSID,  # pSid
)
FreeSid.restype = LPVOID
