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
from collections import OrderedDict
from configobj import ConfigObj, ConfigObjError
from validate import Validator
from logHandler import log
import shlobj
import baseObject
import easeOfAccess
import winKernel

def validateConfig(configObj,validator,validationResult=None,keyList=None):
	"""
	@deprecated: Add-ons which need this should provide their own implementation.
	"""
	import warnings
	warnings.warn("config.validateConfig deprecated. Callers should provide their own implementation.",
		DeprecationWarning, 2)
	if validationResult is None:
		validationResult=configObj.validate(validator,preserve_errors=True)
	if validationResult is True:
		return None #No errors
	if validationResult is False:
		return "Badly formed configuration file"
	errorStrings=[]
	for k,v in validationResult.iteritems():
		if v is True:
			continue
		newKeyList=list(keyList) if keyList is not None else []
		newKeyList.append(k)
		if isinstance(v,dict):
			errorStrings.extend(validateConfig(configObj[k],validator,v,newKeyList))
		else:
			#If a key is invalid configObj does not record its default, thus we need to get and set the default manually 
			defaultValue=validator.get_default_value(configObj.configspec[k])
			configObj[k]=defaultValue
			if k not in configObj.defaults:
				configObj.defaults.append(k)
			errorStrings.append("%s: %s, defaulting to %s"%(k,v,defaultValue))
	return errorStrings

#: @deprecated: Use C{conf.validator} instead.
val = Validator()

#: The configuration specification
#: @type: ConfigObj
confspec = ConfigObj(StringIO(
"""# NVDA Configuration File

[general]
	language = string(default="Windows")
	saveConfigurationOnExit = boolean(default=True)
	askToExit = boolean(default=true)
	playStartAndExitSounds = boolean(default=true)
	#possible log levels are DEBUG, IO, DEBUGWARNING, INFO
	loggingLevel = string(default="INFO")
	showWelcomeDialogAtStartup = boolean(default=true)

# Speech settings
[speech]
	# The synthesiser to use
	synth = string(default=auto)
	symbolLevel = integer(default=100)
	trustVoiceLanguage = boolean(default=true)
	beepSpeechModePitch = integer(default=10000,min=50,max=11025)
	outputDevice = string(default=default)
	autoLanguageSwitching = boolean(default=true)
	autoDialectSwitching = boolean(default=false)

	[[__many__]]
		capPitchChange = integer(default=30,min=-100,max=100)
		sayCapForCapitals = boolean(default=false)
		beepForCapitals = boolean(default=false)
		useSpellingFunctionality = boolean(default=true)

# Braille settings
[braille]
	display = string(default=noBraille)
	translationTable = string(default=en-us-comp8.ctb)
	inputTable = string(default=en-us-comp8.ctb)
	expandAtCursor = boolean(default=true)
	cursorBlinkRate = integer(default=500,min=0,max=2000)
	messageTimeout = integer(default=4,min=0,max=20)
	tetherTo = string(default="focus")
	readByParagraph = boolean(default=false)
	wordWrap = boolean(default=true)

	# Braille display driver settings
	[[__many__]]
		port = string(default="")

# Presentation settings
[presentation]
		reportKeyboardShortcuts = boolean(default=true)
		reportObjectPositionInformation = boolean(default=true)
		guessObjectPositionInformationWhenUnavailable = boolean(default=false)
		reportTooltips = boolean(default=false)
		reportHelpBalloons = boolean(default=true)
		reportObjectDescriptions = boolean(default=True)
		reportDynamicContentChanges = boolean(default=True)
	[[progressBarUpdates]]
		reportBackgroundProgressBars = boolean(default=false)
		#output modes are beep, speak, both, or off
		progressBarOutputMode = string(default="beep")
		speechPercentageInterval = integer(default=10)
		beepPercentageInterval = integer(default=1)
		beepMinHZ = integer(default=110)

[mouse]
	enableMouseTracking = boolean(default=True) #must be true for any of the other settings to work
	mouseTextUnit = string(default="paragraph")
	reportObjectRoleOnMouseEnter = boolean(default=False)
	audioCoordinatesOnMouseMove = boolean(default=False)
	audioCoordinates_detectBrightness = boolean(default=False)
	audioCoordinates_blurFactor = integer(default=3)
	audioCoordinates_minVolume = float(default=0.1)
	audioCoordinates_maxVolume = float(default=1.0)
	audioCoordinates_minPitch = integer(default=220)
	audioCoordinates_maxPitch = integer(default=880)
	reportMouseShapeChanges = boolean(default=false)

#Keyboard settings
[keyboard]
	useCapsLockAsNVDAModifierKey = boolean(default=false)
	useNumpadInsertAsNVDAModifierKey = boolean(default=true)
	useExtendedInsertAsNVDAModifierKey = boolean(default=true)
	keyboardLayout = string(default="desktop")
	speakTypedCharacters = boolean(default=true)
	speakTypedWords = boolean(default=false)
	beepForLowercaseWithCapslock = boolean(default=true)
	speakCommandKeys = boolean(default=false)
	speechInterruptForCharacters = boolean(default=true)
	speechInterruptForEnter = boolean(default=true)
	allowSkimReadingInSayAll = boolean(default=False)
	handleInjectedKeys= boolean(default=true)

[virtualBuffers]
	maxLineLength = integer(default=100)
	linesPerPage = integer(default=25)
	useScreenLayout = boolean(default=True)
	autoPassThroughOnFocusChange = boolean(default=true)
	autoPassThroughOnCaretMove = boolean(default=false)
	passThroughAudioIndication = boolean(default=true)
	autoSayAllOnPageLoad = boolean(default=true)
	trapNonCommandGestures = boolean(default=true)

#Settings for document reading (such as MS Word and wordpad)
[documentFormatting]
	#These settings affect what information is reported when you navigate to text where the formatting  or placement has changed
	detectFormatAfterCursor = boolean(default=false)
	reportFontName = boolean(default=false)
	reportFontSize = boolean(default=false)
	reportFontAttributes = boolean(default=false)
	reportRevisions = boolean(default=true)
	reportEmphasis = boolean(default=false)
	reportColor = boolean(default=False)
	reportAlignment = boolean(default=false)
	reportStyle = boolean(default=false)
	reportSpellingErrors = boolean(default=true)
	reportPage = boolean(default=true)
	reportLineNumber = boolean(default=False)
	reportLineIndentation = boolean(default=False)
	reportParagraphIndentation = boolean(default=False)
	reportTables = boolean(default=true)
	includeLayoutTables = boolean(default=False)
	reportTableHeaders = boolean(default=True)
	reportTableCellCoords = boolean(default=True)
	reportLinks = boolean(default=true)
	reportComments = boolean(default=true)
	reportLists = boolean(default=true)
	reportHeadings = boolean(default=true)
	reportBlockQuotes = boolean(default=true)
	reportLandmarks = boolean(default=true)
	reportFrames = boolean(default=true)
	reportClickable = boolean(default=true)

[reviewCursor]
	simpleReviewMode = boolean(default=True)
	followFocus = boolean(default=True)
	followCaret = boolean(default=True)
	followMouse = boolean(default=False)

[UIA]
	minWindowsVersion = float(default=6.1)
	enabled = boolean(default=true)

[update]
	autoCheck = boolean(default=true)

[inputComposition]
	autoReportAllCandidates = boolean(default=True)
	announceSelectedCandidate = boolean(default=True)
	alwaysIncludeShortCharacterDescriptionInCandidateName = boolean(default=True)
	reportReadingStringChanges = boolean(default=True)
	reportCompositionStringChanges = boolean(default=True)

[upgrade]
	newLaptopKeyboardLayout = boolean(default=false)
"""
), list_values=False, encoding="UTF-8")
confspec.newlines = "\r\n"

