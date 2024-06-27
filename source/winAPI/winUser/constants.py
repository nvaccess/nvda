# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Cyrille Bougot
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


class SysColorIndex(IntEnum):
	"""
	Color index to be used with GetSystemColor.
	See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsyscolor
	"""
	
	WINDOW = 5
	"""
	Window background.
	The associated foreground colors are COLOR_WINDOWTEXT and COLOR_HOTLITE.
	"""
	
	WINDOW_TEXT = 8
	"""
	Text in windows.
	The associated background color is COLOR_WINDOW.
	"""
	
	HIGHLIGHT = 13
	"""
	Item(s) selected in a control.
	The associated foreground color is COLOR_HIGHLIGHTTEXT.
	"""
	
	HIGHLIGHT_TEXT = 14
	"""
	Text of item(s) selected in a control.
	The associated background color is COLOR_HIGHLIGHT.
	"""
