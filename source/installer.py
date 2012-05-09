#installer.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011-2012 NV Access Limited

from ctypes import *
from ctypes.wintypes import *
import _winreg
import threading
import time
import os
import tempfile
import shutil
import shellapi
import globalVars
import languageHandler
import config
import versionInfo
from logHandler import log

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
	short=wsh.CreateShortcut(path)
	short.TargetPath=targetPath
	if arguments:
		short.arguments=arguments
	if hotkey:
		short.Hotkey=hotkey
	if iconLocation:
		short.IconLocation=iconLocation
	if workingDirectory:
		short.workingDirectory=workingDirectory
	short.Save()

def getStartMenuFolder(noDefault=False):
	try:
		with _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,u"SOFTWARE\\NVDA") as k:
			return _winreg.QueryValueEx(k,u"Start Menu Folder")[0]
	except WindowsError:
		return defaultStartMenuFolder if not noDefault else None

def getInstallPath(noDefault=False):
	try:
		k=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NVDA")
		return _winreg.QueryValueEx(k,"UninstallDirectory")[0]
	except WindowsError:
		return defaultInstallPath if not noDefault else None

def isPreviousInstall():
	return bool(getInstallPath(True))

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
			if windll.kernel32.CopyFileW(u"\\\\?\\"+sourceFilePath,u"\\\\?\\"+destFilePath,False)==0:
				log.debugWarning("Unable to copy %s, trying rename and delete on reboot"%sourceFilePath)
				tempPath=tempfile.mktemp(dir=os.path.dirname(destFilePath))
				try:
					os.rename(destFilePath,tempPath)
				except (WindowsError,OSError):
					raise RetriableFailier("Failed to rename %s after failed remove"%destFilePath) 
				if windll.kernel32.MoveFileExW(u"\\\\?\\"+tempPath,None,4)==0:
					raise OSError("Unable to mark file %s for delete on reboot"%tempPath)
				if windll.kernel32.CopyFileW(u"\\\\?\\"+sourceFilePath,u"\\\\?\\"+destFilePath,False)==0:
					raise OSError("Still unable to copy file %s"%sourceFilePath)

def copyUserConfig(destPath):
	sourcePath=os.path.abspath(globalVars.appArgs.configPath)
	for curSourceDir,subDirs,files in os.walk(sourcePath):
		curDestDir=os.path.join(destPath,os.path.relpath(curSourceDir,sourcePath))
		if not os.path.isdir(curDestDir):
			os.makedirs(curDestDir)
		for f in files:
			sourceFilePath=os.path.join(curSourceDir,f)
			destFilePath=os.path.join(destPath,os.path.relpath(sourceFilePath,sourcePath))
			if windll.kernel32.CopyFileW(u"\\\\?\\"+sourceFilePath,u"\\\\?\\"+destFilePath,False)==0:
				log.debugWarning("Unable to copy %s, trying rename and delete on reboot"%sourceFilePath)
				tempPath=tempfile.mktemp(dir=os.path.dirname(destFilePath))
				try:
					os.rename(destFilePath,tempPath)
				except (WindowsError,OSError):
					raise RetriableFailier("Failed to rename %s after failed remove"%destFilePath)
				if windll.kernel32.MoveFileExW(u"\\\\?\\"+tempPath,None,4)==0:
					raise OSError("Unable to mark file %s for delete on reboot"%tempPath)
				if windll.kernel32.CopyFileW(u"\\\\?\\"+sourceFilePath,u"\\\\?\\"+destFilePath,False)==0:
					raise OSError("Still unable to copy file %s"%sourceFilePath)

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

def registerInstallation(installDir,startMenuFolder,shouldCreateDesktopShortcut,startOnLogonScreen):
	import _winreg
	with _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\NVDA",0,_winreg.KEY_WRITE) as k:
		for name,value in uninstallerRegInfo.iteritems(): 
			_winreg.SetValueEx(k,name,None,_winreg.REG_SZ,value.format(installDir=installDir))
	with _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\nvda.exe",0,_winreg.KEY_WRITE) as k:
		_winreg.SetValueEx(k,"",None,_winreg.REG_SZ,os.path.join(installDir,"nvda.exe"))
	with _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\nvda",0,_winreg.KEY_WRITE) as k:
		_winreg.SetValueEx(k,"startMenuFolder",None,_winreg.REG_SZ,startMenuFolder)
		if startOnLogonScreen is not None:
			_winreg.SetValueEx(k,"startOnLogonScreen",None,_winreg.REG_DWORD,int(startOnLogonScreen))
	import nvda_service
	nvda_service.installService(installDir)
	nvda_service.startService()
	NVDAExe=os.path.join(installDir,u"nvda.exe")
	slaveExe=os.path.join(installDir,u"nvda_slave.exe")
	if shouldCreateDesktopShortcut:
		createShortcut(u"NVDA.lnk",targetPath=slaveExe,arguments="launchNVDA -r",hotkey="CTRL+ALT+N",workingDirectory=installDir,prependSpecialFolder="AllUsersDesktop")
	createShortcut(os.path.join(startMenuFolder,"NVDA.lnk"),targetPath=NVDAExe,workingDirectory=installDir,prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("NVDA Website")+".lnk"),targetPath=versionInfo.url,prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("Uninstall NVDA")+".lnk"),targetPath=os.path.join(installDir,"uninstall.exe"),workingDirectory=installDir,prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("Explore NVDA user configuration directory")+".lnk"),targetPath=slaveExe,arguments="explore_userConfigPath",workingDirectory=installDir,prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("Documentation"),_("Keyboard command quick reference")+".lnk"),targetPath=getDocFilePath("keycommands.html",installDir),prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("Documentation"),_("User Guide")+".lnk"),targetPath=getDocFilePath("userGuide.html",installDir),prependSpecialFolder="AllUsersPrograms")

