# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	List,
	Optional,
	Callable,
)

import wx
import wx.lib.newevent
from wx.lib.expando import ExpandoTextCtrl

import gui
from gui import guiHelper, nvdaControls, DpiScalingHelperMixinWithoutInit
from gui.settingsDialogs import SettingsDialog
from logHandler import log

from addonStore.dataManager import (
	DataManager,
)

from .viewModels import (
	AddonListVM,
	AddonDetailsVM,
	AddonDetailsModel,
	AddonStoreVM,
)


_fontFaceName = "Segoe UI"
_fontFaceName_semiBold = "Segoe UI Semibold"


class AddonVirtualList(
		nvdaControls.AutoWidthColumnListCtrl,
		DpiScalingHelperMixinWithoutInit,
):

	def __init__(self, parent, addonsListVM: AddonListVM):
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

		self.SetMinSize(self.scaleSize((400, 600)))
		self._addonsListVM = addonsListVM
		self.SetItemCount(addonsListVM.getCount())

		# Translators: The name of the column that contains names of addons. In the add-on store dialog.
		self.InsertColumn(0, pgettext("addonStore", "Name"))
		# Translators: The name of the column that contains the addons version string. In the add-on store dialog.
		self.InsertColumn(1, pgettext("addonStore", "Version"))
		# Translators: The name of the column that contains the addons publisher. In the add-on store dialog.
		self.InsertColumn(2, pgettext("addonStore", "Publisher"))

		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
		self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

		selIndex = self._addonsListVM.getSelectedIndex()
		if selIndex is not None:
			self.Select(selIndex)
			self.Focus(selIndex)

	def OnItemSelected(self, evt: wx.ListEvent):
		newIndex = evt.GetIndex()
		log.debug(f"item selected: {newIndex}")
		addonItem = self._addonsListVM.setSelection(index=newIndex)
		evt.SetClientObject(addonItem)
		evt.Skip()  # Let other handlers know about the change in selection.

	def OnItemActivated(self, evt: wx.ListEvent):
		activatedIndex = evt.GetIndex()
		log.debug(f"item activated: {activatedIndex}")

	def OnItemDeselected(self, evt: wx.ListEvent):
		log.debug(f"item deselected")
		self._addonsListVM.setSelection(None)
		evt.SetClientObject(None)
		evt.Skip()  # Let other handlers know about the deselection.

	def OnGetItemText(self, itemIndex: int, colIndex: int):
		dataItem = self._addonsListVM.getAddonAttrText(
			itemIndex,
			AddonListVM.presentedAttributes[colIndex]
		)
		return str(dataItem)

	def OnColClick(self, evt: wx.ListEvent):
		colIndex = evt.GetColumn()
		log.debug(f"col clicked: {colIndex}")
		self._addonsListVM.setSortField(AddonListVM.presentedAttributes[colIndex])
		self.doRefresh()

	def doRefresh(self):
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

	def __init__(self, parent, detailsVM: AddonDetailsVM):
		self.detailsVM = detailsVM
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

		self.descriptionTextCtrl = ExpandoTextCtrl(
			self,
			size=(self.scaleSize(400), -1),
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
			size=self.scaleSize((400, 400)),
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

	def setAddonDetail(self, detailsVM: AddonDetailsVM):
		log.debug(f"Setting addon: {detailsVM.getAddonId()}")
		if (
			self.detailsVM == detailsVM  # both may be same ref or None
			or self.detailsVM.getAddonId() == detailsVM.getAddonId()  # confirm with addonId
		):
			# already set, exit early
			return
		self.detailsVM = detailsVM
		self._refresh()

	def _refresh(self):
		details = self.detailsVM.display

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
					details.versionName
				)
				self._appendDetailsLabelValue(
					# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
					pgettext("addonStore", "Channel:"),
					details.channel
				)
				self._appendDetailsLabelValue(
					# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
					pgettext("addonStore", "Homepage:"),
					details.homepage, URL=details.homepage
				)
				self._appendDetailsLabelValue(
					# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
					pgettext("addonStore", "License:"),
					details.licenseName, URL=details.licenseUrl
				)
				self._appendDetailsLabelValue(
					# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
					pgettext("addonStore", "Source Code:"),
					details.sourceUrl, URL=details.sourceUrl
				)

		self.otherDetailsTextCtrl.SetDefaultStyle(self.urlStyle)
		for urlFunc in self._urlQueue:
			urlFunc()
		self._urlQueue.clear()
		# Set caret/insertion point at the beginning so that NVDA users can more easily read from the start.
		self.otherDetailsTextCtrl.SetInsertionPoint(0)

	def _addDetailsLabel(self, label):
		detailsTextCtrl = self.otherDetailsTextCtrl
		detailsTextCtrl.SetDefaultStyle(self.labelStyle)
		detailsTextCtrl.AppendText(label)
		detailsTextCtrl.SetDefaultStyle(self.defaultStyle)

	def _appendDetailsLabelValue(self, label, value, URL: Optional[str] = None):
		detailsTextCtrl = self.otherDetailsTextCtrl

		if detailsTextCtrl.GetValue():
			detailsTextCtrl.AppendText('\n')

		self._addDetailsLabel(label)
		labelSpace = " "  # em space, wider than regular space, for visual layout.

		if URL:
			detailsTextCtrl.SetDefaultStyle(self.urlStyle)
			detailsTextCtrl.AppendText(labelSpace)
			self._urlQueue.append(
				lambda: _insertLinkForLabelWithTomViaComIDispatch(detailsTextCtrl, label, value, URL)
			)
		else:
			detailsTextCtrl.SetDefaultStyle(self.defaultStyle)
			detailsTextCtrl.AppendText(labelSpace)
			detailsTextCtrl.AppendText(value)


