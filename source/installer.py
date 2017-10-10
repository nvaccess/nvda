#installer.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011-2017 NV Access Limited, Joseph Lee, Babbage B.V.

from ctypes import *
from ctypes.wintypes import *
import _winreg
import threading
import time
import os
import tempfile
import shutil
import itertools
import shellapi
import globalVars
import languageHandler
import config
import versionInfo
from logHandler import log
import addonHandler
import easeOfAccess

MOVEFILE_DELAY_UNTIL_REBOOT=4

_wsh=None
def _getWSH():
	global _wsh
	if not _wsh:
		import comtypes.client
		_wsh=comtypes.client.CreateObject("wScript.Shell",dynamic=True)
	return _wsh

defaultStartMenuFolder=versionInfo.name
with _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows\CurrentVersion") as k: 
	programFilesPath=_winreg.QueryValueEx(k, "ProgramFilesDir")[0] 
defaultInstallPath=os.path.join(programFilesPath, versionInfo.name)

def createShortcut(path,targetPath=None,arguments=None,iconLocation=None,workingDirectory=None,hotkey=None,prependSpecialFolder=None):
	wsh=_getWSH()
	if prependSpecialFolder:
		specialPath=wsh.SpecialFolders(prependSpecialFolder)
		path=os.path.join(specialPath,path)
	if not os.path.isdir(os.path.dirname(path)):
		os.makedirs(os.path.dirname(path))
	shortcutExists=os.path.isfile(path)
	short=wsh.CreateShortcut(path)
	short.TargetPath=targetPath
	if arguments:
		short.arguments=arguments
	if not shortcutExists and hotkey:
		short.Hotkey=hotkey
	if iconLocation:
		short.IconLocation=iconLocation
	if workingDirectory:
		short.workingDirectory=workingDirectory
	short.Save()

def getStartMenuFolder(noDefault=False):
	try:
		with _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,config.NVDA_REGKEY) as k:
			return _winreg.QueryValueEx(k,u"Start Menu Folder")[0]
	except WindowsError:
		return defaultStartMenuFolder if not noDefault else None

def getInstallPath(noDefault=False):
	try:
		k=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NVDA")
		return _winreg.QueryValueEx(k,"UninstallDirectory")[0]
	except WindowsError:
		return defaultInstallPath if not noDefault else None

def comparePreviousInstall():
	"""Returns 1 if the existing installation is newer than this running version,
	0 if it is the same, -1 if it is older,
	None if there is no existing installation.
	"""
	path = getInstallPath(True)
	if not path or not os.path.isdir(path):
		return None
	try:
		return cmp(
			os.path.getmtime(os.path.join(path, "nvda_slave.exe")),
			os.path.getmtime("nvda_slave.exe"))
	except OSError:
		return None

def getDocFilePath(fileName,installDir):
	rootPath=os.path.join(installDir,'documentation')
	lang = languageHandler.getLanguage()
	tryLangs = [lang]
	if "_" in lang:
		# This locale has a sub-locale, but documentation might not exist for the sub-locale, so try stripping it.
		tryLangs.append(lang.split("_")[0])
	# If all else fails, use English.
	tryLangs.append("en")
	fileName, fileExt = os.path.splitext(fileName)
	for tryLang in tryLangs:
		tryDir = os.path.join(rootPath, tryLang)
		if not os.path.isdir(tryDir):
			continue
		# Some out of date translations might include .txt files which are now .html files in newer translations.
		# Therefore, ignore the extension and try both .html and .txt.
		for tryExt in ("html", "txt"):
			tryPath = os.path.join(tryDir, "%s.%s" % (fileName, tryExt))
			if os.path.isfile(tryPath):
				return tryPath

