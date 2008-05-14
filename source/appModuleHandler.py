#appModuleHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Manages appModules.
@var default: holds the default appModule.
@type default: appModule
@var runningTable: a dictionary of the currently running appModules, using their application's main window handle as a key.
@type runningTable: dict
@var re_keyScript: a compiled regular expression that can grab a keyName and a script name from a line in a NVDA key map file (kbd file).
@type re_keyScript: regular expression
"""

import re
import ctypes
import os
import logging
import baseObject
import globalVars
import speech
import winUser
import winKernel
import config
import NVDAObjects #Catches errors before loading default appModule

#This is here so that the appModules are able to import modules from the appModules dir themselves
__path__=['.\\appModules']

#Dictionary of windowHandle:appModule paires used to hold the currently running modules
runningTable={}
#Variable to hold the active (focused) appModule
activeModule=None
#variable to hold the default appModule instance
default=None
#: The process ID of NVDA itself.
NVDAProcessID=None

#regexp to collect the key and script from a line in a keyMap file 
re_keyScript=re.compile(r'^\s*(?P<key>[\S]+)\s*=\s*(?P<script>[\S]+)\s*$')

class TProcessEntry32(ctypes.Structure):
	_fields_ = [
		("dwSize",ctypes.c_ulong),
		("cntUsage", ctypes.c_ulong),
		("th32ProcessID", ctypes.c_ulong),
		("th32DefaultHeapID", ctypes.c_ulong),
		("th32ModuleID",ctypes.c_ulong),
		("cntThreads",ctypes.c_ulong),
		("th32ParentProcessID",ctypes.c_ulong),
		("pcPriClassBase",ctypes.c_long),
		("dwFlags",ctypes.c_ulong),
		("szExeFile", ctypes.c_char * 259)
	]

def getAppName(window,includeExt=False):
	"""Finds out the application name of the given window.
	@param window: the window handle of the application you wish to get the name of.
	@type window: int
	@param includeExt: C{True} to include the extension of the application's executable filename, C{False} to exclude it.
	@type window: bool
	@returns: application name
	@rtype: str
	"""
	processID=winUser.getWindowThreadProcessID(winUser.getAncestor(window,winUser.GA_ROOTOWNER))[0]
	if processID==NVDAProcessID:
		return "nvda.exe" if includeExt else "nvda"
	FSnapshotHandle = winKernel.kernel32.CreateToolhelp32Snapshot (2,0)
	FProcessEntry32 = TProcessEntry32()
	FProcessEntry32.dwSize = ctypes.sizeof(TProcessEntry32)
	ContinueLoop = winKernel.kernel32.Process32First(FSnapshotHandle, ctypes.byref(FProcessEntry32))
	appName = str()
	while ContinueLoop:
		if FProcessEntry32.th32ProcessID == processID:
			appName = FProcessEntry32.szExeFile
			break
		ContinueLoop = winKernel.kernel32.Process32Next(FSnapshotHandle, ctypes.byref(FProcessEntry32))
	winKernel.kernel32.CloseHandle(FSnapshotHandle)
	if not includeExt:
		appName=os.path.splitext(appName)[0].lower()
	globalVars.log.debug("appName: %s"%appName)
	return appName

def moduleExists(name):
	"""Checks if an appModule by the given application name exists.
	@param name: the application name
	@type name: str
	@returns: True if it exists, false otherwise.
	@rtype: bool
	"""
	res=os.path.isfile('appModules/%s.py'%name)
	globalVars.log.debug("Does appModules/%s.py exist: %s"%(name,res))
	return res

def getKeyMapFileName(appName,layout):
	"""Finds the file path for the key map file, given the application name and keyboard layout.
	@param appName: name of application
	@type appName: str
	@returns: file path of key map file (.kbd file)
	@rtype: str
	"""
	fname='appModules/%s_%s.kbd'%(appName,layout)
	if os.path.isfile(fname):
		globalVars.log.debug("Found keymap file for %s at %s"%(appName,fname)) 
		return fname
	elif layout!='desktop':
		return getKeyMapFileName(appName,'desktop')
	else:
		globalVars.log.debug("No keymapFile for %s"%appName)
		return None

def getActiveModule():
	"""Finds the appModule that is for the current foreground window.
	@returns: the active appModule
	@rtype: appModule
	"""
	fg=winUser.getForegroundWindow()
	mod=getAppModuleFromWindow(fg)
	if globalVars.log.getEffectiveLevel()<=logging.DEBUG:
		globalVars.log.debug("Using window %s (%s), got appModule %s"%(fg,winUser.getClassName(fg),mod))
	return mod

def getAppModuleForNVDAObject(obj):
	if not isinstance(obj,NVDAObjects.window.Window):
		return
	return getAppModuleFromWindow(obj.windowHandle)

def getAppModuleFromWindow(windowHandle):
	"""Finds the appModule that is for the given window handle.
	This window handle can be any window with in an application, not just the app main window.
	@param windowHandle: The window for which you wish to find the appModule.
	@type windowHandle: int
	@returns: the appModule, or None if there isn't one
	@rtype: appModule 
	"""
	appWindow=winUser.getAncestor(windowHandle,winUser.GA_ROOTOWNER)
	globalVars.log.debug("appWindow %s, from window %s"%(appWindow,windowHandle))
	mod=runningTable.get(appWindow)
	if mod:
		globalVars.log.debug("found appModule %s"%mod)
	else:
		globalVars.log.debug("no appModule")
	return mod

def update(windowHandle):
	"""Removes any appModules connected with windows that no longer exist, and uses the given window handle to try and load a new appModule if need be.
	@param windowHandle: any window in an application
	@type windowHandle: int
	"""
	global activeModule
	for w in [x for x in runningTable if not winUser.isWindow(x)]:
		if isinstance(activeModule,AppModule) and w==activeModule.appWindow: 
			if hasattr(activeModule,"event_appLooseFocus"):
				globalVars.log.debug("calling appLoseFocus event on appModule %s"%activeModule)
				activeModule.event_appLooseFocus()
			activeModule=None
		globalVars.log.info("application %s closed, window %s"%(runningTable[w].appName,w))
		del runningTable[w]
	appWindow=winUser.getAncestor(windowHandle,winUser.GA_ROOTOWNER)
	globalVars.log.debug("Using window %s, got appWindow %s"%(windowHandle,appWindow))
	if appWindow<=0:
		globalVars.log.debug("bad appWindow")
		return
	if appWindow not in runningTable:
		globalVars.log.debug("new appWindow")
		appName=getAppName(appWindow)
		if not appName:
			globalVars.log.warning("could not get application name from window %s (%s)"%(appWindow,winUser.getClassName(appWindow)))
			return
		mod=fetchModule(appName)
		if mod: 
			mod=mod(appName,appWindow)
			if mod.__class__!=AppModule:
				globalVars.log.info("Loaded appModule %s, %s"%(mod.appName,mod)) 
			loadKeyMap(appName,mod)
		runningTable[appWindow]=mod
	activeAppWindow=winUser.getAncestor(winUser.getForegroundWindow(),winUser.GA_ROOTOWNER)
	if isinstance(activeModule,AppModule) and activeAppWindow!=activeModule.appWindow: 
		globalVars.log.info("appModule %s lost focus"%activeModule)
		if hasattr(activeModule,"event_appLooseFocus"):
			activeModule.event_appLooseFocus()
		activeModule=None
	if not activeModule and activeAppWindow in runningTable:
		activeModule=runningTable[activeAppWindow]
		globalVars.log.info("appModule %s gained focus"%activeModule)
		if hasattr(activeModule,"event_appGainFocus"):
			activeModule.event_appGainFocus()

def loadKeyMap(appName,mod):
	"""Loads a key map in to the given appModule, with the given name. if the key map exists. It takes in to account what layout NVDA is currently set to.
	@param appName: the application name
	@type appName: str
	@param mod: the appModule
	@type mod: appModule
	"""  
	layout=config.conf["keyboard"]["keyboardLayout"]
	keyMapFileName=getKeyMapFileName(appName,layout)
	if not keyMapFileName:
		return False
	keyMapFile=open(keyMapFileName,'r')
	bindCount=0
	#If the appModule already has a running keyMap, clear it
	if '_keyMap' in mod.__dict__:
		mod._keyMap={}
	for line in (x for x in keyMapFile if not x.startswith('#') and not x.isspace()):
		m=re_keyScript.match(line)
		if m:
			try:
				mod.bindKey_runtime(m.group('key'),m.group('script'))
				bindCount+=1
			except:
				globalVars.log.error("error binding %s to %s in module %s"%(m.group('script'),m.group('key'),appName))
	globalVars.log.info("added %s bindings to module %s from file %s"%(bindCount,appName,keyMapFileName))
  	return True

def fetchModule(appName):
	"""Returns an appModule found in the appModules directory, for the given application name.
	It only returns the class, it must be initialized with a name and a window to actually be used.
	@param appName: the application name for which an appModule should be found.
	@type appName: str
	@returns: the appModule, or None if not found
	@rtype: appModule
	"""  
	mod=None
	if moduleExists(appName):
		try:
			mod=__import__(appName,globals(),locals(),[]).appModule
		except:
			globalVars.log.error("Error in appModule %s"%appName,exc_info=True)
			speech.speakMessage(_("Error in appModule %s")%appName)
			raise RuntimeError
	if mod is None:
		return AppModule
	return mod

def initialize():
	"""Initializes the appModule subsystem. 
	"""
	global NVDAProcessID,default
	NVDAProcessID=os.getpid()
	defaultModClass=fetchModule('_default')
	if defaultModClass:
		default=defaultModClass('_default',winUser.getDesktopWindow())
	if default:
		if loadKeyMap('_default',default):
			globalVars.log.info("loaded default module")
		else:
			speech.speakMessage(_("Could not load default module keyMap"),wait=True)
			raise RuntimeError("appModuleHandler.initialize: could not load default module keymap")
	else:
		speech.speakMessage(_("Could not load default module "),wait=True)
		raise RuntimeError("appModuleHandler.initialize: could not load default module ")

#base class for appModules
class AppModule(baseObject.ScriptableObject):
	"""AppModule base class
	@var appName: the application name
	@type appName: str
	@var appWindow: the application main window
	@type appWindow: int
	"""

	def __init__(self,appName,appWindow):
		self.appName=appName
		self.appWindow=appWindow

	def __repr__(self):
		return "AppModule (appName %s, appWindow %s) at address %x"%(self.appName,self.appWindow,id(self))
