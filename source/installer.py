# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2011-2019 NV Access Limited, Joseph Lee, Babbage B.V., Łukasz Golonka

import ctypes
import winreg
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
import COMRegistrationFixes
import winKernel

_wsh=None
def _getWSH():
	global _wsh
	if not _wsh:
		import comtypes.client
		_wsh=comtypes.client.CreateObject("wScript.Shell",dynamic=True)
	return _wsh

defaultStartMenuFolder=versionInfo.name
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion") as k:
	programFilesPath=winreg.QueryValueEx(k, "ProgramFilesDir")[0] 
defaultInstallPath=os.path.join(programFilesPath, versionInfo.name)

def createShortcut(path,targetPath=None,arguments=None,iconLocation=None,workingDirectory=None,hotkey=None,prependSpecialFolder=None):
	# #7696: The shortcut is only physically saved to disk if it does not already exist, or one or more properties have changed. 
	wsh=_getWSH()
	if prependSpecialFolder:
		specialPath=wsh.SpecialFolders(prependSpecialFolder)
		path=os.path.join(specialPath,path)
	if not os.path.isdir(os.path.dirname(path)):
		os.makedirs(os.path.dirname(path))
	shortcutExists=os.path.isfile(path)
	short=wsh.CreateShortcut(path)
	needsSave=not shortcutExists
	if short.targetPath!=targetPath:
		short.TargetPath=targetPath
		needsSave=True
	if arguments and short.arguments!=arguments:
		short.arguments=arguments
		needsSave=True
	if not shortcutExists and hotkey:
		short.Hotkey=hotkey
		needsSave=True
	if iconLocation and short.iconLocation!=iconLocation:
		short.IconLocation=iconLocation
		needsSave=True
	if workingDirectory and short.workingDirectory!=workingDirectory:
		short.workingDirectory=workingDirectory
		needsSave=True
	if needsSave:
		short.Save()

def getStartMenuFolder(noDefault=False):
	try:
		with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, config.RegistryKey.NVDA.value) as k:
			return winreg.QueryValueEx(k,u"Start Menu Folder")[0]
	except WindowsError:
		return defaultStartMenuFolder if not noDefault else None

def getInstallPath(noDefault=False):
	try:
		k=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NVDA")
		return winreg.QueryValueEx(k,"UninstallDirectory")[0]
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
		oldTime=os.path.getmtime(os.path.join(path, "nvda_slave.exe"))
		newTime=os.path.getmtime("nvda_slave.exe")
	except OSError:
		return None
	# cmp no longer exists in Python3.
	# Per the Python3 What's New docs:
	# cmp can be replaced with (a>b)-(a<b).
	# In other words, False and True coerce to 0 and 1 respectively.
	return (oldTime>newTime)-(oldTime<newTime)

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
	sourcePath = globalVars.appDir
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
	sourcePath = globalVars.appArgs.configPath
	for curSourceDir,subDirs,files in os.walk(sourcePath):
		curDestDir=os.path.join(destPath,os.path.relpath(curSourceDir,sourcePath))
		if not os.path.isdir(curDestDir):
			os.makedirs(curDestDir)
		for f in files:
			sourceFilePath=os.path.join(curSourceDir,f)
			destFilePath=os.path.join(destPath,os.path.relpath(sourceFilePath,sourcePath))
			tryCopyFile(sourceFilePath,destFilePath)


