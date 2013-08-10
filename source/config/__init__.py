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
from configobj import ConfigObj, ConfigObjError
from validate import Validator
from logHandler import log
import shlobj

#: The configuration specification
#: @type: ConfigObj
confspec = ConfigObj(StringIO(
"""# NVDA Configuration File

[general]
	language = string(default="Windows")
	saveConfigurationOnExit = boolean(default=True)
	askToExit = boolean(default=true)
	#possible log levels are DEBUG, IO, DEBUGWARNING, INFO
	loggingLevel = string(default="INFO")
	showWelcomeDialogAtStartup = boolean(default=true)

# Speech settings
[speech]
	# The synthesiser to use
	synth = string(default=auto)
	symbolLevel = integer(default=100)
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

[virtualBuffers]
	maxLineLength = integer(default=100)
	linesPerPage = integer(default=25)
	useScreenLayout = boolean(default=True)
	autoPassThroughOnFocusChange = boolean(default=true)
	autoPassThroughOnCaretMove = boolean(default=false)
	passThroughAudioIndication = boolean(default=true)
	autoSayAllOnPageLoad = boolean(default=true)

#Settings for document reading (such as MS Word and wordpad)
[documentFormatting]
	#These settings affect what information is reported when you navigate to text where the formatting  or placement has changed
	detectFormatAfterCursor = boolean(default=false)
	reportFontName = boolean(default=false)
	reportFontSize = boolean(default=false)
	reportFontAttributes = boolean(default=false)
	reportRevisions = boolean(default=false)
	reportColor = boolean(default=False)
	reportAlignment = boolean(default=false)
	reportStyle = boolean(default=false)
	reportSpellingErrors = boolean(default=true)
	reportPage = boolean(default=true)
	reportLineNumber = boolean(default=False)
	reportLineIndentation = boolean(default=False)
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
	try:
		k = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, RUN_REGKEY)
		val = _winreg.QueryValueEx(k, u"nvda")[0]
		return os.stat(val) == os.stat(sys.argv[0])
	except (WindowsError, OSError):
		return False

def setStartAfterLogon(enable):
	if getStartAfterLogon() == enable:
		return
	k = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, RUN_REGKEY, 0, _winreg.KEY_WRITE)
	if enable:
		_winreg.SetValueEx(k, u"nvda", None, _winreg.REG_SZ, sys.argv[0])
	else:
		_winreg.DeleteValue(k, u"nvda")

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

def execElevated(path, params=None, wait=False,handleAlreadyElevated=False):
	import subprocess
	import shellapi
	import winKernel
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
	try:
		k = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, NVDA_REGKEY)
		return bool(_winreg.QueryValueEx(k, u"startOnLogonScreen")[0])
	except WindowsError:
		return False

def _setStartOnLogonScreen(enable):
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
		self.validator = Validator()
		self.rootSection = None
		self._initBaseConf()
		#: The names of all profiles that have been modified since they were last saved.
		self._dirtyProfiles = set()

	def _handleProfileSwitch(self):
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

	def _pushProfile(self, profile):
		self.profiles.append(profile)
		self._handleProfileSwitch()

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
		self._pushProfile(profile)

	def deactivateProfile(self):
		"""Deactivate the most recently activated profile.
		@raise IndexError: If there is no profile to deactivate.
		"""
		if len(self.profiles) == 1:
			raise IndexError("No profile to deactivate")
		self.profiles.pop()
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

	def _getProfile(self, name):
		try:
			return self._profileCache[name]
		except KeyError:
			pass

		# Load the profile.
		fn = self._getProfileFn(name)
		profile = ConfigObj(fn, indent_type="\t", encoding="UTF-8", file_error=True)
		# Python converts \r\n to \n when reading files in Windows, so ConfigObj can't determine the true line ending.
		profile.newlines = "\r\n"
		profile.name = name
		self._profileCache[name] = profile
		return profile

	def activateProfile(self, name):
		"""Activate a profile, loading it if appropriate.
		@param name: The name of the profile.
		@type name: basestring
		"""
		self._pushProfile(self._getProfile(name))

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
		# Signal that we're initialising.
		self.rootSection = None
		self._initBaseConf(factoryDefaults=factoryDefaults)

	def createProfile(self, name):
		"""Create a profile.
		@param name: The name of the profile ot create.
		@type name: basestring
		@raise ValueError: If a profile with this name already exists.
		"""
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
		fn = self._getProfileFn(name)
		if not os.path.isfile(fn):
			raise LookupError("No such profile: %s" % name)
		os.remove(fn)
		try:
			del self._profileCache[name]
		except KeyError:
			pass
		# Check if this profile was active.
		for index, profile in enumerate(self.profiles):
			if profile.name == name:
				break
		else:
			return
		# Deactivate it.
		del self.profiles[index]
		self._handleProfileSwitch()

	def renameProfile(self, oldName, newName):
		"""Rename a profile.
		@param oldName: The current name of the profile.
		@type oldName: basestring
		@param newName: The new name for the profile.
		@type newName: basestring
		@raise LookupError: If the profile doesn't exist.
		@raise ValueError: If a profile with the new name already exists.
		"""
		if newName == oldName:
			return
		oldFn = self._getProfileFn(oldName)
		newFn = self._getProfileFn(newName)
		if not os.path.isfile(oldFn):
			raise LookupError("No such profile: %s" % oldName)
		if os.path.isfile(newFn):
			raise ValueError("A profile with the same name already exists: %s" % newName)

		os.rename(oldFn, newFn)
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
				cache[key].profiles[-1] = val
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
