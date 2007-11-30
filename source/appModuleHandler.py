#appModuleHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Manages appModules.
@var default: holds the default appModule.
@type: default: appModule
@var runningTable: a dictionary of the currently running appModules, using their application's main window handle as a key value.
@type runningTable: dict
@var re_keyScript: a compiled regular expression that can grab a keyName and a script name from a line in a NVDA key map file (kbd file).
@type re_keyScript: regular expression
"""

from new import instancemethod
import datetime
import re
import ctypes
import os
import logging
import baseObject
import sayAllHandler
from keyUtils import key
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

#regexp to collect the key and script from a line in a keyMap file 
re_keyScript=re.compile(r'^\s*(?P<key>[\w+]+)\s*=\s*(?P<script>[\w]+)\s*$')

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
@param includeExt: Optimal parameter when set to true return value will include extension of the application executable.
@type window: boolean
@returns: application name
@rtype: string
"""
	processID=winUser.getWindowThreadProcessID(winUser.getAncestor(window,winUser.GA_ROOTOWNER))[0]
	FSnapshotHandle = winKernel.kernel32.CreateToolhelp32Snapshot (2,0)
	FProcessEntry32 = TProcessEntry32()
	FProcessEntry32.dwSize = ctypes.sizeof(TProcessEntry32)
	ContinueLoop = winKernel.kernel32.Process32First(FSnapshotHandle, ctypes.byref(FProcessEntry32))
	appName = str()
	while ContinueLoop:
		if FProcessEntry32.th32ProcessID == processID:
			appName = FProcessEntry32.szExeFile
			break
		ContinueLoop = winKernel.kernel32.Process32Next(FSnapshotHandle, ctypes.byref(FProcessEntry32));
	winKernel.kernel32.CloseHandle(FSnapshotHandle)
	if not includeExt:
		appName=os.path.splitext(appName)[0].lower()
	globalVars.log.debug("appName: %s"%appName)
	return appName

def moduleExists(name):
	"""Checks if an appModule by the given application name exists.
@param name: the application name
@type name: string
@returns: True if it exists, false otherwise.
@rtype: bool
"""
	res=os.path.isfile('appModules/%s.py'%name)
	globalVars.log.debug("Does appModules/%s.py exist: %s"%(name,res))
	return res

def getKeyMapFileName(appName,layout):
	"""Finds the file path for the key map file, given the application name and keyboard layout.
@param appName: name of application
@type appName: string
@returns: file path of key map file (.kbd file)
@rtype: string 
"""
	if os.path.isfile('appModules/%s_%s.kbd'%(appName,layout)):
		globalVars.log.debug("Found keymap file for %s at appModules/%s_%s.kbd"%(appName,appName,layout)) 
		return 'appModules/%s_%s.kbd'%(appName,layout)
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

def getAppModuleFromWindow(windowHandle):
	"""Finds the appModule that is for the given window handle. This window handle can be any window with in an application, not just the app main window.
@param windowHandle: window who's appModule you want to find
@type windowHandle: int
@returns: the appModule, or None if there isn't one
@rtype: appModule 
"""
	appWindow=winUser.getAncestor(windowHandle,winUser.GA_ROOTOWNER)
	globalVars.log.debug("appWindow %s, from window %s"%(appWindow,windowHandle))
	if runningTable.has_key(appWindow):
		mod=runningTable[appWindow]
		globalVars.log.debug("found appModle %s"%mod)
	else:
		mod=None
		globalVars.log.debug("no appModule")
	return mod

