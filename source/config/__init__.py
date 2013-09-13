"""Manages NVDA configuration.
""" 

import globalVars
import _winreg
import ctypes
import ctypes.wintypes
from copy import deepcopy
import os
import sys
from cStringIO import StringIO
from configobj import ConfigObj, ConfigObjError
from validate import Validator
from logHandler import log
import shlobj

def validateConfig(configObj,validator,validationResult=None,keyList=None):
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

val = Validator()

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
	allowSkimReadingInSayAll = boolean(default=False)

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
#: template config spec for concrete synthesizer's settings. It is used in SynthDriver.getConfigSpec() to build a real spec
#: @type: L{configobj.Section}
synthSpec=None

def load(factoryDefaults=False):
	"""Loads the configuration from the configFile.
	It also takes note of the file's modification time so that L{save} won't lose any changes made to the file while NVDA is running. 
	"""
	global conf,synthSpec
	configFileName=os.path.join(globalVars.appArgs.configPath,"nvda.ini")
	if factoryDefaults:
		conf = ConfigObj(None, configspec = confspec, indent_type = "\t", encoding="UTF-8")
		conf.filename=configFileName
	else:
		try:
			conf = ConfigObj(configFileName, configspec = confspec, indent_type = "\t", encoding="UTF-8")
		except ConfigObjError as e:
			conf = ConfigObj(None, configspec = confspec, indent_type = "\t", encoding="UTF-8")
			conf.filename=configFileName
			globalVars.configFileError="Error parsing configuration file: %s"%e
	# Python converts \r\n to \n when reading files in Windows, so ConfigObj can't determine the true line ending.
	conf.newlines = "\r\n"
	errorList=validateConfig(conf,val)
	if synthSpec is None: 
		synthSpec=deepcopy(conf["speech"].configspec["__many__"])
	if errorList:
		globalVars.configFileError="Errors in configuration file '%s':\n%s"%(conf.filename,"\n".join(errorList))
	if globalVars.configFileError:
		log.warn(globalVars.configFileError)

def save():
	"""Saves the configuration to the config file.
	"""
	#We never want to save config if runing securely
	if globalVars.appArgs.secure: return
	global conf
	if globalVars.configFileError:
		raise RuntimeError("config file errors still exist")
	if not os.path.isdir(globalVars.appArgs.configPath):
		try:
			os.makedirs(globalVars.appArgs.configPath)
		except OSError, e:
			log.warning("Could not create configuration directory")
			log.debugWarning("", exc_info=True)
			raise e
	try:
		# Copy default settings and formatting.
		conf.validate(val, copy = True)
		conf.write()
		log.info("Configuration saved")
	except Exception, e:
		log.warning("Could not save configuration - probably read only file system")
		log.debugWarning("", exc_info=True)
		raise e

def saveOnExit():
	"""Save the configuration if configured to save on exit.
	This should only be called if NVDA is about to exit.
	Errors are ignored.
	"""
	if conf["general"]["saveConfigurationOnExit"]:
		try:
			save()
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
	for subdir in ("addons", "appModules","brailleDisplayDrivers","speechDicts","synthDrivers","globalPlugins"):
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
