# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import enum
from typing import (
	Dict,
	Optional,
	OrderedDict,
	Set,
	TYPE_CHECKING,
)

from logHandler import log
from utils.displayString import DisplayStringEnum

if TYPE_CHECKING:
	from .addon import AddonGUIModel  # noqa: F401


@enum.unique
class AvailableAddonStatus(DisplayStringEnum):
	""" Values to represent the status of add-ons within the NVDA add-on store.
	Although related, these are independent of the states in L{addonHandler}
	"""
	PENDING_REMOVE = enum.auto()
	AVAILABLE = enum.auto()
	UPDATE = enum.auto()
	REPLACE_SIDE_LOAD = enum.auto()
	"""
	Used when an addon in the store matches an installed add-on ID.
	However, it cannot be determined if it is an upgrade.
	Encourage the user to compare the version strings.
	"""
	INCOMPATIBLE = enum.auto()
	DOWNLOADING = enum.auto()
	DOWNLOAD_FAILED = enum.auto()
	DOWNLOAD_SUCCESS = enum.auto()
	INSTALLING = enum.auto()
	INSTALL_FAILED = enum.auto()
	INSTALLED = enum.auto()  # installed, requires restart
	PENDING_DISABLE = enum.auto()  # disabled after restart
	INCOMPATIBLE_DISABLED = enum.auto()  # disabled due to being incompatible
	DISABLED = enum.auto()
	PENDING_ENABLE = enum.auto()  # enabled after restart
	RUNNING = enum.auto()  # enabled / active.

	@property
	def _displayStringLabels(self) -> Dict["AvailableAddonStatus", str]:
		return {
			# Translators: Status for addons shown in the add-on store dialog
			self.PENDING_REMOVE: pgettext("addonStore", "Pending removed"),
			# Translators: Status for addons shown in the add-on store dialog
			self.AVAILABLE: pgettext("addonStore", "Available"),
			# Translators: Status for addons shown in the add-on store dialog
			self.UPDATE: pgettext("addonStore", "Update Available"),
			# Translators: Status for addons shown in the add-on store dialog
			self.REPLACE_SIDE_LOAD: pgettext("addonStore", "Migrate to add-on store"),
			# Translators: Status for addons shown in the add-on store dialog
			self.INCOMPATIBLE: pgettext("addonStore", "Incompatible"),
			# Translators: Status for addons shown in the add-on store dialog
			self.DOWNLOADING: pgettext("addonStore", "Downloading"),
			# Translators: Status for addons shown in the add-on store dialog
			self.DOWNLOAD_FAILED: pgettext("addonStore", "Download failed"),
			# Translators: Status for addons shown in the add-on store dialog
			self.DOWNLOAD_SUCCESS: pgettext("addonStore", "Downloaded, pending install"),
			# Translators: Status for addons shown in the add-on store dialog
			self.INSTALLING: pgettext("addonStore", "Installing"),
			# Translators: Status for addons shown in the add-on store dialog
			self.INSTALL_FAILED: pgettext("addonStore", "Install failed"),
			# Translators: Status for addons shown in the add-on store dialog
			self.INSTALLED: pgettext("addonStore", "Installed, pending restart"),
			# Translators: Status for addons shown in the add-on store dialog
			self.PENDING_DISABLE: pgettext("addonStore", "Disabled, pending restart"),
			# Translators: Status for addons shown in the add-on store dialog
			self.DISABLED: pgettext("addonStore", "Disabled"),
			# Translators: Status for addons shown in the add-on store dialog
			self.INCOMPATIBLE_DISABLED: pgettext("addonStore", "Disabled (Incompatible)"),
			# Translators: Status for addons shown in the add-on store dialog
			self.PENDING_ENABLE: pgettext("addonStore", "Enabled, pending restart"),
			# Translators: Status for addons shown in the add-on store dialog
			self.RUNNING: pgettext("addonStore", "Enabled"),
		}


class AddonStateCategory(str, enum.Enum):
	"""
	For backwards compatibility, the enums must remain functionally a string.
	I.E. the following must be true:
	> assert isinstance(AddonStateCategory.PENDING_REMOVE, str)
	> assert AddonStateCategory.PENDING_REMOVE == "pendingRemovesSet"
	"""
	PENDING_REMOVE = "pendingRemovesSet"
	PENDING_INSTALL = "pendingInstallsSet"
	DISABLED = "disabledAddons"
	PENDING_ENABLE = "pendingEnableSet"
	PENDING_DISABLE = "pendingDisableSet"
	OVERRIDE_COMPATIBILITY = "overrideCompatibility"
	"""
	Should be reset when changing to a new breaking release,
	add-ons should be removed from this list when they are updated, disabled or removed
	"""
	BLOCKED = "blocked"
	"""Add-ons that are blocked from running because they are incompatible"""


