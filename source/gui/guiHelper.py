# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2016-2025 NV Access Limited, Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


"""Utilities to simplify the creation of wx GUIs, including automatic management of spacing.
Example usage:

class myDialog(wx.Dialog):

	def __init__(self, parent):
		super().__init__(parent, title='Usage example of guiHelper')

		mainSizer = wx.BoxSizer(wx.VERTICAL)

		sHelper = guiHelper.BoxSizerHelper(self, wx.VERTICAL)

		# Adding controls with their associated label
		# according on the control type, they are associated horizontally or vertically.
		filterElement = sHelper.addLabeledControl("Filter:", wx.TextCtrl)
		symbols = sHelper.addLabeledControl("Select a row:", wx.ListCtrl)

		# A control with its associated label
		choice = sHelper.addLabeledControl("Choose option", wx.Choice, choices=["1", "2", "3"])

		# A single button
		button = sHelper.addItem(wx.Button(self, label="Does stuff"))

		# for general items
		checkbox = sHelper.addItem(wx.CheckBox(self, label="always do something"))

		# for groups of buttons
		buttonGroup = gui.guiHelper.ButtonHelper(wx.VERTICAL)
		oneButton = buttonGroup.addButton(self, label="one")
		twoButton = buttonGroup.addButton(self, label="two")
		threeButton = buttonGroup.addButton(self, label="three")
		sHelper.addItem(buttonGroup)

		mainSizer.Add(sHelper.sizer, border=10, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
	...
"""

from collections.abc import Callable
from contextlib import contextmanager
from functools import wraps
import sys
import threading
import weakref
from typing import (
	Any,
	Generic,
	Optional,
	ParamSpec,
	Type,
	TypeVar,
	Union,
	cast,
	overload,
)

import wx
from wx.lib import scrolledpanel, newevent
from abc import ABCMeta

#: border space to be used around all controls in dialogs
BORDER_FOR_DIALOGS = 10

#: when dialog items are laid out vertically use this much space between them
SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS = 10

#: put this much space between buttons  next to each other horizontally.
SPACE_BETWEEN_BUTTONS_HORIZONTAL = 7

#: put this much space between buttons next to each other vertically
SPACE_BETWEEN_BUTTONS_VERTICAL = 5

#: put this much space between two horizontally associated elements (such as a wx.StaticText and a wx.Choice or wx.TextCtrl)
SPACE_BETWEEN_ASSOCIATED_CONTROL_HORIZONTAL = 10

#: put this much space between two vertically associated elements (such as a wx.StaticText and a wx.Choice or wx.TextCtrl)
SPACE_BETWEEN_ASSOCIATED_CONTROL_VERTICAL = 3


@contextmanager
def autoThaw(control: wx.Window):
	control.Freeze()
	yield
	control.Thaw()


class ButtonHelper(object):
	"""Class used to ensure that the appropriate space is added between each button, whether in horizontal or vertical
	arrangement. This class should be used for groups of buttons. While it won't cause problems to use this class with a
	single button there is little benefit. Individual buttons can be added directly to a sizer / sizer helper.
	"""

	def __init__(self, orientation):
		"""
		@param orientation: the orientation for the buttons, either wx.HORIZONTAL or wx.VERTICAL
		"""
		object.__init__(self)
		self._firstButton = True
		self._sizer = wx.BoxSizer(orientation)
		self._space = (
			SPACE_BETWEEN_BUTTONS_HORIZONTAL
			if orientation is wx.HORIZONTAL
			else SPACE_BETWEEN_BUTTONS_VERTICAL
		)

	@property
	def sizer(self):
		"""Useful if you wish to add this group of buttons to another sizer and provide other arguments"""
		return self._sizer

	def addButton(self, *args, **kwargs):
		"""add another button to the group. Space between the buttons is added automatically.
		usage hint:
			parent = self # a wx window class. EG wx.Dialog
			myButtonHelper.addButton(dialog, label=_("my new button"))
		@param args: The formal arguments to pass directly to wx.Button. The only required parameter is 'parent'.
		@param kwargs: The keyword args passed directly to wx.Button
		"""
		wxButton = wx.Button(*args, **kwargs)
		if not self._firstButton:
			self._sizer.AddSpacer(self._space)
		self._sizer.Add(wxButton)
		self._firstButton = False
		return wxButton


# vertical controls where the label should go above visually, and the control should go below
_VerticalCtrlT = TypeVar("_VerticalCtrlT", wx.ListCtrl, wx.ListBox, wx.TreeCtrl)
# horizontal controls where the label should go first visually, and the control should go after
_HorizontalCtrlT = TypeVar(
	"_HorizontalCtrlT",
	wx.Button,
	wx.Choice,
	wx.ComboBox,
	wx.Slider,
	wx.SpinCtrl,
	wx.TextCtrl,
)


