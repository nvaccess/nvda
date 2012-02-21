#addonHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2012 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import glob
import itertools
import os
import os.path
import pkgutil
from StringIO import StringIO
import zipfile

from configobj import ConfigObj, ConfigObjError
from validate import Validator

import config
import globalVars
from logHandler import log


MANIFEST_FILENAME = "manifest.ini"
BUNDLE_EXTENSION = "nvdaadon"

#: Currently loaded add-ons.
#: @type runningAddons: string
runningAddons = []

def initialize():
	""" Initializes the addons subsystem. """
	global runningAddons
	availableAddons = getAvailableAddons()
	for addon in availableAddons:
		try:
			addon.activate()
		except:
			log.exception("Error activating addon.")
			continue
		runningAddons.append(addon)

def terminate():
	""" Terminates the add-ons subsystem. """
	global runningAddons
	addons = list(runningAddons)
	for addon in runningAddons:
		addon.deactivate()
	runningAddons = []


def runHook(hookName, *args, **kwargs):
	""" Runs the specified hook on all active add.ons.
	@param hookName: the hook name
	@type hookName: string
	"""
	rets = []
	for addon in runningAddons:
		try:
			ret = addon.runHook(hookName, *args, **kwargs)
			if ret is not None:
				rets.append((ret, addon))
		except:
			log.exception("Error running hook %s on plugin %s", hookName, addon.name)
	return rets


def _getDefaultAddonPaths():
	""" Returns paths where addons can be found.
	Paths are constructed from source dir location and user configuration directory.
	@rtype list(string)
	"""
	addon_paths = []
	source_addons = os.path.join(os.getcwd(), "addons")
	if os.path.isdir(source_addons):
		dirs.append(source_addons)
	user_addons = os.path.join(globalVars.appArgs.configPath, "addons")
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
				log.exception("Error loading Addon from path: %s", p)

def getAvailableAddons():
	""" Gets all available addons on the system.
	@rtype generator of Addon instances.
	"""
	generators = [_getAvailableAddonsFromPath(path) for path in _getDefaultAddonPaths()]
	return itertools.chain(*generators)


def installAddonBundle(bundle):
	userAddonsPath = os.path.join(globalVars.appArgs.configPath, "addons")
	bundle.extract(userAddonsPath)


class AddonError(Exception):
	""" Represents an exception coming from the addon subsystem. """
	pass


class Addon(object):
	""" Represents an Addon available on the file system."""
	def __init__(self, path):
		""" Constructs an C[Addon} from.
		@param path: the base directory for the addon data.
		@type path: string
		"""
		self.path = path
		self._extendedPackages = set()
		manifest_path = os.path.join(path, MANIFEST_FILENAME)
		with open(manifest_path) as f:
			self.manifest = AddonManifest(f)
		self._hooksModule = self.loadModule('hooks')

	@property
	def name(self):
		return self.manifest['name']

	def addToPackagePath(self, package):
		""" Adds this C{Addon} extensions to the specific package path if those exist.
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

	def activate(self):
		""" Activates this addon, running the activate hook if exists. """
		self.runHook('activate')

	def deactivate(self):
		""" Removes this add-on extensions from the system. """
		self.runHook('deactivate')
		log.debug("Deactivating plugin.")
		for package in self._extendedPackages:
			extension_path = self._getPathForInclusionInPackage(package)
			package.__path__.remove(extension_path)

	def _getPathForInclusionInPackage(self, package):
		extension_path = os.path.join(self.path, package.__name__)
		return extension_path.encode("mbcs")

	def loadModule(self, name):
		""" loads a python mudle from the addon directory
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
		fullname = "%s.%s" % (self.name, name)
		try:
			return loader.load_module(fullname)
		except ImportError:
			# in this case return None, any other error throw to be handled elsewhere
			return None

	def runHook(self, hookName, *args, **kwargs):
		""" Runs the specified hook on this addon, if implemented."""
		if not self._hooksModule:
			return None
		func = getattr(self._hooksModule, hookName, None)
		if func:
			log.debug("Running hook %s of addon %s", hookName, self.name)
			return func(*args, **kwargs)

class AddonBundle(object):
	""" Represents the contents of an NVDA addon in a for suitable for distribution.
	The bundle is compressed using the zip file format. Manifest information
	is available without the need for extraction."""
	def __init__(self, bundlePath):
		""" Constructs a C{AddonBundle} from a filename.
		@param bundlePath: The path for the bundle file.
		"""
		self._path = bundlePath
		# Read manifest:
		with zipfile.ZipFile(self._path, 'r') as z:
			self._manifest = AddonManifest(z.open(MANIFEST_FILENAME))

	def extract(self, addonsPath, override=False):
		""" Extracts the bundle content to the specified path.
		A directory with the addon's name will be created under C{addons_path}.
		@param addons_path: Path where to extract contents.
		@type addonsPath: string
		@param override: specifies if the contents of the addon-directory are or not overriden
		@type override: boolean
		"""
		name = self._manifest['name']
		path = os.path.join(addonsPath, name)
		if not override and os.path.isdir(path):
			raise AddonError, "Addon already installed."
		with zipfile.ZipFile(self._path, 'r') as z:
			z.extractall(path)

	@property
	def manifest(self):
		""" Gets the manifest for the represented Addon.
		@rtype AddonManifest
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
		raise AddonError, "Can't find %s manifest file." % manifest_path
	with open(manifest_path) as f:
		manifest = AddonManifest(f)
	if manifest.errors is not None:
		_report_manifest_errors(manifest)
		raise AddonError, "Manifest file as errors."
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
# Add-on name
name = string()
# Quick description of the add-on to show to users.
description = string()
# Long description with further information and instructions
long_description = string(default=None)
# Name of the author or entity that created the add-on
author = string()
# Version of the add-on. Should preferably in some standard format such as x.y.z
version = string()
# URL for more information about the add-on. New versions and such.
url= string(default=None)
# Categories where this add-on belongs to.
categories = list(default=list())

# Compatibility with NVDA releases
# Only considering stable versions.
[compatibility]
# Minimum version compatible with this add-on.
minVersion = string(default=None)
# Maximum compatible version.
maxVersion = string(default=None)
"""))

	def __init__(self, input):
		""" Constructs an C{AddonManfiest} instance from manifest string data
		@param input: data to read the manifest informatinon
		@type input: a fie-like object.
		"""
		
		super(AddonManifest, self).__init__(input, configspec=self.configspec)
		self._errors = []
		val = Validator()
		self._errors = None
		result = self.validate(val, copy=True, preserve_errors=True)
		if result != True:
			self._errors = result

	@property
	def errors(self):
		return self._errors
