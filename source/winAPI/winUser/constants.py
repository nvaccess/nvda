# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from enum import IntEnum


class SystemMetrics(IntEnum):
	"""
	GetSystemMetrics constants
	https://docs.microsoft.com/en-gb/windows/win32/api/winuser/nf-winuser-getsystemmetrics
	"""

	CX_SCREEN = 0
	"""
	The width of the screen of the primary display monitor, in pixels.

	SM_CXSCREEN
	"""

	CY_SCREEN = 1
	"""
	The height of the screen of the primary display monitor, in pixels.

	SM_CYSCREEN
	"""

	SWAP_BUTTON = 23
	"""
	Whether the left and right mouse buttons are swapped.

	SM_SWAPBUTTON
	"""

	X_VIRTUAL_SCREEN = 76
	"""
	The coordinates for the left side of the virtual screen.

	SM_XVIRTUALSCREEN
	"""

	Y_VIRTUAL_SCREEN = 77
	"""
	The coordinates for the top of the virtual screen.

	SM_YVIRTUALSCREEN
	"""

	CX_VIRTUAL_SCREEN = 78
	"""
	The width of the virtual screen, in pixels.

	SM_CXVIRTUALSCREEN
	"""

	CY_VIRTUAL_SCREEN = 79
	"""
	The height of the virtual screen, in pixels.

	SM_CYVIRTUALSCREEN
	"""