@overload
def associateElements(firstElement: wx.StaticText, secondElement: _HorizontalCtrlT) -> wx.BoxSizer: ...
@overload
def associateElements(firstElement: wx.StaticText, secondElement: wx.CheckBox) -> wx.BoxSizer: ...
@overload
def associateElements(firstElement: wx.StaticText, secondElement: _VerticalCtrlT) -> wx.BoxSizer: ...
@overload
def associateElements(firstElement: wx.Button, secondElement: wx.CheckBox) -> wx.BoxSizer: ...
@overload
def associateElements(firstElement: wx.TextCtrl, secondElement: wx.Button) -> wx.BoxSizer: ...


def associateElements(firstElement, secondElement) -> wx.BoxSizer:
	"""Associates two GUI elements together. Handles choosing a layout and appropriate spacing. Abstracts away common
	pairings used in the NVDA GUI.
	Currently handles:
		wx.StaticText and :const:`_HorizontalCtrlT` - Horizontal layout
		wx.StaticText and wx.CheckBox - Horizontal layout, control first, label second
		wx.StaticText and :const:`_VerticalCtrlT` - Vertical layout
		wx.Button and wx.CheckBox - Horizontal layout
		wx.TextCtrl and wx.Button - Horizontal layout
	"""
	if isinstance(firstElement, ButtonHelper) or isinstance(secondElement, ButtonHelper):
		raise NotImplementedError("AssociateElements has no implementation for ButtonHelper elements")
	if isinstance(firstElement, LabeledControlHelper) or isinstance(secondElement, LabeledControlHelper):
		raise NotImplementedError("AssociateElements as no implementation for LabeledControlHelper elements")

	# staticText and input control
	# likely a labelled control from LabeledControlHelper
	if isinstance(firstElement, wx.StaticText):
		# Horizontal layout, label first, control second
		if isinstance(secondElement, _HorizontalCtrlT.__constraints__):
			sizer = wx.BoxSizer(wx.HORIZONTAL)
			sizer.Add(firstElement, flag=wx.ALIGN_CENTER_VERTICAL)
			sizer.AddSpacer(SPACE_BETWEEN_ASSOCIATED_CONTROL_HORIZONTAL)
			sizer.Add(secondElement)
		# Horizontal layout, control first, label second
		elif isinstance(secondElement, wx.CheckBox):
			sizer = wx.BoxSizer(wx.HORIZONTAL)
			sizer.Add(secondElement)
			sizer.AddSpacer(SPACE_BETWEEN_ASSOCIATED_CONTROL_HORIZONTAL)
			sizer.Add(firstElement, flag=wx.ALIGN_CENTER_VERTICAL)
		# Vertical layout, label above, control below
		elif isinstance(secondElement, _VerticalCtrlT.__constraints__):
			sizer = wx.BoxSizer(wx.VERTICAL)
			sizer.Add(firstElement)
			sizer.AddSpacer(SPACE_BETWEEN_ASSOCIATED_CONTROL_VERTICAL)
			sizer.Add(secondElement, flag=wx.EXPAND, proportion=1)
	# button and checkBox
	elif isinstance(firstElement, wx.Button) and isinstance(secondElement, wx.CheckBox):
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(firstElement)
		sizer.AddSpacer(SPACE_BETWEEN_ASSOCIATED_CONTROL_HORIZONTAL)
		sizer.Add(secondElement, flag=wx.ALIGN_CENTER_VERTICAL)
	# textCtrl and button
	elif isinstance(firstElement, wx.TextCtrl) and isinstance(secondElement, wx.Button):
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(firstElement, flag=wx.ALIGN_CENTER_VERTICAL, proportion=1)
		sizer.AddSpacer(SPACE_BETWEEN_BUTTONS_HORIZONTAL)
		sizer.Add(secondElement, flag=wx.ALIGN_CENTER_VERTICAL)
	else:
		raise NotImplementedError(
			"The firstElement and secondElement argument combination has no implementation",
		)

	return sizer


_LabeledControlT = TypeVar("_LabeledControlT", bound=wx.Control)