class AddonStoreDialog(SettingsDialog):
	# Translators: The title of the addonStore dialog where the user can find and download add-ons
	title = pgettext("addonStore", "Add-on Store")
	helpId = "addonStore"

	def __init__(self, parent: wx.Window, addonDataManager: DataManager):
		self._addonDataManager = addonDataManager
		self._storeVM = AddonStoreVM(
			availableAddonsModel=addonDataManager.getLatestAvailableAddons()
		)
		super().__init__(parent, resizeable=True)

	def makeSettings(self, settingsSizer):
		# Translators: The label of a text field to filter the list of add-ons in the add-on store dialog.
		filterLabel = wx.StaticText(self, label=pgettext("addonStore", "&Filter by:"))
		self.filterCtrl = filterCtrl = wx.TextCtrl(self)
		filterCtrl.Bind(wx.EVT_TEXT, self.onFilterChange, filterCtrl)

		filterSizer = wx.BoxSizer(wx.HORIZONTAL)
		filterSizer.Add(filterLabel, flag=wx.ALIGN_CENTER_VERTICAL)
		filterSizer.AddSpacer(guiHelper.SPACE_BETWEEN_ASSOCIATED_CONTROL_HORIZONTAL)
		filterSizer.Add(filterCtrl, proportion=1)
		settingsSizer.Add(filterSizer, flag=wx.EXPAND)

		settingsSizer.AddSpacer(5)

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

		self.addonListVM = AddonListVM(
			addonsModel=self._storeVM.availableAddonsModel
		)
		self.addonListView = AddonVirtualList(
			parent=self,
			addonsListVM=self.addonListVM
		)
		self.Bind(
			wx.EVT_LIST_ITEM_SELECTED,
			lambda evt: self.onAddonSelect(evt.GetClientObject()),
		)
		self.Bind(
			wx.EVT_LIST_ITEM_DESELECTED,
			lambda evt: self.onAddonSelect(evt.GetClientObject()),
		)
		self.contentsSizer.Add(self.addonListView, flag=wx.EXPAND)
		self.contentsSizer.AddSpacer(5)
		self.addonDetailsView = AddonDetails(
			parent=self,
			detailsVM=AddonDetailsVM(display=None)
		)
		self.contentsSizer.Add(self.addonDetailsView, flag=wx.EXPAND, proportion=1)

	def postInit(self):
		self.addonListView.SetFocus()

	def _onWindowDestroy(self, evt: wx.WindowDestroyEvent):
		super()._onWindowDestroy(evt)

	def onFilterChange(self, evt):
		filterText = evt.GetEventObject().GetValue()
		self.filter(filterText)

	def filter(self, filterText: str):
		self.addonListVM.applyFilter(filterText)
		self.addonListView.doRefresh()

	def onAddonSelect(self, addonModel: AddonDetailsModel):
		log.debug(f"selected: {addonModel}")
		self.addonDetailsView.setAddonDetail(AddonDetailsVM(display=addonModel))
