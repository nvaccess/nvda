#appModuleHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Manages appModules.
@var runningTable: a dictionary of the currently running appModules, using their application's main window handle as a key.
@type runningTable: dict
@var re_keyScript: a compiled regular expression that can grab a keyName and a script name from a line in a NVDA key map file (kbd file).
@type re_keyScript: regular expression
"""

import itertools
import re
import ctypes
import os
import pkgutil
import baseObject
import globalVars
from logHandler import log
import NVDAHelper
import ui
import winUser
import winKernel
import config
import NVDAObjects #Catches errors before loading default appModule
import api
import unicodedata
import appModules

#Dictionary of processID:appModule paires used to hold the currently running modules
runningTable={}
#: The process ID of NVDA itself.
NVDAProcessID=None
_importers=None

#regexp to collect the key and script from a line in a keyMap file 
re_keyScript=re.compile(r'^\s*(?P<key>[\S]+)\s*=\s*(?P<script>[\S]+)\s*$')

class processEntry32W(ctypes.Structure):
	_fields_ = [
		("dwSize",ctypes.wintypes.DWORD),
		("cntUsage", ctypes.wintypes.DWORD),
		("th32ProcessID", ctypes.wintypes.DWORD),
		("th32DefaultHeapID", ctypes.wintypes.DWORD),
		("th32ModuleID",ctypes.wintypes.DWORD),
		("cntThreads",ctypes.wintypes.DWORD),
		("th32ParentProcessID",ctypes.wintypes.DWORD),
		("pcPriClassBase",ctypes.c_long),
		("dwFlags",ctypes.wintypes.DWORD),
		("szExeFile", ctypes.c_wchar * 260)
	]

def getAppNameFromProcessID(processID,includeExt=False):
	"""Finds out the application name of the given process.
	@param processID: the ID of the process handle of the application you wish to get the name of.
	@type processID: int
	@param includeExt: C{True} to include the extension of the application's executable filename, C{False} to exclude it.
	@type window: bool
	@returns: application name
	@rtype: unicode or str
	"""
	if processID==NVDAProcessID:
		return "nvda.exe" if includeExt else "nvda"
	FSnapshotHandle = winKernel.kernel32.CreateToolhelp32Snapshot (2,0)
	FProcessEntry32 = processEntry32W()
	FProcessEntry32.dwSize = ctypes.sizeof(processEntry32W)
	ContinueLoop = winKernel.kernel32.Process32FirstW(FSnapshotHandle, ctypes.byref(FProcessEntry32))
	appName = unicode()
	while ContinueLoop:
		if FProcessEntry32.th32ProcessID == processID:
			appName = FProcessEntry32.szExeFile
			break
		ContinueLoop = winKernel.kernel32.Process32NextW(FSnapshotHandle, ctypes.byref(FProcessEntry32))
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
	for dir in appModules.__path__+['.\\appModules']:
		# Python's import paths aren't unicode, but we prefer to deal with unicode, so convert them.
		dir = dir.decode("mbcs")
		fname = os.path.join(dir, '%s_%s.kbd' % (appName, layout))
		if os.path.isfile(fname):
			log.debug("Found keymap file for %s at %s"%(appName,fname)) 
			return fname

	if layout!='desktop':
		# Fall back to desktop.
		return getKeyMapFileName(appName,'desktop')

	log.debug("No keymapFile for %s"%appName)
	return None

def getAppModuleForNVDAObject(obj):
	if not isinstance(obj,NVDAObjects.NVDAObject):
		return
	return getAppModuleFromProcessID(obj.processID)

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

def doesAppModuleExist(name):
	return any(importer.find_module("appModules.%s" % name) for importer in _importers)

def fetchAppModule(processID,appName,useDefault=False):
	"""Returns an appModule found in the appModules directory, for the given application name.
	@param processID: process ID for it to be associated with
	@type processID: integer
	@param appName: the application name for which an appModule should be found.
	@type appName: unicode or str
	@returns: the appModule, or None if not found
	@rtype: AppModule
	"""  
	friendlyAppName=appName
	if useDefault:
		appName='_default'

	# First, check whether the module exists.
	# We need to do this separately because even though an ImportError is raised when a module can't be found, it might also be raised for other reasons.
	try:
		exists = doesAppModuleExist(appName)
	except UnicodeEncodeError:
		# Since Python can't handle unicode characters in module names, we need to decompose unicode string and strip out accents.
		appName = unicodedata.normalize("NFD", appName)
		exists = doesAppModuleExist(appName)
	if not exists:
		# It is not an error if the module doesn't exist.
		return None

	try:
		mod = __import__("appModules.%s" % appName, globals(), locals(), ("appModules",)).AppModule(processID, friendlyAppName)
	except:
		log.error("error in appModule %s"%appName, exc_info=True)
		ui.message(_("Error in appModule %s")%appName)
		return None

	mod.loadKeyMap()
	return mod

def initialize():
	"""Initializes the appModule subsystem. 
	"""
	global NVDAProcessID,_importers
	NVDAProcessID=os.getpid()
	config.addConfigDirsToPythonPackagePath(appModules)
	_importers=list(pkgutil.iter_importers("appModules._default"))

#base class for appModules
class AppModule(baseObject.ScriptableObject):
	"""AppModule base class
	@var appName: the application name
	@type appName: str
	@var processID: the ID of the process this appModule is for.
	@type processID: int
	"""

	selfVoicing=False #Set to true so all undefined events and script requests are silently dropped.

	_overlayClassCache={}

	def __init__(self,processID,appName=None):
		self.processID=processID
		self.helperLocalBindingHandle=NVDAHelper.localLib.createConnection(processID)
		if appName is None:
			appName=getAppNameFromProcessID(processID)
		self.appName=appName
		self.processHandle=winKernel.openProcess(winKernel.SYNCHRONIZE,False,processID)

	def __repr__(self):
		return "<%s (appName %s, process ID %s) at address %x>"%(self.appModuleName,self.appName,self.processID,id(self))

	def _get_appModuleName(self):
		return self.__class__.__module__.split('.')[-1]

	def _get_isAlive(self):
		return bool(winKernel.waitForSingleObject(self.processHandle,0))

	def __del__(self):
		winKernel.closeHandle(self.processHandle)
		NVDAHelper.localLib.destroyConnection(self.helperLocalBindingHandle)

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		"""Choose NVDAObject overlay classes for a given NVDAObject.
		This is called when an NVDAObject is being instantiated after L{NVDAObjects.NVDAObject.findOverlayClasses} has been called on the API-level class.
		This allows an AppModule to add or remove overlay classes.
		See L{NVDAObjects.NVDAObject.findOverlayClasses} for details about overlay classes.
		@param obj: The object being created.
		@type obj: L{NVDAObjects.NVDAObject}
		@param clsList: The list of classes, which will be modified by this method if appropriate.
		@type clsList: list of L{NVDAObjects.NVDAObject}
		"""

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
