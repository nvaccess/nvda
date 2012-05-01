#addonHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2012 Rui Batista <ruiandrebatista@gmail.com>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import gettext
import glob
import tempfile
import cPickle
import inspect
import itertools
import os.path
import pkgutil
import shutil
from cStringIO import StringIO
import zipfile

from configobj import ConfigObj, ConfigObjError
from validate import Validator

import config
import globalVars
import languageHandler
from logHandler import log


MANIFEST_FILENAME = "manifest.ini"
stateFilename="state.pickle"
BUNDLE_EXTENSION = "nvda-addon"
ADDON_PENDINGINSTALL_SUFFIX=".pendingInstall"

state={}

def loadState():
	global state
	statePath=os.path.join(globalVars.appArgs.configPath,"addons",stateFilename)
	try:
		state = cPickle.load(file(statePath, "r"))
	except:
		# Defaults.
		state = {
			"pendingRemovesSet":set(),
			"pendingInstallsSet":set(),
		}

def saveState():
	statePath=os.path.join(globalVars.appArgs.configPath,"addons",stateFilename)
	try:
		cPickle.dump(state, file(statePath, "wb"))
	except:
		log.debugWarning("Error saving state", exc_info=True)

def getRunningAddons():
	""" Returns currently loaded addons.
	"""
	return itertools.ifilter(lambda a : a.isLoaded, getAvailableAddons())

def completePendingRemoves():
	"""Removes any addons that could not be removed on the last run of NVDA"""
	user_addons = os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons"))
	pendingRemovesSet=state['pendingRemovesSet']
	for addonName in pendingRemovesSet:
		addonPath=os.path.join(user_addons,addonName)
		if os.path.isdir(addonPath):
			shutil.rmtree(addonPath,ignore_errors=True)
			if os.path.exists(addonPath):
				log.error("Could not remove addon at %s"%addonPath)
	pendingRemovesSet.clear()

def completePendingInstalls():
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

def initialize():
	""" Initializes the add-ons subsystem. """
	loadState()
	completePendingRemoves()
	completePendingInstalls()
	saveState()
	for addon in getAvailableAddons(refresh=True):
		if addon.path.endswith(ADDON_PENDINGINSTALL_SUFFIX): continue
		try:
			addon.load()
		except:
			log.exception("Error loading addon.")
			continue
		log.debug("Loadded addon from %s", addon.path) 

def terminate():
	""" Terminates the add-ons subsystem. """
	addons = getRunningAddons()
	for addon in addons:
		addon.unload()


def runHook(hookName, *args, **kwargs):
	""" Runs the specified hook on the loaded addons.
	
	Check the documentation for the specific hook to know what arguments to pass.
	@param hookName: the hook name
	@type hookName: string
	@param args: positional arguments to the hook
	@param kwargs, keyword arguments to the hook function.
	@return list of C[(addon, ret)} tupples with the values returned by the add-ons that implement the hook.
	"""
	rets = []
	for addon in getRunningAddons():
		try:
			hook = addon.getHookFunction(hookName)
			if calable(hook):
				ret = hook(*args, **kwargs)
				rets.append((addon, ret))
		except:
			log.exception("Error running hook %s on plugin %s", hookName, addon.name, exc_info=True)
	return rets


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
		addon_path = os.path.join(path, p)
		if os.path.isdir(addon_path) and addon_path not in ('.', '..'):
			log.debug("Loading add-on from %s", addon_path)
			try:
				a = Addon(addon_path)
				log.debug("Found add-on %s", a.manifest['name'])
				yield a
			except:
				log.error("Error loading Addon from path: %s", addon_path, exc_info=True)

_availableAddons = None
def getAvailableAddons(refresh=False):
	""" Gets all available addons on the system.
	@rtype generator of Addon instances.
	"""
	global _availableAddons
	if _availableAddons is None or refresh:
		_availableAddons = {}
		generators = [_getAvailableAddonsFromPath(path) for path in _getDefaultAddonPaths()]
		for addon in itertools.chain(*generators):
			_availableAddons[addon.path] = addon
	return _availableAddons.itervalues()

def installAddonBundle(bundle):
	"""Extracts an Addon bundle in to a unique subdirectory of the user addons directory, marking the addon as needing install completion on NVDA restart.""" 
	addonPath = os.path.join(globalVars.appArgs.configPath, "addons",bundle.manifest['name']+ADDON_PENDINGINSTALL_SUFFIX)
	bundle.extract(addonPath)
	state['pendingInstallsSet'].add(bundle.manifest['name'])
	saveState()

