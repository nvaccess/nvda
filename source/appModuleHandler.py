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

import imp
import itertools
import re
import ctypes
import os
import baseObject
import globalVars
from logHandler import log
import speech
import winUser
import winKernel
import config
import NVDAObjects #Catches errors before loading default appModule
import api

#This is here so that the appModules are able to import modules from the appModules dir themselves
__path__=['.\\appModules']

#Dictionary of processID:appModule paires used to hold the currently running modules
runningTable={}
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

def getAppNameFromProcessID(processID,includeExt=False):
	"""Finds out the application name of the given process.
	@param processID: the ID of the process handle of the application you wish to get the name of.
	@type processID: int
	@param includeExt: C{True} to include the extension of the application's executable filename, C{False} to exclude it.
	@type window: bool
	@returns: application name
	@rtype: str
	"""
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
	log.debug("appName: %s"%appName)
	return appName

def getKeyMapFileName(appName,layout):
	"""Finds the file path for the key map file, given the application name and keyboard layout.
	@param appName: name of application
	@type appName: str
	@returns: file path of key map file (.kbd file)
	@rtype: str
	"""
	fname='appModules/%s_%s.kbd'%(appName,layout)
	if os.path.isfile(fname):
		log.debug("Found keymap file for %s at %s"%(appName,fname)) 
		return fname
	elif layout!='desktop':
		return getKeyMapFileName(appName,'desktop')
	else:
		log.debug("No keymapFile for %s"%appName)
		return None

def getAppModuleForNVDAObject(obj):
	if not isinstance(obj,NVDAObjects.window.Window):
		return
	return getAppModuleFromProcessID(obj.windowProcessID)

def getAppModuleFromProcessID(processID):
	"""Finds the appModule that is for the given process ID. The module is also cached for later retreavals.
	@param processID: The ID of the process for which you wish to find the appModule.
	@type processID: int
	@returns: the appModule, or None if there isn't one
	@rtype: appModule 
	"""
	mod=runningTable.get(processID)
	if not mod:
		appName=getAppNameFromProcessID(processID)
		mod=fetchAppModule(processID,appName)
		if not mod:
			mod=fetchAppModule(processID,appName,useDefault=True)
		if not mod:
			raise RuntimeError("error fetching default appModule")
		runningTable[processID]=mod
	return mod

def update(processID):
	"""Removes any appModules from te cache who's process has died, and also tries to load a new appModule for the given process ID if need be.
	@param processID: the ID of the process.
	@type processID: int
	"""
	for deadMod in [mod for mod in runningTable.itervalues() if not mod.isAlive]:
		log.debug("application %s closed"%deadMod.appName)
		del runningTable[deadMod.processID];
		if deadMod in set(o.appModule for o in api.getFocusAncestors()+[api.getFocusObject()] if o and o.appModule):
			if hasattr(deadMod,'event_appLoseFocus'):
				deadMod.event_appLoseFocus();
		getAppModuleFromProcessID(processID)

def fetchAppModule(processID,appName,useDefault=False):
	"""Returns an appModule found in the appModules directory, for the given application name.
	@param processID: process ID for it to be associated with
	@type processID: integer
	@param appName: the application name for which an appModule should be found.
	@type appName: str
	@returns: the appModule, or None if not found
	@rtype: AppModule
	"""  
	mod=None
	friendlyAppName=appName
	if useDefault:
		appName='_default'
	try:
		found=imp.find_module(appName,__path__)
		try:
			#best to use imp.load_module but then imports of other appModules in this module fail
			mod=__import__(appName,globals(),locals(),[]).AppModule(processID,friendlyAppName)
		except:
			log.error("error in appModule %s"%appName,exc_info=True)
			speech.speakMessage(_("Error in appModule %s")%appName)
	except ImportError: #find_module couldn't find an appModule
		pass
	if mod and isinstance(mod,AppModule):
		mod.loadKeyMap()
		return mod


def initialize():
	"""Initializes the appModule subsystem. 
	"""
	global NVDAProcessID,default
	NVDAProcessID=os.getpid()

#base class for appModules
class AppModule(baseObject.ScriptableObject):
	"""AppModule base class
	@var appName: the application name
	@type appName: str
	@var processID: the ID of the process this appModule is for.
	@type processID: int
	"""

	def __init__(self,processID,appName=None):
		self.processID=processID
		if appName is None:
			appName=getAppNameFromProcessID(processID)
		self.appName=appName
		self.processHandle=winKernel.openProcess(winKernel.SYNCHRONIZE,False,processID)

	def __repr__(self):
		return "<%s (appName %s, process ID %s) at address %x>"%(self.appModuleName,self.appName,self.processID,id(self))

	def _get_appModuleName(self):
		return "%s.%s"%(self.__class__.__module__.split('.')[-1],self.__class__.__name__)

	def _get_isAlive(self):
		return bool(winKernel.waitForSingleObject(self.processHandle,0))

	def __del__(self):
		winKernel.closeHandle(self.processHandle)

	def loadKeyMap(self):
		"""Loads a key map in to this appModule . if the key map exists. It takes in to account what layout NVDA is currently set to.
		"""  
		if '_keyMap' in self.__dict__:
			self._keyMap={}
		layout=config.conf["keyboard"]["keyboardLayout"]
		for modClass in reversed(list(itertools.takewhile(lambda x: issubclass(x,AppModule) and x is not AppModule,self.__class__.__mro__))):
			name=modClass.__module__.split('.')[-1]
			keyMapFileName=getKeyMapFileName(name,layout)
			if not keyMapFileName:
				continue
			keyMapFile=open(keyMapFileName,'r')
			bindCount=0
			#If the appModule already has a running keyMap, clear it
			for line in (x for x in keyMapFile if not x.startswith('#') and not x.isspace()):
				m=re_keyScript.match(line)
				if m:
					try:
						self.bindKey_runtime(m.group('key'),m.group('script'))
						bindCount+=1
					except:
						log.error("error binding %s to %s in appModule %s"%(m.group('script'),m.group('key'),self))
			log.debug("added %s bindings to appModule %s from file %s"%(bindCount,self,keyMapFileName))
