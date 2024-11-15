# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2024 NV Access Limited, Aleksey Sadovoy, Peter Vágner, Rui Batista, Zahari Yurukov,
# Joseph Lee, Babbage B.V., Łukasz Golonka, Julien Cochuyt, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Manages NVDA configuration.
The heart of NVDA's configuration is Configuration Manager, which records current options, profile information and functions to load, save, and switch amongst configuration profiles.
In addition, this module provides three actions: profile switch notifier, an action to be performed when NVDA saves settings, and action to be performed when NVDA is asked to reload configuration from disk or reset settings to factory defaults.
For the latter two actions, one can perform actions prior to and/or after they take place.
"""

from enum import Enum
import globalVars
import winreg
import ctypes
import ctypes.wintypes
import os
import sys
import errno
import itertools
import contextlib
from copy import deepcopy
from collections import OrderedDict
from configobj import ConfigObj
from configobj.validate import Validator
from logHandler import log
import logging
from logging import DEBUG
from shlobj import FolderId, SHGetKnownFolderPath
import baseObject
import easeOfAccess
from fileUtils import FaultTolerantFile
import extensionPoints

from . import profileUpgrader
from . import aggregatedSection
from .configSpec import confspec
from .configFlags import OutputMode
from .featureFlag import (
	_transformSpec_AddFeatureFlagDefault,
	_validateConfig_featureFlag,
)
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Set,
	Tuple,
)
from addonAPIVersion import BACK_COMPAT_TO
import NVDAState
from NVDAState import WritePaths

#: True if NVDA is running as a Windows Store Desktop Bridge application
isAppX = False

#: The active configuration, C{None} if it has not yet been loaded.
#: @type: ConfigManager
conf = None

#: Notifies after the configuration profile has been switched.
#: This allows components and add-ons to apply changes required by the new configuration.
#: For example, braille switches braille displays if necessary.
#: Handlers are called with no arguments.
post_configProfileSwitch = extensionPoints.Action()
#: Notifies when NVDA is saving current configuration.
#: Handlers can listen to "pre" and/or "post" action to perform tasks prior to and/or after NVDA's own configuration is saved.
#: Handlers are called with no arguments.
pre_configSave = extensionPoints.Action()
post_configSave = extensionPoints.Action()
#: Notifies when configuration is reloaded from disk or factory defaults are applied.
#: Handlers can listen to "pre" and/or "post" action to perform tasks prior to and/or after NVDA's own configuration is reloaded.
#: Handlers are called with a boolean argument indicating whether this is a factory reset (True) or just reloading from disk (False).
pre_configReset = extensionPoints.Action()
post_configReset = extensionPoints.Action()


def __getattr__(attrName: str) -> Any:
	"""Module level `__getattr__` used to preserve backward compatibility."""
	if attrName == "NVDA_REGKEY" and NVDAState._allowDeprecatedAPI():
		log.warning("NVDA_REGKEY is deprecated, use RegistryKey.NVDA instead.")
		return RegistryKey.NVDA.value
	if attrName == "RUN_REGKEY" and NVDAState._allowDeprecatedAPI():
		log.warning("RUN_REGKEY is deprecated, use RegistryKey.RUN instead.")
		return RegistryKey.RUN.value
	if attrName == "addConfigDirsToPythonPackagePath" and NVDAState._allowDeprecatedAPI():
		log.warning(
			"addConfigDirsToPythonPackagePath is deprecated, "
			"use addonHandler.packaging.addDirsToPythonPackagePath instead.",
		)
		from addonHandler.packaging import addDirsToPythonPackagePath

		return addDirsToPythonPackagePath
	if attrName == "CONFIG_IN_LOCAL_APPDATA_SUBKEY" and NVDAState._allowDeprecatedAPI():
		# Note: this should only log in situations where it will not be excessively noisy.
		log.warning(
			"CONFIG_IN_LOCAL_APPDATA_SUBKEY is deprecated. "
			"Instead use RegistryKey.CONFIG_IN_LOCAL_APPDATA_SUBKEY. ",
			stack_info=True,
		)
		return RegistryKey.CONFIG_IN_LOCAL_APPDATA_SUBKEY.value
	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")


def initialize():
	global conf
	conf = ConfigManager()


def saveOnExit():
	"""Save the configuration if configured to save on exit.
	This should only be called if NVDA is about to exit.
	Errors are ignored.
	"""
	if conf["general"]["saveConfigurationOnExit"]:
		try:
			conf.save()
		except:  # noqa: E722
			pass


class RegistryKey(str, Enum):
	INSTALLED_COPY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NVDA"
	RUN = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
	NVDA = r"SOFTWARE\NVDA"
	r"""
	The name of the registry key stored under HKEY_LOCAL_MACHINE where system wide NVDA settings are stored.
	Note that NVDA is a 32-bit application, so on X64 systems,
	this will evaluate to `r"SOFTWARE\WOW6432Node\nvda"`
	"""
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


def isInstalledCopy() -> bool:
	"""Checks to see if this running copy of NVDA is installed on the system"""
	try:
		k = winreg.OpenKey(
			winreg.HKEY_LOCAL_MACHINE,
			RegistryKey.INSTALLED_COPY.value,
		)
	except FileNotFoundError:
		log.debug(
			f"Unable to find isInstalledCopy registry key {RegistryKey.INSTALLED_COPY}"
			"- this is not an installed copy.",
		)
		return False
	except WindowsError:
		log.error(
			f"Unable to open isInstalledCopy registry key {RegistryKey.INSTALLED_COPY}",
			exc_info=True,
		)
		return False

	try:
		instDir = winreg.QueryValueEx(k, "UninstallDirectory")[0]
	except FileNotFoundError:
		log.debug(
			f"Unable to find UninstallDirectory value for {RegistryKey.INSTALLED_COPY}"
			"- this may not be an installed copy.",
		)
		return False
	except WindowsError:
		log.error("Unable to query isInstalledCopy registry key", exc_info=True)
		return False

	winreg.CloseKey(k)
	try:
		return os.stat(instDir) == os.stat(globalVars.appDir)
	except (WindowsError, FileNotFoundError):
		log.error(
			"Failed to access the installed NVDA directory,"
			"or, a portable copy failed to access the current NVDA app directory",
			exc_info=True,
		)
		return False


def getInstalledUserConfigPath() -> Optional[str]:
	try:
		winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value)
	except FileNotFoundError:
		log.debug("Could not find nvda registry key, NVDA is not currently installed")
		return None
	except WindowsError:
		log.error("Could not open nvda registry key", exc_info=True)
		return None

	if NVDAState._configInLocalAppDataEnabled():
		configFolder = FolderId.LOCAL_APP_DATA
	else:
		configFolder = FolderId.ROAMING_APP_DATA

	configParent = SHGetKnownFolderPath(configFolder)
	try:
		return os.path.join(configParent, "nvda")
	except WindowsError:
		# (#13242) There is some uncertainty as to how this could be caused
		log.debugWarning("Installed user config is not in local app data", exc_info=True)
		return None


def getUserDefaultConfigPath(useInstalledPathIfExists=False):
	"""Get the default path for the user configuration directory.
	This is the default path and doesn't reflect overriding from the command line,
	which includes temporary copies.
	Most callers will want the C{NVDAState.WritePaths.configDir variable} instead.
	"""
	installedUserConfigPath = getInstalledUserConfigPath()
	if installedUserConfigPath and (
		isInstalledCopy() or isAppX or (useInstalledPathIfExists and os.path.isdir(installedUserConfigPath))
	):
		if isAppX:
			# NVDA is running as a Windows Store application.
			# Although Windows will redirect %APPDATA% to a user directory specific to the Windows Store application,
			# It also makes existing %APPDATA% files available here.
			# We cannot share NVDA user config directories  with other copies of NVDA as their config may be using add-ons
			# Therefore add a suffix to the directory to make it specific to Windows Store application versions.
			installedUserConfigPath += "_appx"
		return installedUserConfigPath
	return os.path.join(globalVars.appDir, "userConfig")


SCRATCH_PAD_ONLY_DIRS = (
	"appModules",
	"brailleDisplayDrivers",
	"brailleTables",
	"globalPlugins",
	"synthDrivers",
	"visionEnhancementProviders",
)


def getScratchpadDir(ensureExists: bool = False) -> str:
	"""Returns the path where custom appModules, globalPlugins and drivers can be placed while being developed."""
	path = WritePaths.scratchpadDir
	if ensureExists:
		if not os.path.isdir(path):
			os.makedirs(path)
		for subdir in SCRATCH_PAD_ONLY_DIRS:
			subpath = os.path.join(path, subdir)
			if not os.path.isdir(subpath):
				os.makedirs(subpath)
	return path


def initConfigPath(configPath: Optional[str] = None) -> None:
	"""
	Creates the current configuration path if it doesn't exist. Also makes sure that various sub directories also exist.
	@param configPath: an optional path which should be used instead (only useful when being called from outside of NVDA)
	"""
	if not configPath:
		configPath = WritePaths.configDir
	if not os.path.isdir(configPath):
		os.makedirs(configPath)
	else:
		OLD_CODE_DIRS = ("appModules", "brailleDisplayDrivers", "globalPlugins", "synthDrivers")
		# #10014: Since #9238 code from these directories is no longer loaded.
		# However they still exist in config for older installations. Remove them if empty to minimize confusion.
		for dir in OLD_CODE_DIRS:
			dir = os.path.join(configPath, dir)
			if os.path.isdir(dir):
				try:
					os.rmdir(dir)
					log.info("Removed old plugins dir: %s", dir)
				except OSError as ex:
					if ex.errno == errno.ENOTEMPTY:
						log.info("Failed to remove old plugins dir: %s. Directory not empty.", dir)
	subdirs = ["speechDicts", "profiles"]
	if not isAppX:
		subdirs.append("addons")
	for subdir in subdirs:
		subdir = os.path.join(configPath, subdir)
		if not os.path.isdir(subdir):
			os.makedirs(subdir)


def getStartAfterLogon() -> bool:
	"""Not to be confused with getStartOnLogonScreen.

	Checks if NVDA is set to start after a logon.
	Checks related easeOfAccess current user registry keys on Windows 8 or newer.
	Then, checks the registry run key to see if NVDA
	has been registered to start after logon on Windows 7
	or by earlier NVDA versions.
	"""
	if easeOfAccess.willAutoStart(easeOfAccess.AutoStartContext.AFTER_LOGON):
		return True
	try:
		k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RegistryKey.RUN.value)
	except FileNotFoundError:
		log.debugWarning(
			f"Unable to find run registry key {RegistryKey.RUN}",
			exc_info=True,
		)
		return False
	except WindowsError:
		log.error(
			f"Unable to open run registry key {RegistryKey.RUN}",
			exc_info=True,
		)
		return False

	try:
		val = winreg.QueryValueEx(k, "nvda")[0]
	except FileNotFoundError:
		log.debug("NVDA is not set to start after logon")
		return False
	except WindowsError:
		log.error("Failed to query NVDA key to set start after logon", exc_info=True)
		return False

	try:
		startAfterLogonPath = os.stat(val)
	except WindowsError:
		log.error(
			"Failed to access the start after logon directory.",
			exc_info=True,
		)
		return False

	try:
		currentSourcePath = os.stat(sys.argv[0])
	except FileNotFoundError:
		log.debug("Failed to access the current running NVDA directory.")
		return False
	except WindowsError:
		log.error(
			"Failed to access the current running NVDA directory.",
			exc_info=True,
		)
		return False

	return currentSourcePath == startAfterLogonPath


def setStartAfterLogon(enable: bool) -> None:
	"""Not to be confused with setStartOnLogonScreen.

	Toggle if NVDA automatically starts after a logon.
	Sets easeOfAccess related registry keys.

	When toggling off, always delete the registry run key
	in case it was set by an earlier version of NVDA.
	"""
	if getStartAfterLogon() == enable:
		return
	easeOfAccess.setAutoStart(easeOfAccess.AutoStartContext.AFTER_LOGON, enable)
	if enable:
		return
	# We're disabling, so ensure the run key is cleared,
	# as it might have been set by an old version.
	k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RegistryKey.RUN.value, 0, winreg.KEY_WRITE)
	try:
		winreg.QueryValue(k, "nvda")
	except FileNotFoundError:
		log.debug(
			"The run registry key is not set for setStartAfterLogon."
			"This is expected since ease of access is used",
		)
		return
	try:
		winreg.DeleteValue(k, "nvda")
	except WindowsError:
		log.error(
			"Couldn't unset registry key for nvda to start after logon.",
			exc_info=True,
		)


SLAVE_FILENAME = os.path.join(globalVars.appDir, "nvda_slave.exe")


def getStartOnLogonScreen() -> bool:
	"""Not to be confused with getStartAfterLogon.

	Checks if NVDA is set to start on the logon screen.

	Checks related easeOfAccess local machine registry keys.
	Then, checks a NVDA registry key to see if NVDA
	has been registered to start on logon by earlier NVDA versions.
	"""
	if easeOfAccess.willAutoStart(easeOfAccess.AutoStartContext.ON_LOGON_SCREEN):
		return True
	try:
		k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value)
	except FileNotFoundError:
		log.debugWarning(f"Could not find NVDA reg key {RegistryKey.NVDA}", exc_info=True)
	except WindowsError:
		log.error(f"Failed to open NVDA reg key {RegistryKey.NVDA}", exc_info=True)
	else:
		try:
			return bool(winreg.QueryValueEx(k, "startOnLogonScreen")[0])
		except FileNotFoundError:
			log.debug(f"Could not find startOnLogonScreen value for {RegistryKey.NVDA} - likely unset.")
			return False
		except WindowsError:
			log.error(f"Failed to query startOnLogonScreen value for {RegistryKey.NVDA}", exc_info=True)
			return False
	return False


def _setStartOnLogonScreen(enable: bool) -> None:
	easeOfAccess.setAutoStart(easeOfAccess.AutoStartContext.ON_LOGON_SCREEN, enable)


def setSystemConfigToCurrentConfig():
	fromPath = WritePaths.configDir
	if ctypes.windll.shell32.IsUserAnAdmin():
		_setSystemConfig(fromPath)
	else:
		import systemUtils

		res = systemUtils.execElevated(SLAVE_FILENAME, ("setNvdaSystemConfig", fromPath), wait=True)
		if res == 2:
			import installer

			raise installer.RetriableFailure
		elif res != 0:
			raise RuntimeError("Slave failure")


def _setSystemConfig(fromPath):
	import installer

	toPath = os.path.join(sys.prefix, "systemConfig")
	log.debug("Copying config to systemconfig dir: %s", toPath)
	if os.path.isdir(toPath):
		installer.tryRemoveFile(toPath)
	for curSourceDir, subDirs, files in os.walk(fromPath):
		if curSourceDir == fromPath:
			curDestDir = toPath
			# Don't copy from top-level config dirs we know will be ignored due to security risks.
			removeSubs = set(SCRATCH_PAD_ONLY_DIRS).intersection(subDirs)
			for subPath in removeSubs:
				log.debug("Ignored folder that may contain unpackaged addons: %s", subPath)
				subDirs.remove(subPath)
		else:
			relativePath = os.path.relpath(curSourceDir, fromPath)
			curDestDir = os.path.join(toPath, relativePath)
		if not os.path.isdir(curDestDir):
			os.makedirs(curDestDir)
		for f in files:
			# Do not copy executables to the system configuration, as this may cause security risks.
			# This will also exclude pending updates.
			if f.endswith(".exe"):
				log.debug(
					"Ignored file %s while copying current user configuration to system configuration" % f,
				)
				continue
			sourceFilePath = os.path.join(curSourceDir, f)
			destFilePath = os.path.join(curDestDir, f)
			installer.tryCopyFile(sourceFilePath, destFilePath)


def setStartOnLogonScreen(enable: bool) -> None:
	"""
	Not to be confused with setStartAfterLogon.

	Toggle whether NVDA starts on the logon screen automatically.
	On failure to set, retries with escalated permissions.

	Raises a RuntimeError on failure.
	"""
	if getStartOnLogonScreen() == enable:
		return
	try:
		# Try setting it directly.
		_setStartOnLogonScreen(enable)
	except WindowsError:
		log.debugWarning("Failed to set start on logon screen's config.")
		# We probably don't have admin privs, so we need to elevate to do this using the slave.
		import systemUtils

		if (
			systemUtils.execElevated(
				SLAVE_FILENAME,
				("config_setStartOnLogonScreen", "%d" % enable),
				wait=True,
			)
			!= 0
		):
			raise RuntimeError("Slave failed to set startOnLogonScreen")


def _transformSpec(spec: ConfigObj):
	"""To make the spec less verbose, transform the spec:
	- Add default="default" to all featureFlag items. This is required so that the key can be read,
	even if it is missing from the config.
	"""
	spec.configspec = spec
	spec.validate(
		Validator(
			{
				"featureFlag": _transformSpec_AddFeatureFlagDefault,
			},
		),
		preserve_errors=True,
	)


class ConfigManager(object):
	"""Manages and provides access to configuration.
	In addition to the base configuration, there can be multiple active configuration profiles.
	Settings in more recently activated profiles take precedence,
	with the base configuration being consulted last.
	This allows a profile to override settings in profiles activated earlier and the base configuration.
	A profile need only include a subset of the available settings.
	Changed settings are written to the most recently activated profile.
	"""

	BASE_ONLY_SECTIONS = {
		"general",
		"update",
		"development",
		"addonStore",
	}
	"""
	Sections that only apply to the base configuration;
	i.e. they cannot be overridden in profiles.
	Note this set may be extended by add-ons.
	"""

	def __init__(self):
		self.spec = confspec
		_transformSpec(self.spec)
		#: All loaded profiles by name.
		self._profileCache: Optional[Dict[Optional[str], ConfigObj]] = {}
		#: The active profiles.
		self.profiles: List[ConfigObj] = []
		#: Whether profile triggers are enabled (read-only).
		self.profileTriggersEnabled: bool = True
		self.validator: Validator = Validator(
			{
				"_featureFlag": _validateConfig_featureFlag,
			},
		)
		self.rootSection: Optional[AggregatedSection] = None
		self._shouldHandleProfileSwitch: bool = True
		self._pendingHandleProfileSwitch: bool = False
		self._suspendedTriggers: Optional[List[ProfileTrigger]] = None
		self._initBaseConf()
		#: Maps triggers to profiles.
		self.triggersToProfiles: Optional[Dict[ProfileTrigger, ConfigObj]] = None
		self._loadProfileTriggers()
		#: The names of all profiles that have been modified since they were last saved.
		self._dirtyProfiles: Set[str] = set()

	def _handleProfileSwitch(self, shouldNotify=True):
		if not self._shouldHandleProfileSwitch:
			self._pendingHandleProfileSwitch = True
			return
		currentRootSection = self.rootSection
		init = currentRootSection is None
		# Reset the cache.
		self.rootSection = AggregatedSection(self, (), self.spec, self.profiles)
		if init:
			# We're still initialising, so don't notify anyone about this change.
			return
		if shouldNotify:
			post_configProfileSwitch.notify(prevConf=currentRootSection.dict())

	def _initBaseConf(self, factoryDefaults=False):
		fn = WritePaths.nvdaConfigFile
		if factoryDefaults:
			profile = self._loadConfig(None)
			profile.filename = fn
		else:
			try:
				profile = self._loadConfig(fn)  # a blank config returned if fn does not exist
				self.baseConfigError = False
			except:  # noqa: E722
				backupFileName = fn + ".corrupted.bak"
				log.error(
					"Error loading base configuration; the base configuration file will be reinitialized."
					f" A copy of your previous configuration file will be saved at {backupFileName}",
					exc_info=True,
				)
				try:
					if os.path.exists(backupFileName):
						os.unlink(backupFileName)
					os.rename(fn, backupFileName)
				except Exception:
					log.error(
						f"Unable to save a copy of the corrupted configuration to {backupFileName}",
						exc_info=True,
					)
				self.baseConfigError = True
				return self._initBaseConf(factoryDefaults=True)

		for key in self.BASE_ONLY_SECTIONS:
			# These sections are returned directly from the base config, so validate them here.
			try:
				sect = profile[key]
			except KeyError:
				profile[key] = {}
				# ConfigObj mutates this into a configobj.Section.
				sect = profile[key]
			sect.configspec = self.spec[key]
			profile.validate(self.validator, section=sect)

		self._profileCache[None] = profile
		self.profiles.append(profile)
		self._handleProfileSwitch()

	def _loadConfig(self, fn, fileError=False):
		log.info("Loading config: {0}".format(fn))
		profile = ConfigObj(fn, indent_type="\t", encoding="UTF-8", file_error=fileError)
		# Python converts \r\n to \n when reading files in Windows, so ConfigObj can't determine the true line ending.
		profile.newlines = "\r\n"
		profileCopy = deepcopy(profile)
		try:
			if NVDAState.shouldWriteToDisk() and profile.filename is not None:
				writeProfileFunc = self._writeProfileToFile
			else:
				writeProfileFunc = None
			profileUpgrader.upgrade(profile, self.validator, writeProfileFunc)
		except Exception as e:
			# Log at level info to ensure that the profile is logged.
			log.info("Config before schema update:\n%s" % profileCopy, exc_info=False)
			raise e
		# since profile settings are not yet imported we have to "peek" to see
		# if debug level logging is enabled.
		try:
			logLevelName = profile["general"]["loggingLevel"]
		except KeyError:
			logLevelName = None
		if log.isEnabledFor(log.DEBUG) or (logLevelName and DEBUG >= logging.getLevelName(logLevelName)):
			# Log at level info to ensure that the profile is logged.
			log.info(
				"Config loaded (after upgrade, and in the state it will be used by NVDA):\n{0}".format(
					profile,
				),
			)
		return profile

	def __getitem__(self, key):
		if key in self.BASE_ONLY_SECTIONS:
			# Return these directly from the base configuration.
			return self.profiles[0][key]
		return self.rootSection[key]

	def __contains__(self, key):
		return key in self.rootSection

	def get(self, key, default=None):
		return self.rootSection.get(key, default)

	def __setitem__(self, key, val):
		self.rootSection[key] = val

	def dict(self):
		return self.rootSection.dict()

	def listProfiles(self):
		try:
			profileFiles = os.listdir(WritePaths.profilesDir)
		except FileNotFoundError:
			log.debugWarning("Profiles directory does not exist.")
			profileFiles = []
		for name in profileFiles:
			name, ext = os.path.splitext(name)
			if ext == ".ini":
				yield name

	def _getProfileFn(self, name: str) -> str:
		return WritePaths.getProfileConfigFile(name)

	def _getProfile(self, name, load=True):
		try:
			return self._profileCache[name]
		except KeyError:
			if not load:
				raise KeyError(name)

		# Load the profile.
		fn = self._getProfileFn(name)
		profile = self._loadConfig(fn, fileError=True)  # file must exist.
		profile.name = name
		profile.manual = False
		profile.triggered = False
		self._profileCache[name] = profile
		return profile

	def getProfile(self, name):
		"""Get a profile given its name.
		This is useful for checking whether a profile has been manually activated or triggered.
		@param name: The name of the profile.
		@type name: str
		@return: The profile object.
		@raise KeyError: If the profile is not loaded.
		"""
		return self._getProfile(name, load=False)

	def manualActivateProfile(self, name):
		"""Manually activate a profile.
		Only one profile can be manually active at a time.
		If another profile was manually activated, deactivate it first.
		If C{name} is C{None}, a profile will not be activated.
		@param name: The name of the profile or C{None} for no profile.
		@type name: str
		"""
		if len(self.profiles) > 1:
			profile = self.profiles[-1]
			if profile.manual:
				del self.profiles[-1]
				profile.manual = False
		if name:
			profile = self._getProfile(name)
			profile.manual = True
			self.profiles.append(profile)
		self._handleProfileSwitch()

	def _markWriteProfileDirty(self):
		if len(self.profiles) == 1:
			# There's nothing other than the base config, which is always saved anyway.
			return
		self._dirtyProfiles.add(self.profiles[-1].name)

	def _writeProfileToFile(self, filename, profile):
		with FaultTolerantFile(filename) as f:
			profile.write(f)

	def save(self):
		"""Save all modified profiles and the base configuration to disk."""
		# #7598: give others a chance to either save settings early or terminate tasks.
		pre_configSave.notify()
		if not NVDAState.shouldWriteToDisk():
			log.info("Not writing profile, either --secure or --launcher args present")
			return
		try:
			self._writeProfileToFile(self.profiles[0].filename, self.profiles[0])
			log.info("Base configuration saved")
			for name in self._dirtyProfiles:
				self._writeProfileToFile(self._profileCache[name].filename, self._profileCache[name])
				log.info("Saved configuration profile %s" % name)
			self._dirtyProfiles.clear()
		except PermissionError as e:
			log.warning("Error saving configuration; probably read only file system", exc_info=True)
			raise e
		post_configSave.notify()

	def reset(self, factoryDefaults=False):
		"""Reset the configuration to saved settings or factory defaults.
		@param factoryDefaults: C{True} to reset to factory defaults, C{False} to reset to saved configuration.
		@type factoryDefaults: bool
		"""
		pre_configReset.notify(factoryDefaults=factoryDefaults)
		self.profiles = []
		self._profileCache.clear()
		self._dirtyProfiles.clear()
		# Signal that we're initialising.
		self.rootSection = None
		self._initBaseConf(factoryDefaults=factoryDefaults)
		post_configReset.notify(factoryDefaults=factoryDefaults)

	def createProfile(self, name):
		"""Create a profile.
		@param name: The name of the profile to create.
		@type name: str
		@raise ValueError: If a profile with this name already exists.
		"""
		if globalVars.appArgs.secure:
			return
		if not name:
			raise ValueError("Missing name.")
		fn = self._getProfileFn(name)
		if os.path.isfile(fn):
			raise ValueError("A profile with the same name already exists: %s" % name)
		# Just create an empty file to make sure we can.
		open(fn, "w").close()
		# Register a script for the new profile.
		# Import late to avoid circular import.
		from globalCommands import ConfigProfileActivationCommands

		ConfigProfileActivationCommands.addScriptForProfile(name)

	def deleteProfile(self, name):
		"""Delete a profile.
		@param name: The name of the profile to delete.
		@type name: str
		@raise LookupError: If the profile doesn't exist.
		"""
		if globalVars.appArgs.secure:
			return
		fn = self._getProfileFn(name)
		if not os.path.isfile(fn):
			raise LookupError("No such profile: %s" % name)
		os.remove(fn)
		# Remove the script for the deleted profile from the script collector.
		# Import late to avoid circular import.
		from globalCommands import ConfigProfileActivationCommands

		ConfigProfileActivationCommands.removeScriptForProfile(name)
		try:
			del self._profileCache[name]
		except KeyError:
			pass
		# Remove any triggers associated with this profile.
		allTriggers = self.triggersToProfiles
		# You can't delete from a dict while iterating through it.
		delTrigs = [trigSpec for trigSpec, trigProfile in allTriggers.items() if trigProfile == name]
		if delTrigs:
			for trigSpec in delTrigs:
				del allTriggers[trigSpec]
			self.saveProfileTriggers()
		# Remove the profile from the dirty profile list
		try:
			self._dirtyProfiles.remove(name)
		except KeyError:
			# The profile wasn't dirty.
			pass
		# Check if this profile was active.
		delProfile = None
		for index in range(len(self.profiles) - 1, -1, -1):
			profile = self.profiles[index]
			if profile.name == name:
				# Deactivate it.
				del self.profiles[index]
				delProfile = profile
		if not delProfile:
			return
		self._handleProfileSwitch()
		if self._suspendedTriggers:
			# Remove any suspended triggers referring to this profile.
			# As the dictionary changes during iteration, wrap this inside a list call.
			for trigger in list(self._suspendedTriggers):
				if trigger._profile == delProfile:
					del self._suspendedTriggers[trigger]

	def renameProfile(self, oldName, newName):
		"""Rename a profile.
		@param oldName: The current name of the profile.
		@type oldName: str
		@param newName: The new name for the profile.
		@type newName: str
		@raise LookupError: If the profile doesn't exist.
		@raise ValueError: If a profile with the new name already exists.
		"""
		if globalVars.appArgs.secure:
			return
		if newName == oldName:
			return
		if not newName:
			raise ValueError("Missing newName")
		oldFn = self._getProfileFn(oldName)
		newFn = self._getProfileFn(newName)
		if not os.path.isfile(oldFn):
			raise LookupError("No such profile: %s" % oldName)
		# Windows file names are case insensitive,
		# so only test for file existence if the names don't match case insensitively.
		if oldName.lower() != newName.lower() and os.path.isfile(newFn):
			raise ValueError("A profile with the same name already exists: %s" % newName)

		os.rename(oldFn, newFn)
		# Update any associated triggers.
		allTriggers = self.triggersToProfiles
		saveTrigs = False
		for trigSpec, trigProfile in allTriggers.items():
			if trigProfile == oldName:
				allTriggers[trigSpec] = newName
				saveTrigs = True
		if saveTrigs:
			self.saveProfileTriggers()
		# Rename the script for the profile.
		# Import late to avoid circular import.
		from globalCommands import ConfigProfileActivationCommands

		ConfigProfileActivationCommands.updateScriptForRenamedProfile(oldName, newName)
		try:
			profile = self._profileCache.pop(oldName)
		except KeyError:
			# The profile hasn't been loaded, so there's nothing more to do.
			return
		profile.name = newName
		self._profileCache[newName] = profile
		try:
			self._dirtyProfiles.remove(oldName)
		except KeyError:
			# The profile wasn't dirty.
			return
		self._dirtyProfiles.add(newName)

	def _triggerProfileEnter(self, trigger):
		"""Called by L{ProfileTrigger.enter}}}."""
		if not self.profileTriggersEnabled:
			return
		if self._suspendedTriggers is not None:
			self._suspendedTriggers[trigger] = "enter"
			return

		log.debug("Activating triggered profile %s" % trigger.profileName)
		try:
			profile = trigger._profile = self._getProfile(trigger.profileName)
		except:
			trigger._profile = None
			raise
		profile.triggered = True
		if len(self.profiles) > 1 and self.profiles[-1].manual:
			# There's a manually activated profile.
			# Manually activated profiles must be at the top of the stack, so insert this one below.
			self.profiles.insert(-1, profile)
		else:
			self.profiles.append(profile)
		self._handleProfileSwitch(trigger._shouldNotifyProfileSwitch)

	def _triggerProfileExit(self, trigger):
		"""Called by L{ProfileTrigger.exit}}}."""
		if not self.profileTriggersEnabled:
			return
		if self._suspendedTriggers is not None:
			if trigger in self._suspendedTriggers:
				# This trigger was entered and is now being exited.
				# These cancel each other out.
				del self._suspendedTriggers[trigger]
			else:
				self._suspendedTriggers[trigger] = "exit"
			return

		profile = trigger._profile
		if profile is None:
			return
		log.debug("Deactivating triggered profile %s" % trigger.profileName)
		profile.triggered = False
		try:
			self.profiles.remove(profile)
		except ValueError:
			# This is probably due to the user resetting the configuration.
			log.debugWarning("Profile not active when exiting trigger")
			return
		self._handleProfileSwitch(trigger._shouldNotifyProfileSwitch)

	@contextlib.contextmanager
	def atomicProfileSwitch(self):
		"""Indicate that multiple profile switches should be treated as one.
		This is useful when multiple triggers may be exited/entered at once;
		e.g. when switching applications.
		While multiple switches aren't harmful, they might take longer;
		e.g. unnecessarily switching speech synthesizers or braille displays.
		This is a context manager to be used with the C{with} statement.
		"""
		self._shouldHandleProfileSwitch = False
		try:
			yield
		finally:
			self._shouldHandleProfileSwitch = True
			if self._pendingHandleProfileSwitch:
				self._handleProfileSwitch()
				self._pendingHandleProfileSwitch = False

	def suspendProfileTriggers(self):
		"""Suspend handling of profile triggers.
		Any triggers that currently apply will continue to apply.
		Subsequent enters or exits will not apply until triggers are resumed.
		@see: L{resumeTriggers}
		"""
		if self._suspendedTriggers is not None:
			return
		self._suspendedTriggers = OrderedDict()

	def resumeProfileTriggers(self):
		"""Resume handling of profile triggers after previous suspension.
		Any trigger enters or exits that occurred while triggers were suspended will be applied.
		Trigger handling will then return to normal.
		@see: L{suspendTriggers}
		"""
		if self._suspendedTriggers is None:
			return
		triggers = self._suspendedTriggers
		self._suspendedTriggers = None
		with self.atomicProfileSwitch():
			for trigger, action in triggers.items():
				trigger.enter() if action == "enter" else trigger.exit()

	def disableProfileTriggers(self):
		"""Temporarily disable all profile triggers.
		Any triggered profiles will be deactivated and subsequent triggers will not apply.
		Call L{enableTriggers} to re-enable triggers.
		"""
		if not self.profileTriggersEnabled:
			return
		self.profileTriggersEnabled = False
		for profile in self.profiles[1:]:
			profile.triggered = False
		if len(self.profiles) > 1 and self.profiles[-1].manual:
			del self.profiles[1:-1]
		else:
			del self.profiles[1:]
		self._suspendedTriggers = None
		self._handleProfileSwitch()

	def enableProfileTriggers(self):
		"""Re-enable profile triggers after they were previously disabled."""
		self.profileTriggersEnabled = True

	def _loadProfileTriggers(self):
		fn = WritePaths.profileTriggersFile
		try:
			cobj = ConfigObj(fn, indent_type="\t", encoding="UTF-8")
		except:  # noqa: E722
			log.error("Error loading profile triggers", exc_info=True)
			cobj = ConfigObj(None, indent_type="\t", encoding="UTF-8")
			cobj.filename = fn
		# Python converts \r\n to \n when reading files in Windows, so ConfigObj can't determine the true line ending.
		cobj.newlines = "\r\n"
		try:
			self.triggersToProfiles = cobj["triggersToProfiles"]
		except KeyError:
			cobj["triggersToProfiles"] = {}
			# ConfigObj will have mutated this into a configobj.Section.
			self.triggersToProfiles = cobj["triggersToProfiles"]

	def saveProfileTriggers(self):
		"""Save profile trigger information to disk.
		This should be called whenever L{profilesToTriggers} is modified.
		"""
		if globalVars.appArgs.secure:
			# Never save if running securely.
			return
		self.triggersToProfiles.parent.write()
		log.info("Profile triggers saved")

	def _getSpecFromKeyPath(self, keyPath):
		if not keyPath or len(keyPath) < 1:
			raise ValueError("Key path not provided")

		spec = conf.spec
		for nextKey in keyPath:
			spec = spec[nextKey]
		return spec

	def _getConfigValidation(self, spec):
		"""returns a tuple with the spec for the config spec:
		("type", [], {}, "default value") EG:
		- (u'boolean', [], {}, u'false')
		- (u'integer', [], {'max': u'255', 'min': u'1'}, u'192')
		- (u'option', [u'changedContext', u'fill', u'scroll'], {}, u'changedContext')
		"""
		return conf.validator._parse_with_caching(spec)

	def getConfigValidation(self, keyPath):
		"""Get a config validation details
		This can be used to get a L{ConfigValidationData} containing the type, default, options list, or
		other validation parameters (min, max, etc) for a config key.
		@param keyPath: a sequence of the identifiers leading to the config key. EG ("braille", "messageTimeout")
		@return ConfigValidationData
		"""
		spec = self._getSpecFromKeyPath(keyPath)
		parsedSpec = self._getConfigValidation(spec)
		data = ConfigValidationData(parsedSpec[0])
		data.args = parsedSpec[1]
		data.kwargs = parsedSpec[2]
		data.default = conf.validator.get_default_value(spec)
		return data


class ConfigValidationData(object):
	validationFuncName = None  # type: str

	def __init__(self, validationFuncName):
		self.validationFuncName = validationFuncName
		super(ConfigValidationData, self).__init__()

	# args passed to the convert function
	args = []  # type: List[Any]

	# kwargs passed to the convert function.
	kwargs = {}  # type: Dict[str, Any]

	# the default value, used when config is missing.
	default = None  # converted to the appropriate type


class AggregatedSection:
	"""A view of a section of configuration which aggregates settings from all active profiles."""

	# TODO: move to config.aggregatedSection

	def __init__(
		self,
		manager: ConfigManager,
		path: Tuple[str],
		spec: ConfigObj,
		profiles: List[ConfigObj],
	):
		self.manager = manager
		self.path = path
		self._spec = spec
		#: The relevant section in all of the profiles.
		self.profiles = profiles
		self._cache: aggregatedSection._cacheT = {}

	@staticmethod
	def _isSection(val: Any) -> bool:
		"""Checks if a given value or spec is a section of a config profile."""
		return isinstance(val, dict)

	def __getitem__(
		self,
		key: aggregatedSection._cacheKeyT,
		checkValidity: bool = True,
	):
		# Try the cache first.
		try:
			val = self._cache[key]
		except KeyError:
			pass
		else:
			if val is KeyError:
				# We know there's no such setting.
				raise KeyError(key)
			return val

		spec = self._spec.get(key)
		foundSection = False
		if self._isSection(spec):
			foundSection = True

		# Walk through the profiles looking for the key.
		# If it's a section, collect that section from all profiles.
		subProfiles = []
		for profile in reversed(self.profiles):
			try:
				val = profile[key]
			except (KeyError, TypeError):
				# Indicate that this key doesn't exist in this profile.
				subProfiles.append(None)
				continue
			if self._isSection(val):
				foundSection = True
				subProfiles.append(val)
			else:
				# This is a setting.
				if not checkValidity:
					return val  # Never cache unvalidated values
				return self._cacheLeaf(key, spec, val)
		subProfiles.reverse()

		if not foundSection and spec:
			# This might have a default.
			try:
				val = self.manager.validator.get_default_value(spec)
			except KeyError:
				pass
			else:
				self._cache[key] = val
				return val

		if not foundSection:
			# The key doesn't exist, so cache this fact.
			self._cache[key] = KeyError
			raise KeyError(key)

		if spec is None:
			# Create this section in the config spec.
			self._spec[key] = {}
			# ConfigObj might have mutated this into a configobj.Section.
			spec = self._spec[key]
		sect = self._cache[key] = AggregatedSection(self.manager, self.path + (key,), spec, subProfiles)
		return sect

	def __contains__(self, key):
		try:
			self[key]
			return True
		except KeyError:
			return False

	def get(self, key, default=None):
		try:
			return self[key]
		except KeyError:
			return default

	def isSet(self, key):
		"""Check whether a given key has been explicitly set.
		This is sometimes useful because it can return C{False} even if there is a default for the key.
		@return: C{True} if the key has been explicitly set, C{False} if not.
		@rtype: bool
		"""
		for profile in self.profiles:
			if not profile:
				continue
			if key in profile:
				return True
		return False

	def _cacheLeaf(self, key, spec, val):
		if spec:
			# Validate and convert the value.
			val = self.manager.validator.check(spec, val)
		self._cache[key] = val
		return val

	def __iter__(self):
		keys = set()
		# Start with the cached items.
		for key, val in self._cache.items():
			keys.add(key)
			if val is not KeyError:
				yield key
		# Walk through the profiles and spec looking for items not yet cached.
		for profile in itertools.chain(reversed(self.profiles), (self._spec,)):
			if not profile:
				continue
			for key in profile:
				if key in keys:
					continue
				keys.add(key)
				yield key

	def items(self):
		for key in self:
			try:
				yield (key, self[key])
			except KeyError:
				# This could happen if the item is in the spec but there's no default.
				pass

	def copy(self):
		return dict(self.items())

	def dict(self):
		"""Return a deepcopy of self as a dictionary.
		Adapted from L{configobj.Section.dict}.
		"""
		newdict = {}
		for key, value in self.items():
			if isinstance(value, AggregatedSection):
				value = value.dict()
			elif isinstance(value, list):
				# create a copy rather than a reference
				value = list(value)
			elif isinstance(value, tuple):
				# create a copy rather than a reference
				value = tuple(value)
			newdict[key] = value
		return newdict

	def __setitem__(
		self,
		key: aggregatedSection._cacheKeyT,
		val: aggregatedSection._cacheValueT,
	):
		spec = self._spec.get(key) if self.spec else None
		if self._isSection(spec) and not self._isSection(val):
			raise ValueError("Value must be a section")

		if self._isSection(spec) or self._isSection(val):
			# Update the profile.
			updateSect = self._getUpdateSection()
			updateSect[key] = val
			self.manager._markWriteProfileDirty()
			# ConfigObj will have mutated this into a configobj.Section.
			val = updateSect[key]
			cache = self._cache.get(key)
			if cache and cache is not KeyError:
				# An AggregatedSection has already been cached, so update it.
				cache = self._cache[key]
				cache.profiles[-1] = val
				cache._cache.clear()
			elif cache is KeyError:
				# This key now exists, so remove the cached non-existence.
				del self._cache[key]
			# If an AggregatedSection isn't already cached,
			# An appropriate AggregatedSection will be created the next time this section is fetched.
			return

		if spec:
			# Validate and convert the value.
			val = self.manager.validator.check(spec, val)

		try:
			# when setting the value we dont care if the existing value
			# is not valid.
			curVal = self.__getitem__(key, checkValidity=False)
		except KeyError:
			pass
		else:
			if self._isSection(val) or self._isSection(curVal):
				# If value is a section, continue to update
				pass
			elif str(val) == str(curVal):
				# Check str comparison as this is what is written to the config.
				# If the value is unchanged, do not update
				# or mark the profile as dirty.
				return

		# Set this value in the most recently activated profile.
		self._getUpdateSection()[key] = val
		self.manager._markWriteProfileDirty()
		self._cache[key] = val

		# Alias ["documentFormatting"]["reportFontAttributes"] and ["speech"]["includeCLDR"]
		# for backwards compatibility.
		# TODO: Comment out in 2025.1.
		if BACK_COMPAT_TO < (2025, 1, 0) and NVDAState._allowDeprecatedAPI():
			self._linkDeprecatedValues(key, val)

	def _linkDeprecatedValues(self, key: aggregatedSection._cacheKeyT, val: aggregatedSection._cacheValueT):
		"""Link deprecated config keys and values to their replacements.

		Args:
			key: The configuration key to link to its new or old counterpart.
			val: The value associated with the configuration key.

		postconditions:
			- If self.path is "documentFormatting":
				- If key is "reportFontAttributes":
					- If val is True, "documentFormatting.fontAttributeReporting" is set to OutputMode.SPEECH_AND_BRAILLE, otherwise, it is set to OutputMode.OFF.
				- If key is "fontAttributeReporting":
					- if val is OutputMode.OFF, "documentFormatting.reportFontAttributes" is set to False, otherwise, it is set to True.
		"""
		match self.path:
			case ("documentFormatting",):
				match key:
					case "fontAttributeReporting":
						# Alias documentFormatting.fontAttributeReporting to documentFormatting.reportFontAttributes for backwards compatibility.
						key = "reportFontAttributes"
						val = bool(val)

					case "reportFontAttributes":
						# Alias documentFormatting.reportFontAttributes to documentFormatting.fontAttributeReporting for forwards compatibility.
						log.warning(
							"documentFormatting.reportFontAttributes is deprecated. Use documentFormatting.fontAttributeReporting instead.",
							# Include stack info so testers can report warning to add-on author.
							stack_info=True,
						)
						key = "fontAttributeReporting"
						val = OutputMode.SPEECH_AND_BRAILLE if val else OutputMode.OFF

					case _:
						# We don't care about other keys in this section.
						return

			case ("speech",):
				match key:
					case "symbolDictionaries":
						# Alias speech.symbolDictionaries to speech.includeCLDR for backwards compatibility.
						key = "includeCLDR"
						val = "cldr" in val

					case "includeCLDR":
						# Alias speech.includeCLDR to speech.symbolDictionaries for forwards compatibility.
						log.warning(
							"speech.includeCLDR is deprecated. Use speech.symbolDictionaries instead.",
							# Include stack info so testers can report warning to add-on author.
							stack_info=True,
						)
						key = "symbolDictionaries"
						curVal = self.get(key, []).copy()
						if val and "cldr" not in curVal:
							curVal.append("cldr")
						elif not val and "cldr" in curVal:
							curVal.remove("cldr")
						val = curVal

					case _:
						# We don't care about other keys in this section.
						return

			case _:
				# We don't care about other sections.
				return

		# Update the value in the most recently activated profile.
		# If we have reached this point, we must have a new key and value to set.
		self._getUpdateSection()[key] = val
		self._cache[key] = val

	def _getUpdateSection(self):
		profile = self.profiles[-1]
		if profile is not None:
			# This section already exists in the profile.
			return profile

		section = self.manager.rootSection
		profile = section.profiles[-1]
		for part in self.path:
			parentProfile = profile
			section = section[part]
			profile = section.profiles[-1]
			if profile is None:
				# This section doesn't exist in the profile yet.
				# Create it and update the AggregatedSection.
				parentProfile[part] = {}
				# ConfigObj might have mutated this into a configobj.Section.
				profile = section.profiles[-1] = parentProfile[part]
		return profile

	@property
	def spec(self):
		return self._spec

	@spec.setter
	def spec(self, val):
		# This section is being replaced.
		# Clear it and replace the content so it remains linked to the main spec.
		self._spec.clear()
		self._spec.update(val)


class ProfileTrigger(object):
	"""A trigger for automatic activation/deactivation of a configuration profile.
	The user can associate a profile with a trigger.
	When the trigger applies, the associated profile is activated.
	When the trigger no longer applies, the profile is deactivated.
	L{spec} is a string used to search for this trigger and must be implemented.
	To signal that this trigger applies, call L{enter}.
	To signal that it no longer applies, call L{exit}.
	Alternatively, you can use this object as a context manager via the with statement;
	i.e. this trigger will apply only inside the with block.
	"""

	#: Whether to notify handlers when activating a triggered profile.
	#: This should usually be C{True}, but might be set to C{False} when
	#: only specific settings should be applied.
	#: For example, when switching profiles during a speech sequence,
	#: we only want to apply speech settings, not switch braille displays.
	_shouldNotifyProfileSwitch = True

	@baseObject.Getter
	def spec(self):
		"""The trigger specification.
		This is a string used to search for this trigger in the user's configuration.
		@rtype: str
		"""
		raise NotImplementedError

	@property
	def hasProfile(self):
		"""Whether this trigger has an associated profile.
		@rtype: bool
		"""
		return self.spec in conf.triggersToProfiles

	def enter(self):
		"""Signal that this trigger applies.
		The associated profile (if any) will be activated.
		"""
		try:
			self.profileName = conf.triggersToProfiles[self.spec]
		except KeyError:
			self.profileName = None
			return
		try:
			conf._triggerProfileEnter(self)
		except:  # noqa: E722
			log.error(
				"Error entering trigger %s, profile %s" % (self.spec, self.profileName),
				exc_info=True,
			)

	__enter__ = enter

	def exit(self):
		"""Signal that this trigger no longer applies.
		The associated profile (if any) will be deactivated.
		"""
		if not self.profileName:
			return
		try:
			conf._triggerProfileExit(self)
		except:  # noqa: E722
			log.error(
				"Error exiting trigger %s, profile %s" % (self.spec, self.profileName),
				exc_info=True,
			)

	def __exit__(self, excType, excVal, traceback):
		self.exit()


class AllowUiaInChromium(Enum):
	_DEFAULT = 0  # maps to 'when necessary'
	WHEN_NECESSARY = 1  # the current default
	YES = 2
	NO = 3

	@staticmethod
	def getConfig() -> "AllowUiaInChromium":
		allow = AllowUiaInChromium(conf["UIA"]["allowInChromium"])
		if allow == AllowUiaInChromium._DEFAULT:
			return AllowUiaInChromium.WHEN_NECESSARY
		return allow


class AllowUiaInMSWord(Enum):
	_DEFAULT = 0  # maps to 'where suitable'
	WHEN_NECESSARY = 1
	WHERE_SUITABLE = 2
	ALWAYS = 3

	@staticmethod
	def getConfig() -> "AllowUiaInMSWord":
		allow = AllowUiaInMSWord(conf["UIA"]["allowInMSWord"])
		if allow == AllowUiaInMSWord._DEFAULT:
			return AllowUiaInMSWord.WHERE_SUITABLE
		return allow