def isDesktopShortcutInstalled():
	wsh=_getWSH()
	specialPath=wsh.SpecialFolders("allUsersDesktop")
	shortcutPath=os.path.join(specialPath,"nvda.lnk")
	return os.path.isfile(shortcutPath)

def unregisterInstallation(forUpdate=False):
	import nvda_service
	try:
		nvda_service.stopService()
	except:
		pass
	try:
		nvda_service.removeService()
	except:
		pass
	wsh=_getWSH()
	desktopPath=os.path.join(wsh.SpecialFolders("AllUsersDesktop"),"NVDA.lnk")
	if os.path.isfile(desktopPath):
		try:
			os.remove(desktopPath)
		except WindowsError:
			pass
	startMenuFolder=getStartMenuFolder()
	if startMenuFolder:
		programsPath=wsh.SpecialFolders("AllUsersPrograms")
		startMenuPath=os.path.join(programsPath,startMenuFolder)
		if os.path.isdir(startMenuPath):
			shutil.rmtree(startMenuPath)
	try:
		_winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\nvda")
		_winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\nvda.exe")
		_winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\nvda")
	except WindowsError:
		pass

class RetriableFailier(Exception):
	pass

MB_RETRYCANCEL=0x5
MB_SYSTEMMODAL=0x1000
IDRETRY=4
IDCANCEL=3
def tryRemoveFile(path,numRetries=6,retryInterval=0.5):
	for count in xrange(numRetries):
		try:
			os.remove(path)
			return
		except OSError:
			pass
		time.sleep(retryInterval)
	raise RetriableFailier("File %s could not be removed"%path)

def install(shouldCreateDesktopShortcut=True,shouldRunAtLogon=True):
	prevInstallPath=getInstallPath(noDefault=True)
	unregisterInstallation()
	installDir=defaultInstallPath
	startMenuFolder=defaultStartMenuFolder
	#Remove all the main executables always
	for f in ("nvda.exe","nvda_noUIAccess.exe","nvda_UIAccess.exe"):
		f=os.path.join(installDir,f)
		if os.path.isfile(f):
			tryRemoveFile(f)
	if prevInstallPath:
		removeOldLoggedFiles(prevInstallPath)
	copyProgramFiles(installDir)
	for f in ("nvda_UIAccess.exe","nvda_noUIAccess.exe"):
		f=os.path.join(installDir,f)
		if os.path.isfile(f):
			if windll.kernel32.CopyFileW(u"\\\\?\\"+f,u"\\\\?\\"+os.path.join(installDir,"nvda.exe"),False)==0:
				raise OSError("Error copying %s to nvda.exe"%f)
			break
	else:
		raise RuntimeError("No available executable to use as nvda.exe")
	registerInstallation(installDir,startMenuFolder,shouldCreateDesktopShortcut,shouldRunAtLogon)

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
		try:
			if os.path.isfile(filePath):
				os.remove(filePath)
			elif os.path.isdir(filePath):
				os.rmdir(filePath)
		except WindowsError:
			log.debugWarning("Failed to remove %s, removing on reboot"%filePath)
			tempPath=tempfile.mktemp(dir=installPath)
			try:
				os.rename(filePath,tempPath)
			except (WindowsError,IOError):
				raise RetriableFailier("Failed to rename file %s after failed remove"%filePath)
			if windll.kernel32.MoveFileExA("\\\\?\\"+tempPath,None,4)==0:
				raise OSError("Unable to mark file %s for delete on reboot"%tempPath)

autorunTemplate="""[AutoRun]
open={exe}
action={name} {version}
icon={icon}
"""

def createPortableCopy(destPath,shouldCopyUserConfig=True,shouldCreateAutorun=False):
	destPath=os.path.abspath(destPath)
	#Remove all the main executables always
	for f in ("nvda.exe","nvda_noUIAccess.exe","nvda_UIAccess.exe"):
		f=os.path.join(destPath,f)
		if os.path.isfile(f):
			tryRemoveFile(f)
	copyProgramFiles(destPath)
	if windll.kernel32.CopyFileW(u"\\\\?\\"+os.path.join(destPath,"nvda_noUIAccess.exe"),u"\\\\?\\"+os.path.join(destPath,"nvda.exe"),False)==0:
		raise OSError("Error copying %s to nvda.exe"%f)
	if shouldCopyUserConfig:
		copyUserConfig(os.path.join(destPath,'userConfig'))
	if shouldCreateAutorun:
		drive,relDestPath=os.path.splitdrive(destPath)
		autorunPath=os.path.join(drive,"autorun.inf")
		autorunString=autorunTemplate.format(exe=os.path.join(relDestPath,'nvda.exe'),name=versionInfo.name,version=versionInfo.version,icon=os.path.join(relDestPath,'images/nvda.ico'))
		with open(autorunPath,"wt") as autorunFile:
			autorunFile.write(autorunString)
