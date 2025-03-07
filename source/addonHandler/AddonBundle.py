# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2025 Rui Batista, NV Access Limited, Noelia Ruiz Martínez, Joseph Lee, Babbage B.V.,
# Arnold Loubriat, Łukasz Golonka, Leonard de Ruijter, Julien Cochuyt, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
import zipfile
from typing import Optional

import winKernel

from .addonBase import AddonBase, AddonError
from .AddonManifest import MANIFEST_FILENAME, AddonManifest, _report_manifest_errors, _translatedManifestPaths

BUNDLE_EXTENSION = "nvda-addon"


class AddonBundle(AddonBase):
	"""Represents the contents of an NVDA addon suitable for distribution.
	The bundle is compressed using the zip file format. Manifest information
	is available without the need for extraction."""

	def __init__(self, bundlePath: str):
		"""Constructs an AddonBundle from a filename.

		:param bundlePath: The path for the bundle file.
		"""
		self._installExceptions: list[Exception] = []
		"""Exceptions thrown during the installation process."""

		self._path = bundlePath
		# Read manifest:
		translatedInput = None
		try:
			z = zipfile.ZipFile(self._path, "r")
		except (zipfile.BadZipfile, FileNotFoundError) as e:
			raise AddonError(f"Invalid bundle file: {self._path}") from e
		with z:
			for translationPath in _translatedManifestPaths(forBundle=True):
				try:
					# ZipFile.open opens every file in binary mode.
					# decoding is handled by configobj.
					translatedInput = z.open(translationPath, "r")
					break
				except KeyError:
					pass
			self._manifest = AddonManifest(
				# ZipFile.open opens every file in binary mode.
				# decoding is handled by configobj.
				z.open(MANIFEST_FILENAME, "r"),
				translatedInput=translatedInput,
			)
			if self.manifest.errors is not None:
				_report_manifest_errors(self.manifest)
				raise AddonError("Manifest file has errors.")

	def extract(self, addonPath: Optional[str] = None):
		"""Extracts the bundle content to the specified path.

		The addon will be extracted to the specified addonPath.

		:param addonPath: Path where to extract contents. If None, uses pendingInstallPath.
		"""
		if addonPath is None:
			addonPath = self.pendingInstallPath

		with zipfile.ZipFile(self._path, "r") as z:
			for info in z.infolist():
				if isinstance(info.filename, bytes):
					# #2505: Handle non-Unicode file names.
					# Most archivers seem to use the local OEM code page, even though the spec says only cp437.
					# HACK: Overriding info.filename is a bit ugly, but it avoids a lot of code duplication.
					info.filename = info.filename.decode("cp%d" % winKernel.kernel32.GetOEMCP())
				z.extract(info, addonPath)

	@property
	def manifest(self) -> "AddonManifest":
		"""Gets the manifest for the represented Addon.

		:return: The addon manifest.
		"""
		return self._manifest

	def __repr__(self):
		return "<AddonBundle at %s>" % self._path


def createAddonBundleFromPath(path, destDir=None):
	"""Creates a bundle from a directory that contains an addon manifest file.

	:param path: Path to the directory containing the addon.
	:param destDir: Directory where the bundle should be created. If None, uses the parent directory of path.
	:return: The created AddonBundle.
	:raises AddonError: If the manifest file is missing or has errors.
	"""
	basedir = path
	# If  caller did not provide a destination directory name
	# Put the bundle at the same level as the add-on's top-level directory,
	# That is, basedir/..
	if destDir is None:
		destDir = os.path.dirname(basedir)
	manifest_path = os.path.join(basedir, MANIFEST_FILENAME)
	if not os.path.isfile(manifest_path):
		raise AddonError("Can't find %s manifest file." % manifest_path)
	with open(manifest_path, "rb") as f:
		manifest = AddonManifest(f)
	if manifest.errors is not None:
		_report_manifest_errors(manifest)
		raise AddonError("Manifest file has errors.")
	bundleFilename = "%s-%s.%s" % (manifest["name"], manifest["version"], BUNDLE_EXTENSION)
	bundleDestination = os.path.join(destDir, bundleFilename)
	with zipfile.ZipFile(bundleDestination, "w") as z:
		# FIXME: the include/exclude feature may or may not be useful. Also python files can be pre-compiled.
		for dir, dirnames, filenames in os.walk(basedir):
			relativePath = os.path.relpath(dir, basedir)
			for filename in filenames:
				pathInBundle = os.path.join(relativePath, filename)
				absPath = os.path.join(dir, filename)
				z.write(absPath, pathInBundle)
	return AddonBundle(bundleDestination)
