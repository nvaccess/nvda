# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	cast,
)

import wx
from wx.adv import BannerWindow

from addonHandler import (
	BUNDLE_EXTENSION,
)
from addonStore.dataManager import addonDataManager
from addonStore.models.channel import Channel, _channelFilters
from addonStore.models.status import (
	EnabledStatus,
	_statusFilters,
	_StatusFilterKey,
)
import config
from core import callLater
import globalVars
import gui
from gui import (
	guiHelper,
	addonGui,
)
from gui.message import DisplayableError, displayDialogAsModal
from gui.settingsDialogs import SettingsDialog
from logHandler import log

from ..viewModels.store import AddonStoreVM
from .actions import _MonoActionsContextMenu
from .addonList import AddonVirtualList
from .details import AddonDetails
from .messageDialogs import _SafetyWarningDialog


class AddonStoreDialog(SettingsDialog):
	# Translators: The title of the addonStore dialog where the user can find and download add-ons
	title = pgettext("addonStore", "Add-on Store")
	# For the Add-on Store paragraph in the User Guide, we have kept "AddonsManager" anchor instead of something
	# more adapted like "AddonStore" so that old external links pointing to the add-ons manager paragraph now
	# point to the Add-on Store one.
	helpId = "AddonsManager"

	def __init__(self, parent: wx.Window, storeVM: AddonStoreVM):
		self._storeVM = storeVM
		self._storeVM.onDisplayableError.register(self.handleDisplayableError)
		self._actionsContextMenu = _MonoActionsContextMenu(self._storeVM)
		super().__init__(parent, resizeable=True, buttons={wx.CLOSE})
		if config.conf["addonStore"]["showWarning"]:
			displayDialogAsModal(_SafetyWarningDialog(parent))
		self.Maximize()

	def _enterActivatesOk_ctrlSActivatesApply(self, evt: wx.KeyEvent):
		"""Disables parent behaviour which overrides behaviour for enter and ctrl+s"""
		evt.Skip()

	def handleDisplayableError(self, displayableError: DisplayableError):
		displayableError.displayError(gui.mainFrame)

	def makeSettings(self, settingsSizer: wx.BoxSizer):
		if globalVars.appArgs.disableAddons:
			self._makeBanner()

		splitViewSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.addonListTabs = wx.Notebook(self)
		# Use a single tab page for every tab.
		# Instead perform dynamic updates to the tab page when the tab is changed.
		dynamicTabPage = wx.Panel(self.addonListTabs)
		tabPageHelper = guiHelper.BoxSizerHelper(dynamicTabPage, wx.VERTICAL)
		splitViewSizer.Add(tabPageHelper.sizer, flag=wx.EXPAND, proportion=1)
		for statusFilter in _statusFilters:
			self.addonListTabs.AddPage(dynamicTabPage, statusFilter.displayString)
		tabPageHelper.addItem(self.addonListTabs, flag=wx.EXPAND)
		if any(self._storeVM._installedAddons[channel] for channel in self._storeVM._installedAddons):
			# If there's any installed add-ons, use the installed add-ons page by default
			self.addonListTabs.SetSelection(0)
		else:
			availableTabIndex = list(_statusFilters.keys()).index(_StatusFilterKey.AVAILABLE)
			self.addonListTabs.SetSelection(availableTabIndex)
		self.addonListTabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onListTabPageChange, self.addonListTabs)

		self.filterCtrlHelper = guiHelper.BoxSizerHelper(self, wx.VERTICAL)
		self._createFilterControls()
		tabPageHelper.addItem(self.filterCtrlHelper.sizer, flag=wx.EXPAND)

		tabPageHelper.sizer.AddSpacer(5)

		settingsSizer.Add(splitViewSizer, flag=wx.EXPAND, proportion=1)

		self.listLabel = wx.StaticText(self)
		tabPageHelper.addItem(
			self.listLabel,
			flag=wx.EXPAND
		)
		self._setListLabels()

		self.addonListView = AddonVirtualList(
			parent=self,
			addonsListVM=self._storeVM.listVM,
			actionsContextMenu=self._actionsContextMenu,
		)
		self.bindHelpEvent("AddonStoreBrowsing", self.addonListView)
		tabPageHelper.addItem(self.addonListView, flag=wx.EXPAND, proportion=1)
		splitViewSizer.AddSpacer(5)

		self.addonDetailsView = AddonDetails(
			parent=self,
			detailsVM=self._storeVM.detailsVM,
			actionsContextMenu=self._actionsContextMenu,
		)
		splitViewSizer.Add(self.addonDetailsView, flag=wx.EXPAND, proportion=1)
		self.bindHelpEvent("AddonStoreActions", self.addonDetailsView.actionsButton)

		generalActions = guiHelper.ButtonHelper(wx.HORIZONTAL)
		# Translators: The label for a button in add-ons Store dialog to install an external add-on.
		externalInstallLabelText = pgettext("addonStore", "Install from e&xternal source")
		self.externalInstallButton = generalActions.addButton(self, label=externalInstallLabelText)
		self.externalInstallButton.Bind(wx.EVT_BUTTON, self.openExternalInstall, self.externalInstallButton)
		self.bindHelpEvent("AddonStoreInstalling", self.externalInstallButton)

		settingsSizer.AddSpacer(guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		settingsSizer.Add(generalActions.sizer)
		self.onListTabPageChange(None)

	def _makeBanner(self):
		self.banner = BannerWindow(self, dir=wx.TOP)
		# Translators: Banner notice that is displayed in the Add-on Store.
		bannerText = pgettext("addonStore", "Note: NVDA was started with add-ons disabled")
		self.banner.SetText(
			bannerText,
			"",
		)
		normalBgColour = self.GetBackgroundColour()
		self.banner.SetGradient(normalBgColour, normalBgColour)
		self.settingsSizer.Add(self.banner, flag=wx.CENTER)

	def _createFilterControls(self):
		filterCtrlsLine0 = guiHelper.BoxSizerHelper(self, wx.HORIZONTAL)
		filterCtrlsLine1 = guiHelper.BoxSizerHelper(self, wx.HORIZONTAL)
		self.filterCtrlHelper.addItem(filterCtrlsLine0.sizer)

		# Add margin left padding
		FILTER_MARGIN_PADDING = 15
		filterCtrlsLine0.sizer.AddSpacer(FILTER_MARGIN_PADDING)
		filterCtrlsLine1.sizer.AddSpacer(FILTER_MARGIN_PADDING)
		self.filterCtrlHelper.addItem(filterCtrlsLine1.sizer, flag=wx.EXPAND, proportion=1)

		self.channelFilterCtrl = cast(wx.Choice, filterCtrlsLine0.addLabeledControl(
			# Translators: The label of a selection field to filter the list of add-ons in the add-on store dialog.
			labelText=pgettext("addonStore", "Cha&nnel:"),
			wxCtrlClass=wx.Choice,
			choices=list(c.displayString for c in _channelFilters),
		))
		self.channelFilterCtrl.Bind(wx.EVT_CHOICE, self.onChannelFilterChange, self.channelFilterCtrl)
		self.bindHelpEvent("AddonStoreFilterChannel", self.channelFilterCtrl)

		# Translators: The label of a checkbox to filter the list of add-ons in the add-on store dialog.
		incompatibleAddonsLabel = pgettext("addonStore", "Include &incompatible add-ons")
		self.includeIncompatibleCtrl = cast(wx.CheckBox, filterCtrlsLine0.addItem(
			wx.CheckBox(self, label=incompatibleAddonsLabel)
		))
		self.includeIncompatibleCtrl.SetValue(0)
		self.includeIncompatibleCtrl.Bind(
			wx.EVT_CHECKBOX,
			self.onIncompatibleFilterChange,
			self.includeIncompatibleCtrl
		)
		self.bindHelpEvent("AddonStoreFilterIncompatible", self.includeIncompatibleCtrl)

		self.enabledFilterCtrl = cast(wx.Choice, filterCtrlsLine0.addLabeledControl(
			# Translators: The label of a selection field to filter the list of add-ons in the add-on store dialog.
			labelText=pgettext("addonStore", "Ena&bled/disabled:"),
			wxCtrlClass=wx.Choice,
			choices=list(c.displayString for c in EnabledStatus),
		))
		self.enabledFilterCtrl.Bind(wx.EVT_CHOICE, self.onEnabledFilterChange, self.enabledFilterCtrl)
		self.bindHelpEvent("AddonStoreFilterEnabled", self.enabledFilterCtrl)

		# Translators: The label of a text field to filter the list of add-ons in the add-on store dialog.
		searchFilterLabel = wx.StaticText(self, label=pgettext("addonStore", "&Search:"))
		# noinspection PyAttributeOutsideInit
		self.searchFilterCtrl = wx.TextCtrl(self)
		self.searchFilterCtrl.Bind(wx.EVT_TEXT, self.onFilterTextChange, self.searchFilterCtrl)
		self.bindHelpEvent("AddonStoreFilterSearch", self.searchFilterCtrl)

		filterCtrlsLine1.addItem(searchFilterLabel)
		filterCtrlsLine1.addItem(self.searchFilterCtrl, proportion=1)

		# Add end margin right padding
		filterCtrlsLine0.sizer.AddSpacer(FILTER_MARGIN_PADDING)
		filterCtrlsLine1.sizer.AddSpacer(FILTER_MARGIN_PADDING)

	def postInit(self):
		if globalVars.appArgs.disableAddons:
			self.banner.SetFocus()
		else:
			self.addonListView.SetFocus()

	def _onWindowDestroy(self, evt: wx.WindowDestroyEvent):
		requiresRestart = self._requiresRestart
		super()._onWindowDestroy(evt)
		if requiresRestart:
			wx.CallAfter(addonGui.promptUserForRestart)

	# Translators: Title for message shown prior to installing add-ons when closing the add-on store dialog.
	_installationPromptTitle = pgettext("addonStore", "Add-on installation")

	def onClose(self, evt: wx.CommandEvent):
		numInProgress = len(self._storeVM._downloader.progress)
		if numInProgress:
			res = gui.messageBox(
				npgettext(
					"addonStore",
					# Translators: Message shown prior to installing add-ons when closing the add-on store dialog
					# The placeholder {} will be replaced with the number of add-ons to be installed
					"Download of {} add-on in progress, cancel downloading?",
					"Download of {} add-ons in progress, cancel downloading?",
					numInProgress,
				).format(numInProgress),
				self._installationPromptTitle,
				style=wx.YES_NO
			)
			if res == wx.YES:
				log.debug("Cancelling the download.")
				self._storeVM.cancelDownloads()
				# Continue to installation if any downloads completed
			else:
				# Let the user return to the add-on store and inspect add-ons being downloaded.
				return

		if addonDataManager._downloadsPendingInstall:
			nAddonsPendingInstall = len(addonDataManager._downloadsPendingInstall)
			installingDialog = gui.IndeterminateProgressDialog(
				self,
				self._installationPromptTitle,
				npgettext(
					"addonStore",
					# Translators: Message shown while installing add-ons after closing the add-on store dialog
					# The placeholder {} will be replaced with the number of add-ons to be installed
					"Installing {} add-on, please wait.",
					"Installing {} add-ons, please wait.",
					nAddonsPendingInstall,
				).format(nAddonsPendingInstall)
			)
			self._storeVM.installPending()

			def postInstall():
				installingDialog.done()
				# let the dialog exit.
				super(AddonStoreDialog, self).onClose(evt)

			return wx.CallAfter(postInstall)

		# let the dialog exit.
		super().onClose(evt)

	@property
	def _requiresRestart(self) -> bool:
		from addonHandler import state, AddonStateCategory
		if (
			addonDataManager._downloadsPendingInstall
			or state[AddonStateCategory.PENDING_INSTALL]
		):
			log.debug(
				"Add-ons pending install, restart required.\n"
				f"Downloads pending install (add-on store installs): {addonDataManager._downloadsPendingInstall}.\n"
				f"Addons pending install (external installs): {state[AddonStateCategory.PENDING_INSTALL]}.\n"
			)
			return True

		for addonsForChannel in self._storeVM._installedAddons.values():
			for addon in addonsForChannel.values():
				if addon._addonHandlerModel.requiresRestart:
					log.debug(f"Add-on {addon.name} modified, restart required")
					return True

		return False

	@property
	def _statusFilterKey(self) -> _StatusFilterKey:
		index = self.addonListTabs.GetSelection()
		return list(_statusFilters.keys())[index]

	@property
	def _channelFilterKey(self) -> Channel:
		index = self.channelFilterCtrl.GetSelection()
		return list(_channelFilters.keys())[index]

	@property
	def _titleText(self) -> str:
		return f"{self.title} - {self._statusFilterKey.displayString} ({self._channelFilterKey.displayString})"

	@property
	def _listLabelText(self) -> str:
		return pgettext(
			"addonStore",
			# Translators: The label of the add-on list in the add-on store; {category} is replaced by the selected
			# tab's name.
			"{category}:",
		).format(category=self._statusFilterKey.displayStringWithAccelerator)

	def _setListLabels(self):
		self.listLabel.SetLabel(self._listLabelText)
		self.SetTitle(self._titleText)

	def _toggleFilterControls(self):
		self.channelFilterCtrl.Clear()
		for c in _channelFilters:
			if c != Channel.EXTERNAL:
				self.channelFilterCtrl.Append(c.displayString)
		if self._storeVM._filteredStatusKey in {
			_StatusFilterKey.AVAILABLE,
			_StatusFilterKey.UPDATE,
		}:
			self._storeVM._filterChannelKey = Channel.STABLE
			self.enabledFilterCtrl.Hide()
			self.enabledFilterCtrl.Disable()
			self.includeIncompatibleCtrl.Enable()
			self.includeIncompatibleCtrl.Show()
		else:
			self.channelFilterCtrl.Append(Channel.EXTERNAL.displayString)
			self._storeVM._filterChannelKey = Channel.ALL
			self.enabledFilterCtrl.Show()
			self.enabledFilterCtrl.Enable()
			self.includeIncompatibleCtrl.Hide()
			self.includeIncompatibleCtrl.Disable()

	def onListTabPageChange(self, evt: wx.EVT_CHOICE):
		self.searchFilterCtrl.SetValue("")

		self._storeVM._filterEnabledDisabled = EnabledStatus.ALL
		self.enabledFilterCtrl.SetSelection(0)

		self._storeVM._filteredStatusKey = self._statusFilterKey
		self.addonListView._refreshColumns()
		self._toggleFilterControls()

		channelFilterIndex = list(_channelFilters.keys()).index(self._storeVM._filterChannelKey)
		self.channelFilterCtrl.SetSelection(channelFilterIndex)
		self._storeVM.listVM.setSelection(None)
		self._setListLabels()
		self._storeVM.refresh()
		self.Layout()

		# avoid erratic focus on the contained panel
		if not self.addonListTabs.HasFocus():
			self.addonListTabs.SetFocus()

	def onChannelFilterChange(self, evt: wx.EVT_CHOICE):
		self._storeVM._filterChannelKey = self._channelFilterKey
		self._storeVM.listVM.setSelection(None)
		self._setListLabels()
		self._storeVM.refresh()

	def onFilterTextChange(self, evt: wx.EVT_TEXT):
		filterText = self.searchFilterCtrl.GetValue()
		self.filter(filterText)

	def onEnabledFilterChange(self, evt: wx.EVT_CHOICE):
		index = self.enabledFilterCtrl.GetCurrentSelection()
		self._storeVM._filterEnabledDisabled = list(EnabledStatus)[index]
		self._storeVM.refresh()

	def onIncompatibleFilterChange(self, evt: wx.EVT_CHECKBOX):
		self._storeVM._filterIncludeIncompatible = self.includeIncompatibleCtrl.GetValue()
		self._storeVM.refresh()

	def filter(self, filterText: str):
		self._storeVM.listVM.applyFilter(filterText)

	def openExternalInstall(self, evt: wx.EVT_BUTTON):
		# Translators: the label for the NVDA add-on package file type in the Choose add-on dialog.
		fileTypeLabel = pgettext("addonStore", "NVDA Add-on Package (*.{ext})")
		fd = wx.FileDialog(
			self,
			# Translators: The message displayed in the dialog that
			# allows you to choose an add-on package for installation.
			message=pgettext("addonStore", "Choose Add-on Package File"),
			wildcard=(fileTypeLabel + "|*.{ext}").format(ext=BUNDLE_EXTENSION),
			defaultDir="c:",
			style=wx.FD_OPEN,
		)
		if displayDialogAsModal(fd) != wx.ID_OK:
			return
		addonPath = fd.GetPath()
		try:
			addonGui.installAddon(self, addonPath)
		except DisplayableError as displayableError:
			callLater(delay=0, callable=self._storeVM.onDisplayableError.notify, displayableError=displayableError)
			return
		self._storeVM.refresh()
