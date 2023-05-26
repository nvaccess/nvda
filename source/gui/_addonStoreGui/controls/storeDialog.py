# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	cast,
)

import wx

from addonHandler import (
	BUNDLE_EXTENSION,
)
from _addonStore.models.channel import Channel, _channelFilters
from _addonStore.models.status import (
	EnabledStatus,
	_statusFilters,
	_StatusFilterKey,
)
from core import callLater
import gui
from gui import (
	guiHelper,
	addonGui,
)
from gui.message import DisplayableError
from gui.settingsDialogs import SettingsDialog
from logHandler import log

from ..viewModels.store import AddonStoreVM
from .actions import _ActionsContextMenu
from .addonList import AddonVirtualList
from .details import AddonDetails


class AddonStoreDialog(SettingsDialog):
	# Translators: The title of the addonStore dialog where the user can find and download add-ons
	title = pgettext("addonStore", "Add-on Store")
	helpId = "addonStore"

	def __init__(self, parent: wx.Window, storeVM: AddonStoreVM):
		self._storeVM = storeVM
		self._storeVM.onDisplayableError.register(self.handleDisplayableError)
		self._actionsContextMenu = _ActionsContextMenu(self._storeVM)
		super().__init__(parent, resizeable=True, buttons={wx.CLOSE})

	def _enterActivatesOk_ctrlSActivatesApply(self, evt: wx.KeyEvent):
		"""Disables parent behaviour which overrides behaviour for enter and ctrl+s"""
		evt.Skip()

	def handleDisplayableError(self, displayableError: DisplayableError):
		displayableError.displayError(gui.mainFrame)

	def makeSettings(self, settingsSizer: wx.BoxSizer):
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
		self.addonListTabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onStatusFilterChange, self.addonListTabs)

		self.filterCtrlHelper = guiHelper.BoxSizerHelper(self, wx.HORIZONTAL)
		self._createFilterControls()
		tabPageHelper.addItem(self.filterCtrlHelper.sizer, flag=wx.EXPAND)

		tabPageHelper.sizer.AddSpacer(5)

		settingsSizer.Add(splitViewSizer, flag=wx.EXPAND, proportion=1)

		# add a label for the AddonListVM so that it is announced with a name in NVDA
		self.listLabel = wx.StaticText(self)
		tabPageHelper.addItem(
			self.listLabel,
			flag=wx.EXPAND
		)
		self.listLabel.Hide()
		self._setListLabels()

		self.addonListView = AddonVirtualList(
			parent=self,
			addonsListVM=self._storeVM.listVM,
			actionsContextMenu=self._actionsContextMenu,
		)
		# Add alt+l accelerator key
		_setFocusToAddonListView_eventId = wx.NewIdRef(count=1)
		self.Bind(wx.EVT_MENU, lambda e: self.addonListView.SetFocus(), _setFocusToAddonListView_eventId)
		self.SetAcceleratorTable(wx.AcceleratorTable([
			wx.AcceleratorEntry(wx.ACCEL_ALT, ord("l"), _setFocusToAddonListView_eventId)
		]))
		tabPageHelper.addItem(self.addonListView, flag=wx.EXPAND, proportion=1)
		splitViewSizer.AddSpacer(5)

		self.addonDetailsView = AddonDetails(
			parent=self,
			detailsVM=self._storeVM.detailsVM,
			actionsContextMenu=self._actionsContextMenu,
		)
		splitViewSizer.Add(self.addonDetailsView, flag=wx.EXPAND, proportion=1)

		generalActions = guiHelper.ButtonHelper(wx.HORIZONTAL)
		# Translators: The label for a button in add-ons Store dialog to install an external add-on.
		externalInstallLabelText = pgettext("addonStore", "Install from e&xternal source")
		self.externalInstallButton = generalActions.addButton(self, label=externalInstallLabelText)
		self.externalInstallButton.Bind(wx.EVT_BUTTON, self.openExternalInstall, self.externalInstallButton)
		self.bindHelpEvent("AddonStoreInstalling", self.externalInstallButton)

		settingsSizer.Add(generalActions.sizer)
		self.onStatusFilterChange(None)

	def _createFilterControls(self):
		self.channelFilterCtrl = cast(wx.Choice, self.filterCtrlHelper.addLabeledControl(
			# Translators: The label of a selection field to filter the list of add-ons in the add-on store dialog.
			labelText=pgettext("addonStore", "Cha&nnel:"),
			wxCtrlClass=wx.Choice,
			choices=list(c.displayString for c in _channelFilters),
		))
		self.channelFilterCtrl.Bind(wx.EVT_CHOICE, self.onChannelFilterChange, self.channelFilterCtrl)
		self.bindHelpEvent("AddonStoreFilterChannel", self.channelFilterCtrl)

		self.searchFilterCtrl = cast(wx.TextCtrl, self.filterCtrlHelper.addLabeledControl(
			# Translators: The label of a text field to filter the list of add-ons in the add-on store dialog.
			labelText=pgettext("addonStore", "&Search:"),
			wxCtrlClass=wx.TextCtrl,
		))
		self.searchFilterCtrl.Bind(wx.EVT_TEXT, self.onFilterTextChange, self.searchFilterCtrl)
		self.bindHelpEvent("AddonStoreFilterSearch", self.searchFilterCtrl)

		# Translators: The label of a checkbox to filter the list of add-ons in the add-on store dialog.
		incompatibleAddonsLabel = _("Include &incompatible add-ons")
		self.includeIncompatibleCtrl = cast(wx.CheckBox, self.filterCtrlHelper.addItem(
			wx.CheckBox(self, label=incompatibleAddonsLabel)
		))
		self.includeIncompatibleCtrl.SetValue(0)
		self.includeIncompatibleCtrl.Bind(
			wx.EVT_CHECKBOX,
			self.onIncompatibleFilterChange,
			self.includeIncompatibleCtrl
		)
		self.bindHelpEvent("AddonStoreFilterIncompatible", self.includeIncompatibleCtrl)

		self.enabledFilterCtrl = cast(wx.Choice, self.filterCtrlHelper.addLabeledControl(
			# Translators: The label of a selection field to filter the list of add-ons in the add-on store dialog.
			labelText=pgettext("addonStore", "Ena&bled/disabled:"),
			wxCtrlClass=wx.Choice,
			choices=list(c.displayString for c in EnabledStatus),
		))
		self.enabledFilterCtrl.Bind(wx.EVT_CHOICE, self.onEnabledFilterChange, self.enabledFilterCtrl)
		self.bindHelpEvent("AddonStoreFilterEnabled", self.enabledFilterCtrl)

	def postInit(self):
		self.addonListView.SetFocus()

	def _onWindowDestroy(self, evt: wx.WindowDestroyEvent):
		super()._onWindowDestroy(evt)

	def onClose(self, evt: wx.CommandEvent):
		# Translators: Title for message shown prior to installing add-ons when closing the add-on store dialog.
		installationPromptTitle = pgettext("addonStore", "Add-on installation")
		numInProgress = len(self._storeVM._downloader.progress)
		if numInProgress:
			res = gui.messageBox(
				# Translators: Message shown prior to installing add-ons when closing the add-on store dialog
				# The placeholder {} will be replaced with the number of add-ons to be installed
				pgettext("addonStore", "Download of {} add-ons in progress, cancel downloading?").format(
					numInProgress
				),
				installationPromptTitle,
				style=wx.YES_NO
			)
			if res == wx.YES:
				log.debug("Cancelling the download.")
				self._storeVM.cancelDownloads()
				# Continue to installation if any downloads completed
			else:
				# Let the user return to the add-on store and inspect add-ons being downloaded.
				return

		if self._storeVM._pendingInstalls:
			installingDialog = gui.IndeterminateProgressDialog(
				self,
				installationPromptTitle,
				# Translators: Message shown while installing add-ons after closing the add-on store dialog
				# The placeholder {} will be replaced with the number of add-ons to be installed
				pgettext("addonStore", "Installing {} add-ons, please wait.").format(len(self._storeVM._pendingInstalls))
			)
			self._storeVM.installPending()
			wx.CallAfter(installingDialog.done)
			addonGui.promptUserForRestart()
		
		requiresRestart = False
		for addonsForChannel in self._storeVM._installedAddons.values():
			for addon in addonsForChannel.values():
				if addon._addonHandlerModel.requiresRestart:
					log.debug(f"Add-on {addon.name} modified, restart required")
					requiresRestart = True
					break
			if requiresRestart:
				break

		if requiresRestart:
			addonGui.promptUserForRestart()

		# let the dialog exit.
		super().onClose(evt)

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
		return f"{self.title} - {self._listLabelText}"

	@property
	def _listLabelText(self) -> str:
		return f"{self._channelFilterKey.displayString} {self._statusFilterKey.displayString}"

	def _setListLabels(self):
		self.listLabel.SetLabelText(self._listLabelText)
		self.SetTitle(self._titleText)

	def _toggleFilterControls(self):
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
			self._storeVM._filterChannelKey = Channel.ALL
			self.enabledFilterCtrl.Show()
			self.enabledFilterCtrl.Enable()
			self.includeIncompatibleCtrl.Hide()
			self.includeIncompatibleCtrl.Disable()

	def onStatusFilterChange(self, evt: wx.EVT_CHOICE):
		self._storeVM._filterEnabledDisabled = EnabledStatus.ENABLED
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
		self._storeVM._filterEnabledDisabled = EnabledStatus.DISABLED if index else EnabledStatus.ENABLED
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
		if fd.ShowModal() != wx.ID_OK:
			return
		addonPath = fd.GetPath()
		try:
			addonGui.installAddon(self, addonPath)
		except DisplayableError as displayableError:
			callLater(delay=0, callable=self._storeVM.onDisplayableError.notify, displayableError=displayableError)
			return
		self._storeVM.refresh()