def copyProgramFiles(destPath):
	sourcePath=os.getcwdu()
	detectUserConfig=True
	detectNVDAExe=True
	for curSourceDir,subDirs,files in os.walk(sourcePath):
		if detectUserConfig:
			detectUserConfig=False
			subDirs[:]=[x for x in subDirs if os.path.basename(x).lower() not in ('userconfig','systemconfig')]
		curDestDir=os.path.join(destPath,os.path.relpath(curSourceDir,sourcePath))
		if not os.path.isdir(curDestDir):
			os.makedirs(curDestDir)
		for f in files:
			#Never copy nvda.exe as one of the other executables will be renamed later
			if sourcePath==curSourceDir and f.lower()=="nvda.exe":
				continue
			sourceFilePath=os.path.join(curSourceDir,f)
			destFilePath=os.path.join(destPath,os.path.relpath(sourceFilePath,sourcePath))
			tryCopyFile(sourceFilePath,destFilePath)

def copyUserConfig(destPath):
	sourcePath=os.path.abspath(globalVars.appArgs.configPath)
	for curSourceDir,subDirs,files in os.walk(sourcePath):
		curDestDir=os.path.join(destPath,os.path.relpath(curSourceDir,sourcePath))
		if not os.path.isdir(curDestDir):
			os.makedirs(curDestDir)
		for f in files:
			sourceFilePath=os.path.join(curSourceDir,f)
			destFilePath=os.path.join(destPath,os.path.relpath(sourceFilePath,sourcePath))
			tryCopyFile(sourceFilePath,destFilePath)

def removeOldProgramFiles(destPath):
	# #3181: Remove espeak-ng-data\voices except for variants.
	# Otherwise, there will be duplicates if voices have been moved in this new eSpeak version.
	root = os.path.join(destPath, "synthDrivers", "espeak-ng-data", "voices")
	try:
		files = set(os.listdir(root))
	except OSError:
		pass
	else:
		# Don't remove variants.
		files.discard("!v")
		for fn in files:
			fn = os.path.join(root, fn)
			# No need to use tryRemoveFile here because these files should never be locked.
			if os.path.isdir(fn):
				shutil.rmtree(fn)
			else:
				os.remove(fn)

	# #7546: Remove old version-specific libs
	for topDir in ('lib','lib64'):
		for parent,subdirs,files in os.walk(os.path.join(destPath,topDir),topdown=False):
			for d in subdirs:
				path=os.path.join(parent,d)
				try:
					os.rmdir(path)
				except OSError as e:
					log.debugWarning("Failed to remove directory %s, %s"%(path,e))
			for f in files:
				tryRemoveFile(os.path.join(parent,f),tempDir=destPath)

	# #4235: mpr.dll is a Windows system dll accidentally included with
	# earlier versions of NVDA. Its presence causes problems in Windows Vista.
	fn = os.path.join(destPath, "mpr.dll")
	if os.path.isfile(fn):
		tryRemoveFile(fn)

uninstallerRegInfo={
	"DisplayName":versionInfo.name,
	"DisplayVersion":versionInfo.version,
	"DisplayIcon":u"{installDir}\\images\\nvda.ico",
	"InstallDir":u"{installDir}",
	"Publisher":versionInfo.publisher,
	"UninstallDirectory":u"{installDir}",
	"UninstallString":u"{installDir}\\uninstall.exe",
	"URLInfoAbout":versionInfo.url,
}

