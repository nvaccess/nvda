# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2024 NV Access Limited, Peter Vágner, Aleksey Sadovoy,
# Rui Batista, Joseph Lee, Heiko Folkerts, Zahari Yurukov, Leonard de Ruijter,
# Derek Riemer, Babbage B.V., Davy Kager, Ethan Holliger, Bill Dengler, Thomas Stivers,
# Julien Cochuyt, Peter Vágner, Cyrille Bougot, Mesar Hameed, Łukasz Golonka, Aaron Cannon,
# Adriani90, André-Abush Clause, Dawid Pieper, Heiko Folkerts, Takuya Nishimoto, Thomas Stivers,
# jakubl7545, mltony, Rob Meredith, Burman's Computer and Education Ltd, hwf1324.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import logging
from abc import ABCMeta, abstractmethod
import copy
import os
from enum import IntEnum
from locale import strxfrm
import re
import typing
import wx
from NVDAState import WritePaths

from vision.providerBase import VisionEnhancementProviderSettings
from wx.lib.expando import ExpandoTextCtrl
import wx.lib.newevent
import winUser
import logHandler
import installer
from synthDriverHandler import changeVoice, getSynth, getSynthList, setSynth, SynthDriver
import config
from config.configFlags import (
	AddonsAutomaticUpdate,
	NVDAKey,
	ShowMessages,
	TetherTo,
	ParagraphStartMarker,
	ReportLineIndentation,
	ReportTableHeaders,
	ReportCellBorders,
	OutputMode,
)
import languageHandler
import speech
import systemUtils
import gui
import gui.contextHelp
import globalVars
from logHandler import log
import nvwave
import audio
import audioDucking
import queueHandler
import braille
import brailleTables
import brailleInput
import vision
import vision.providerInfo
import vision.providerBase
from typing import (
	Any,
	Callable,
	List,
	Optional,
	Set,
	cast,
)
from url_normalize import url_normalize
import core
import keyboardHandler
import characterProcessing
from . import guiHelper

try:
	import updateCheck
except RuntimeError:
	updateCheck = None
from . import nvdaControls
from autoSettingsUtils.utils import UnsupportedConfigParameterError
from autoSettingsUtils.autoSettings import AutoSettings
from autoSettingsUtils.driverSetting import BooleanDriverSetting, NumericDriverSetting, DriverSetting
import touchHandler
import winVersion
import weakref
import time
from .dpiScalingHelper import DpiScalingHelperMixinWithoutInit

#: The size that settings panel text descriptions should be wrapped at.
# Ensure self.scaleSize is used to adjust for OS scaling adjustments.
PANEL_DESCRIPTION_WIDTH = 544


class SettingsDialog(
	DpiScalingHelperMixinWithoutInit,
	gui.contextHelp.ContextHelpMixin,
	wx.Dialog,  # wxPython does not seem to call base class initializer, put last in MRO
	metaclass=guiHelper.SIPABCMeta,
):
	"""A settings dialog.
	A settings dialog consists of one or more settings controls and OK and Cancel buttons and an optional Apply button.
	Action may be taken in response to the OK, Cancel or Apply buttons.

	To use this dialog:
		* Set L{title} to the title of the dialog.
		* Override L{makeSettings} to populate a given sizer with the settings controls.
		* Optionally, override L{postInit} to perform actions after the dialog is created, such as setting the focus. Be
			aware that L{postInit} is also called by L{onApply}.
		* Optionally, extend one or more of L{onOk}, L{onCancel} or L{onApply} to perform actions in response to the
			OK, Cancel or Apply buttons, respectively.

	@ivar title: The title of the dialog.
	@type title: str
	"""

	class MultiInstanceError(RuntimeError):
		pass

	class MultiInstanceErrorWithDialog(MultiInstanceError):
		dialog: "SettingsDialog"

		def __init__(self, dialog: "SettingsDialog", *args: object) -> None:
			self.dialog = dialog
			super().__init__(*args)

	class DialogState(IntEnum):
		CREATED = 0
		DESTROYED = 1

	# holds instances of SettingsDialogs as keys, and state as the value
	_instances = weakref.WeakKeyDictionary()
	title = ""
	helpId = "NVDASettings"
	shouldSuspendConfigProfileTriggers = True

	def __new__(cls, *args, **kwargs):
		# We are iterating over instanceItems only once, so it can safely be an iterator.
		instanceItems = SettingsDialog._instances.items()
		instancesOfSameClass = ((dlg, state) for dlg, state in instanceItems if isinstance(dlg, cls))
		firstMatchingInstance, state = next(instancesOfSameClass, (None, None))
		multiInstanceAllowed = kwargs.get("multiInstanceAllowed", False)
		if log.isEnabledFor(log.DEBUG):
			instancesState = dict(SettingsDialog._instances)
			log.debug(
				"Creating new settings dialog (multiInstanceAllowed:{}). " "State of _instances {!r}".format(
					multiInstanceAllowed,
					instancesState,
				),
			)
		if state is cls.DialogState.CREATED and not multiInstanceAllowed:
			raise SettingsDialog.MultiInstanceErrorWithDialog(
				firstMatchingInstance,
				"Only one instance of SettingsDialog can exist at a time",
			)
		if state is cls.DialogState.DESTROYED and not multiInstanceAllowed:
			# The dialog has been destroyed by wx, but the instance is still available.
			# This indicates there is something keeping it alive.
			raise RuntimeError(
				f"Cannot open new settings dialog while instance still exists: {firstMatchingInstance!r}",
			)
		obj = super().__new__(cls, *args, **kwargs)
		SettingsDialog._instances[obj] = cls.DialogState.CREATED
		return obj

	def _setInstanceDestroyedState(self):
		# prevent race condition with object deletion
		# prevent deletion of the object while we work on it.
		nonWeak: typing.Dict[SettingsDialog, SettingsDialog.DialogState] = dict(SettingsDialog._instances)

		if (
			self in SettingsDialog._instances
			# Because destroy handlers are use evt.skip, _setInstanceDestroyedState may be called many times
			# prevent noisy logging.
			and self.DialogState.DESTROYED != SettingsDialog._instances[self]
		):
			if log.isEnabledFor(log.DEBUG):
				instanceStatesGen = (
					f"{instance.title} - {state.name}" for instance, state in nonWeak.items()
				)
				instancesList = list(instanceStatesGen)
				log.debug(
					f"Setting state to destroyed for instance: {self.title} - {self.__class__.__qualname__} - {self}\n"
					f"Current _instances {instancesList}",
				)
			SettingsDialog._instances[self] = self.DialogState.DESTROYED

	def __init__(
		self,
		parent: wx.Window,
		resizeable: bool = False,
		hasApplyButton: bool = False,
		settingsSizerOrientation: int = wx.VERTICAL,
		multiInstanceAllowed: bool = False,
		buttons: Set[int] = {wx.OK, wx.CANCEL},
	):
		"""
		@param parent: The parent for this dialog; C{None} for no parent.
		@param resizeable: True if the settings dialog should be resizable by the user, only set this if
			you have tested that the components resize correctly.
		@param hasApplyButton: C{True} to add an apply button to the dialog; defaults to C{False} for backwards compatibility.
			Deprecated, use buttons instead.
		@param settingsSizerOrientation: Either wx.VERTICAL or wx.HORIZONTAL. This controls the orientation of the
			sizer that is passed into L{makeSettings}. The default is wx.VERTICAL.
		@param multiInstanceAllowed: Whether multiple instances of SettingsDialog may exist.
			Note that still only one instance of a particular SettingsDialog subclass may exist at one time.
		@param buttons: Buttons to add to the settings dialog.
			Should be a subset of {wx.OK, wx.CANCEL, wx.APPLY, wx.CLOSE}.
		"""
		if gui._isDebug():
			startTime = time.time()
		windowStyle = wx.DEFAULT_DIALOG_STYLE
		if resizeable:
			windowStyle |= wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX
		super().__init__(parent, title=self.title, style=windowStyle)

		buttonFlag = 0
		for button in buttons:
			buttonFlag |= button
		if hasApplyButton:
			log.debugWarning(
				"The hasApplyButton parameter is deprecated. " "Use buttons instead. ",
			)
			buttonFlag |= wx.APPLY
		self.hasApply = hasApplyButton or wx.APPLY in buttons
		if not buttons.issubset({wx.OK, wx.CANCEL, wx.APPLY, wx.CLOSE}):
			log.error(f"Unexpected buttons set provided: {buttons}")

		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.settingsSizer = wx.BoxSizer(settingsSizerOrientation)
		self.makeSettings(self.settingsSizer)

		self.mainSizer.Add(
			self.settingsSizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL | wx.EXPAND,
			proportion=1,
		)
		self.mainSizer.Add(
			self.CreateSeparatedButtonSizer(buttonFlag),
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT,
		)

		self.mainSizer.Fit(self)
		self.SetSizer(self.mainSizer)

		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		self.Bind(wx.EVT_BUTTON, self.onClose, id=wx.ID_CLOSE)
		self.Bind(wx.EVT_BUTTON, self.onApply, id=wx.ID_APPLY)
		self.Bind(wx.EVT_CHAR_HOOK, self._enterActivatesOk_ctrlSActivatesApply)
		# Garbage collection normally handles removing the settings instance, however this may not happen immediately
		# after a window is closed, or may be blocked by a circular reference. So instead, remove when the window is
		# destroyed.
		self.Bind(wx.EVT_WINDOW_DESTROY, self._onWindowDestroy)

		self.postInit()
		if resizeable:
			self.SetMinSize(self.mainSizer.GetMinSize())
		self.CentreOnScreen()
		if gui._isDebug():
			log.debug("Loading %s took %.2f seconds" % (self.__class__.__name__, time.time() - startTime))

	def _enterActivatesOk_ctrlSActivatesApply(self, evt):
		"""Listens for keyboard input and triggers ok button on enter and triggers apply button when control + S is
		pressed. Cancel behavior is built into wx.
		Pressing enter will also close the dialog when a list has focus
		(e.g. the list of symbols in the symbol pronunciation dialog).
		Without this custom handler, enter would propagate to the list control (wx ticket #3725).
		"""
		if evt.KeyCode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
			self.ProcessEvent(wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK))
		elif self.hasApply and evt.UnicodeKey == ord("S") and evt.controlDown:
			self.ProcessEvent(wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_APPLY))
		else:
			evt.Skip()

	@abstractmethod
	def makeSettings(self, sizer):
		"""Populate the dialog with settings controls.
		Subclasses must override this method.
		@param sizer: The sizer to which to add the settings controls.
		@type sizer: wx.Sizer
		"""
		raise NotImplementedError

	def postInit(self):
		"""Called after the dialog has been created.
		For example, this might be used to set focus to the desired control.
		Sub-classes may override this method.
		"""

	def onOk(self, evt: wx.CommandEvent):
		"""Take action in response to the OK button being pressed.
		Sub-classes may extend this method.
		This base method should always be called to clean up the dialog.
		"""
		self.DestroyLater()
		self.SetReturnCode(wx.ID_OK)

	def onCancel(self, evt: wx.CommandEvent):
		"""Take action in response to the Cancel button being pressed.
		Sub-classes may extend this method.
		This base method should always be called to clean up the dialog.
		"""
		self.DestroyLater()
		self.SetReturnCode(wx.ID_CANCEL)

	def onClose(self, evt: wx.CommandEvent):
		"""Take action in response to the Close button being pressed.
		Sub-classes may extend this method.
		This base method should always be called to clean up the dialog.
		"""
		self.DestroyLater()
		self.SetReturnCode(wx.ID_CLOSE)

	def onApply(self, evt: wx.CommandEvent):
		"""Take action in response to the Apply button being pressed.
		Sub-classes may extend or override this method.
		This base method should be called to run the postInit method.
		"""
		self.postInit()
		self.SetReturnCode(wx.ID_APPLY)

	def _onWindowDestroy(self, evt: wx.WindowDestroyEvent):
		# Destroy events are sent to parent windows for handling.
		# If a child window is being destroyed, we don't want to
		# set this object as destroyed.
		# The ExpandoTextCtrl creates a destroy event as part of
		# initialization, this caused the NVDASettings dialog
		# to be incorrectly set to destroyed, causing #12818.
		isSelfAlive = bool(self)
		if not isSelfAlive:
			evt.Skip()
			self._setInstanceDestroyedState()


# An event and event binder that will notify the containers that they should
# redo the layout in whatever way makes sense for their particular content.
_RWLayoutNeededEvent, EVT_RW_LAYOUT_NEEDED = wx.lib.newevent.NewCommandEvent()


class SettingsPanel(
	DpiScalingHelperMixinWithoutInit,
	gui.contextHelp.ContextHelpMixin,
	wx.Panel,  # wxPython does not seem to call base class initializer, put last in MRO
	metaclass=guiHelper.SIPABCMeta,
):
	"""A settings panel, to be used in a multi category settings dialog.
	A settings panel consists of one or more settings controls.
	Action may be taken in response to the parent dialog's OK or Cancel buttons.

	To use this panel:
		* Set L{title} to the title of the category.
		* Override L{makeSettings} to populate a given sizer with the settings controls.
		* Optionally, extend L{onPanelActivated} to perform actions after the category has been selected in the list of categories, such as synthesizer or braille display list population.
		* Optionally, extend L{onPanelDeactivated} to perform actions after the category has been deselected (i.e. another category is selected) in the list of categories.
		* Optionally, extend one or both of L{onSave} or L{onDiscard} to perform actions in response to the parent dialog's OK or Cancel buttons, respectively.
		* Optionally, extend one or both of L{isValid} or L{postSave} to perform validation before or steps after saving, respectively.

	@ivar title: The title of the settings panel, also listed in the list of settings categories.
	@type title: str
	"""

	title = ""
	panelDescription = ""

	def __init__(self, parent: wx.Window):
		"""
		@param parent: The parent for this panel; C{None} for no parent.
		"""
		if gui._isDebug():
			startTime = time.time()
		super().__init__(parent)

		self._buildGui()

		if gui._isDebug():
			elapsedSeconds = time.time() - startTime
			panelName = self.__class__.__qualname__
			log.debug(f"Loading {panelName} took {elapsedSeconds:.2f} seconds")

	def _buildGui(self):
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.settingsSizer = wx.BoxSizer(wx.VERTICAL)
		self.makeSettings(self.settingsSizer)
		self.mainSizer.Add(self.settingsSizer, flag=wx.ALL | wx.EXPAND)
		self.mainSizer.Fit(self)
		self.SetSizer(self.mainSizer)

	@abstractmethod
	def makeSettings(self, sizer: wx.BoxSizer):
		"""Populate the panel with settings controls.
		Subclasses must override this method.
		@param sizer: The sizer to which to add the settings controls.
		"""
		raise NotImplementedError

	def onPanelActivated(self):
		"""Called after the panel has been activated (i.e. de corresponding category is selected in the list of categories).
		For example, this might be used for resource intensive tasks.
		Sub-classes should extend this method.
		"""
		self.Show()

	def onPanelDeactivated(self):
		"""Called after the panel has been deactivated (i.e. another category has been selected in the list of categories).
		Sub-classes should extendthis method.
		"""
		self.Hide()

	@abstractmethod
	def onSave(self):
		"""Take action in response to the parent's dialog OK or apply button being pressed.
		Sub-classes should override this method.
		MultiCategorySettingsDialog is responsible for cleaning up the panel when OK is pressed.
		"""
		raise NotImplementedError

	def isValid(self) -> bool:
		"""Evaluate whether the current circumstances of this panel are valid
		and allow saving all the settings in a L{MultiCategorySettingsDialog}.
		Sub-classes may extend this method.
		@returns: C{True} if validation should continue,
			C{False} otherwise.
		"""
		return True

	def _validationErrorMessageBox(
		self,
		message: str,
		option: str,
		category: Optional[str] = None,
	):
		if category is None:
			category = self.title
		gui.messageBox(
			message=_(
				# Translators: Content of the message displayed when a validation error occurs in the settings dialog
				"{message}\n" "\n" 'Category: "{category}"\n' 'Option: "{option}"',
			).format(
				message=message,
				category=category,
				option=option,
			),
			# Translators: The title of the message box when a setting's configuration is not valid.
			caption=_("Invalid configuration"),
			style=wx.OK | wx.ICON_ERROR,
			parent=self,
		)

	def postSave(self):
		"""Take action whenever saving settings for all panels in a L{MultiCategorySettingsDialog} succeeded.
		Sub-classes may extend this method.
		"""

	def onDiscard(self):
		"""Take action in response to the parent's dialog Cancel button being pressed.
		Sub-classes may override this method.
		MultiCategorySettingsDialog is responsible for cleaning up the panel when Cancel is pressed.
		"""

	def _sendLayoutUpdatedEvent(self):
		"""Notify any wx parents that may be listening that they should redo their layout in whatever way
		makes sense for them. It is expected that sub-classes call this method in response to changes in
		the number of GUI items in their panel.
		"""
		event = _RWLayoutNeededEvent(self.GetId())
		event.SetEventObject(self)
		self.GetEventHandler().ProcessEvent(event)


class SettingsPanelAccessible(wx.Accessible):
	"""
	WX Accessible implementation to set the role of a settings panel to property page,
	as well as to set the accessible description based on the panel's description.
	"""

	Window: SettingsPanel

	def GetRole(self, childId):
		return (wx.ACC_OK, wx.ROLE_SYSTEM_PROPERTYPAGE)

	def GetDescription(self, childId):
		return (wx.ACC_OK, self.Window.panelDescription)


class MultiCategorySettingsDialog(SettingsDialog):
	"""A settings dialog with multiple settings categories.
	A multi category settings dialog consists of a list view with settings categories on the left side,
	and a settings panel on the right side of the dialog.
	Furthermore, in addition to Ok and Cancel buttons, it has an Apply button by default,
	which is different  from the default behavior of L{SettingsDialog}.

	To use this dialog: set title and populate L{categoryClasses} with subclasses of SettingsPanel.
	Make sure that L{categoryClasses} only  contains panels that are available on a particular system.
	For example, if a certain category of settings is only supported on Windows 10 and higher,
	that category should be left out of L{categoryClasses}
	"""

	title = ""
	categoryClasses: typing.List[typing.Type[SettingsPanel]] = []

	class CategoryUnavailableError(RuntimeError):
		pass

	def __init__(self, parent, initialCategory=None):
		"""
		@param parent: The parent for this dialog; C{None} for no parent.
		@type parent: wx.Window
		@param initialCategory: The initial category to select when opening this dialog
		@type parent: SettingsPanel
		"""
		if initialCategory and not issubclass(initialCategory, SettingsPanel):
			if gui._isDebug():
				log.debug("Unable to open category: {}".format(initialCategory), stack_info=True)
			raise TypeError("initialCategory should be an instance of SettingsPanel")
		if initialCategory and initialCategory not in self.categoryClasses:
			if gui._isDebug():
				log.debug("Unable to open category: {}".format(initialCategory), stack_info=True)
			raise MultiCategorySettingsDialog.CategoryUnavailableError(
				"The provided initial category is not a part of this dialog",
			)
		self.initialCategory = initialCategory
		self.currentCategory = None
		self.setPostInitFocus = None
		# dictionary key is index of category in self.catList, value is the instance.
		# Partially filled, check for KeyError
		self.catIdToInstanceMap: typing.Dict[int, SettingsPanel] = {}

		super(MultiCategorySettingsDialog, self).__init__(
			parent,
			resizeable=True,
			settingsSizerOrientation=wx.HORIZONTAL,
			buttons={wx.OK, wx.CANCEL, wx.APPLY},
		)

		# setting the size must be done after the parent is constructed.
		self.SetMinSize(self.scaleSize(self.MIN_SIZE))
		self.SetSize(self.scaleSize(self.INITIAL_SIZE))
		# the size has changed, so recenter on the screen
		self.CentreOnScreen()

	# Initial / min size for the dialog. This size was chosen as a medium fit, so the
	# smaller settings panels are not surrounded by too much space but most of
	# the panels fit. Vertical scrolling is acceptable. Horizontal scrolling less
	# so, the width was chosen to eliminate horizontal scroll bars. If a panel
	# exceeds the the initial width a debugWarning will be added to the log.
	INITIAL_SIZE = (800, 480)
	MIN_SIZE = (470, 240)  # Min height required to show the OK, Cancel, Apply buttons

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		# Translators: The label for the list of categories in a multi category settings dialog.
		categoriesLabelText = _("&Categories:")
		categoriesLabel = wx.StaticText(self, label=categoriesLabelText)

		# since the categories list and the container both expand in height, the y
		# portion is essentially a "min" height.
		# These sizes are set manually so that the initial proportions within the dialog look correct. If these sizes are
		# not given, then I believe the proportion arguments (as given to the gridBagSizer.AddGrowableColumn) are used
		# to set their relative sizes. We want the proportion argument to be used for resizing, but not the initial size.
		catListDim = (150, 10)
		catListDim = self.scaleSize(catListDim)

		initialScaledWidth = self.scaleSize(self.INITIAL_SIZE[0])
		spaceForBorderWidth = self.scaleSize(20)
		catListWidth = catListDim[0]
		containerDim = (initialScaledWidth - catListWidth - spaceForBorderWidth, self.scaleSize(10))

		self.catListCtrl = nvdaControls.AutoWidthColumnListCtrl(
			self,
			autoSizeColumn=1,
			size=catListDim,
			style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER,
		)
		# This list consists of only one column.
		# The provided column header is just a placeholder, as it is hidden due to the wx.LC_NO_HEADER style flag.
		self.catListCtrl.InsertColumn(0, categoriesLabelText)

		self.container = nvdaControls.TabbableScrolledPanel(
			parent=self,
			style=wx.TAB_TRAVERSAL | wx.BORDER_THEME,
			size=containerDim,
		)

		# Th min size is reset so that they can be reduced to below their "size" constraint.
		self.container.SetMinSize((1, 1))
		self.catListCtrl.SetMinSize((1, 1))

		self.containerSizer = wx.BoxSizer(wx.VERTICAL)
		self.container.SetSizer(self.containerSizer)

		for cls in self.categoryClasses:
			if not issubclass(cls, SettingsPanel):
				raise RuntimeError(
					"Invalid category class %s provided in %s.categoryClasses"
					% (cls.__name__, self.__class__.__name__),
				)
			# It's important here that the listItems are added to catListCtrl in the same order that they exist in categoryClasses.
			# the ListItem index / Id is used to index categoryClasses, and used as the key in catIdToInstanceMap
			self.catListCtrl.Append((cls.title,))

		# populate the GUI with the initial category
		initialCatIndex = 0 if not self.initialCategory else self.categoryClasses.index(self.initialCategory)
		self._doCategoryChange(initialCatIndex)
		self.catListCtrl.Select(initialCatIndex)
		# we must focus the initial category in the category list.
		self.catListCtrl.Focus(initialCatIndex)
		self.setPostInitFocus = self.container.SetFocus if self.initialCategory else self.catListCtrl.SetFocus

		self.gridBagSizer = gridBagSizer = wx.GridBagSizer(
			hgap=guiHelper.SPACE_BETWEEN_BUTTONS_HORIZONTAL,
			vgap=guiHelper.SPACE_BETWEEN_BUTTONS_VERTICAL,
		)
		# add the label, the categories list, and the settings panel to a 2 by 2 grid.
		# The label should span two columns, so that the start of the categories list
		# and the start of the settings panel are at the same vertical position.
		gridBagSizer.Add(categoriesLabel, pos=(0, 0), span=(1, 2))
		gridBagSizer.Add(self.catListCtrl, pos=(1, 0), flag=wx.EXPAND)
		gridBagSizer.Add(self.container, pos=(1, 1), flag=wx.EXPAND)
		# Make the row with the listCtrl and settings panel grow vertically.
		gridBagSizer.AddGrowableRow(1)
		# Make the columns with the listCtrl and settings panel grow horizontally if the dialog is resized.
		# They should grow 1:3, since the settings panel is much more important, and already wider
		# than the listCtrl.
		gridBagSizer.AddGrowableCol(0, proportion=1)
		gridBagSizer.AddGrowableCol(1, proportion=3)
		sHelper.sizer.Add(gridBagSizer, flag=wx.EXPAND, proportion=1)

		self.container.Layout()
		self.catListCtrl.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onCategoryChange)
		self.Bind(wx.EVT_CHAR_HOOK, self.onCharHook)
		self.Bind(EVT_RW_LAYOUT_NEEDED, self._onPanelLayoutChanged)

	def _getCategoryPanel(self, catId):
		panel = self.catIdToInstanceMap.get(catId, None)
		if not panel:
			try:
				cls = self.categoryClasses[catId]
			except IndexError:
				raise ValueError("Unable to create panel for unknown category ID: {}".format(catId))
			panel = cls(parent=self.container)
			panel.Hide()
			self.containerSizer.Add(
				panel,
				flag=wx.ALL | wx.EXPAND,
				border=guiHelper.SPACE_BETWEEN_ASSOCIATED_CONTROL_HORIZONTAL,
			)
			self.catIdToInstanceMap[catId] = panel
			panelWidth = panel.Size[0]
			availableWidth = self.containerSizer.GetSize()[0]
			if panelWidth > availableWidth and gui._isDebug():
				log.debugWarning(
					(
						"Panel width ({1}) too large for: {0} Try to reduce the width of this panel, or increase width of "
						+ "MultiCategorySettingsDialog.MIN_SIZE"
					).format(cls, panel.Size[0]),
				)
			panel.SetLabel(panel.title.replace("&", "&&"))
			panel.SetAccessible(SettingsPanelAccessible(panel))
		return panel

	def postInit(self):
		# By default after the dialog is created, focus lands on the button group for wx.Dialogs. However this is not where
		# we want focus. We only want to modify focus after creation (makeSettings), but postInit is also called after
		# onApply, so we reset the setPostInitFocus function.
		if self.setPostInitFocus:
			self.setPostInitFocus()
			self.setPostInitFocus = None
		else:
			# when postInit is called without a setPostInitFocus ie because onApply was called
			# then set the focus to the listCtrl. This is a good starting point for a "fresh state"
			self.catListCtrl.SetFocus()

	def onCharHook(self, evt):
		"""Listens for keyboard input and switches panels for control+tab"""
		if not self.catListCtrl:
			# Dialog has not yet been constructed.
			# Allow another handler to take the event, and return early.
			evt.Skip()
			return
		key = evt.GetKeyCode()
		listHadFocus = self.catListCtrl.HasFocus()
		if evt.ControlDown() and key == wx.WXK_TAB:
			# Focus the categories list. If we don't, the panel won't hide correctly
			if not listHadFocus:
				self.catListCtrl.SetFocus()
			index = self.catListCtrl.GetFirstSelected()
			newIndex = index - 1 if evt.ShiftDown() else index + 1
			# Less than first wraps to the last index, greater than last wraps to first index.
			newIndex = newIndex % self.catListCtrl.ItemCount
			self.catListCtrl.Select(newIndex)
			# we must focus the new selection in the category list to trigger the change of category.
			self.catListCtrl.Focus(newIndex)
			if not listHadFocus and self.currentCategory:
				self.currentCategory.SetFocus()
		else:
			evt.Skip()

	def _onPanelLayoutChanged(self, evt):
		# call layout and SetupScrolling on the container so that the controls apear in their expected locations.
		self.container.Layout()
		self.container.SetupScrolling()
		# when child elements get smaller the scrolledPanel does not
		# erase the old contents and must be redrawn
		self.container.Refresh()

	def _doCategoryChange(self, newCatId):
		oldCat = self.currentCategory
		# Freeze and Thaw are called to stop visual artifact's while the GUI
		# is being rebuilt. Without this, the controls can sometimes be seen being
		# added.
		self.container.Freeze()
		try:
			newCat = self._getCategoryPanel(newCatId)
		except ValueError as e:
			newCatTitle = self.catListCtrl.GetItemText(newCatId)
			log.error("Unable to change to category: {}".format(newCatTitle), exc_info=e)
			return
		if oldCat:
			oldCat.onPanelDeactivated()
		self.currentCategory = newCat
		newCat.onPanelActivated()
		# call Layout and SetupScrolling on the container to make sure that the controls apear in their expected locations.
		self.container.Layout()
		self.container.SetupScrolling()
		self.container.Thaw()

	def onCategoryChange(self, evt):
		currentCat = self.currentCategory
		newIndex = evt.GetIndex()
		if not currentCat or newIndex != self.categoryClasses.index(currentCat.__class__):
			self._doCategoryChange(newIndex)
		else:
			evt.Skip()

	def _validateAllPanels(self):
		"""Check if all panels are valid, and can be saved
		@note: raises ValueError if a panel is not valid. See c{SettingsPanel.isValid}
		"""
		for panel in self.catIdToInstanceMap.values():
			if panel.isValid() is False:
				raise ValueError("Validation for %s blocked saving settings" % panel.__class__.__name__)

	def _saveAllPanels(self):
		for panel in self.catIdToInstanceMap.values():
			panel.onSave()

	def _notifyAllPanelsSaveOccurred(self):
		for panel in self.catIdToInstanceMap.values():
			panel.postSave()

	def _doSave(self):
		self._validateAllPanels()
		self._saveAllPanels()
		self._notifyAllPanelsSaveOccurred()

	def onOk(self, evt):
		try:
			self._doSave()
		except ValueError:
			log.debugWarning("Error while saving settings:", exc_info=True)
			evt.StopPropagation()
		else:
			super().onOk(evt)

	def onCancel(self, evt):
		for panel in self.catIdToInstanceMap.values():
			panel.onDiscard()
		super(MultiCategorySettingsDialog, self).onCancel(evt)

	def onApply(self, evt):
		try:
			self._doSave()
		except ValueError:
			log.debugWarning("Error while saving settings:", exc_info=True)
			evt.StopPropagation()
		else:
			super().onApply(evt)


