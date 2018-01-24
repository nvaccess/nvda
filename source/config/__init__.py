# -*- coding: UTF-8 -*-
#config/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2018 NV Access Limited, Aleksey Sadovoy, Peter Vágner, Rui Batista, Zahari Yurukov, Joseph Lee, Babbage B.V.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Manages NVDA configuration.
""" 
import globalVars
import _winreg
import ctypes
import ctypes.wintypes
import os
import sys
from cStringIO import StringIO
import itertools
import contextlib
from copy import deepcopy
from collections import OrderedDict
from configobj import ConfigObj, ConfigObjError
from validate import Validator
from logHandler import log, levelNames
from logging import DEBUG
import shlobj
import baseObject
import easeOfAccess
from fileUtils import FaultTolerantFile
import winKernel
import extensionPoints
import profileUpgrader
from .configSpec import confspec

#: True if NVDA is running as a Windows Store Desktop Bridge application
isAppX=False

#: The active configuration, C{None} if it has not yet been loaded.
#: @type: ConfigObj
conf = None

#: Notifies when the configuration profile is switched.
#: This allows components to apply changes required by the new configuration.
#: For example, braille switches braille displays if necessary.
#: Handlers are called with no arguments.
configProfileSwitched = extensionPoints.Action()

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
		except:
			pass

def isInstalledCopy():
	"""Checks to see if this running copy of NVDA is installed on the system"""
	try:
		k=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NVDA")
		instDir=_winreg.QueryValueEx(k,"UninstallDirectory")[0]
	except WindowsError:
		return False
	_winreg.CloseKey(k)
	try:
		return os.stat(instDir)==os.stat(os.getcwdu()) 
	except WindowsError:
		return False


#: #6864: The name of the subkey stored under NVDA_REGKEY where the value is stored
#: which will make an installed NVDA load the user configuration either from the local or from the roaming application data profile.
#: The registry value is unset by default.
#: When setting it manually, a DWORD value is prefered.
#: A value of 0 will evaluate to loading the configuration from the roaming application data (default).
#: A value of 1 means loading the configuration from the local application data folder.
#: @type: unicode
CONFIG_IN_LOCAL_APPDATA_SUBKEY=u"configInLocalAppData"

def getInstalledUserConfigPath():
	try:
		k = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, NVDA_REGKEY)
		configInLocalAppData = bool(_winreg.QueryValueEx(k, CONFIG_IN_LOCAL_APPDATA_SUBKEY)[0])
	except WindowsError:
		configInLocalAppData=False
	configParent=shlobj.SHGetFolderPath(0, shlobj.CSIDL_LOCAL_APPDATA if configInLocalAppData else shlobj.CSIDL_APPDATA)
	try:
		return os.path.join(configParent, "nvda")
	except WindowsError:
		return None

def getUserDefaultConfigPath(useInstalledPathIfExists=False):
	"""Get the default path for the user configuration directory.
	This is the default path and doesn't reflect overriding from the command line,
	which includes temporary copies.
	Most callers will want the C{globalVars.appArgs.configPath variable} instead.
	"""
	installedUserConfigPath=getInstalledUserConfigPath()
	if installedUserConfigPath and (isInstalledCopy() or isAppX or (useInstalledPathIfExists and os.path.isdir(installedUserConfigPath))):
		if isAppX:
			# NVDA is running as a Windows Store application.
			# Although Windows will redirect %APPDATA% to a user directory specific to the Windows Store application,
			# It also makes existing %APPDATA% files available here. 
			# We cannot share NVDA user config directories  with other copies of NVDA as their config may be using add-ons
			# Therefore add a suffix to the directory to make it specific to Windows Store application versions.
			installedUserConfigPath+='_appx'
		return installedUserConfigPath
	return u'.\\userConfig\\'

def getSystemConfigPath():
	if isInstalledCopy():
		try:
			return os.path.join(shlobj.SHGetFolderPath(0, shlobj.CSIDL_COMMON_APPDATA), "nvda")
		except WindowsError:
			pass
	return None

def initConfigPath(configPath=None):
	"""
	Creates the current configuration path if it doesn't exist. Also makes sure that various sub directories also exist.
	@param configPath: an optional path which should be used instead (only useful when being called from outside of NVDA)
	@type configPath: basestring
	"""
	if not configPath:
		configPath=globalVars.appArgs.configPath
	if not os.path.isdir(configPath):
		os.makedirs(configPath)
	subdirs=["speechDicts","profiles"]
	if not isAppX:
		subdirs.extend(["addons", "appModules","brailleDisplayDrivers","synthDrivers","globalPlugins"])
	for subdir in subdirs:
		subdir=os.path.join(configPath,subdir)
		if not os.path.isdir(subdir):
			os.makedirs(subdir)

RUN_REGKEY = ur"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

def getStartAfterLogon():
	if (easeOfAccess.isSupported and easeOfAccess.canConfigTerminateOnDesktopSwitch
			and easeOfAccess.willAutoStart(_winreg.HKEY_CURRENT_USER)):
		return True
	try:
		k = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, RUN_REGKEY)
		val = _winreg.QueryValueEx(k, u"nvda")[0]
		return os.stat(val) == os.stat(sys.argv[0])
	except (WindowsError, OSError):
		return False

def setStartAfterLogon(enable):
	if getStartAfterLogon() == enable:
		return
	if easeOfAccess.isSupported and easeOfAccess.canConfigTerminateOnDesktopSwitch:
		easeOfAccess.setAutoStart(_winreg.HKEY_CURRENT_USER, enable)
		if enable:
			return
		# We're disabling, so ensure the run key is cleared,
		# as it might have been set by an old version.
		run = False
	else:
		run = enable
	k = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, RUN_REGKEY, 0, _winreg.KEY_WRITE)
	if run:
		_winreg.SetValueEx(k, u"nvda", None, _winreg.REG_SZ, sys.argv[0])
	else:
		try:
			_winreg.DeleteValue(k, u"nvda")
		except WindowsError:
			pass

def canStartOnSecureScreens():
	# No more need to check for the NVDA service nor presence of Ease of Access, as only Windows 7 SP1 and higher is supported.
	# This function will be transformed into a flag in a future release.
	return isInstalledCopy()

def execElevated(path, params=None, wait=False,handleAlreadyElevated=False):
	import subprocess
	import shellapi
	import winUser
	if params is not None:
		params = subprocess.list2cmdline(params)
	sei = shellapi.SHELLEXECUTEINFO(lpFile=os.path.abspath(path), lpParameters=params, nShow=winUser.SW_HIDE)
	#IsUserAnAdmin is apparently deprecated so may not work above Windows 8
	if not handleAlreadyElevated or not ctypes.windll.shell32.IsUserAnAdmin():
		sei.lpVerb=u"runas"
	if wait:
		sei.fMask = shellapi.SEE_MASK_NOCLOSEPROCESS
	shellapi.ShellExecuteEx(sei)
	if wait:
		try:
			h=ctypes.wintypes.HANDLE(sei.hProcess)
			msg=ctypes.wintypes.MSG()
			while ctypes.windll.user32.MsgWaitForMultipleObjects(1,ctypes.byref(h),False,-1,255)==1:
				while ctypes.windll.user32.PeekMessageW(ctypes.byref(msg),None,0,0,1):
					ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
					ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
			return winKernel.GetExitCodeProcess(sei.hProcess)
		finally:
			winKernel.closeHandle(sei.hProcess)

SLAVE_FILENAME = u"nvda_slave.exe"

#: The name of the registry key stored under  HKEY_LOCAL_MACHINE where system wide NVDA settings are stored.
#: Note that NVDA is a 32-bit application, so on X64 systems, this will evaluate to "SOFTWARE\WOW6432Node\nvda"
NVDA_REGKEY = ur"SOFTWARE\NVDA"

def getStartOnLogonScreen():
	if easeOfAccess.isSupported and easeOfAccess.willAutoStart(_winreg.HKEY_LOCAL_MACHINE):
		return True
	try:
		k = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, NVDA_REGKEY)
		return bool(_winreg.QueryValueEx(k, u"startOnLogonScreen")[0])
	except WindowsError:
		return False

def _setStartOnLogonScreen(enable):
	if easeOfAccess.isSupported:
		# The installer will have migrated service config to EoA if appropriate,
		# so we only need to deal with EoA here.
		easeOfAccess.setAutoStart(_winreg.HKEY_LOCAL_MACHINE, enable)
	else:
		k = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, NVDA_REGKEY, 0, _winreg.KEY_WRITE)
		_winreg.SetValueEx(k, u"startOnLogonScreen", None, _winreg.REG_DWORD, int(enable))

def setSystemConfigToCurrentConfig():
	fromPath=os.path.abspath(globalVars.appArgs.configPath)
	if ctypes.windll.shell32.IsUserAnAdmin():
		_setSystemConfig(fromPath)
	else:
		res=execElevated(SLAVE_FILENAME, (u"setNvdaSystemConfig", fromPath), wait=True)
		if res==2:
			raise installer.RetriableFailure
		elif res!=0:
			raise RuntimeError("Slave failure")

def _setSystemConfig(fromPath):
	import installer
	toPath=os.path.join(sys.prefix.decode('mbcs'),'systemConfig')
	if os.path.isdir(toPath):
		installer.tryRemoveFile(toPath)
	for curSourceDir,subDirs,files in os.walk(fromPath):
		if curSourceDir==fromPath:
			curDestDir=toPath
		else:
			curDestDir=os.path.join(toPath,os.path.relpath(curSourceDir,fromPath))
		if not os.path.isdir(curDestDir):
			os.makedirs(curDestDir)
		for f in files:
			# Do not copy executables to the system configuration, as this may cause security risks.
			# This will also exclude pending updates.
			if f.endswith(".exe"):
				log.debug("Ignored file %s while copying current user configuration to system configuration"%f)
				continue
			sourceFilePath=os.path.join(curSourceDir,f)
			destFilePath=os.path.join(curDestDir,f)
			installer.tryCopyFile(sourceFilePath,destFilePath)

def setStartOnLogonScreen(enable):
	if getStartOnLogonScreen() == enable:
		return
	try:
		# Try setting it directly.
		_setStartOnLogonScreen(enable)
	except WindowsError:
		# We probably don't have admin privs, so we need to elevate to do this using the slave.
		if execElevated(SLAVE_FILENAME, (u"config_setStartOnLogonScreen", u"%d" % enable), wait=True) != 0:
			raise RuntimeError("Slave failed to set startOnLogonScreen")

def getConfigDirs(subpath=None):
	"""Retrieve all directories that should be used when searching for configuration.
	IF C{subpath} is provided, it will be added to each directory returned.
	@param subpath: The path to be added to each directory, C{None} for none.
	@type subpath: str
	@return: The configuration directories in the order in which they should be searched.
	@rtype: list of str
	"""
	return [os.path.join(dir, subpath) if subpath else dir
		for dir in (globalVars.appArgs.configPath,)
	]

def addConfigDirsToPythonPackagePath(module, subdir=None):
	"""Add the configuration directories to the module search path (__path__) of a Python package.
	C{subdir} is added to each configuration directory. It defaults to the name of the Python package.
	@param module: The root module of the package.
	@type module: module
	@param subdir: The subdirectory to be used, C{None} for the name of C{module}.
	@type subdir: str
	"""
	if isAppX or globalVars.appArgs.disableAddons:
		return
	if not subdir:
		subdir = module.__name__
	# Python 2.x doesn't properly handle unicode import paths, so convert them.
	dirs = [dir.encode("mbcs") for dir in getConfigDirs(subdir)]
	dirs.extend(module.__path__ )
	module.__path__ = dirs
	# FIXME: this should not be coupled to the config module....
	import addonHandler
	for addon in addonHandler.getRunningAddons():
		addon.addToPackagePath(module)

class ConfigManager(object):
	"""Manages and provides access to configuration.
	In addition to the base configuration, there can be multiple active configuration profiles.
	Settings in more recently activated profiles take precedence,
	with the base configuration being consulted last.
	This allows a profile to override settings in profiles activated earlier and the base configuration.
	A profile need only include a subset of the available settings.
	Changed settings are written to the most recently activated profile.
	"""

	#: Sections that only apply to the base configuration;
	#: i.e. they cannot be overridden in profiles.
	BASE_ONLY_SECTIONS = {"general", "update", "upgrade"}

	def __init__(self):
		self.spec = confspec
		#: All loaded profiles by name.
		self._profileCache = {}
		#: The active profiles.
		self.profiles = []
		#: Whether profile triggers are enabled (read-only).
		#: @type: bool
		self.profileTriggersEnabled = True
		self.validator = Validator()
		self.rootSection = None
		self._shouldHandleProfileSwitch = True
		self._pendingHandleProfileSwitch = False
		self._suspendedTriggers = None
		# Never save the config if running securely or if running from the launcher.
		# When running from the launcher we don't save settings because the user may decide not to
		# install this version, and these settings may not be compatible with the already
		# installed version. See #7688
		self._shouldWriteProfile = not (globalVars.appArgs.secure or globalVars.appArgs.launcher)
		self._initBaseConf()
		#: Maps triggers to profiles.
		self.triggersToProfiles = None
		self._loadProfileTriggers()
		#: The names of all profiles that have been modified since they were last saved.
		self._dirtyProfiles = set()

	def _handleProfileSwitch(self):
		if not self._shouldHandleProfileSwitch:
			self._pendingHandleProfileSwitch = True
			return
		init = self.rootSection is None
		# Reset the cache.
		self.rootSection = AggregatedSection(self, (), self.spec, self.profiles)
		if init:
			# We're still initialising, so don't notify anyone about this change.
			return
		configProfileSwitched.notify()

	def _initBaseConf(self, factoryDefaults=False):
		fn = os.path.join(globalVars.appArgs.configPath, "nvda.ini")
		if factoryDefaults:
			profile = self._loadConfig(None)
			profile.filename = fn
		else:
			try:
				profile = self._loadConfig(fn) # a blank config returned if fn does not exist
				self.baseConfigError = False
			except:
				log.error("Error loading base configuration", exc_info=True)
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
		log.info(u"Loading config: {0}".format(fn))
		profile = ConfigObj(fn, indent_type="\t", encoding="UTF-8", file_error=fileError)
		# Python converts \r\n to \n when reading files in Windows, so ConfigObj can't determine the true line ending.
		profile.newlines = "\r\n"
		profileCopy = deepcopy(profile)
		try:
			writeProfileFunc = self._writeProfileToFile if self._shouldWriteProfile else None
			profileUpgrader.upgrade(profile, self.validator, writeProfileFunc)
		except Exception as e:
			# Log at level info to ensure that the profile is logged.
			log.info(u"Config before schema update:\n%s" % profileCopy, exc_info=False)
			raise e
		# since profile settings are not yet imported we have to "peek" to see
		# if debug level logging is enabled.
		try:
			logLevelName = profile["general"]["loggingLevel"]
		except KeyError as e:
			logLevelName = None
		if log.isEnabledFor(log.DEBUG) or (logLevelName and DEBUG >= levelNames.get(logLevelName)):
			# Log at level info to ensure that the profile is logged.
			log.info(u"Config loaded (after upgrade, and in the state it will be used by NVDA):\n{0}".format(profile))
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

	def listProfiles(self):
		for name in os.listdir(os.path.join(globalVars.appArgs.configPath, "profiles")):
			name, ext = os.path.splitext(name)
			if ext == ".ini":
				yield name

	def _getProfileFn(self, name):
		return os.path.join(globalVars.appArgs.configPath, "profiles", name + ".ini")

	def _getProfile(self, name, load=True):
		try:
			return self._profileCache[name]
		except KeyError:
			if not load:
				raise KeyError(name)

		# Load the profile.
		fn = self._getProfileFn(name)
		profile = self._loadConfig(fn, fileError = True) # file must exist.
		profile.name = name
		profile.manual = False
		profile.triggered = False
		self._profileCache[name] = profile
		return profile

	def getProfile(self, name):
		"""Get a profile given its name.
		This is useful for checking whether a profile has been manually activated or triggered.
		@param name: The name of the profile.
		@type name: basestring
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
		@type name: basestring
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
		"""Save all modified profiles and the base configuration to disk.
		"""
		if not self._shouldWriteProfile:
			log.info("Not writing profile, either --secure or --launcher args present")
			return
		try:
			self._writeProfileToFile(self.profiles[0].filename, self.profiles[0])
			log.info("Base configuration saved")
			for name in self._dirtyProfiles:
				self._writeProfileToFile(self._profileCache[name].filename, self._profileCache[name])
				log.info("Saved configuration profile %s" % name)
			self._dirtyProfiles.clear()
		except Exception as e:
			log.warning("Error saving configuration; probably read only file system")
			log.debugWarning("", exc_info=True)
			raise e

	def reset(self, factoryDefaults=False):
		"""Reset the configuration to saved settings or factory defaults.
		@param factoryDefaults: C{True} to reset to factory defaults, C{False} to reset to saved configuration.
		@type factoryDefaults: bool
		"""
		self.profiles = []
		self._profileCache.clear()
		# Signal that we're initialising.
		self.rootSection = None
		self._initBaseConf(factoryDefaults=factoryDefaults)

	def createProfile(self, name):
		"""Create a profile.
		@param name: The name of the profile ot create.
		@type name: basestring
		@raise ValueError: If a profile with this name already exists.
		"""
		if globalVars.appArgs.secure:
			return
		fn = self._getProfileFn(name)
		if os.path.isfile(fn):
			raise ValueError("A profile with the same name already exists: %s" % name)
		# Just create an empty file to make sure we can.
		file(fn, "w")

	def deleteProfile(self, name):
		"""Delete a profile.
		@param name: The name of the profile to delete.
		@type name: basestring
		@raise LookupError: If the profile doesn't exist.
		"""
		if globalVars.appArgs.secure:
			return
		fn = self._getProfileFn(name)
		if not os.path.isfile(fn):
			raise LookupError("No such profile: %s" % name)
		os.remove(fn)
		try:
			del self._profileCache[name]
		except KeyError:
			pass
		# Remove any triggers associated with this profile.
		allTriggers = self.triggersToProfiles
		# You can't delete from a dict while iterating through it.
		delTrigs = [trigSpec for trigSpec, trigProfile in allTriggers.iteritems()
			if trigProfile == name]
		if delTrigs:
			for trigSpec in delTrigs:
				del allTriggers[trigSpec]
			self.saveProfileTriggers()
		# Check if this profile was active.
		delProfile = None
		for index in xrange(len(self.profiles) - 1, -1, -1):
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
			for trigger in self._suspendedTriggers.keys():
				if trigger._profile == delProfile:
					del self._suspendedTriggers[trigger]

	def renameProfile(self, oldName, newName):
		"""Rename a profile.
		@param oldName: The current name of the profile.
		@type oldName: basestring
		@param newName: The new name for the profile.
		@type newName: basestring
		@raise LookupError: If the profile doesn't exist.
		@raise ValueError: If a profile with the new name already exists.
		"""
		if globalVars.appArgs.secure:
			return
		if newName == oldName:
			return
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
		for trigSpec, trigProfile in allTriggers.iteritems():
			if trigProfile == oldName:
				allTriggers[trigSpec] = newName
				saveTrigs = True
		if saveTrigs:
			self.saveProfileTriggers()
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
		"""Called by L{ProfileTrigger.enter}}}.
		"""
		if not self.profileTriggersEnabled:
			return
		if self._suspendedTriggers is not None:
			self._suspendedTriggers[trigger] = "enter"
			return

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
		self._handleProfileSwitch()

	def _triggerProfileExit(self, trigger):
		"""Called by L{ProfileTrigger.exit}}}.
		"""
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
		profile.triggered = False
		try:
			self.profiles.remove(profile)
		except ValueError:
			# This is probably due to the user resetting the configuration.
			log.debugWarning("Profile not active when exiting trigger")
			return
		self._handleProfileSwitch()

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
			for trigger, action in triggers.iteritems():
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
		"""Re-enable profile triggers after they were previously disabled.
		"""
		self.profileTriggersEnabled = True

	def _loadProfileTriggers(self):
		fn = os.path.join(globalVars.appArgs.configPath, "profileTriggers.ini")
		try:
			cobj = ConfigObj(fn, indent_type="\t", encoding="UTF-8")
		except:
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

	def getConfigValidationParameter(self, keyPath, validationParameter):
		"""Get a config validation parameter
		This can be used to get the min, max, default, or other values for a config key.
		@param keyPath: a sequence of the identifiers leading to the config key. EG ("braille", "messageTimeout")
		@param validationParameter: the parameter to return the value for. EG "max"
		@type validationParameter: string
		"""
		if not keyPath or len(keyPath) < 1:
			raise ValueError("Key path not provided")

		spec = conf.spec
		for nextKey in keyPath:
			spec = spec[nextKey]
		return conf.validator._parse_with_caching(spec)[2][validationParameter]

