# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by winmm.dll, and supporting data structures and enumerations."""

from ctypes import (
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


dll = windll.winmm


waveOutGetNumDevs = dll.waveOutGetNumDevs
"""
Retrieves the number of waveform-audio output devices present in the system.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/nf-mmeapi-waveoutgetnumdevs
"""
waveOutGetNumDevs.restype = UINT
waveOutGetNumDevs.argtypes = ()

waveOutMessage = dll.waveOutMessage
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