class GeneralSettingsPanel(SettingsPanel):
	# Translators: This is the label for the general settings panel.
	title = _("General")
	helpId = "GeneralSettings"
	LOG_LEVELS = (
		# Translators: One of the log levels of NVDA (the disabled mode turns off logging completely).
		(log.OFF, _("disabled")),
		# Translators: One of the log levels of NVDA (the info mode shows info as NVDA runs).
		(log.INFO, _("info")),
		# Translators: One of the log levels of NVDA (the debug warning shows debugging messages and warnings as NVDA runs).
		(log.DEBUGWARNING, _("debug warning")),
		# Translators: One of the log levels of NVDA (the input/output shows keyboard commands and/or braille commands as well as speech and/or braille output of NVDA).
		(log.IO, _("input/output")),
		# Translators: One of the log levels of NVDA (the debug mode shows debug messages as NVDA runs).
		(log.DEBUG, _("debug")),
	)

	def makeSettings(self, settingsSizer):
		settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.languageNames = languageHandler.getAvailableLanguages(presentational=True)
		languageChoices = [x[1] for x in self.languageNames]
		if languageHandler.isLanguageForced():
			try:
				cmdLangDescription = next(
					ld for code, ld in self.languageNames if code == globalVars.appArgs.language
				)
			except StopIteration:
				# In case --lang=Windows is passed to the command line, globalVars.appArgs.language is the current
				# Windows language,, which may not be in the list of NVDA supported languages, e.g. Windows language may
				# be 'fr_FR' but NVDA only supports 'fr'.
				# In this situation, only use language code as a description.
				cmdLangDescription = globalVars.appArgs.language
			languageChoices.append(
				# Translators: Shown for a language which has been provided from the command line
				# 'langDesc' would be replaced with description of the given locale.
				_("Command line option: {langDesc}").format(langDesc=cmdLangDescription),
			)
			self.languageNames.append("FORCED")
		# Translators: The label for a setting in general settings to select NVDA's interface language
		# (once selected, NVDA must be restarted; the option user default means the user's Windows language
		# will be used).
		languageLabelText = _("NVDA &Language (requires restart):")
		self.languageList = settingsSizerHelper.addLabeledControl(
			languageLabelText,
			wx.Choice,
			choices=languageChoices,
		)
		self.bindHelpEvent("GeneralSettingsLanguage", self.languageList)
		self.oldLanguage = config.conf["general"]["language"]
		if languageHandler.isLanguageForced():
			index = len(self.languageNames) - 1
		else:
			index = [x[0] for x in self.languageNames].index(self.oldLanguage)
		self.languageList.SetSelection(index)
		if globalVars.appArgs.secure:
			self.languageList.Disable()

		# Translators: The label for a setting in general settings to save current configuration when NVDA
		# exits (if it is not checked, user needs to save configuration before quitting NVDA).
		self.saveOnExitCheckBox = wx.CheckBox(self, label=_("&Save configuration when exiting NVDA"))
		self.bindHelpEvent("GeneralSettingsSaveConfig", self.saveOnExitCheckBox)
		self.saveOnExitCheckBox.SetValue(config.conf["general"]["saveConfigurationOnExit"])
		if globalVars.appArgs.secure:
			self.saveOnExitCheckBox.Disable()
		settingsSizerHelper.addItem(self.saveOnExitCheckBox)

		# Translators: The label for a setting in general settings to ask before quitting NVDA (if not checked, NVDA will exit without asking the user for action).
		self.askToExitCheckBox = wx.CheckBox(self, label=_("Sho&w exit options when exiting NVDA"))
		self.askToExitCheckBox.SetValue(config.conf["general"]["askToExit"])
		settingsSizerHelper.addItem(self.askToExitCheckBox)
		self.bindHelpEvent("GeneralSettingsShowExitOptions", self.askToExitCheckBox)

		self.playStartAndExitSoundsCheckBox = wx.CheckBox(
			self,
			# Translators: The label for a setting in general settings to play sounds when NVDA starts or exits.
			label=_("&Play sounds when starting or exiting NVDA"),
		)
		self.bindHelpEvent("GeneralSettingsPlaySounds", self.playStartAndExitSoundsCheckBox)
		self.playStartAndExitSoundsCheckBox.SetValue(config.conf["general"]["playStartAndExitSounds"])
		settingsSizerHelper.addItem(self.playStartAndExitSoundsCheckBox)

		# Translators: The label for a setting in general settings to select logging level of NVDA as it runs
		# (available options and what they are logging are found under comments for the logging level messages
		# themselves).
		logLevelLabelText = _("L&ogging level:")
		logLevelChoices = [name for level, name in self.LOG_LEVELS]
		self.logLevelList = settingsSizerHelper.addLabeledControl(
			logLevelLabelText,
			wx.Choice,
			choices=logLevelChoices,
		)
		self.bindHelpEvent("GeneralSettingsLogLevel", self.logLevelList)
		curLevel = log.getEffectiveLevel()
		if logHandler.isLogLevelForced():
			self.logLevelList.Disable()
		for index, (level, name) in enumerate(self.LOG_LEVELS):
			if level == curLevel:
				self.logLevelList.SetSelection(index)
				break
		else:
			log.debugWarning("Could not set log level list to current log level")

		# Translators: The label for a setting in general settings to allow NVDA to start after logging onto
		# Windows (if checked, NVDA will start automatically after logging into Windows; if not, user must
		# start NVDA by pressing the shortcut key (CTRL+Alt+N by default).
		self.startAfterLogonCheckBox = wx.CheckBox(self, label=_("St&art NVDA after I sign in"))
		self.startAfterLogonCheckBox.SetValue(config.getStartAfterLogon())
		if globalVars.appArgs.secure or not config.isInstalledCopy():
			self.startAfterLogonCheckBox.Disable()
		settingsSizerHelper.addItem(self.startAfterLogonCheckBox)
		self.bindHelpEvent("GeneralSettingsStartAfterLogOn", self.startAfterLogonCheckBox)
		self.startOnLogonScreenCheckBox = wx.CheckBox(
			self,
			# Translators: The label for a setting in general settings to
			# allow NVDA to come up in Windows login screen (useful if user
			# needs to enter passwords or if multiple user accounts are present
			# to allow user to choose the correct account).
			label=_("Use NVDA during sign-in (requires administrator privileges)"),
		)
		self.bindHelpEvent("GeneralSettingsStartOnLogOnScreen", self.startOnLogonScreenCheckBox)
		self.startOnLogonScreenCheckBox.SetValue(config.getStartOnLogonScreen())
		if globalVars.appArgs.secure or not config.isInstalledCopy():
			self.startOnLogonScreenCheckBox.Disable()
		settingsSizerHelper.addItem(self.startOnLogonScreenCheckBox)

		self.copySettingsButton = wx.Button(
			self,
			label=_(
				# Translators: The label for a button in general settings to copy
				# current user settings to system settings (to allow current
				# settings to be used in secure screens such as User Account
				# Control (UAC) dialog).
				"Use currently saved settings during sign-in and on secure screens"
				" (requires administrator privileges)",
			),
		)
		self.bindHelpEvent("GeneralSettingsCopySettings", self.copySettingsButton)
		self.copySettingsButton.Bind(wx.EVT_BUTTON, self.onCopySettings)
		if globalVars.appArgs.secure or not config.isInstalledCopy():
			self.copySettingsButton.Disable()
		settingsSizerHelper.addItem(self.copySettingsButton)

		if updateCheck:
			item = self.autoCheckForUpdatesCheckBox = wx.CheckBox(
				self,
				# Translators: The label of a checkbox in general settings to toggle automatic checking for updated versions of NVDA.
				# If not checked, user must check for updates manually.
				label=_("Automatically check for &updates to NVDA"),
			)
			self.bindHelpEvent("GeneralSettingsCheckForUpdates", self.autoCheckForUpdatesCheckBox)
			item.Value = config.conf["update"]["autoCheck"]
			if globalVars.appArgs.secure:
				item.Disable()
			settingsSizerHelper.addItem(item)

			item = self.notifyForPendingUpdateCheckBox = wx.CheckBox(
				self,
				# Translators: The label of a checkbox in general settings to toggle startup notifications
				# for a pending NVDA update.
				label=_("Notify for &pending update on startup"),
			)
			self.bindHelpEvent("GeneralSettingsNotifyPendingUpdates", self.notifyForPendingUpdateCheckBox)
			item.Value = config.conf["update"]["startupNotification"]
			if globalVars.appArgs.secure:
				item.Disable()
			settingsSizerHelper.addItem(item)
			item = self.allowUsageStatsCheckBox = wx.CheckBox(
				self,
				# Translators: The label of a checkbox in general settings to toggle allowing of usage stats gathering
				label=_("Allow NV Access to gather NVDA usage statistics"),
			)
			self.bindHelpEvent("GeneralSettingsGatherUsageStats", self.allowUsageStatsCheckBox)
			item.Value = config.conf["update"]["allowUsageStats"]
			if globalVars.appArgs.secure:
				item.Disable()
			settingsSizerHelper.addItem(item)

			# Translators: The label for the update mirror on the General Settings panel.
			mirrorBoxSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=_("Update mirror"))
			mirrorBox = mirrorBoxSizer.GetStaticBox()
			mirrorBoxSizerHelper = guiHelper.BoxSizerHelper(self, sizer=mirrorBoxSizer)
			settingsSizerHelper.addItem(mirrorBoxSizerHelper)

			# Use an ExpandoTextCtrl because even when read-only it accepts focus from keyboard, which
			# standard read-only TextCtrl does not. ExpandoTextCtrl is a TE_MULTILINE control, however
			# by default it renders as a single line. Standard TextCtrl with TE_MULTILINE has two lines,
			# and a vertical scroll bar. This is not neccessary for the single line of text we wish to
			# display here.
			# Note: To avoid code duplication, the value of this text box will be set in `onPanelActivated`.
			self.mirrorURLTextBox = ExpandoTextCtrl(
				mirrorBox,
				size=(self.scaleSize(250), -1),
				style=wx.TE_READONLY,
			)
			# Translators: This is the label for the button used to change the NVDA update mirror URL,
			# it appears in the context of the update mirror group on the General page of NVDA's settings.
			changeMirrorBtn = wx.Button(mirrorBox, label=_("Change..."))
			mirrorBoxSizerHelper.addItem(
				guiHelper.associateElements(
					self.mirrorURLTextBox,
					changeMirrorBtn,
				),
			)
			self.bindHelpEvent("UpdateMirror", mirrorBox)
			self.mirrorURLTextBox.Bind(wx.EVT_CHAR_HOOK, self._enterTriggersOnChangeMirrorURL)
			changeMirrorBtn.Bind(wx.EVT_BUTTON, self.onChangeMirrorURL)
			if globalVars.appArgs.secure:
				mirrorBox.Disable()

	def onChangeMirrorURL(self, evt: wx.CommandEvent | wx.KeyEvent):
		"""Show the dialog to change the update mirror URL, and refresh the dialog in response to the URL being changed."""
		# Import late to avoid circular dependency.
		from gui._SetURLDialog import _SetURLDialog

		changeMirror = _SetURLDialog(
			self,
			# Translators: Title of the dialog used to change NVDA's update server mirror URL.
			title=_("Set NVDA Update Mirror"),
			configPath=("update", "serverURL"),
			helpId="SetUpdateMirror",
			urlTransformer=lambda url: f"{url}?versionType=stable",
		)
		ret = changeMirror.ShowModal()
		if ret == wx.ID_OK:
			self.Freeze()
			# trigger a refresh of the settings
			self.onPanelActivated()
			self._sendLayoutUpdatedEvent()
			self.Thaw()

	def _enterTriggersOnChangeMirrorURL(self, evt: wx.KeyEvent):
		"""Open the change update mirror URL dialog in response to the enter key in the mirror URL read-only text box."""
		if evt.KeyCode == wx.WXK_RETURN:
			self.onChangeMirrorURL(evt)
		else:
			evt.Skip()

	def onCopySettings(self, evt):
		if os.path.isdir(WritePaths.addonsDir) and 0 < len(os.listdir(WritePaths.addonsDir)):
			message = _(
				# Translators: A message to warn the user when attempting to copy current
				# settings to system settings.
				"Add-ons were detected in your user settings directory. "
				"Copying these to the system profile could be a security risk. "
				"Do you still wish to copy your settings?",
			)
			# Translators: The title of the warning dialog displayed when trying to
			# copy settings for use in secure screens.
			title = _("Warning")
			style = wx.YES | wx.NO | wx.ICON_WARNING
			if wx.NO == gui.messageBox(message, title, style, self):
				return
		progressDialog = gui.IndeterminateProgressDialog(
			gui.mainFrame,
			# Translators: The title of the dialog presented while settings are being copied
			_("Copying Settings"),
			# Translators: The message displayed while settings are being copied
			# to the system configuration (for use on Windows logon etc)
			_("Please wait while settings are copied to the system configuration."),
		)
		while True:
			try:
				systemUtils.ExecAndPump(config.setSystemConfigToCurrentConfig)
				res = True
				break
			except installer.RetriableFailure:
				log.debugWarning("Error when copying settings to system config", exc_info=True)
				message = _(
					# Translators: a message dialog asking to retry or cancel when copying settings  fails
					"Unable to copy a file. "
					"Perhaps it is currently being used by another process or you have run out of disc space on the drive you are copying to.",
				)
				# Translators: the title of a retry cancel dialog when copying settings  fails
				title = _("Error Copying")
				if winUser.MessageBox(None, message, title, winUser.MB_RETRYCANCEL) == winUser.IDRETRY:
					continue
				res = False
				break
			except:  # noqa: E722
				log.debugWarning("Error when copying settings to system config", exc_info=True)
				res = False
				break
		progressDialog.done()
		del progressDialog
		if not res:
			# Translators: The message displayed when errors were found while trying to copy current configuration to system settings.
			gui.messageBox(_("Error copying NVDA user settings"), _("Error"), wx.OK | wx.ICON_ERROR, self)
		else:
			gui.messageBox(
				# Translators: The message displayed when copying configuration to system settings was successful.
				_("Successfully copied NVDA user settings"),
				# Translators: The message title displayed when copying configuration to system settings was successful.
				_("Success"),
				wx.OK | wx.ICON_INFORMATION,
				self,
			)

	def onSave(self):
		if (
			not languageHandler.isLanguageForced()
			or self.languageList.GetSelection() != len(self.languageNames) - 1
		):
			newLanguage = [x[0] for x in self.languageNames][self.languageList.GetSelection()]
			config.conf["general"]["language"] = newLanguage
		config.conf["general"]["saveConfigurationOnExit"] = self.saveOnExitCheckBox.IsChecked()
		config.conf["general"]["askToExit"] = self.askToExitCheckBox.IsChecked()
		config.conf["general"]["playStartAndExitSounds"] = self.playStartAndExitSoundsCheckBox.IsChecked()
		logLevel = self.LOG_LEVELS[self.logLevelList.GetSelection()][0]
		if not logHandler.isLogLevelForced():
			config.conf["general"]["loggingLevel"] = logging.getLevelName(logLevel)
			logHandler.setLogLevelFromConfig()
		if self.startAfterLogonCheckBox.IsEnabled():
			config.setStartAfterLogon(self.startAfterLogonCheckBox.GetValue())
		if self.startOnLogonScreenCheckBox.IsEnabled():
			try:
				config.setStartOnLogonScreen(self.startOnLogonScreenCheckBox.GetValue())
			except (WindowsError, RuntimeError):
				gui.messageBox(
					_("This change requires administrator privileges."),
					_("Insufficient Privileges"),
					style=wx.OK | wx.ICON_ERROR,
					parent=self,
				)
		if updateCheck:
			config.conf["update"]["autoCheck"] = self.autoCheckForUpdatesCheckBox.IsChecked()
			config.conf["update"]["allowUsageStats"] = self.allowUsageStatsCheckBox.IsChecked()
			config.conf["update"]["startupNotification"] = self.notifyForPendingUpdateCheckBox.IsChecked()
			updateCheck.terminate()
			updateCheck.initialize()

	def onPanelActivated(self):
		if updateCheck:
			self._updateCurrentMirrorURL()
		super().onPanelActivated()

	def _updateCurrentMirrorURL(self):
		self.mirrorURLTextBox.SetValue(
			(
				url
				if (url := config.conf["update"]["serverURL"])
				# Translators: A value that appears in NVDA's Settings to indicate that no mirror is in use.
				else _("No mirror")
			),
		)

	def postSave(self):
		if self.oldLanguage != config.conf["general"]["language"]:
			LanguageRestartDialog(self).ShowModal()


