# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from enum import Enum, nonmember


EASE_OF_ACCESS_APP_KEY_NAME = "nvda_nvda_v1"


class RegistryKey(str, Enum):
	_SOFTWARE = nonmember("SOFTWARE")
	r"""
	The name of the registry key stored under HKEY_LOCAL_MACHINE where system wide NVDA settings are stored.
	Note that if NVDA is a 32-bit application, on x64 systems,
	this will evaluate to `r"SOFTWARE\WOW6432Node"`
	"""
	CURRENT_VERSION = rf"{_SOFTWARE}\Microsoft\Windows\CurrentVersion"
	INSTALLED_COPY = rf"{CURRENT_VERSION}\Uninstall\NVDA"
	RUN = rf"{CURRENT_VERSION}\Run"
	NVDA = rf"{_SOFTWARE}\NVDA"
	APP_PATH = rf"{CURRENT_VERSION}\App Paths\nvda.exe"
	EXPLORER_ADVANCED = rf"{CURRENT_VERSION}\Explorer\Advanced"
	SYSTEM_POLICIES = rf"{CURRENT_VERSION}\Policies\System"
	NT_CURRENT_VERSION = rf"{_SOFTWARE}\Microsoft\Windows NT\CurrentVersion"
	EASE_OF_ACCESS = rf"{NT_CURRENT_VERSION}\Accessibility"
	EASE_OF_ACCESS_TEMP = rf"{NT_CURRENT_VERSION}\AccessibilityTemp"
	EASE_OF_ACCESS_APP = rf"{EASE_OF_ACCESS}\ATs\{EASE_OF_ACCESS_APP_KEY_NAME}"

	# Sub keys

	CONFIG_IN_LOCAL_APPDATA_SUBKEY = "configInLocalAppData"
	"""
	#6864: The name of the subkey stored under RegistryKey.NVDA where the value is stored
	which will make an installed NVDA load the user configuration either from the local or from
	the roaming application data profile.
	The registry value is unset by default.
	When setting it manually, a DWORD value is preferred.
	A value of 0 will evaluate to loading the configuration from the roaming application data (default).
	A value of 1 means loading the configuration from the local application data folder.
	"""
	FORCE_SECURE_MODE_SUBKEY = "forceSecureMode"
	SERVICE_DEBUG_SUBKEY = "serviceDebug"


class _RegistryKeyX86(str, Enum):  # type: ignore[reportUnusedClass]
	"""
	Used to access the 32-bit registry view on x64 systems.
	For cleaning up legacy 32-bit NVDA copies.
	"""

	_SOFTWARE = nonmember(r"SOFTWARE\WOW6432Node")
	CURRENT_VERSION = rf"{_SOFTWARE}\Microsoft\Windows\CurrentVersion"
	INSTALLED_COPY = rf"{CURRENT_VERSION}\Uninstall\NVDA"
	RUN = rf"{CURRENT_VERSION}\Run"
	NVDA = rf"{_SOFTWARE}\NVDA"
	APP_PATH = rf"{CURRENT_VERSION}\App Paths\nvda.exe"
	EXPLORER_ADVANCED = rf"{CURRENT_VERSION}\Explorer\Advanced"
	SYSTEM_POLICIES = rf"{CURRENT_VERSION}\Policies\System"
	NT_CURRENT_VERSION = rf"{_SOFTWARE}\Microsoft\Windows NT\CurrentVersion"
	EASE_OF_ACCESS = rf"{NT_CURRENT_VERSION}\Accessibility"
	EASE_OF_ACCESS_TEMP = rf"{NT_CURRENT_VERSION}\AccessibilityTemp"
	EASE_OF_ACCESS_APP = rf"{EASE_OF_ACCESS}\ATs\{EASE_OF_ACCESS_APP_KEY_NAME}"
