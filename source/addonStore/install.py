# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from os import (
	PathLike,
)
from typing import (
	TYPE_CHECKING,
	cast,
	Optional,
)

import systemUtils
from logHandler import log

from .dataManager import (
	addonDataManager,
)

if TYPE_CHECKING:
	from addonHandler import AddonBundle, Addon as AddonHandlerModel  # noqa: F401


def _getAddonBundleToInstallIfValid(addonPath: str) -> "AddonBundle":
	"""
	@param addonPath: path to the 'nvda-addon' file.
	@return: the addonBundle, if valid
	@raise DisplayableError if the addon bundle is invalid / incompatible.
	"""
	from addonHandler import AddonBundle, AddonError
	from gui.message import DisplayableError

	try:
		bundle = AddonBundle(addonPath)
	except AddonError:
		log.error("Error opening addon bundle from %s" % addonPath, exc_info=True)
		raise DisplayableError(
			displayMessage=pgettext(
				"addonStore",
				# Translators: The message displayed when an error occurs when opening an add-on package for adding.
				# The %s will be replaced with the path to the add-on that could not be opened.
				"Failed to open add-on package file at {filePath} - missing file or invalid file format"
			).format(filePath=addonPath)
		)

	if not bundle.isCompatible and not (
		bundle.canOverrideCompatibility and bundle._hasOverriddenCompat
	):
		# This should not happen, only compatible or overridable add-ons are
		# intended to be presented in the add-on store.
		raise DisplayableError(
			displayMessage=pgettext(
				"addonStore",
				# Translators: The message displayed when an add-on is not supported by this version of NVDA.
				# The %s will be replaced with the path to the add-on that is not supported.
				"Add-on not supported %s"
			) % addonPath
		)
	return bundle


def _getPreviouslyInstalledAddonById(addon: "AddonBundle") -> Optional["AddonHandlerModel"]:
	assert addonDataManager
	installedAddon = addonDataManager._installedAddonsCache.installedAddons.get(addon.name)
	if installedAddon is None or installedAddon.isPendingRemove:
		return None
	return installedAddon


def installAddon(addonPath: PathLike) -> None:
	""" Installs the addon at path.
	Any error messages / warnings are presented to the user via a GUI message box.
	If attempting to install an addon that is pending removal, it will no longer be pending removal.
	@note See also L{gui.addonGui.installAddon}
	@raise DisplayableError on failure
	"""
	import addonHandler
	from gui.message import DisplayableError

	addonPath = cast(str, addonPath)
	bundle = _getAddonBundleToInstallIfValid(addonPath)
	prevAddon = _getPreviouslyInstalledAddonById(bundle)

	try:
		addonObj = systemUtils.ExecAndPump[addonHandler.Addon](addonHandler.installAddonBundle, bundle).funcRes
		if prevAddon:
			prevAddon.requestRemove()
	except addonHandler.AddonError:  # Handle other exceptions as they are known
		log.error("Error installing addon bundle from %s" % addonPath, exc_info=True)
		raise DisplayableError(
			displayMessage=pgettext(
				"addonStore",
				# Translators: The message displayed when an error occurs when installing an add-on package.
				# The %s will be replaced with the path to the add-on that could not be installed.
				"Failed to install add-on from %s"
			) % addonPath
		)
	finally:
		if addonObj is not None:
			addonObj._cleanupAddonImports()