class AggregatedSection(object):
	"""A view of a section of configuration which aggregates settings from all active profiles.
	"""

	def __init__(self, manager, path, spec, profiles):
		self.manager = manager
		self.path = path
		self._spec = spec
		#: The relevant section in all of the profiles.
		self.profiles = profiles
		self._cache = {}

	def __getitem__(self, key, checkValidity=True):
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
		if isinstance(spec, dict):
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
			if isinstance(val, dict):
				foundSection = True
				subProfiles.append(val)
			else:
				# This is a setting.
				if not checkValidity:
					spec = None
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

	def iteritems(self):
		keys = set()
		# Start with the cached items.
		for key, val in self._cache.iteritems():
			keys.add(key)
			if val is not KeyError:
				yield key, val
		# Walk through the profiles and spec looking for items not yet cached.
		for profile in itertools.chain(reversed(self.profiles), (self._spec,)):
			if not profile:
				continue
			for key in profile:
				if key in keys:
					continue
				keys.add(key)
				# Use __getitem__ so caching, AggregatedSections, etc. are handled.
				try:
					yield key, self[key]
				except KeyError:
					# This could happen if the item is in the spec but there's no default.
					pass

	def copy(self):
		return dict(self.iteritems())

	def __setitem__(self, key, val):
		spec = self._spec.get(key) if self.spec else None
		if isinstance(spec, dict) and not isinstance(val, dict):
			raise ValueError("Value must be a section")

		if isinstance(spec, dict) or isinstance(val, dict):
			# The value is a section.
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
			if val == curVal:
				# The value isn't different, so there's nothing to do.
				return

		# Set this value in the most recently activated profile.
		self._getUpdateSection()[key] = val
		self.manager._markWriteProfileDirty()
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

	@baseObject.Getter
	def spec(self):
		"""The trigger specification.
		This is a string used to search for this trigger in the user's configuration.
		@rtype: basestring
		"""
		raise NotImplementedError

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
		except:
			log.error("Error entering trigger %s, profile %s"
				% (self.spec, self.profileName), exc_info=True)
	__enter__ = enter

	def exit(self):
		"""Signal that this trigger no longer applies.
		The associated profile (if any) will be deactivated.
		"""
		if not self.profileName:
			return
		try:
			conf._triggerProfileExit(self)
		except:
			log.error("Error exiting trigger %s, profile %s"
				% (self.spec, self.profileName), exc_info=True)

	def __exit__(self, excType, excVal, traceback):
		self.exit()

TokenUIAccess = 26
def hasUiAccess():
	token = ctypes.wintypes.HANDLE()
	ctypes.windll.advapi32.OpenProcessToken(ctypes.windll.kernel32.GetCurrentProcess(),
		winKernel.MAXIMUM_ALLOWED, ctypes.byref(token))
	try:
		val = ctypes.wintypes.DWORD()
		ctypes.windll.advapi32.GetTokenInformation(token, TokenUIAccess,
			ctypes.byref(val), ctypes.sizeof(ctypes.wintypes.DWORD),
			ctypes.byref(ctypes.wintypes.DWORD()))
		return bool(val.value)
	finally:
		ctypes.windll.kernel32.CloseHandle(token)
