import zipfile
from typing import Optional

import winKernel

from .addonBase import AddonBase, AddonError
from .AddonManifest import MANIFEST_FILENAME, AddonManifest, _report_manifest_errors, _translatedManifestPaths


class AddonBundle(AddonBase):
	"""Represents the contents of an NVDA addon suitable for distribution.
	The bundle is compressed using the zip file format. Manifest information
	is available without the need for extraction."""

	def __init__(self, bundlePath: str):
		"""Constructs an L{AddonBundle} from a filename.
		@param bundlePath: The path for the bundle file.
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
		The addon will be extracted to L{addonPath}
		@param addonPath: Path where to extract contents.
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
		"""Gets the manifest for the represented Addon."""
		return self._manifest

	def __repr__(self):
		return "<AddonBundle at %s>" % self._path
