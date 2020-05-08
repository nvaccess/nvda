# -*- coding: UTF-8 -*-
#addonHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2012-2019 Rui Batista, NV Access Limited, Noelia Ruiz Martínez, Joseph Lee, Babbage B.V., Arnold Loubriat
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import sys
import os.path
import gettext
import tempfile
import inspect
import itertools
import collections
import pkgutil
import shutil
from io import StringIO
import pickle
from six import string_types
import globalVars
import zipfile
from configobj import ConfigObj
from configobj.validate import Validator

import config
import globalVars
import languageHandler
from logHandler import log
import winKernel
import addonAPIVersion
from . import addonVersionCheck
from .addonVersionCheck import isAddonCompatible

MANIFEST_FILENAME = "manifest.ini"
stateFilename="addonsState.pickle"
BUNDLE_EXTENSION = "nvda-addon"
BUNDLE_MIMETYPE = "application/x-nvda-addon"
NVDA_ADDON_PROG_ID = "NVDA.Addon.1"
ADDON_PENDINGINSTALL_SUFFIX=".pendingInstall"
DELETEDIR_SUFFIX=".delete"

state={}

# addons that are blocked from running because they are incompatible
_blockedAddons=set()

def loadState():
	global state
	statePath=os.path.join(globalVars.appArgs.configPath,stateFilename)
	try:
		# #9038: Python 3 requires binary format when working with pickles.
		with open(statePath, "rb") as f:
			state = pickle.load(f)
		if "disabledAddons" not in state:
			state["disabledAddons"] = set()
		if "pendingDisableSet" not in state:
			state["pendingDisableSet"] = set()
		if "pendingEnableSet" not in state:
			state["pendingEnableSet"] = set()
	except:
		# Defaults.
		state = {
			"pendingRemovesSet":set(),
			"pendingInstallsSet":set(),
			"disabledAddons":set(),
			"pendingEnableSet":set(),
			"pendingDisableSet":set(),
		}

def saveState():
	statePath=os.path.join(globalVars.appArgs.configPath,stateFilename)
	try:
		# #9038: Python 3 requires binary format when working with pickles.
		with open(statePath, "wb") as f:
			pickle.dump(state, f, protocol=0)
	except:
		log.debugWarning("Error saving state", exc_info=True)

def getRunningAddons():
	""" Returns currently loaded addons.
	"""
	return getAvailableAddons(filterFunc=lambda addon: addon.isRunning)

def getIncompatibleAddons(
		currentAPIVersion=addonAPIVersion.CURRENT,
		backCompatToAPIVersion=addonAPIVersion.BACK_COMPAT_TO):
	""" Returns a generator of the add-ons that are not compatible.
	"""
	return getAvailableAddons(
		filterFunc=lambda addon: (
			not addonVersionCheck.isAddonCompatible(
				addon,
				currentAPIVersion=currentAPIVersion,
				backwardsCompatToVersion=backCompatToAPIVersion
		)
	))

def completePendingAddonRemoves():
	"""Removes any addons that could not be removed on the last run of NVDA"""
	user_addons = os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons"))
	pendingRemovesSet=state['pendingRemovesSet']
	for addonName in list(pendingRemovesSet):
		addonPath=os.path.join(user_addons,addonName)
		if os.path.isdir(addonPath):
			addon=Addon(addonPath)
			try:
				addon.completeRemove()
			except RuntimeError:
				log.exception("Failed to remove %s add-on"%addonName)
				continue
		pendingRemovesSet.discard(addonName)

def completePendingAddonInstalls():
	user_addons = os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons"))
	pendingInstallsSet=state['pendingInstallsSet']
	for addonName in pendingInstallsSet:
		newPath=os.path.join(user_addons,addonName)
		oldPath=newPath+ADDON_PENDINGINSTALL_SUFFIX
		try:
			os.rename(oldPath,newPath)
		except:
			log.error("Failed to complete addon installation for %s"%addonName,exc_info=True)
	pendingInstallsSet.clear()

def removeFailedDeletions():
	user_addons = os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons"))
	for p in os.listdir(user_addons):
		if p.endswith(DELETEDIR_SUFFIX):
			path=os.path.join(user_addons,p)
			shutil.rmtree(path,ignore_errors=True)
			if os.path.exists(path):
				log.error("Failed to delete path %s, try removing manually"%path)

