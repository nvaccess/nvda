#easeOfAccess.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2014 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Utilities for working with the Windows Ease of Access Center.
"""

import _winreg
import ctypes

APP_KEY = "nvda_nvda_v1"

def isRegistered():
	try:
		_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
			r"Software\Microsoft\Windows NT\CurrentVersion\Accessibility\ATs\%s"
				% APP_KEY,
			0, _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY)
		return True
	except WindowsError:
		return False

def notify(signal):
	if not isRegistered():
		return
	with _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\AccessibilityTemp") as rkey:
		_winreg.SetValueEx(rkey, APP_KEY, None, _winreg.REG_DWORD, signal)
	keys = (0x5b, 0x55) # leftWindows+u
	# Press the keys.
	for vk in keys:
		ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
	# Release the keys.
	for vk in reversed(keys):
		ctypes.windll.user32.keybd_event(vk, 0, 2, 0)
