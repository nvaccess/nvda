# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2019 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Patrick Zajda, Joseph Lee,
# Babbage B.V., Mozilla Corporation
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Manages appModules.
@var runningTable: a dictionary of the currently running appModules, using their application's main window handle as a key.
@type runningTable: dict
"""

import itertools
import ctypes
import ctypes.wintypes
import os
import sys
import winVersion
import pkgutil
import importlib
import threading
import tempfile
import comtypes.client
import baseObject
import globalVars
from logHandler import log
import NVDAHelper
import winUser
import winKernel
import config
import NVDAObjects #Catches errors before loading default appModule
import api
import appModules
import watchdog
import extensionPoints
from fileUtils import getFileVersionInfo

#Dictionary of processID:appModule paires used to hold the currently running modules
runningTable={}
#: The process ID of NVDA itself.
NVDAProcessID=None
_importers=None
_getAppModuleLock=threading.RLock()
#: Notifies when another application is taking foreground.
#: This allows components to react upon application switches.
#: For example, braille triggers bluetooth polling for braille displaysf necessary.
#: Handlers are called with no arguments.
post_appSwitch = extensionPoints.Action()


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
	@rtype: str
	"""
	if processID==NVDAProcessID:
		return "nvda.exe" if includeExt else "nvda"
	FSnapshotHandle = winKernel.kernel32.CreateToolhelp32Snapshot (2,0)
	FProcessEntry32 = processEntry32W()
	FProcessEntry32.dwSize = ctypes.sizeof(processEntry32W)
	ContinueLoop = winKernel.kernel32.Process32FirstW(FSnapshotHandle, ctypes.byref(FProcessEntry32))
	appName = str()
	while ContinueLoop:
		if FProcessEntry32.th32ProcessID == processID:
			appName = FProcessEntry32.szExeFile
			break
		ContinueLoop = winKernel.kernel32.Process32NextW(FSnapshotHandle, ctypes.byref(FProcessEntry32))
	winKernel.kernel32.CloseHandle(FSnapshotHandle)
	if not includeExt:
		appName=os.path.splitext(appName)[0].lower()
	if not appName:
		return appName

	# This might be an executable which hosts multiple apps.
	# Try querying the app module for the name of the app being hosted.
	try:
		mod = importlib.import_module("appModules.%s" % appName, package="appModules")
		return mod.getAppNameFromHost(processID)
	except (ImportError, AttributeError, LookupError):
		pass
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
	with _getAppModuleLock:
		mod=runningTable.get(processID)
		if not mod:
			# #5323: Certain executables contain dots as part of their file names.
			appName=getAppNameFromProcessID(processID).replace(".","_")
			mod=fetchAppModule(processID,appName)
			if not mod:
				raise RuntimeError("error fetching default appModule")
			runningTable[processID]=mod
	return mod

def update(processID,helperLocalBindingHandle=None,inprocRegistrationHandle=None):
	"""Tries to load a new appModule for the given process ID if need be.
	@param processID: the ID of the process.
	@type processID: int
	@param helperLocalBindingHandle: an optional RPC binding handle pointing to the RPC server for this process
	@param inprocRegistrationHandle: an optional rpc context handle representing successful registration with the rpc server for this process
	"""
	# This creates a new app module if necessary.
	mod=getAppModuleFromProcessID(processID)
	if helperLocalBindingHandle:
		mod.helperLocalBindingHandle=helperLocalBindingHandle
	if inprocRegistrationHandle:
		mod._inprocRegistrationHandle=inprocRegistrationHandle

def cleanup():
	"""Removes any appModules from the cache whose process has died.
	"""
	for deadMod in [mod for mod in runningTable.values() if not mod.isAlive]:
		log.debug("application %s closed"%deadMod.appName)
		del runningTable[deadMod.processID]
		if deadMod in set(o.appModule for o in api.getFocusAncestors()+[api.getFocusObject()] if o and o.appModule):
			if hasattr(deadMod,'event_appLoseFocus'):
				deadMod.event_appLoseFocus()
		import eventHandler
		eventHandler.handleAppTerminate(deadMod)
		try:
			deadMod.terminate()
		except:
			log.exception("Error terminating app module %r" % deadMod)