_disabledAddons = set()
def disableAddonsIfAny():
	"""
	Disables add-ons if told to do so by the user from add-ons manager.
	This is usually executed before refreshing the list of available add-ons.
	"""
	global _disabledAddons
	# Pull in and enable add-ons that should be disabled and enabled, respectively.
	state["disabledAddons"] |= state["pendingDisableSet"]
	state["disabledAddons"] -= state["pendingEnableSet"]
	_disabledAddons = state["disabledAddons"]
	state["pendingDisableSet"].clear()
	state["pendingEnableSet"].clear()

def initialize():
	""" Initializes the add-ons subsystem. """
	if config.isAppX:
		log.info("Add-ons not supported when running as a Windows Store application")
		return
	loadState()
	removeFailedDeletions()
	completePendingAddonRemoves()
	completePendingAddonInstalls()
	# #3090: Are there add-ons that are supposed to not run for this session?
	disableAddonsIfAny()
	getAvailableAddons(refresh=True)
	saveState()


def terminate():
	""" Terminates the add-ons subsystem. """
	pass

def _getDefaultAddonPaths():
	""" Returns paths where addons can be found.
	For now, only <userConfig\addons is supported.
	@rtype: list(string)
	"""
	addon_paths = []
	user_addons = os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons"))
	if os.path.isdir(user_addons):
		addon_paths.append(user_addons)
	return addon_paths

def _getAvailableAddonsFromPath(path):
	""" Gets available add-ons from path.
	An addon is only considered available if the manifest file is loaded with no errors.
	@param path: path from where to find addon directories.
	@type path: string
	@rtype generator of Addon instances
	"""
	log.debug("Listing add-ons from %s", path)
	for p in os.listdir(path):
		if p.endswith(DELETEDIR_SUFFIX): continue
		addon_path = os.path.join(path, p)
		if os.path.isdir(addon_path) and addon_path not in ('.', '..'):
			if not len(os.listdir(addon_path)):
				log.error("Error loading Addon from path: %s", addon_path)
			else:
				log.debug("Loading add-on from %s", addon_path)
				try:
					a = Addon(addon_path)
					name = a.manifest['name']
					log.debug(
						"Found add-on {name} - {a.version}."
						" Requires API: {a.minimumNVDAVersion}."
						" Last-tested API: {a.lastTestedNVDAVersion}".format(
							name=name,
							a=a
						))
					if a.isDisabled:
						log.debug("Disabling add-on %s", name)
					if not isAddonCompatible(a):
						log.debugWarning("Add-on %s is considered incompatible", name)
						_blockedAddons.add(a.name)
					yield a
				except:
					log.error("Error loading Addon from path: %s", addon_path, exc_info=True)
				
_availableAddons = collections.OrderedDict()
def getAvailableAddons(refresh=False, filterFunc=None):
	""" Gets all available addons on the system.
	@param refresh: Whether or not to query the file system for available add-ons.
	@type refresh: bool
	@param filterFunc: A function that allows filtering of add-ons.
		It takes an L{Addon} as its only argument
		and returns a C{bool} indicating whether the add-on matches the provided filter.
	@type filterFunc: callable
	@rtype generator of Addon instances.
	"""
	if filterFunc and not callable(filterFunc):
		raise TypeError("The provided filterFunc is not callable")
	if refresh:
		_availableAddons.clear()
		generators = [_getAvailableAddonsFromPath(path) for path in _getDefaultAddonPaths()]
		for addon in itertools.chain(*generators):
			_availableAddons[addon.path] = addon
	return (addon for addon in _availableAddons.values() if not filterFunc or filterFunc(addon))

def installAddonBundle(bundle):
	"""Extracts an Addon bundle in to a unique subdirectory of the user addons directory, marking the addon as needing install completion on NVDA restart."""
	addonPath = os.path.join(globalVars.appArgs.configPath, "addons",bundle.manifest['name']+ADDON_PENDINGINSTALL_SUFFIX)
	bundle.extract(addonPath)
	addon=Addon(addonPath)
	# #2715: The add-on must be added to _availableAddons here so that
	# translations can be used in installTasks module.
	_availableAddons[addon.path]=addon
	try:
		addon.runInstallTask("onInstall")
	except:
		log.error("task 'onInstall' on addon '%s' failed"%addon.name,exc_info=True)
		del _availableAddons[addon.path]
		addon.completeRemove(runUninstallTask=False)
		raise AddonError("Installation failed")
	state['pendingInstallsSet'].add(bundle.manifest['name'])
	saveState()
	return addon

