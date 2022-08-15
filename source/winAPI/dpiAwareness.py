# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import ctypes

from logHandler import log


PROCESS_PER_MONITOR_DPI_AWARE = 2
DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = -4


def setDPIAwareness() -> None:
	"""
	Different versions of Windows inconsistently support different styles of DPI Awareness.
	This function attempts to set process DPI awareness using the most modern Windows API method available.

	https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setprocessdpiawarenesscontext
	"""
	# Support is inconsistent across versions of Windows, so try/excepts are used rather than explicit
	# version checks.
	try:
		# Method introduced in Windows 10
		ctypes.windll.user32.SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)
	except AttributeError:
		log.debug("Cannot set DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2, falling back to older method")
	else:
		return
	try:
		# Method introduced in Windows 8
		ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
	except AttributeError:
		log.debug("Cannot set PROCESS_PER_MONITOR_DPI_AWARE, falling back to universal method")
	else:
		ctypes.windll.user32.SetProcessDPIAware()