def doesAppModuleExist(name):
	return any(importer.find_module("appModules.%s" % name) for importer in _importers)

def fetchAppModule(processID,appName):
	"""Returns an appModule found in the appModules directory, for the given application name.
	@param processID: process ID for it to be associated with
	@type processID: integer
	@param appName: the application name for which an appModule should be found.
	@type appName: str
	@returns: the appModule, or None if not found
	@rtype: AppModule
	"""  
	# First, check whether the module exists.
	# We need to do this separately because even though an ImportError is raised when a module can't be found, it might also be raised for other reasons.
	modName = appName

	if doesAppModuleExist(modName):
		try:
			return importlib.import_module("appModules.%s" % modName, package="appModules").AppModule(processID, appName)
		except:
			log.exception(f"error in appModule {modName!r}")
			import ui
			import speech.priorities
			ui.message(
				# Translators: This is presented when errors are found in an appModule
				# (example output: error in appModule explorer).
				_("Error in appModule %s") % modName,
				speechPriority=speech.priorities.Spri.NOW
			)

	# Use the base AppModule.
	return AppModule(processID, appName)

def reloadAppModules():
	"""Reloads running appModules.
	especially, it clears the cache of running appModules and deletes them from sys.modules.
	Each appModule will then be reloaded immediately.
	"""
	global appModules
	state = []
	for mod in runningTable.values():
		state.append({key: getattr(mod, key) for key in ("processID",
			# #2892: We must save nvdaHelperRemote handles, as we can't reinitialize without a foreground/focus event.
			# Also, if there is an active context handle such as a loaded buffer,
			# nvdaHelperRemote can't reinit until that handle dies.
			"helperLocalBindingHandle", "_inprocRegistrationHandle",
			# #5380: We must save config profile triggers so they can be cleaned up correctly.
			# Otherwise, they'll remain active forever.
			"_configProfileTrigger",
		) if hasattr(mod, key)})
		# #2892: Don't disconnect from nvdaHelperRemote during termination.
		mod._helperPreventDisconnect = True
	terminate()
	del appModules
	mods=[k for k,v in sys.modules.items() if k.startswith("appModules") and v is not None]
	for mod in mods:
		del sys.modules[mod]
	import appModules
	initialize()
	for entry in state:
		pid = entry.pop("processID")
		mod = getAppModuleFromProcessID(pid)
		mod.__dict__.update(entry)
	# The appModule property for existing NVDAObjects will now be None, since their AppModule died.
	# Force focus, navigator, etc. objects to re-fetch,
	# since NVDA depends on the appModule property for these.
	for obj in itertools.chain((api.getFocusObject(), api.getNavigatorObject()), api.getFocusAncestors()):
		try:
			del obj._appModuleRef
		except AttributeError:
			continue
		# Fetch and cache right away; the process could die any time.
		obj.appModule

def initialize():
	"""Initializes the appModule subsystem. 
	"""
	global NVDAProcessID,_importers
	NVDAProcessID=os.getpid()
	config.addConfigDirsToPythonPackagePath(appModules)
	_importers=list(pkgutil.iter_importers("appModules.__init__"))

def terminate():
	for processID, app in runningTable.items():
		try:
			app.terminate()
		except:
			log.exception("Error terminating app module %r" % app)
	runningTable.clear()