class AddonError(Exception):
	""" Represents an exception coming from the addon subsystem. """

class AddonBase(object):
	"""The base class for functionality that is available both for add-on bundles and add-ons on the file system.
	Subclasses should at least implement L{manifest}.
	"""

	@property
	def name(self):
		return self.manifest['name']

	@property
	def version(self):
		return self.manifest['version']

	@property
	def minimumNVDAVersion(self):
		return self.manifest.get('minimumNVDAVersion')

	@property
	def lastTestedNVDAVersion(self):
		return self.manifest.get('lastTestedNVDAVersion')

class Addon(AddonBase):
	""" Represents an Add-on available on the file system."""
	def __init__(self, path):
		""" Constructs an L{Addon} from.
		@param path: the base directory for the addon data.
		@type path: string
		"""
		self.path = os.path.abspath(path)
		self._extendedPackages = set()
		manifest_path = os.path.join(path, MANIFEST_FILENAME)
		with open(manifest_path, 'rb') as f:
			translatedInput = None
			for translatedPath in _translatedManifestPaths():
				p = os.path.join(self.path, translatedPath)
				if os.path.exists(p):
					log.debug("Using manifest translation from %s", p)
					translatedInput = open(p, 'rb')
					break
			self.manifest = AddonManifest(f, translatedInput)
			if self.manifest.errors is not None:
				_report_manifest_errors(self.manifest)
				raise AddonError("Manifest file has errors.")

	@property
	def isPendingInstall(self):
		"""True if this addon has not yet been fully installed."""
		return self.path.endswith(ADDON_PENDINGINSTALL_SUFFIX)

	@property
	def isPendingRemove(self):
		"""True if this addon is marked for removal."""
		return not self.isPendingInstall and self.name in state['pendingRemovesSet']

	def requestRemove(self):
		"""Markes this addon for removal on NVDA restart."""
		if self.isPendingInstall:
			self.completeRemove()
			state['pendingInstallsSet'].discard(self.name)
			#Force availableAddons to be updated
			getAvailableAddons(refresh=True)
		else:
			state['pendingRemovesSet'].add(self.name)
			# There's no point keeping a record of this add-on pending being disabled now.
			# However, if the addon is in _disabledAddons, then it needs to stay there so that
			# the status in addonsManager continues to say "disabled"
			state['pendingDisableSet'].discard(self.name)
		saveState()

	def completeRemove(self,runUninstallTask=True):
		if runUninstallTask:
			try:
				# #2715: The add-on must be added to _availableAddons here so that
				# translations can be used in installTasks module.
				_availableAddons[self.path] = self
				self.runInstallTask("onUninstall")
			except:
				log.error("task 'onUninstall' on addon '%s' failed"%self.name,exc_info=True)
			finally:
				del _availableAddons[self.path]
		tempPath=tempfile.mktemp(suffix=DELETEDIR_SUFFIX,dir=os.path.dirname(self.path))
		try:
			os.rename(self.path,tempPath)
		except (WindowsError,IOError):
			raise RuntimeError("Cannot rename add-on path for deletion")
		shutil.rmtree(tempPath,ignore_errors=True)
		if os.path.exists(tempPath):
			log.error("Error removing addon directory %s, deferring until next NVDA restart"%self.path)
		# clean up the addons state. If an addon with the same name is installed, it should not be automatically
		# disabled / blocked.
		log.debug("removing addon {} from _disabledAddons/_blockedAddons".format(self.name))
		_disabledAddons.discard(self.name)
		_blockedAddons.discard(self.name)
		saveState()

	def addToPackagePath(self, package):
		""" Adds this L{Addon} extensions to the specific package path if those exist.
		This allows the addon to "run" / be available because the package is able to search its path,
		looking for particular modules. This is used by the following:
		- `globalPlugins`
		- `appModules`
		- `synthDrivers`
		- `brailleDisplayDrivers`
		@param package: the python module representing the package.
		@type package: python module.
		"""
		# #3090: Ensure that we don't add disabled / blocked add-ons to package path.
		# By returning here the addon does not "run"/ become active / registered.
		if self.isDisabled or self.isBlocked:
			return

		extension_path = os.path.join(self.path, package.__name__)
		if not os.path.isdir(extension_path):
			# This addon does not have extension points for this package
			return
		converted_path = self._getPathForInclusionInPackage(package)
		package.__path__.insert(0, converted_path)
		self._extendedPackages.add(package)
		log.debug("Addon %s added to %s package path", self.manifest['name'], package.__name__)

	def enable(self, shouldEnable):
		"""Sets this add-on to be disabled or enabled when NVDA restarts."""
		if shouldEnable:
			if not isAddonCompatible(self):
				import addonAPIVersion
				raise AddonError(
					"Add-on is not compatible:"
					" minimum NVDA version {}, last tested version {},"
					" NVDA current {}, NVDA backwards compatible to {}".format(
						self.manifest['minimumNVDAVersion'],
						self.manifest['lastTestedNVDAVersion'],
						addonAPIVersion.CURRENT,
						addonAPIVersion.BACK_COMPAT_TO
					)
				)
			if self.name in state["pendingDisableSet"]:
				# Undoing a pending disable.
				state["pendingDisableSet"].discard(self.name)
			else:
				state["pendingEnableSet"].add(self.name)
		else:
			if self.name in state["pendingEnableSet"]:
				# Undoing a pending enable.
				state["pendingEnableSet"].discard(self.name)
			# No need to disable an addon that is already disabled.
			# This also prevents the status in the add-ons dialog from saying "disabled, pending disable"
			elif self.name not in state["disabledAddons"]:
				state["pendingDisableSet"].add(self.name)
		# Record enable/disable flags as a way of preparing for disaster such as sudden NVDA crash.
		saveState()

	@property
	def isRunning(self):
		return not (globalVars.appArgs.disableAddons or self.isPendingInstall or self.isDisabled or self.isBlocked)

	@property
	def isDisabled(self):
		return self.name in _disabledAddons

	@property
	def isBlocked(self):
		return self.name in _blockedAddons

	@property
	def isPendingEnable(self):
		return self.name in state["pendingEnableSet"]

	@property
	def isPendingDisable(self):
		return self.name in state["pendingDisableSet"]

	def _getPathForInclusionInPackage(self, package):
		extension_path = os.path.join(self.path, package.__name__)
		return extension_path

	def loadModule(self, name):
		""" loads a python module from the addon directory
		@param name: the module name
		@type name: string
		@returns the python module with C{name}
		@rtype python module
		"""
		log.debug("Importing module %s from plugin %s", name, self.name)
		importer = pkgutil.ImpImporter(self.path)
		loader = importer.find_module(name)
		if not loader:
			return None
		# Create a qualified full name to avoid modules with the same name on sys.modules.
		fullname = "addons.%s.%s" % (self.name, name)
		try:
			return loader.load_module(fullname)
		except ImportError:
			# in this case return None, any other error throw to be handled elsewhere
			return None

	def getTranslationsInstance(self, domain='nvda'):
		""" Gets the gettext translation instance for this addon.
		<addon-path<\locale will be used to find .mo files, if exists.
		If a translation file is not found the default fallback null translation is returned.
		@param domain: the tranlation domain to retrieve. The 'nvda' default should be used in most cases.
		@returns: the gettext translation class.
		"""
		localedir = os.path.join(self.path, "locale")
		return gettext.translation(domain, localedir=localedir, languages=[languageHandler.getLanguage()], fallback=True)

	def runInstallTask(self,taskName,*args,**kwargs):
		"""
		Executes the function having the given taskName with the given args and kwargs in the addon's installTasks module if it exists.
		"""
		if not hasattr(self,'_installTasksModule'):
			self._installTasksModule=self.loadModule('installTasks')
		if self._installTasksModule:
			func=getattr(self._installTasksModule,taskName,None)
			if func:
				func(*args,**kwargs)

	def getDocFilePath(self, fileName=None):
		"""Get the path to a documentation file for this add-on.
		The file should be located in C{doc\lang\file} inside the add-on,
		where C{lang} is the language code and C{file} is the requested file name.
		Failing that, the language without country is tried.
		English is tried as a last resort.
		An add-on can specify a default documentation file name
		via the docFileName parameter in its manifest.
		@param fileName: The requested file name or C{None} for the add-on's default.
		@type fileName: str
		@return: The path to the requested file or C{None} if it wasn't found.
		@rtype: str
		"""
		if not fileName:
			fileName = self.manifest["docFileName"]
			if not fileName:
				return None
		docRoot = os.path.join(self.path, "doc")
		lang = languageHandler.getLanguage()
		langs = [lang]
		if "_" in lang:
			lang = lang.split("_", 1)[0]
			langs.append(lang)
		if lang != "en":
			langs.append("en")
		for lang in langs:
			docFile = os.path.join(docRoot, lang, fileName)
			if os.path.isfile(docFile):
				return docFile
		return None