class AddonError(Exception):
	""" Represents an exception coming from the addon subsystem. """


class Addon(object):
	""" Represents an Add-on available on the file system."""
	def __init__(self, path):
		""" Constructs an L[Addon} from.
		@param path: the base directory for the addon data.
		@type path: string
		"""
		self.path = os.path.abspath(path)
		self._extendedPackages = set()
		self._isLoaded = False
		manifest_path = os.path.join(path, MANIFEST_FILENAME)
		with open(manifest_path) as f:
			translatedInput = None
			for translatedPath in _translatedManifestPaths():
				p = os.path.join(self.path, translatedPath)
				if os.path.exists(p):
					log.debug("Using manifest translation from %s", p)
					translatedInput = open(p, 'r')
					break
			self.manifest = AddonManifest(f, translatedInput)
		self._hooksModule = self.loadModule('hooks')

	@property
	def isPendingInstall(self):
		"""True if this addon has not yet been fully installed."""
		return self.path.endswith(ADDON_PENDINGINSTALL_SUFFIX)

	@property
	def isPendingRemove(self):
		"""True if this addon is marked for removal."""
		return self.name in state['pendingRemovesSet']

	def requestRemove(self):
		"""Markes this addon for removal on NVDA restart."""
		if self.isPendingInstall:
			state['pendingInstallsSet'].discard(self.name)
			shutil.rmtree(self.path,ignore_errors=True)
			if os.path.exists(self.path):
				log.error("Failed to remove pending install addon at %s"%self.path)
		else: #Normal removal
			state['pendingRemovesSet'].add(self.name)
		saveState()

	@property
	def name(self):
		return self.manifest['name']

	def addToPackagePath(self, package):
		""" Adds this L{Addon} extensions to the specific package path if those exist.
		@param package: the python module representing the package.
		@type package: python module.
		"""
		extension_path = os.path.join(self.path, package.__name__)
		if not os.path.isdir(extension_path):
			# This addon does not have extension points for this package
			return
		# Python 2.x doesn't properly handle unicode import paths, so convert them before adding.
		converted_path = self._getPathForInclusionInPackage(package)
		package.__path__.insert(0, converted_path)
		self._extendedPackages.add(package)
		log.debug("Addon %s added to %s package path", self.manifest['name'], package.__name__)

	@property
	def isLoaded(self):
		return self._isLoaded

	def load(self):
		""" Loads this L{Addon}, running the load hook if exists. """
		self.runHook('load')
		self._isLoaded = True

	def unload(self):
		""" Removes this add-on extensions from the running NVDA. 
		For most addons other measures should be taken: reloading of plugins, etc. """
		self.runHook('unload')
		log.debug("Deactivating addon.")
		for package in self._extendedPackages:
			extension_path = self._getPathForInclusionInPackage(package)
			package.__path__.remove(extension_path)
		self._extendedPackages = None
		self._isLoaded = False

	def _getPathForInclusionInPackage(self, package):
		extension_path = os.path.join(self.path, package.__name__)
		return extension_path.encode("mbcs")

	def loadModule(self, name):
		""" loads a python module from the addon directory
		@param name: the module name
		@type name: string
		@returns the python module with C[name}
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

	def getHookFunction(self, hookName):
		""" returns the hook function object for this L{Addon} if available.
		@param hookName the name of the hook.
		@type hookName: string
		@return a calable from the L{Addon} hooks module.
		@rtype calalbe.
		"""
		if not self._hooksModule:
			return None
		return getattr(self._hooksModule, hookName, None)

	def runHook(self, hookName, *args, **kwargs):
		""" Runs the specified hook on this addon, if implemented.
		If access to the hook calable is desired see L{getHookFunction}.
		
		@param hookName: the hook name
		@return the hooks return value, or none if it is not implemented.
		"""
		func = self.getHookFunction(hookName)
		if func:
			return func(*args, **kwargs)

	def removeContents(self):
		""" This method removes the contents of the addon from the system.
		Any calls to the majority of the addon methods will throw an error.
		This method will do its best to remove files, but on failier it will rename the directory and remove on next NVDA run.
		"""
		if self.isLoaded:
			raise RuntimeError("This addon is still active.")
		shutil.rmtree(self.path,ignore_errors=True)
		if os.path.exists(self.path):
			log.debugWarning("Unable to remove some files, removing on next run of NVDA",exc_info=True)
			basePath=os.path.dirname(self.path)
			tempName=tempfile.mktemp(suffix=".%s"%ADDON_REMOVED_EXTENSION,dir=basePath)
			os.rename(self.path,tempName)

def getCodeAddon(obj=None, frameDist=1):
	""" Returns the L{Addon} where C{obj} is defined. If obj is None the caller code frame is assumed to allow simple retrieval of "current calling addon".
	@param obj: python object or None for default behaviour.
	@param frameDist: howmany frames is the caller code. Only change this for functions in this module.
	@return: L{Addon} instance or None if no code does not belong to a add-on package.
	@rtype: C{Addon}
	 """
	global _availableAddons
	if obj is None:
		fileName = inspect.stack()[frameDist][1]
	else:
		fileName  = inspect.getfile(obj)
	dir= unicode(os.path.abspath(os.path.dirname(fileName)))
	# if fileName is not a subdir of one of the addon paths
	# It does not belong to an addon.
	for p in _getDefaultAddonPaths():
		if dir.startswith(p):
			break
	else:
		raise AddonError("Code does not belong to an addon package.")
	curdir = dir
	while curdir not in _getDefaultAddonPaths():
		if curdir in _availableAddons.keys():
			return _availableAddons[curdir]
	# Not found!
	raise AddonError("Code does not belong to an addon")

def initTranslation():
	addon = getCodeAddon(frameDist=2)
	translations = addon.getTranslationsInstance()
	# Point _ to the translation object in the globals namespace of the caller frame
	# FIXME: shall we retrieve the caller module object explicitly?
	try:
		callerFrame = inspect.currentframe().f_back
		callerFrame.f_globals['_'] = translations.ugettext
	finally:
		del callerFrame # Avoid reference problems with frames (per python docs)

def _translatedManifestPaths(lang=None):
	if lang is None:
		lang = languageHandler.getLanguage() # can't rely on default keyword arguments here.
	langs=[lang]
	if '_' in lang:
		langs.append(lang.split('_')[0])
		if lang!='en' and not lang.startswith('en_'):
			langs.append('en')
	return [r"locale\%s\%s" % (lang,  MANIFEST_FILENAME) for lang in langs]


class AddonBundle(object):
	""" Represents the contents of an NVDA addon in a for suitable for distribution.
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
			for translationPath in _translatedManifestPaths(): 
				try:
					translatedInput = z.open(translationPath, 'r')
					break
				except KeyError:
					pass
			self._manifest = AddonManifest(z.open(MANIFEST_FILENAME), translatedInput=translatedInput)

	def extract(self, addonPath):
		""" Extracts the bundle content to the specified path.
		The addon will be extracted to L{addonPath}
		@param addonPath: Path where to extract contents.
		@type addonPath: string
		"""
		with zipfile.ZipFile(self._path, 'r') as z:
			z.extractall(addonPath)

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
	with open(manifest_path) as f:
		manifest = AddonManifest(f)
	if manifest.errors is not None:
		_report_manifest_errors(manifest)
		raise AddonError("Manifest file as errors.")
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
# NVDA Ad-on Manifest configuration specification
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
# URL for more information about the add-on. New versions and such.
url= string(default=None)

"""))

	translatedConfigspec = ConfigObj(StringIO(
	"""
# NVDA localized Ad-on Manifest configuration specification
# This configspec contains the data that can be translated on a manifest.
# 
# short summary (label)  for the addon shown to users
summary = string()
# Long description with further information and instructions
description = string(default=none)
"""))

	def __init__(self, input, translatedInput=None):
		""" Constructs an L{AddonManifest} instance from manifest string data
		@param input: data to read the manifest informatinon
		@type input: a fie-like object.
		@param translatedInput: translated manifest input
		@type translatedInput: file-like object
		"""
		super(AddonManifest, self).__init__(input, configspec=self.configspec)
		self._errors = []
		val = Validator()
		result = self.validate(val, copy=True, preserve_errors=True)
		if result != True:
			self._errors = result
		self._translatedConfig = None
		if translatedInput is not None:
			self._translatedConfig = ConfigObj(translatedInput, configspec=self.translatedConfigspec)
			for k in ('summary','description'):
				val=self._translatedConfig.get(k)
				if val:
					self[k]=val

	@property
	def errors(self):
		return self._errors
