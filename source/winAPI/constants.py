# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import enum
import os

import winVersion


IS_64_BIT_WINDOWS: bool = winVersion.getWinVer().processorArchitecture.endswith("64")
"""True if the Windows copy is 64bit"""

IS_64_BIT_NVDA = os.environ.get("PROCESSOR_ARCHITECTURE") == "AMD64"


class HResult(enum.IntEnum):
	# https://docs.microsoft.com/en-us/windows/win32/seccrypto/common-hresult-values
	S_OK = 0x00000000
	E_ACCESS_DENIED = 0x80070005  # E_ACCESSDENIED
	E_INVALID_ARG = 0x80070057  # E_INVALIDARG


class SystemErrorCodes(enum.IntEnum):
	# https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-
	SUCCESS = 0x0
	ACCESS_DENIED = 0x5
	INVALID_DATA = 0xD
	NOT_READY = 0x15
	SHARING_VIOLATION = 0x20
	"""The process cannot access the file because it is being used by another process."""
	INVALID_PARAMETER = 0x57
	INSUFFICIENT_BUFFER = 0x7A
	"""The data area passed to a system call is too small."""
	MOD_NOT_FOUND = 0x7E
	NO_MORE_ITEMS = 0x103
	"""No more data is available."""
	CANCELLED = 0x4C7