class LabeledControlHelper(Generic[_LabeledControlT]):
	"""Represents a Labeled Control. Provides a class to create and hold on to the objects and automatically associate
	the two controls together.
	Relies on guiHelper.associateElements(), any limitations in guiHelper.associateElements() also apply here.
	"""

	# When the control is enabled / disabled this event is raised.
	# A handler is automatically added to the control to ensure the label is also enabled/disabled.
	EnableChanged, EVT_ENABLE_CHANGED = newevent.NewEvent()

	# When the control is shown / hidden this event is raised.
	# A handler is automatically added to the control to ensure the label is also shown / hidden.
	ShowChanged, EVT_SHOW_CHANGED = newevent.NewEvent()

	def __init__(self, parent: wx.Window, labelText: str, wxCtrlClass: Type[_LabeledControlT], **kwargs):
		"""@param parent: An instance of the parent wx window. EG wx.Dialog
		@param labelText: The text to associate with a wx control.
		@param wxCtrlClass: The class to associate with the label, eg: wx.TextCtrl
		@param kwargs: The keyword arguments used to instantiate the wxCtrlClass
		"""

		class LabelEnableChangedListener(wx.StaticText):
			isDestroyed = False
			isListening = False

			def _onDestroy(self, evt: wx.WindowDestroyEvent):
				self.isDestroyed = True

			def listenForEnableChanged(self, _ctrl: _LabeledControlT):
				self.Bind(wx.EVT_WINDOW_DESTROY, self._onDestroy)
				self._labelText = self.GetLabelText()
				_ctrl.Bind(LabeledControlHelper.EVT_ENABLE_CHANGED, self._onEnableChanged)
				_ctrl.Bind(LabeledControlHelper.EVT_SHOW_CHANGED, self._onShowChanged)
				self.isListening = True

			def _onEnableChanged(self, evt: wx.Event):
				if self.isListening and not self.isDestroyed:
					self.Enable(evt.isEnabled)

			def _onShowChanged(self, evt: wx.Event):
				if self.isListening and not self.isDestroyed:
					if evt.shouldShow:
						self.SetLabelText(self._labelText)
					else:
						self.SetLabelText("")
					self.Parent.Layout()

		class WxCtrlWithEnableEvnt(wxCtrlClass):
			def Enable(self, enable=True):
				evt = LabeledControlHelper.EnableChanged(isEnabled=enable)
				wx.PostEvent(self, evt)
				super().Enable(enable)

			def Disable(self):
				evt = LabeledControlHelper.EnableChanged(isEnabled=False)
				wx.PostEvent(self, evt)
				super().Disable()

			def Show(self, show: bool = True):
				evt = LabeledControlHelper.ShowChanged(shouldShow=show)
				wx.PostEvent(self, evt)
				super().Show(show)

			def Hide(self):
				evt = LabeledControlHelper.ShowChanged(shouldShow=False)
				wx.PostEvent(self, evt)
				super().Hide()

		self._label = LabelEnableChangedListener(parent, label=labelText)
		self._ctrl = cast(_LabeledControlT, WxCtrlWithEnableEvnt(parent, **kwargs))
		self._label.listenForEnableChanged(self._ctrl)
		self._sizer = associateElements(self._label, self._ctrl)

	@property
	def control(self) -> _LabeledControlT:
		return self._ctrl

	@property
	def sizer(self) -> wx.BoxSizer:
		return self._sizer


class PathSelectionHelper(object):
	"""
	Abstracts away details for creating a path selection helper. The path selection helper is a textCtrl with a
	button in horizontal layout. The Button launches a directory explorer. To get the path selected by the user, use the
	`pathControl` property which exposes a wx.TextCtrl.
	"""

	def __init__(self, parent, buttonText, browseForDirectoryTitle):
		"""@param parent: An instance of the parent wx window. EG wx.Dialog
		@param buttonText: The text for the button to launch a directory dialog (wx.DirDialog). This is typically 'Browse'
		@type buttonText: string
		@param browseForDirectoryTitle: The text for the title of the directory dialog (wx.DirDialog)
		@type browseForDirectoryTitle: string
		"""
		object.__init__(self)
		self._textCtrl = wx.TextCtrl(parent)
		self._browseButton = wx.Button(parent, label=buttonText)
		self._browseForDirectoryTitle = browseForDirectoryTitle
		self._browseButton.Bind(wx.EVT_BUTTON, self.onBrowseForDirectory)
		self._sizer = associateElements(self._textCtrl, self._browseButton)
		self._parent = parent

	@property
	def pathControl(self):
		return self._textCtrl

	@property
	def sizer(self):
		return self._sizer

	def getDefaultBrowseForDirectoryPath(self):
		return self._textCtrl.Value or "c:\\"

	def onBrowseForDirectory(self, evt):
		startPath = self.getDefaultBrowseForDirectoryPath()
		with wx.DirDialog(self._parent, self._browseForDirectoryTitle, defaultPath=startPath) as d:
			if d.ShowModal() == wx.ID_OK:
				self._textCtrl.Value = d.Path


