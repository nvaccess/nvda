from ctypes import *
from ctypes.wintypes import *
import threading
import time
import os
import tempfile
import shutil
import shellapi
import globalVars
import versionInfo

_wsh=None
def _getWSH():
	global _wsh
	if not _wsh:
		import comtypes
		_wsh=comtypes.client.CreateObject("wScript.Shell")
		return _wsh

def createShortcut(path,targetPath=None,arguments=None,iconLocation=None,workingDirectory=None,hotkey=None,prependSpecialFolder=None):
	wsh=_getWSH()
	if prependSpecialFolder:
		specialPath=wScript.SpecialFolders("prependSpecialFolder")
		path=os.path.join(specialPath,path)
	if not os.path.isdir(os.path.dirname(path)):
		os.makedirs(path)
	short=wScript.CreateShortcut(path)
	short.TargetPath=targetPath
	short.arguments=arguments
	short.Hotkey=hotkey
	short.IconLocation=iconLocation
	short.workingDirectory=workingDirectory
	short.Save()

def deleteShortcut(path,prependSpecialFolder=None):
	wsh=_getWSH()
	if prependSpecialFolder:
		specialPath=wScript.SpecialFolders("prependSpecialFolder")
		path=os.path.join(specialPath,path)
	try:
		os.remove(path)
	except OSError:
		pass

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
	sourcePath=u"c:\\users\\mick\\programming\\bzr\\nvda\\work\\dist"
	sourceConfigPath=globalVars.appArgs.configPath
	for curSourceDir,subDirs,files in os.walk(sourcePath):
		if os.stat(curSourceDir)==os.stat(sourceConfigPath):
			del subDirs[:]
			continue
		curDestDir=os.path.join(destPath,os.path.relpath(curSourceDir,sourcePath))
		if not os.path.isdir(curDestDir):
			os.makedirs(curDestDir)
		for f in files:
			sourceFilePath=os.path.join(curSourceDir,f)
			destFilePath=os.path.join(destPath,os.path.relpath(sourceFilePath,sourcePath))
			if windll.kernel32.CopyFileW(u"\\\\?\\"+sourceFilePath,u"\\\\?\\"+destFilePath,False)==0:
				tempPath=tempfile.mktemp(dir=os.path.dirname(destFilePath))
				os.rename(destFilePath,tempPath)
				windll.kernel32.MoveFileExW(u"\\\\?\\"+tempPath,None,4)
				windll.kernel32.CopyFileW(u"\\\\?\\"+sourceFilePath,u"\\\\?\\"+destFilePath,False)

def copyUserConfig(destPath):
	sourcePath=globalVars.appArgs.configPath
	for curSourceDir,subDirs,files in os.walk(sourcePath):
		curDestDir=os.path.join(destPath,os.path.relpath(curSourceDir,sourcePath))
		if not os.path.isdir(curDestDir):
			os.makedirs(curDestDir)
		for f in files:
			sourceFilePath=os.path.join(curSourceDir,f)
			destFilePath=os.path.join(destPath,os.path.relpath(sourceFilePath,sourcePath))
			if windll.kernel32.CopyFileW(u"\\\\?\\"+sourceFilePath,u"\\\\?\\"+destFilePath,False)==0:
				tempPath=tempfile.mktemp(dir=os.path.dirname(destFilePath))
				os.rename(destFilePath,tempPath)
				windll.kernel32.MoveFileExW(u"\\\\?\\"+tempPath,None,4)
				windll.kernel32.CopyFileW(u"\\\\?\\"+sourceFilePath,u"\\\\?\\"+destFilePath,False)

uninstallerRegInfo={
	"DisplayName":versionInfo.version,
	"DisplayVersion":versionInfo.version,
	"DisplayIcon":u"{installDir}\\images\\nvda.ico",
	"InstallDir":u"{installDir}",
	"Publisher":versionInfo.publisher,
	"UninstallDirectory":u"{InstallDir}",
	"UninstallString":u"{installDir}\\uninstall.exe",
	"URLInfoAbout":versionInfo.url,
}

