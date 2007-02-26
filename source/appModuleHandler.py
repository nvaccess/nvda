#appModuleHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Manages appModules.
@var default: holds the default appModule.
@type: default: appModule
@var runningTable: a dctionary of the currently running appModules, using their application's main window handle as a key value.
@type runningTable: dict
@var re_keyScript: a compiled regular expression that can grab a keyName and a script name from a line in a NVDA key map file (kbd file).
@type re_keyScript: regular expression
"""

from new import instancemethod
import pythoncom
import win32com.client
import datetime
import re
import ctypes
import os
import baseObject
import sayAllHandler
from keyUtils import key
import debug
import audio
import winUser
import winKernel
import config
import NVDAObjects #Catches errors before loading default appModule

#This is here so that the appModules are able to import modules from the appModules dir themselves
__path__=['.\\appModules']

#Dictionary of windowHandle:appModule paires used to hold the currently running modules
runningTable={}
#variable to hold the default appModule instance
default=None

#regexp to collect the key and script from a line in a keyMap file 
re_keyScript=re.compile(r'^\s*(?P<key>[\w+]+)\s*=\s*(?P<script>[\w]+)\s*$')

# Initialise WMI; required for getAppName.
_wmi = win32com.client.GetObject('winmgmts:')

def getAppName(window):
	"""Finds out the application name of the given window.
@param window: the window handle of the application you wish to get the name of.
@type window: int
@returns: application name
@rtype: string
"""
	try:
		processID=winUser.getWindowThreadProcessID(winUser.getAncestor(window,winUser.GA_ROOTOWNER))
		result  =  _wmi.ExecQuery("select * from Win32_Process where ProcessId=%d" % processID[0])
		if len(result) > 0:
			appName=result[0].Properties_('Name').Value
			appName=os.path.splitext(appName)[0].lower()
			return appName
		else:
			return None
	except:
		return None

def moduleExists(name):
	"""Checks if an appModule by the given application name exists.
@param name: the application name
@type name: string
@returns: True if it exists, false otherwise.
@rtype: bool
"""
	return os.path.isfile('appModules/%s.py'%name)

def getKeyMapFileName(appName,layout):
	"""Finds the file path for the key map file, given the application name and keyboard layout.
@param appName: name of application
@type appName: string
@returns: file path of key map file (.kbd file)
@rtype: string 
"""
	if os.path.isfile('appModules/%s_%s.kbd'%(appName,layout)):
		return 'appModules/%s_%s.kbd'%(appName,layout)
	elif layout!='desktop':
		return getKeyMapFileName(appName,'desktop')
	else:
		return None

def getActiveModule():
	"""Finds the appModule that is for the current foreground window.
@returns: the active appModule
@rtype: appModule
"""
		return getAppModuleFromWindow(winUser.getForegroundWindow())

def getAppModuleFromWindow(windowHandle):
	"""Finds the appModule that is for the given window handle. This window handle can be any window with in an application, not just the app main window.
@param windowHandle: window who's appModule you want to find
@type windowHandle: int
@returns: the appModule, or None if there isn't one
@rtype: appModule 
"""
	appWindow=winUser.getAncestor(windowHandle,winUser.GA_ROOTOWNER)
	if runningTable.has_key(appWindow):
		mod=runningTable[appWindow]
	else:
		mod=None
	return mod

def update(windowHandle):
	"""Removes any appModules connected with windows that no longer exist, and uses the given window handle to try and load a new appModule if need be.
@param windowHandle: any window in an application
@type windowHandle: int
"""
	for w in [x for x in runningTable if not winUser.isWindow(x)]:
		debug.writeMessage("appModuleHandler.update: application %s closed, window %s"%(runningTable[w].appName,w))
		del runningTable[w]
	appWindow=winUser.getAncestor(windowHandle,winUser.GA_ROOTOWNER)
	if appWindow<=0 or not winUser.isWindowVisible(appWindow) or not winUser.isWindowEnabled(appWindow):
		return
	if not runningTable.has_key(appWindow):
		appName=getAppName(appWindow)
		if not appName:
			debug.writeMessage("appModuleHandler.update: could not get application name from window %s (%s)"%(appWindow,winUser.getClassName(appWindow)))
			return
		debug.writeMessage("appModuleHandler.update: Application %s registered, window %s (%s)"%(appName,appWindow,winUser.getClassName(appWindow)))
		mod=fetchModule(appName)
		if mod: 
			mod=mod(appName,appWindow)
			debug.writeMessage("Loaded appModule %s"%mod.appName) 
			loadKeyMap(appName,mod)
		runningTable[appWindow]=mod

def loadKeyMap(appName,mod):
	"""Loads a key map in to the given appModule, with the given name. if the key map exists. It takes in to account what layout NVDA is currently set to.
@param appName: the application name
@type appName: string
@param mod: athe appModule
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
				debug.writeException("appModuleHandler.loadKeyMap: error binding %s to %s in module %s"%(m.group('script'),m.group('key'),appName))
	debug.writeMessage("appModuleHandler.loadKeyMap: added %s bindings to module %s from file %s"%(bindCount,appName,keyMapFileName))
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
			mod=__import__(appName,globals(),locals(),[]).appModule(appName,appWindow)
		except:
			debug.writeException("appModuleHandler.loadModule: Error in appModule %s"%appName)
			audio.speakMessage("Error in appModule %s"%appName,wait=True)
	if mod is None:
		mod=appModule(appName,appWindow)
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
			debug.writeMessage("appModuleHandler.initialize: loaded default module")
		else:
			audio.speakMessage("Could not load default module keyMap",wait=True)
			raise RuntimeError("appModuleHandler.initialize: could not load default module keymap")
	else:
		audio.speakMessage("Could not load default module ",wait=True)
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