def getCodeAddon(obj=None, frameDist=1):
	""" Returns the L{Addon} where C{obj} is defined. If obj is None the caller code frame is assumed to allow simple retrieval of "current calling addon".
	@param obj: python object or None for default behaviour.
	@param frameDist: howmany frames is the caller code. Only change this for functions in this module.
	@return: L{Addon} instance or None if no code does not belong to a add-on package.
	@rtype: C{Addon}
	"""
	global _availableAddons
	if obj is None:
		obj = sys._getframe(frameDist)
	fileName  = inspect.getfile(obj)
	dir= os.path.abspath(os.path.dirname(fileName))
	# if fileName is not a subdir of one of the addon paths
	# It does not belong to an addon.
	for p in _getDefaultAddonPaths():
		if dir.startswith(p):
			break
	else:
		raise AddonError("Code does not belong to an addon package.")
	curdir = dir
	while curdir not in _getDefaultAddonPaths():
		if curdir in _availableAddons:
			return _availableAddons[curdir]
		curdir = os.path.abspath(os.path.join(curdir, ".."))
	# Not found!
	raise AddonError("Code does not belong to an addon")

def initTranslation():
	addon = getCodeAddon(frameDist=2)
	translations = addon.getTranslationsInstance()
	# Point _ to the translation object in the globals namespace of the caller frame
	# FIXME: shall we retrieve the caller module object explicitly?
	try:
		callerFrame = inspect.currentframe().f_back
		callerFrame.f_globals['_'] = translations.gettext
		# Install our pgettext function.
		callerFrame.f_globals['pgettext'] = languageHandler.makePgettext(translations)
	finally:
		del callerFrame # Avoid reference problems with frames (per python docs)

