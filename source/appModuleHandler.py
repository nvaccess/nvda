#appModuleHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Manages appModules.
@var runningTable: a dictionary of the currently running appModules, using their application's main window handle as a key.
@type runningTable: dict
"""

import itertools
import array
import ctypes
import ctypes.wintypes
import os
import sys
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
import appModules
import watchdog

#Dictionary of processID:appModule paires used to hold the currently running modules
runningTable={}
#: The process ID of NVDA itself.
NVDAProcessID=None
_importers=None

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
	return appName

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
			raise RuntimeError("error fetching default appModule")
		runningTable[processID]=mod
	return mod

def update(processID,helperLocalBindingHandle=None,inprocRegistrationHandle=None):
	"""Removes any appModules from the cache whose process has died, and also tries to load a new appModule for the given process ID if need be.
	@param processID: the ID of the process.
	@type processID: int
	@param helperLocalBindingHandle: an optional RPC binding handle pointing to the RPC server for this process
	@param inprocRegistrationHandle: an optional rpc context handle representing successful registration with the rpc server for this process
	"""
	for deadMod in [mod for mod in runningTable.itervalues() if not mod.isAlive]:
		log.debug("application %s closed"%deadMod.appName)
		del runningTable[deadMod.processID]
		if deadMod in set(o.appModule for o in api.getFocusAncestors()+[api.getFocusObject()] if o and o.appModule):
			if hasattr(deadMod,'event_appLoseFocus'):
				deadMod.event_appLoseFocus()
		try:
			deadMod.terminate()
		except:
			log.exception("Error terminating app module %r" % deadMod)
	# This creates a new app module if necessary.
	mod=getAppModuleFromProcessID(processID)
	if helperLocalBindingHandle:
		mod.helperLocalBindingHandle=helperLocalBindingHandle
	if inprocRegistrationHandle:
		mod._inprocRegistrationHandle=inprocRegistrationHandle

def doesAppModuleExist(name):
	return any(importer.find_module("appModules.%s" % name) for importer in _importers)

def fetchAppModule(processID,appName):
	"""Returns an appModule found in the appModules directory, for the given application name.
	@param processID: process ID for it to be associated with
	@type processID: integer
	@param appName: the application name for which an appModule should be found.
	@type appName: unicode or str
	@returns: the appModule, or None if not found
	@rtype: AppModule
	"""  
	# First, check whether the module exists.
	# We need to do this separately because even though an ImportError is raised when a module can't be found, it might also be raised for other reasons.
	# Python 2.x can't properly handle unicode module names, so convert them.
	modName = appName.encode("mbcs")

	if doesAppModuleExist(modName):
		try:
			return __import__("appModules.%s" % modName, globals(), locals(), ("appModules",)).AppModule(processID, appName)
		except:
			log.error("error in appModule %r"%modName, exc_info=True)
			# We can't present a message which isn't unicode, so use appName, not modName.
			# Translators: This is presented when errors are found in an appModule (example output: error in appModule explorer).
			ui.message(_("Error in appModule %s")%appName)

	# Use the base AppModule.
	return AppModule(processID, appName)

def reloadAppModules():
	"""Reloads running appModules.
	especially, it clears the cache of running appModules and deletes them from sys.modules.
	Each appModule will be reloaded immediately as a reaction on a first event coming from the process.
	"""
	global appModules
	terminate()
	del appModules
	mods=[k for k,v in sys.modules.iteritems() if k.startswith("appModules") and v is not None]
	for mod in mods:
		del sys.modules[mod]
	import appModules
	initialize()

def initialize():
	"""Initializes the appModule subsystem. 
	"""
	global NVDAProcessID,_importers
	NVDAProcessID=os.getpid()
	config.addConfigDirsToPythonPackagePath(appModules)
	_importers=list(pkgutil.iter_importers("appModules.__init__"))

def terminate():
	for processID, app in runningTable.iteritems():
		try:
			app.terminate()
		except:
			log.exception("Error terminating app module %r" % app)
	runningTable.clear()

def handleAppSwitch(oldMods, newMods):
	newModsSet = set(newMods)
	processed = set()
	nextStage = []

	# Determine all apps that are losing focus and fire appropriate events.
	for mod in reversed(oldMods):
		if mod in processed:
			# This app has already been handled.
			continue
		processed.add(mod)
		if mod in newModsSet:
			# This app isn't losing focus.
			continue
		processed.add(mod)
		# This app is losing focus.
		nextStage.append(mod)
		if not mod.sleepMode and hasattr(mod,'event_appModule_loseFocus'):
			try:
				mod.event_appModule_loseFocus()
			except watchdog.CallCancelled:
				pass

	nvdaGuiLostFocus = nextStage and nextStage[-1].appName == "nvda"
	if not nvdaGuiLostFocus and (not oldMods or oldMods[-1].appName != "nvda") and newMods[-1].appName == "nvda":
		# NVDA's GUI just got focus.
		import gui
		if gui.shouldConfigProfileTriggersBeSuspended():
			config.conf.suspendProfileTriggers()

	with config.conf.atomicProfileSwitch():
		# Exit triggers for apps that lost focus.
		for mod in nextStage:
			mod._configProfileTrigger.exit()
			mod._configProfileTrigger = None

		nextStage = []
		# Determine all apps that are gaining focus and enter triggers.
		for mod in newMods:
			if mod in processed:
				# This app isn't gaining focus or it has already been handled.
				continue
			processed.add(mod)
			# This app is gaining focus.
			nextStage.append(mod)
			trigger = mod._configProfileTrigger = AppProfileTrigger(mod.appName)
			trigger.enter()

	if nvdaGuiLostFocus:
		import gui
		if not gui.shouldConfigProfileTriggersBeSuspended():
			config.conf.resumeProfileTriggers()

	# Fire appropriate events for apps gaining focus.
	for mod in nextStage:
		if not mod.sleepMode and hasattr(mod,'event_appModule_gainFocus'):
			mod.event_appModule_gainFocus()

#base class for appModules
class AppModule(baseObject.ScriptableObject):
	"""Base app module.
	App modules provide specific support for a single application.
	Each app module should be a Python module in the appModules package named according to the executable it supports;
	e.g. explorer.py for the explorer.exe application.
	It should containa  C{AppModule} class which inherits from this base class.
	App modules can implement and bind gestures to scripts.
	These bindings will only take effect while an object in the associated application has focus.
	See L{ScriptableObject} for details.
	App modules can also receive NVDAObject events for objects within the associated application.
	This is done by implementing methods called C{event_eventName},
	where C{eventName} is the name of the event; e.g. C{event_gainFocus}.
	These event methods take two arguments: the NVDAObject on which the event was fired
	and a callable taking no arguments which calls the next event handler.
	"""

	#: Whether NVDA should sleep while in this application (e.g. the application is self-voicing).
	#: If C{True}, all  events and script requests inside this application are silently dropped.
	#: @type: bool
	sleepMode=False

	def __init__(self,processID,appName=None):
		super(AppModule,self).__init__()
		#: The ID of the process this appModule is for.
		#: @type: int
		self.processID=processID
		if appName is None:
			appName=getAppNameFromProcessID(processID)
		#: The application name.
		#: @type: str
		self.appName=appName
		self.processHandle=winKernel.openProcess(winKernel.SYNCHRONIZE|winKernel.PROCESS_QUERY_INFORMATION|winKernel.PROCESS_VM_READ,False,processID)
		self.helperLocalBindingHandle=None
		self._inprocRegistrationHandle=None

	def _setProductInfo(self):
		"""Set productName and productVersion attributes.
		"""
		# If the processHandle is greater than 0, we get application name and version by reading it in its main executable file
		if self.processHandle >0:
			# We define where to find the function GetModuleFileNameW
			try:
				GetModuleFileName = ctypes.windll.kernel32.GetModuleFileNameExW
			except AttributeError:
				GetModuleFileName = ctypes.windll.psapi.GetModuleFileNameExW
			GetModuleFileName.restype = ctypes.wintypes.DWORD
			# Create the buffer to get the executable name
			exeFileName = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
			if GetModuleFileName(self.processHandle, 0, exeFileName, ctypes.wintypes.MAX_PATH) > 0:
				fileName = exeFileName.value
				# Get size needed for buffer (0 if no info)
				size = ctypes.windll.version.GetFileVersionInfoSizeW(fileName, None)
				if size:
					# Create buffer
					res = ctypes.create_string_buffer(size)
					# Load file informations into buffer res
					ctypes.windll.version.GetFileVersionInfoW(fileName, None, size, res)
					r = ctypes.c_uint()
					l = ctypes.c_uint()
					l = ctypes.c_uint()
					# Look for codepages
					ctypes.windll.version.VerQueryValueW(res, u'\\VarFileInfo\\Translation',
						ctypes.byref(r), ctypes.byref(l))
					if l.value:
						# Take the first codepage (what else ?)
						codepages = array.array('H', ctypes.string_at(r.value, l.value))
						codepage = tuple(codepages[:2].tolist())
						# Extract product name and put it to self.productName
						ctypes.windll.version.VerQueryValueW(res, (u'\\StringFileInfo\\%04x%04x\\'
							+ u"ProductName") % codepage, ctypes.byref(r), ctypes.byref(l))
						self.productName = ctypes.wstring_at(r.value, l.value-1)
						# Extract product version and put it to self.productVersion
						ctypes.windll.version.VerQueryValueW(res, (u'\\StringFileInfo\\%04x%04x\\'
							+ u"ProductVersion") % codepage, ctypes.byref(r), ctypes.byref(l))
						self.productVersion = ctypes.wstring_at(r.value, l.value-1)
					else:
						raise Exception("No codepage.")
				else:
					raise Exception("No version informations.")
			else:
				raise ctypes.WinError()
		else:
			raise Exception("processHandle is 0")

	def _get_productName(self):
		self._setProductInfo()
		return self.productName

	def _get_productVersion(self):
		self._setProductInfo()
		return self.productVersion

	def __repr__(self):
		return "<%r (appName %r, process ID %s) at address %x>"%(self.appModuleName,self.appName,self.processID,id(self))

	def _get_appModuleName(self):
		return self.__class__.__module__.split('.')[-1]

	def _get_isAlive(self):
		return bool(winKernel.waitForSingleObject(self.processHandle,0))

	def terminate(self):
		"""Terminate this app module.
		This is called to perform any clean up when this app module is being destroyed.
		Subclasses should call the superclass method first.
		"""
		winKernel.closeHandle(self.processHandle)
		if self._inprocRegistrationHandle:
			ctypes.windll.rpcrt4.RpcSsDestroyClientContext(ctypes.byref(self._inprocRegistrationHandle))
		if self.helperLocalBindingHandle:
			ctypes.windll.rpcrt4.RpcBindingFree(ctypes.byref(self.helperLocalBindingHandle))

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

	def _get_is64BitProcess(self):
		"""Whether the underlying process is a 64 bit process.
		@rtype: bool
		"""
		if os.environ.get("PROCESSOR_ARCHITEW6432") != "AMD64":
			# This is 32 bit Windows.
			self.is64BitProcess = False
			return False
		res = ctypes.wintypes.BOOL()
		if ctypes.windll.kernel32.IsWow64Process(self.processHandle, ctypes.byref(res)) == 0:
			self.is64BitProcess = False
			return False
		self.is64BitProcess = not res
		return self.is64BitProcess

class AppProfileTrigger(config.ProfileTrigger):
	"""A configuration profile trigger for when a particular application has focus.
	"""

	def __init__(self, appName):
		self.spec = "app:%s" % appName
