# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import functools
from typing import (
	List,
	Optional,
	Callable,
	Dict,
)

import wx
import wx.lib.newevent
from wx.lib.expando import ExpandoTextCtrl

import gui
import winVersion
from gui import (
	guiHelper,
	nvdaControls,
	addonGui,
)
from gui.dpiScalingHelper import DpiScalingHelperMixinWithoutInit
from gui.settingsDialogs import SettingsDialog
from logHandler import log

from .viewModels import (
	AddonListVM,
	AddonDetailsVM,
	AddonListItemVM,
	AddonStoreVM,
	AddonActionVM,
	TranslatedError,
)


_fontFaceName = "Segoe UI"
_fontFaceName_semiBold = "Segoe UI Semibold"


class AddonVirtualList(
		nvdaControls.AutoWidthColumnListCtrl,
		DpiScalingHelperMixinWithoutInit,
):

	def __init__(self, parent, addonsListVM: AddonListVM, actionVMList: List[AddonActionVM]):
		super().__init__(
			parent,
			style=(
				wx.LC_REPORT  # Single or multicolumn report view, with optional header.
				| wx.LC_VIRTUAL  # The application provides items text on demand. May only be used with LC_REPORT.
				| wx.LC_SINGLE_SEL  # Single selection (default is multiple).
				| wx.LC_HRULES  # Draws light horizontal rules between rows in report mode.
				| wx.LC_VRULES  # Draws light vertical rules between columns in report mode.
			),
			autoSizeColumn=1,
		)

		self.SetMinSize(self.scaleSize((550, 600)))

		# Translators: The name of the column that contains names of addons. In the add-on store dialog.
		self.InsertColumn(0, pgettext("addonStore", "Name"))
		# Translators: The name of the column that contains the addons version string. In the add-on store dialog.
		self.InsertColumn(1, pgettext("addonStore", "Version"))
		# Translators: The name of the column that contains the addons publisher. In the add-on store dialog.
		self.InsertColumn(2, pgettext("addonStore", "Publisher"))
		self.InsertColumn(
			3,
			# Translators: The name of the column that contains the status of the addon (E.G. available, downloading
			# installing). In the add-on store dialog.
			pgettext("addonStore", "Status"),
			# Enough space for the longer contents, eg: "Installed, restart required"
			width=self.scaleSize(150)
		)

		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
		self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

		self._addonsListVM = addonsListVM
		self._actionVMList = actionVMList
		self._contextMenu = wx.Menu()
		self._actionMenuItemMap = {}
		self.Bind(event=wx.EVT_CONTEXT_MENU, handler=self._popupContextMenu)
		for action in self._actionVMList:
			menuItem: wx.MenuItem = self._contextMenu.Append(id=-1, item=action.displayName)
			self._actionMenuItemMap[action] = menuItem
			action.updated.register(self._updateContextMenuItem)
			self.Bind(
				event=wx.EVT_MENU,
				handler=functools.partial(self._menuItemClicked, actionVM=action),
				source=menuItem,
			)
			self._updateContextMenuItem(action)

		self.SetItemCount(addonsListVM.getCount())
		selIndex = self._addonsListVM.getSelectedIndex()
		if selIndex is not None:
			self.Select(selIndex)
			self.Focus(selIndex)
		self._addonsListVM.itemUpdated.register(self._itemDataUpdated)
		self._addonsListVM.updated.register(self._doRefresh)

	def _popupContextMenu(self, evt: wx.ContextMenuEvent):
		position = evt.GetPosition()
		firstSelectedIndex: int = self.GetFirstSelected()
		if firstSelectedIndex == -1:
			# context menu only valid on an item.
			return
		if position == wx.DefaultPosition:
			# keyboard triggered context menu (due to "applications" key)
			# don't have position set. It must be fetched from the selected item.
			itemRect: wx.Rect = self.GetItemRect(firstSelectedIndex)
			position: wx.Position = itemRect.GetBottomLeft()
			self.PopupMenu(self._contextMenu, position)
		else:
			# Mouse (right click) triggered context menu.
			# In this case the menu is positioned better with GetPopupMenuSelectionFromUser.
			self.GetPopupMenuSelectionFromUser(self._contextMenu)

	def _menuItemClicked(self, evt: wx.CommandEvent, actionVM: AddonActionVM):
		selectedAddon: AddonListItemVM = self._addonsListVM.getSelection()
		log.debug(f"evt {evt}, actionVM: {actionVM}, selectedAddon: {selectedAddon}")
		actionVM.actionHandler(selectedAddon)

	def _itemDataUpdated(self, index: int):
		log.debug(f"index: {index}")
		self.RefreshItem(index)

	def OnItemSelected(self, evt: wx.ListEvent):
		newIndex = evt.GetIndex()
		log.debug(f"item selected: {newIndex}")
		self._addonsListVM.setSelection(index=newIndex)

	def _updateContextMenuItem(self, addonActionVM: AddonActionVM):
		menuItem = self._actionMenuItemMap[addonActionVM]
		menuItem.Enable(enable=addonActionVM.isValid)

	# noinspection PyMethodMayBeStatic
	def OnItemActivated(self, evt: wx.ListEvent):
		activatedIndex = evt.GetIndex()
		log.debug(f"item activated: {activatedIndex}")

	def OnItemDeselected(self, evt: wx.ListEvent):
		log.debug(f"item deselected")
		self._addonsListVM.setSelection(None)

	def OnGetItemText(self, itemIndex: int, colIndex: int):
		dataItem = self._addonsListVM.getAddonAttrText(
			itemIndex,
			AddonListVM.presentedAttributes[colIndex]
		)
		if dataItem is None:
			# Failed to get dataItem, index may have been lost in refresh.
			return ''
		return str(dataItem)

	def OnColClick(self, evt: wx.ListEvent):
		colIndex = evt.GetColumn()
		log.debug(f"col clicked: {colIndex}")
		self._addonsListVM.setSortField(AddonListVM.presentedAttributes[colIndex])

	def _doRefresh(self):
		with guiHelper.autoThaw(self):
			newCount = self._addonsListVM.getCount()
			self.SetItemCount(newCount)
			self._refreshSelection()

	def _refreshSelection(self):
		selected = self.GetFirstSelected()
		newSelectedIndex = self._addonsListVM.getSelectedIndex()
		log.debug(f"_refreshSelection {newSelectedIndex}")
		if newSelectedIndex is not None:
			self.Select(newSelectedIndex)
			self.Focus(newSelectedIndex)
			# wx.ListCtrl doesn't send a selection event if the index hasn't changed,
			# however, the item at that index may have changed as a result of filtering.
			# To ensure parent dialogs are notified, explicitly send an event.
			if selected == newSelectedIndex:
				evt = wx.ListEvent(wx.wxEVT_LIST_ITEM_SELECTED, self.GetId())
				evt.SetIndex(newSelectedIndex)
				evt.SetClientObject(self._addonsListVM.getSelection())
				self.GetEventHandler().ProcessEvent(evt)
		elif newSelectedIndex is None:
			# wx.ListCtrl doesn't send a deselection event when the list is emptied.
			# To ensure parent dialogs are notified, explicitly send an event.
			self.Select(selected, on=0)
			evt = wx.ListEvent(wx.wxEVT_LIST_ITEM_DESELECTED, self.GetId())
			evt.SetIndex(-1)
			evt.SetClientObject(None)
			self.GetEventHandler().ProcessEvent(evt)


