from ctypes import *
from ctypes import *
from ctypes.wintypes import *
import _winreg
import threading
import time
import os
import tempfile
import shutil
import shellapi
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
defaultInstallPath=os.path.join(unicode(os.getenv("ProgramFiles")), versionInfo.name)

def createShortcut(path,targetPath=None,arguments=None,iconLocation=None,workingDirectory=None,hotkey=None,prependSpecialFolder=None):
	wsh=_getWSH()
	if prependSpecialFolder:
		specialPath=wsh.SpecialFolders(prependSpecialFolder)
		path=os.path.join(specialPath,path)
	log.info("Creating shortcut at %s"%path)
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
			if os.path.split(curSourceDir)[1].lower()=="userconfig":
				del subDirs[:]
				continue
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
				os.rename(destFilePath,tempPath)
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
				os.rename(destFilePath,tempPath)
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
		_winreg.SetValueEx(k,"@",None,_winreg.REG_SZ,installDir)
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
		createShortcut(u"nvda.lnk",targetPath=slaveExe,arguments="launchNVDA -r",iconLocation=NVDAExe+",0",hotkey="CTRL+ALT+N",workingDirectory=installDir,prependSpecialFolder="AllUsersDesktop")
	createShortcut(os.path.join(startMenuFolder,"NVDA.lnk"),targetPath=NVDAExe,iconLocation=NVDAExe+",0",workingDirectory=installDir,prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("NVDA Website")+".lnk"),targetPath=versionInfo.url,prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("Uninstall NVDA")+".lnk"),targetPath=os.path.join(installDir,"uninstall.exe"),workingDirectory=installDir,prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("Explore NVDA user configuration directory")+".lnk"),targetPath=slaveExe,arguments="exploreUserconfigPath",workingDirectory=installDir,prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("Documentation"),_("Key Command quick reference")+".lnk"),targetPath=getDocFilePath("keycommands.html",installDir),prependSpecialFolder="AllUsersPrograms")
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
	desktopPath=wsh.SpecialFolders("AllUsersDesktop")
	if os.path.isfile(desktopPath):
		try:
			os.remove(os.path.join(desktopPath,"nvda.lnk"))
		except WindowsError:
			pass
	startMenuFolder=getStartMenuFolder()
	if startMenuFolder:
		programsPath=wsh.SpecialFolders("AllUsersPrograms")
		startMenuPath=os.path.join(programsPath,startMenuFolder)
		if os.path.isdir(startMenuPath):
			shutil.rmtree(startMenuPath)
	try:
		_winreg.DeleteKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\nvda",0,0)
		_winreg.DeleteKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\nvda.exe",0,0)
		_winreg.DeleteKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\nvda",0,0)
	except WindowsError:
		pass

def install(shouldCreateDesktopShortcut=True,shouldRunAtLogon=True):
	prevInstallPath=getInstallPath(noDefault=True)
	unregisterInstallation()
	if prevInstallPath:
		removeOldLoggedFiles(prevInstallPath)
	installDir=defaultInstallPath
	startMenuFolder=defaultStartMenuFolder
	#Remove all the main executables always
	for f in ("nvda.exe","nvda_noUIAccess.exe","nvda_UIAccess.exe"):
		f=os.path.join(installDir,f)
		if os.path.isfile(f):
			os.remove(f)
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
			lines.append(os.path.join(installPath,'uninstall.dat'))
			lines.append(os.path.join(installPath,'uninstall.exe'))
			lines.sort(reverse=True)
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
			os.rename(filePath,tempPath)
			if windll.kernel32.MoveFileExA("\\\\?\\"+tempPath,None,4)==0:
				raise OSError("Unable to mark file %s for delete on reboot"%tempPath)

autorunTemplate="""[AutoRun]
open={exe}
action={name} {version}
icon={icon}
"""

class CreatePortableCopy(threading.Thread):

	def __init__(self,destPath,copyUserConfig=True,createAutorun=False):
		super(CreatePortableCopy,self).__init__()
		self.destPath=destPath
		self.copyUserConfig=copyUserConfig
		self.createAutorun=createAutorun
		self.threadExc=None
		self.start()
		time.sleep(0.1)
		threadHandle=c_int()
		threadHandle.value=windll.kernel32.OpenThread(0x100000,False,self.ident)
		msg=MSG()
		while windll.user32.MsgWaitForMultipleObjects(1,byref(threadHandle),False,-1,255)==1:
			while windll.user32.PeekMessageW(byref(msg),None,0,0,1):
				windll.user32.TranslateMessage(byref(msg))
				windll.user32.DispatchMessageW(byref(msg))
		if self.threadExc:
			raise self.threadExc

	def run(self,*args,**kwargs):
		try:
			destPath=os.path.abspath(self.destPath)
			#Remove all the main executables always
			for f in ("nvda.exe","nvda_noUIAccess.exe","nvda_UIAccess.exe"):
				f=os.path.join(destPath,f)
				if os.path.isfile(f):
					os.remove(f)
			copyProgramFiles(destPath)
			if windll.kernel32.CopyFileW(u"\\\\?\\"+os.path.join(destPath,"nvda_noUIAccess.exe"),u"\\\\?\\"+os.path.join(destPath,"nvda.exe"),False)==0:
				raise OSError("Error copying %s to nvda.exe"%f)
			if self.copyUserConfig:
				copyUserConfig(os.path.join(destPath,'userConfig'))
			if self.createAutorun:
				drive,relDestPath=os.path.splitdrive(destPath)
				autorunPath=os.path.join(drive,"autorun.inf")
				autorunString=autorunTemplate.format(exe=os.path.join(relDestPath,'nvda.exe'),name=versionInfo.name,version=versionInfo.version,icon=os.path.join(relDestPath,'images/nvda.ico'))
				with open(autorunPath,"wt") as autorunFile:
					autorunFile.write(autorunString)
		except Exception as e:
			self.threadExc=e