def registerInstallation(installDir,startMenuFolder,shouldCreateDesktopShortcut,startOnLogonScreen,configInLocalAppData=False):
	import _winreg
	with _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\NVDA",0,_winreg.KEY_WRITE) as k:
		for name,value in uninstallerRegInfo.iteritems(): 
			_winreg.SetValueEx(k,name,None,_winreg.REG_SZ,value.format(installDir=installDir))
	with _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\nvda.exe",0,_winreg.KEY_WRITE) as k:
		_winreg.SetValueEx(k,"",None,_winreg.REG_SZ,os.path.join(installDir,"nvda.exe"))
	with _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE,config.NVDA_REGKEY,0,_winreg.KEY_WRITE) as k:
		_winreg.SetValueEx(k,"startMenuFolder",None,_winreg.REG_SZ,startMenuFolder)
		if configInLocalAppData:
			_winreg.SetValueEx(k,config.CONFIG_IN_LOCAL_APPDATA_SUBKEY,None,_winreg.REG_DWORD,int(configInLocalAppData))
	if easeOfAccess.isSupported:
		registerEaseOfAccess(installDir)
	else:
		import nvda_service
		nvda_service.installService(installDir)
		nvda_service.startService()
	if startOnLogonScreen is not None:
		config._setStartOnLogonScreen(startOnLogonScreen)
	NVDAExe=os.path.join(installDir,u"nvda.exe")
	slaveExe=os.path.join(installDir,u"nvda_slave.exe")
	if shouldCreateDesktopShortcut:
		# Translators: The shortcut key used to start NVDA.
		# This should normally be left as is, but might be changed for some locales
		# if the default key causes problems for the normal locale keyboard layout.
		# The key must be formatted as described in this article:
		# http://msdn.microsoft.com/en-us/library/3zb1shc6%28v=vs.84%29.aspx
		createShortcut(u"NVDA.lnk",targetPath=slaveExe,arguments="launchNVDA -r",hotkey=_("CTRL+ALT+N"),workingDirectory=installDir,prependSpecialFolder="AllUsersDesktop")
	createShortcut(os.path.join(startMenuFolder,"NVDA.lnk"),targetPath=NVDAExe,workingDirectory=installDir,prependSpecialFolder="AllUsersPrograms")
	# Translators: A label for a shortcut in start menu and a menu entry in NVDA menu (to go to NVDA website).
	createShortcut(os.path.join(startMenuFolder,_("NVDA web site")+".lnk"),targetPath=versionInfo.url,prependSpecialFolder="AllUsersPrograms")
	# Translators: A label for a shortcut item in start menu to uninstall NVDA from the computer.
	createShortcut(os.path.join(startMenuFolder,_("Uninstall NVDA")+".lnk"),targetPath=os.path.join(installDir,"uninstall.exe"),workingDirectory=installDir,prependSpecialFolder="AllUsersPrograms")
	# Translators: A label for a shortcut item in start menu to open current user's NVDA configuration directory.
	createShortcut(os.path.join(startMenuFolder,_("Explore NVDA user configuration directory")+".lnk"),targetPath=slaveExe,arguments="explore_userConfigPath",workingDirectory=installDir,prependSpecialFolder="AllUsersPrograms")
	# Translators: The label of the NVDA Documentation menu in the Start Menu.
	docFolder=os.path.join(startMenuFolder,_("Documentation"))
	# Translators: The label of the Start Menu item to open the Commands Quick Reference document.
	createShortcut(os.path.join(docFolder,_("Commands Quick Reference")+".lnk"),targetPath=getDocFilePath("keyCommands.html",installDir),prependSpecialFolder="AllUsersPrograms")
	# Translators: A label for a shortcut in start menu to open NVDA user guide.
	createShortcut(os.path.join(docFolder,_("User Guide")+".lnk"),targetPath=getDocFilePath("userGuide.html",installDir),prependSpecialFolder="AllUsersPrograms")
	registerAddonFileAssociation(slaveExe)

def isDesktopShortcutInstalled():
	wsh=_getWSH()
	specialPath=wsh.SpecialFolders("allUsersDesktop")
	shortcutPath=os.path.join(specialPath,"nvda.lnk")
	return os.path.isfile(shortcutPath)

def unregisterInstallation(keepDesktopShortcut=False):
	import nvda_service
	try:
		nvda_service.stopService()
	except:
		pass
	try:
		nvda_service.removeService()
	except:
		pass
	if easeOfAccess.isSupported:
		try:
			_winreg.DeleteKeyEx(_winreg.HKEY_LOCAL_MACHINE, easeOfAccess.APP_KEY_PATH,
				_winreg.KEY_WOW64_64KEY)
			easeOfAccess.setAutoStart(_winreg.HKEY_LOCAL_MACHINE, False)
		except WindowsError:
			pass
	wsh=_getWSH()
	desktopPath=os.path.join(wsh.SpecialFolders("AllUsersDesktop"),"NVDA.lnk")
	if not keepDesktopShortcut and os.path.isfile(desktopPath):
		try:
			os.remove(desktopPath)
		except WindowsError:
			pass
	startMenuFolder=getStartMenuFolder()
	if startMenuFolder:
		programsPath=wsh.SpecialFolders("AllUsersPrograms")
		startMenuPath=os.path.join(programsPath,startMenuFolder)
		if os.path.isdir(startMenuPath):
			shutil.rmtree(startMenuPath,ignore_errors=True)
	try:
		_winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\nvda")
	except WindowsError:
		pass
	try:
		_winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\nvda.exe")
	except WindowsError:
		pass
	try:
		_winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE,config.NVDA_REGKEY)
	except WindowsError:
		pass
	unregisterAddonFileAssociation()