class LanguageRestartDialog(
	gui.contextHelp.ContextHelpMixin,
	wx.Dialog,  # wxPython does not seem to call base class initializer, put last in MRO
):
	helpId = "GeneralSettingsLanguage"

	def __init__(self, parent):
		# Translators: The title of the dialog which appears when the user changed NVDA's interface language.
		super(LanguageRestartDialog, self).__init__(parent, title=_("Language Configuration Change"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		sHelper.addItem(
			# Translators: The message displayed after NVDA interface language has been changed.
			wx.StaticText(self, label=_("NVDA must be restarted for the new language to take effect.")),
		)

		bHelper = sHelper.addDialogDismissButtons(guiHelper.ButtonHelper(wx.HORIZONTAL))
		# Translators: The label for a button  in the dialog which appears when the user changed NVDA's interface language.
		restartNowButton = bHelper.addButton(self, label=_("Restart &now"))
		restartNowButton.Bind(wx.EVT_BUTTON, self.onRestartNowButton)
		restartNowButton.SetFocus()

		# Translators: The label for a button  in the dialog which appears when the user changed NVDA's interface language.
		restartLaterButton = bHelper.addButton(self, wx.ID_CLOSE, label=_("Restart &later"))
		restartLaterButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		self.Bind(wx.EVT_CLOSE, lambda evt: self.Destroy())
		self.EscapeId = wx.ID_CLOSE

		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.CentreOnScreen()

	def onRestartNowButton(self, evt):
		self.Destroy()
		config.conf.save()
		queueHandler.queueFunction(queueHandler.eventQueue, core.restart)


class SpeechSettingsPanel(SettingsPanel):
	# Translators: This is the label for the speech panel
	title = _("Speech")
	helpId = "SpeechSettings"

	def makeSettings(self, settingsSizer):
		settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: A label for the synthesizer on the speech panel.
		synthLabel = _("Synthesizer")
		synthBoxSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=synthLabel)
		synthBox = synthBoxSizer.GetStaticBox()
		synthGroup = guiHelper.BoxSizerHelper(self, sizer=synthBoxSizer)
		settingsSizerHelper.addItem(synthGroup)

		# Use a ExpandoTextCtrl because even when readonly it accepts focus from keyboard, which
		# standard readonly TextCtrl does not. ExpandoTextCtrl is a TE_MULTILINE control, however
		# by default it renders as a single line. Standard TextCtrl with TE_MULTILINE has two lines,
		# and a vertical scroll bar. This is not neccessary for the single line of text we wish to
		# display here.
		synthDesc = getSynth().description
		self.synthNameCtrl = ExpandoTextCtrl(
			synthBox,
			size=(self.scaleSize(250), -1),
			value=synthDesc,
			style=wx.TE_READONLY,
		)
		self.synthNameCtrl.Bind(wx.EVT_CHAR_HOOK, self._enterTriggersOnChangeSynth)

		# Translators: This is the label for the button used to change synthesizer,
		# it appears in the context of a synthesizer group on the speech settings panel.
		changeSynthBtn = wx.Button(synthBox, label=_("C&hange..."))
		self.bindHelpEvent("SpeechSettingsChange", self.synthNameCtrl)
		self.bindHelpEvent("SpeechSettingsChange", changeSynthBtn)
		synthGroup.addItem(
			guiHelper.associateElements(
				self.synthNameCtrl,
				changeSynthBtn,
			),
		)
		changeSynthBtn.Bind(wx.EVT_BUTTON, self.onChangeSynth)

		self.voicePanel = VoiceSettingsPanel(self)
		settingsSizerHelper.addItem(self.voicePanel)

	def _enterTriggersOnChangeSynth(self, evt):
		if evt.KeyCode == wx.WXK_RETURN:
			self.onChangeSynth(evt)
		else:
			evt.Skip()

	def onChangeSynth(self, evt):
		changeSynth = SynthesizerSelectionDialog(self, multiInstanceAllowed=True)
		ret = changeSynth.ShowModal()
		if ret == wx.ID_OK:
			self.Freeze()
			# trigger a refresh of the settings
			self.onPanelActivated()
			self._sendLayoutUpdatedEvent()
			self.Thaw()

	def updateCurrentSynth(self):
		synthDesc = getSynth().description
		self.synthNameCtrl.SetValue(synthDesc)

	def onPanelActivated(self):
		# call super after all panel updates have been completed, we dont want the panel to show until this is complete.
		self.voicePanel.onPanelActivated()
		super(SpeechSettingsPanel, self).onPanelActivated()

	def onPanelDeactivated(self):
		self.voicePanel.onPanelDeactivated()
		super(SpeechSettingsPanel, self).onPanelDeactivated()

	def onDiscard(self):
		self.voicePanel.onDiscard()

	def onSave(self):
		self.voicePanel.onSave()

	def isValid(self) -> bool:
		return self.voicePanel.isValid()


class SynthesizerSelectionDialog(SettingsDialog):
	# Translators: This is the label for the synthesizer selection dialog
	title = _("Select Synthesizer")
	helpId = "SynthesizerSelection"
	synthNames: List[str] = []

	def makeSettings(self, settingsSizer):
		settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: This is a label for the select
		# synthesizer combobox in the synthesizer dialog.
		synthListLabelText = _("&Synthesizer:")
		self.synthList = settingsSizerHelper.addLabeledControl(synthListLabelText, wx.Choice, choices=[])
		self.bindHelpEvent("SelectSynthesizerSynthesizer", self.synthList)
		self.updateSynthesizerList()

	def postInit(self):
		# Finally, ensure that focus is on the synthlist
		self.synthList.SetFocus()

	def updateSynthesizerList(self):
		driverList = getSynthList()
		self.synthNames = [x[0] for x in driverList]
		options = [x[1] for x in driverList]
		self.synthList.Clear()
		self.synthList.AppendItems(options)
		try:
			index = self.synthNames.index(getSynth().name)
			self.synthList.SetSelection(index)
		except:  # noqa: E722
			pass

	def onOk(self, evt):
		if not self.synthNames:
			# The list of synths has not been populated yet, so we didn't change anything in this panel
			return

		newSynth = self.synthNames[self.synthList.GetSelection()]
		if not setSynth(newSynth):
			_synthWarningDialog(newSynth)
			return

		# Reinitialize the tones module to update the audio device
		import tones

		tones.terminate()
		tones.initialize()

		if self.IsModal():
			# Hack: we need to update the synth in our parent window before closing.
			# Otherwise, NVDA will report the old synth even though the new synth is reflected visually.
			self.Parent.updateCurrentSynth()
		super(SynthesizerSelectionDialog, self).onOk(evt)


class DriverSettingChanger(object):
	"""Functor which acts as callback for GUI events."""

	def __init__(self, driver, setting):
		self._driverRef = weakref.ref(driver)
		self.setting = setting

	@property
	def driver(self):
		return self._driverRef()

	def __call__(self, evt):
		evt.Skip()  # allow other handlers to also process this event.
		val = evt.GetSelection()
		setattr(self.driver, self.setting.id, val)


class StringDriverSettingChanger(DriverSettingChanger):
	"""Same as L{DriverSettingChanger} but handles combobox events."""

	def __init__(self, driver, setting, container):
		self.container = container
		super(StringDriverSettingChanger, self).__init__(driver, setting)

	def __call__(self, evt):
		evt.Skip()  # allow other handlers to also process this event.
		# Quick workaround to deal with voice changes.
		if self.setting.id == "voice":
			# Cancel speech first so that the voice will change immediately instead of the change being queued.
			speech.cancelSpeech()
			changeVoice(
				self.driver,
				getattr(self.container, "_%ss" % self.setting.id)[evt.GetSelection()].id,
			)
			self.container.updateDriverSettings(changedSetting=self.setting.id)
		else:
			setattr(
				self.driver,
				self.setting.id,
				getattr(self.container, "_%ss" % self.setting.id)[evt.GetSelection()].id,
			)


class AutoSettingsMixin(metaclass=ABCMeta):
	"""
	Mixin class that provides support for driver/vision provider specific gui settings.
	Derived classes should implement:
	- L{getSettings}
	- L{settingsSizer}
	Derived classes likely need to inherit from L{SettingsPanel}, in particular
	the following methods must be provided:
	- makeSettings
	- onPanelActivated
	@note: This mixin uses self.lastControl and self.sizerDict to keep track of the
	controls added / and maintain ordering.
	If you plan to maintain other controls in the same panel care will need to be taken.
	"""

	def __init__(self, *args, **kwargs):
		"""
		Mixin init, forwards args to other base class.
		The other base class is likely L{gui.SettingsPanel}.
		@param args: Positional args to passed to other base class.
		@param kwargs: Keyword args to passed to other base class.
		"""
		self.sizerDict = {}
		self.lastControl = None
		super(AutoSettingsMixin, self).__init__(*args, **kwargs)
		# because settings instances can be of type L{Driver} as well, we have to handle
		# showing settings for non-instances. Because of this, we must reacquire a reference
		# to the settings class whenever we wish to use it (via L{getSettings}) in case the instance changes.
		# We also use the weakref to refresh the gui when an instance dies.
		self._currentSettingsRef = weakref.ref(
			self.getSettings(),
			lambda ref: wx.CallAfter(self.refreshGui),
		)

	settingsSizer: wx.BoxSizer

	@abstractmethod
	def getSettings(self) -> AutoSettings: ...

	@abstractmethod
	def makeSettings(self, sizer: wx.BoxSizer):
		"""Populate the panel with settings controls.
		@note: Normally classes also inherit from settingsDialogs.SettingsPanel.
		@param sizer: The sizer to which to add the settings controls.
		"""
		...

	def _getSettingsStorage(self) -> Any:
		"""Override to change storage object for setting values."""
		return self.getSettings()

	@property
	def hasOptions(self) -> bool:
		return bool(self.getSettings().supportedSettings)

	@classmethod
	def _setSliderStepSizes(cls, slider, setting):
		slider.SetLineSize(setting.minStep)
		slider.SetPageSize(setting.largeStep)

	def _getSettingControlHelpId(self, controlId):
		"""Define the helpId associated to this control."""
		return self.helpId

	def _makeSliderSettingControl(
		self,
		setting: NumericDriverSetting,
		settingsStorage: Any,
	) -> wx.BoxSizer:
		"""Constructs appropriate GUI controls for given L{DriverSetting} such as label and slider.
		@param setting: Setting to construct controls for
		@param settingsStorage: where to get initial values / set values.
			This param must have an attribute with a name matching setting.id.
			In most cases it will be of type L{AutoSettings}
		@return: wx.BoxSizer containing newly created controls.
		"""
		labeledControl = guiHelper.LabeledControlHelper(
			self,
			f"{setting.displayNameWithAccelerator}:",
			nvdaControls.EnhancedInputSlider,
			minValue=setting.minVal,
			maxValue=setting.maxVal,
		)
		lSlider = labeledControl.control
		setattr(self, f"{setting.id}Slider", lSlider)
		lSlider.Bind(
			wx.EVT_SLIDER,
			DriverSettingChanger(
				settingsStorage,
				setting,
			),
		)
		self.bindHelpEvent(
			self._getSettingControlHelpId(setting.id),
			lSlider,
		)
		self._setSliderStepSizes(lSlider, setting)
		lSlider.SetValue(getattr(settingsStorage, setting.id))
		if self.lastControl:
			lSlider.MoveAfterInTabOrder(self.lastControl)
		self.lastControl = lSlider
		return labeledControl.sizer

	def _makeStringSettingControl(
		self,
		setting: DriverSetting,
		settingsStorage: Any,
	):
		"""
		Same as L{_makeSliderSettingControl} but for string settings displayed in a wx.Choice control
		Options for the choice control come from the availableXstringvalues property
		(Dict[id, StringParameterInfo]) on the instance returned by self.getSettings()
		The id of the value is stored on settingsStorage.
		Returns sizer with label and combobox.
		"""
		labelText = f"{setting.displayNameWithAccelerator}:"
		stringSettingAttribName = f"_{setting.id}s"
		setattr(
			self,
			stringSettingAttribName,
			# Settings are stored as an ordered dict.
			# Therefore wrap this inside a list call.
			list(
				getattr(
					self.getSettings(),
					f"available{setting.id.capitalize()}s",
				).values(),
			),
		)
		stringSettings = getattr(self, stringSettingAttribName)
		labeledControl = guiHelper.LabeledControlHelper(
			self,
			labelText,
			wx.Choice,
			choices=[x.displayName for x in stringSettings],
		)
		lCombo = labeledControl.control
		setattr(self, f"{setting.id}List", lCombo)
		self.bindHelpEvent(
			self._getSettingControlHelpId(setting.id),
			lCombo,
		)

		try:
			cur = getattr(settingsStorage, setting.id)
			selectionIndex = [x.id for x in stringSettings].index(cur)
			lCombo.SetSelection(selectionIndex)
		except ValueError:
			pass
		lCombo.Bind(
			wx.EVT_CHOICE,
			StringDriverSettingChanger(settingsStorage, setting, self),
		)
		if self.lastControl:
			lCombo.MoveAfterInTabOrder(self.lastControl)
		self.lastControl = lCombo
		return labeledControl.sizer

	def _makeBooleanSettingControl(
		self,
		setting: BooleanDriverSetting,
		settingsStorage: Any,
	):
		"""
		Same as L{_makeSliderSettingControl} but for boolean settings. Returns checkbox.
		"""
		checkbox = wx.CheckBox(self, label=setting.displayNameWithAccelerator)
		setattr(self, f"{setting.id}Checkbox", checkbox)
		settingsStorageProxy = weakref.proxy(settingsStorage)
		self.bindHelpEvent(self._getSettingControlHelpId(setting.id), checkbox)

		def _onCheckChanged(evt: wx.CommandEvent):
			evt.Skip()  # allow other handlers to also process this event.
			setattr(settingsStorageProxy, setting.id, evt.IsChecked())

		checkbox.Bind(wx.EVT_CHECKBOX, _onCheckChanged)
		checkbox.SetValue(
			getattr(
				settingsStorage,
				setting.id,
			),
		)
		if self.lastControl:
			checkbox.MoveAfterInTabOrder(self.lastControl)
		self.lastControl = checkbox
		return checkbox

	def updateDriverSettings(self, changedSetting=None):
		"""
		Creates, hides or updates existing GUI controls for all of supported settings.
		"""
		settingsInst = self.getSettings()
		settingsStorage = self._getSettingsStorage()
		# firstly check already created options
		for name, sizer in self.sizerDict.items():
			if name == changedSetting:
				# Changing a setting shouldn't cause that setting itself to disappear.
				continue
			if not settingsInst.isSupported(name):
				self.settingsSizer.Hide(sizer)
		# Create new controls, update already existing
		if gui._isDebug():
			log.debug(f"Current sizerDict: {self.sizerDict!r}")
			log.debug(f"Current supportedSettings: {self.getSettings().supportedSettings!r}")
		for setting in settingsInst.supportedSettings:
			if setting.id == changedSetting:
				# Changing a setting shouldn't cause that setting's own values to change.
				continue
			if setting.id in self.sizerDict:  # update a value
				self._updateValueForControl(setting, settingsStorage)
			else:  # create a new control
				self._createNewControl(setting, settingsStorage)
		# Update graphical layout of the dialog
		self.settingsSizer.Layout()

	def _createNewControl(self, setting, settingsStorage):
		settingMaker = self._getSettingMaker(setting)
		try:
			s = settingMaker(setting, settingsStorage)
		except UnsupportedConfigParameterError:
			log.debugWarning(f"Unsupported setting {setting.id}; ignoring", exc_info=True)
		else:
			self.sizerDict[setting.id] = s
			self.settingsSizer.Insert(
				len(self.sizerDict) - 1,
				s,
				border=10,
				flag=wx.BOTTOM,
			)

	def _getSettingMaker(self, setting):
		if isinstance(setting, NumericDriverSetting):
			settingMaker = self._makeSliderSettingControl
		elif isinstance(setting, BooleanDriverSetting):
			settingMaker = self._makeBooleanSettingControl
		else:
			settingMaker = self._makeStringSettingControl
		return settingMaker

	def _updateValueForControl(self, setting, settingsStorage):
		self.settingsSizer.Show(self.sizerDict[setting.id])
		if isinstance(setting, NumericDriverSetting):
			getattr(self, f"{setting.id}Slider").SetValue(
				getattr(settingsStorage, setting.id),
			)
		elif isinstance(setting, BooleanDriverSetting):
			getattr(self, f"{setting.id}Checkbox").SetValue(
				getattr(settingsStorage, setting.id),
			)
		else:
			options = getattr(self, f"_{setting.id}s")
			lCombo = getattr(self, f"{setting.id}List")
			try:
				cur = getattr(settingsStorage, setting.id)
				indexOfItem = [x.id for x in options].index(cur)
				lCombo.SetSelection(indexOfItem)
			except ValueError:
				pass

	def onDiscard(self):
		# unbind change events for string settings as wx closes combo boxes on cancel
		settingsInst = self.getSettings()
		for setting in settingsInst.supportedSettings:
			if isinstance(setting, (NumericDriverSetting, BooleanDriverSetting)):
				continue
			getattr(self, f"{setting.id}List").Unbind(wx.EVT_CHOICE)
		# restore settings
		settingsInst.loadSettings()

	def onSave(self):
		self.getSettings().saveSettings()

	def refreshGui(self):
		if not self._currentSettingsRef():
			if gui._isDebug():
				log.debug("refreshing panel")
			self.sizerDict.clear()
			self.settingsSizer.Clear(delete_windows=True)
			self._currentSettingsRef = weakref.ref(
				self.getSettings(),
				lambda ref: wx.CallAfter(self.refreshGui),
			)
			self.makeSettings(self.settingsSizer)

	def onPanelActivated(self):
		"""Called after the panel has been activated
		@note: Normally classes also inherit from settingsDialogs.SettingsPanel.
		"""
		self.refreshGui()
		super().onPanelActivated()


class VoiceSettingsPanel(AutoSettingsMixin, SettingsPanel):
	# Translators: This is the label for the voice settings panel.
	title = _("Voice")
	helpId = "SpeechSettings"

	@property
	def driver(self):
		synth: SynthDriver = getSynth()
		return synth

	def getSettings(self) -> AutoSettings:
		return self.driver

	def _getSettingControlHelpId(self, controlId):
		standardSettings = ["voice", "variant", "rate", "rateBoost", "pitch", "inflection", "volume"]
		if controlId in standardSettings:
			capitalizedId = controlId[0].upper() + controlId[1:]
			return f"{self.helpId}{capitalizedId}"
		else:
			return self.helpId

	def makeSettings(self, settingsSizer):
		# Construct synthesizer settings
		self.updateDriverSettings()

		settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: This is the label for a checkbox in the
		# voice settings panel (if checked, text will be read using the voice for the language of the text).
		autoLanguageSwitchingText = _("Automatic language switching (when supported)")
		self.autoLanguageSwitchingCheckbox = settingsSizerHelper.addItem(
			wx.CheckBox(
				self,
				label=autoLanguageSwitchingText,
			),
		)
		self.bindHelpEvent("SpeechSettingsLanguageSwitching", self.autoLanguageSwitchingCheckbox)
		self.autoLanguageSwitchingCheckbox.SetValue(
			config.conf["speech"]["autoLanguageSwitching"],
		)

		# Translators: This is the label for a checkbox in the
		# voice settings panel (if checked, different voices for dialects will be used to
		# read text in that dialect).
		autoDialectSwitchingText = _("Automatic dialect switching (when supported)")
		self.autoDialectSwitchingCheckbox = settingsSizerHelper.addItem(
			wx.CheckBox(self, label=autoDialectSwitchingText),
		)
		self.bindHelpEvent("SpeechSettingsDialectSwitching", self.autoDialectSwitchingCheckbox)
		self.autoDialectSwitchingCheckbox.SetValue(
			config.conf["speech"]["autoDialectSwitching"],
		)

		# Translators: This is the label for a combobox in the
		# voice settings panel (possible choices are none, some, most and all).
		punctuationLabelText = _("Punctuation/symbol &level:")
		symbolLevelLabels = characterProcessing.SPEECH_SYMBOL_LEVEL_LABELS
		symbolLevelChoices = [
			symbolLevelLabels[level] for level in characterProcessing.CONFIGURABLE_SPEECH_SYMBOL_LEVELS
		]
		self.symbolLevelList = settingsSizerHelper.addLabeledControl(
			punctuationLabelText,
			wx.Choice,
			choices=symbolLevelChoices,
		)
		self.bindHelpEvent("SpeechSettingsSymbolLevel", self.symbolLevelList)
		curLevel = config.conf["speech"]["symbolLevel"]
		self.symbolLevelList.SetSelection(
			characterProcessing.CONFIGURABLE_SPEECH_SYMBOL_LEVELS.index(curLevel),
		)

		# Translators: This is the label for a checkbox in the
		# voice settings panel (if checked, text will be read using the voice for the language of the text).
		trustVoiceLanguageText = _("Trust voice's language when processing characters and symbols")
		self.trustVoiceLanguageCheckbox = settingsSizerHelper.addItem(
			wx.CheckBox(self, label=trustVoiceLanguageText),
		)
		self.bindHelpEvent("SpeechSettingsTrust", self.trustVoiceLanguageCheckbox)
		self.trustVoiceLanguageCheckbox.SetValue(config.conf["speech"]["trustVoiceLanguage"])

		self.unicodeNormalizationCombo: nvdaControls.FeatureFlagCombo = settingsSizerHelper.addLabeledControl(
			labelText=_(
				# Translators: This is a label for a combo-box in the Speech settings panel.
				"Unicode normali&zation",
			),
			wxCtrlClass=nvdaControls.FeatureFlagCombo,
			keyPath=["speech", "unicodeNormalization"],
			conf=config.conf,
			onChoiceEventHandler=self._onUnicodeNormalizationChange,
		)
		self.bindHelpEvent("SpeechUnicodeNormalization", self.unicodeNormalizationCombo)

		# Translators: This is the label for a checkbox in the
		# speech settings panel.
		reportNormalizedForCharacterNavigationText = _("Report '&Normalized' when navigating by character")
		self.reportNormalizedForCharacterNavigationCheckBox = settingsSizerHelper.addItem(
			wx.CheckBox(self, label=reportNormalizedForCharacterNavigationText),
		)
		self.bindHelpEvent(
			"SpeechReportNormalizedForCharacterNavigation",
			self.reportNormalizedForCharacterNavigationCheckBox,
		)
		self.reportNormalizedForCharacterNavigationCheckBox.SetValue(
			config.conf["speech"]["reportNormalizedForCharacterNavigation"],
		)
		self.reportNormalizedForCharacterNavigationCheckBox.Enable(
			bool(self.unicodeNormalizationCombo._getControlCurrentFlag()),
		)

		self._appendSymbolDictionariesList(settingsSizerHelper)

		self._appendDelayedCharacterDescriptions(settingsSizerHelper)

		minPitchChange = int(
			config.conf.getConfigValidation(
				("speech", self.driver.name, "capPitchChange"),
			).kwargs["min"],
		)

		maxPitchChange = int(
			config.conf.getConfigValidation(
				("speech", self.driver.name, "capPitchChange"),
			).kwargs["max"],
		)

		# Translators: This is a label for a setting in voice settings (an edit box to change
		# voice pitch for capital letters; the higher the value, the pitch will be higher).
		capPitchChangeLabelText = _("Capital pitch change percentage")
		self.capPitchChangeEdit = settingsSizerHelper.addLabeledControl(
			capPitchChangeLabelText,
			nvdaControls.SelectOnFocusSpinCtrl,
			min=minPitchChange,
			max=maxPitchChange,
			initial=config.conf["speech"][self.driver.name]["capPitchChange"],
		)
		self.bindHelpEvent(
			"SpeechSettingsCapPitchChange",
			self.capPitchChangeEdit,
		)

		# Translators: This is the label for a checkbox in the
		# voice settings panel.
		sayCapForCapsText = _("Say &cap before capitals")
		self.sayCapForCapsCheckBox = settingsSizerHelper.addItem(
			wx.CheckBox(self, label=sayCapForCapsText),
		)
		self.bindHelpEvent("SpeechSettingsSayCapBefore", self.sayCapForCapsCheckBox)
		self.sayCapForCapsCheckBox.SetValue(
			config.conf["speech"][self.driver.name]["sayCapForCapitals"],
		)

		# Translators: This is the label for a checkbox in the
		# voice settings panel.
		beepForCapsText = _("&Beep for capitals")
		self.beepForCapsCheckBox = settingsSizerHelper.addItem(
			wx.CheckBox(self, label=beepForCapsText),
		)
		self.bindHelpEvent(
			"SpeechSettingsBeepForCaps",
			self.beepForCapsCheckBox,
		)
		self.beepForCapsCheckBox.SetValue(
			config.conf["speech"][self.driver.name]["beepForCapitals"],
		)

		# Translators: This is the label for a checkbox in the
		# voice settings panel.
		useSpellingFunctionalityText = _("Use &spelling functionality if supported")
		self.useSpellingFunctionalityCheckBox = settingsSizerHelper.addItem(
			wx.CheckBox(self, label=useSpellingFunctionalityText),
		)
		self.bindHelpEvent("SpeechSettingsUseSpelling", self.useSpellingFunctionalityCheckBox)
		self.useSpellingFunctionalityCheckBox.SetValue(
			config.conf["speech"][self.driver.name]["useSpellingFunctionality"],
		)
		self._appendSpeechModesList(settingsSizerHelper)

	def _appendSymbolDictionariesList(self, settingsSizerHelper: guiHelper.BoxSizerHelper) -> None:
		self._availableSymbolDictionaries = [
			d for d in characterProcessing.listAvailableSymbolDictionaryDefinitions() if d.userVisible
		]
		self.symbolDictionariesList: nvdaControls.CustomCheckListBox = settingsSizerHelper.addLabeledControl(
			# Translators: Label of the list where user can enable or disable symbol dictionaires.
			_("E&xtra dictionaries for character and symbol processing:"),
			nvdaControls.CustomCheckListBox,
			choices=[d.displayName for d in self._availableSymbolDictionaries],
		)
		self.bindHelpEvent("SpeechSymbolDictionaries", self.symbolDictionariesList)
		self.symbolDictionariesList.CheckedItems = [
			i for i, d in enumerate(self._availableSymbolDictionaries) if d.enabled
		]
		self.symbolDictionariesList.Select(0)

	def _appendSpeechModesList(self, settingsSizerHelper: guiHelper.BoxSizerHelper) -> None:
		self._allSpeechModes = list(speech.SpeechMode)
		self.speechModesList: nvdaControls.CustomCheckListBox = settingsSizerHelper.addLabeledControl(
			# Translators: Label of the list where user can select speech modes that will be available.
			_("&Modes available in the Cycle speech mode command:"),
			nvdaControls.CustomCheckListBox,
			choices=[mode.displayString for mode in self._allSpeechModes],
		)
		self.bindHelpEvent("SpeechModesDisabling", self.speechModesList)
		excludedModes = config.conf["speech"]["excludedSpeechModes"]
		self.speechModesList.Checked = [
			mIndex for mIndex in range(len(self._allSpeechModes)) if mIndex not in excludedModes
		]
		self.speechModesList.Bind(wx.EVT_CHECKLISTBOX, self._onSpeechModesListChange)
		self.speechModesList.Select(0)

	def _appendDelayedCharacterDescriptions(self, settingsSizerHelper: guiHelper.BoxSizerHelper) -> None:
		# Translators: This is the label for a checkbox in the voice settings panel.
		delayedCharacterDescriptionsText = _("&Delayed descriptions for characters on cursor movement")
		self.delayedCharacterDescriptionsCheckBox = settingsSizerHelper.addItem(
			wx.CheckBox(self, label=delayedCharacterDescriptionsText),
		)
		self.bindHelpEvent("delayedCharacterDescriptions", self.delayedCharacterDescriptionsCheckBox)
		self.delayedCharacterDescriptionsCheckBox.SetValue(
			config.conf["speech"]["delayedCharacterDescriptions"],
		)

	def onSave(self):
		AutoSettingsMixin.onSave(self)

		config.conf["speech"]["autoLanguageSwitching"] = self.autoLanguageSwitchingCheckbox.IsChecked()
		config.conf["speech"]["autoDialectSwitching"] = self.autoDialectSwitchingCheckbox.IsChecked()
		config.conf["speech"]["symbolLevel"] = characterProcessing.CONFIGURABLE_SPEECH_SYMBOL_LEVELS[
			self.symbolLevelList.GetSelection()
		].value
		config.conf["speech"]["trustVoiceLanguage"] = self.trustVoiceLanguageCheckbox.IsChecked()
		self.unicodeNormalizationCombo.saveCurrentValueToConf()
		config.conf["speech"]["reportNormalizedForCharacterNavigation"] = (
			self.reportNormalizedForCharacterNavigationCheckBox.IsChecked()
		)
		currentSymbolDictionaries = config.conf["speech"]["symbolDictionaries"]
		config.conf["speech"]["symbolDictionaries"] = newSymbolDictionaries = [
			d.name
			for i, d in enumerate(self._availableSymbolDictionaries)
			if i in self.symbolDictionariesList.CheckedItems
		]
		if set(currentSymbolDictionaries) != set(newSymbolDictionaries):
			# Either included or excluded symbol dictionaries, so clear the cache.
			characterProcessing.clearSpeechSymbols()
		delayedDescriptions = self.delayedCharacterDescriptionsCheckBox.IsChecked()
		config.conf["speech"]["delayedCharacterDescriptions"] = delayedDescriptions
		config.conf["speech"][self.driver.name]["capPitchChange"] = self.capPitchChangeEdit.Value
		config.conf["speech"][self.driver.name]["sayCapForCapitals"] = self.sayCapForCapsCheckBox.IsChecked()
		config.conf["speech"][self.driver.name]["beepForCapitals"] = self.beepForCapsCheckBox.IsChecked()
		config.conf["speech"][self.driver.name]["useSpellingFunctionality"] = (
			self.useSpellingFunctionalityCheckBox.IsChecked()
		)
		config.conf["speech"]["excludedSpeechModes"] = [
			mIndex
			for mIndex in range(len(self._allSpeechModes))
			if mIndex not in self.speechModesList.CheckedItems
		]

	def _onSpeechModesListChange(self, evt: wx.CommandEvent):
		# continue event propagation to custom control event handler
		# to guarantee user is notified about checkbox being checked or unchecked
		evt.Skip()
		if evt.GetInt() == self._allSpeechModes.index(
			speech.SpeechMode.talk,
		) and not self.speechModesList.IsChecked(evt.GetInt()):
			if (
				gui.messageBox(
					_(
						# Translators: Warning shown when 'talk' speech mode is disabled in settings.
						"You did not choose Talk as one of your speech mode options. "
						"Please note that this may result in no speech output at all. "
						"Are you sure you want to continue?",
					),
					# Translators: Title of the warning message.
					_("Warning"),
					wx.YES | wx.NO | wx.ICON_WARNING,
					self,
				)
				== wx.NO
			):
				self.speechModesList.SetCheckedItems(
					list(self.speechModesList.GetCheckedItems())
					+ [self._allSpeechModes.index(speech.SpeechMode.talk)],
				)

	def _onUnicodeNormalizationChange(self, evt: wx.CommandEvent):
		evt.Skip()
		self.reportNormalizedForCharacterNavigationCheckBox.Enable(
			bool(self.unicodeNormalizationCombo._getControlCurrentFlag()),
		)

	def isValid(self) -> bool:
		enabledSpeechModes = self.speechModesList.CheckedItems
		if len(enabledSpeechModes) < 2:
			log.debugWarning("Too few speech modes enabled.")
			self._validationErrorMessageBox(
				# Translators: Message shown when not enough speech modes are enabled.
				message=_("At least two speech modes have to be checked."),
				# Translators: Same as the label for the list of checkboxes where user can select speech modes that will
				# be available in Speech Settings, but without keyboard accelerator (& character) nor final colon.
				option=_("Modes available in the Cycle speech mode command"),
				category=self.Parent.title,
			)
			return False
		return super().isValid()


class KeyboardSettingsPanel(SettingsPanel):
	# Translators: This is the label for the keyboard settings panel.
	title = _("Keyboard")
	helpId = "KeyboardSettings"

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: This is the label for a combobox in the
		# keyboard settings panel.
		kbdLabelText = _("&Keyboard layout:")
		layouts = keyboardHandler.KeyboardInputGesture.LAYOUTS
		self.kbdNames = sorted(layouts)
		kbdChoices = [layouts[layout] for layout in self.kbdNames]
		self.kbdList = sHelper.addLabeledControl(kbdLabelText, wx.Choice, choices=kbdChoices)
		self.bindHelpEvent("KeyboardSettingsLayout", self.kbdList)
		try:
			index = self.kbdNames.index(config.conf["keyboard"]["keyboardLayout"])
			self.kbdList.SetSelection(index)
		except:  # noqa: E722
			log.debugWarning("Could not set Keyboard layout list to current layout", exc_info=True)

		# Translators: This is the label for a list of checkboxes
		# controlling which keys are NVDA modifier keys.
		modifierBoxLabel = _("&Select NVDA Modifier Keys")
		self.modifierChoices = [key.displayString for key in NVDAKey]
		self.modifierList = sHelper.addLabeledControl(
			modifierBoxLabel,
			nvdaControls.CustomCheckListBox,
			choices=self.modifierChoices,
		)
		checkedItems = []
		for n, key in enumerate(NVDAKey):
			if config.conf["keyboard"]["NVDAModifierKeys"] & key.value:
				checkedItems.append(n)
		self.modifierList.CheckedItems = checkedItems
		self.modifierList.Select(0)

		self.bindHelpEvent("KeyboardSettingsModifiers", self.modifierList)
		# Translators: This is the label for a checkbox in the
		# keyboard settings panel.
		charsText = _("Speak typed &characters")
		self.charsCheckBox = sHelper.addItem(wx.CheckBox(self, label=charsText))
		self.bindHelpEvent(
			"KeyboardSettingsSpeakTypedCharacters",
			self.charsCheckBox,
		)
		self.charsCheckBox.SetValue(config.conf["keyboard"]["speakTypedCharacters"])

		# Translators: This is the label for a checkbox in the
		# keyboard settings panel.
		speakTypedWordsText = _("Speak typed &words")
		self.wordsCheckBox = sHelper.addItem(wx.CheckBox(self, label=speakTypedWordsText))
		self.bindHelpEvent("KeyboardSettingsSpeakTypedWords", self.wordsCheckBox)
		self.wordsCheckBox.SetValue(config.conf["keyboard"]["speakTypedWords"])

		# Translators: This is the label for a checkbox in the
		# keyboard settings panel.
		speechInterruptForCharText = _("Speech &interrupt for typed characters")
		self.speechInterruptForCharsCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=speechInterruptForCharText),
		)
		self.bindHelpEvent(
			"KeyboardSettingsSpeechInteruptForCharacters",
			self.speechInterruptForCharsCheckBox,
		)
		self.speechInterruptForCharsCheckBox.SetValue(config.conf["keyboard"]["speechInterruptForCharacters"])

		# Translators: This is the label for a checkbox in the
		# keyboard settings panel.
		speechInterruptForEnterText = _("Speech i&nterrupt for Enter key")
		self.speechInterruptForEnterCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=speechInterruptForEnterText),
		)
		self.speechInterruptForEnterCheckBox.SetValue(config.conf["keyboard"]["speechInterruptForEnter"])
		self.bindHelpEvent("KeyboardSettingsSpeechInteruptForEnter", self.speechInterruptForEnterCheckBox)

		# Translators: This is the label for a checkbox in the
		# keyboard settings panel.
		allowSkimReadingInSayAllText = _("Allow skim &reading in Say All")
		self.skimReadingInSayAllCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=allowSkimReadingInSayAllText),
		)
		self.bindHelpEvent("KeyboardSettingsSkimReading", self.skimReadingInSayAllCheckBox)

		self.skimReadingInSayAllCheckBox.SetValue(config.conf["keyboard"]["allowSkimReadingInSayAll"])

		# Translators: This is the label for a checkbox in the
		# keyboard settings panel.
		beepForLowercaseWithCapsLockText = _("&Beep if typing lowercase letters when caps lock is on")
		self.beepLowercaseCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=beepForLowercaseWithCapsLockText),
		)
		self.bindHelpEvent("KeyboardSettingsBeepLowercase", self.beepLowercaseCheckBox)
		self.beepLowercaseCheckBox.SetValue(config.conf["keyboard"]["beepForLowercaseWithCapslock"])

		# Translators: This is the label for a checkbox in the
		# keyboard settings panel.
		commandKeysText = _("Speak c&ommand keys")
		self.commandKeysCheckBox = sHelper.addItem(wx.CheckBox(self, label=commandKeysText))
		self.bindHelpEvent("KeyboardSettingsSpeakCommandKeys", self.commandKeysCheckBox)
		self.commandKeysCheckBox.SetValue(config.conf["keyboard"]["speakCommandKeys"])

		# Translators: This is the label for a checkbox in the
		# keyboard settings panel.
		alertForSpellingErrorsText = _("Play sound for &spelling errors while typing")
		self.alertForSpellingErrorsCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=alertForSpellingErrorsText),
		)
		self.bindHelpEvent("KeyboardSettingsAlertForSpellingErrors", self.alertForSpellingErrorsCheckBox)
		self.alertForSpellingErrorsCheckBox.SetValue(config.conf["keyboard"]["alertForSpellingErrors"])
		if not config.conf["documentFormatting"]["reportSpellingErrors"]:
			self.alertForSpellingErrorsCheckBox.Disable()

		# Translators: This is the label for a checkbox in the
		# keyboard settings panel.
		handleInjectedKeysText = _("Handle keys from other &applications")
		self.handleInjectedKeysCheckBox = sHelper.addItem(wx.CheckBox(self, label=handleInjectedKeysText))
		self.bindHelpEvent("KeyboardSettingsHandleKeys", self.handleInjectedKeysCheckBox)
		self.handleInjectedKeysCheckBox.SetValue(config.conf["keyboard"]["handleInjectedKeys"])

		minTimeout = int(config.conf.getConfigValidation(("keyboard", "multiPressTimeout")).kwargs["min"])
		maxTimeout = int(config.conf.getConfigValidation(("keyboard", "multiPressTimeout")).kwargs["max"])
		# Translators: The label for a control in keyboard settings to modify the timeout for a multiple keypress.
		multiPressTimeoutText = _("&Multiple key press timeout (ms):")
		self.multiPressTimeoutEdit = sHelper.addLabeledControl(
			multiPressTimeoutText,
			nvdaControls.SelectOnFocusSpinCtrl,
			min=minTimeout,
			max=maxTimeout,
			initial=config.conf["keyboard"]["multiPressTimeout"],
		)
		self.bindHelpEvent("MultiPressTimeout", self.multiPressTimeoutEdit)

	def isValid(self) -> bool:
		# #2871: check whether at least one key is the nvda key.
		if not self.modifierList.CheckedItems:
			log.debugWarning("No NVDA key set")
			self._validationErrorMessageBox(
				# Translators: Message to report wrong configuration of the NVDA key
				message=_("At least one key must be used as the NVDA key."),
				# Translators: Same as the label for the list of checkboxes controlling which keys are NVDA modifier
				# keys in Keyboard Settings, but without keyboard accelerator (& character).
				option=_("Select NVDA Modifier Keys"),
			)
			return False
		return super().isValid()

	def onSave(self):
		layout = self.kbdNames[self.kbdList.GetSelection()]
		config.conf["keyboard"]["keyboardLayout"] = layout
		config.conf["keyboard"]["NVDAModifierKeys"] = sum(
			key.value for (n, key) in enumerate(NVDAKey) if self.modifierList.IsChecked(n)
		)
		config.conf["keyboard"]["speakTypedCharacters"] = self.charsCheckBox.IsChecked()
		config.conf["keyboard"]["speakTypedWords"] = self.wordsCheckBox.IsChecked()
		config.conf["keyboard"]["speechInterruptForCharacters"] = (
			self.speechInterruptForCharsCheckBox.IsChecked()
		)
		config.conf["keyboard"]["speechInterruptForEnter"] = self.speechInterruptForEnterCheckBox.IsChecked()
		config.conf["keyboard"]["allowSkimReadingInSayAll"] = self.skimReadingInSayAllCheckBox.IsChecked()
		config.conf["keyboard"]["beepForLowercaseWithCapslock"] = self.beepLowercaseCheckBox.IsChecked()
		config.conf["keyboard"]["speakCommandKeys"] = self.commandKeysCheckBox.IsChecked()
		config.conf["keyboard"]["alertForSpellingErrors"] = self.alertForSpellingErrorsCheckBox.IsChecked()
		config.conf["keyboard"]["handleInjectedKeys"] = self.handleInjectedKeysCheckBox.IsChecked()
		config.conf["keyboard"]["multiPressTimeout"] = self.multiPressTimeoutEdit.GetValue()


class MouseSettingsPanel(SettingsPanel):
	# Translators: This is the label for the mouse settings panel.
	title = _("Mouse")
	helpId = "MouseSettings"

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		# Translators: This is the label for a checkbox in the
		# mouse settings panel.
		shapeChangesText = _("Report mouse &shape changes")
		self.shapeCheckBox = sHelper.addItem(wx.CheckBox(self, label=shapeChangesText))
		self.bindHelpEvent("MouseSettingsShape", self.shapeCheckBox)
		self.shapeCheckBox.SetValue(config.conf["mouse"]["reportMouseShapeChanges"])

		# Translators: This is the label for a checkbox in the
		# mouse settings panel.
		mouseTrackingText = _("Enable mouse &tracking")
		self.mouseTrackingCheckBox = sHelper.addItem(wx.CheckBox(self, label=mouseTrackingText))
		self.bindHelpEvent("MouseSettingsTracking", self.mouseTrackingCheckBox)
		self.mouseTrackingCheckBox.SetValue(config.conf["mouse"]["enableMouseTracking"])

		# Translators: This is the label for a combobox in the
		# mouse settings panel.
		textUnitLabelText = _("Text &unit resolution:")
		import textInfos

		self.textUnits = textInfos.MOUSE_TEXT_RESOLUTION_UNITS
		textUnitsChoices = [textInfos.unitLabels[x] for x in self.textUnits]
		self.textUnitComboBox = sHelper.addLabeledControl(
			textUnitLabelText,
			wx.Choice,
			choices=textUnitsChoices,
		)
		self.bindHelpEvent("MouseSettingsTextUnit", self.textUnitComboBox)
		try:
			index = self.textUnits.index(config.conf["mouse"]["mouseTextUnit"])
		except:  # noqa: E722
			index = 0
		self.textUnitComboBox.SetSelection(index)

		# Translators: This is the label for a checkbox in the
		# mouse settings panel.
		reportObjectPropertiesText = _("Report &object when mouse enters it")
		self.reportObjectPropertiesCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=reportObjectPropertiesText),
		)
		self.bindHelpEvent("MouseSettingsRole", self.reportObjectPropertiesCheckBox)
		self.reportObjectPropertiesCheckBox.SetValue(config.conf["mouse"]["reportObjectRoleOnMouseEnter"])

		# Translators: This is the label for a checkbox in the
		# mouse settings panel.
		audioText = _("&Play audio coordinates when mouse moves")
		self.audioCheckBox = sHelper.addItem(wx.CheckBox(self, label=audioText))
		self.bindHelpEvent("MouseSettingsAudio", self.audioCheckBox)
		self.audioCheckBox.SetValue(config.conf["mouse"]["audioCoordinatesOnMouseMove"])

		# Translators: This is the label for a checkbox in the
		# mouse settings panel.
		audioDetectBrightnessText = _("&Brightness controls audio coordinates volume")
		self.audioDetectBrightnessCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=audioDetectBrightnessText),
		)
		self.bindHelpEvent("MouseSettingsBrightness", self.audioDetectBrightnessCheckBox)
		self.audioDetectBrightnessCheckBox.SetValue(config.conf["mouse"]["audioCoordinates_detectBrightness"])

		# Translators: This is the label for a checkbox in the
		# mouse settings panel.
		ignoreInjectedMouseInputText = _("Ignore mouse input from other &applications")
		self.ignoreInjectedMouseInputCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=ignoreInjectedMouseInputText),
		)
		self.bindHelpEvent("MouseSettingsHandleMouseControl", self.ignoreInjectedMouseInputCheckBox)
		self.ignoreInjectedMouseInputCheckBox.SetValue(config.conf["mouse"]["ignoreInjectedMouseInput"])

	def onSave(self):
		config.conf["mouse"]["reportMouseShapeChanges"] = self.shapeCheckBox.IsChecked()
		config.conf["mouse"]["enableMouseTracking"] = self.mouseTrackingCheckBox.IsChecked()
		config.conf["mouse"]["mouseTextUnit"] = self.textUnits[self.textUnitComboBox.GetSelection()]
		config.conf["mouse"]["reportObjectRoleOnMouseEnter"] = self.reportObjectPropertiesCheckBox.IsChecked()
		config.conf["mouse"]["audioCoordinatesOnMouseMove"] = self.audioCheckBox.IsChecked()
		config.conf["mouse"]["audioCoordinates_detectBrightness"] = (
			self.audioDetectBrightnessCheckBox.IsChecked()
		)
		config.conf["mouse"]["ignoreInjectedMouseInput"] = self.ignoreInjectedMouseInputCheckBox.IsChecked()