def _translatedManifestPaths(lang=None, forBundle=False):
	if lang is None:
		lang = languageHandler.getLanguage() # can't rely on default keyword arguments here.
	langs=[lang]
	if '_' in lang:
		langs.append(lang.split('_')[0])
		if lang!='en' and not lang.startswith('en_'):
			langs.append('en')
	sep = "/" if forBundle else os.path.sep
	return [sep.join(("locale", lang, MANIFEST_FILENAME)) for lang in langs]


class AddonBundle(AddonBase):
	""" Represents the contents of an NVDA addon suitable for distribution.
	The bundle is compressed using the zip file format. Manifest information
	is available without the need for extraction."""
	def __init__(self, bundlePath):
		""" Constructs an L{AddonBundle} from a filename.
		@param bundlePath: The path for the bundle file.
		"""
		self._path = bundlePath
		# Read manifest:
		translatedInput=None
		with zipfile.ZipFile(self._path, 'r') as z:
			for translationPath in _translatedManifestPaths(forBundle=True):
				try:
					# ZipFile.open opens every file in binary mode.
					# decoding is handled by configobj.
					translatedInput = z.open(translationPath, 'r')
					break
				except KeyError:
					pass
			self._manifest = AddonManifest(
				# ZipFile.open opens every file in binary mode.
				# decoding is handled by configobj.
				z.open(MANIFEST_FILENAME, 'r'),
				translatedInput=translatedInput
			)
			if self.manifest.errors is not None:
				_report_manifest_errors(self.manifest)
				raise AddonError("Manifest file has errors.")

	def extract(self, addonPath):
		""" Extracts the bundle content to the specified path.
		The addon will be extracted to L{addonPath}
		@param addonPath: Path where to extract contents.
		@type addonPath: string
		"""
		with zipfile.ZipFile(self._path, 'r') as z:
			for info in z.infolist():
				if isinstance(info.filename, bytes):
					# #2505: Handle non-Unicode file names.
					# Most archivers seem to use the local OEM code page, even though the spec says only cp437.
					# HACK: Overriding info.filename is a bit ugly, but it avoids a lot of code duplication.
					info.filename = info.filename.decode("cp%d" % winKernel.kernel32.GetOEMCP())
				z.extract(info, addonPath)

	@property
	def manifest(self):
		""" Gets the manifest for the represented Addon.
		@rtype: AddonManifest
		"""
		return self._manifest

	def __repr__(self):
		return "<AddonBundle at %s>" % self._path