def registerAddonFileAssociation(slaveExe):
	try:
		# Create progID for NVDA ad-ons
		with _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Classes\\%s" % addonHandler.NVDA_ADDON_PROG_ID, 0, _winreg.KEY_WRITE) as k:
			# Translators: A file extension label for NVDA add-on package.
			_winreg.SetValueEx(k, None, 0, _winreg.REG_SZ, _("NVDA add-on package"))
			with _winreg.CreateKeyEx(k, "DefaultIcon", 0, _winreg.KEY_WRITE) as k2:
				_winreg.SetValueEx(k2, None, 0, _winreg.REG_SZ, "@{slaveExe},1".format(slaveExe=slaveExe))
			# Point the open verb to nvda_slave addons_installAddonPackage action
			with _winreg.CreateKeyEx(k, "shell\\open\\command", 0, _winreg.KEY_WRITE) as k2:
				_winreg.SetValueEx(k2, None, 0, _winreg.REG_SZ, u"\"{slaveExe}\" addons_installAddonPackage \"%1\"".format(slaveExe=slaveExe))
		# Now associate addon extension to the created prog id.
		with _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Classes\\.%s" % addonHandler.BUNDLE_EXTENSION, 0, _winreg.KEY_WRITE) as k:
			_winreg.SetValueEx(k, None, 0, _winreg.REG_SZ, addonHandler.NVDA_ADDON_PROG_ID)
			_winreg.SetValueEx(k, "Content Type", 0, _winreg.REG_SZ, addonHandler.BUNDLE_MIMETYPE)
			# Add NVDA to the "open With" list
			k2 = _winreg.CreateKeyEx(k, "OpenWithProgids\\%s" % addonHandler.NVDA_ADDON_PROG_ID, 0, _winreg.KEY_WRITE)
			_winreg.CloseKey(k2)
		# Notify the shell that a file association has changed:
		shellapi.SHChangeNotify(shellapi.SHCNE_ASSOCCHANGED, shellapi.SHCNF_IDLIST, None, None)
	except WindowsError:
		log.error("Can not create addon file association.", exc_info=True)

def unregisterAddonFileAssociation():
	try:
		# As per MSDN recomendation, we only need to remove the prog ID.
		_deleteKeyAndSubkeys(_winreg.HKEY_LOCAL_MACHINE, "Software\\Classes\\%s" % addonHandler.NVDA_ADDON_PROG_ID)
	except WindowsError:
		# This is probably the first install, so just ignore the error.
		return
	# Notify the shell that a file association has changed:
	shellapi.SHChangeNotify(shellapi.SHCNE_ASSOCCHANGED, shellapi.SHCNF_IDLIST, None, None)

# Windows API call regDeleteTree is only available on vist and above so rule our own.
def _deleteKeyAndSubkeys(key, subkey):
	with _winreg.OpenKey(key, subkey, 0, _winreg.KEY_WRITE|_winreg.KEY_READ) as k:
		# Recursively delete subkeys (Depth first search order)
		# So Pythonic... </rant>
		for i in itertools.count():
			try:
				subkeyName = _winreg.EnumKey(k, i)
			except WindowsError:
				break
			# Recursive call.
			_deleteKeyAndSubkeys(k, subkeyName)
		# Delete this key
		_winreg.DeleteKey(k, "")

class RetriableFailure(Exception):
	pass

def deleteFileOnReboot(path):
	"""
	Marks a file for delete on reboot.
	This uses Windows' MoveFileEx (either unicode or ascii depending on the given path) and also prepends'\\?\' to allow for long file names.
	@return: True if  the action was successfull. False otherwise.
	@rtype: boolean
	"""
	MoveFileEx=windll.kernel32.MoveFileExW if isinstance(path,unicode) else windll.kernel32.MoveFileExA
	return MoveFileEx("\\\\?\\"+path,None,MOVEFILE_DELAY_UNTIL_REBOOT)!=0

