# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This file provides system test library functions for sending keyboard key presses.
"""
import pyautogui
pyautogui.FAILSAFE = False


# In Robot libraries, class name must match the name of the module. Use caps for both.
class KeyInputLib:
	@staticmethod
	def send(*keys):
		"""Sends the keys as if pressed by the user.
		Full list of keys: pyautogui.KEYBOARD_KEY
		"""
		pyautogui.hotkey(*keys)
