# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Types and constants from winnt.h."""

import enum
from ctypes import (
	Structure,
	sizeof,
	POINTER,
	c_void_p,
)
from ctypes.wintypes import (
	LONG,
	BYTE,
	WORD,
	DWORD,
	LPVOID,
	HANDLE,
	LPWSTR,
	BOOL,
)

MAXIMUM_ALLOWED = 0x02000000
DISABLE_MAX_PRIVILEGE = 0x1

PSID = c_void_p


class LUID(Structure):
	"""
	Locally unique identifier (LUID).

	..seealso: https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-luid
	"""
	_fields_ = (
		("LowPart", DWORD),
		("HighPart", LONG),
	)


class LUID_AND_ATTRIBUTES(Structure):
	"""
	Specifies a locally unique identifier (LUID) and its attributes.

	..seealso: https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-luid_and_attributes
	"""
	_fields_ = (
		("Luid", LUID),
		("Attributes", DWORD),
	)


class SID_AND_ATTRIBUTES(Structure):
	"""
	Specifies a SID and its attributes.

	..seealso: https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-sid_and_attributes
	"""
	_fields_ = (
		("Sid", PSID),
		("Attributes", DWORD),
	)


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
		("lpReserved2", POINTER(BYTE)),
		("hSTDInput", HANDLE),
		("hSTDOutput", HANDLE),
		("hSTDError", HANDLE),
	)

	def __init__(self, **kwargs):
		super(STARTUPINFOW, self).__init__(cb=sizeof(self), **kwargs)


STARTUPINFO = STARTUPINFOW


class STARTUPINFOEXW(Structure):
	"""
	An extended version of the STARTUPINFO structure that can be used with the CreateProcess function.

	..seealso:
		https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfoexw
	"""

	_fields_ = (
		("startupInfo", STARTUPINFOW),
		("lpAttributeList", LPVOID),
	)

STARTUPINFOEX = STARTUPINFOEXW


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


class SECURITY_CAPABILITIES(Structure):
	"""
	Specifies the security capabilities of a process.

	..seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-security_capabilities
	"""

	_fields_ = (
		("AppContainerSid", PSID),
		("Capabilities", POINTER(SID_AND_ATTRIBUTES)),
		("CapabilityCount", DWORD),
		("Reserved", DWORD),
	 )

class PROC_THREAD_ATTRIBUTE(enum.IntEnum):
	HANDLE_LIST = 0x20002
	SECURITY_CAPABILITIES = 0x20009

SE_GROUP_ENABLED = 0x4
EXTENDED_STARTUPINFO_PRESENT = 0x00080000
HANDLE_FLAG_INHERIT = 0x1
STARTF_USESTDHANDLES = 0x00000100
LOGON32_LOGON_INTERACTIVE = 2
LOGON32_LOGON_SERVICE = 5
LOGON32_PROVIDER_DEFAULT = 0
TokenSessionId = 12
CREATIONFLAGS_EXTENDED_STARTUPINFO_PRESENT = 0x00080000
CREATIONFLAGS_CREATE_NO_WINDOW = 0x08000000
CREATIONFLAGS_CREATE_SUSPENDED = 0x00000004
CREATIONFLAGS_CREATE_UNICODE_ENVIRONMENT = 0x00000400
GENERIC_ALL = 0x10000000

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

LPSECURITY_ATTRIBUTES = POINTER(SECURITY_ATTRIBUTES)
