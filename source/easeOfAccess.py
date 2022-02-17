# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2014-2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Utilities for working with the Windows Ease of Access Center.
"""

from buildVersion import version_year
from enum import Enum, IntEnum
from typing import List
from logHandler import log
import winreg
import winUser
import winVersion


# Windows >= 8
canConfigTerminateOnDesktopSwitch: bool = winVersion.getWinVer() >= winVersion.WIN8
_APP_KEY_NAME = "nvda_nvda_v1"


class RegistryKey(str, Enum):
	ROOT = r"Software\Microsoft\Windows NT\CurrentVersion\Accessibility"
	TEMP = r"Software\Microsoft\Windows NT\CurrentVersion\AccessibilityTemp"
	APP = r"%s\ATs\%s" % (ROOT, _APP_KEY_NAME)


class AutoStartContext(IntEnum):
	"""Registry HKEY used for tracking when NVDA starts automatically"""
	ON_LOGON_SCREEN = winreg.HKEY_LOCAL_MACHINE
	AFTER_LOGON = winreg.HKEY_CURRENT_USER


if version_year < 2023:
	ROOT_KEY = RegistryKey.ROOT.value
	"""
	Deprecated, for removal in 2023.
	Use L{RegistryKey.ROOT} instead.
	"""

	APP_KEY_NAME = _APP_KEY_NAME
	"""Deprecated, for removal in 2023"""

	APP_KEY_PATH = RegistryKey.APP.value
	"""
	Deprecated, for removal in 2023.
	Use L{RegistryKey.APP} instead.
	"""


def isRegistered() -> bool:
	try:
		winreg.OpenKey(
			winreg.HKEY_LOCAL_MACHINE,
			RegistryKey.APP.value,
			0,
			winreg.KEY_READ | winreg.KEY_WOW64_64KEY
		)
		return True
	except FileNotFoundError:
		log.debug("Unable to find AT registry key")
	except WindowsError:
		log.error("Unable to open AT registry key", exc_info=True)
	return False


def notify(signal):
	if not isRegistered():
		return
	with winreg.CreateKey(winreg.HKEY_CURRENT_USER, RegistryKey.TEMP.value) as rkey:
		winreg.SetValueEx(rkey, _APP_KEY_NAME, None, winreg.REG_DWORD, signal)
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


def willAutoStart(autoStartContext: AutoStartContext) -> bool:
	"""Based on autoStartContext, gets whether NVDA starts automatically:
	 - AutoStartContext.ON_LOGON_SCREEN : on the logon screen
	 - AutoStartContext.AFTER_LOGON : after logging on

	Returns False on failure
	"""
	return (_APP_KEY_NAME in _getAutoStartConfiguration(autoStartContext))


def _getAutoStartConfiguration(autoStartContext: AutoStartContext) -> List[str]:
	"""Based on autoStartContext, returns a list of app names which start automatically:
	 - AutoStartContext.ON_LOGON_SCREEN : on the logon screen
	 - AutoStartContext.AFTER_LOGON : after logging on

	Returns an empty list on failure.
	"""
	try:
		k = winreg.OpenKey(
			autoStartContext.value,
			RegistryKey.ROOT.value,
			0,
			winreg.KEY_READ | winreg.KEY_WOW64_64KEY
		)
	except FileNotFoundError:
		log.debug(f"Unable to find existing {autoStartContext} {RegistryKey.ROOT}")
		return []
	except WindowsError:
		log.error(f"Unable to open {autoStartContext} {RegistryKey.ROOT} for reading", exc_info=True)
		return []

	try:
		conf: List[str] = winreg.QueryValueEx(k, "Configuration")[0].split(",")
	except FileNotFoundError:
		log.debug(f"Unable to find {autoStartContext} {RegistryKey.ROOT} configuration")
	except WindowsError:
		log.error(f"Unable to query {autoStartContext} {RegistryKey.ROOT} configuration", exc_info=True)
	else:
		if not conf[0]:
			# "".split(",") returns [""], so remove the empty string.
			del conf[0]
		return conf
	return []


def setAutoStart(autoStartContext: AutoStartContext, enable: bool) -> None:
	"""
	Based on autoStartContext, sets NVDA to start automatically:
	 - AutoStartContext.ON_LOGON_SCREEN : on the logon screen
	 - AutoStartContext.AFTER_LOGON : after logging on

	May incorrectly set autoStart to False upon failing to fetch the previously set value from the registry.

	Raises `Union[WindowsError, FileNotFoundError]`
	"""
	conf = _getAutoStartConfiguration(autoStartContext)
	currentlyEnabled = _APP_KEY_NAME in conf
	changed = False

	if enable and not currentlyEnabled:
		conf.append(_APP_KEY_NAME)
		changed = True
	elif not enable and currentlyEnabled:
		conf.remove(_APP_KEY_NAME)
		changed = True

	if changed:
		k = winreg.OpenKey(
			autoStartContext.value,
			RegistryKey.ROOT.value,
			0,
			winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY
		)
		winreg.SetValueEx(k, "Configuration", None, winreg.REG_SZ,
			",".join(conf))
