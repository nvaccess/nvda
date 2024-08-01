# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import ctypes

from logHandler import log

from .constants import (
	HResult,
	SystemErrorCodes,
)


def setDPIAwareness() -> None:
	"""
	Different versions of Windows inconsistently support different styles of DPI Awareness.
	This function attempts to set process DPI awareness using the most modern Windows API method available.

	Only call this function once per instance of NVDA.

	Only call this function when running from source.
	It is recommended that you set the process-default DPI awareness via application manifest.
	Setting the process-default DPI awareness via these API calls can lead to unexpected application behavior.
	"""
	# Support is inconsistent across versions of Windows, so try/excepts are used rather than explicit
	# version checks.
	# https://docs.microsoft.com/en-us/windows/win32/hidpi/setting-the-default-dpi-awareness-for-a-process
	try:
		# An advancement over the original per-monitor DPI awareness mode,
		# which enables applications to access new DPI-related scaling behaviors on a per top-level window basis.
		# For more information on behaviours, refer to:
		# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setprocessdpiawarenesscontext
		DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = -4
		# Method introduced in Windows 10
		# https://docs.microsoft.com/en-us/windows/win32/hidpi/dpi-awareness-context
		success = ctypes.windll.user32.SetProcessDpiAwarenessContext(
			DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2,
		)
	except AttributeError:
		log.debug("Cannot set DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2")
	else:
		if success:
			return
		else:
			errorCode = ctypes.GetLastError()
			if errorCode == SystemErrorCodes.ACCESS_DENIED:
				# The DPI awareness is already set,
				# either by calling this API previously or through the application (.exe) manifest.
				# This is unexpected as we should only set DPI awareness once.
				# NVDA sets DPI awareness from the manifest,
				# however this function should only be called when running from source.
				log.error("DPI Awareness already set.")
				return
			elif errorCode == SystemErrorCodes.INVALID_PARAMETER:
				log.error("DPI Awareness function provided invalid argument.")
			else:
				log.error(f"Unknown error setting DPI Awareness. Error code: {errorCode}")

	log.debug("Falling back to older method of setting DPI Awareness")

	try:
		# https://docs.microsoft.com/en-us/windows/win32/api/shellscalingapi/nf-shellscalingapi-setprocessdpiawareness
		# This window checks for the DPI when it is created and adjusts the scale factor whenever the DPI changes.
		# These processes are not automatically scaled by the system.
		PROCESS_PER_MONITOR_DPI_AWARE = 2
		# Method introduced in Windows 8.1
		hResult = ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
	except AttributeError:
		# Windows 8 / Server 2012 - `shcore` library exists,
		# but `SetProcessDpiAwareness` is not present yet.
		log.debug("Cannot set PROCESS_PER_MONITOR_DPI_AWARE - SetProcessDpiAwareness missing")
	else:
		if hResult == HResult.S_OK:
			return
		elif hResult == HResult.E_ACCESS_DENIED:
			# The DPI awareness is already set,
			# either by calling this API previously or through the application (.exe) manifest.
			# This is unexpected as we should only set DPI awareness once.
			# NVDA sets DPI awareness from the manifest,
			# however this function should only be called when running from source.
			log.error("DPI Awareness already set.")
			return
		elif hResult == HResult.E_INVALID_ARG:
			log.error("DPI Awareness function provided invalid argument.")
		else:
			log.error(f"Unknown error setting DPI Awareness. HRESULT: {hResult}")

	log.debug("Falling back to legacy method of setting DPI Awareness")

	# Method introduced in Windows Vista
	# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setprocessdpiaware
	result = ctypes.windll.user32.SetProcessDPIAware()
	if result == 0:
		errorCode = ctypes.GetLastError()
		log.error(f"Unknown error setting DPI Awareness. Error code: {errorCode}")
