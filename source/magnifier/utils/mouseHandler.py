# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import ctypes
from ctypes import wintypes


class MouseHandler:
	def __init__(self):
		self._mousePosition: tuple[int, int] = (0, 0)

	@property
	def mousePosition(self):
		return self.getMousePosition()

	@mousePosition.setter
	def mousePosition(self, pos: tuple[int, int]):
		self._mousePosition = pos

	def getMousePosition(self) -> tuple[int, int]:
		"""
		Get the current mouse position as (x, y).
		"""
		pt = wintypes.POINT()
		ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
		return (pt.x, pt.y)

	def isLeftClickPressed(self) -> bool:
		"""
		Check if the left mouse button is currently pressed.
		"""
		# VK_LBUTTON = 0x01 (Virtual key code for left mouse button)
		# GetKeyState returns negative value if key is pressed
		return ctypes.windll.user32.GetKeyState(0x01) < 0
