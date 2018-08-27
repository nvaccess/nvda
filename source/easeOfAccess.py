#easeOfAccess.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2014 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Utilities for working with the Windows Ease of Access Center.
"""

try:
	import _winreg as winreg # Python 2.7 import
except ImportError:
	import winreg # Python 3 import
import ctypes
import winUser
from winVersion import winVersion

# Windows >= Vista
isSupported = winVersion.major >= 6
# Windows >= 8
canConfigTerminateOnDesktopSwitch = isSupported and (winVersion.major, winVersion.minor) >= (6, 2)

ROOT_KEY = r"Software\Microsoft\Windows NT\CurrentVersion\Accessibility"
APP_KEY_NAME = "nvda_nvda_v1"
APP_KEY_PATH = r"%s\ATs\%s" % (ROOT_KEY, APP_KEY_NAME)

def isRegistered():
	try:
		winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, APP_KEY_PATH, 0,
			winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
		return True
	except WindowsError:
		return False

def notify(signal):
	if not isRegistered():
		return
	with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\AccessibilityTemp") as rkey:
		winreg.SetValueEx(rkey, APP_KEY_NAME, None, winreg.REG_DWORD, signal)
	keys = []
	# The user might be holding unwanted modifiers.
	for vk in winUser.VK_SHIFT, winUser.VK_CONTROL, winUser.VK_MENU:
		if winUser.getAsyncKeyState(vk) & 32768:
			keys.append((vk, False))
	keys.append((0x5B, True)) # leftWindows
	keys.append((0x55, True)) # u
	inputs = []
	# Release unwanted keys and press desired keys.
	for vk, desired in keys:
		input = winUser.Input(type=winUser.INPUT_KEYBOARD)
		input.ii.ki.wVk = vk
		if not desired:
			input.ii.ki.dwFlags = winUser.KEYEVENTF_KEYUP
		inputs.append(input)
	# Release desired keys and press unwanted keys.
	for vk, desired in reversed(keys):
		input = winUser.Input(type=winUser.INPUT_KEYBOARD)
		input.ii.ki.wVk = vk
		if desired:
			input.ii.ki.dwFlags = winUser.KEYEVENTF_KEYUP
		inputs.append(input)
	winUser.SendInput(inputs)

def willAutoStart(hkey):
	try:
		k = winreg.OpenKey(hkey, ROOT_KEY, 0,
			winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
		return (APP_KEY_NAME in
			winreg.QueryValueEx(k, "Configuration")[0].split(","))
	except WindowsError:
		return False

def setAutoStart(hkey, enable):
	k = winreg.OpenKey(hkey, ROOT_KEY, 0,
		winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY)
	try:
		conf = winreg.QueryValueEx(k, "Configuration")[0].split(",")
	except WindowsError:
		conf = []
	else:
		if not conf[0]:
			# "".split(",") returns [""], so remove the empty string.
			del conf[0]
	changed = False
	if enable and APP_KEY_NAME not in conf:
		conf.append(APP_KEY_NAME)
		changed = True
	elif not enable:
		try:
			conf.remove(APP_KEY_NAME)
			changed = True
		except ValueError:
			pass
	if changed:
		winreg.SetValueEx(k, "Configuration", None, winreg.REG_SZ,
			",".join(conf))