def removeOldLibFiles(destPath, rebootOK=False):
	"""
	Removes library files from previous versions of NVDA.
	@param destPath: The path where NVDA is installed.
	@type destPath: string
	@param rebootOK: If true then files can be removed on next reboot if trying to do so now fails.
	@type rebootOK: boolean
	"""
	for topDir in ('lib', 'lib64', 'libArm64'):
		currentLibPath = os.path.join(destPath, topDir, versionInfo.version)
		for parent, subdirs, files in os.walk(os.path.join(destPath, topDir), topdown=False):
			if parent==currentLibPath:
				# Lib dir for current installation. Don't touch this!
				log.debug("Skipping current install lib path: %r"%parent)
				continue
			for d in subdirs:
				path = os.path.join(parent, d)
				if path != currentLibPath:
					log.debug(f"Removing old lib directory: {repr(path)}")
					try:
						os.rmdir(path)
					except OSError:
						log.warning(
							"Failed to remove a directory no longer needed. "
							"This can be manually removed after a reboot or the  installer will try"
							f" removing it again next time. Directory: {repr(path)}"
						)
			for f in files:
				path = os.path.join(parent, f)
				log.debug("Removing old lib file: %r"%path)
				try:
					tryRemoveFile(path, numRetries=2, rebootOK=rebootOK)
				except RetriableFailure:
					log.warning("A file no longer needed could not be removed. This can be manually removed after a reboot, or  the installer will try again next time. File: %r"%path)

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

	# #9960: If compiled python files from older versions aren't removed correctly,
	# this could cause strange errors when Python tries to create tracebacks
	# in a newer version of NVDA.
	#  However don't touch user and system config.
	#  Also remove old .dll and .manifest files.
	for curDestDir,subDirs,files in os.walk(destPath):
		if curDestDir == destPath:
			subDirs[:] = [x for x in subDirs if os.path.basename(x).lower() not in (
				'userconfig',
				'systemconfig',
				#  Do not remove old libraries here. It is done by removeOldLibFiles.
				'lib',
				'lib64',
				'libarm64')]
		for f in files:
			if f.endswith((".pyc", ".pyo", ".pyd", ".dll", ".manifest")):
				path=os.path.join(curDestDir, f)
				log.debug(f"Removing old byte compiled python file: {path!r}")
				try:
					tryRemoveFile(path)
				except RetriableFailure:
					log.warning(f"Couldn't remove file: {path!r}")

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
	with winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\NVDA",0,winreg.KEY_WRITE) as k:
		for name,value in uninstallerRegInfo.items(): 
			winreg.SetValueEx(k,name,None,winreg.REG_SZ,value.format(installDir=installDir))
	with winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\nvda.exe",0,winreg.KEY_WRITE) as k:
		winreg.SetValueEx(k,"",None,winreg.REG_SZ,os.path.join(installDir,"nvda.exe"))
	with winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, config.RegistryKey.NVDA.value, 0, winreg.KEY_WRITE) as k:
		winreg.SetValueEx(k,"startMenuFolder",None,winreg.REG_SZ,startMenuFolder)
		if configInLocalAppData:
			winreg.SetValueEx(k,config.CONFIG_IN_LOCAL_APPDATA_SUBKEY,None,winreg.REG_DWORD,int(configInLocalAppData))
	registerEaseOfAccess(installDir)
	if startOnLogonScreen is not None:
		config._setStartOnLogonScreen(startOnLogonScreen)
	NVDAExe=os.path.join(installDir,u"nvda.exe")
	slaveExe=os.path.join(installDir,u"nvda_slave.exe")
	try:
		_updateShortcuts(NVDAExe, installDir, shouldCreateDesktopShortcut, slaveExe, startMenuFolder)
	except Exception:
		log.error("Error while creating shortcuts", exc_info=True)
	registerAddonFileAssociation(slaveExe)


def _createShortcutWithFallback(
		path,
		targetPath=None,
		arguments=None,
		iconLocation=None,
		workingDirectory=None,
		hotkey=None,
		prependSpecialFolder=None,
		fallbackHotkey=None,
		fallbackPath=None,
):
	"""Sometimes translations are used (for `path` or `hotkey` arguments) which include unicode characters
	which cause the createShortcut method to fail. In these cases, try again using the English string if it is
	provided via the `fallbackHotkey` / `fallbackPath` arguments.
	"""
	try:
		createShortcut(
			path,
			targetPath,
			arguments,
			iconLocation,
			workingDirectory,
			hotkey,
			prependSpecialFolder
		)
	except Exception:
		if hotkey is not None and fallbackHotkey is not None:
			log.error(f"Error creating {path}. With hotkey ({hotkey}). Trying fallback hotkey: {fallbackHotkey}")
			_createShortcutWithFallback(
				hotkey=fallbackHotkey,
				fallbackHotkey=None,
				path=path,
				fallbackPath=fallbackPath,
				targetPath=targetPath,
				arguments=arguments,
				prependSpecialFolder=prependSpecialFolder,
			)
		elif fallbackPath is not None:
			log.error(f"Error creating {path}. Trying without translation of filename, instead using: {fallbackPath}")
			_createShortcutWithFallback(
				path=fallbackPath,
				fallbackPath=None,
				targetPath=targetPath,
				arguments=arguments,
				hotkey=hotkey,
				prependSpecialFolder=prependSpecialFolder,
				fallbackHotkey=fallbackHotkey,
			)
		else:
			log.error(
				f"Error creating {path}, no mitigation possible. "
				f"Perhaps controlled folder access is active for this directory."
			)


