# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2014-2026 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Utilities for working with the Windows Ease of Access Center."""

from enum import Enum, IntEnum  # noqa: I001
from typing import Any

from config.registry import RegistryKey as _RegistryKey, EASE_OF_ACCESS_APP_KEY_NAME
from logHandler import log
import NVDAState
import winreg
import winUser
import winBindings.user32


def __getattr__(attrName: str) -> Any:
	"""Module level `__getattr__` used to preserve backward compatibility."""
	if attrName == "RegistryKey" and NVDAState._allowDeprecatedAPI():
		log.warning("easeOfAccess.RegistryKey is deprecated, use config.registry.RegistryKey instead.")

		class RegistryKey(str, Enum):
			ROOT = _RegistryKey.EASE_OF_ACCESS.value
			TEMP = _RegistryKey.EASE_OF_ACCESS_TEMP.value
			APP = _RegistryKey.EASE_OF_ACCESS_APP.value

		return RegistryKey

	if attrName == "ROOT_KEY" and NVDAState._allowDeprecatedAPI():
		log.warning("ROOT_KEY is deprecated, use config.registry.RegistryKey.EASE_OF_ACCESS instead.")
		return _RegistryKey.EASE_OF_ACCESS.value
	if attrName == "APP_KEY_PATH" and NVDAState._allowDeprecatedAPI():
		log.warning("APP_KEY_PATH is deprecated, use config.registry.RegistryKey.EASE_OF_ACCESS_APP instead.")
		return _RegistryKey.EASE_OF_ACCESS_APP.value
	if attrName == "APP_KEY_NAME" and NVDAState._allowDeprecatedAPI():
		log.warning("APP_KEY_NAME is deprecated, use config.registry.EASE_OF_ACCESS_APP_KEY_NAME instead.")
		return EASE_OF_ACCESS_APP_KEY_NAME
	if attrName == "canConfigTerminateOnDesktopSwitch" and NVDAState._allowDeprecatedAPI():
		log.warning("canConfigTerminateOnDesktopSwitch is deprecated.")
		return True
	raise AttributeError(f"module {__name__!r} has no attribute {attrName!r}")


class AutoStartContext(IntEnum):
	"""Registry HKEY used for tracking when NVDA starts automatically"""

	ON_LOGON_SCREEN = winreg.HKEY_LOCAL_MACHINE
	AFTER_LOGON = winreg.HKEY_CURRENT_USER


def isRegistered() -> bool:
	try:
		winreg.OpenKey(
			winreg.HKEY_LOCAL_MACHINE,
			_RegistryKey.EASE_OF_ACCESS_APP.value,
			access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
		)
		return True
	except FileNotFoundError:
		log.debug("Unable to find AT registry key")
	except OSError:
		log.error("Unable to open AT registry key", exc_info=True)  # noqa: G201
	return False


def notify(signal):
	if not isRegistered():
		return
	with winreg.CreateKey(winreg.HKEY_CURRENT_USER, _RegistryKey.EASE_OF_ACCESS_TEMP.value) as rkey:
		winreg.SetValueEx(rkey, EASE_OF_ACCESS_APP_KEY_NAME, None, winreg.REG_DWORD, signal)
	keys = []
	# The user might be holding unwanted modifiers.
	for vk in winUser.VK_SHIFT, winUser.VK_CONTROL, winUser.VK_MENU:
		if winUser.getAsyncKeyState(vk) & 32768:
			keys.append((vk, False))
	keys.append((0x5B, True))  # leftWindows
	keys.append((0x55, True))  # u
	inputs = []
	# Release unwanted keys and press desired keys.
	for vk, desired in keys:
		input = winBindings.user32.INPUT(type=winBindings.user32.INPUT_TYPE.KEYBOARD)
		input.ii.ki.wVk = vk
		if not desired:
			input.ii.ki.dwFlags = winBindings.user32.KEYEVENTF.KEYUP
		inputs.append(input)
	# Release desired keys and press unwanted keys.
	for vk, desired in reversed(keys):
		input = winBindings.user32.INPUT(type=winBindings.user32.INPUT_TYPE.KEYBOARD)
		input.ii.ki.wVk = vk
		if desired:
			input.ii.ki.dwFlags = winBindings.user32.KEYEVENTF.KEYUP
		inputs.append(input)
	winUser.SendInput(inputs)


def willAutoStart(autoStartContext: AutoStartContext) -> bool:
	"""Based on autoStartContext, gets whether NVDA starts automatically:
	 - AutoStartContext.ON_LOGON_SCREEN : on the logon screen
	 - AutoStartContext.AFTER_LOGON : after logging on

	Returns False on failure
	"""
	try:
		return EASE_OF_ACCESS_APP_KEY_NAME in _getAutoStartConfiguration(autoStartContext)
	except (OSError, TypeError):
		log.error(f"Unable to read {autoStartContext} auto-start configuration", exc_info=True)  # noqa: G201
		return False


def _getAutoStartConfiguration(autoStartContext: AutoStartContext) -> list[str]:
	"""Based on autoStartContext, returns a list of app names which start automatically:
	 - AutoStartContext.ON_LOGON_SCREEN : on the logon screen
	 - AutoStartContext.AFTER_LOGON : after logging on

	Returns an empty list if the registry key or value does not exist.

	:raises OSError: For other registry errors.
	:raises TypeError: If the configuration data is not a string.
	"""
	try:
		with winreg.OpenKey(
			autoStartContext.value,
			_RegistryKey.EASE_OF_ACCESS.value,
			access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
		) as k:
			value = winreg.QueryValueEx(k, "Configuration")[0]
	except FileNotFoundError:
		log.debug(f"Unable to find {autoStartContext} {_RegistryKey.EASE_OF_ACCESS} configuration")
		return []
	if not isinstance(value, str):
		raise TypeError(f"Expected a string for {autoStartContext} auto-start configuration")
	conf: list[str] = value.split(",")
	if not conf[0]:
		# "".split(",") returns [""], so remove the empty string.
		del conf[0]
	return conf


def setAutoStart(autoStartContext: AutoStartContext, enable: bool) -> None:
	"""
	Based on autoStartContext, sets NVDA to start automatically:
	 - AutoStartContext.ON_LOGON_SCREEN : on the logon screen
	 - AutoStartContext.AFTER_LOGON : after logging on

	Does not write if the existing configuration cannot be read.

	:raises OSError: For registry errors.
	:raises TypeError: If the configuration data is not a string.
	"""
	conf = _getAutoStartConfiguration(autoStartContext)
	currentlyEnabled = EASE_OF_ACCESS_APP_KEY_NAME in conf
	changed = False

	if enable and not currentlyEnabled:
		conf.append(EASE_OF_ACCESS_APP_KEY_NAME)
		changed = True
	elif not enable and currentlyEnabled:
		conf.remove(EASE_OF_ACCESS_APP_KEY_NAME)
		changed = True

	if changed:
		with winreg.CreateKeyEx(
			autoStartContext.value,
			_RegistryKey.EASE_OF_ACCESS.value,
			access=winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY,
		) as k:
			winreg.SetValueEx(
				k,
				"Configuration",
				None,
				winreg.REG_SZ,
				",".join(conf),
			)
