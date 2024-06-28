# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import enum


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
	INVALID_PARAMETER = 0x57
	MOD_NOT_FOUND = 0x7E
	CANCELLED = 0x4C7