def _updateShortcuts(NVDAExe, installDir, shouldCreateDesktopShortcut, slaveExe, startMenuFolder) -> None:
	if shouldCreateDesktopShortcut:
		# Translators: The shortcut key used to start NVDA.
		# This should normally be left as is, but might be changed for some locales
		# if the default key causes problems for the normal locale keyboard layout.
		# The key must be formatted as described in this article:
		# http://msdn.microsoft.com/en-us/library/3zb1shc6%28v=vs.84%29.aspx
		hotkeyTranslated = _("CTRL+ALT+N")

		# #8320: -r|--replace is now the default. Nevertheless, keep creating
		# the shortcut with the now superfluous argument in case a downgrade of
		# NVDA is later performed.
		_createShortcutWithFallback(
			path="NVDA.lnk",
			targetPath=slaveExe,
			arguments="launchNVDA -r",
			hotkey=hotkeyTranslated,
			fallbackHotkey="CTRL+ALT+N",
			workingDirectory=installDir,
			prependSpecialFolder="AllUsersDesktop",
		)

	_createShortcutWithFallback(
		path=os.path.join(startMenuFolder, "NVDA.lnk"),
		targetPath=NVDAExe,
		workingDirectory=installDir,
		prependSpecialFolder="AllUsersPrograms"
	)

	# Translators: A label for a shortcut in start menu and a menu entry in NVDA menu (to go to NVDA website).
	webSiteTranslated = _("NVDA web site")
	_createShortcutWithFallback(
		path=os.path.join(startMenuFolder, webSiteTranslated + ".lnk"),
		fallbackPath=os.path.join(startMenuFolder, "NVDA web site.lnk"),
		targetPath=versionInfo.url,
		prependSpecialFolder="AllUsersPrograms"
	)

	# Translators: A label for a shortcut item in start menu to uninstall NVDA from the computer.
	uninstallTranslated = _("Uninstall NVDA")
	_createShortcutWithFallback(
		path=os.path.join(startMenuFolder, uninstallTranslated + ".lnk"),
		fallbackPath=os.path.join(startMenuFolder, "Uninstall NVDA.lnk"),
		targetPath=os.path.join(installDir, "uninstall.exe"),
		workingDirectory=installDir,
		prependSpecialFolder="AllUsersPrograms"
	)

	# Translators: A label for a shortcut item in start menu to open current user's NVDA configuration directory.
	exploreConfDirTranslated = _("Explore NVDA user configuration directory")
	_createShortcutWithFallback(
		path=os.path.join(startMenuFolder, exploreConfDirTranslated + ".lnk"),
		fallbackPath=os.path.join(startMenuFolder, "Explore NVDA user configuration directory.lnk"),
		targetPath=slaveExe,
		arguments="explore_userConfigPath",
		workingDirectory=installDir,
		prependSpecialFolder="AllUsersPrograms"
	)

	# Translators: The label of the NVDA Documentation menu in the Start Menu.
	docFolder = os.path.join(startMenuFolder, _("Documentation"))

	# Translators: The label of the Start Menu item to open the Commands Quick Reference document.
	commandsRefTranslated = _("Commands Quick Reference")
	_createShortcutWithFallback(
		path=os.path.join(docFolder, commandsRefTranslated + ".lnk"),
		fallbackPath=os.path.join(docFolder, "Commands Quick Reference.lnk"),
		targetPath=getDocFilePath("keyCommands.html", installDir),
		prependSpecialFolder="AllUsersPrograms"
	)

	# Translators: A label for a shortcut in start menu to open NVDA user guide.
	userGuideTranslated = _("User Guide")
	_createShortcutWithFallback(
		path=os.path.join(docFolder, userGuideTranslated + ".lnk"),
		fallbackPath=os.path.join(docFolder, "User Guide.lnk"),
		targetPath=getDocFilePath("userGuide.html", installDir),
		prependSpecialFolder="AllUsersPrograms"
	)

	# Translators: A label for a shortcut in start menu to open NVDA what's new.
	changesTranslated = _("What's new")
	_createShortcutWithFallback(
		path=os.path.join(docFolder, changesTranslated + ".lnk"),
		fallbackPath=os.path.join(docFolder, "What's new.lnk"),
		targetPath=getDocFilePath("changes.html", installDir),
		prependSpecialFolder="AllUsersPrograms"
	)


def isDesktopShortcutInstalled():
	wsh=_getWSH()
	specialPath=wsh.SpecialFolders("allUsersDesktop")
	shortcutPath=os.path.join(specialPath,"nvda.lnk")
	return os.path.isfile(shortcutPath)