def update(windowHandle):
	"""Removes any appModules connected with windows that no longer exist, and uses the given window handle to try and load a new appModule if need be.
@param windowHandle: any window in an application
@type windowHandle: int
"""
	global activeModule
	for w in [x for x in runningTable if not winUser.isWindow(x)]:
		if isinstance(activeModule,appModule) and w==activeModule.appWindow: 
			if hasattr(activeModule,"event_appLooseFocus"):
				globalVars.log.debug("calling appLoseFocus event on appModule %s"%activeModule)
				activeModule.event_appLooseFocus()
			activeModule=None
		globalVars.log.info("application %s closed, window %s"%(runningTable[w].appName,w))
		del runningTable[w]
	appWindow=winUser.getAncestor(windowHandle,winUser.GA_ROOTOWNER)
	globalVars.log.debug("Using window %s, got appWindow %s"%(windowHandle,appWindow))
	if appWindow<=0 or not winUser.isWindowVisible(appWindow) or not winUser.isWindowEnabled(appWindow):
		globalVars.log.debug("bad appWindow")
		return
	if not runningTable.has_key(appWindow):
		globalVars.log.debug("new appWindow")
		appName=getAppName(appWindow)
		if not appName:
			globalVars.log.warning("could not get application name from window %s (%s)"%(appWindow,winUser.getClassName(appWindow)))
			return
		mod=fetchModule(appName)
		if mod: 
			mod=mod(appName,appWindow)
			if mod.__class__!=appModule:
				globalVars.log.info("Loaded appModule %s, %s"%(mod.appName,mod)) 
			loadKeyMap(appName,mod)
		runningTable[appWindow]=mod
	activeAppWindow=winUser.getAncestor(winUser.getForegroundWindow(),winUser.GA_ROOTOWNER)
	if isinstance(activeModule,appModule) and activeAppWindow!=activeModule.appWindow: 
		globalVars.log.info("appModule %s lost focus"%activeModule)
		if hasattr(activeModule,"event_appLooseFocus"):
			activeModule.event_appLooseFocus()
		activeModule=None
	if not activeModule and runningTable.has_key(activeAppWindow):
		activeModule=runningTable[activeAppWindow]
		globalVars.log.info("appModule %s gained focus"%activeModule)
		if hasattr(activeModule,"event_appGainFocus"):
			activeModule.event_appGainFocus()

def loadKeyMap(appName,mod):
	"""Loads a key map in to the given appModule, with the given name. if the key map exists. It takes in to account what layout NVDA is currently set to.
@param appName: the application name
@type appName: string
@param mod: the appModule
@type mod: appModule
"""  
	layout=config.conf["keyboard"]["keyboardLayout"]
	keyMapFileName=getKeyMapFileName(appName,layout)
	if not keyMapFileName:
		return False
	keyMapFile=open(keyMapFileName,'r')
	bindCount=0
	for line in filter(lambda x: not x.startswith('#') and not x.isspace(),keyMapFile.readlines()):
		m=re_keyScript.match(line)
		if m:
			try:
				mod.bindKey(m.group('key'),m.group('script'))
				bindCount+=1
			except:
				globalVars.log.error("error binding %s to %s in module %s"%(m.group('script'),m.group('key'),appName))
	globalVars.log.info("added %s bindings to module %s from file %s"%(bindCount,appName,keyMapFileName))
  	return True

def fetchModule(appName):
	"""Returns an appModule found in the appModules directory, for the given application name. It only returns the class, it must be initialized with a name and a window to actually be used.
@param appName: the application name who's appModule to find
@type appName: string
@returns: the appModule, or None if not found
@rtype: appModule
"""  
	mod=None
	if moduleExists(appName):
		try:
			mod=__import__(appName,globals(),locals(),[]).appModule
		except:
			globalVars.log.error("Error in appModule %s"%appName)
			speech.speakMessage(_("Error in appModule %s")%appName,wait=True)
			raise RuntimeError
	if mod is None:
		return appModule
	return mod

def initialize():
	"""Initializes the appModule subsystem. 
"""
	global default
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
class appModule(baseObject.scriptableObject):
	"""AppModule base class
@var appName: the application name
@type appName: string
@var appWindow: the application main window
@type appWindow: int
"""

	def __init__(self,appName,appWindow):
		self.appName=appName
		self.appWindow=appWindow

	def __repr__(self):
		return "AppModule (appName %s, appWindow %s) at address %x"%(self.appName,self.appWindow,id(self))
