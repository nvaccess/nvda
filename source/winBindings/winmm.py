# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by winmm.dll, and supporting data structures and enumerations."""

from ctypes import (
	WINFUNCTYPE,
	c_size_t,
	windll,
	c_long,
)
from ctypes.wintypes import (
	HANDLE,
	UINT,
)


DWORD_PTR = c_size_t
MMRESULT = c_long
TIMERR_NOERROR: int = 0

dll = windll.winmm


waveOutGetNumDevs = WINFUNCTYPE(None)(("waveOutGetNumDevs", dll))
"""
Retrieves the number of waveform-audio output devices present in the system.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/nf-mmeapi-waveoutgetnumdevs
"""
waveOutGetNumDevs.restype = UINT
waveOutGetNumDevs.argtypes = ()

waveOutMessage = WINFUNCTYPE(None)(("waveOutMessage", dll))
"""
Sends a message to the given waveform-audio output device.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/nf-mmeapi-waveoutmessage
"""
waveOutMessage.restype = MMRESULT
waveOutMessage.argtypes = (
	HANDLE,  # hWaveOut: Handle to the waveform-audio output device
	UINT,  # uMsg: Message to send
	DWORD_PTR,  # dw1: Message parameter (DWORD_PTR)
	DWORD_PTR,  # dw2: Message parameter (DWORD_PTR)
)

timeBeginPeriod = WINFUNCTYPE(None)(("timeBeginPeriod", dll))
"""
Sets the minimum timer resolution for the application.
Must be matched with a corresponding call to timeEndPeriod using the same uPeriod value.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/timeapi/nf-timeapi-timebeginperiod
"""
timeBeginPeriod.restype = MMRESULT
timeBeginPeriod.argtypes = (
	UINT,  # uPeriod: Minimum timer resolution, in milliseconds
)

timeEndPeriod = WINFUNCTYPE(None)(("timeEndPeriod", dll))
"""
Clears a previously set minimum timer resolution.
uPeriod must match the value passed to the corresponding timeBeginPeriod call.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/timeapi/nf-timeapi-timeendperiod
"""
timeEndPeriod.restype = MMRESULT
timeEndPeriod.argtypes = (
	UINT,  # uPeriod: Minimum timer resolution to clear, in milliseconds
)