def getStatus(model: "AddonGUIModel") -> Optional[AvailableAddonStatus]:
	from addonHandler import (
		state as addonHandlerState,
	)
	from ..dataManager import addonDataManager
	from .addon import AddonStoreModel
	from .version import MajorMinorPatch
	addonHandlerModel = model._addonHandlerModel
	if addonHandlerModel is None:
		if not model.isCompatible:
			# Installed incompatible add-ons have a status of disabled or running
			return AvailableAddonStatus.INCOMPATIBLE

		# Any compatible add-on which is not installed should be listed as available
		return AvailableAddonStatus.AVAILABLE

	for storeState, handlerStateCategory in _addonStoreStateToAddonHandlerState.items():
		# Ensure disabled status and install status are checked first if installed
		if model.addonId in addonHandlerState[handlerStateCategory]:
			return storeState

	addonStoreData = addonDataManager._getCachedInstalledAddonData(model.addonId)
	if isinstance(model, AddonStoreModel):
		# If the listed add-on is installed from a side-load
		# and not available on the add-on store
		# the type will not be AddonStoreModel
		if addonStoreData is not None:
			if model.addonVersionNumber > addonStoreData.addonVersionNumber:
				return AvailableAddonStatus.UPDATE
		else:
			# Parsing from a side-loaded add-on
			try:
				manifestAddonVersion = MajorMinorPatch._parseVersionFromVersionStr(addonHandlerModel.version)
			except ValueError:
				# Parsing failed to get a numeric version.
				# Ideally a numeric version would be compared,
				# however the manifest only has a version string.
				# Ensure the user is aware that it may be a downgrade or reinstall.
				# Encourage users to re-install or upgrade the add-on from the add-on store.
				return AvailableAddonStatus.REPLACE_SIDE_LOAD

			if model.addonVersionNumber > manifestAddonVersion:
				return AvailableAddonStatus.UPDATE

	if addonHandlerModel.isRunning:
		return AvailableAddonStatus.RUNNING

	log.debugWarning(f"Add-on in unknown state: {model.addonId}")
	return None


_addonStoreStateToAddonHandlerState: OrderedDict[AvailableAddonStatus, AddonStateCategory] = OrderedDict({
	# Pending states must be first as the pending state may be altering another state.
	AvailableAddonStatus.PENDING_ENABLE: AddonStateCategory.PENDING_ENABLE,
	AvailableAddonStatus.PENDING_DISABLE: AddonStateCategory.PENDING_DISABLE,
	AvailableAddonStatus.PENDING_REMOVE: AddonStateCategory.PENDING_REMOVE,
	AvailableAddonStatus.INCOMPATIBLE_DISABLED: AddonStateCategory.BLOCKED,
	AvailableAddonStatus.DISABLED: AddonStateCategory.DISABLED,
	AvailableAddonStatus.INSTALLED: AddonStateCategory.PENDING_INSTALL,
})


class _StatusFilterKey(DisplayStringEnum):
	"""Keys for filtering by status in the NVDA add-on store."""
	INSTALLED = enum.auto()
	UPDATE = enum.auto()
	AVAILABLE = enum.auto()
	DISABLED = enum.auto()

	@property
	def _displayStringLabels(self) -> Dict["_StatusFilterKey", str]:
		return {
			# Translators: A selection option to display installed add-ons in the add-on store
			self.INSTALLED: pgettext("addonStore", "Installed add-ons"),
			# Translators: A selection option to display updatable add-ons in the add-on store
			self.UPDATE: pgettext("addonStore", "Updatable add-ons"),
			# Translators: A selection option to display available add-ons in the add-on store
			self.AVAILABLE: pgettext("addonStore", "Available add-ons"),
			# Translators: A selection option to display disabled add-ons in the add-on store
			self.DISABLED: pgettext("addonStore", "Disabled add-ons"),
		}


_statusFilters: OrderedDict[_StatusFilterKey, Set[AvailableAddonStatus]] = OrderedDict({
	_StatusFilterKey.INSTALLED: {
		AvailableAddonStatus.UPDATE,
		AvailableAddonStatus.REPLACE_SIDE_LOAD,
		AvailableAddonStatus.INSTALLED,
		AvailableAddonStatus.PENDING_DISABLE,
		AvailableAddonStatus.INCOMPATIBLE_DISABLED,
		AvailableAddonStatus.DISABLED,
		AvailableAddonStatus.PENDING_ENABLE,
		AvailableAddonStatus.PENDING_REMOVE,
		AvailableAddonStatus.RUNNING,
	},
	_StatusFilterKey.UPDATE: {
		AvailableAddonStatus.UPDATE,
		AvailableAddonStatus.REPLACE_SIDE_LOAD,
	},
	_StatusFilterKey.AVAILABLE: {
		AvailableAddonStatus.INCOMPATIBLE,
		AvailableAddonStatus.AVAILABLE,
		AvailableAddonStatus.UPDATE,
		AvailableAddonStatus.REPLACE_SIDE_LOAD,
		AvailableAddonStatus.DOWNLOAD_FAILED,
		AvailableAddonStatus.DOWNLOAD_SUCCESS,
		AvailableAddonStatus.DOWNLOADING,
		AvailableAddonStatus.INSTALLING,
		AvailableAddonStatus.INSTALL_FAILED,
		AvailableAddonStatus.INSTALLED,
	},
	_StatusFilterKey.DISABLED: {
		AvailableAddonStatus.INCOMPATIBLE_DISABLED,
		AvailableAddonStatus.DISABLED,
		AvailableAddonStatus.PENDING_DISABLE,
		AvailableAddonStatus.PENDING_ENABLE,
	},
})
"""A dictionary where the keys are a status to filter by,
and the values are which statuses should be shown for a given filter.
"""