#: The active configuration, C{None} if it has not yet been loaded.
#: @type: ConfigObj
conf = None

def initialize():
	global conf
	conf = ConfigManager()

def save():
	"""
	@deprecated: Use C{conf.save} instead.
	"""
	import warnings
	warnings.warn("config.save deprecated. Use config.conf.save instead.",
		DeprecationWarning, 2)
	conf.save()

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


def getInstalledUserConfigPath():
	try:
		return os.path.join(shlobj.SHGetFolderPath(0, shlobj.CSIDL_APPDATA), "nvda")
	except WindowsError:
		return None

def getUserDefaultConfigPath(useInstalledPathIfExists=False):
	"""Get the default path for the user configuration directory.
	This is the default path and doesn't reflect overriding from the command line,
	which includes temporary copies.
	Most callers will want the C{globalVars.appArgs.configPath variable} instead.
	"""
	installedUserConfigPath=getInstalledUserConfigPath()
	if installedUserConfigPath and (isInstalledCopy() or (useInstalledPathIfExists and os.path.isdir(installedUserConfigPath))):
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
	for subdir in ("addons", "appModules","brailleDisplayDrivers","speechDicts","synthDrivers","globalPlugins","profiles"):
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

SERVICE_FILENAME = u"nvda_service.exe"

def isServiceInstalled():
	if not os.path.isfile(SERVICE_FILENAME):
		return False
	try:
		k = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, ur"SYSTEM\CurrentControlSet\Services\nvda")
		val = _winreg.QueryValueEx(k, u"ImagePath")[0].replace(u'"', u'')
		return os.stat(val) == os.stat(SERVICE_FILENAME)
	except (WindowsError, OSError):
		return False

def canStartOnSecureScreens():
	return isInstalledCopy() and (easeOfAccess.isSupported or isServiceInstalled())

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
	if globalVars.appArgs.disableAddons:
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
		self.validator = val
		self.rootSection = None
		self._shouldHandleProfileSwitch = True
		self._pendingHandleProfileSwitch = False
		self._suspendedTriggers = None
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
		import synthDriverHandler
		synthDriverHandler.handleConfigProfileSwitch()
		import braille
		braille.handler.handleConfigProfileSwitch()

	def _initBaseConf(self, factoryDefaults=False):
		fn = os.path.join(globalVars.appArgs.configPath, "nvda.ini")
		if factoryDefaults:
			profile = ConfigObj(None, indent_type="\t", encoding="UTF-8")
			profile.filename = fn
		else:
			try:
				profile = ConfigObj(fn, indent_type="\t", encoding="UTF-8")
				self.baseConfigError = False
			except:
				log.error("Error loading base configuration", exc_info=True)
				self.baseConfigError = True
				return self._initBaseConf(factoryDefaults=True)
		# Python converts \r\n to \n when reading files in Windows, so ConfigObj can't determine the true line ending.
		profile.newlines = "\r\n"

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
		profile = ConfigObj(fn, indent_type="\t", encoding="UTF-8", file_error=True)
		# Python converts \r\n to \n when reading files in Windows, so ConfigObj can't determine the true line ending.
		profile.newlines = "\r\n"
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

	def save(self):
		"""Save all modified profiles and the base configuration to disk.
		"""
		if globalVars.appArgs.secure:
			# Never save the config if running securely.
			return
		try:
			self.profiles[0].write()
			log.info("Base configuration saved")
			for name in self._dirtyProfiles:
				self._profileCache[name].write()
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

	def __getitem__(self, key):
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
			curVal = self[key]
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