class BoxSizerHelper:
	"""Used to abstract away spacing logic for a wx.BoxSizer"""

	def __init__(
		self,
		parent: wx.Dialog,
		orientation: Optional[int] = None,
		sizer: Optional[Union[wx.BoxSizer, wx.StaticBoxSizer]] = None,
	):
		"""Init. Pass in either orientation OR sizer.
		@param parent: An instance of the parent wx window. EG wx.Dialog
		@param orientation: the orientation to use when constructing the sizer, either wx.HORIZONTAL or wx.VERTICAL
		@type orientation: wx.HORIZONTAL or wx.VERTICAL
		@param sizer: the sizer to use rather than constructing one.
		"""
		self._parentRef = weakref.ref(parent)
		self.hasFirstItemBeenAdded = False
		if orientation and sizer:
			raise ValueError("Supply either orientation OR sizer. Not both.")
		if orientation and orientation in (wx.VERTICAL, wx.HORIZONTAL):
			self.sizer = wx.BoxSizer(orientation)
		elif sizer and isinstance(sizer, wx.BoxSizer):
			self.sizer = sizer
		else:
			raise ValueError("Orientation OR Sizer must be supplied.")
		self.dialogDismissButtonsAdded = False

	_ItemT = TypeVar("_ItemT")

	def addItem(self, item: "_ItemT", **keywordArgs) -> "_ItemT":
		"""Adds an item with space between it and the previous item.
		Does not handle adding LabledControlHelper; use L{addLabeledControl} instead.
		@param item: the item to add to the sizer
		@param **keywordArgs: the extra args to pass when adding the item to the wx.Sizer. This parameter is
			normally not necessary.
		"""
		assert not self.dialogDismissButtonsAdded, (
			"Buttons to dismiss the dialog already added, they should be the last item added."
		)

		toAdd = item
		shouldAddSpacer = self.hasFirstItemBeenAdded

		if isinstance(item, ButtonHelper):
			toAdd = item.sizer
			buttonBorderAmount = 5
			keywordArgs["border"] = buttonBorderAmount
			keywordArgs["flag"] = keywordArgs.get("flag", 0) | wx.ALL
			shouldAddSpacer = False  # no need to add a spacer, since the button border has been added.
		elif isinstance(item, BoxSizerHelper):
			toAdd = item.sizer
		elif isinstance(item, PathSelectionHelper):
			toAdd = item.sizer
			if self.sizer.GetOrientation() == wx.VERTICAL:
				keywordArgs["flag"] = keywordArgs.get("flag", 0) | wx.EXPAND
			else:
				raise NotImplementedError(
					"Adding PathSelectionHelper to a horizontal BoxSizerHelper is not implemented",
				)
		elif isinstance(item, wx.CheckBox):
			if self.sizer.GetOrientation() == wx.HORIZONTAL:
				keywordArgs["flag"] = keywordArgs.get("flag", 0) | wx.EXPAND
		elif isinstance(item, LabeledControlHelper):
			raise NotImplementedError("Use addLabeledControl instead")

		# a boxSizerHelper could contain a wx.StaticBoxSizer
		if isinstance(toAdd, (wx.StaticBoxSizer, scrolledpanel.ScrolledPanel)):
			keywordArgs["flag"] = keywordArgs.get("flag", 0) | wx.EXPAND

		if shouldAddSpacer:
			self.sizer.AddSpacer(SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		self.sizer.Add(toAdd, **keywordArgs)
		self.hasFirstItemBeenAdded = True
		return item

	def addLabeledControl(
		self,
		labelText: str,
		wxCtrlClass: Type[_LabeledControlT],
		**kwargs,
	) -> _LabeledControlT:
		"""Convenience method to create a labeled control
		@param labelText: Text to use when constructing the wx.StaticText to label the control.
		@param wxCtrlClass: Control class to construct and associate with the label
		@param kwargs: keyword arguments used to construct the wxCtrlClass. As taken by guiHelper.LabeledControlHelper

		Relies on guiHelper.LabeledControlHelper and thus guiHelper.associateElements, and therefore inherits any
		limitations from there.
		"""
		parent = self._parentRef()
		if isinstance(self.sizer, wx.StaticBoxSizer):
			parent = self.sizer.GetStaticBox()
		labeledControl = LabeledControlHelper(parent, labelText, wxCtrlClass, **kwargs)
		if isinstance(labeledControl.control, (wx.ListCtrl, wx.ListBox, wx.TreeCtrl)):
			self.addItem(labeledControl.sizer, flag=wx.EXPAND, proportion=1)
		else:
			self.addItem(labeledControl.sizer)
		return labeledControl.control

	_ButtonsT = TypeVar("_ButtonsT", wx.Sizer, ButtonHelper, wx.Button, int)

	def addDialogDismissButtons(
		self,
		buttons: "_ButtonsT",
		separated: bool = False,
	) -> "_ButtonsT":
		"""Adds and aligns the buttons for dismissing the dialog; e.g. "ok | cancel". These buttons are expected
		to be the last items added to the dialog. Buttons that launch an action, do not dismiss the dialog, or are not
		the last item should be added via L{addItem}
		@param buttons: The buttons to add
		@type buttons:
		  wx.Sizer or guiHelper.ButtonHelper or single wx.Button
		  or a bit list of the following flags: wx.OK, wx.CANCEL, wx.YES, wx.NO, wx.APPLY, wx.CLOSE,
		  wx.HELP, wx.NO_DEFAULT
		@param separated:
		  Whether a separator should be added between the dialog content and its footer.
		  Should be set to L{False} for message or single input dialogs, L{True} otherwise.
		"""
		if self.sizer.GetOrientation() != wx.VERTICAL:
			raise NotImplementedError(
				"Adding dialog dismiss buttons to a horizontal BoxSizerHelper is not implemented.",
			)
		if isinstance(buttons, ButtonHelper):
			toAdd = buttons.sizer
		elif isinstance(buttons, (wx.Sizer, wx.Button)):
			toAdd = buttons
		elif isinstance(buttons, int):
			toAdd = self._parentRef().CreateButtonSizer(buttons)
		else:
			raise NotImplementedError("Unknown type: {}".format(buttons))
		if separated:
			parentBox = self._parentRef()
			if isinstance(self.sizer, wx.StaticBoxSizer):
				parentBox = self.sizer.GetStaticBox()
			self.addItem(wx.StaticLine(parentBox), flag=wx.EXPAND)
		self.addItem(toAdd, flag=wx.ALIGN_RIGHT)
		self.dialogDismissButtonsAdded = True
		return buttons


class SIPABCMeta(wx.siplib.wrappertype, ABCMeta):
	"""Meta class to be used for wx subclasses with abstract methods."""

	pass


# TODO: Rewrite to use type parameter lists when upgrading to python 3.12 or later.
_WxCallOnMain_P = ParamSpec("_WxCallOnMain_P")
_WxCallOnMain_T = TypeVar("_WxCallOnMain_T")


def wxCallOnMain(
	function: Callable[_WxCallOnMain_P, _WxCallOnMain_T],
	*args: _WxCallOnMain_P.args,
	**kwargs: _WxCallOnMain_P.kwargs,
) -> _WxCallOnMain_T:
	"""Call a non-thread-safe wx function in a thread-safe way.
	Blocks current thread.

	Using this function is preferable over calling :fun:`wx.CallAfter` directly when you care about the return time or return value of the function.

	This function blocks the thread on which it is called.

	:param function: Callable to call on the main GUI thread.
		If this thread is the GUI thread, the function will be called immediately.
		Otherwise, it will be scheduled to be called on the GUI thread.
		In either case, the current thread will be blocked until it returns.
	:raises Exception: If `function` raises an exception, it is transparently re-raised so it can be handled on the calling thread.
	:return: Return value from calling `function` with the given positional and keyword arguments.
	"""
	result: Any = None
	exception: BaseException | None = None
	event = threading.Event()

	def functionWrapper():
		nonlocal result, exception
		try:
			result = function(*args, **kwargs)
		except Exception:
			exception = sys.exception()
		event.set()

	if wx.IsMainThread():
		functionWrapper()
	else:
		wx.CallAfter(functionWrapper)
		event.wait()

	if exception is not None:
		raise exception
	else:
		return result


# TODO: Rewrite to use type parameter lists when upgrading to python 3.12 or later.
_AlwaysCallAfterP = ParamSpec("_AlwaysCallAfterP")


def alwaysCallAfter(func: Callable[_AlwaysCallAfterP, Any]) -> Callable[_AlwaysCallAfterP, None]:
	"""Makes GUI updates thread-safe by running in the main thread.

	Example:
		@alwaysCallAfter
		def updateLabel(text):
			label.SetLabel(text)  # Safe GUI update from any thread

	.. note::
		The value returned by the decorated function will be discarded.
	"""

	@wraps(func)
	def wrapper(*args: _AlwaysCallAfterP.args, **kwargs: _AlwaysCallAfterP.kwargs) -> None:
		wx.CallAfter(func, *args, **kwargs)

	return wrapper
