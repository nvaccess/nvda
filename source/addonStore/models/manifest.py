# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functionality related to add-on manifests."""

import os
import os.path
from collections.abc import Generator, Sequence

from addonHandler import (
	ADDON_PENDINGINSTALL_SUFFIX,
	DELETEDIR_SUFFIX,
	MANIFEST_FILENAME,
	AddonManifest,
	_translatedManifestPaths,
)
from fileUtils import isDirEmpty
from logHandler import log


def _loadManifest(path: os.PathLike, translationRelpaths: Sequence[str]) -> AddonManifest:
	"""Load an add-on manifest from the given directory, applying the first available translation.

	:param path: Path to the add-on directory containing the manifest file.
	:param translationRelpaths: Relative paths to translated manifest files, in priority order.
	:return: The loaded manifest, translated if a translation file was found.
	"""
	with open(os.path.join(path, MANIFEST_FILENAME), "rb") as untranslatedFile:
		for translationRelpath in translationRelpaths:
			translationPath = os.path.join(path, translationRelpath)
			if not os.path.isfile(translationPath):
				continue
			try:
				with open(translationPath, "rb") as translatedFile:
					return AddonManifest(untranslatedFile, translatedFile)
			except OSError:
				continue
		return AddonManifest(untranslatedFile)


def _getAddonManifestsFromPath(path: os.PathLike) -> Generator[AddonManifest, None, None]:
	"""Yield add-on manifests from subdirectories of the given path.

	Subdirectories that are empty, pending deletion, or pending install are skipped.
	Manifests that fail to load are logged and skipped.

	:param path: Path to the directory containing add-on subdirectories.
	:return: An iterator of successfully loaded add-on manifests.
	"""
	translationPaths = None
	with os.scandir(path) as scanner:
		for entry in scanner:
			if (
				not entry.is_dir(follow_symlinks=False)
				or entry.name.endswith(DELETEDIR_SUFFIX)
				or entry.name.endswith(ADDON_PENDINGINSTALL_SUFFIX)
				or isDirEmpty(entry.path)
			):
				log.debug(f"Skipping {entry.path}")
				continue
			if translationPaths is None:
				translationPaths = _translatedManifestPaths()
			try:
				yield _loadManifest(entry.path, translationPaths)
			except Exception:
				log.debug(f"Failed to load add-on manifest from {entry.path}.", exc_info=True)