def unregisterInstallation(keepDesktopShortcut=False):
	try:
		winreg.DeleteKeyEx(
			winreg.HKEY_LOCAL_MACHINE,
			easeOfAccess.RegistryKey.APP.value,
			winreg.KEY_WOW64_64KEY
		)
		easeOfAccess.setAutoStart(easeOfAccess.AutoStartContext.ON_LOGON_SCREEN, False)
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
		winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\nvda")
	except WindowsError:
		pass
	try:
		winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\nvda.exe")
	except WindowsError:
		pass
	try:
		winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, config.RegistryKey.NVDA.value)
	except WindowsError:
		pass
	unregisterAddonFileAssociation()

def registerAddonFileAssociation(slaveExe):
	try:
		# Create progID for NVDA ad-ons
		with winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Classes\\%s" % addonHandler.NVDA_ADDON_PROG_ID, 0, winreg.KEY_WRITE) as k:
			# Translators: A file extension label for NVDA add-on package.
			winreg.SetValueEx(k, None, 0, winreg.REG_SZ, _("NVDA add-on package"))
			with winreg.CreateKeyEx(k, "DefaultIcon", 0, winreg.KEY_WRITE) as k2:
				winreg.SetValueEx(k2, None, 0, winreg.REG_SZ, "@{slaveExe},1".format(slaveExe=slaveExe))
			# Point the open verb to nvda_slave addons_installAddonPackage action
			with winreg.CreateKeyEx(k, "shell\\open\\command", 0, winreg.KEY_WRITE) as k2:
				winreg.SetValueEx(k2, None, 0, winreg.REG_SZ, u"\"{slaveExe}\" addons_installAddonPackage \"%1\"".format(slaveExe=slaveExe))
		# Now associate addon extension to the created prog id.
		with winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Classes\\.%s" % addonHandler.BUNDLE_EXTENSION, 0, winreg.KEY_WRITE) as k:
			winreg.SetValueEx(k, None, 0, winreg.REG_SZ, addonHandler.NVDA_ADDON_PROG_ID)
			winreg.SetValueEx(k, "Content Type", 0, winreg.REG_SZ, addonHandler.BUNDLE_MIMETYPE)
			# Add NVDA to the "open With" list
			k2 = winreg.CreateKeyEx(k, "OpenWithProgids\\%s" % addonHandler.NVDA_ADDON_PROG_ID, 0, winreg.KEY_WRITE)
			winreg.CloseKey(k2)
		# Notify the shell that a file association has changed:
		shellapi.SHChangeNotify(shellapi.SHCNE_ASSOCCHANGED, shellapi.SHCNF_IDLIST, None, None)
	except WindowsError:
		log.error("Can not create addon file association.", exc_info=True)

def unregisterAddonFileAssociation():
	try:
		# As per MSDN recomendation, we only need to remove the prog ID.
		_deleteKeyAndSubkeys(winreg.HKEY_LOCAL_MACHINE, "Software\\Classes\\%s" % addonHandler.NVDA_ADDON_PROG_ID)
	except WindowsError:
		# This is probably the first install, so just ignore the error.
		return
	# Notify the shell that a file association has changed:
	shellapi.SHChangeNotify(shellapi.SHCNE_ASSOCCHANGED, shellapi.SHCNF_IDLIST, None, None)

# Windows API call regDeleteTree is only available on vist and above so rule our own.
def _deleteKeyAndSubkeys(key, subkey):
	with winreg.OpenKey(key, subkey, 0, winreg.KEY_WRITE|winreg.KEY_READ) as k:
		# Recursively delete subkeys (Depth first search order)
		# So Pythonic... </rant>
		for i in itertools.count():
			try:
				subkeyName = winreg.EnumKey(k, i)
			except WindowsError:
				break
			# Recursive call.
			_deleteKeyAndSubkeys(k, subkeyName)
		# Delete this key
		winreg.DeleteKey(k, "")

class RetriableFailure(Exception):
	pass

def tryRemoveFile(path,numRetries=6,retryInterval=0.5,rebootOK=False):
	dirPath=os.path.dirname(path)
	tempPath=tempfile.mktemp(dir=dirPath)
	try:
		os.rename(path,tempPath)
	except (WindowsError,IOError):
		raise RetriableFailure("Failed to rename file %s before  remove"%path)
	for count in range(numRetries):
		try:
			if os.path.isdir(tempPath):
				shutil.rmtree(tempPath)
			else:
				os.remove(tempPath)
			return
		except OSError:
			pass
		time.sleep(retryInterval)
	if rebootOK:
		log.debugWarning("Failed to delete file %s, marking for delete on reboot"%tempPath)
		try:
			# Use escapes in a unicode string instead of raw.
			# In a raw string the trailing slash escapes the closing quote leading to a python syntax error.
			pathQualifier=u"\\\\?\\"
			# #9847: Move file to None to delete it.
			winKernel.moveFileEx(pathQualifier+tempPath,None,winKernel.MOVEFILE_DELAY_UNTIL_REBOOT)
		except WindowsError:
			log.debugWarning("Failed to delete file %s, marking for delete on reboot"%tempPath, exc_info=True)
		return
	try:
		os.rename(tempPath,path)
	except:
		log.error("Unable to rename back to %s before retriable failier"%path)
	raise RetriableFailure("File %s could not be removed"%path)