def createAddonBundleFromPath(path, destDir=None):
	""" Creates a bundle from a directory that contains a a addon manifest file."""
	basedir = os.path.abspath(path)
	# If  caller did not provide a destination directory name
	# Put the bundle at the same level of the addon's top directory,
	# That is, basedir/..
	if destDir is None:
		destDir = os.path.dirname(basedir)
	manifest_path = os.path.join(basedir, MANIFEST_FILENAME)
	if not os.path.isfile(manifest_path):
		raise AddonError("Can't find %s manifest file." % manifest_path)
	with open(manifest_path, 'rb') as f:
		manifest = AddonManifest(f)
	if manifest.errors is not None:
		_report_manifest_errors(manifest)
		raise AddonError("Manifest file has errors.")
	bundleFilename = "%s-%s.%s" % (manifest['name'], manifest['version'], BUNDLE_EXTENSION)
	bundleDestination = os.path.join(destDir, bundleFilename)
	with zipfile.ZipFile(bundleDestination, 'w') as z:
		# FIXME: the include/exclude feature may or may not be useful. Also python files can be pre-compiled.
		for dir, dirnames, filenames in os.walk(basedir):
			relativePath = os.path.relpath(dir, basedir)
			for filename in filenames:
				pathInBundle = os.path.join(relativePath, filename)
				absPath = os.path.join(dir, filename)
				z.write(absPath, pathInBundle)
	return AddonBundle(bundleDestination)


def _report_manifest_errors(manifest):
	log.warning("Error loading manifest:\n%s", manifest.errors)

class AddonManifest(ConfigObj):
	""" Add-on manifest file. It contains metadata about an NVDA add-on package. """
	configspec = ConfigObj(StringIO(
	"""
# NVDA Add-on Manifest configuration specification
# Add-on unique name
name = string()

# short  summary (label) of the add-on to show to users.
summary = string()

# Long description with further information and instructions
description = string(default=None)

# Name of the author or entity that created the add-on
author = string()

# Version of the add-on. Should preferably in some standard format such as x.y.z
version = string()

# The minimum required NVDA version for this add-on to work correctly.
# Should be less than or equal to lastTestedNVDAVersion
minimumNVDAVersion = apiVersion(default="0.0.0")

# Must be greater than or equal to minimumNVDAVersion
lastTestedNVDAVersion = apiVersion(default="0.0.0")

# URL for more information about the add-on. New versions and such.
url= string(default=None)

# Name of default documentation file for the add-on.
docFileName = string(default=None)

# NOTE: apiVersion:
# Eg: 2019.1.0 or 0.0.0
# Must have 3 integers separated by dots.
# The first integer must be a Year (4 characters)
# "0.0.0" is also valid.
# The final integer can be left out, and in that case will default to 0. E.g. 2019.1

"""))

	def __init__(self, input, translatedInput=None):
		""" Constructs an L{AddonManifest} instance from manifest string data
		@param input: data to read the manifest informatinon
		@type input: a fie-like object.
		@param translatedInput: translated manifest input
		@type translatedInput: file-like object
		"""
		super(AddonManifest, self).__init__(input, configspec=self.configspec, encoding='utf-8', default_encoding='utf-8')
		self._errors = None
		val = Validator({"apiVersion":validate_apiVersionString})
		result = self.validate(val, copy=True, preserve_errors=True)
		if result != True:
			self._errors = result
		elif True != self._validateApiVersionRange():
			self._errors = "Constraint not met: minimumNVDAVersion ({}) <= lastTestedNVDAVersion ({})".format(
				self.get("minimumNVDAVersion"),
				self.get("lastTestedNVDAVersion")
			)
		self._translatedConfig = None
		if translatedInput is not None:
			self._translatedConfig = ConfigObj(translatedInput, encoding='utf-8', default_encoding='utf-8')
			for k in ('summary','description'):
				val=self._translatedConfig.get(k)
				if val:
					self[k]=val

	@property
	def errors(self):
		return self._errors

	def _validateApiVersionRange(self):
		lastTested = self.get("lastTestedNVDAVersion")
		minRequiredVersion = self.get("minimumNVDAVersion")
		return minRequiredVersion <= lastTested

def validate_apiVersionString(value):
	from configobj.validate import ValidateError
	if not value or value == "None":
		return (0, 0, 0)
	if not isinstance(value, string_types):
		raise ValidateError('Expected an apiVersion in the form of a string. EG "2019.1.0"')
	try:
		tuple = addonAPIVersion.getAPIVersionTupleFromString(value)
		return tuple
	except ValueError as e:
		raise ValidateError('"{}" is not a valid API Version string: {}'.format(value, e))
