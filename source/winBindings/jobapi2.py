# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Types and constants from jobapi2.h."""

import enum
from ctypes import (
	Structure,
	c_size_t,
	c_int,
)
from ctypes.wintypes import (
	DWORD,
	LARGE_INTEGER,
)

ULONG_PTR = c_size_t

class JOBOBJECTINFOCLASS(enum.IntEnum):
	"""Enumeration of Job Object Information Classes.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/ne-jobapi2-jobobjectinformationclass
	"""
	BasicLimitInformation = 2
	BasicUIRestrictions = 4
	ExtendedLimitInformation = 9

	# as a ctypes param
	@classmethod
	def from_param(cls, obj):
		return c_int(obj)

class JOB_OBJECT_LIMIT(enum.IntFlag):
	KILL_ON_JOB_CLOSE = 0x00002000


class JOBOBJECT_BASIC_LIMIT_INFORMATION(Structure):
	"""
	Contains basic limit information for a job object.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/ns-jobapi2-jobobject_basic_limit_information
	"""

	_fields_ = (
		("PerProcessUserTimeLimit", LARGE_INTEGER),
		("PerJobUserTimeLimit", LARGE_INTEGER),
		("LimitFlags", DWORD),
		("MinimumWorkingSetSize", c_size_t),
		("MaximumWorkingSetSize", c_size_t),
		("ActiveProcessLimit", DWORD),
		("Affinity", ULONG_PTR),
		("PriorityClass", DWORD),
		("SchedulingClass", DWORD),
	)

class IO_COUNTERS(Structure):
	"""
	Contains I/O accounting information for a job object or process.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-io_counters
	"""

	_fields_ = (
		("ReadOperationCount", c_size_t),
		("WriteOperationCount", c_size_t),
		("OtherOperationCount", c_size_t),
		("ReadTransferCount", c_size_t),
		("WriteTransferCount", c_size_t),
		("OtherTransferCount", c_size_t),
	)


class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(Structure):
	"""
	Contains extended limit information for a job object.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/ns-jobapi2-jobobject_extended_limit_information
	"""

	_fields_ = (
		("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
		("IoInfo", IO_COUNTERS),
		("ProcessMemoryLimit", c_size_t),
		("JobMemoryLimit", c_size_t),
		("PeakProcessMemoryUsed", c_size_t),
		("PeakJobMemoryUsed", c_size_t),
	)


class JOB_OBJECT_UILIMIT(enum.IntFlag):
	DESKTOP = 0x00000040
	DISPLAYSETTINGS = 0x00000010
	EXITWINDOWS = 0x00000080
	GLOBALATOMS = 0x00000020
	HANDLES = 0x00000001
	READCLIPBOARD = 0x00000002
	SYSTEMPARAMETERS = 0x00000008
	WRITECLIPBOARD = 0x00000004


class JOBOBJECT_BASIC_UI_RESTRICTIONS (Structure):
	"""
	Contains UI restrictions for a job object.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/ns-jobapi2-jobobject_basic_ui_restrictions
	"""

	_fields_ = (
		("UIRestrictionsClass", DWORD),
	)
