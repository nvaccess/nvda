# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import os
import sys
import time
import winreg

import globalVars


class _WritePaths:
	@property
	def configDir(self) -> str:
		return globalVars.appArgs.configPath
	
	@configDir.setter
	def configDir(self, configPath: str):
		globalVars.appArgs.configPath = configPath
		return configPath

	@property
	def addonsDir(self) -> str:
		return os.path.join(self.configDir, "addons")

	@property
	def addonStoreDir(self) -> str:
		return os.path.join(self.configDir, "addonStore")

	@property
	def addonStoreDownloadDir(self) -> str:
		return os.path.join(self.addonStoreDir, "_dl")

	@property
	def profilesDir(self) -> str:
		return os.path.join(self.configDir, "profiles")

	@property
	def scratchpadDir(self) -> str:
		return os.path.join(self.configDir, "scratchpad")

	@property
	def speechDictsDir(self) -> str:
		return os.path.join(self.configDir, "speechDicts")

	@property
	def voiceDictsDir(self) -> str:
		return os.path.join(self.speechDictsDir, "voiceDicts.v1")

	@property
	def voiceDictsBackupDir(self) -> str:
		return os.path.join(self.speechDictsDir, "voiceDictsBackup.v0")

	@property
	def updatesDir(self) -> str:
		return os.path.join(self.configDir, "updates")

	@property
	def nvdaConfigFile(self) -> str:
		return os.path.join(self.configDir, "nvda.ini")

	@property
	def addonStateFile(self) -> str:
		from addonHandler import stateFilename
		return os.path.join(self.configDir, stateFilename)

	@property
	def profileTriggersFile(self) -> str:
		return os.path.join(self.configDir, "profileTriggers.ini")

	@property
	def gesturesConfigFile(self) -> str:
		return os.path.join(self.configDir, "gestures.ini")

	@property
	def speechDictDefaultFile(self) -> str:
		return os.path.join(self.speechDictsDir, "default.dic")

	@property
	def updateCheckStateFile(self) -> str:
		return os.path.join(self.configDir, "updateCheckState.pickle")

	def getSymbolsConfigFile(self, locale: str) -> str:
		return os.path.join(self.configDir, f"symbols-{locale}.dic")

	def getProfileConfigFile(self, name: str) -> str:
		return os.path.join(self.profilesDir, f"{name}.ini")


WritePaths = _WritePaths()


def isRunningAsSource() -> bool:
	"""
	True if NVDA is running as a source copy.
	When running as an installed copy, py2exe sets sys.frozen to 'windows_exe'.
	"""
	return getattr(sys, 'frozen', None) is None


def _allowDeprecatedAPI() -> bool:
	"""
	Used for marking code as deprecated.
	This should never be False in released code.

	Making this False may be useful for testing if code is compliant without using deprecated APIs.
	Note that deprecated code may be imported at runtime,
	and as such, this value cannot be changed at runtime to test compliance.
	"""
	return True


def getStartTime() -> float:
	return globalVars.startTime


def _initializeStartTime() -> None:
	assert globalVars.startTime == 0
	globalVars.startTime = time.time()


def _getExitCode() -> int:
	return globalVars.exitCode


def _setExitCode(exitCode: int) -> None:
	globalVars.exitCode = exitCode


def shouldWriteToDisk() -> bool:
	"""
	Never save config or state if running securely or if running from the launcher.
	When running from the launcher we don't save settings because the user may decide not to
	install this version, and these settings may not be compatible with the already
	installed version. See #7688
	"""
	return not (globalVars.appArgs.secure or globalVars.appArgs.launcher)


class _TrackNVDAInitialization:
	"""
	During NVDA initialization,
	core._initializeObjectCaches needs to cache the desktop object,
	regardless of lock state.
	Security checks may cause the desktop object to not be set if NVDA starts on the lock screen.
	As such, during initialization, NVDA should behave as if Windows is unlocked,
	i.e. winAPI.sessionTracking.isLockScreenModeActive should return False.
	"""

	_isNVDAInitialized = False
	"""When False, isLockScreenModeActive is forced to return False.
	"""

	@staticmethod
	def markInitializationComplete():
		assert not _TrackNVDAInitialization._isNVDAInitialized
		_TrackNVDAInitialization._isNVDAInitialized = True

	@staticmethod
	def isInitializationComplete() -> bool:
		return _TrackNVDAInitialization._isNVDAInitialized


def _forceSecureModeEnabled() -> bool:
	from config import RegistryKey
	try:
		k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value)
		return bool(winreg.QueryValueEx(k, RegistryKey.FORCE_SECURE_MODE_SUBKEY.value)[0])
	except WindowsError:
		# Expected state by default, forceSecureMode parameter not set
		return False


def _serviceDebugEnabled() -> bool:
	from config import RegistryKey
	try:
		k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value)
		return bool(winreg.QueryValueEx(k, RegistryKey.SERVICE_DEBUG_SUBKEY.value)[0])
	except WindowsError:
		# Expected state by default, serviceDebug parameter not set
		return False


def _configInLocalAppDataEnabled() -> bool:
	from config import RegistryKey
	from logHandler import log

	try:
		k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value)
		return bool(winreg.QueryValueEx(k, RegistryKey.CONFIG_IN_LOCAL_APPDATA_SUBKEY.value)[0])
	except FileNotFoundError:
		log.debug("Installed user config is not in local app data")
		return False
	except WindowsError:
		# Expected state by default, configInLocalAppData parameter not set
		return False