def tryCopyFile(sourceFilePath,destFilePath):
	if not sourceFilePath.startswith('\\\\'):
		sourceFilePath=u"\\\\?\\"+sourceFilePath
	if not destFilePath.startswith('\\\\'):
		destFilePath=u"\\\\?\\"+destFilePath
	if ctypes.windll.kernel32.CopyFileW(sourceFilePath, destFilePath, False) == 0:
		errorCode = ctypes.GetLastError()
		log.debugWarning("Unable to copy %s, error %d"%(sourceFilePath,errorCode))
		if not os.path.exists(destFilePath):
			raise OSError("error %d copying %s to %s"%(errorCode,sourceFilePath,destFilePath))
		tempPath=tempfile.mktemp(dir=os.path.dirname(destFilePath))
		try:
			os.rename(destFilePath,tempPath)
		except (WindowsError,OSError):
			log.error("Failed to rename %s after failed overwrite"%destFilePath,exc_info=True)
			raise RetriableFailure("Failed to rename %s after failed overwrite"%destFilePath) 
		winKernel.moveFileEx(tempPath,None,winKernel.MOVEFILE_DELAY_UNTIL_REBOOT)
		if ctypes.windll.kernel32.CopyFileW(sourceFilePath, destFilePath, False) == 0:
			errorCode = ctypes.GetLastError()
			raise OSError("Unable to copy file %s to %s, error %d"%(sourceFilePath,destFilePath,errorCode))

def install(shouldCreateDesktopShortcut=True,shouldRunAtLogon=True):
	prevInstallPath=getInstallPath(noDefault=True)
	try:
		k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, config.RegistryKey.NVDA.value)
		configInLocalAppData = bool(winreg.QueryValueEx(k, config.CONFIG_IN_LOCAL_APPDATA_SUBKEY)[0])
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
	removeOldLibFiles(installDir,rebootOK=True)
	COMRegistrationFixes.fixCOMRegistrations()

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
	assert os.path.isabs(destPath), f"Destination path {destPath} is not absolute"
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
	removeOldLibFiles(destPath,rebootOK=True)

def registerEaseOfAccess(installDir):
	with winreg.CreateKeyEx(
		winreg.HKEY_LOCAL_MACHINE,
		easeOfAccess.RegistryKey.APP.value,
		0,
		winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_64KEY
	) as appKey:
		winreg.SetValueEx(appKey, "ApplicationName", None, winreg.REG_SZ,
			versionInfo.name)
		winreg.SetValueEx(appKey, "Description", None, winreg.REG_SZ,
			versionInfo.longName)
		if easeOfAccess.canConfigTerminateOnDesktopSwitch:
			winreg.SetValueEx(appKey, "Profile", None, winreg.REG_SZ,
				'<HCIModel><Accommodation type="severe vision"/></HCIModel>')
			winreg.SetValueEx(appKey, "SimpleProfile", None, winreg.REG_SZ,
				"screenreader")
			winreg.SetValueEx(appKey, "ATExe", None, winreg.REG_SZ,
				"nvda.exe")
			winreg.SetValueEx(appKey, "StartExe", None, winreg.REG_SZ,
				os.path.join(installDir, u"nvda.exe"))
			winreg.SetValueEx(appKey, "StartParams", None, winreg.REG_SZ,
				"--ease-of-access")
			winreg.SetValueEx(appKey, "TerminateOnDesktopSwitch", None,
				winreg.REG_DWORD, 0)
		else:
			# We don't want NVDA to appear in EoA because
			# starting NVDA from there won't work in this case.
			# We can do this by not setting Profile and SimpleProfile.
			# NVDA can still change the EoA logon settings.
			winreg.SetValueEx(appKey, "ATExe", None, winreg.REG_SZ,
				"nvda_eoaProxy.exe")
			winreg.SetValueEx(appKey, "StartExe", None, winreg.REG_SZ,
				os.path.join(installDir, u"nvda_eoaProxy.exe"))