def copyFile(sourceFilePath,destFilePath):
	"""
	Copies the file at sourcePath to destPath.
	This uses Windows' CopyFile and prepends'\\?\' to allow for long file names.
	@return: True if  the action was successfull. False otherwise.
	@rtype: boolean
	"""
	return windll.kernel32.CopyFileW(u'\\\\?\\'+sourceFilePath,u'\\\\?\\'+destFilePath,False)!=0

def tryRemoveFile(path,numTries=6,retryInterval=0.5,tempDir=None):
	"""
	Tries to remove a file multiple times using veris strategies.
	It first tries a simple delete. If that fails, it tries to rename the file to a temp file in the given temp directory, and marks it for delete on next reboot.
	If both the delete and or the rename fail, the function waits a small period of time and tries to remove the file again, just in case the file was temporarily locked.
	@param path: the path to the file that should be removed
	@ type path: string
	@param numTries: the number of times the file should try to be removed.
	@type numTries: int
	@param retryInterval: the number of seconds the function waits before trying to remove the file again.
	@type retryInterval: float
	@param tempDir: the path to the temporary directory where files marked for delete on reboot should be stored.
	This directory should be on the same physical drive as the file being removed.
	A value of None (default) uses the same directory as the file being removed.
	@type tempDir: string
	@raises: RetriableFailure if the file could not be removed at all.
	"""
	if not tempDir:
		tempDir=os.path.dirname(path)
	for count in xrange(numTries):
		if count>0:
			log.debugWarning("Will try to remove file again after delay")
			time.sleep(retryInterval)
		try:
			if os.path.isdir(path):
				shutil.rmtree(path)
			else:
				os.remove(path)
			return
		except OSError as e:
			log.debugWarning("Failed to delete file %s, %s, will try renaming"%(path,e))
		# The file could not be removed.
		# Rename it to a temporary file, and try removing on reboot if allowed
		tempPath=tempfile.mktemp(dir=tempDir)
		log.debug("Renaming %s to %s"%(path,tempPath))
		try:
			os.rename(path,tempPath)
		except (WindowsError,IOError) as e:
			log.debugWarning("Failed to rename file %s before  remove on reboot"%path)
			continue
		log.debug("Marking file for delete on reboot: %s"%tempPath)
		if not deleteFileOnReboot(tempPath):
			log.warning("Could not mark file for remove on reboot: %s"%tempPath)
		return
	raise RetriableFailure("File %s could not be removed"%path)

def tryCopyFile(sourceFilePath,destFilePath):
	if copyFile(sourceFilePath,destFilePath)==0:
		errorCode=GetLastError()
		log.debugWarning("Unable to copy %s, error %d"%(sourceFilePath,errorCode))
		if not os.path.exists(destFilePath):
			raise OSError("error %d copying %s to %s"%(errorCode,sourceFilePath,destFilePath))
		tryRemoveFile(destFilePath)
		log.debug("Trying to copy again after remove")
		if copyFile(sourceFilePath,destFilePath)==0:
			errorCode=GetLastError()
			raise OSError("Unable to copy file %s to %s, error %d"%(sourceFilePath,destFilePath,errorCode))

