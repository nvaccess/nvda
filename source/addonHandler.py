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

#: Currently loaded add-ons.
#: @type runningAddons: string
runningAddons = []

def initialize():
	""" Initializes the addons subsystem. """
	global runningAddons
	try:
		runningAddons = list(getAvailableAddons())
	except:
		log.exception("error initializing addons subsystem.")

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
	pass


class AddonError(Exception):
	""" Represents an exception comming from the addon subsystem. """
	pass


MANIFEST_FILENAME = "manifest.ini"

class Addon(object):
	""" Represents an Addon available on the file system."""
	def __init__(self, path):
		""" Constructs an C[Addon} from.
		@param path: the base directory for the addon data.
		@type path: string
		"""
		self.path = path
		manifest_path = os.path.join(path, MANIFEST_FILENAME)
		with open(manifest_path) as f:
			self.manifest = AddonManifest(f)

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
		converted_path = extension_path.encode("mbcs")
		package.__path__.insert(0, converted_path)
		log.debug("Addon %s added to %s package path", self.manifest['name'], package.__name__)


class AddonBundle(object):
	""" Represents the contents of an NVDA addon in a for suitable for distribution and.
	The bundle is compressed using the zip file format. Manifest information
	is available without the need for extraction."""
	def __init__(self, bundle_filename):
		""" Constructs a C{AddonBundle} from a filename.
		@param: bundle_filename the bundle's file path on the file system.
		"""
		self._filename = bundle_filename
		# Read manifest:
		with zipfile.ZipFile(bundle_filename, 'r') as z:
			self._manifest = AddonManifest(z.open(MANIFEST_FILENAME))

	def extract(addons_path, override=False):
		""" Extracts the bundle content to the specified path.
		A directory with the addon's name will be created under C{addons_path}.
		@param addons_path: Path where to extract contents.
		@type addons_path: string
		@param override: specifies if the contents of the addon-directory are or not overriden
		@type override: boolean
		"""
		name = self._manifest['name']
		path = os.path.join(addons_path, name)
		if not override and os.path.isdir(path):
			raise AddonError, "Addon already installed."
		with zipfile.ZipFile(self._filename, 'r') as z:
			z.extractall(path)

	@property
	def manifest(self):
		""" Gets the manifest for the represented Addon.
		@rtype AddonManifest
		"""
		return self._manifest

def _report_manifest_errors(manifest):
	log.warning("Error loading manifest:\n%s", manifest.errors)

def create_addon_bundle_from_manifest(manifest_path, dest_dir='.'):
	""" Creates the bundle in zip format from a manifest and specified data.
"""
	basedir = os.path.dirname(os.path.abspath(manifest_path))
	with open(manifest_path) as f:
		manifest = AddonManifest(f)
	if manifest.errors is not None:
		_report_manifest_errors(manifest)
		return False
	bundle_name = "%s-%s.nda-adon" % (manifest['name'], manifest['version'])
	with zipfile.PyZipFile(bundle_name, 'w') as z:
		# write manifest
		z.write(manifest_path, MANIFEST_FILENAME)
		# Write python files. Compiling if necessary.
		z.writepy(basedir)
		# simple includes
		includes = itertools.chain(*[glob.glob(path) for path in manifest['data']['include']])
		for path in includes:
			z.write(os.path.join(basedir, path), path)


class AddonManifest(ConfigObj):
	""" Add-on manifest file. It contains metadata about an NVDA add-on package. """
	configspec = ConfigObj(StringIO(
	"""
# NVDA Ad-don Manifest configuration specification
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

# Extra data to bundle with the add-on.
# Python files and packages are bundled by default.
# Must be relative to the base directory where are this manifest.
[data]
# Extra files to include. Can use glob expressions.
include = list(default=list())
# Directories to include recursively.
include_recursive = list(default=list())
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
