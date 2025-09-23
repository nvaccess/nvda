# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions exported by dbgHelp.dll, and supporting data structures and enumerations."""

from ctypes import (
	c_void_p,
	POINTER,
	Structure,
	windll,
)
from ctypes.wintypes import (
	HANDLE,
	DWORD,
	BOOL,
)


MINIDUMP_TYPE = DWORD


class MINIDUMP_EXCEPTION_INFORMATION(Structure):
	_fields_ = (
		("ThreadId", DWORD),
		("ExceptionPointers", c_void_p),
		("ClientPointers", BOOL),
	)


PMINIDUMP_EXCEPTION_INFORMATION = POINTER(MINIDUMP_EXCEPTION_INFORMATION)

PMINIDUMP_USER_STREAM_INFORMATION = c_void_p
PMINIDUMP_CALLBACK_INFORMATION = c_void_p

dll = windll.dbgHelp


MiniDumpWriteDump = dll.MiniDumpWriteDump
"""
Writes a memory dump of the specified process to a file.
.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/minidumpapiset/nf-minidumpapiset-minidumpwritedump
"""
MiniDumpWriteDump.argtypes = (
	HANDLE,  # hProcess: A handle to the process to be dumped.
	DWORD,  # ProcessId: The identifier of the process to be dumped.
	HANDLE,  # hFile: A handle to the file to which the dump is written.
	MINIDUMP_TYPE,  # DumpType: The type of dump to be written.
	PMINIDUMP_EXCEPTION_INFORMATION,  # ExceptionParam: A pointer to an EXCEPTION_POINTERS structure that contains information about the exception that caused the dump.
	PMINIDUMP_USER_STREAM_INFORMATION,  # UserStreamParam: A pointer to a user-defined data structure that contains additional information to be included in the dump.
	PMINIDUMP_CALLBACK_INFORMATION,  # CallbackParam: A pointer to a callback function that is called during the dump process.
)
MiniDumpWriteDump.restype = BOOL