class ReviewCursorPanel(SettingsPanel):
	# Translators: This is the label for the review cursor settings panel.
	title = _("Review Cursor")
	helpId = "ReviewCursorSettings"

	def makeSettings(self, settingsSizer):
		# Translators: This is the label for a checkbox in the
		# review cursor settings panel.
		self.followFocusCheckBox = wx.CheckBox(self, label=_("Follow system &focus"))
		self.bindHelpEvent("ReviewCursorFollowFocus", self.followFocusCheckBox)
		self.followFocusCheckBox.SetValue(config.conf["reviewCursor"]["followFocus"])
		settingsSizer.Add(self.followFocusCheckBox, border=10, flag=wx.BOTTOM)
		# Translators: This is the label for a checkbox in the
		# review cursor settings panel.
		self.followCaretCheckBox = wx.CheckBox(self, label=_("Follow System &Caret"))
		self.bindHelpEvent("ReviewCursorFollowCaret", self.followCaretCheckBox)
		self.followCaretCheckBox.SetValue(config.conf["reviewCursor"]["followCaret"])
		settingsSizer.Add(self.followCaretCheckBox, border=10, flag=wx.BOTTOM)
		# Translators: This is the label for a checkbox in the
		# review cursor settings panel.
		self.followMouseCheckBox = wx.CheckBox(self, label=_("Follow &mouse cursor"))
		self.bindHelpEvent("ReviewCursorFollowMouse", self.followMouseCheckBox)
		self.followMouseCheckBox.SetValue(config.conf["reviewCursor"]["followMouse"])
		settingsSizer.Add(self.followMouseCheckBox, border=10, flag=wx.BOTTOM)
		# Translators: This is the label for a checkbox in the
		# review cursor settings panel.
		self.simpleReviewModeCheckBox = wx.CheckBox(self, label=_("&Simple review mode"))
		self.bindHelpEvent("ReviewCursorSimple", self.simpleReviewModeCheckBox)
		self.simpleReviewModeCheckBox.SetValue(config.conf["reviewCursor"]["simpleReviewMode"])
		settingsSizer.Add(self.simpleReviewModeCheckBox, border=10, flag=wx.BOTTOM)

	def onSave(self):
		config.conf["reviewCursor"]["followFocus"] = self.followFocusCheckBox.IsChecked()
		config.conf["reviewCursor"]["followCaret"] = self.followCaretCheckBox.IsChecked()
		config.conf["reviewCursor"]["followMouse"] = self.followMouseCheckBox.IsChecked()
		config.conf["reviewCursor"]["simpleReviewMode"] = self.simpleReviewModeCheckBox.IsChecked()


class InputCompositionPanel(SettingsPanel):
	# Translators: This is the label for the Input Composition settings panel.
	title = _("Input Composition")
	helpId = "InputCompositionSettings"

	def makeSettings(self, settingsSizer):
		self.autoReportAllCandidatesCheckBox = wx.CheckBox(
			self,
			wx.ID_ANY,
			# Translators: This is the label for a checkbox in the
			# Input composition settings panel.
			label=_("Automatically report all available &candidates"),
		)
		self.bindHelpEvent("InputCompositionReportAllCandidates", self.autoReportAllCandidatesCheckBox)
		self.autoReportAllCandidatesCheckBox.SetValue(
			config.conf["inputComposition"]["autoReportAllCandidates"],
		)
		settingsSizer.Add(self.autoReportAllCandidatesCheckBox, border=10, flag=wx.BOTTOM)
		self.announceSelectedCandidateCheckBox = wx.CheckBox(
			self,
			wx.ID_ANY,
			# Translators: This is the label for a checkbox in the
			# Input composition settings panel.
			label=_("Announce &selected candidate"),
		)
		self.bindHelpEvent(
			"InputCompositionAnnounceSelectedCandidate",
			self.announceSelectedCandidateCheckBox,
		)
		self.announceSelectedCandidateCheckBox.SetValue(
			config.conf["inputComposition"]["announceSelectedCandidate"],
		)
		settingsSizer.Add(self.announceSelectedCandidateCheckBox, border=10, flag=wx.BOTTOM)
		self.candidateIncludesShortCharacterDescriptionCheckBox = wx.CheckBox(
			self,
			wx.ID_ANY,
			# Translators: This is the label for a checkbox in the
			# Input composition settings panel.
			label=_("Always include short character &description when announcing candidates"),
		)
		self.bindHelpEvent(
			"InputCompositionCandidateIncludesShortCharacterDescription",
			self.candidateIncludesShortCharacterDescriptionCheckBox,
		)
		self.candidateIncludesShortCharacterDescriptionCheckBox.SetValue(
			config.conf["inputComposition"]["alwaysIncludeShortCharacterDescriptionInCandidateName"],
		)
		settingsSizer.Add(self.candidateIncludesShortCharacterDescriptionCheckBox, border=10, flag=wx.BOTTOM)
		self.reportReadingStringChangesCheckBox = wx.CheckBox(
			self,
			wx.ID_ANY,
			# Translators: This is the label for a checkbox in the
			# Input composition settings panel.
			label=_("Report changes to the &reading string"),
		)
		self.bindHelpEvent(
			"InputCompositionReadingStringChanges",
			self.reportReadingStringChangesCheckBox,
		)
		self.reportReadingStringChangesCheckBox.SetValue(
			config.conf["inputComposition"]["reportReadingStringChanges"],
		)
		settingsSizer.Add(self.reportReadingStringChangesCheckBox, border=10, flag=wx.BOTTOM)
		self.reportCompositionStringChangesCheckBox = wx.CheckBox(
			self,
			wx.ID_ANY,
			# Translators: This is the label for a checkbox in the
			# Input composition settings panel.
			label=_("Report changes to the &composition string"),
		)
		self.bindHelpEvent(
			"InputCompositionCompositionStringChanges",
			self.reportCompositionStringChangesCheckBox,
		)
		self.reportCompositionStringChangesCheckBox.SetValue(
			config.conf["inputComposition"]["reportCompositionStringChanges"],
		)
		settingsSizer.Add(self.reportCompositionStringChangesCheckBox, border=10, flag=wx.BOTTOM)

	def onSave(self):
		config.conf["inputComposition"]["autoReportAllCandidates"] = (
			self.autoReportAllCandidatesCheckBox.IsChecked()
		)
		config.conf["inputComposition"]["announceSelectedCandidate"] = (
			self.announceSelectedCandidateCheckBox.IsChecked()
		)
		config.conf["inputComposition"]["alwaysIncludeShortCharacterDescriptionInCandidateName"] = (
			self.candidateIncludesShortCharacterDescriptionCheckBox.IsChecked()
		)
		config.conf["inputComposition"]["reportReadingStringChanges"] = (
			self.reportReadingStringChangesCheckBox.IsChecked()
		)
		config.conf["inputComposition"]["reportCompositionStringChanges"] = (
			self.reportCompositionStringChangesCheckBox.IsChecked()
		)


class ObjectPresentationPanel(SettingsPanel):
	panelDescription = _(
		# Translators: This is a label appearing on the Object Presentation settings panel.
		"Configure how much information NVDA will present about controls."
		" These options apply to focus reporting and NVDA object navigation,"
		" but not when reading text content e.g. web content with browse mode.",
	)

	# Translators: This is the label for the object presentation panel.
	title = _("Object Presentation")
	helpId = "ObjectPresentationSettings"
	progressLabels = (
		# Translators: An option for progress bar output in the Object Presentation dialog
		# which disables reporting of progress bars.
		# See Progress bar output in the Object Presentation Settings section of the User Guide.
		("off", _("off")),
		# Translators: An option for progress bar output in the Object Presentation dialog
		# which reports progress bar updates by speaking.
		# See Progress bar output in the Object Presentation Settings section of the User Guide.
		("speak", _("Speak")),
		# Translators: An option for progress bar output in the Object Presentation dialog
		# which reports progress bar updates by beeping.
		# See Progress bar output in the Object Presentation Settings section of the User Guide.
		("beep", _("Beep")),
		# Translators: An option for progress bar output in the Object Presentation dialog
		# which reports progress bar updates by both speaking and beeping.
		# See Progress bar output in the Object Presentation Settings section of the User Guide.
		("both", _("Speak and beep")),
	)

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		self.windowText = sHelper.addItem(
			wx.StaticText(self, label=self.panelDescription),
		)
		self.windowText.Wrap(self.scaleSize(PANEL_DESCRIPTION_WIDTH))

		# Translators: This is the label for a checkbox in the
		# object presentation settings panel.
		reportToolTipsText = _("Report &tooltips")
		self.tooltipCheckBox = sHelper.addItem(wx.CheckBox(self, label=reportToolTipsText))
		self.bindHelpEvent("ObjectPresentationReportToolTips", self.tooltipCheckBox)
		self.tooltipCheckBox.SetValue(config.conf["presentation"]["reportTooltips"])

		# Translators: This is the label for a checkbox in the
		# object presentation settings panel.
		balloonText = _("Report &notifications")
		self.balloonCheckBox = sHelper.addItem(wx.CheckBox(self, label=balloonText))
		self.bindHelpEvent("ObjectPresentationReportNotifications", self.balloonCheckBox)
		self.balloonCheckBox.SetValue(config.conf["presentation"]["reportHelpBalloons"])

		# Translators: This is the label for a checkbox in the
		# object presentation settings panel.
		shortcutText = _("Report object shortcut &keys")
		self.shortcutCheckBox = sHelper.addItem(wx.CheckBox(self, label=shortcutText))
		self.bindHelpEvent("ObjectPresentationShortcutKeys", self.shortcutCheckBox)
		self.shortcutCheckBox.SetValue(config.conf["presentation"]["reportKeyboardShortcuts"])

		# Translators: This is the label for a checkbox in the
		# object presentation settings panel.
		positionInfoText = _("Report object &position information")
		self.positionInfoCheckBox = sHelper.addItem(wx.CheckBox(self, label=positionInfoText))
		self.bindHelpEvent("ObjectPresentationPositionInfo", self.positionInfoCheckBox)
		self.positionInfoCheckBox.SetValue(config.conf["presentation"]["reportObjectPositionInformation"])

		# Translators: This is the label for a checkbox in the
		# object presentation settings panel.
		guessPositionInfoText = _("&Guess object position information when unavailable")
		self.guessPositionInfoCheckBox = sHelper.addItem(wx.CheckBox(self, label=guessPositionInfoText))
		self.bindHelpEvent("ObjectPresentationGuessPositionInfo", self.guessPositionInfoCheckBox)
		self.guessPositionInfoCheckBox.SetValue(
			config.conf["presentation"]["guessObjectPositionInformationWhenUnavailable"],
		)

		# Translators: This is the label for a checkbox in the
		# object presentation settings panel.
		descriptionText = _("Report object &descriptions")
		self.descriptionCheckBox = sHelper.addItem(wx.CheckBox(self, label=descriptionText))
		self.bindHelpEvent("ObjectPresentationReportDescriptions", self.descriptionCheckBox)
		self.descriptionCheckBox.SetValue(config.conf["presentation"]["reportObjectDescriptions"])

		# Translators: This is the label for a combobox in the
		# object presentation settings panel.
		progressLabelText = _("Progress &bar output:")
		progressChoices = [name for setting, name in self.progressLabels]
		self.progressList = sHelper.addLabeledControl(progressLabelText, wx.Choice, choices=progressChoices)
		self.bindHelpEvent("ObjectPresentationProgressBarOutput", self.progressList)
		for index, (setting, name) in enumerate(self.progressLabels):
			if setting == config.conf["presentation"]["progressBarUpdates"]["progressBarOutputMode"]:
				self.progressList.SetSelection(index)
				break
		else:
			log.debugWarning("Could not set progress list to current report progress bar updates setting")

		# Translators: This is the label for a checkbox in the
		# object presentation settings panel.
		reportBackgroundProgressBarsText = _("Report backg&round progress bars")
		self.reportBackgroundProgressBarsCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=reportBackgroundProgressBarsText),
		)
		self.bindHelpEvent(
			"ObjectPresentationReportBackgroundProgressBars",
			self.reportBackgroundProgressBarsCheckBox,
		)
		self.reportBackgroundProgressBarsCheckBox.SetValue(
			config.conf["presentation"]["progressBarUpdates"]["reportBackgroundProgressBars"],
		)

		# Translators: This is the label for a checkbox in the
		# object presentation settings panel.
		dynamicContentText = _("Report dynamic &content changes")
		self.dynamicContentCheckBox = sHelper.addItem(wx.CheckBox(self, label=dynamicContentText))
		self.bindHelpEvent(
			"ObjectPresentationReportDynamicContent",
			self.dynamicContentCheckBox,
		)
		self.dynamicContentCheckBox.SetValue(config.conf["presentation"]["reportDynamicContentChanges"])

		# Translators: This is the label for a checkbox in the
		# object presentation settings panel.
		autoSuggestionsLabelText = _("Play a sound when &auto-suggestions appear")
		self.autoSuggestionSoundsCheckBox = sHelper.addItem(wx.CheckBox(self, label=autoSuggestionsLabelText))
		self.bindHelpEvent(
			"ObjectPresentationSuggestionSounds",
			self.autoSuggestionSoundsCheckBox,
		)
		self.autoSuggestionSoundsCheckBox.SetValue(
			config.conf["presentation"]["reportAutoSuggestionsWithSound"],
		)

	def onSave(self):
		config.conf["presentation"]["reportTooltips"] = self.tooltipCheckBox.IsChecked()
		config.conf["presentation"]["reportHelpBalloons"] = self.balloonCheckBox.IsChecked()
		config.conf["presentation"]["reportKeyboardShortcuts"] = self.shortcutCheckBox.IsChecked()
		config.conf["presentation"]["reportObjectPositionInformation"] = self.positionInfoCheckBox.IsChecked()
		config.conf["presentation"]["guessObjectPositionInformationWhenUnavailable"] = (
			self.guessPositionInfoCheckBox.IsChecked()
		)
		config.conf["presentation"]["reportObjectDescriptions"] = self.descriptionCheckBox.IsChecked()
		config.conf["presentation"]["progressBarUpdates"]["progressBarOutputMode"] = self.progressLabels[
			self.progressList.GetSelection()
		][0]
		config.conf["presentation"]["progressBarUpdates"]["reportBackgroundProgressBars"] = (
			self.reportBackgroundProgressBarsCheckBox.IsChecked()
		)
		config.conf["presentation"]["reportDynamicContentChanges"] = self.dynamicContentCheckBox.IsChecked()
		config.conf["presentation"]["reportAutoSuggestionsWithSound"] = (
			self.autoSuggestionSoundsCheckBox.IsChecked()
		)


class BrowseModePanel(SettingsPanel):
	# Translators: This is the label for the browse mode settings panel.
	title = _("Browse Mode")
	helpId = "BrowseModeSettings"

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: This is the label for a textfield in the
		# browse mode settings panel.
		maxLengthLabelText = _("&Maximum number of characters on one line")
		self.maxLengthEdit = sHelper.addLabeledControl(
			maxLengthLabelText,
			nvdaControls.SelectOnFocusSpinCtrl,
			# min and max are not enforced in the config for virtualBuffers.maxLineLength
			min=10,
			max=250,
			initial=config.conf["virtualBuffers"]["maxLineLength"],
		)
		self.bindHelpEvent("BrowseModeSettingsMaxLength", self.maxLengthEdit)

		# Translators: This is the label for a textfield in the
		# browse mode settings panel.
		pageLinesLabelText = _("&Number of lines per page")
		self.pageLinesEdit = sHelper.addLabeledControl(
			pageLinesLabelText,
			nvdaControls.SelectOnFocusSpinCtrl,
			# min and max are not enforced in the config for virtualBuffers.linesPerPage
			min=5,
			max=150,
			initial=config.conf["virtualBuffers"]["linesPerPage"],
		)
		self.bindHelpEvent("BrowseModeSettingsPageLines", self.pageLinesEdit)

		# Translators: This is the label for a checkbox in the
		# browse mode settings panel.
		useScreenLayoutText = _("Use &screen layout (when supported)")
		self.useScreenLayoutCheckBox = sHelper.addItem(wx.CheckBox(self, label=useScreenLayoutText))
		self.bindHelpEvent("BrowseModeSettingsScreenLayout", self.useScreenLayoutCheckBox)
		self.useScreenLayoutCheckBox.SetValue(config.conf["virtualBuffers"]["useScreenLayout"])

		# Translators: The label for a checkbox in browse mode settings to
		# enable browse mode on page load.
		enableOnPageLoadText = _("&Enable browse mode on page load")
		self.enableOnPageLoadCheckBox = sHelper.addItem(wx.CheckBox(self, label=enableOnPageLoadText))
		self.bindHelpEvent("BrowseModeSettingsEnableOnPageLoad", self.enableOnPageLoadCheckBox)
		self.enableOnPageLoadCheckBox.SetValue(config.conf["virtualBuffers"]["enableOnPageLoad"])

		# Translators: This is the label for a checkbox in the
		# browse mode settings panel.
		autoSayAllText = _("Automatic &Say All on page load")
		self.autoSayAllCheckBox = sHelper.addItem(wx.CheckBox(self, label=autoSayAllText))
		self.bindHelpEvent("BrowseModeSettingsAutoSayAll", self.autoSayAllCheckBox)
		self.autoSayAllCheckBox.SetValue(config.conf["virtualBuffers"]["autoSayAllOnPageLoad"])

		# Translators: This is the label for a checkbox in the
		# browse mode settings panel.
		layoutTablesText = _("Include l&ayout tables")
		self.layoutTablesCheckBox = sHelper.addItem(wx.CheckBox(self, label=layoutTablesText))
		self.bindHelpEvent("BrowseModeSettingsIncludeLayoutTables", self.layoutTablesCheckBox)
		self.layoutTablesCheckBox.SetValue(config.conf["documentFormatting"]["includeLayoutTables"])

		# Translators: This is the label for a checkbox in the
		# browse mode settings panel.
		autoPassThroughOnFocusChangeText = _("Automatic focus mode for focus changes")
		self.autoPassThroughOnFocusChangeCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=autoPassThroughOnFocusChangeText),
		)
		self.bindHelpEvent(
			"BrowseModeSettingsAutoPassThroughOnFocusChange",
			self.autoPassThroughOnFocusChangeCheckBox,
		)
		self.autoPassThroughOnFocusChangeCheckBox.SetValue(
			config.conf["virtualBuffers"]["autoPassThroughOnFocusChange"],
		)

		# Translators: This is the label for a checkbox in the
		# browse mode settings panel.
		autoPassThroughOnCaretMoveText = _("Automatic focus mode for caret movement")
		self.autoPassThroughOnCaretMoveCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=autoPassThroughOnCaretMoveText),
		)
		self.bindHelpEvent(
			"BrowseModeSettingsAutoPassThroughOnCaretMove",
			self.autoPassThroughOnCaretMoveCheckBox,
		)
		self.autoPassThroughOnCaretMoveCheckBox.SetValue(
			config.conf["virtualBuffers"]["autoPassThroughOnCaretMove"],
		)

		# Translators: This is the label for a checkbox in the
		# browse mode settings panel.
		passThroughAudioIndicationText = _("Audio indication of focus and browse modes")
		self.passThroughAudioIndicationCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=passThroughAudioIndicationText),
		)
		self.bindHelpEvent(
			"BrowseModeSettingsPassThroughAudioIndication",
			self.passThroughAudioIndicationCheckBox,
		)
		self.passThroughAudioIndicationCheckBox.SetValue(
			config.conf["virtualBuffers"]["passThroughAudioIndication"],
		)

		# Translators: This is the label for a checkbox in the
		# browse mode settings panel.
		trapNonCommandGesturesText = _("&Trap all non-command gestures from reaching the document")
		self.trapNonCommandGesturesCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=trapNonCommandGesturesText),
		)
		self.bindHelpEvent(
			"BrowseModeSettingsTrapNonCommandGestures",
			self.trapNonCommandGesturesCheckBox,
		)
		self.trapNonCommandGesturesCheckBox.SetValue(config.conf["virtualBuffers"]["trapNonCommandGestures"])

		# Translators: This is the label for a checkbox in the
		# browse mode settings panel.
		autoFocusFocusableElementsText = _("Automatically set system &focus to focusable elements")
		self.autoFocusFocusableElementsCheckBox = sHelper.addItem(
			wx.CheckBox(self, label=autoFocusFocusableElementsText),
		)
		self.bindHelpEvent(
			"BrowseModeSettingsAutoFocusFocusableElements",
			self.autoFocusFocusableElementsCheckBox,
		)
		self.autoFocusFocusableElementsCheckBox.SetValue(
			config.conf["virtualBuffers"]["autoFocusFocusableElements"],
		)

	def onSave(self):
		config.conf["virtualBuffers"]["maxLineLength"] = self.maxLengthEdit.GetValue()
		config.conf["virtualBuffers"]["linesPerPage"] = self.pageLinesEdit.GetValue()
		config.conf["virtualBuffers"]["useScreenLayout"] = self.useScreenLayoutCheckBox.IsChecked()
		config.conf["virtualBuffers"]["enableOnPageLoad"] = self.enableOnPageLoadCheckBox.IsChecked()
		config.conf["virtualBuffers"]["autoSayAllOnPageLoad"] = self.autoSayAllCheckBox.IsChecked()
		config.conf["documentFormatting"]["includeLayoutTables"] = self.layoutTablesCheckBox.IsChecked()
		config.conf["virtualBuffers"]["autoPassThroughOnFocusChange"] = (
			self.autoPassThroughOnFocusChangeCheckBox.IsChecked()
		)
		config.conf["virtualBuffers"]["autoPassThroughOnCaretMove"] = (
			self.autoPassThroughOnCaretMoveCheckBox.IsChecked()
		)
		config.conf["virtualBuffers"]["passThroughAudioIndication"] = (
			self.passThroughAudioIndicationCheckBox.IsChecked()
		)
		config.conf["virtualBuffers"]["trapNonCommandGestures"] = (
			self.trapNonCommandGesturesCheckBox.IsChecked()
		)
		config.conf["virtualBuffers"]["autoFocusFocusableElements"] = (
			self.autoFocusFocusableElementsCheckBox.IsChecked()
		)