def registerInstallation(installDir,startMenuFolder,shouldInstallService,shouldCreateDesktopShortcut,startOnLogonScreen):
	import _winreg
	with _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\NVDA",0,_winreg.KEY_WRITE) as k:
		for name,value in uninstallerRegInfo: 
			_winreg.SetValueEx(k,name,None,_winreg.REG_SZ,value.format(installDir=installDir))
	with _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\nvda.exe",0,_winreg.KEY_WRITE) as k:
		_winreg.SetValueEx(k,"@",None,_winreg.REG_SZ,installDir)
	with _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\nvda",0,_winreg.KEY_WRITE) as k:
		_winreg.SetValueEx(k,"startMenuFolder",None,_winreg.REG_SZ,startMenuFolder)
		if startOnLogonScreen is not None:
			_winreg.SetValueEx(k,"startOnLogonScreen",None,_winreg.REG_SZ,"1" if startOnLogonScreen else "0")
	if shouldInstallService:
		import nvda_service
		nvda_service.installService(installDir)
		nvda_service.startService()
	NVDAExe=os.path.join(installDir,u"nvda.exe")
	if shouldCreateDesktopShortcut:
		createShortcut(u"nvda.lnk",targetPath=NVDAExe,arguments="-r",iconLocation=NVDAExe+",0",hotkey="CTRL+ALT+N",workingDirectory=installDir,prependSpecialFolder="Desktop")
	createShortcut(os.path.join(startMenuFolder,"NVDA.lnk"),targetPath=NVDAExe,iconLocation=NVDAExe+",0",workingDirectory=installDir,prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("NVDA Website")+".lnk"),targetPath=versionInfo.url,prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("Uninstall NVDA")+".lnk"),targetPath=os.path.join(installDir,"uninstall.exe"),workingDirectory=installDir,prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("Explore NVDA user configuration directory")+".lnk"),targetPath=os.path.join(installDir,"nvda_slave.exe"),arguments="exploreUserconfigPath",workingDirectory=installDir,prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("Documentation"),_("Key Command quick reference")+".lnk"),targetPath=getdocFilePath("keycommands.html",installDir),prependSpecialFolder="AllUsersPrograms")
	createShortcut(os.path.join(startMenuFolder,_("Documentation"),_("User Guide")+".lnk"),targetPath=getdocFilePath("userGuide.html",installDir),prependSpecialFolder="AllUsersPrograms")

def unregisterInstallation(forUpdate=False):
	import nvda_service
	try:
		nvda_service.stopService()
	except:
		pass
	nvda_service.removeService()
	deleteShortcut(u"nvda.lnk",prependSpecialFolder="Desktop")
	deleteShortcut(os.path.join(startMenuFolder,"NVDA.lnk"),prependSpecialFolder="AllUsersPrograms")
	deleteShortcut(os.path.join(startMenuFolder,_("NVDA Website")+".lnk"),prependSpecialFolder="AllUsersPrograms")
	deleteShortcut(os.path.join(startMenuFolder,_("Uninstall NVDA")+".lnk"),prependSpecialFolder="AllUsersPrograms")
	deleteShortcut(os.path.join(startMenuFolder,_("Explore NVDA user configuration directory")+".lnk"),prependSpecialFolder="AllUsersPrograms")
	deleteShortcut(os.path.join(startMenuFolder,_("Documentation"),_("Key Command quick reference")+".lnk"),prependSpecialFolder="AllUsersPrograms")
	deleteShortcut(os.path.join(startMenuFolder,_("Documentation"),_("User Guide")+".lnk"),prependSpecialFolder="AllUsersPrograms")
	if not forUpdate:
		_winreg.DeleteKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\nvda",0,None)
		_winreg.DeleteKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\nvda.exe",0,None)
		_winreg.DeleteKeyEx(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\nvda",0,None)

def install(installDir,startMenuFolder,shouldInstallService=True,shouldCreateDesktopShortcut=True,shouldRunAtLogon=None,forUpdate=False):
	unregisterInstallation(forUpdate)
	copyProgramFiles(installDir)
	registerInstallation(installDir,startMenuFolder,shouldInstallService,shouldCreateDesktopShortcut,startOnLogonScreen)

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
			copyProgramFiles(destPath)
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