def install(shouldCreateDesktopShortcut=True,shouldRunAtLogon=True):
	prevInstallPath=getInstallPath(noDefault=True)
	try:
		k = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, config.NVDA_REGKEY)
		configInLocalAppData = bool(_winreg.QueryValueEx(k, config.CONFIG_IN_LOCAL_APPDATA_SUBKEY)[0])
	except WindowsError:
		configInLocalAppData = False
	unregisterInstallation(keepDesktopShortcut=shouldCreateDesktopShortcut)
	installDir=defaultInstallPath
	startMenuFolder=defaultStartMenuFolder
	# Remove all the main executables always.
	# We do this for two reasons:
	# 1. If this fails, it means another copy of NVDA is running elsewhere,
	# so we shouldn't proceed.
	# 2. The appropriate executable for nvda.exe will be determined by
	# which executables exist after copying program files.
	for f in ("nvda.exe","nvda_noUIAccess.exe","nvda_UIAccess.exe","nvda_service.exe","nvda_slave.exe"):
		f=os.path.join(installDir,f)
		if os.path.isfile(f):
			tryRemoveFile(f)
	if prevInstallPath:
		removeOldLoggedFiles(prevInstallPath)
	removeOldProgramFiles(installDir)
	copyProgramFiles(installDir)
	for f in ("nvda_UIAccess.exe","nvda_noUIAccess.exe"):
		f=os.path.join(installDir,f)
		if os.path.isfile(f):
			tryCopyFile(f,os.path.join(installDir,"nvda.exe"))
			break
	else:
		raise RuntimeError("No available executable to use as nvda.exe")
	registerInstallation(installDir,startMenuFolder,shouldCreateDesktopShortcut,shouldRunAtLogon,configInLocalAppData)

def removeOldLoggedFiles(installPath):
	datPath=os.path.join(installPath,"uninstall.dat")
	lines=[]
	if os.path.isfile(datPath):
		with open(datPath,"r") as datFile:
			datFile.readline()
			lines=datFile.readlines()
			lines.append(os.path.join(installPath,'uninstall.exe'))
			lines.sort(reverse=True)
			lines.append(os.path.join(installPath,'uninstall.dat'))
	for line in lines:
		filePath=line.rstrip('\n')
		if os.path.exists(filePath):
			tryRemoveFile(filePath,rebootOK=True)

def createPortableCopy(destPath,shouldCopyUserConfig=True):
	destPath=os.path.abspath(destPath)
	#Remove all the main executables always
	for f in ("nvda.exe","nvda_noUIAccess.exe","nvda_UIAccess.exe"):
		f=os.path.join(destPath,f)
		if os.path.isfile(f):
			tryRemoveFile(f)
	removeOldProgramFiles(destPath)
	copyProgramFiles(destPath)
	tryCopyFile(os.path.join(destPath,"nvda_noUIAccess.exe"),os.path.join(destPath,"nvda.exe"))
	if shouldCopyUserConfig:
		copyUserConfig(os.path.join(destPath,'userConfig'))

def registerEaseOfAccess(installDir):
	with _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE, easeOfAccess.APP_KEY_PATH, 0,
			_winreg.KEY_ALL_ACCESS | _winreg.KEY_WOW64_64KEY) as appKey:
		_winreg.SetValueEx(appKey, "ApplicationName", None, _winreg.REG_SZ,
			versionInfo.name)
		_winreg.SetValueEx(appKey, "Description", None, _winreg.REG_SZ,
			versionInfo.longName)
		if easeOfAccess.canConfigTerminateOnDesktopSwitch:
			_winreg.SetValueEx(appKey, "Profile", None, _winreg.REG_SZ,
				'<HCIModel><Accommodation type="severe vision"/></HCIModel>')
			_winreg.SetValueEx(appKey, "SimpleProfile", None, _winreg.REG_SZ,
				"screenreader")
			_winreg.SetValueEx(appKey, "ATExe", None, _winreg.REG_SZ,
				"nvda.exe")
			_winreg.SetValueEx(appKey, "StartExe", None, _winreg.REG_SZ,
				os.path.join(installDir, u"nvda.exe"))
			_winreg.SetValueEx(appKey, "StartParams", None, _winreg.REG_SZ,
				"--ease-of-access")
			_winreg.SetValueEx(appKey, "TerminateOnDesktopSwitch", None,
				_winreg.REG_DWORD, 0)
		else:
			# We don't want NVDA to appear in EoA because
			# starting NVDA from there won't work in this case.
			# We can do this by not setting Profile and SimpleProfile.
			# NVDA can still change the EoA logon settings.
			_winreg.SetValueEx(appKey, "ATExe", None, _winreg.REG_SZ,
				"nvda_eoaProxy.exe")
			_winreg.SetValueEx(appKey, "StartExe", None, _winreg.REG_SZ,
				os.path.join(installDir, u"nvda_eoaProxy.exe"))