class DocumentFormattingPanel(SettingsPanel):
	# Translators: This is the label for the document formatting panel.
	title = _("Document Formatting")
	helpId = "DocumentFormattingSettings"

	# Translators: This is a label appearing on the document formatting settings panel.
	panelDescription = _("The following options control the types of document formatting reported by NVDA.")

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		sHelper.addItem(wx.StaticText(self, label=self.panelDescription))

		# Translators: This is the label for a group of document formatting options in the
		# document formatting settings panel
		fontGroupText = _("Font")
		fontGroupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=fontGroupText)
		fontGroupBox = fontGroupSizer.GetStaticBox()
		fontGroup = guiHelper.BoxSizerHelper(self, sizer=fontGroupSizer)
		sHelper.addItem(fontGroup)

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		fontNameText = _("&Font name")
		self.fontNameCheckBox = fontGroup.addItem(wx.CheckBox(fontGroupBox, label=fontNameText))
		self.fontNameCheckBox.SetValue(config.conf["documentFormatting"]["reportFontName"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		fontSizeText = _("Font &size")
		self.fontSizeCheckBox = fontGroup.addItem(wx.CheckBox(fontGroupBox, label=fontSizeText))
		self.fontSizeCheckBox.SetValue(config.conf["documentFormatting"]["reportFontSize"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		fontAttributesText = _("Font attrib&utes")
		fontAttributesOptions = [i.displayString for i in OutputMode.__members__.values()]
		self.fontAttrsList = fontGroup.addLabeledControl(
			fontAttributesText,
			wx.Choice,
			choices=fontAttributesOptions,
		)
		self.bindHelpEvent("DocumentFormattingFontAttributes", self.fontAttrsList)
		self.fontAttrsList.SetSelection(config.conf["documentFormatting"]["fontAttributeReporting"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		superscriptsAndSubscriptsText = _("Su&perscripts and subscripts")
		self.superscriptsAndSubscriptsCheckBox = fontGroup.addItem(
			wx.CheckBox(fontGroupBox, label=superscriptsAndSubscriptsText),
		)
		self.superscriptsAndSubscriptsCheckBox.SetValue(
			config.conf["documentFormatting"]["reportSuperscriptsAndSubscripts"],
		)

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		emphasisText = _("E&mphasis")
		self.emphasisCheckBox = fontGroup.addItem(wx.CheckBox(fontGroupBox, label=emphasisText))
		self.emphasisCheckBox.SetValue(config.conf["documentFormatting"]["reportEmphasis"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		highlightText = _("Highlighted (mar&ked) text")
		self.highlightCheckBox = fontGroup.addItem(
			wx.CheckBox(fontGroupBox, label=highlightText),
		)
		self.highlightCheckBox.SetValue(
			config.conf["documentFormatting"]["reportHighlight"],
		)

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		styleText = _("St&yle")
		self.styleCheckBox = fontGroup.addItem(wx.CheckBox(fontGroupBox, label=styleText))
		self.styleCheckBox.SetValue(config.conf["documentFormatting"]["reportStyle"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		colorsText = _("&Colors")
		self.colorCheckBox = fontGroup.addItem(wx.CheckBox(fontGroupBox, label=colorsText))
		self.colorCheckBox.SetValue(config.conf["documentFormatting"]["reportColor"])

		# Translators: This is the label for a group of document formatting options in the
		# document formatting settings panel
		documentInfoGroupText = _("Document information")
		docInfoSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=documentInfoGroupText)
		docInfoBox = docInfoSizer.GetStaticBox()
		docInfoGroup = guiHelper.BoxSizerHelper(self, sizer=docInfoSizer)
		sHelper.addItem(docInfoGroup)

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		commentsText = _("No&tes and comments")
		self.commentsCheckBox = docInfoGroup.addItem(wx.CheckBox(docInfoBox, label=commentsText))
		self.commentsCheckBox.SetValue(config.conf["documentFormatting"]["reportComments"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		bookmarksText = _("&Bookmarks")
		self.bookmarksCheckBox = docInfoGroup.addItem(wx.CheckBox(docInfoBox, label=bookmarksText))
		self.bookmarksCheckBox.SetValue(config.conf["documentFormatting"]["reportBookmarks"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		revisionsText = _("&Editor revisions")
		self.revisionsCheckBox = docInfoGroup.addItem(wx.CheckBox(docInfoBox, label=revisionsText))
		self.revisionsCheckBox.SetValue(config.conf["documentFormatting"]["reportRevisions"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		spellingErrorText = _("Spelling e&rrors")
		self.spellingErrorsCheckBox = docInfoGroup.addItem(wx.CheckBox(docInfoBox, label=spellingErrorText))
		self.spellingErrorsCheckBox.SetValue(config.conf["documentFormatting"]["reportSpellingErrors"])

		# Translators: This is the label for a group of document formatting options in the
		# document formatting settings panel
		pageAndSpaceGroupText = _("Pages and spacing")
		pageAndSpaceSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=pageAndSpaceGroupText)
		pageAndSpaceBox = pageAndSpaceSizer.GetStaticBox()
		pageAndSpaceGroup = guiHelper.BoxSizerHelper(self, sizer=pageAndSpaceSizer)
		sHelper.addItem(pageAndSpaceGroup)

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		pageText = _("&Pages")
		self.pageCheckBox = pageAndSpaceGroup.addItem(wx.CheckBox(pageAndSpaceBox, label=pageText))
		self.pageCheckBox.SetValue(config.conf["documentFormatting"]["reportPage"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		lineText = _("Line &numbers")
		self.lineNumberCheckBox = pageAndSpaceGroup.addItem(wx.CheckBox(pageAndSpaceBox, label=lineText))
		self.lineNumberCheckBox.SetValue(config.conf["documentFormatting"]["reportLineNumber"])

		lineIndentationChoices = [i.displayString for i in ReportLineIndentation]
		self.lineIndentationCombo = pageAndSpaceGroup.addLabeledControl(
			# Translators: This is the label for a combobox controlling the reporting of line indentation in the
			# Document  Formatting  dialog (possible choices are Off, Speech, Tones, or Both.
			_("Line &indentation reporting:"),
			wx.Choice,
			choices=lineIndentationChoices,
		)
		self.bindHelpEvent(
			"DocumentFormattingSettingsLineIndentation",
			self.lineIndentationCombo,
		)
		self.lineIndentationCombo.Bind(wx.EVT_CHOICE, self._onLineIndentationChange)
		reportLineIndentation = config.conf["documentFormatting"]["reportLineIndentation"]
		self.lineIndentationCombo.SetSelection(reportLineIndentation)

		# Translators: This is the label of a checkbox in the document formatting settings panel
		# If this option is selected, NVDA will ignore blank lines for line indentation reporting
		ignoreBlankLinesText = _("Ignore &blank lines for line indentation reporting")
		ignoreBlankLinesCheckBox = wx.CheckBox(pageAndSpaceBox, label=ignoreBlankLinesText)
		self.ignoreBlankLinesRLICheckbox = pageAndSpaceGroup.addItem(ignoreBlankLinesCheckBox)
		self.bindHelpEvent(
			"DocumentFormattingSettingsLineIndentation",
			self.ignoreBlankLinesRLICheckbox,
		)
		self.ignoreBlankLinesRLICheckbox.SetValue(config.conf["documentFormatting"]["ignoreBlankLinesForRLI"])
		self.ignoreBlankLinesRLICheckbox.Enable(reportLineIndentation != 0)

		# Translators: This message is presented in the document formatting settings panel
		# If this option is selected, NVDA will report paragraph indentation if available.
		paragraphIndentationText = _("&Paragraph indentation")
		_paragraphIndentationCheckBox = wx.CheckBox(pageAndSpaceBox, label=paragraphIndentationText)
		self.paragraphIndentationCheckBox = pageAndSpaceGroup.addItem(_paragraphIndentationCheckBox)
		self.paragraphIndentationCheckBox.SetValue(
			config.conf["documentFormatting"]["reportParagraphIndentation"],
		)

		# Translators: This message is presented in the document formatting settings panel
		# If this option is selected, NVDA will report line spacing if available.
		lineSpacingText = _("&Line spacing")
		_lineSpacingCheckBox = wx.CheckBox(pageAndSpaceBox, label=lineSpacingText)
		self.lineSpacingCheckBox = pageAndSpaceGroup.addItem(_lineSpacingCheckBox)
		self.lineSpacingCheckBox.SetValue(config.conf["documentFormatting"]["reportLineSpacing"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		alignmentText = _("&Alignment")
		self.alignmentCheckBox = pageAndSpaceGroup.addItem(wx.CheckBox(pageAndSpaceBox, label=alignmentText))
		self.alignmentCheckBox.SetValue(config.conf["documentFormatting"]["reportAlignment"])

		# Translators: This is the label for a group of document formatting options in the
		# document formatting settings panel
		tablesGroupText = _("Table information")
		tablesGroupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=tablesGroupText)
		tablesGroupBox = tablesGroupSizer.GetStaticBox()
		tablesGroup = guiHelper.BoxSizerHelper(self, sizer=tablesGroupSizer)
		sHelper.addItem(tablesGroup)

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		self.tablesCheckBox = tablesGroup.addItem(wx.CheckBox(tablesGroupBox, label=_("&Tables")))
		self.tablesCheckBox.SetValue(config.conf["documentFormatting"]["reportTables"])

		tableHeaderChoices = [i.displayString for i in ReportTableHeaders]
		self.tableHeadersComboBox = tablesGroup.addLabeledControl(
			# Translators: This is the label for a combobox in the
			# document formatting settings panel.
			_("H&eaders"),
			wx.Choice,
			choices=tableHeaderChoices,
		)
		self.tableHeadersComboBox.SetSelection(config.conf["documentFormatting"]["reportTableHeaders"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		_tableCellCoordsCheckBox = wx.CheckBox(tablesGroupBox, label=_("Cell c&oordinates"))
		self.tableCellCoordsCheckBox = tablesGroup.addItem(_tableCellCoordsCheckBox)
		self.tableCellCoordsCheckBox.SetValue(config.conf["documentFormatting"]["reportTableCellCoords"])

		borderChoices = [i.displayString for i in ReportCellBorders]
		self.borderComboBox = tablesGroup.addLabeledControl(
			# Translators: This is the label for a combobox in the
			# document formatting settings panel.
			_("Cell &borders:"),
			wx.Choice,
			choices=borderChoices,
		)
		self.borderComboBox.SetSelection(config.conf["documentFormatting"]["reportCellBorders"])

		# Translators: This is the label for a group of document formatting options in the
		# document formatting settings panel
		elementsGroupText = _("Elements")
		elementsGroupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=elementsGroupText)
		elementsGroupBox = elementsGroupSizer.GetStaticBox()
		elementsGroup = guiHelper.BoxSizerHelper(self, sizer=elementsGroupSizer)
		sHelper.addItem(elementsGroup, flag=wx.EXPAND, proportion=1)

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		self.headingsCheckBox = elementsGroup.addItem(wx.CheckBox(elementsGroupBox, label=_("&Headings")))
		self.headingsCheckBox.SetValue(config.conf["documentFormatting"]["reportHeadings"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		self.linksCheckBox = elementsGroup.addItem(wx.CheckBox(elementsGroupBox, label=_("Lin&ks")))
		self.linksCheckBox.Bind(wx.EVT_CHECKBOX, self._onLinksChange)
		self.linksCheckBox.SetValue(config.conf["documentFormatting"]["reportLinks"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		self.linkTypeCheckBox = elementsGroup.addItem(wx.CheckBox(elementsGroupBox, label=_("Link type")))
		self.linkTypeCheckBox.SetValue(config.conf["documentFormatting"]["reportLinkType"])
		self.linkTypeCheckBox.Enable(self.linksCheckBox.IsChecked())

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		self.graphicsCheckBox = elementsGroup.addItem(wx.CheckBox(elementsGroupBox, label=_("&Graphics")))
		self.graphicsCheckBox.SetValue(config.conf["documentFormatting"]["reportGraphics"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		self.listsCheckBox = elementsGroup.addItem(wx.CheckBox(elementsGroupBox, label=_("&Lists")))
		self.listsCheckBox.SetValue(config.conf["documentFormatting"]["reportLists"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		_blockQuotesCheckBox = wx.CheckBox(elementsGroupBox, label=_("Block &quotes"))
		self.blockQuotesCheckBox = elementsGroup.addItem(_blockQuotesCheckBox)
		self.blockQuotesCheckBox.SetValue(config.conf["documentFormatting"]["reportBlockQuotes"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		groupingsText = _("&Groupings")
		self.groupingsCheckBox = elementsGroup.addItem(wx.CheckBox(elementsGroupBox, label=groupingsText))
		self.groupingsCheckBox.SetValue(config.conf["documentFormatting"]["reportGroupings"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		landmarksText = _("Lan&dmarks and regions")
		self.landmarksCheckBox = elementsGroup.addItem(wx.CheckBox(elementsGroupBox, label=landmarksText))
		self.landmarksCheckBox.SetValue(config.conf["documentFormatting"]["reportLandmarks"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		self.articlesCheckBox = elementsGroup.addItem(wx.CheckBox(elementsGroupBox, label=_("Arti&cles")))
		self.articlesCheckBox.SetValue(config.conf["documentFormatting"]["reportArticles"])

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		self.framesCheckBox = elementsGroup.addItem(wx.CheckBox(elementsGroupBox, label=_("Fra&mes")))
		self.framesCheckBox.Value = config.conf["documentFormatting"]["reportFrames"]

		self.figuresCheckBox = elementsGroup.addItem(
			# Translators: This is the label for a checkbox in the
			# document formatting settings panel.
			wx.CheckBox(elementsGroupBox, label=_("&Figures and captions")),
		)
		self.figuresCheckBox.Value = config.conf["documentFormatting"]["reportFigures"]

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		self.clickableCheckBox = elementsGroup.addItem(wx.CheckBox(elementsGroupBox, label=_("&Clickable")))
		self.clickableCheckBox.Value = config.conf["documentFormatting"]["reportClickable"]

		# Translators: This is the label for a checkbox in the
		# document formatting settings panel.
		detectFormatAfterCursorText = _("Report formatting chan&ges after the cursor (can cause a lag)")
		self.detectFormatAfterCursorCheckBox = wx.CheckBox(self, label=detectFormatAfterCursorText)
		self.bindHelpEvent(
			"DocumentFormattingDetectFormatAfterCursor",
			self.detectFormatAfterCursorCheckBox,
		)
		self.detectFormatAfterCursorCheckBox.SetValue(
			config.conf["documentFormatting"]["detectFormatAfterCursor"],
		)
		sHelper.addItem(self.detectFormatAfterCursorCheckBox)

	def _onLineIndentationChange(self, evt: wx.CommandEvent) -> None:
		self.ignoreBlankLinesRLICheckbox.Enable(evt.GetSelection() != 0)

	def _onLinksChange(self, evt: wx.CommandEvent):
		self.linkTypeCheckBox.Enable(evt.IsChecked())

	def onSave(self):
		config.conf["documentFormatting"]["detectFormatAfterCursor"] = (
			self.detectFormatAfterCursorCheckBox.IsChecked()
		)
		config.conf["documentFormatting"]["reportFontName"] = self.fontNameCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportFontSize"] = self.fontSizeCheckBox.IsChecked()
		config.conf["documentFormatting"]["fontAttributeReporting"] = self.fontAttrsList.GetSelection()
		config.conf["documentFormatting"]["reportSuperscriptsAndSubscripts"] = (
			self.superscriptsAndSubscriptsCheckBox.IsChecked()
		)
		config.conf["documentFormatting"]["reportColor"] = self.colorCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportComments"] = self.commentsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportBookmarks"] = self.bookmarksCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportRevisions"] = self.revisionsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportEmphasis"] = self.emphasisCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportHighlight"] = self.highlightCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportAlignment"] = self.alignmentCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportStyle"] = self.styleCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportSpellingErrors"] = self.spellingErrorsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportPage"] = self.pageCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportLineNumber"] = self.lineNumberCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportLineIndentation"] = self.lineIndentationCombo.GetSelection()
		config.conf["documentFormatting"]["ignoreBlankLinesForRLI"] = (
			self.ignoreBlankLinesRLICheckbox.IsChecked()
		)
		config.conf["documentFormatting"]["reportParagraphIndentation"] = (
			self.paragraphIndentationCheckBox.IsChecked()
		)
		config.conf["documentFormatting"]["reportLineSpacing"] = self.lineSpacingCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportTables"] = self.tablesCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportTableHeaders"] = self.tableHeadersComboBox.GetSelection()
		config.conf["documentFormatting"]["reportTableCellCoords"] = self.tableCellCoordsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportCellBorders"] = self.borderComboBox.GetSelection()
		config.conf["documentFormatting"]["reportLinks"] = self.linksCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportLinkType"] = self.linkTypeCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportGraphics"] = self.graphicsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportHeadings"] = self.headingsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportLists"] = self.listsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportBlockQuotes"] = self.blockQuotesCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportGroupings"] = self.groupingsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportLandmarks"] = self.landmarksCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportArticles"] = self.articlesCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportFrames"] = self.framesCheckBox.Value
		config.conf["documentFormatting"]["reportFigures"] = self.figuresCheckBox.Value
		config.conf["documentFormatting"]["reportClickable"] = self.clickableCheckBox.Value


class DocumentNavigationPanel(SettingsPanel):
	# Translators: This is the label for the document navigation settings panel.
	title = _("Document Navigation")
	helpId = "DocumentNavigation"

	def makeSettings(self, settingsSizer: wx.BoxSizer) -> None:
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: This is a label for the paragraph navigation style in the document navigation dialog
		paragraphStyleLabel = _("&Paragraph style:")
		self.paragraphStyleCombo: nvdaControls.FeatureFlagCombo = sHelper.addLabeledControl(
			labelText=paragraphStyleLabel,
			wxCtrlClass=nvdaControls.FeatureFlagCombo,
			keyPath=["documentNavigation", "paragraphStyle"],
			conf=config.conf,
		)
		self.bindHelpEvent("ParagraphStyle", self.paragraphStyleCombo)

	def onSave(self):
		self.paragraphStyleCombo.saveCurrentValueToConf()


def _synthWarningDialog(newSynth: str):
	gui.messageBox(
		# Translators: This message is presented when
		# NVDA is unable to load the selected synthesizer.
		_("Could not load the %s synthesizer.") % newSynth,
		# Translators: Dialog title presented when
		# NVDA is unable to load the selected synthesizer.
		_("Synthesizer Error"),
		wx.OK | wx.ICON_WARNING,
	)


class AudioPanel(SettingsPanel):
	# Translators: This is the label for the audio settings panel.
	title = _("Audio")
	helpId = "AudioSettings"

	def makeSettings(self, settingsSizer: wx.BoxSizer) -> None:
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		# Translators: This is the label for the select output device combo in NVDA audio settings.
		# Examples of an output device are default soundcard, usb headphones, etc.
		deviceListLabelText = _("Audio output &device:")
		deviceNames = nvwave.getOutputDeviceNames()
		# #11349: On Windows 10 20H1 and 20H2, Microsoft Sound Mapper returns an empty string.
		if deviceNames[0] in ("", "Microsoft Sound Mapper"):
			# Translators: name for default (Microsoft Sound Mapper) audio output device.
			deviceNames[0] = _("Microsoft Sound Mapper")
		self.deviceList = sHelper.addLabeledControl(deviceListLabelText, wx.Choice, choices=deviceNames)
		self.bindHelpEvent("SelectSynthesizerOutputDevice", self.deviceList)
		try:
			selection = deviceNames.index(config.conf["speech"]["outputDevice"])
		except ValueError:
			selection = 0
		self.deviceList.SetSelection(selection)

		# Translators: This is a label for the audio ducking combo box in the Audio Settings dialog.
		duckingListLabelText = _("Audio d&ucking mode:")
		self.duckingList = sHelper.addLabeledControl(
			duckingListLabelText,
			wx.Choice,
			choices=[mode.displayString for mode in audioDucking.AudioDuckingMode],
		)
		self.bindHelpEvent("SelectSynthesizerDuckingMode", self.duckingList)
		index = config.conf["audio"]["audioDuckingMode"]
		self.duckingList.SetSelection(index)
		if not audioDucking.isAudioDuckingSupported():
			self.duckingList.Disable()

		# Translators: This is the label for a checkbox control in the
		# Audio settings panel.
		label = _("Volume of NVDA sounds follows voice volume")
		self.soundVolFollowCheckBox: wx.CheckBox = sHelper.addItem(wx.CheckBox(self, label=label))
		self.bindHelpEvent("SoundVolumeFollowsVoice", self.soundVolFollowCheckBox)
		self.soundVolFollowCheckBox.SetValue(config.conf["audio"]["soundVolumeFollowsVoice"])
		self.soundVolFollowCheckBox.Bind(wx.EVT_CHECKBOX, self._onSoundVolChange)

		# Translators: This is the label for a slider control in the
		# Audio settings panel.
		label = _("Volume of NVDA sounds")
		self.soundVolSlider: nvdaControls.EnhancedInputSlider = sHelper.addLabeledControl(
			label,
			nvdaControls.EnhancedInputSlider,
			minValue=0,
			maxValue=100,
		)
		self.bindHelpEvent("SoundVolume", self.soundVolSlider)
		self.soundVolSlider.SetValue(config.conf["audio"]["soundVolume"])

		# Translators: This is a label for the sound split combo box in the Audio Settings dialog.
		soundSplitLabelText = _("&Sound split mode:")
		self.soundSplitComboBox = sHelper.addLabeledControl(
			soundSplitLabelText,
			wx.Choice,
			choices=[mode.displayString for mode in audio.SoundSplitState],
		)
		self.bindHelpEvent("SelectSoundSplitMode", self.soundSplitComboBox)
		index = config.conf["audio"]["soundSplitState"]
		self.soundSplitComboBox.SetSelection(index)

		self._appendSoundSplitModesList(sHelper)

		# Translators: This is a label for the applications volume adjuster combo box in settings.
		label = _("&Application volume adjuster status")
		self.appVolAdjusterCombo: nvdaControls.FeatureFlagCombo = sHelper.addLabeledControl(
			labelText=label,
			wxCtrlClass=nvdaControls.FeatureFlagCombo,
			keyPath=["audio", "applicationsVolumeMode"],
			conf=config.conf,
		)
		self.appVolAdjusterCombo.Bind(wx.EVT_CHOICE, self._onSoundVolChange)
		self.bindHelpEvent("AppsVolumeAdjusterStatus", self.appVolAdjusterCombo)

		# Translators: This is the label for a slider control in the
		# Audio settings panel.
		label = _("Volume of other applications")
		self.appSoundVolSlider: nvdaControls.EnhancedInputSlider = sHelper.addLabeledControl(
			label,
			nvdaControls.EnhancedInputSlider,
			minValue=0,
			maxValue=100,
		)
		self.bindHelpEvent("OtherAppVolume", self.appSoundVolSlider)
		volume = config.conf["audio"]["applicationsSoundVolume"]
		if 0 <= volume <= 100:
			self.appSoundVolSlider.SetValue(volume)
		else:
			log.error("Invalid volume level: {}", volume)
			defaultVolume = config.conf.getConfigValidation(["audio", "applicationsSoundVolume"]).default
			self.appSoundVolSlider.SetValue(defaultVolume)

		self.muteOtherAppsCheckBox: wx.CheckBox = sHelper.addItem(
			# Translators: Mute other apps checkbox in settings
			wx.CheckBox(self, label=_("Mute other apps")),
		)
		self.muteOtherAppsCheckBox.SetValue(config.conf["audio"]["applicationsSoundMuted"])
		self.bindHelpEvent("OtherAppMute", self.muteOtherAppsCheckBox)

		self._onSoundVolChange(None)

		audioAwakeTimeLabelText = _(
			# Translators: The label for a setting in Audio settings panel
			# to change how long the audio device is kept awake after speech
			"Time to &keep audio device awake after speech (seconds)",
		)
		minTime = int(config.conf.getConfigValidation(("audio", "audioAwakeTime")).kwargs["min"])
		maxTime = int(config.conf.getConfigValidation(("audio", "audioAwakeTime")).kwargs["max"])
		self.audioAwakeTimeEdit = sHelper.addLabeledControl(
			audioAwakeTimeLabelText,
			nvdaControls.SelectOnFocusSpinCtrl,
			min=minTime,
			max=maxTime,
			initial=config.conf["audio"]["audioAwakeTime"],
		)
		self.bindHelpEvent("AudioAwakeTime", self.audioAwakeTimeEdit)
		self.audioAwakeTimeEdit.Enable(nvwave.usingWasapiWavePlayer())

	def _appendSoundSplitModesList(self, settingsSizerHelper: guiHelper.BoxSizerHelper) -> None:
		self._allSoundSplitModes = list(audio.SoundSplitState)
		self.soundSplitModesList: nvdaControls.CustomCheckListBox = settingsSizerHelper.addLabeledControl(
			# Translators: Label of the list where user can select sound split modes that will be available.
			_("&Modes available in the 'Cycle sound split mode' command:"),
			nvdaControls.CustomCheckListBox,
			choices=[mode.displayString for mode in self._allSoundSplitModes],
		)
		self.bindHelpEvent("CustomizeSoundSplitModes", self.soundSplitModesList)
		includedModes: list[int] = config.conf["audio"]["includedSoundSplitModes"]
		self.soundSplitModesList.Checked = [
			mIndex for mIndex in range(len(self._allSoundSplitModes)) if mIndex in includedModes
		]
		self.soundSplitModesList.Select(0)

	def onSave(self):
		if config.conf["speech"]["outputDevice"] != self.deviceList.GetStringSelection():
			# Synthesizer must be reload if output device changes
			config.conf["speech"]["outputDevice"] = self.deviceList.GetStringSelection()
			currentSynth = getSynth()
			if not setSynth(currentSynth.name):
				_synthWarningDialog(currentSynth.name)

			# Reinitialize the tones module to update the audio device
			import tones

			tones.terminate()
			tones.initialize()

		config.conf["audio"]["soundVolumeFollowsVoice"] = self.soundVolFollowCheckBox.IsChecked()
		config.conf["audio"]["soundVolume"] = self.soundVolSlider.GetValue()

		index = self.soundSplitComboBox.GetSelection()
		config.conf["audio"]["soundSplitState"] = index
		if nvwave.usingWasapiWavePlayer():
			audio._setSoundSplitState(audio.SoundSplitState(index))
		config.conf["audio"]["includedSoundSplitModes"] = [
			mIndex
			for mIndex in range(len(self._allSoundSplitModes))
			if mIndex in self.soundSplitModesList.CheckedItems
		]
		config.conf["audio"]["applicationsSoundVolume"] = self.appSoundVolSlider.GetValue()
		config.conf["audio"]["applicationsSoundMuted"] = self.muteOtherAppsCheckBox.GetValue()
		self.appVolAdjusterCombo.saveCurrentValueToConf()
		audio.appsVolume._updateAppsVolumeImpl(
			volume=self.appSoundVolSlider.GetValue() / 100.0,
			muted=self.muteOtherAppsCheckBox.GetValue(),
			state=self.appVolAdjusterCombo._getControlCurrentValue(),
		)

		if audioDucking.isAudioDuckingSupported():
			index = self.duckingList.GetSelection()
			config.conf["audio"]["audioDuckingMode"] = index
			audioDucking.setAudioDuckingMode(index)

		config.conf["audio"]["audioAwakeTime"] = self.audioAwakeTimeEdit.GetValue()

	def onPanelActivated(self):
		self._onSoundVolChange(None)
		super().onPanelActivated()

	def _onSoundVolChange(self, event: wx.Event) -> None:
		"""Called when the sound volume follow checkbox is checked or unchecked."""
		wasapi = nvwave.usingWasapiWavePlayer()
		self.soundVolFollowCheckBox.Enable(wasapi)
		self.soundVolSlider.Enable(
			wasapi and not self.soundVolFollowCheckBox.IsChecked(),
		)
		self.soundSplitComboBox.Enable(wasapi)
		self.soundSplitModesList.Enable(wasapi)

		avEnabled = config.featureFlagEnums.AppsVolumeAdjusterFlag.ENABLED
		self.appSoundVolSlider.Enable(
			wasapi and self.appVolAdjusterCombo._getControlCurrentValue() == avEnabled,
		)
		self.muteOtherAppsCheckBox.Enable(
			wasapi and self.appVolAdjusterCombo._getControlCurrentValue() == avEnabled,
		)
		self.appVolAdjusterCombo.Enable(wasapi)

	def isValid(self) -> bool:
		enabledSoundSplitModes = self.soundSplitModesList.CheckedItems
		if len(enabledSoundSplitModes) < 1:
			log.debugWarning("No sound split modes enabled.")
			self._validationErrorMessageBox(
				# Translators: Message shown when no sound split modes are enabled.
				message=_("At least one sound split mode has to be checked."),
				# Translators: Same as the label for the list of checkboxes controlling which sound split modes will be
				# available. in Audio Settings, but without keyboard accelerator (& character) nor final colon.
				option=_("Modes available in the 'Cycle sound split mode' command"),
			)
			return False
		return super().isValid()


class AddonStorePanel(SettingsPanel):
	# Translators: This is the label for the addon navigation settings panel.
	title = _("Add-on Store")
	helpId = "AddonStoreSettings"

	def makeSettings(self, settingsSizer: wx.BoxSizer) -> None:
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: This is a label for the automatic updates combo box in the Add-on Store Settings dialog.
		automaticUpdatesLabelText = _("&Update notifications:")
		# TODO: change label to the following when the feature is implemented
		# automaticUpdatesLabelText = _("Automatic &updates:")
		self.automaticUpdatesComboBox = sHelper.addLabeledControl(
			automaticUpdatesLabelText,
			wx.Choice,
			choices=[mode.displayString for mode in AddonsAutomaticUpdate],
		)
		self.bindHelpEvent("AutomaticAddonUpdates", self.automaticUpdatesComboBox)
		index = [x.value for x in AddonsAutomaticUpdate].index(config.conf["addonStore"]["automaticUpdates"])
		self.automaticUpdatesComboBox.SetSelection(index)

		# Translators: This is the label for a text box in the add-on store settings dialog.
		self.addonMetadataMirrorLabelText = _("Server &mirror URL")
		self.addonMetadataMirrorTextbox = sHelper.addLabeledControl(
			self.addonMetadataMirrorLabelText,
			wx.TextCtrl,
		)
		self.addonMetadataMirrorTextbox.SetValue(config.conf["addonStore"]["baseServerURL"])
		self.bindHelpEvent("AddonStoreMetadataMirror", self.addonMetadataMirrorTextbox)

	def isValid(self) -> bool:
		self.addonMetadataMirrorTextbox.SetValue(
			url_normalize(self.addonMetadataMirrorTextbox.GetValue().strip()).rstrip("/"),
		)
		return True

	def onSave(self):
		index = self.automaticUpdatesComboBox.GetSelection()
		config.conf["addonStore"]["automaticUpdates"] = [x.value for x in AddonsAutomaticUpdate][index]

		config.conf["addonStore"]["baseServerURL"] = self.addonMetadataMirrorTextbox.Value.strip().rstrip("/")


class TouchInteractionPanel(SettingsPanel):
	# Translators: This is the label for the touch interaction settings panel.
	title = _("Touch Interaction")
	helpId = "TouchInteraction"

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: This is the label for a checkbox in the
		# touch interaction settings panel.
		touchSupportEnableLabel = _("Enable touch interaction support")
		self.enableTouchSupportCheckBox = sHelper.addItem(wx.CheckBox(self, label=touchSupportEnableLabel))
		self.bindHelpEvent("TouchSupportEnable", self.enableTouchSupportCheckBox)
		self.enableTouchSupportCheckBox.SetValue(config.conf["touch"]["enabled"])
		# Translators: This is the label for a checkbox in the
		# touch interaction settings panel.
		self.touchTypingCheckBox = sHelper.addItem(wx.CheckBox(self, label=_("&Touch typing mode")))
		self.bindHelpEvent("TouchTypingMode", self.touchTypingCheckBox)
		self.touchTypingCheckBox.SetValue(config.conf["touch"]["touchTyping"])

	def onSave(self):
		config.conf["touch"]["enabled"] = self.enableTouchSupportCheckBox.IsChecked()
		config.conf["touch"]["touchTyping"] = self.touchTypingCheckBox.IsChecked()
		touchHandler.setTouchSupport(config.conf["touch"]["enabled"])


class UwpOcrPanel(SettingsPanel):
	# Translators: The title of the Windows OCR panel.
	title = _("Windows OCR")
	helpId = "Win10OcrSettings"

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Lazily import this.
		from contentRecog import uwpOcr

		self.languageCodes = uwpOcr.getLanguages()
		languageChoices = []
		for lang in self.languageCodes:
			normLang = languageHandler.normalizeLanguage(lang)
			desc = languageHandler.getLanguageDescription(normLang)
			if not desc:
				# Raise an error in the hope that people be more likely to report the issue
				log.error(f"No description for language: {lang}. Using language code instead.")
				desc = lang
			languageChoices.append(desc)
		# Translators: Label for an option in the Windows OCR dialog.
		languageLabel = _("Recognition &language:")
		self.languageChoice = sHelper.addLabeledControl(languageLabel, wx.Choice, choices=languageChoices)
		self.bindHelpEvent("Win10OcrSettingsRecognitionLanguage", self.languageChoice)
		try:
			langIndex = self.languageCodes.index(config.conf["uwpOcr"]["language"])
			self.languageChoice.Selection = langIndex
		except ValueError:
			self.languageChoice.Selection = 0

		# Translators: Label for an option in the Windows OCR settings panel.
		autoRefreshText = _("Periodically &refresh recognized content")
		self.autoRefreshCheckbox = sHelper.addItem(
			wx.CheckBox(self, label=autoRefreshText),
		)
		self.bindHelpEvent("Win10OcrSettingsAutoRefresh", self.autoRefreshCheckbox)
		self.autoRefreshCheckbox.SetValue(config.conf["uwpOcr"]["autoRefresh"])

	def onSave(self):
		lang = self.languageCodes[self.languageChoice.Selection]
		config.conf["uwpOcr"]["language"] = lang
		config.conf["uwpOcr"]["autoRefresh"] = self.autoRefreshCheckbox.IsChecked()


class AdvancedPanelControls(
	gui.contextHelp.ContextHelpMixin,
	wx.Panel,  # wxPython does not seem to call base class initializer, put last in MRO
):
	"""Holds the actual controls for the Advanced Settings panel, this allows the state of the controls to
	be more easily managed.
	"""

	helpId = "AdvancedSettings"

	def __init__(self, parent):
		super().__init__(parent)
		self._defaultsRestored = False

		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		self.SetSizer(sHelper.sizer)
		# Translators: This is the label for a group of advanced options in the
		#  Advanced settings panel
		groupText = _("NVDA Development")
		devGroupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=groupText)
		devGroupBox = devGroupSizer.GetStaticBox()
		devGroup = guiHelper.BoxSizerHelper(self, sizer=devGroupSizer)
		sHelper.addItem(devGroup)

		# Translators: This is the label for a checkbox in the
		#  Advanced settings panel.
		label = _("Enable loading custom code from Developer Scratchpad directory")
		self.scratchpadCheckBox = devGroup.addItem(wx.CheckBox(devGroupBox, label=label))
		self.bindHelpEvent("AdvancedSettingsEnableScratchpad", self.scratchpadCheckBox)
		self.scratchpadCheckBox.SetValue(config.conf["development"]["enableScratchpadDir"])
		self.scratchpadCheckBox.defaultValue = self._getDefaultValue(["development", "enableScratchpadDir"])
		self.scratchpadCheckBox.Bind(
			wx.EVT_CHECKBOX,
			lambda evt: self.openScratchpadButton.Enable(evt.IsChecked()),
		)
		if config.isAppX:
			self.scratchpadCheckBox.Disable()

		# Translators: the label for a button in the Advanced settings category
		label = _("Open developer scratchpad directory")
		self.openScratchpadButton = devGroup.addItem(wx.Button(devGroupBox, label=label))
		self.bindHelpEvent("AdvancedSettingsOpenScratchpadDir", self.openScratchpadButton)
		self.openScratchpadButton.Enable(config.conf["development"]["enableScratchpadDir"])
		self.openScratchpadButton.Bind(wx.EVT_BUTTON, self.onOpenScratchpadDir)
		if config.isAppX:
			self.openScratchpadButton.Disable()

		# Translators: This is the label for a group of advanced options in the
		#  Advanced settings panel
		label = _("Microsoft UI Automation")
		UIASizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=label)
		UIABox = UIASizer.GetStaticBox()
		UIAGroup = guiHelper.BoxSizerHelper(self, sizer=UIASizer)
		sHelper.addItem(UIAGroup)

		selectiveUIAEventRegistrationComboText = _(
			# Translators: This is the label for a combo box for selecting the
			# means of registering for UI Automation events in the advanced settings panel.
			# Choices are automatic, selective, and global.
			"Regi&stration for UI Automation events and property changes:",
		)
		selectiveUIAEventRegistrationChoices = [
			# Translators: A choice in a combo box in the advanced settings
			# panel to have NVDA decide whether to register
			# selectively or globally for UI Automation events.
			_("Automatic (prefer selective)"),
			# Translators: A choice in a combo box in the advanced settings
			# panel to have NVDA register selectively for UI Automation events
			# (i.e. not to request events for objects outside immediate focus).
			_("Selective"),
			# Translators: A choice in a combo box in the advanced settings
			# panel to have NVDA register for all UI Automation events
			# in all cases.
			_("Global"),
		]
		#: The possible event registration config values, in the order they appear
		#: in the combo box.
		self.selectiveUIAEventRegistrationVals = (
			"auto",
			"selective",
			"global",
		)
		self.selectiveUIAEventRegistrationCombo = UIAGroup.addLabeledControl(
			selectiveUIAEventRegistrationComboText,
			wx.Choice,
			choices=selectiveUIAEventRegistrationChoices,
		)
		self.bindHelpEvent(
			"AdvancedSettingsSelectiveUIAEventRegistration",
			self.selectiveUIAEventRegistrationCombo,
		)
		curChoice = self.selectiveUIAEventRegistrationVals.index(
			config.conf["UIA"]["eventRegistration"],
		)
		self.selectiveUIAEventRegistrationCombo.SetSelection(curChoice)
		self.selectiveUIAEventRegistrationCombo.defaultValue = self.selectiveUIAEventRegistrationVals.index(
			self._getDefaultValue(["UIA", "eventRegistration"]),
		)

		label = pgettext(
			"advanced.uiaWithMSWord",
			# Translators: Label for the Use UIA with MS Word combobox, in the Advanced settings panel.
			"Use UI Automation to access Microsoft &Word document controls",
		)
		wordChoices = (
			# Translators: Label for the default value of the Use UIA with MS Word combobox,
			# in the Advanced settings panel.
			pgettext("advanced.uiaWithMSWord", "Default (Where suitable)"),
			# Translators: Label for a value in the Use UIA with MS Word combobox, in the Advanced settings panel.
			pgettext("advanced.uiaWithMSWord", "Only when necessary"),
			# Translators: Label for a value in the Use UIA with MS Word combobox, in the Advanced settings panel.
			pgettext("advanced.uiaWithMSWord", "Where suitable"),
			# Translators: Label for a value in the Use UIA with MS Word combobox, in the Advanced settings panel.
			pgettext("advanced.uiaWithMSWord", "Always"),
		)
		self.UIAInMSWordCombo = UIAGroup.addLabeledControl(label, wx.Choice, choices=wordChoices)
		self.bindHelpEvent("MSWordUIA", self.UIAInMSWordCombo)
		self.UIAInMSWordCombo.SetSelection(config.conf["UIA"]["allowInMSWord"])
		self.UIAInMSWordCombo.defaultValue = self._getDefaultValue(["UIA", "allowInMSWord"])

		# Translators: This is the label for a checkbox in the
		#  Advanced settings panel.
		label = _("Use UI Automation to access Microsoft &Excel spreadsheet controls when available")
		self.UIAInMSExcelCheckBox = UIAGroup.addItem(wx.CheckBox(UIABox, label=label))
		self.bindHelpEvent("UseUiaForExcel", self.UIAInMSExcelCheckBox)
		self.UIAInMSExcelCheckBox.SetValue(config.conf["UIA"]["useInMSExcelWhenAvailable"])
		self.UIAInMSExcelCheckBox.defaultValue = self._getDefaultValue(["UIA", "useInMSExcelWhenAvailable"])
		# Translators: This is the label for a combo box for selecting the
		# active console implementation in the advanced settings panel.
		# Choices are automatic, UIA when available, and legacy.
		consoleComboText = _("Windows C&onsole support:")
		consoleChoices = [
			# Translators: A choice in a combo box in the advanced settings
			# panel to have NVDA determine its Windows Console implementation
			# automatically.
			_("Automatic (prefer UIA)"),
			# Translators: A choice in a combo box in the advanced settings
			# panel to have NVDA use UIA in the Windows Console when available.
			_("UIA when available"),
			# Translators: A choice in a combo box in the advanced settings
			# panel to have NVDA use its legacy Windows Console support
			# in all cases.
			_("Legacy"),
		]
		#: The possible console config values, in the order they appear
		#: in the combo box.
		self.consoleVals = (
			"auto",
			"UIA",
			"legacy",
		)
		self.consoleCombo = UIAGroup.addLabeledControl(consoleComboText, wx.Choice, choices=consoleChoices)
		self.bindHelpEvent("AdvancedSettingsConsoleUIA", self.consoleCombo)
		curChoice = self.consoleVals.index(
			config.conf["UIA"]["winConsoleImplementation"],
		)
		self.consoleCombo.SetSelection(curChoice)
		self.consoleCombo.defaultValue = self.consoleVals.index(
			self._getDefaultValue(["UIA", "winConsoleImplementation"]),
		)

		label = pgettext(
			"advanced.uiaWithChromium",
			# Translators: Label for the Use UIA with Chromium combobox, in the Advanced settings panel.
			# Note the '\n' is used to split this long label approximately in half.
			"Use UIA with Microsoft Edge and other \n&Chromium based browsers when available:",
		)
		chromiumChoices = (
			# Translators: Label for the default value of the Use UIA with Chromium combobox,
			# in the Advanced settings panel.
			pgettext("advanced.uiaWithChromium", "Default (Only when necessary)"),
			# Translators: Label for a value in the Use UIA with Chromium combobox, in the Advanced settings panel.
			pgettext("advanced.uiaWithChromium", "Only when necessary"),
			# Translators: Label for a value in the Use UIA with Chromium combobox, in the Advanced settings panel.
			pgettext("advanced.uiaWithChromium", "Yes"),
			# Translators: Label for a value in the Use UIA with Chromium combobox, in the Advanced settings panel.
			pgettext("advanced.uiaWithChromium", "No"),
		)
		self.UIAInChromiumCombo = UIAGroup.addLabeledControl(label, wx.Choice, choices=chromiumChoices)
		self.bindHelpEvent("ChromiumUIA", self.UIAInChromiumCombo)
		self.UIAInChromiumCombo.SetSelection(config.conf["UIA"]["allowInChromium"])
		self.UIAInChromiumCombo.defaultValue = self._getDefaultValue(["UIA", "allowInChromium"])

		# Translators: This is the label for a COMBOBOX in the Advanced settings panel.
		label = _("Use en&hanced event processing (requires restart)")
		self.enhancedEventProcessingComboBox = cast(
			nvdaControls.FeatureFlagCombo,
			UIAGroup.addLabeledControl(
				labelText=label,
				wxCtrlClass=nvdaControls.FeatureFlagCombo,
				keyPath=["UIA", "enhancedEventProcessing"],
				conf=config.conf,
			),
		)
		self.bindHelpEvent("UIAEnhancedEventProcessing", self.enhancedEventProcessingComboBox)

		# Translators: This is the label for a group of advanced options in the
		#  Advanced settings panel
		label = _("Annotations")
		AnnotationsSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=label)
		AnnotationsBox = AnnotationsSizer.GetStaticBox()
		AnnotationsGroup = guiHelper.BoxSizerHelper(self, sizer=AnnotationsSizer)
		self.bindHelpEvent("Annotations", AnnotationsBox)
		sHelper.addItem(AnnotationsGroup)

		# Translators: This is the label for a checkbox in the
		#  Advanced settings panel.
		label = _("Report 'has details' for structured annotations")
		self.annotationsDetailsCheckBox = AnnotationsGroup.addItem(wx.CheckBox(AnnotationsBox, label=label))
		self.annotationsDetailsCheckBox.SetValue(config.conf["annotations"]["reportDetails"])
		self.annotationsDetailsCheckBox.defaultValue = self._getDefaultValue(["annotations", "reportDetails"])

		# Translators: This is the label for a checkbox in the
		#  Advanced settings panel.
		label = _("Report aria-description always")
		self.ariaDescCheckBox: wx.CheckBox = AnnotationsGroup.addItem(
			wx.CheckBox(AnnotationsBox, label=label),
		)
		self.ariaDescCheckBox.SetValue(config.conf["annotations"]["reportAriaDescription"])
		self.ariaDescCheckBox.defaultValue = self._getDefaultValue(["annotations", "reportAriaDescription"])

		# Translators: This is the label for a group of advanced options in the
		#  Advanced settings panel
		label = _("Braille")
		brailleSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=label)
		brailleGroup = guiHelper.BoxSizerHelper(self, sizer=brailleSizer)
		sHelper.addItem(brailleGroup)

		self.brailleLiveRegionsCombo: nvdaControls.FeatureFlagCombo = brailleGroup.addLabeledControl(
			# Translators: This is the label for a combo-box in the Advanced settings panel.
			labelText=_("Report live regions:"),
			wxCtrlClass=nvdaControls.FeatureFlagCombo,
			keyPath=["braille", "reportLiveRegions"],
			conf=config.conf,
		)
		self.bindHelpEvent("BrailleLiveRegions", self.brailleLiveRegionsCombo)

		# Translators: This is the label for a group of advanced options in the
		#  Advanced settings panel
		label = _("Terminal programs")
		terminalsSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=label)
		terminalsBox = terminalsSizer.GetStaticBox()
		terminalsGroup = guiHelper.BoxSizerHelper(self, sizer=terminalsSizer)
		sHelper.addItem(terminalsGroup)
		# Translators: This is the label for a checkbox in the
		#  Advanced settings panel.
		label = _("Speak &passwords in all enhanced terminals (may improve performance)")
		self.winConsoleSpeakPasswordsCheckBox = terminalsGroup.addItem(wx.CheckBox(terminalsBox, label=label))
		self.bindHelpEvent("AdvancedSettingsWinConsoleSpeakPasswords", self.winConsoleSpeakPasswordsCheckBox)
		self.winConsoleSpeakPasswordsCheckBox.SetValue(config.conf["terminals"]["speakPasswords"])
		self.winConsoleSpeakPasswordsCheckBox.defaultValue = self._getDefaultValue(
			["terminals", "speakPasswords"],
		)
		# Translators: This is the label for a checkbox in the
		#  Advanced settings panel.
		label = _("Use enhanced t&yped character support in legacy Windows Console when available")
		self.keyboardSupportInLegacyCheckBox = terminalsGroup.addItem(wx.CheckBox(terminalsBox, label=label))
		self.bindHelpEvent("AdvancedSettingsKeyboardSupportInLegacy", self.keyboardSupportInLegacyCheckBox)
		self.keyboardSupportInLegacyCheckBox.SetValue(config.conf["terminals"]["keyboardSupportInLegacy"])
		self.keyboardSupportInLegacyCheckBox.defaultValue = self._getDefaultValue(
			["terminals", "keyboardSupportInLegacy"],
		)
		self.keyboardSupportInLegacyCheckBox.Enable(winVersion.getWinVer() >= winVersion.WIN10_1607)

		# Translators: This is the label for a combo box for selecting a
		# method of detecting changed content in terminals in the advanced
		# settings panel.
		# Choices are automatic, Diff Match Patch, and Difflib.
		diffAlgoComboText = _("&Diff algorithm:")
		diffAlgoChoices = [
			# Translators: A choice in a combo box in the advanced settings
			# panel to have NVDA determine the method of detecting changed
			# content in terminals automatically.
			_("Automatic (prefer Diff Match Patch)"),
			# Translators: A choice in a combo box in the advanced settings
			# panel to have NVDA detect changes in terminals
			# by character, using the diff match patch algorithm.
			_("Diff Match Patch"),
			# Translators: A choice in a combo box in the advanced settings
			# panel to have NVDA detect changes in terminals
			# by line, using the difflib algorithm.
			_("Difflib"),
		]
		#: The possible diffAlgo config values, in the order they appear
		#: in the combo box.
		self.diffAlgoVals = (
			"auto",
			"dmp",
			"difflib",
		)
		self.diffAlgoCombo = terminalsGroup.addLabeledControl(
			diffAlgoComboText,
			wx.Choice,
			choices=diffAlgoChoices,
		)
		self.bindHelpEvent("DiffAlgo", self.diffAlgoCombo)
		curChoice = self.diffAlgoVals.index(
			config.conf["terminals"]["diffAlgo"],
		)
		self.diffAlgoCombo.SetSelection(curChoice)
		self.diffAlgoCombo.defaultValue = self.diffAlgoVals.index(
			self._getDefaultValue(["terminals", "diffAlgo"]),
		)

		self.wtStrategyCombo: nvdaControls.FeatureFlagCombo = terminalsGroup.addLabeledControl(
			labelText=_(
				# Translators: This is the label for a combo-box in the Advanced settings panel.
				"Speak new text in Windows Terminal via:",
			),
			wxCtrlClass=nvdaControls.FeatureFlagCombo,
			keyPath=["terminals", "wtStrategy"],
			conf=config.conf,
		)
		self.bindHelpEvent("WtStrategy", self.wtStrategyCombo)

		# Translators: This is the label for a group of advanced options in the
		#  Advanced settings panel
		label = _("Speech")
		speechSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=label)
		speechGroup = guiHelper.BoxSizerHelper(speechSizer, sizer=speechSizer)
		sHelper.addItem(speechGroup)

		expiredFocusSpeechChoices = [
			# Translators: Label for the 'Cancel speech for expired &focus events' combobox
			# in the Advanced settings panel.
			_("Default (Yes)"),
			# Translators: Label for the 'Cancel speech for expired &focus events' combobox
			# in the Advanced settings panel.
			_("Yes"),
			# Translators: Label for the 'Cancel speech for expired &focus events' combobox
			# in the Advanced settings panel.
			_("No"),
		]

		# Translators: This is the label for combobox in the Advanced settings panel.
		cancelExpiredFocusSpeechText = _("Attempt to cancel speech for expired focus events:")
		self.cancelExpiredFocusSpeechCombo: wx.Choice = speechGroup.addLabeledControl(
			cancelExpiredFocusSpeechText,
			wx.Choice,
			choices=expiredFocusSpeechChoices,
		)
		self.bindHelpEvent("CancelExpiredFocusSpeech", self.cancelExpiredFocusSpeechCombo)
		self.cancelExpiredFocusSpeechCombo.SetSelection(
			config.conf["featureFlag"]["cancelExpiredFocusSpeech"],
		)
		self.cancelExpiredFocusSpeechCombo.defaultValue = self._getDefaultValue(
			["featureFlag", "cancelExpiredFocusSpeech"],
		)

		# Translators: This is the label for a group of advanced options in the
		#  Advanced settings panel
		label = _("Virtual Buffers")
		vBufSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=label)
		vBufGroup = guiHelper.BoxSizerHelper(vBufSizer, sizer=vBufSizer)
		sHelper.addItem(vBufGroup)

		self.loadChromeVBufWhenBusyCombo: nvdaControls.FeatureFlagCombo = vBufGroup.addLabeledControl(
			labelText=_(
				# Translators: This is the label for a combo-box in the Advanced settings panel.
				"Load Chromium virtual buffer when document busy.",
			),
			wxCtrlClass=nvdaControls.FeatureFlagCombo,
			keyPath=["virtualBuffers", "loadChromiumVBufOnBusyState"],
			conf=config.conf,
		)

		# Translators: This is the label for a group of advanced options in the
		#  Advanced settings panel
		label = _("Editable Text")
		editableSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=label)
		editableTextGroup = guiHelper.BoxSizerHelper(editableSizer, sizer=editableSizer)
		sHelper.addItem(editableTextGroup)

		# Translators: This is the label for a numeric control in the
		#  Advanced settings panel.
		label = _("Caret movement timeout (in ms)")
		self.caretMoveTimeoutSpinControl = editableTextGroup.addLabeledControl(
			label,
			nvdaControls.SelectOnFocusSpinCtrl,
			min=0,
			max=2000,
			initial=config.conf["editableText"]["caretMoveTimeoutMs"],
		)
		self.bindHelpEvent("AdvancedSettingsCaretMoveTimeout", self.caretMoveTimeoutSpinControl)
		self.caretMoveTimeoutSpinControl.defaultValue = self._getDefaultValue(
			["editableText", "caretMoveTimeoutMs"],
		)

		# Translators: This is the label for a group of advanced options in the
		# Advanced settings panel
		label = _("Document Formatting")
		docFormatting = wx.StaticBoxSizer(wx.VERTICAL, self, label=label)
		docFormattingBox = docFormatting.GetStaticBox()
		docFormattingGroup = guiHelper.BoxSizerHelper(self, sizer=docFormatting)
		sHelper.addItem(docFormattingGroup)

		# Translators: This is the label for a checkbox control in the
		#  Advanced settings panel.
		label = _("Report transparent color values")
		self.reportTransparentColorCheckBox: wx.CheckBox = docFormattingGroup.addItem(
			wx.CheckBox(docFormattingBox, label=label),
		)
		self.bindHelpEvent("ReportTransparentColors", self.reportTransparentColorCheckBox)
		self.reportTransparentColorCheckBox.SetValue(
			config.conf["documentFormatting"]["reportTransparentColor"],
		)
		self.reportTransparentColorCheckBox.defaultValue = self._getDefaultValue(
			["documentFormatting", "reportTransparentColor"],
		)

		# Translators: This is the label for a group of advanced options in the
		# Advanced settings panel
		label = _("Audio")
		audio = wx.StaticBoxSizer(wx.VERTICAL, self, label=label)
		audioGroup = guiHelper.BoxSizerHelper(self, sizer=audio)
		sHelper.addItem(audioGroup)

		# Translators: This is the label for a checkbox control in the Advanced settings panel.
		label = _("Use WASAPI for audio output (requires restart)")
		self.wasapiComboBox = cast(
			nvdaControls.FeatureFlagCombo,
			audioGroup.addLabeledControl(
				labelText=label,
				wxCtrlClass=nvdaControls.FeatureFlagCombo,
				keyPath=["audio", "WASAPI"],
				conf=config.conf,
			),
		)
		self.bindHelpEvent("WASAPI", self.wasapiComboBox)

		# Translators: This is the label for a group of advanced options in the
		# Advanced settings panel
		label = _("Debug logging")
		debugLogSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=label)
		debugLogGroup = guiHelper.BoxSizerHelper(self, sizer=debugLogSizer)
		sHelper.addItem(debugLogGroup)

		self.logCategories = [
			"hwIo",
			"MSAA",
			"UIA",
			"audioDucking",
			"gui",
			"louis",
			"timeSinceInput",
			"vision",
			"speech",
			"speechManager",
			"synthDriver",
			"nvwave",
			"annotations",
			"events",
			"garbageHandler",
		]
		# Translators: This is the label for a list in the
		#  Advanced settings panel
		logCategoriesLabel = _("Enabled logging categories")
		self.logCategoriesList = debugLogGroup.addLabeledControl(
			logCategoriesLabel,
			nvdaControls.CustomCheckListBox,
			choices=self.logCategories,
		)
		self.bindHelpEvent("AdvancedSettingsDebugLoggingCategories", self.logCategoriesList)
		self.logCategoriesList.CheckedItems = [
			index for index, x in enumerate(self.logCategories) if config.conf["debugLog"][x]
		]
		self.logCategoriesList.Select(0)
		self.logCategoriesList.defaultCheckedItems = [
			index
			for index, x in enumerate(self.logCategories)
			if bool(
				self._getDefaultValue(["debugLog", x]),
			)
		]

		# Translators: Label for the Play a sound for logged errors combobox, in the Advanced settings panel.
		label = _("Play a sound for logged e&rrors:")
		playErrorSoundChoices = (
			# Translators: Label for a value in the Play a sound for logged errors combobox, in the Advanced settings.
			pgettext("advanced.playErrorSound", "Only in NVDA test versions"),
			# Translators: Label for a value in the Play a sound for logged errors combobox, in the Advanced settings.
			pgettext("advanced.playErrorSound", "Yes"),
		)
		self.playErrorSoundCombo = debugLogGroup.addLabeledControl(
			label,
			wx.Choice,
			choices=playErrorSoundChoices,
		)
		self.bindHelpEvent("PlayErrorSound", self.playErrorSoundCombo)
		self.playErrorSoundCombo.SetSelection(config.conf["featureFlag"]["playErrorSound"])
		self.playErrorSoundCombo.defaultValue = self._getDefaultValue(["featureFlag", "playErrorSound"])

		# Translators: This is the label for a textfield in the
		# advanced settings panel.
		self.textParagraphRegexLabelText = _("Regular expression for text paragraph navigation")
		self.textParagraphRegexEdit = sHelper.addLabeledControl(
			self.textParagraphRegexLabelText,
			wxCtrlClass=wx.TextCtrl,
			size=(self.Parent.scaleSize(300), -1),
		)
		self.textParagraphRegexEdit.SetValue(config.conf["virtualBuffers"]["textParagraphRegex"])
		self.bindHelpEvent("TextParagraphRegexEdit", self.textParagraphRegexEdit)
		self.textParagraphRegexEdit.defaultValue = self._getDefaultValue(
			["virtualBuffers", "textParagraphRegex"],
		)

		self.Layout()

	def isValid(self) -> bool:
		regex = self.textParagraphRegexEdit.GetValue()
		try:
			re.compile(regex)
		except re.error as e:
			log.debugWarning("Failed to compile text paragraph regex", exc_info=True)
			self.Parent._validationErrorMessageBox(
				# Translators: Message shown when invalid text paragraph regex entered
				message=_("Failed to compile text paragraph regular expression: %s") % str(e),
				option=self.textParagraphRegexLabelText,
			)
			return False
		return True

	def onOpenScratchpadDir(self, evt):
		path = config.getScratchpadDir(ensureExists=True)
		os.startfile(path)

	def _getDefaultValue(self, configPath):
		return config.conf.getConfigValidation(configPath).default

	def haveConfigDefaultsBeenRestored(self):
		return (
			self._defaultsRestored
			and self.scratchpadCheckBox.IsChecked() == self.scratchpadCheckBox.defaultValue
			and (
				self.selectiveUIAEventRegistrationCombo.GetSelection()
				== self.selectiveUIAEventRegistrationCombo.defaultValue
			)
			and self.UIAInMSWordCombo.GetSelection() == self.UIAInMSWordCombo.defaultValue
			and self.UIAInMSExcelCheckBox.IsChecked() == self.UIAInMSExcelCheckBox.defaultValue
			and self.consoleCombo.GetSelection() == self.consoleCombo.defaultValue
			and self.UIAInChromiumCombo.GetSelection() == self.UIAInChromiumCombo.defaultValue
			and self.enhancedEventProcessingComboBox.isValueConfigSpecDefault()
			and self.annotationsDetailsCheckBox.IsChecked() == self.annotationsDetailsCheckBox.defaultValue
			and self.ariaDescCheckBox.IsChecked() == self.ariaDescCheckBox.defaultValue
			and self.brailleLiveRegionsCombo.isValueConfigSpecDefault()
			and self.keyboardSupportInLegacyCheckBox.IsChecked()
			== self.keyboardSupportInLegacyCheckBox.defaultValue
			and self.winConsoleSpeakPasswordsCheckBox.IsChecked()
			== self.winConsoleSpeakPasswordsCheckBox.defaultValue
			and self.diffAlgoCombo.GetSelection() == self.diffAlgoCombo.defaultValue
			and self.wtStrategyCombo.isValueConfigSpecDefault()
			and self.cancelExpiredFocusSpeechCombo.GetSelection()
			== self.cancelExpiredFocusSpeechCombo.defaultValue
			and self.loadChromeVBufWhenBusyCombo.isValueConfigSpecDefault()
			and self.caretMoveTimeoutSpinControl.GetValue() == self.caretMoveTimeoutSpinControl.defaultValue
			and self.reportTransparentColorCheckBox.GetValue()
			== self.reportTransparentColorCheckBox.defaultValue
			and self.wasapiComboBox.isValueConfigSpecDefault()
			and set(self.logCategoriesList.CheckedItems) == set(self.logCategoriesList.defaultCheckedItems)
			and self.playErrorSoundCombo.GetSelection() == self.playErrorSoundCombo.defaultValue
			and self.textParagraphRegexEdit.GetValue() == self.textParagraphRegexEdit.defaultValue
			and True  # reduce noise in diff when the list is extended.
		)

	def restoreToDefaults(self):
		self.scratchpadCheckBox.SetValue(self.scratchpadCheckBox.defaultValue)
		self.selectiveUIAEventRegistrationCombo.SetSelection(
			self.selectiveUIAEventRegistrationCombo.defaultValue,
		)
		self.UIAInMSWordCombo.SetSelection(self.UIAInMSWordCombo.defaultValue)
		self.UIAInMSExcelCheckBox.SetValue(self.UIAInMSExcelCheckBox.defaultValue)
		self.consoleCombo.SetSelection(self.consoleCombo.defaultValue)
		self.UIAInChromiumCombo.SetSelection(self.UIAInChromiumCombo.defaultValue)
		self.enhancedEventProcessingComboBox.resetToConfigSpecDefault()
		self.annotationsDetailsCheckBox.SetValue(self.annotationsDetailsCheckBox.defaultValue)
		self.ariaDescCheckBox.SetValue(self.ariaDescCheckBox.defaultValue)
		self.brailleLiveRegionsCombo.resetToConfigSpecDefault()
		self.winConsoleSpeakPasswordsCheckBox.SetValue(self.winConsoleSpeakPasswordsCheckBox.defaultValue)
		self.keyboardSupportInLegacyCheckBox.SetValue(self.keyboardSupportInLegacyCheckBox.defaultValue)
		self.diffAlgoCombo.SetSelection(self.diffAlgoCombo.defaultValue)
		self.wtStrategyCombo.resetToConfigSpecDefault()
		self.cancelExpiredFocusSpeechCombo.SetSelection(self.cancelExpiredFocusSpeechCombo.defaultValue)
		self.loadChromeVBufWhenBusyCombo.resetToConfigSpecDefault()
		self.caretMoveTimeoutSpinControl.SetValue(self.caretMoveTimeoutSpinControl.defaultValue)
		self.reportTransparentColorCheckBox.SetValue(self.reportTransparentColorCheckBox.defaultValue)
		self.wasapiComboBox.resetToConfigSpecDefault()
		self.logCategoriesList.CheckedItems = self.logCategoriesList.defaultCheckedItems
		self.playErrorSoundCombo.SetSelection(self.playErrorSoundCombo.defaultValue)
		self.textParagraphRegexEdit.SetValue(self.textParagraphRegexEdit.defaultValue)
		self._defaultsRestored = True

	def onSave(self):
		log.debug("Saving advanced config")
		config.conf["development"]["enableScratchpadDir"] = self.scratchpadCheckBox.IsChecked()
		selectiveUIAEventRegistrationChoice = self.selectiveUIAEventRegistrationCombo.GetSelection()
		config.conf["UIA"]["eventRegistration"] = self.selectiveUIAEventRegistrationVals[
			selectiveUIAEventRegistrationChoice
		]
		config.conf["UIA"]["allowInMSWord"] = self.UIAInMSWordCombo.GetSelection()
		config.conf["UIA"]["useInMSExcelWhenAvailable"] = self.UIAInMSExcelCheckBox.IsChecked()
		consoleChoice = self.consoleCombo.GetSelection()
		config.conf["UIA"]["winConsoleImplementation"] = self.consoleVals[consoleChoice]
		config.conf["featureFlag"]["cancelExpiredFocusSpeech"] = (
			self.cancelExpiredFocusSpeechCombo.GetSelection()
		)
		config.conf["UIA"]["allowInChromium"] = self.UIAInChromiumCombo.GetSelection()
		self.enhancedEventProcessingComboBox.saveCurrentValueToConf()
		config.conf["terminals"]["speakPasswords"] = self.winConsoleSpeakPasswordsCheckBox.IsChecked()
		config.conf["terminals"]["keyboardSupportInLegacy"] = self.keyboardSupportInLegacyCheckBox.IsChecked()
		diffAlgoChoice = self.diffAlgoCombo.GetSelection()
		config.conf["terminals"]["diffAlgo"] = self.diffAlgoVals[diffAlgoChoice]
		self.wtStrategyCombo.saveCurrentValueToConf()
		config.conf["editableText"]["caretMoveTimeoutMs"] = self.caretMoveTimeoutSpinControl.GetValue()
		config.conf["documentFormatting"]["reportTransparentColor"] = (
			self.reportTransparentColorCheckBox.IsChecked()
		)
		self.wasapiComboBox.saveCurrentValueToConf()
		config.conf["annotations"]["reportDetails"] = self.annotationsDetailsCheckBox.IsChecked()
		config.conf["annotations"]["reportAriaDescription"] = self.ariaDescCheckBox.IsChecked()
		self.brailleLiveRegionsCombo.saveCurrentValueToConf()
		self.loadChromeVBufWhenBusyCombo.saveCurrentValueToConf()

		for index, key in enumerate(self.logCategories):
			config.conf["debugLog"][key] = self.logCategoriesList.IsChecked(index)
		config.conf["featureFlag"]["playErrorSound"] = self.playErrorSoundCombo.GetSelection()
		config.conf["virtualBuffers"]["textParagraphRegex"] = self.textParagraphRegexEdit.GetValue()


class AdvancedPanel(SettingsPanel):
	enableControlsCheckBox = None  # type: wx.CheckBox
	# Translators: This is the label for the Advanced settings panel.
	title = _("Advanced")
	helpId = "AdvancedSettings"

	# Translators: This is the label to warn users about the Advanced options in the
	# Advanced settings panel
	warningHeader = _("Warning!")

	warningExplanation = _(
		# Translators: This is a label appearing on the Advanced settings panel.
		"The following settings are for advanced users. "
		"Changing them may cause NVDA to function incorrectly. "
		"Please only change these if you know what you are doing or "
		"have been specifically instructed by NVDA developers.",
	)

	panelDescription = "{}\n{}".format(warningHeader, warningExplanation)

	def makeSettings(self, settingsSizer):
		"""
		:type settingsSizer: wx.BoxSizer
		"""
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		warningSizer = wx.StaticBoxSizer(wx.VERTICAL, self)
		warningGroup = guiHelper.BoxSizerHelper(self, sizer=warningSizer)
		warningBox = warningGroup.sizer.GetStaticBox()  # type: wx.StaticBox
		sHelper.addItem(warningGroup)

		warningText = wx.StaticText(warningBox, label=self.warningHeader)
		warningText.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD))
		warningGroup.addItem(warningText)

		self.windowText = warningGroup.addItem(wx.StaticText(warningBox, label=self.warningExplanation))
		self.windowText.Wrap(self.scaleSize(PANEL_DESCRIPTION_WIDTH))

		enableAdvancedControlslabel = _(
			# Translators: This is the label for a checkbox in the Advanced settings panel.
			"I understand that changing these settings may cause NVDA to function incorrectly.",
		)
		self.enableControlsCheckBox = warningGroup.addItem(
			wx.CheckBox(parent=warningBox, label=enableAdvancedControlslabel, id=wx.NewIdRef()),
		)
		boldedFont = self.enableControlsCheckBox.GetFont().Bold()
		self.enableControlsCheckBox.SetFont(boldedFont)
		self.bindHelpEvent("AdvancedSettingsMakingChanges", self.enableControlsCheckBox)

		restoreDefaultsButton = warningGroup.addItem(
			# Translators: This is the label for a button in the Advanced settings panel
			wx.Button(warningBox, label=_("Restore defaults")),
		)
		self.bindHelpEvent("AdvancedSettingsRestoringDefaults", restoreDefaultsButton)
		restoreDefaultsButton.Bind(wx.EVT_BUTTON, lambda evt: self.advancedControls.restoreToDefaults())

		self.advancedControls = AdvancedPanelControls(self)
		sHelper.sizer.Add(self.advancedControls, flag=wx.EXPAND)

		self.enableControlsCheckBox.Bind(
			wx.EVT_CHECKBOX,
			self.onEnableControlsCheckBox,
		)
		self.advancedControls.Enable(self.enableControlsCheckBox.IsChecked())

	def onSave(self):
		if self.enableControlsCheckBox.IsChecked() or self.advancedControls.haveConfigDefaultsBeenRestored():
			self.advancedControls.onSave()

	def onEnableControlsCheckBox(self, evt):
		# due to some not very well understood mis ordering of event processing, we force NVDA to
		# process pending events. This fixes an issue where the checkbox state was being reported
		# incorrectly. This checkbox is slightly different from most, in that its behaviour is to
		# enable more controls than is typical. This might be causing enough of a delay, that there
		# is a mismatch in the state of the checkbox and when the events are processed by NVDA.
		from api import processPendingEvents

		processPendingEvents()
		self.advancedControls.Enable(evt.IsChecked())

	def isValid(self) -> bool:
		if not self.advancedControls.isValid():
			return False
		return super().isValid()


class BrailleSettingsPanel(SettingsPanel):
	# Translators: This is the label for the braille panel
	title = _("Braille")
	helpId = "BrailleSettings"

	def makeSettings(self, settingsSizer):
		settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: A label for the braille display on the braille panel.
		displayLabel = _("Braille display")

		displaySizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=displayLabel)
		displayBox = displaySizer.GetStaticBox()
		displayGroup = guiHelper.BoxSizerHelper(self, sizer=displaySizer)
		settingsSizerHelper.addItem(displayGroup)
		self.displayNameCtrl = ExpandoTextCtrl(
			displayBox,
			size=(self.scaleSize(250), -1),
			style=wx.TE_READONLY,
		)
		self.bindHelpEvent("BrailleSettingsChange", self.displayNameCtrl)
		self.updateCurrentDisplay()
		# Translators: This is the label for the button used to change braille display,
		# it appears in the context of a braille display group on the braille settings panel.
		changeDisplayBtn = wx.Button(displayBox, label=_("C&hange..."))
		self.bindHelpEvent("BrailleSettingsChange", changeDisplayBtn)
		displayGroup.addItem(
			guiHelper.associateElements(
				self.displayNameCtrl,
				changeDisplayBtn,
			),
		)
		self.displayNameCtrl.Bind(wx.EVT_CHAR_HOOK, self._enterTriggersOnChangeDisplay)
		changeDisplayBtn.Bind(wx.EVT_BUTTON, self.onChangeDisplay)

		self.brailleSubPanel = BrailleSettingsSubPanel(self)
		settingsSizerHelper.addItem(self.brailleSubPanel)

	def _enterTriggersOnChangeDisplay(self, evt):
		if evt.KeyCode == wx.WXK_RETURN:
			self.onChangeDisplay(evt)
		else:
			evt.Skip()

	def onChangeDisplay(self, evt):
		changeDisplay = BrailleDisplaySelectionDialog(self, multiInstanceAllowed=True)
		ret = changeDisplay.ShowModal()
		if ret == wx.ID_OK:
			self.Freeze()
			# trigger a refresh of the settings
			self.onPanelActivated()
			self._sendLayoutUpdatedEvent()
			self.Thaw()

	def updateCurrentDisplay(self):
		if config.conf["braille"]["display"] == braille.AUTO_DISPLAY_NAME:
			displayDesc = BrailleDisplaySelectionDialog.getCurrentAutoDisplayDescription()
		else:
			displayDesc = braille.handler.display.description
		self.displayNameCtrl.SetValue(displayDesc)

	def onPanelActivated(self):
		self.brailleSubPanel.onPanelActivated()
		super(BrailleSettingsPanel, self).onPanelActivated()

	def onPanelDeactivated(self):
		self.brailleSubPanel.onPanelDeactivated()
		super(BrailleSettingsPanel, self).onPanelDeactivated()

	def onDiscard(self):
		self.brailleSubPanel.onDiscard()

	def onSave(self):
		self.brailleSubPanel.onSave()


class BrailleDisplaySelectionDialog(SettingsDialog):
	# Translators: This is the label for the braille display selection dialog.
	title = _("Select Braille Display")
	helpId = "SelectBrailleDisplay"
	displayNames = []
	possiblePorts = []

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		# Translators: The label for a setting in braille settings to choose a braille display.
		displayLabelText = _("Braille &display:")
		self.displayList = sHelper.addLabeledControl(displayLabelText, wx.Choice, choices=[])
		self.bindHelpEvent("SelectBrailleDisplayDisplay", self.displayList)
		self.Bind(wx.EVT_CHOICE, self.onDisplayNameChanged, self.displayList)

		# Translators: The label for a setting in braille settings to enable displays for automatic detection.
		autoDetectLabelText = _("&Displays to detect automatically:")
		self.autoDetectList = sHelper.addLabeledControl(
			autoDetectLabelText,
			nvdaControls.CustomCheckListBox,
			choices=[],
		)
		self.bindHelpEvent("SelectBrailleDisplayAutoDetect", self.autoDetectList)

		# Translators: The label for a setting in braille settings to choose the connection port (if the selected braille display supports port selection).
		portsLabelText = _("&Port:")
		self.portsList = sHelper.addLabeledControl(portsLabelText, wx.Choice, choices=[])
		self.bindHelpEvent("SelectBrailleDisplayPort", self.portsList)

		self.updateBrailleDisplayLists()
		self.updateStateDependentControls()

	def postInit(self):
		# Finally, ensure that focus is on the list of displays.
		self.displayList.SetFocus()

	@staticmethod
	def getCurrentAutoDisplayDescription():
		description = braille.AUTOMATIC_PORT[1]
		if (
			config.conf["braille"]["display"] == braille.AUTO_DISPLAY_NAME
			and braille.handler.display.name != "noBraille"
		):
			description = "%s (%s)" % (description, braille.handler.display.description)
		return description

	def updateBrailleDisplayLists(self):
		driverList = [(braille.AUTO_DISPLAY_NAME, self.getCurrentAutoDisplayDescription())]
		driverList.extend(braille.getDisplayList())
		self.displayNames = [driver[0] for driver in driverList]
		displayChoices = [driver[1] for driver in driverList]
		self.displayList.Clear()
		self.displayList.AppendItems(displayChoices)
		try:
			if config.conf["braille"]["display"] == braille.AUTO_DISPLAY_NAME:
				selection = 0
			else:
				selection = self.displayNames.index(braille.handler.display.name)
			self.displayList.SetSelection(selection)
		except:  # noqa: E722
			pass

		import bdDetect

		autoDetectDrivers = list(bdDetect.getSupportedBrailleDisplayDrivers())
		autoDetectDrivers.sort(key=lambda d: strxfrm(d.description))
		autoDetectChoices = [d.description for d in autoDetectDrivers]
		self.autoDetectValues = [d.name for d in autoDetectDrivers]
		self.autoDetectList.Items = autoDetectChoices
		self.autoDetectList.CheckedItems = [
			i
			for i, n in enumerate(self.autoDetectValues)
			if n in bdDetect.getBrailleDisplayDriversEnabledForDetection()
		]
		self.autoDetectList.Selection = 0

	def updateStateDependentControls(self):
		displayName = self.displayNames[self.displayList.GetSelection()]
		self.possiblePorts = []
		isAutoDisplaySelected = displayName == braille.AUTOMATIC_PORT[0]
		if not isAutoDisplaySelected:
			displayCls = braille._getDisplayDriver(displayName)
			try:
				self.possiblePorts.extend(displayCls.getPossiblePorts().items())
			except NotImplementedError:
				pass
		if self.possiblePorts:
			self.portsList.SetItems([p[1] for p in self.possiblePorts])
			try:
				selectedPort = config.conf["braille"][displayName].get("port")
				portNames = [p[0] for p in self.possiblePorts]
				selection = portNames.index(selectedPort)
			except (KeyError, ValueError):
				# Display name not in config or port not valid
				selection = 0
			self.portsList.SetSelection(selection)
		# If no port selection is possible or only automatic selection is available, disable the port selection control
		enable = len(self.possiblePorts) > 0 and not (
			len(self.possiblePorts) == 1 and self.possiblePorts[0][0] == "auto"
		)
		self.portsList.Enable(enable)

		self.autoDetectList.Enable(isAutoDisplaySelected)

	def onDisplayNameChanged(self, evt):
		self.updateStateDependentControls()

	def onOk(self, evt):
		if not self.displayNames:
			# The list of displays has not been populated yet, so we didn't change anything in this panel
			return
		display = self.displayNames[self.displayList.GetSelection()]
		if display not in config.conf["braille"]:
			config.conf["braille"][display] = {}
		if self.possiblePorts:
			port = self.possiblePorts[self.portsList.GetSelection()][0]
			config.conf["braille"][display]["port"] = port
		if self.autoDetectList.IsEnabled():
			# Excluded drivers that are not loaded (e.g. because add-ons are disabled) should be persisted.
			unknownDriversExcluded = [
				n
				for n in config.conf["braille"]["auto"]["excludedDisplays"]
				if n not in self.autoDetectValues
			]
			config.conf["braille"]["auto"]["excludedDisplays"] = [
				n for i, n in enumerate(self.autoDetectValues) if i not in self.autoDetectList.CheckedItems
			] + unknownDriversExcluded

		if not braille.handler.setDisplayByName(display):
			gui.messageBox(
				# Translators: The message in a dialog presented when NVDA is unable to load the selected
				# braille display.
				message=_("Could not load the {display} display.").format(display=display),
				# Translators: The title in a dialog presented when NVDA is unable to load the selected
				# braille display.
				caption=_("Braille Display Error"),
				style=wx.OK | wx.ICON_WARNING,
				parent=self,
			)
			return

		if self.IsModal():
			# Hack: we need to update the display in our parent window before closing.
			# Otherwise, NVDA will report the old display even though the new display is reflected visually.
			self.Parent.updateCurrentDisplay()
		super(BrailleDisplaySelectionDialog, self).onOk(evt)


class BrailleSettingsSubPanel(AutoSettingsMixin, SettingsPanel):
	helpId = "BrailleSettings"

	@property
	def driver(self):
		return braille.handler.display

	def getSettings(self) -> AutoSettings:
		return self.driver

	def makeSettings(self, settingsSizer):
		shouldDebugGui = gui._isDebug()
		startTime = 0 if not shouldDebugGui else time.time()
		# Construct braille display specific settings
		self.updateDriverSettings()

		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		tables = brailleTables.listTables()
		# Translators: The label for a setting in braille settings to select the output table (the braille table used to read braille text on the braille display).
		outputsLabelText = _("&Output table:")
		self.outTables = [table for table in tables if table.output]
		self.outTableNames = [table.fileName for table in self.outTables]
		outTableChoices = [table.displayName for table in self.outTables]
		self.outTableList = sHelper.addLabeledControl(outputsLabelText, wx.Choice, choices=outTableChoices)
		self.bindHelpEvent("BrailleSettingsOutputTable", self.outTableList)
		try:
			selection = self.outTables.index(braille.handler.table)
			self.outTableList.SetSelection(selection)
		except:  # noqa: E722
			log.exception()
		if shouldDebugGui:
			timePassed = time.time() - startTime
			log.debug(
				f"Loading output tables completed, now at {timePassed:.2f} seconds from start",
			)

		# Translators: The label for a setting in braille settings to select the input table (the braille table used to type braille characters on a braille keyboard).
		inputLabelText = _("&Input table:")
		self.inTables = [table for table in tables if table.input]
		inTableChoices = [table.displayName for table in self.inTables]
		self.inTableList = sHelper.addLabeledControl(inputLabelText, wx.Choice, choices=inTableChoices)
		self.bindHelpEvent("BrailleSettingsInputTable", self.inTableList)
		try:
			selection = self.inTables.index(brailleInput.handler.table)
			self.inTableList.SetSelection(selection)
		except:  # noqa: E722
			log.exception()
		if shouldDebugGui:
			timePassed = time.time() - startTime
			log.debug(
				f"Loading input tables completed, now at {timePassed:.2f} seconds from start",
			)
		# Translators: The label for a setting in braille settings to select which braille mode to use
		modeListText = _("Braille mode:")
		modeChoices = [x.displayString for x in braille.BrailleMode]
		self.brailleModes = sHelper.addLabeledControl(modeListText, wx.Choice, choices=modeChoices)
		self.bindHelpEvent("BrailleMode", self.brailleModes)
		self.brailleModes.Bind(wx.EVT_CHOICE, self._onModeChange)
		current = braille.BrailleMode(config.conf["braille"]["mode"])
		modeList = list(braille.BrailleMode)
		index = modeList.index(current)
		self.brailleModes.SetSelection(index)
		followCursorGroupSizer = wx.StaticBoxSizer(wx.VERTICAL, self)
		self.followCursorGroupBox = followCursorGroupSizer.GetStaticBox()
		followCursorGroupHelper = guiHelper.BoxSizerHelper(self, sizer=followCursorGroupSizer)
		sHelper.addItem(followCursorGroupHelper)

		# Translators: The label for a setting in braille settings to expand the current word under cursor to computer braille.
		expandAtCursorText = _("E&xpand to computer braille for the word at the cursor")
		self.expandAtCursorCheckBox = followCursorGroupHelper.addItem(
			wx.CheckBox(self.followCursorGroupBox, wx.ID_ANY, label=expandAtCursorText),
		)
		self.bindHelpEvent("BrailleSettingsExpandToComputerBraille", self.expandAtCursorCheckBox)
		self.expandAtCursorCheckBox.SetValue(config.conf["braille"]["expandAtCursor"])

		# Translators: The label for a setting in braille settings to show the cursor.
		showCursorLabelText = _("&Show cursor")
		self.showCursorCheckBox = followCursorGroupHelper.addItem(
			wx.CheckBox(self.followCursorGroupBox, label=showCursorLabelText),
		)
		self.bindHelpEvent("BrailleSettingsShowCursor", self.showCursorCheckBox)
		self.showCursorCheckBox.Bind(wx.EVT_CHECKBOX, self.onShowCursorChange)
		self.showCursorCheckBox.SetValue(config.conf["braille"]["showCursor"])

		# Translators: The label for a setting in braille settings to enable cursor blinking.
		cursorBlinkLabelText = _("Blink cursor")
		self.cursorBlinkCheckBox = followCursorGroupHelper.addItem(
			wx.CheckBox(self.followCursorGroupBox, label=cursorBlinkLabelText),
		)
		self.bindHelpEvent("BrailleSettingsBlinkCursor", self.cursorBlinkCheckBox)
		self.cursorBlinkCheckBox.Bind(wx.EVT_CHECKBOX, self.onBlinkCursorChange)
		self.cursorBlinkCheckBox.SetValue(config.conf["braille"]["cursorBlink"])
		if not self.showCursorCheckBox.GetValue():
			self.cursorBlinkCheckBox.Disable()

		# Translators: The label for a setting in braille settings to change cursor blink rate in milliseconds (1 second is 1000 milliseconds).
		cursorBlinkRateLabelText = _("Cursor blink rate (ms)")
		minBlinkRate = int(
			config.conf.getConfigValidation(
				("braille", "cursorBlinkRate"),
			).kwargs["min"],
		)
		maxBlinkRate = int(config.conf.getConfigValidation(("braille", "cursorBlinkRate")).kwargs["max"])
		self.cursorBlinkRateEdit = followCursorGroupHelper.addLabeledControl(
			cursorBlinkRateLabelText,
			nvdaControls.SelectOnFocusSpinCtrl,
			min=minBlinkRate,
			max=maxBlinkRate,
			initial=config.conf["braille"]["cursorBlinkRate"],
		)
		self.bindHelpEvent("BrailleSettingsBlinkRate", self.cursorBlinkRateEdit)
		if not self.showCursorCheckBox.GetValue() or not self.cursorBlinkCheckBox.GetValue():
			self.cursorBlinkRateEdit.Disable()

		self.cursorShapes = [s[0] for s in braille.CURSOR_SHAPES]
		cursorShapeChoices = [s[1] for s in braille.CURSOR_SHAPES]

		# Translators: The label for a setting in braille settings to select the cursor shape when tethered to focus.
		cursorShapeFocusLabelText = _("Cursor shape for &focus:")
		self.cursorShapeFocusList = followCursorGroupHelper.addLabeledControl(
			cursorShapeFocusLabelText,
			wx.Choice,
			choices=cursorShapeChoices,
		)
		self.bindHelpEvent("BrailleSettingsCursorShapeForFocus", self.cursorShapeFocusList)
		try:
			selection = self.cursorShapes.index(config.conf["braille"]["cursorShapeFocus"])
			self.cursorShapeFocusList.SetSelection(selection)
		except:  # noqa: E722
			pass
		if not self.showCursorCheckBox.GetValue():
			self.cursorShapeFocusList.Disable()

		# Translators: The label for a setting in braille settings to select the cursor shape when tethered to review.
		cursorShapeReviewLabelText = _("Cursor shape for &review:")
		self.cursorShapeReviewList = followCursorGroupHelper.addLabeledControl(
			cursorShapeReviewLabelText,
			wx.Choice,
			choices=cursorShapeChoices,
		)
		self.bindHelpEvent("BrailleSettingsCursorShapeForReview", self.cursorShapeReviewList)
		try:
			selection = self.cursorShapes.index(config.conf["braille"]["cursorShapeReview"])
			self.cursorShapeReviewList.SetSelection(selection)
		except:  # noqa: E722
			pass
		if not self.showCursorCheckBox.GetValue():
			self.cursorShapeReviewList.Disable()
		if gui._isDebug():
			log.debug(
				"Loading cursor settings completed, now at %.2f seconds from start"
				% (time.time() - startTime),
			)

		# Translators: The label for a setting in braille settings to combobox enabling user
		# to decide if braille messages should be shown and automatically disappear from braille display.
		showMessagesText = _("Show messages")
		showMessagesChoices = [i.displayString for i in ShowMessages]
		self.showMessagesList = followCursorGroupHelper.addLabeledControl(
			showMessagesText,
			wx.Choice,
			choices=showMessagesChoices,
		)
		self.bindHelpEvent("BrailleSettingsShowMessages", self.showMessagesList)
		self.showMessagesList.Bind(wx.EVT_CHOICE, self.onShowMessagesChange)
		self.showMessagesList.SetSelection(config.conf["braille"]["showMessages"])

		minTimeout = int(
			config.conf.getConfigValidation(
				("braille", "messageTimeout"),
			).kwargs["min"],
		)
		maxTimeOut = int(
			config.conf.getConfigValidation(
				("braille", "messageTimeout"),
			).kwargs["max"],
		)
		# Translators: The label for a setting in braille settings to change how long a message stays on the braille display (in seconds).
		messageTimeoutText = _("Message &timeout (sec)")
		self.messageTimeoutEdit = followCursorGroupHelper.addLabeledControl(
			messageTimeoutText,
			nvdaControls.SelectOnFocusSpinCtrl,
			min=minTimeout,
			max=maxTimeOut,
			initial=config.conf["braille"]["messageTimeout"],
		)
		self.bindHelpEvent("BrailleSettingsMessageTimeout", self.messageTimeoutEdit)
		if self.showMessagesList.GetSelection() != ShowMessages.USE_TIMEOUT:
			self.messageTimeoutEdit.Disable()

		if gui._isDebug():
			log.debug(
				"Loading timeout settings completed, now at %.2f seconds from start"
				% (time.time() - startTime),
			)

		# Translators: The label for a setting in braille settings to set whether braille should be tethered to focus or review cursor.
		tetherListText = _("Tether B&raille:")
		# Translators: The value for a setting in the braille settings, to set whether braille should be tethered to
		# focus or review cursor.
		tetherChoices = [x[1] for x in braille.handler.tetherValues]
		self.tetherList = followCursorGroupHelper.addLabeledControl(
			tetherListText,
			wx.Choice,
			choices=tetherChoices,
		)
		self.bindHelpEvent("BrailleTether", self.tetherList)
		self.tetherList.Bind(wx.EVT_CHOICE, self.onTetherToChange)
		tetherChoice = config.conf["braille"]["tetherTo"]
		selection = [x.value for x in TetherTo].index(tetherChoice)
		self.tetherList.SetSelection(selection)
		if gui._isDebug():
			log.debug(
				"Loading tether settings completed, now at %.2f seconds from start"
				% (time.time() - startTime),
			)

		self.brailleReviewRoutingMovesSystemCaretCombo: nvdaControls.FeatureFlagCombo = (
			followCursorGroupHelper.addLabeledControl(
				labelText=_(
					# Translators: This is a label for a combo-box in the Braille settings panel.
					"Move system caret when ro&uting review cursor",
				),
				wxCtrlClass=nvdaControls.FeatureFlagCombo,
				keyPath=["braille", "reviewRoutingMovesSystemCaret"],
				conf=config.conf,
			)
		)
		self.bindHelpEvent(
			"BrailleSettingsReviewRoutingMovesSystemCaret",
			self.brailleReviewRoutingMovesSystemCaretCombo,
		)
		# Setting has no effect when braille is tethered to focus.
		if tetherChoice == TetherTo.FOCUS.value:
			self.brailleReviewRoutingMovesSystemCaretCombo.Disable()

		# Translators: The label for a setting in braille settings to read by paragraph (if it is checked, the commands to move the display by lines moves the display by paragraphs instead).
		readByParagraphText = _("Read by &paragraph")
		self.readByParagraphCheckBox = followCursorGroupHelper.addItem(
			wx.CheckBox(self.followCursorGroupBox, label=readByParagraphText),
		)
		self.bindHelpEvent("BrailleSettingsReadByParagraph", self.readByParagraphCheckBox)
		self.readByParagraphCheckBox.Bind(wx.EVT_CHECKBOX, self.onReadByParagraphChange)
		self.readByParagraphCheckBox.Value = config.conf["braille"]["readByParagraph"]

		# Translators: This is a label for a combo-box in the Braille settings panel to select paragraph start markers.
		labelText = _("Paragraph start marker:")
		self.paragraphStartMarkersComboBox = followCursorGroupHelper.addLabeledControl(
			labelText,
			wx.Choice,
			choices=[marker.displayString for marker in ParagraphStartMarker],
		)
		self.bindHelpEvent("BrailleParagraphStartMarkers", self.paragraphStartMarkersComboBox)
		paragraphStartMarker = config.conf["braille"]["paragraphStartMarker"]
		self.paragraphStartMarkersComboBox.SetSelection(
			[marker.value for marker in ParagraphStartMarker].index(paragraphStartMarker),
		)
		if not self.readByParagraphCheckBox.GetValue():
			self.paragraphStartMarkersComboBox.Disable()

		# Translators: The label for a setting in braille settings to select how the context for the focus object should be presented on a braille display.
		focusContextPresentationLabelText = _("Focus context presentation:")
		self.focusContextPresentationValues = [x[0] for x in braille.focusContextPresentations]
		focusContextPresentationChoices = [x[1] for x in braille.focusContextPresentations]
		self.focusContextPresentationList = followCursorGroupHelper.addLabeledControl(
			focusContextPresentationLabelText,
			wx.Choice,
			choices=focusContextPresentationChoices,
		)
		self.bindHelpEvent("BrailleSettingsFocusContextPresentation", self.focusContextPresentationList)
		try:
			index = self.focusContextPresentationValues.index(
				config.conf["braille"]["focusContextPresentation"],
			)
		except:  # noqa: E722
			index = 0
		self.focusContextPresentationList.SetSelection(index)

		self.brailleShowSelectionCombo: nvdaControls.FeatureFlagCombo = (
			followCursorGroupHelper.addLabeledControl(
				labelText=_(
					# Translators: This is a label for a combo-box in the Braille settings panel.
					"Show se&lection",
				),
				wxCtrlClass=nvdaControls.FeatureFlagCombo,
				keyPath=["braille", "showSelection"],
				conf=config.conf,
			)
		)
		self.bindHelpEvent("BrailleSettingsShowSelection", self.brailleShowSelectionCombo)

		self.formattingDisplayCombo: nvdaControls.FeatureFlagCombo = (
			followCursorGroupHelper.addLabeledControl(
				# Translators: This is a label for a combo-box in the Braille settings panel.
				labelText=_("Formatting &display"),
				wxCtrlClass=nvdaControls.FeatureFlagCombo,
				keyPath=("braille", "fontFormattingDisplay"),
				conf=config.conf,
			)
		)
		self.bindHelpEvent("BrailleFormattingDisplay", self.formattingDisplayCombo)

		# Translators: The label for a setting in braille settings to speak the character under the cursor when cursor routing in text.
		speakOnRoutingText = _("Spea&k character when routing cursor in text")
		self.speakOnRoutingCheckBox = followCursorGroupHelper.addItem(
			wx.CheckBox(self.followCursorGroupBox, label=speakOnRoutingText),
		)
		self.bindHelpEvent("BrailleSpeakOnRouting", self.speakOnRoutingCheckBox)
		self.speakOnRoutingCheckBox.Value = config.conf["braille"]["speakOnRouting"]

		self.followCursorGroupBox.Enable(
			list(braille.BrailleMode)[self.brailleModes.GetSelection()] is braille.BrailleMode.FOLLOW_CURSORS,
		)

		# Translators: The label for a setting in braille settings to enable word wrap
		# (try to avoid splitting words at the end of the braille display).
		wordWrapText = _("Avoid splitting &words when possible")
		self.wordWrapCheckBox = sHelper.addItem(wx.CheckBox(self, label=wordWrapText))
		self.bindHelpEvent("BrailleSettingsWordWrap", self.wordWrapCheckBox)
		self.wordWrapCheckBox.Value = config.conf["braille"]["wordWrap"]

		self.unicodeNormalizationCombo: nvdaControls.FeatureFlagCombo = sHelper.addLabeledControl(
			labelText=_(
				# Translators: This is a label for a combo-box in the Braille settings panel.
				"Unicode normali&zation",
			),
			wxCtrlClass=nvdaControls.FeatureFlagCombo,
			keyPath=["braille", "unicodeNormalization"],
			conf=config.conf,
		)
		self.bindHelpEvent("BrailleUnicodeNormalization", self.unicodeNormalizationCombo)

		self.brailleInterruptSpeechCombo: nvdaControls.FeatureFlagCombo = sHelper.addLabeledControl(
			labelText=_(
				# Translators: This is a label for a combo-box in the Braille settings panel.
				"I&nterrupt speech while scrolling",
			),
			wxCtrlClass=nvdaControls.FeatureFlagCombo,
			keyPath=["braille", "interruptSpeechWhileScrolling"],
			conf=config.conf,
		)
		self.bindHelpEvent("BrailleSettingsInterruptSpeech", self.brailleInterruptSpeechCombo)

		if gui._isDebug():
			log.debug("Finished making settings, now at %.2f seconds from start" % (time.time() - startTime))

	def onSave(self):
		AutoSettingsMixin.onSave(self)

		braille.handler.table = self.outTables[self.outTableList.GetSelection()]
		brailleInput.handler.table = self.inTables[self.inTableList.GetSelection()]
		mode = list(braille.BrailleMode)[self.brailleModes.GetSelection()]
		config.conf["braille"]["mode"] = mode.value
		braille.handler.mainBuffer.clear()
		config.conf["braille"]["translationTable"] = self.outTableNames[self.outTableList.GetSelection()]
		config.conf["braille"]["expandAtCursor"] = self.expandAtCursorCheckBox.GetValue()
		config.conf["braille"]["showCursor"] = self.showCursorCheckBox.GetValue()
		config.conf["braille"]["cursorBlink"] = self.cursorBlinkCheckBox.GetValue()
		config.conf["braille"]["cursorBlinkRate"] = self.cursorBlinkRateEdit.GetValue()
		config.conf["braille"]["cursorShapeFocus"] = self.cursorShapes[
			self.cursorShapeFocusList.GetSelection()
		]
		config.conf["braille"]["cursorShapeReview"] = self.cursorShapes[
			self.cursorShapeReviewList.GetSelection()
		]
		config.conf["braille"]["showMessages"] = self.showMessagesList.GetSelection()
		config.conf["braille"]["messageTimeout"] = self.messageTimeoutEdit.GetValue()
		tetherChoice = [x.value for x in TetherTo][self.tetherList.GetSelection()]
		if tetherChoice == TetherTo.AUTO.value:
			config.conf["braille"]["tetherTo"] = TetherTo.AUTO.value
		else:
			braille.handler.setTether(tetherChoice, auto=False)
		self.brailleReviewRoutingMovesSystemCaretCombo.saveCurrentValueToConf()
		config.conf["braille"]["readByParagraph"] = self.readByParagraphCheckBox.Value
		config.conf["braille"]["paragraphStartMarker"] = [marker.value for marker in ParagraphStartMarker][
			self.paragraphStartMarkersComboBox.GetSelection()
		]
		config.conf["braille"]["speakOnRouting"] = self.speakOnRoutingCheckBox.Value
		config.conf["braille"]["wordWrap"] = self.wordWrapCheckBox.Value
		self.unicodeNormalizationCombo.saveCurrentValueToConf()
		config.conf["braille"]["focusContextPresentation"] = self.focusContextPresentationValues[
			self.focusContextPresentationList.GetSelection()
		]
		self.brailleInterruptSpeechCombo.saveCurrentValueToConf()
		self.brailleShowSelectionCombo.saveCurrentValueToConf()
		self.formattingDisplayCombo.saveCurrentValueToConf()

	def onShowCursorChange(self, evt):
		self.cursorBlinkCheckBox.Enable(evt.IsChecked())
		self.cursorBlinkRateEdit.Enable(evt.IsChecked() and self.cursorBlinkCheckBox.GetValue())
		self.cursorShapeFocusList.Enable(evt.IsChecked())
		self.cursorShapeReviewList.Enable(evt.IsChecked())

	def onBlinkCursorChange(self, evt):
		self.cursorBlinkRateEdit.Enable(evt.IsChecked())

	def onShowMessagesChange(self, evt):
		self.messageTimeoutEdit.Enable(evt.GetSelection() == 1)

	def onTetherToChange(self, evt: wx.CommandEvent) -> None:
		"""Shows or hides "Move system caret when routing review cursor" braille setting."""
		tetherChoice = [x.value for x in TetherTo][evt.GetSelection()]
		self.brailleReviewRoutingMovesSystemCaretCombo.Enable(tetherChoice != TetherTo.FOCUS.value)

	def onReadByParagraphChange(self, evt: wx.CommandEvent):
		self.paragraphStartMarkersComboBox.Enable(evt.IsChecked())

	def _onModeChange(self, evt: wx.CommandEvent):
		self.followCursorGroupBox.Enable(not evt.GetSelection())


def showStartErrorForProviders(
	parent: wx.Window,
	providers: List[vision.providerInfo.ProviderInfo],
) -> None:
	if not providers:
		return

	if len(providers) == 1:
		providerName = providers[0].displayName
		# Translators: This message is presented when
		# NVDA is unable to load a single vision enhancement provider.
		message = _("Could not load the {providerName} vision enhancement provider").format(
			providerName=providerName,
		)
	else:
		providerNames = ", ".join(provider.displayName for provider in providers)
		# Translators: This message is presented when NVDA is unable to
		# load multiple vision enhancement providers.
		message = _("Could not load the following vision enhancement providers:\n{providerNames}").format(
			providerNames=providerNames,
		)
	gui.messageBox(
		message,
		# Translators: The title of the vision enhancement provider error message box.
		_("Vision Enhancement Provider Error"),
		wx.OK | wx.ICON_WARNING,
		parent,
	)


def showTerminationErrorForProviders(
	parent: wx.Window,
	providers: List[vision.providerInfo.ProviderInfo],
) -> None:
	if not providers:
		return

	if len(providers) == 1:
		providerName = providers[0].displayName
		# Translators: This message is presented when
		# NVDA is unable to gracefully terminate a single vision enhancement provider.
		message = _("Could not gracefully terminate the {providerName} vision enhancement provider").format(
			providerName=providerName,
		)
	else:
		providerNames = ", ".join(provider.displayName for provider in providers)
		message = _(
			# Translators: This message is presented when
			# NVDA is unable to terminate multiple vision enhancement providers.
			"Could not gracefully terminate the following vision enhancement providers:\n" "{providerNames}",
		).format(providerNames=providerNames)
	gui.messageBox(
		message,
		# Translators: The title of the vision enhancement provider error message box.
		_("Vision Enhancement Provider Error"),
		wx.OK | wx.ICON_WARNING,
		parent,
	)


class VisionProviderStateControl(vision.providerBase.VisionProviderStateControl):
	"""
	Gives settings panels for vision enhancement providers a way to control a
	single vision enhancement provider, handling any error conditions in
	a UX friendly way.
	"""

	def __init__(
		self,
		parent: wx.Window,
		providerInfo: vision.providerInfo.ProviderInfo,
	):
		self._providerInfo = providerInfo
		self._parent = weakref.ref(parent)  # don't keep parent dialog alive with a circular reference.

	def getProviderInfo(self) -> vision.providerInfo.ProviderInfo:
		return self._providerInfo

	def getProviderInstance(self) -> Optional[vision.providerBase.VisionEnhancementProvider]:
		return vision.handler.getProviderInstance(self._providerInfo)

	def startProvider(
		self,
		shouldPromptOnError: bool = True,
	) -> bool:
		"""Initializes the provider, prompting user with the error if necessary.
		@param shouldPromptOnError: True if  the user should be presented with any errors that may occur.
		@return: True on success
		"""
		success = self._doStartProvider()
		if not success and shouldPromptOnError:
			showStartErrorForProviders(self._parent(), [self._providerInfo])
		return success

	def terminateProvider(
		self,
		shouldPromptOnError: bool = True,
	) -> bool:
		"""Terminate the provider, prompting user with the error if necessary.
		@param shouldPromptOnError: True if  the user should be presented with any errors that may occur.
		@return: True on success
		"""
		success = self._doTerminate()
		if not success and shouldPromptOnError:
			showTerminationErrorForProviders(self._parent(), [self._providerInfo])
		return success

	def _doStartProvider(self) -> bool:
		"""Attempt to start the provider, catching any errors.
		@return True on successful termination.
		"""
		try:
			vision.handler.initializeProvider(self._providerInfo)
			return True
		except Exception:
			log.error(
				f"Could not initialize the {self._providerInfo.providerId} vision enhancement provider",
				exc_info=True,
			)
			return False

	def _doTerminate(self) -> bool:
		"""Attempt to terminate the provider, catching any errors.
		@return True on successful termination.
		"""
		try:
			# Terminating a provider from the gui should never save the settings.
			# This is because termination happens on the fly when unchecking check boxes.
			# Saving settings would be harmful if a user opens the vision panel,
			# then changes some settings and disables the provider.
			vision.handler.terminateProvider(self._providerInfo, saveSettings=False)
			return True
		except Exception:
			log.error(
				f"Could not terminate the {self._providerInfo.providerId} vision enhancement provider",
				exc_info=True,
			)
			return False


class VisionSettingsPanel(SettingsPanel):
	settingsSizerHelper: guiHelper.BoxSizerHelper
	providerPanelInstances: List[SettingsPanel]
	initialProviders: List[vision.providerInfo.ProviderInfo]
	# Translators: This is the label for the vision panel
	title = _("Vision")
	helpId = "VisionSettings"

	# Translators: This is a label appearing on the vision settings panel.
	panelDescription = _("Configure visual aids.")

	def _createProviderSettingsPanel(
		self,
		providerInfo: vision.providerInfo.ProviderInfo,
	) -> Optional[SettingsPanel]:
		settingsPanelCls = providerInfo.providerClass.getSettingsPanelClass()
		if not settingsPanelCls:
			if gui._isDebug():
				log.debug(f"Using default panel for providerId: {providerInfo.providerId}")
			settingsPanelCls = VisionProviderSubPanel_Wrapper
		else:
			if gui._isDebug():
				log.debug(f"Using custom panel for providerId: {providerInfo.providerId}")

		providerControl = VisionProviderStateControl(parent=self, providerInfo=providerInfo)
		try:
			return settingsPanelCls(
				parent=self,
				providerControl=providerControl,
			)
		# Broad except used since we can not know what exceptions a provider might throw.
		# We should be able to continue despite a buggy provider.
		except Exception:
			log.debug(f"Error creating providerPanel: {settingsPanelCls!r}", exc_info=True)
			return None

	def makeSettings(self, settingsSizer: wx.BoxSizer):
		self.initialProviders = vision.handler.getActiveProviderInfos()
		self.providerPanelInstances = []
		self.settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.settingsSizerHelper.addItem(wx.StaticText(self, label=self.panelDescription))

		for providerInfo in vision.handler.getProviderList(reloadFromSystem=True):
			providerSizer = self.settingsSizerHelper.addItem(
				wx.StaticBoxSizer(wx.VERTICAL, self, label=providerInfo.displayName),
				flag=wx.EXPAND,
			)
			if len(self.providerPanelInstances) > 0:
				settingsSizer.AddSpacer(guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)

			settingsPanel = self._createProviderSettingsPanel(providerInfo)
			if not settingsPanel:
				continue

			providerSizer.Add(settingsPanel, flag=wx.EXPAND)
			self.providerPanelInstances.append(settingsPanel)

	def safeInitProviders(
		self,
		providers: List[vision.providerInfo.ProviderInfo],
	) -> None:
		"""Initializes one or more providers in a way that is gui friendly,
		showing an error if appropriate.
		"""
		errorProviders: List[vision.providerInfo.ProviderInfo] = []
		for provider in providers:
			success = VisionProviderStateControl(self, provider).startProvider(shouldPromptOnError=False)
			if not success:
				errorProviders.append(provider)
		showStartErrorForProviders(self, errorProviders)

	def safeTerminateProviders(
		self,
		providers: List[vision.providerInfo.ProviderInfo],
		verbose: bool = False,
	) -> None:
		"""Terminates one or more providers in a way that is gui friendly,
		@verbose: Whether to show a termination error.
		@returns: Whether termination succeeded for all providers.
		"""
		errorProviders: List[vision.providerInfo.ProviderInfo] = []
		for provider in providers:
			success = VisionProviderStateControl(self, provider).terminateProvider(shouldPromptOnError=False)
			if not success:
				errorProviders.append(provider)
		if verbose:
			showTerminationErrorForProviders(self, errorProviders)

	def refreshPanel(self):
		self.Freeze()
		# trigger a refresh of the settings
		self.onPanelActivated()
		self._sendLayoutUpdatedEvent()
		self.Thaw()

	def onPanelActivated(self):
		super().onPanelActivated()

	def onDiscard(self):
		for panel in self.providerPanelInstances:
			try:
				panel.onDiscard()
			# Broad except used since we can not know what exceptions a provider might throw.
			# We should be able to continue despite a buggy provider.
			except Exception:
				log.debug(f"Error discarding providerPanel: {panel.__class__!r}", exc_info=True)

		providersToInitialize = [
			provider
			for provider in self.initialProviders
			if not bool(vision.handler.getProviderInstance(provider))
		]
		self.safeInitProviders(providersToInitialize)
		initialProviderIds = [providerInfo.providerId for providerInfo in self.initialProviders]
		providersToTerminate = [
			provider
			for provider in vision.handler.getActiveProviderInfos()
			if provider.providerId not in initialProviderIds
		]
		self.safeTerminateProviders(providersToTerminate)

	def onSave(self):
		for panel in self.providerPanelInstances:
			try:
				panel.onSave()
			# Broad except used since we can not know what exceptions a provider might throw.
			# We should be able to continue despite a buggy provider.
			except Exception:
				log.debug(f"Error saving providerPanel: {panel.__class__!r}", exc_info=True)
		self.initialProviders = vision.handler.getActiveProviderInfos()


class VisionProviderSubPanel_Settings(
	AutoSettingsMixin,
	SettingsPanel,
):
	helpId = "VisionSettings"

	_settingsCallable: Callable[[], VisionEnhancementProviderSettings]

	def __init__(
		self,
		parent: wx.Window,
		*,  # Make next argument keyword only
		settingsCallable: Callable[[], vision.providerBase.VisionEnhancementProviderSettings],
	):
		"""
		@param settingsCallable: A callable that returns an instance to a VisionEnhancementProviderSettings.
			This will usually be a weakref, but could be any callable taking no arguments.
		"""
		self._settingsCallable = settingsCallable
		super().__init__(parent=parent)

	def getSettings(self) -> AutoSettings:
		settings = self._settingsCallable()
		return settings

	def makeSettings(self, settingsSizer):
		# Construct vision enhancement provider settings
		self.updateDriverSettings()


class VisionProviderSubPanel_Wrapper(
	SettingsPanel,
):
	_checkBox: wx.CheckBox

	def __init__(
		self,
		parent: wx.Window,
		providerControl: VisionProviderStateControl,
	):
		self._providerControl = providerControl
		self._providerSettings: Optional[VisionProviderSubPanel_Settings] = None
		self._providerSettingsSizer = wx.BoxSizer(orient=wx.VERTICAL)
		super().__init__(parent=parent)

	def makeSettings(self, settingsSizer):
		self._checkBox = wx.CheckBox(
			self,
			# Translators: Enable checkbox on a vision enhancement provider on the vision settings category panel
			label=_("Enable"),
		)
		settingsSizer.Add(self._checkBox)
		self.bindHelpEvent("VisionSettings", self._checkBox)
		self._optionsSizer = wx.BoxSizer(orient=wx.VERTICAL)
		self._optionsSizer.AddSpacer(size=self.scaleSize(10))
		# Translators: Options label on a vision enhancement provider on the vision settings category panel
		self._optionsText = wx.StaticText(self, label=_("Options:"))
		self._optionsSizer.Add(self._optionsText)
		self._optionsSizer.Add(
			self._providerSettingsSizer,
			border=self.scaleSize(15),
			flag=wx.LEFT | wx.EXPAND,
			proportion=1,
		)
		settingsSizer.Add(
			self._optionsSizer,
			flag=wx.EXPAND,
			proportion=1,
		)
		self._checkBox.SetValue(bool(self._providerControl.getProviderInstance()))
		if self._createProviderSettings():
			self._checkBox.Bind(wx.EVT_CHECKBOX, self._enableToggle)
		else:
			self._checkBox.Bind(wx.EVT_CHECKBOX, self._nonEnableableGUI)
		self._updateOptionsVisibility()

	def _updateOptionsVisibility(self):
		hasProviderOptions = bool(self._providerSettings) and self._providerSettings.hasOptions
		if hasProviderOptions:
			self.settingsSizer.Show(self._optionsSizer, recursive=True)
		else:
			self.settingsSizer.Hide(self._optionsSizer, recursive=True)
		self._sendLayoutUpdatedEvent()

	def _createProviderSettings(self):
		try:
			getSettingsCallable = self._providerControl.getProviderInfo().providerClass.getSettings
			self._providerSettings = VisionProviderSubPanel_Settings(
				self,
				settingsCallable=getSettingsCallable,
			)
			self._providerSettingsSizer.Add(self._providerSettings, flag=wx.EXPAND, proportion=1)
		# Broad except used since we can not know what exceptions a provider might throw.
		# We should be able to continue despite a buggy provider.
		except Exception:
			log.error("unable to create provider settings", exc_info=True)
			return False
		return True

	def _nonEnableableGUI(self, evt):
		gui.messageBox(
			# Translators: Shown when there is an error showing the GUI for a vision enhancement provider
			_("Unable to configure user interface for Vision Enhancement Provider, it can not be enabled."),
			# Translators: The title of the error dialog displayed when there is an error showing the GUI
			# for a vision enhancement provider
			_("Error"),
			parent=self,
		)
		self._checkBox.SetValue(False)

	def _enableToggle(self, evt):
		shouldBeRunning = evt.IsChecked()
		if shouldBeRunning and not self._providerControl.startProvider():
			self._checkBox.SetValue(False)
			self._updateOptionsVisibility()
			return
		elif not shouldBeRunning and not self._providerControl.terminateProvider():
			# When there is an error on termination, don't leave the checkbox checked.
			# The provider should not be left configured to startup.
			self._checkBox.SetValue(False)
			self._updateOptionsVisibility()
			return
		# Able to successfully start / terminate:
		self._providerSettings.updateDriverSettings()
		self._providerSettings.refreshGui()
		self._updateOptionsVisibility()

	def onDiscard(self):
		if self._providerSettings:
			self._providerSettings.onDiscard()

	def onSave(self):
		log.debug("calling VisionProviderSubPanel_Wrapper")
		if self._providerSettings:
			self._providerSettings.onSave()


""" The name of the config profile currently being edited, if any.
This is set when the currently edited configuration profile is determined and returned to None when the dialog is destroyed.
This can be used by an AppModule for NVDA to identify and announce
changes in the name of the edited configuration profile when categories are changed"""
NvdaSettingsDialogActiveConfigProfile = None
NvdaSettingsDialogWindowHandle = None


class NVDASettingsDialog(MultiCategorySettingsDialog):
	# Translators: This is the label for the NVDA settings dialog.
	title = _("NVDA Settings")
	categoryClasses = [
		GeneralSettingsPanel,
		SpeechSettingsPanel,
		BrailleSettingsPanel,
		AudioPanel,
		VisionSettingsPanel,
		KeyboardSettingsPanel,
		MouseSettingsPanel,
		ReviewCursorPanel,
		InputCompositionPanel,
		ObjectPresentationPanel,
		BrowseModePanel,
		DocumentFormattingPanel,
		DocumentNavigationPanel,
		AddonStorePanel,
	]
	if touchHandler.touchSupported():
		categoryClasses.append(TouchInteractionPanel)
	if winVersion.isUwpOcrAvailable():
		categoryClasses.append(UwpOcrPanel)
	# And finally the Advanced panel which should always be last.
	if not globalVars.appArgs.secure:
		categoryClasses.append(AdvancedPanel)

	def makeSettings(self, settingsSizer):
		# Ensure that after the settings dialog is created the name is set correctly
		super(NVDASettingsDialog, self).makeSettings(settingsSizer)
		self._doOnCategoryChange()
		global NvdaSettingsDialogWindowHandle
		NvdaSettingsDialogWindowHandle = self.GetHandle()

	def _doOnCategoryChange(self):
		global NvdaSettingsDialogActiveConfigProfile
		NvdaSettingsDialogActiveConfigProfile = config.conf.profiles[-1].name
		if (
			not NvdaSettingsDialogActiveConfigProfile
			or isinstance(self.currentCategory, GeneralSettingsPanel)
			or isinstance(self.currentCategory, AddonStorePanel)
		):
			# Translators: The profile name for normal configuration
			NvdaSettingsDialogActiveConfigProfile = _("normal configuration")
		self.SetTitle(self._getDialogTitle())
		self.bindHelpEvent(
			self.currentCategory.helpId,
			self.catListCtrl,
		)

	def _getDialogTitle(self):
		return "{dialogTitle}: {panelTitle} ({configProfile})".format(
			dialogTitle=self.title,
			panelTitle=self.currentCategory.title,
			configProfile=NvdaSettingsDialogActiveConfigProfile,
		)

	def onCategoryChange(self, evt):
		super(NVDASettingsDialog, self).onCategoryChange(evt)
		if evt.Skipped:
			return
		self._doOnCategoryChange()

	def Destroy(self):
		global NvdaSettingsDialogActiveConfigProfile, NvdaSettingsDialogWindowHandle
		NvdaSettingsDialogActiveConfigProfile = None
		NvdaSettingsDialogWindowHandle = None
		super(NVDASettingsDialog, self).Destroy()


class AddSymbolDialog(
	gui.contextHelp.ContextHelpMixin,
	wx.Dialog,  # wxPython does not seem to call base class initializer, put last in MRO
):
	helpId = "SymbolPronunciation"

	def __init__(self, parent):
		# Translators: This is the label for the add symbol dialog.
		super().__init__(parent, title=_("Add Symbol"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		# Translators: This is the label for the edit field in the add symbol dialog.
		symbolText = _("&Symbol:")
		self.identifierTextCtrl = sHelper.addLabeledControl(symbolText, wx.TextCtrl)

		sHelper.addDialogDismissButtons(self.CreateButtonSizer(wx.OK | wx.CANCEL))

		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.identifierTextCtrl.SetFocus()
		self.CentreOnScreen()


class SpeechSymbolsDialog(SettingsDialog):
	helpId = "SymbolPronunciation"

	def __init__(self, parent):
		try:
			symbolProcessor = characterProcessing._localeSpeechSymbolProcessors.fetchLocaleData(
				speech.getCurrentLanguage(),
			)
		except LookupError:
			symbolProcessor = characterProcessing._localeSpeechSymbolProcessors.fetchLocaleData("en")
		self.symbolProcessor = symbolProcessor
		desc = languageHandler.getLanguageDescription(self.symbolProcessor.locale)
		if not desc:
			desc = self.symbolProcessor.locale
			# Raise an error in the hope that people be more likely to report the issue
			log.error(f"No description for language: {desc}. Using language code instead.")
		# Translators: This is the label for the symbol pronunciation dialog.
		# %s is replaced by the language for which symbol pronunciation is being edited.
		self.title = _("Symbol Pronunciation (%s)") % desc
		super(SpeechSymbolsDialog, self).__init__(
			parent,
			resizeable=True,
		)

	def makeSettings(self, settingsSizer):
		self.filteredSymbols = self.symbols = [
			copy.copy(symbol) for symbol in self.symbolProcessor.computedSymbols.values()
		]
		self.pendingRemovals = {}

		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: The label of a text field to search for symbols in the speech symbols dialog.
		filterText = pgettext("speechSymbols", "&Filter by:")
		self.filterEdit = sHelper.addLabeledControl(
			labelText=filterText,
			wxCtrlClass=wx.TextCtrl,
			size=(self.scaleSize(310), -1),
		)
		self.filterEdit.Bind(wx.EVT_TEXT, self.onFilterEditTextChange)

		# Translators: The label for symbols list in symbol pronunciation dialog.
		symbolsText = _("&Symbols")
		self.symbolsList = sHelper.addLabeledControl(
			symbolsText,
			nvdaControls.AutoWidthColumnListCtrl,
			autoSizeColumn=2,  # The replacement column is likely to need the most space
			itemTextCallable=self.getItemTextForList,
			style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VIRTUAL,
		)

		# Translators: The label for a column in symbols list used to identify a symbol.
		self.symbolsList.AppendColumn(_("Symbol"), width=self.scaleSize(150))
		# Translators: The label for a column in symbols list used to identify a replacement.
		self.symbolsList.AppendColumn(_("Replacement"))
		# Translators: The label for a column in symbols list used to identify a symbol's speech level (either none, some, most, all or character).
		self.symbolsList.AppendColumn(_("Level"))
		# Translators: The label for a column in symbols list which specifies when the actual symbol will be sent to the synthesizer (preserved).
		# See the "Punctuation/Symbol Pronunciation" section of the User Guide for details.
		self.symbolsList.AppendColumn(_("Preserve"))
		self.symbolsList.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onListItemFocused)

		# Translators: The label for the group of controls in symbol pronunciation dialog to change the pronunciation of a symbol.
		changeSymbolText = _("Change selected symbol")
		changeSymbolSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=changeSymbolText)
		changeSymbolGroup = guiHelper.BoxSizerHelper(self, sizer=changeSymbolSizer)
		changeSymbolHelper = sHelper.addItem(changeSymbolGroup)

		# Used to ensure that event handlers call Skip(). Not calling skip can cause focus problems for controls. More
		# generally the advice on the wx documentation is: "In general, it is recommended to skip all non-command events
		# to allow the default handling to take place. The command events are, however, normally not skipped as usually
		# a single command such as a button click or menu item selection must only be processed by one handler."
		def skipEventAndCall(handler):
			def wrapWithEventSkip(event):
				if event:
					event.Skip()
				return handler()

			return wrapWithEventSkip

		# Translators: The label for the edit field in symbol pronunciation dialog to change the replacement text of a symbol.
		replacementText = _("&Replacement")
		self.replacementEdit = changeSymbolHelper.addLabeledControl(
			labelText=replacementText,
			wxCtrlClass=wx.TextCtrl,
			size=(self.scaleSize(300), -1),
		)
		self.replacementEdit.Bind(wx.EVT_TEXT, skipEventAndCall(self.onSymbolEdited))

		# Translators: The label for the combo box in symbol pronunciation dialog to change the speech level of a symbol.
		levelText = _("&Level")
		symbolLevelLabels = characterProcessing.SPEECH_SYMBOL_LEVEL_LABELS
		levelChoices = [symbolLevelLabels[level] for level in characterProcessing.SPEECH_SYMBOL_LEVELS]
		self.levelList = changeSymbolHelper.addLabeledControl(levelText, wx.Choice, choices=levelChoices)
		self.levelList.Bind(wx.EVT_CHOICE, skipEventAndCall(self.onSymbolEdited))

		# Translators: The label for the combo box in symbol pronunciation dialog to change when a symbol is sent to the synthesizer.
		preserveText = _("&Send actual symbol to synthesizer")
		symbolPreserveLabels = characterProcessing.SPEECH_SYMBOL_PRESERVE_LABELS
		preserveChoices = [symbolPreserveLabels[mode] for mode in characterProcessing.SPEECH_SYMBOL_PRESERVES]
		self.preserveList = changeSymbolHelper.addLabeledControl(
			preserveText,
			wx.Choice,
			choices=preserveChoices,
		)
		self.preserveList.Bind(wx.EVT_CHOICE, skipEventAndCall(self.onSymbolEdited))

		bHelper = sHelper.addItem(guiHelper.ButtonHelper(orientation=wx.HORIZONTAL))
		# Translators: The label for a button in the Symbol Pronunciation dialog to add a new symbol.
		addButton = bHelper.addButton(self, label=_("&Add"))

		# Translators: The label for a button in the Symbol Pronunciation dialog to remove a symbol.
		self.removeButton = bHelper.addButton(self, label=_("Re&move"))
		self.removeButton.Disable()

		addButton.Bind(wx.EVT_BUTTON, self.OnAddClick)
		self.removeButton.Bind(wx.EVT_BUTTON, self.OnRemoveClick)

		# Populate the unfiltered list with symbols.
		self.filter()

	def postInit(self):
		self.symbolsList.SetFocus()

	def filter(self, filterText=""):
		NONE_SELECTED = -1
		previousSelectionValue = None
		previousIndex = self.symbolsList.GetFirstSelected()  # may return NONE_SELECTED
		if previousIndex != NONE_SELECTED:
			previousSelectionValue = self.filteredSymbols[previousIndex]

		if not filterText:
			self.filteredSymbols = self.symbols
		else:
			# Do case-insensitive matching by lowering both filterText and each symbols's text.
			filterText = filterText.lower()
			self.filteredSymbols = [
				symbol
				for symbol in self.symbols
				if filterText in symbol.displayName.lower() or filterText in symbol.replacement.lower()
			]
		self.symbolsList.ItemCount = len(self.filteredSymbols)

		# sometimes filtering may result in an empty list.
		if not self.symbolsList.ItemCount:
			self.editingItem = None
			# disable the "change symbol" controls, since there are no items in the list.
			self.replacementEdit.Disable()
			self.levelList.Disable()
			self.preserveList.Disable()
			self.removeButton.Disable()
			return  # exit early, no need to select an item.

		# If there was a selection before filtering, try to preserve it
		newIndex = 0  # select first item by default.
		if previousSelectionValue:
			try:
				newIndex = self.filteredSymbols.index(previousSelectionValue)
			except ValueError:
				pass

		# Change the selection
		self.symbolsList.Select(newIndex)
		self.symbolsList.Focus(newIndex)
		# We don't get a new focus event with the new index.
		self.symbolsList.sendListItemFocusedEvent(newIndex)

	def getItemTextForList(self, item, column):
		symbol = self.filteredSymbols[item]
		if column == 0:
			return symbol.displayName
		elif column == 1:
			return symbol.replacement
		elif column == 2:
			return characterProcessing.SPEECH_SYMBOL_LEVEL_LABELS[symbol.level]
		elif column == 3:
			return characterProcessing.SPEECH_SYMBOL_PRESERVE_LABELS[symbol.preserve]
		else:
			raise ValueError("Unknown column: %d" % column)

	def onSymbolEdited(self):
		if self.editingItem is not None:
			# Update the symbol the user was just editing.
			item = self.editingItem
			symbol = self.filteredSymbols[item]
			symbol.replacement = self.replacementEdit.Value
			symbol.level = characterProcessing.SPEECH_SYMBOL_LEVELS[self.levelList.Selection]
			symbol.preserve = characterProcessing.SPEECH_SYMBOL_PRESERVES[self.preserveList.Selection]

	def onListItemFocused(self, evt):
		# Update the editing controls to reflect the newly selected symbol.
		item = evt.GetIndex()
		symbol = self.filteredSymbols[item]
		self.editingItem = item
		# ChangeValue and Selection property used because they do not cause EVNT_CHANGED to be fired.
		self.replacementEdit.ChangeValue(symbol.replacement)
		self.levelList.Selection = characterProcessing.SPEECH_SYMBOL_LEVELS.index(symbol.level)
		self.preserveList.Selection = characterProcessing.SPEECH_SYMBOL_PRESERVES.index(symbol.preserve)
		self.removeButton.Enabled = not self.symbolProcessor.isBuiltin(symbol.identifier)
		self.replacementEdit.Enable()
		self.levelList.Enable()
		self.preserveList.Enable()
		evt.Skip()

	def OnAddClick(self, evt):
		with AddSymbolDialog(self) as entryDialog:
			if entryDialog.ShowModal() != wx.ID_OK:
				return
			identifier = entryDialog.identifierTextCtrl.GetValue()
			if not identifier:
				return
		# Clean the filter, so we can select the new entry.
		self.filterEdit.Value = ""
		self.filter()
		for index, symbol in enumerate(self.symbols):
			if identifier == symbol.identifier:
				gui.messageBox(
					# Translators: An error reported in the Symbol Pronunciation dialog
					# when adding a symbol that is already present.
					_('Symbol "%s" is already present.') % identifier,
					# Translators: title of an error message
					_("Error"),
					wx.OK | wx.ICON_ERROR,
				)
				self.symbolsList.Select(index)
				self.symbolsList.Focus(index)
				self.symbolsList.SetFocus()
				return
		addedSymbol = characterProcessing.SpeechSymbol(identifier)
		try:
			del self.pendingRemovals[identifier]
		except KeyError:
			pass
		addedSymbol.displayName = identifier
		addedSymbol.replacement = ""
		addedSymbol.level = characterProcessing.SymbolLevel.ALL
		addedSymbol.preserve = characterProcessing.SYMPRES_NEVER
		self.symbols.append(addedSymbol)
		self.symbolsList.ItemCount = len(self.symbols)
		index = self.symbolsList.ItemCount - 1
		self.symbolsList.Select(index)
		self.symbolsList.Focus(index)
		# We don't get a new focus event with the new index.
		self.symbolsList.sendListItemFocusedEvent(index)
		self.symbolsList.SetFocus()

	def OnRemoveClick(self, evt):
		index = self.symbolsList.GetFirstSelected()
		symbol = self.filteredSymbols[index]
		self.pendingRemovals[symbol.identifier] = symbol
		del self.filteredSymbols[index]
		if self.filteredSymbols is not self.symbols:
			self.symbols.remove(symbol)
		self.symbolsList.ItemCount = len(self.filteredSymbols)
		# sometimes removing may result in an empty list.
		if not self.symbolsList.ItemCount:
			self.editingItem = None
			# disable the "change symbol" controls, since there are no items in the list.
			self.replacementEdit.Disable()
			self.levelList.Disable()
			self.preserveList.Disable()
			self.removeButton.Disable()
		else:
			index = min(index, self.symbolsList.ItemCount - 1)
			self.symbolsList.Select(index)
			self.symbolsList.Focus(index)
			# We don't get a new focus event with the new index.
			self.symbolsList.sendListItemFocusedEvent(index)
		self.symbolsList.SetFocus()

	def onOk(self, evt):
		self.onSymbolEdited()
		self.editingItem = None
		for symbol in self.pendingRemovals.values():
			self.symbolProcessor.deleteSymbol(symbol)
		for symbol in self.symbols:
			if not symbol.replacement:
				continue
			self.symbolProcessor.updateSymbol(symbol)
		try:
			self.symbolProcessor.userSymbols.save()
		except IOError as e:
			log.error("Error saving user symbols info: %s" % e)
		characterProcessing._localeSpeechSymbolProcessors.invalidateLocaleData(self.symbolProcessor.locale)
		super(SpeechSymbolsDialog, self).onOk(evt)

	def _refreshVisibleItems(self):
		count = self.symbolsList.GetCountPerPage()
		first = self.symbolsList.GetTopItem()
		self.symbolsList.RefreshItems(first, first + count)

	def onFilterEditTextChange(self, evt):
		self.filter(self.filterEdit.Value)
		self._refreshVisibleItems()
		evt.Skip()
