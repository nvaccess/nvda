#appModuleHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Manages appModules.
@ivar current: holds the currently loaded appModule
@type current: appModule
"""

from new import instancemethod
import pythoncom
import win32com.client
import datetime
import re
import ctypes
import os
import sayAllHandler
from keyUtils import key
import debug
import audio
import winUser
import winKernel
import config

#This is here so that the appModules are able to import modules from the appModules dir themselves
__path__=['.\\appModules']

#Dictionary of windowHandle:appModule paires used to hold the currently running modules
runningTable={}
#variable to hold the default appModule instance
default=None

#base class for appModules
class appModule(object):

	def __init__(self,hwnd,processID):
		self.appWindow=hwnd
		self.processID=processID
		self.appName=self.__class__.__module__
		self._keyMap={}


#regexp to collect the key and script from a line in a keyMap file 
re_keyScript=re.compile(r'^\s*(?P<key>[\w+]+)\s*=\s*(?P<script>[\w]+)\s*$')

# Initialise WMI; required for getAppName.
_wmi = win32com.client.GetObject('winmgmts:')

def getAppName(window):
	"""Finds out the application name of the given window.
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
	return os.path.isfile('appModules/%s.py'%name)

def getKeyMapFileName(appName,layout):
	if os.path.isfile('appModules/%s_%s.kbd'%(appName,layout)):
		return 'appModules/%s_%s.kbd'%(appName,layout)
	elif layout!='desktop':
		return getKeyMapFileName(appName,'desktop')
	else:
		return None

def getActiveModule():
	appWindow=winUser.getAncestor(winUser.getForegroundWindow(),winUser.GA_ROOTOWNER)
	if runningTable.has_key(appWindow):
		mod=runningTable[appWindow]
	else:
		mod=None
	if mod is None:
		mod=default
	return mod

def update():
	for w in [x for x in runningTable if not winUser.isWindow(x)]:
		if runningTable[w]:
			debug.writeMessage("appModuleHandler.update: removing module %s at %s"%(runningTable[w].__module__,w))
		del runningTable[w]
	appWindow=winUser.getAncestor(winUser.getForegroundWindow(),winUser.GA_ROOTOWNER)
	if not appWindow:
		return
	if not runningTable.has_key(appWindow):
		appName=getAppName(appWindow)
		if not appName:
			debug.writeMessage("appModuleHandler.update: could not get application name from window %s (%s)"%(appWindow,winUser.getClassName(appWindow)))
			return
		mod=fetchModule(appName,appWindow)
		if mod:
			mod._keyMap=default._keyMap.copy()
			loadKeyMap(appName,mod)
		runningTable[appWindow]=mod
		if mod:
			debug.writeMessage("appModuleHandler.update: loaded module %s"%appName)
		else:
			debug.writeMessage("appModuleHandler.update: No module for %s"%appName)

def loadKeyMap(appName,mod):
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

def fetchModule(appName,appWindow):
	if not moduleExists(appName):
		return None
	try:
		mod=__import__(appName,globals(),locals(),[]).appModule(appWindow,winUser.getWindowThreadProcessID(appWindow))
	except:
		debug.writeException("appModuleHandler.loadModule: Error in appModule %s"%appName)
		audio.speakMessage("Error in appModule %s"%appName,wait=True)
		return None
	return mod

def initialize():
	global default
	default=fetchModule('_default',winUser.getDesktopWindow())
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
class appModule(object):

	@classmethod
	def bindKey(cls,keyName,scriptName):
		scriptName="script_%s"%scriptName
		if not hasattr(cls,scriptName):
			raise ValueError("no script \"%s\" in %s"%(scriptName,cls))
		if not cls.__dict__.has_key('_keyMap'):
			cls._keyMap=getattr(cls,'_keyMap',{}).copy()
		cls._keyMap[key(keyName)]=getattr(cls,scriptName)

	_keyMap={}

	def __init__(self,hwnd,processID):
		self.appWindow=hwnd
		self.processID=processID
		self.appName=self.__class__.__module__

	def getScript(self,keyPress):
		"""
Returns a script (instance method) if one is assigned to the keyPress given.
@param keyPress: The key you wish to retreave the script for
@type keyPress: key
""" 
		if self._keyMap.has_key(keyPress):
			return instancemethod(self._keyMap[keyPress],self,self.__class__)