def _insertLinkForLabelWithTomViaComIDispatch(
		ctrl: wx.TextCtrl,
		labelText: str,
		linkText: str,
		url: str,
) -> None:
	""" Use Text Object model via COM IDispatch to insert a link at the end of the TextCtrl content.
	The underlying control must be a win32 RichEdit control, such as RichEdit50.
	Used because wx.TextCtrl does not expose adding URLs.

	@param ctrl: The control to work with.
	@param labelText: The label text to find and insert a link after.
	@param linkText: The text to append.
	@param url: The URL to link to.
	"""
	initialEditableState = ctrl.IsEditable()
	ctrl.SetEditable(True)
	import oleacc
	import winUser
	import comtypes.automation
	import comtypes.client
	import comInterfaces.tom
	hwnd = ctrl.GetHandle()
	obj = oleacc.AccessibleObjectFromWindow(
		hwnd,
		winUser.OBJID_NATIVEOM,
		interface=comtypes.automation.IDispatch
	)
	# No definitions available (in NVDA) for ITextRange2 interface, I.E. they are not in the msftedit type
	# library. Instead, use IDispatch.
	iTextDocument2_disp = comtypes.client.dynamic.Dispatch(obj)
	iTextRange2_disp = iTextDocument2_disp.range(0, 0)
	iTextRange2_disp.FindText(
		labelText,
		comInterfaces.tom.tomForward,
		comInterfaces.tom.tomMatchCase,
	)
	# move passed last character of the label string.
	iTextRange2_disp.moveEnd(comInterfaces.tom.tomCharacter, 1)
	iTextRange2_disp.collapse(comInterfaces.tom.tomEnd)
	iTextRange2_disp.text = linkText
	# URL must be wrapped in quote chars, see docs.microsoft.com: ITextRange2::SetURL method (tom.h)
	iTextRange2_disp.url = f'"{url}"'
	ctrl.SetEditable(initialEditableState)