def handleAppSwitch(oldMods, newMods):
	newModsSet = set(newMods)
	processed = set()
	nextStage = []

	if not oldMods or oldMods[-1].appName != newMods[-1].appName:
		post_appSwitch.notify()

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

	Some executables host many different applications; e.g. javaw.exe.
	In this case, it is desirable that a specific app module be loaded for each
	actual application, rather than the one for the hosting executable.
	To support this, the module for the hosting executable
	(not the C{AppModule} class within it) can implement the function
	C{getAppNameFromHost(processId)}, where C{processId} is the id of the host process.
	It should return a unicode string specifying the name that should be used.
	Alternatively, it can raise C{LookupError} if a name couldn't be determined.
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
		self.processHandle=winKernel.openProcess(winKernel.SYNCHRONIZE|winKernel.PROCESS_QUERY_INFORMATION,False,processID)
		self.helperLocalBindingHandle=None
		self._inprocRegistrationHandle=None

	def _getExecutableFileInfo(self):
		# Used for obtaining file name and version for the executable.
		# This is needed in case immersive app package returns an error,
		# dealing with a native app, or a converted desktop app.
		# Create the buffer to get the executable name
		exeFileName = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
		length = ctypes.wintypes.DWORD(ctypes.wintypes.MAX_PATH)
		if not ctypes.windll.Kernel32.QueryFullProcessImageNameW(
			self.processHandle, 0, exeFileName, ctypes.byref(length)
		):
			raise ctypes.WinError()
		fileName = exeFileName.value
		fileinfo = getFileVersionInfo(fileName, "ProductName", "ProductVersion")
		return (fileinfo["ProductName"], fileinfo["ProductVersion"])

	def _setProductInfo(self):
		"""Set productName and productVersion attributes.
		There are at least two ways of obtaining product info for an app:
		* Package info for hosted apps
		* File version info for other apps and for some hosted apps
		"""
		# Sometimes (I.E. when NVDA starts) handle is 0, so stop if it is the case
		if not self.processHandle:
			raise RuntimeError("processHandle is 0")
		# No need to worry about immersive (hosted) apps and friends until Windows 8.
		# Python 3.7 introduces platform_version to sys.getwindowsversion tuple,
		# which returns major, minor, build.
		if winVersion.winVersion.platform_version >= (6, 2, 9200):
			# Some apps such as File Explorer says it is an immersive process but error 15700 is shown.
			# Therefore resort to file version info behavior because it is not a hosted app.
			# Others such as Store version of Office are not truly hosted apps,
			# yet returns an internal version anyway.
			# For immersive apps, default implementation is generic - returns Windows version information.
			# Thus probe package full name and parse the serialized representation of package info structure.
			length = ctypes.c_uint()
			buf = ctypes.windll.kernel32.GetPackageFullName(self.processHandle, ctypes.byref(length), None)
			packageFullName = ctypes.create_unicode_buffer(buf)
			if ctypes.windll.kernel32.GetPackageFullName(
				self.processHandle, ctypes.byref(length), packageFullName
			) == 0:
				# Product name is of the form publisher.name for a hosted app.
				productInfo = packageFullName.value.split("_")
			else:
				# File Explorer and friends which are really native aps.
				productInfo = self._getExecutableFileInfo()
		else:
			# Not only native apps, but also converted desktop aps such as Office.
			productInfo = self._getExecutableFileInfo()
		self.productName = productInfo[0]
		self.productVersion = productInfo[1]

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
		if getattr(self, "_helperPreventDisconnect", False):
			return
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
	# optimisation: Make it easy to detect that this hasn't been overridden.
	chooseNVDAObjectOverlayClasses._isBase = True

	def _get_is64BitProcess(self):
		"""Whether the underlying process is a 64 bit process.
		@rtype: bool
		"""
		if os.environ.get("PROCESSOR_ARCHITEW6432") not in ("AMD64","ARM64"):
			# This is 32 bit Windows.
			self.is64BitProcess = False
			return False
		try:
			# We need IsWow64Process2 to detect WOW64 on ARM64.
			processMachine = ctypes.wintypes.USHORT()
			if ctypes.windll.kernel32.IsWow64Process2(self.processHandle,
					ctypes.byref(processMachine), None) == 0:
				self.is64BitProcess = False
				return False
			# IMAGE_FILE_MACHINE_UNKNOWN if not a WOW64 process.
			self.is64BitProcess = processMachine.value == winKernel.IMAGE_FILE_MACHINE_UNKNOWN
		except AttributeError:
			# IsWow64Process2 is only supported on Windows 10 version 1511 and later.
			# Fall back to IsWow64Process.
			res = ctypes.wintypes.BOOL()
			if ctypes.windll.kernel32.IsWow64Process(self.processHandle, ctypes.byref(res)) == 0:
				self.is64BitProcess = False
				return False
			self.is64BitProcess = not res
		return self.is64BitProcess

	def isGoodUIAWindow(self,hwnd):
		"""
		returns C{True} if the UIA implementation of the given window must be used, regardless whether native or not.
		This function is the counterpart of and takes precedence over L{isBadUIAWindow}.
		If both functions return C{False}, the decision of whether to use UIA for the window is left to core.
		Warning: this may be called outside of NVDA's main thread, therefore do not try accessing NVDAObjects and such, rather just check window  class names.
		"""
		return False

	def isBadUIAWindow(self,hwnd):
		"""
		returns C{True} if the UIA implementation of the given window must be ignored due to it being broken in some way.
		This function is the counterpart of L{isGoodUIAWindow}.
		When both functions return C{True}, L{isGoodUIAWindow} takes precedence.
		If both functions return C{False}, the decision of whether to use UIA for the window is left to core.
		Warning: this may be called outside of NVDA's main thread, therefore do not try accessing NVDAObjects and such, rather just check window  class names.
		"""
		return False

	def shouldProcessUIAPropertyChangedEvent(self, sender, propertyId):
		"""
		Determines whether NVDA should process a UIA property changed event.
		Returning False will cause the event to be dropped completely. This can be
		used to work around UIA implementations which flood events and cause poor
		performance.
		Returning True means that the event will be processed, but it might still
		be rejected later; e.g. because it isn't native UIA, because
		shouldAcceptEvent returns False, etc.
		"""
		return True

	def dumpOnCrash(self):
		"""Request that this process writes a minidump when it crashes for debugging.
		This should only be called if instructed by a developer.
		"""
		path = os.path.join(tempfile.gettempdir(),
			"nvda_crash_%s_%d.dmp" % (self.appName, self.processID))
		NVDAHelper.localLib.nvdaInProcUtils_dumpOnCrash(
			self.helperLocalBindingHandle, path)
		print("Dump path: %s" % path)

	def _get_statusBar(self):
		"""Retrieve the status bar object of the application.
		If C{NotImplementedError} is raised, L{api.getStatusBar} will resort to
		perform a lookup by position.
		If C{None} is returned, L{GlobalCommands.script_reportStatusLine} will
		in turn resort to reading the bottom line of text written to the
		display.
		@rtype: NVDAObject
		"""
		raise NotImplementedError()

	def _get_statusBarTextInfo(self):
		"""Retrieve a L{TextInfo} positioned at the status bar of the application.
		This is used by L{GlobalCommands.script_reportStatusLine} in cases where
		L{api.getStatusBar} could not locate a proper L{NVDAObject} for the
		status bar.
		For this method to get called, L{_get_statusBar} must return C{None}.
		@rtype: TextInfo
		"""
		raise NotImplementedError()

class AppProfileTrigger(config.ProfileTrigger):
	"""A configuration profile trigger for when a particular application has focus.
	"""

	def __init__(self, appName):
		self.spec = "app:%s" % appName

def getWmiProcessInfo(processId):
	"""Retrieve the WMI Win32_Process class instance for a given process.
	For details about the available properties, see
	http://msdn.microsoft.com/en-us/library/aa394372%28v=vs.85%29.aspx
	@param processId: The id of the process in question.
	@type processId: int
	@return: The WMI Win32_Process class instance.
	@raise LookupError: If there was an error retrieving the instance.
	"""
	try:
		wmi = comtypes.client.CoGetObject(r"winmgmts:root\cimv2", dynamic=True)
		results = wmi.ExecQuery("select * from Win32_Process "
			"where ProcessId = %d" % processId)
		for result in results:
			return result
	except:
		raise LookupError("Couldn't get process information using WMI")
	raise LookupError("No such process")