class AddonDetails(
		wx.Panel,
		DpiScalingHelperMixinWithoutInit,
):
	# Translators: Header (usually the add-on name) when no add-on is selected. In the add-on store dialog.
	_noAddonSelectedLabelText: str = pgettext("addonStore", "No addon selected.")

	# Translators: Label for the text control containing a description of the selected add-on.
	# In the add-on store dialog.
	_descriptionLabelText: str = pgettext("addonStore", "Description:")

	def __init__(self, parent, actionVMList: List[AddonActionVM], detailsVM: AddonDetailsVM):
		self._detailsVM: AddonDetailsVM = detailsVM
		self._actionVMList = actionVMList
		wx.Panel.__init__(
			self,
			parent,
			style=wx.TAB_TRAVERSAL | wx.BORDER_THEME
		)

		sizer = wx.BoxSizer(orient=wx.VERTICAL)
		self.SetSizer(sizer)
		self.contents = wx.BoxSizer(orient=wx.VERTICAL)
		sizer.Add(
			self.contents,
			border=gui.guiHelper.BORDER_FOR_DIALOGS,
			proportion=1,  # make vertically stretchable
			flag=(
				wx.EXPAND  # make horizontally stretchable
				| wx.ALL  # and make border all around
			),
		)
		# To make the text fields less ugly.
		# See Windows explorer file properties dialog for an example.
		self.SetBackgroundColour(wx.Colour("white"))

		self.addonNameCtrl = wx.StaticText(
			self,
			label=AddonDetails._noAddonSelectedLabelText,
			style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ST_NO_AUTORESIZE
		)
		self._setAddonNameCtrlStyle()
		self.contents.Add(self.addonNameCtrl, flag=wx.EXPAND)

		self.contents.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)

		# It would be nice to override the name using wx.Accessible,
		# but using it on a TextCtrl breaks the accessibility of the control entirely (all state/role is reset)
		# Instead, add a hidden label for the textBox, Windows exposes this as the accessible name.
		self.descriptionLabel = wx.StaticText(
			self,
			label=AddonDetails._descriptionLabelText
		)
		self.contents.Add(self.descriptionLabel, flag=wx.EXPAND)
		self.descriptionLabel.Show(False)
		descriptionWidth = 500
		self.descriptionTextCtrl = ExpandoTextCtrl(
			self,
			size=(self.scaleSize(descriptionWidth), -1),
			style=(
				0  # purely to allow subsequent items to line up.
				| wx.TE_MULTILINE  # details will require multiple lines
				| wx.TE_READONLY  # the details shouldn't be user editable
				# Don't specify Auto-URL(wx.TE_AUTO_URL). No links expected in description, any URLs included
				# in an add-on release metadata submission should not be easily activated.
				| wx.BORDER_NONE
			)
		)
		self.contents.Add(self.descriptionTextCtrl, flag=wx.EXPAND)
		self.contents.Add(wx.StaticLine(self), flag=wx.EXPAND)

		self._actionButtonMap: Dict[AddonActionVM, wx.Button] = {}
		self._actionsSizer = self._createActionButtons()
		self.contents.Add(self._actionsSizer)

		self.contents.Add(wx.StaticLine(self), flag=wx.EXPAND)
		self.contents.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)

		# It would be nice to override the name using wx.Accessible,
		# but using it on a TextCtrl breaks the accessibility of the control entirely (all state/role is reset)
		# Instead, add a hidden label for the textBox, Windows exposes this as the accessible name.
		self.otherDetailsLabel = wx.StaticText(
			self,
			# Translators: Label for the text control containing extra details about the selected add-on.
			# In the add-on store dialog.
			label=pgettext("addonStore", "Other Details:")
		)
		self.contents.Add(self.otherDetailsLabel, flag=wx.EXPAND)
		self.otherDetailsLabel.Show(False)
		self.otherDetailsTextCtrl = wx.TextCtrl(
			self,
			size=self.scaleSize((descriptionWidth, 400)),
			style=(
				0  # purely to allow subsequent items to line up.
				| wx.TE_MULTILINE  # details will require multiple lines
				| wx.TE_READONLY  # the details shouldn't be user editable
				# wx.TE_AUTO_URL  # Don't specify Auto-URL, links should have names so create them Text Object Model.
				| wx.TE_RICH2
				| wx.TE_NO_VSCROLL  # No scroll by default.
				| wx.BORDER_NONE
			)
		)
		self._createRichTextStyles()
		self._urlQueue: List[Callable] = []
		self.contents.Add(self.otherDetailsTextCtrl, flag=wx.EXPAND, proportion=1)
		self._refresh()  # ensure that the visual state matches.
		self._detailsVM.updated.register(self._updatedListItem)

	def _createRichTextStyles(self):
		# Set up the text styles for the "other details" (which contains several fields)
		# Note, wx seems to merge text styles when using 'SetDefaultStyle',
		# so if color is used in one text attr, the others need to override it also.
		# If this isn't done and E.G. style1 doesn't specify color, style2 is blue, then
		# setting style1 as the default style will continue to result in blue text.
		self.defaultStyle = wx.TextAttr()
		self.defaultStyle.SetFontFaceName(_fontFaceName)
		self.defaultStyle.SetTextColour("black")
		self.defaultStyle.SetFontSize(10)

		self.labelStyle = wx.TextAttr(self.defaultStyle)
		# Note: setting font weight doesn't seem to work for RichText, instead specify via the font face name
		self.labelStyle.SetFontFaceName(_fontFaceName_semiBold)

		self.urlStyle = wx.TextAttr(self.defaultStyle)
		self.urlStyle.SetTextColour("blue")

	def _setAddonNameCtrlStyle(self):
		addonNameFont: wx.Font = self.addonNameCtrl.GetFont()
		addonNameFont.SetPointSize(18)
		# Note: setting font weight via the font face name doesn't seem to work on staticText
		# set explicitly using SetWeight
		addonNameFont.SetWeight(wx.FONTWEIGHT_BOLD)
		addonNameFont.SetFaceName(_fontFaceName)
		self.addonNameCtrl.SetFont(addonNameFont)
		self.addonNameCtrl.SetForegroundColour("white")
		nvdaPurple = wx.Colour((71, 47, 95))
		self.addonNameCtrl.SetBackgroundColour(nvdaPurple)

	def updateAddonName(self, displayName: str):
		self.addonNameCtrl.SetLabelText(displayName)

	def _updatedListItem(self, addonDetailsVM: AddonDetailsVM):
		log.debug(f"Setting listItem: {addonDetailsVM.listItem}")
		assert self._detailsVM.listItem == addonDetailsVM.listItem
		self._refresh()

	def _refresh(self):
		details = None if not self._detailsVM.listItem else self._detailsVM.listItem.model

		with guiHelper.autoThaw(self):
			# AppendText is used to build up the details so that formatting can be set as text is added, via
			# SetDefaultStyle, however, this means the text control must start empty.
			self.otherDetailsTextCtrl.SetValue("")
			if not details:
				text = AddonDetails._noAddonSelectedLabelText
				self.updateAddonName(text)
				self.descriptionTextCtrl.SetValue("")
				self.descriptionLabel.SetLabelText(AddonDetails._noAddonSelectedLabelText)
			else:
				log.debugWarning(f"URL queue len {len(self._urlQueue)}")
				self.updateAddonName(details.displayName)
				self.descriptionLabel.SetLabelText(AddonDetails._descriptionLabelText)

				# For a ExpandoTextCtr, SetDefaultStyle can not be used to set the style (along with the use
				# of AppendText) because AppendText has been overridden to use SetValue(GetValue()+newStr)
				# which drops formatting. Instead, set the text, then the style.
				self.descriptionTextCtrl.SetValue(details.description)
				self.descriptionTextCtrl.SetStyle(
					0,
					self.descriptionTextCtrl.GetLastPosition(),
					self.defaultStyle
				)

				self._appendDetailsLabelValue(
					# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
					pgettext("addonStore", "Publisher:"),
					details.publisher
				)
				self._appendDetailsLabelValue(
					# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
					pgettext("addonStore", "Version:"),
					details.addonVersionName
				)
				self._appendDetailsLabelValue(
					# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
					pgettext("addonStore", "Channel:"),
					details.channel
				)
				if details.homepage:
					self._appendDetailsLabelValue(
						# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
						pgettext("addonStore", "Homepage:"),
						details.homepage, URL=details.homepage
					)
				self._appendDetailsLabelValue(
					# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
					pgettext("addonStore", "License:"),
					details.license, URL=details.licenseURL
				)
				self._appendDetailsLabelValue(
					# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
					pgettext("addonStore", "Source Code:"),
					details.sourceURL, URL=details.sourceURL
				)

		self.otherDetailsTextCtrl.SetDefaultStyle(self.urlStyle)
		for urlFunc in self._urlQueue:
			urlFunc()
		self._urlQueue.clear()
		# Set caret/insertion point at the beginning so that NVDA users can more easily read from the start.
		self.otherDetailsTextCtrl.SetInsertionPoint(0)

	def _addDetailsLabel(self, label: str):
		detailsTextCtrl = self.otherDetailsTextCtrl
		detailsTextCtrl.SetDefaultStyle(self.labelStyle)
		detailsTextCtrl.AppendText(label)
		detailsTextCtrl.SetDefaultStyle(self.defaultStyle)

	def _appendDetailsLabelValue(self, label: str, value: str, URL: Optional[str] = None):
		detailsTextCtrl = self.otherDetailsTextCtrl

		if detailsTextCtrl.GetValue():
			detailsTextCtrl.AppendText('\n')

		self._addDetailsLabel(label)
		labelSpace = " "  # em space, wider than regular space, for visual layout.

		if URL:
			if winVersion.getWinVer() < winVersion.WIN8:
				# ITextRange2 is not available before Windows 8, instead just insert the URL as text
				detailsTextCtrl.SetDefaultStyle(self.defaultStyle)
				detailsTextCtrl.AppendText(labelSpace)
				detailsTextCtrl.AppendText(value)
				if value != URL:  # don't insert the URL twice.
					detailsTextCtrl.AppendText(f" ({URL})")
			else:
				detailsTextCtrl.SetDefaultStyle(self.urlStyle)
				detailsTextCtrl.AppendText(labelSpace)
				self._urlQueue.append(
					lambda: _insertLinkForLabelWithTomViaComIDispatch(detailsTextCtrl, label, value, URL)
				)
		else:
			detailsTextCtrl.SetDefaultStyle(self.defaultStyle)
			detailsTextCtrl.AppendText(labelSpace)
			detailsTextCtrl.AppendText(value)

	def _createActionButtons(self) -> wx.BoxSizer:
		_actionsSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

		def _makeButtonClickedEventHandler(_action: AddonActionVM) -> Callable[[wx.CommandEvent, ], None]:
			"""Get around python binding to the latest value in a for loop, create a new lambda
			for each value with an explicit binding to the addon details.
			"""
			# evt: wx.CommandEvent
			return lambda evt: _action.actionHandler(self._detailsVM.listItem)

		for action in self._actionVMList:
			button = wx.Button(parent=self, label=action.displayName)
			_actionsSizer.Add(button)

			button.Bind(
				event=wx.EVT_BUTTON,
				handler=_makeButtonClickedEventHandler(action)
			)
			button.Enable(enable=action.isValid)
			action.updated.register(self._actionVmChanged)
			self._actionButtonMap[action] = button
		return _actionsSizer

	def _actionVmChanged(self, addonActionVM: AddonActionVM):
		self._actionButtonMap[addonActionVM].Enable(enable=addonActionVM.isValid)


def displayError(error: TranslatedError):
	gui.messageBox(
		error.displayMessage,
		# Translators: The title of a dialog presented when an error occurs.
		pgettext("addonStore", "Error"),
		wx.OK | wx.ICON_ERROR
	)


class AddonStoreDialog(SettingsDialog):
	# Translators: The title of the addonStore dialog where the user can find and download add-ons
	title = pgettext("addonStore", "Add-on Store")
	helpId = "addonStore"

	def __init__(self, parent: wx.Window, storeVM: AddonStoreVM):
		self._storeVM = storeVM
		self._storeVM.hasError.register(displayError)
		super().__init__(parent, resizeable=True)

	def makeSettings(self, settingsSizer):
		# Translators: The label of a text field to filter the list of add-ons in the add-on store dialog.
		filterLabel = wx.StaticText(self, label=pgettext("addonStore", "&Filter by:"))
		# noinspection PyAttributeOutsideInit
		self.filterCtrl = filterCtrl = wx.TextCtrl(self)
		filterCtrl.Bind(wx.EVT_TEXT, self.onFilterChange, filterCtrl)

		filterSizer = wx.BoxSizer(wx.HORIZONTAL)
		filterSizer.Add(filterLabel, flag=wx.ALIGN_CENTER_VERTICAL)
		filterSizer.AddSpacer(guiHelper.SPACE_BETWEEN_ASSOCIATED_CONTROL_HORIZONTAL)
		filterSizer.Add(filterCtrl, proportion=1)
		settingsSizer.Add(filterSizer, flag=wx.EXPAND)

		settingsSizer.AddSpacer(5)

		# noinspection PyAttributeOutsideInit
		self.contentsSizer = wx.BoxSizer(wx.HORIZONTAL)
		settingsSizer.Add(self.contentsSizer, flag=wx.EXPAND, proportion=1)

		# add a label for the AddonListVM so that it is announced with a name in NVDA
		listLabel = wx.StaticText(
			self,
			# Translators: Label for the list of available add-ons. In the add-on store dialog.
			label=pgettext("addonStore", "Available Add-ons:")
		)
		self.contentsSizer.Add(
			listLabel,
			flag=wx.EXPAND
		)
		listLabel.Show(False)

		# noinspection PyAttributeOutsideInit
		self.addonListView = AddonVirtualList(
			parent=self,
			addonsListVM=self._storeVM.listVM,
			actionVMList=self._storeVM.actionVMList,
		)
		self.contentsSizer.Add(self.addonListView, flag=wx.EXPAND)
		self.contentsSizer.AddSpacer(5)
		# noinspection PyAttributeOutsideInit
		self.addonDetailsView = AddonDetails(
			parent=self,
			actionVMList=self._storeVM.actionVMList,
			detailsVM=self._storeVM.detailsVM,
		)
		self.contentsSizer.Add(self.addonDetailsView, flag=wx.EXPAND, proportion=1)

	def postInit(self):
		self.addonListView.SetFocus()

	def _onWindowDestroy(self, evt: wx.WindowDestroyEvent):
		super()._onWindowDestroy(evt)

	def onOk(self, evt: wx.CommandEvent):
		# Translators: Title for message shown prior to installing add-ons when closing the add-on store dialog.
		installationPromptTitle = _("Add-on installation")
		numInProgress = len(self._storeVM._downloader.progress)
		if numInProgress:
			res = gui.messageBox(
				# Translators: Message shown prior to installing add-ons when closing the add-on store dialog
				# The placeholder {} will be replaced with the number of add-ons to be installed
				_("Download of {} add-ons in progress, cancel downloading?").format(
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
			gui.messageBox(
				# Translators: Message shown prior to installing add-ons when closing the add-on store dialog
				# The placeholder {} will be replaced with the number of add-ons to be installed
				_("Now installing {} add-ons.").format(len(self._storeVM._pendingInstalls)),
				installationPromptTitle
			)
			self._storeVM.installPending()
			addonGui.promptUserForRestart()

		# let the dialog exit.
		super().onOk(evt)

	def onFilterChange(self, evt):
		filterText = evt.GetEventObject().GetValue()
		self.filter(filterText)

	def filter(self, filterText: str):
		self._storeVM.listVM.applyFilter(filterText)
