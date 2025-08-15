# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Mesar Hameed, Joseph Lee,
# Thomas Stivers, Babbage B.V., Accessolutions, Julien Cochuyt
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from dataclasses import dataclass
import threading
import time
import warnings
import winsound
from collections import deque
from collections.abc import Callable, Collection
from enum import Enum, IntEnum, auto
from functools import partialmethod, singledispatchmethod, wraps
from typing import Any, Literal, NamedTuple, Optional, Self

import core
import extensionPoints
import wx
from .contextHelp import ContextHelpMixin
from logHandler import log

import gui

from . import guiHelper
from .dpiScalingHelper import DpiScalingHelperMixinWithoutInit
from .guiHelper import SIPABCMeta, wxCallOnMain

_messageBoxCounterLock = threading.Lock()
_messageBoxCounter = 0


def isModalMessageBoxActive() -> bool:
	"""
	`gui.message.messageBox` is a function which blocks the calling thread,
	until a user responds to the modal dialog.
	When some action (e.g. quitting NVDA) should be prevented due to any active modal message box,
	even if unrelated, use `isModalMessageBoxActive` to check before triggering the action.
	NVDA is in an uncertain state while waiting for an answer from a `gui.message.messageBox`.

	It's possible for multiple message boxes to be open at a time.
	This function can be used to check before opening subsequent `gui.message.messageBox` instances.

	Because an answer is required to continue after a modal messageBox is opened,
	some actions such as shutting down are prevented while NVDA is in a possibly uncertain state.

	@return: True if a thread blocking modal response is still pending.
	"""
	with _messageBoxCounterLock:
		return _messageBoxCounter != 0


def _countAsMessageBox():
	"""Wrapper to increment and decrement the message box counter around the wrapped function."""

	def _wrap(func):
		@wraps(func)
		def funcWrapper(*args, **kwargs):
			global _messageBoxCounter
			with _messageBoxCounterLock:
				_messageBoxCounter += 1
			try:
				return func(*args, **kwargs)
			except Exception:
				raise
			finally:
				with _messageBoxCounterLock:
					_messageBoxCounter -= 1

		return funcWrapper

	return _wrap


@_countAsMessageBox()
def displayDialogAsModal(dialog: wx.Dialog) -> int:
	"""Display a dialog as modal.
	@return: Same as for wx.MessageBox.

	`displayDialogAsModal` is a function which blocks the calling thread,
	until a user responds to the modal dialog.
	This function should be used when an answer is required before proceeding.

	It's possible for multiple message boxes to be open at a time.
	Before opening a new messageBox, use `isModalMessageBoxActive`
	to check if another messageBox modal response is still pending.

	Because an answer is required to continue after a modal messageBox is opened,
	some actions such as shutting down are prevented while NVDA is in a possibly uncertain state.
	"""
	try:
		if not dialog.GetParent():
			gui.mainFrame.prePopup()
		res = dialog.ShowModal()
	finally:
		if not dialog.GetParent():
			gui.mainFrame.postPopup()

	return res


def messageBox(
	message: str,
	caption: str = wx.MessageBoxCaptionStr,
	style: int = wx.OK | wx.CENTER,
	parent: Optional[wx.Window] = None,
) -> int:
	"""Display a modal message dialog.

	.. warning:: This function is deprecated.
		Use :class:`MessageDialog` instead.

	This function blocks the calling thread until the user responds to the modal dialog.
	This function should be used when an answer is required before proceeding.
	Consider using :class:`MessageDialog` or a custom :class:`wx.Dialog` subclass if an answer is not required, or a default answer can be provided.

	It's possible for multiple message boxes to be open at a time.
	Before opening a new messageBox, use :func:`isModalMessageBoxActive` to check if another messageBox modal response is still pending.

	Because an answer is required to continue after a modal messageBox is opened, some actions such as shutting down are prevented while NVDA is in a possibly uncertain state.

	:param message: The message text.
	:param caption: The caption (title) of the dialog.
	:param style: Same as for :func:`wx.MessageBox`, defaults to wx.OK | wx.CENTER.
	:param parent: The parent window, defaults to None.
	:return: Same as for :func:`wx.MessageBox`.
	"""
	warnings.warn(
		"gui.message.messageBox is deprecated. Use gui.message.MessageDialog instead.",
		DeprecationWarning,
	)
	if not core._hasShutdownBeenTriggered:
		res = wxCallOnMain(_messageBoxShim, message, caption, style, parent=parent or gui.mainFrame)
	else:
		log.debugWarning("Not displaying message box as shutdown has been triggered.", stack_info=True)
		res = wx.CANCEL
	return res


class DisplayableError(Exception):
	OnDisplayableErrorT = extensionPoints.Action
	"""
	A type of extension point used to notify a handler when an error occurs.
	This allows a handler to handle displaying an error.

	@param displayableError: Error that can be displayed to the user.
	@type displayableError: DisplayableError
	"""

	def __init__(self, displayMessage: str, titleMessage: Optional[str] = None):
		"""
		@param displayMessage: A translated message, to be displayed to the user.
		@param titleMessage: A translated message, to be used as a title for the display message.
		If left None, "Error" is presented as the title by default.
		"""
		self.displayMessage = displayMessage
		if titleMessage is None:
			# Translators: A message indicating that an error occurred.
			self.titleMessage = _("Error")
		else:
			self.titleMessage = titleMessage

	def displayError(self, parentWindow: wx.Window):
		wx.CallAfter(
			messageBox,
			message=self.displayMessage,
			caption=self.titleMessage,
			style=wx.OK | wx.ICON_ERROR,
			parent=parentWindow,
		)


@dataclass(frozen=True)
class Payload:
	"""Payload of information to pass to message dialog callbacks."""


type _Callback_T = Callable[[Payload], Any]


class _Missing_Type:
	"""Sentinel class to provide a nice repr."""

	def __repr__(self) -> str:
		return "MISSING"


_MISSING = _Missing_Type()
"""Sentinel for discriminating between `None` and an actually omitted argument."""


class ReturnCode(IntEnum):
	"""Enumeration of possible returns from :class:`MessageDialog`."""

	OK = wx.ID_OK
	CANCEL = wx.ID_CANCEL
	YES = wx.ID_YES
	NO = wx.ID_NO
	SAVE = wx.ID_SAVE
	APPLY = wx.ID_APPLY
	CLOSE = wx.ID_CLOSE
	HELP = wx.ID_HELP
	CUSTOM_1 = wx.ID_HIGHEST + 1
	CUSTOM_2 = wx.ID_HIGHEST + 2
	CUSTOM_3 = wx.ID_HIGHEST + 3
	CUSTOM_4 = wx.ID_HIGHEST + 4
	CUSTOM_5 = wx.ID_HIGHEST + 5


class EscapeCode(IntEnum):
	"""Enumeration of the behavior of the escape key and programmatic attempts to close a :class:`MessageDialog`."""

	NO_FALLBACK = wx.ID_NONE
	"""The escape key should have no effect, and programatically attempting to close the dialog should fail."""

	CANCEL_OR_AFFIRMATIVE = wx.ID_ANY
	"""The Cancel button should be emulated when closing the dialog by any means other than with a button in the dialog.
	If no Cancel button is present, the affirmative button should be used.
	"""


type wxArtID = int


class DialogType(Enum):
	"""Types of message dialogs.
	These are used to determine the icon and sound to play when the dialog is shown.
	"""

	STANDARD = auto()
	"""A simple message dialog, with no icon or sound.
	This should be used in most situations.
	"""

	WARNING = auto()
	"""A warning dialog, which makes the Windows alert sound and has an exclamation mark icon.
	This should be used when you have critical information to present to the user, such as when their action may result in irreversible loss of data.
	"""

	ERROR = auto()
	"""An error dialog, which has a cross mark icon and makes the Windows error sound.
	This should be used when a critical error has been encountered.
	"""

	@property
	def _wxIconId(self) -> wxArtID | None:
		"""The wx icon ID to use for this dialog type.
		This is used to determine the icon to display in the dialog.
		This will be None when the default icon should be used.
		"""
		match self:
			case self.ERROR:
				return wx.ART_ERROR
			case self.WARNING:
				return wx.ART_WARNING
			case _:
				return None

	@property
	def _windowsSoundId(self) -> int | None:
		"""The Windows sound ID to play for this dialog type.
		This is used to determine the sound to play when the dialog is shown.
		This will be None when no sound should be played.
		"""
		match self:
			case self.ERROR:
				return winsound.MB_ICONHAND
			case self.WARNING:
				return winsound.MB_ICONASTERISK
			case _:
				return None


class Button(NamedTuple):
	"""A button to add to a message dialog."""

	id: ReturnCode
	"""The ID to use for this button.

	This will be returned after showing the dialog modally.
	It is also used to modify the button later.
	"""

	label: str
	"""The label to display on the button."""

	callback: _Callback_T | None = None
	"""The callback to call when the button is clicked."""

	defaultFocus: bool = False
	"""Whether this button should explicitly be the default focused button.

	.. note:: This only overrides the default focus.
		If no buttons have this property, the first button will be the default focus.
	"""

	fallbackAction: bool = False
	"""Whether this button is the fallback action.

	The fallback action is called when the user presses escape, the title bar close button, or the system menu close item.
	It is also called when programatically closing the dialog, such as when shutting down NVDA.

	.. note:: This only sets whether to override the fallback action.
			`EscapeCode.DEFAULT` may still result in this button being the fallback action, even if `fallbackAction=False`.
	"""

	closesDialog: bool = True
	"""Whether this button should close the dialog when clicked.

	.. note:: Buttons with fallbackAction=True and closesDialog=False are not supported.
			See the documentation of :class:`MessageDialog` for information on how these buttons are handled.
	"""

	returnCode: ReturnCode | None = None
	"""Override for the default return code, which is the button's ID.

	.. note:: If None, the button's ID will be used as the return code when closing a modal dialog with this button.
	"""


class DefaultButton(Button, Enum):
	"""Default buttons for message dialogs."""

	# Translators: An ok button on a message dialog.
	OK = Button(id=ReturnCode.OK, label=_("OK"))
	# Translators: A yes button on a message dialog.
	YES = Button(id=ReturnCode.YES, label=_("&Yes"))
	# Translators: A no button on a message dialog.
	NO = Button(id=ReturnCode.NO, label=_("&No"))
	# Translators: A cancel button on a message dialog.
	CANCEL = Button(id=ReturnCode.CANCEL, label=_("Cancel"))
	# Translators: A save button on a message dialog.
	SAVE = Button(id=ReturnCode.SAVE, label=_("&Save"))
	# Translators: An apply button on a message dialog.
	APPLY = Button(id=ReturnCode.APPLY, label=_("&Apply"), closesDialog=False)
	# Translators: A close button on a message dialog.
	CLOSE = Button(id=ReturnCode.CLOSE, label=_("Close"))
	# Translators: A help button on a message dialog.
	HELP = Button(id=ReturnCode.HELP, label=_("Help"), closesDialog=False)


class DefaultButtonSet(tuple[DefaultButton], Enum):
	"""Commonly needed button combinations."""

	OK_CANCEL = (
		DefaultButton.OK,
		DefaultButton.CANCEL,
	)
	YES_NO = (
		DefaultButton.YES,
		DefaultButton.NO,
	)
	YES_NO_CANCEL = (
		DefaultButton.YES,
		DefaultButton.NO,
		DefaultButton.CANCEL,
	)
	SAVE_NO_CANCEL = (
		DefaultButton.SAVE,
		# Translators: A don't save button on a message dialog.
		DefaultButton.NO.value._replace(label=_("Do&n't save")),
		DefaultButton.CANCEL,
	)


class _Command(NamedTuple):
	"""Internal representation of a command for a message dialog."""

	callback: _Callback_T | None
	"""The callback function to be executed. Defaults to None."""

	closesDialog: bool
	"""Indicates whether the dialog should be closed after the command is executed. Defaults to True."""

	returnCode: ReturnCode


class MessageDialog(DpiScalingHelperMixinWithoutInit, ContextHelpMixin, wx.Dialog, metaclass=SIPABCMeta):
	"""Provides a more flexible message dialog.

	Creating dialogs with this class is extremely flexible. You can create a dialog, passing almost all parameters to the initialiser, and only call `Show` or `ShowModal` on the instance.
	You can also call the initialiser with very few arguments, and modify the dialog by calling methods on the created instance.
	Mixing and matching both patterns is also allowed.

	When subclassing this class, you can override `_addButtons` and `_addContents` to insert custom buttons or contents that you want your subclass to always have.

	.. warning:: Unless noted otherwise, the message dialog API is **not** thread safe.
	"""

	_instances: deque["MessageDialog"] = deque()
	"""Double-ended queue of open instances.
	When programatically closing non-blocking instances or focusing blocking instances, this should operate like a stack (I.E. LIFO behaviour).
	Random access still needs to be supported for the case of non-modal dialogs being closed out of order.
	"""
	_FAIL_ON_NONMAIN_THREAD = True
	"""Class default for whether to run the :meth:`._checkMainThread` test."""
	_FAIL_ON_NO_BUTTONS = True
	"""Class default for whether to run the :meth:`._checkHasButtons` test."""

	# region Constructors
	def __new__(cls, *args, **kwargs) -> Self:
		"""Override to disallow creation on non-main threads."""
		cls._checkMainThread()
		return super().__new__(cls, *args, **kwargs)

	def __init__(
		self,
		parent: wx.Window | None,
		message: str,
		title: str = wx.MessageBoxCaptionStr,
		dialogType: DialogType = DialogType.STANDARD,
		*,
		buttons: Collection[Button] | None = (DefaultButton.OK,),
		helpId: str = "",
	):
		"""Initialize the MessageDialog.

		:param parent: Parent window of this dialog.
			If given, this window will become inoperable while the dialog is shown modally.
		:param message: Message to display in the dialog.
		:param title: Window title for the dialog.
		:param dialogType: The type of the dialog, defaults to DialogType.STANDARD.
			Affects things like the icon and sound of the dialog.
		:param buttons: What buttons to place in the dialog, defaults to (DefaultButton.OK,).
			Further buttons can easily be added later.
		:param helpId: URL fragment of the relevant help entry in the user guide for this dialog, defaults to ""
		"""
		self._checkMainThread()
		self.helpId = helpId  # Must be set before initialising ContextHelpMixin.
		super().__init__(parent, title=title)
		self._isLayoutFullyRealized = False
		self._commands: dict[int, _Command] = {}
		"""Registry of commands bound to this MessageDialog."""

		# Stylistic matters.
		self.EnableCloseButton(False)
		self._setIcon(dialogType)
		self._setSound(dialogType)

		# Bind event listeners.
		self.Bind(wx.EVT_SHOW, self._onShowEvent, source=self)
		self.Bind(wx.EVT_ACTIVATE, self._onActivateEvent, source=self)
		self.Bind(wx.EVT_CLOSE, self._onCloseEvent)
		self.Bind(wx.EVT_BUTTON, self._onButtonEvent)
		self.Bind(wx.EVT_WINDOW_DESTROY, self._onDestroyEvent)

		# Scafold the dialog.
		mainSizer = self._mainSizer = wx.BoxSizer(wx.VERTICAL)
		contentsSizer = self._contentsSizer = guiHelper.BoxSizerHelper(parent=self, orientation=wx.VERTICAL)
		messageControl = self._messageControl = wx.StaticText(self)
		contentsSizer.addItem(messageControl)
		buttonHelper = self._buttonHelper = guiHelper.ButtonHelper(wx.HORIZONTAL)
		mainSizer.Add(
			contentsSizer.sizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL,
		)
		self.SetSizer(mainSizer)

		# Finally, populate the dialog.
		self.setMessage(message)
		self._addContents(contentsSizer)
		self._addButtons(buttonHelper)
		if buttons is not None:
			self.addButtons(buttons)
		contentsSizer.addDialogDismissButtons(buttonHelper)

	# endregion

	# region Public object API
	@singledispatchmethod
	def addButton(
		self,
		id: ReturnCode,
		/,
		label: str,
		*args,
		callback: _Callback_T | None = None,
		defaultFocus: bool = False,
		fallbackAction: bool = False,
		closesDialog: bool = True,
		returnCode: ReturnCode | None = None,
		**kwargs,
	) -> Self:
		"""Add a button to the dialog.

		:param id: The ID to use for the button.
		:param label: Text label to show on this button.
		:param callback: Function to call when the button is pressed, defaults to None.
			This is most useful for dialogs that are shown as non-modal.
		:param defaultFocus: whether this button should receive focus when the dialog is first opened, defaults to False.
			If multiple buttons with `defaultFocus=True` are added, the last one added will receive initial focus.
		:param fallbackAction: Whether or not this button should be the fallback action for the dialog, defaults to False.
			The fallback action is called when the user closes the dialog with the escape key, title bar close button, system menu close item etc.
			If multiple buttons with `fallbackAction=True` are added, the last one added will be the fallback action.
		:param closesDialog: Whether the button should close the dialog when pressed, defaults to True.
		:param returnCode: Override for the value returned from calls to :meth:`.ShowModal` when this button is pressed, defaults to None.
			If None, the button's ID will be used instead.
		:raises KeyError: If a button with this ID has already been added.
		:return: The updated instance for chaining.
		"""
		if id in self._commands:
			raise KeyError(f"A button with {id=} has already been added.")
		button = self._buttonHelper.addButton(self, id, label, *args, **kwargs)
		# Get the ID from the button instance in case it was created with id=wx.ID_ANY.
		buttonId = button.GetId()
		self.AddMainButtonId(buttonId)
		# fallback actions that do not close the dialog do not make sense.
		if fallbackAction and not closesDialog:
			log.warning(
				"fallback actions that do not close the dialog are not supported. Forcing closesDialog to True.",
			)
			closesDialog = True
		self._commands[buttonId] = _Command(
			callback=callback,
			closesDialog=closesDialog,
			returnCode=buttonId if returnCode is None else returnCode,
		)
		if defaultFocus:
			self.SetDefaultItem(button)
		if fallbackAction:
			self.setFallbackAction(buttonId)
		self.EnableCloseButton(self.hasFallback)
		self._isLayoutFullyRealized = False
		return self

	@addButton.register
	def _(
		self,
		button: Button,
		/,
		*args,
		label: str | _Missing_Type = _MISSING,
		callback: _Callback_T | None | _Missing_Type = _MISSING,
		defaultFocus: bool | _Missing_Type = _MISSING,
		fallbackAction: bool | _Missing_Type = _MISSING,
		closesDialog: bool | _Missing_Type = _MISSING,
		returnCode: ReturnCode | None | _Missing_Type = _MISSING,
		**kwargs,
	) -> Self:
		"""Add a :class:`Button` to the dialog.

		:param button: The button to add.
		:param label: Override for :attr:`~.Button.label`, defaults to the passed button's `label`.
		:param callback: Override for :attr:`~.Button.callback`, defaults to the passed button's `callback`.
		:param defaultFocus: Override for :attr:`~.Button.defaultFocus`, defaults to the passed button's `defaultFocus`.
		:param fallbackAction: Override for :attr:`~.Button.fallbackAction`, defaults to the passed button's `fallbackAction`.
		:param closesDialog: Override for :attr:`~.Button.closesDialog`, defaults to the passed button's `closesDialog`.
		:param returnCode: Override for :attr:`~.Button.returnCode`, defaults to the passed button's `returnCode`.
		:return: The updated instance for chaining.
		"""
		keywords = button._asdict()
		# We need to pass `id` as a positional argument as `singledispatchmethod` matches on the type of the first argument.
		id = keywords.pop("id")
		if label is not _MISSING:
			keywords["label"] = label
		if defaultFocus is not _MISSING:
			keywords["defaultFocus"] = defaultFocus
		if fallbackAction is not _MISSING:
			keywords["fallbackAction"] = fallbackAction
		if callback is not _MISSING:
			keywords["callback"] = callback
		if closesDialog is not _MISSING:
			keywords["closesDialog"] = closesDialog
		if returnCode is not _MISSING:
			keywords["returnCode"] = returnCode
		keywords.update(kwargs)
		return self.addButton(id, *args, **keywords)

	addOkButton = partialmethod(addButton, DefaultButton.OK)
	addOkButton.__doc__ = "Add an OK button to the dialog."
	addCancelButton = partialmethod(addButton, DefaultButton.CANCEL)
	addCancelButton.__doc__ = "Add a Cancel button to the dialog."
	addYesButton = partialmethod(addButton, DefaultButton.YES)
	addYesButton.__doc__ = "Add a Yes button to the dialog."
	addNoButton = partialmethod(addButton, DefaultButton.NO)
	addNoButton.__doc__ = "Add a No button to the dialog."
	addSaveButton = partialmethod(addButton, DefaultButton.SAVE)
	addSaveButton.__doc__ = "Add a Save button to the dialog."
	addApplyButton = partialmethod(addButton, DefaultButton.APPLY)
	addApplyButton.__doc__ = "Add an Apply button to the dialog."
	addCloseButton = partialmethod(addButton, DefaultButton.CLOSE)
	addCloseButton.__doc__ = "Add a Close button to the dialog."
	addHelpButton = partialmethod(addButton, DefaultButton.HELP)
	addHelpButton.__doc__ = "Add a Help button to the dialog."

	def addButtons(self, buttons: Collection[Button]) -> Self:
		"""Add multiple buttons to the dialog.

		:return: The dialog instance.
		"""
		buttonIds = set(button.id for button in buttons)
		if len(buttonIds) != len(buttons):
			raise KeyError("Button IDs must be unique.")
		if not buttonIds.isdisjoint(self._commands):
			raise KeyError("You may not add a new button with an existing id.")
		for button in buttons:
			self.addButton(button)
		return self

	addOkCancelButtons = partialmethod(addButtons, DefaultButtonSet.OK_CANCEL)
	addOkCancelButtons.__doc__ = "Add OK and Cancel buttons to the dialog."
	addYesNoButtons = partialmethod(addButtons, DefaultButtonSet.YES_NO)
	addYesNoButtons.__doc__ = "Add Yes and No buttons to the dialog."
	addYesNoCancelButtons = partialmethod(addButtons, DefaultButtonSet.YES_NO_CANCEL)
	addYesNoCancelButtons.__doc__ = "Add Yes, No and Cancel buttons to the dialog."
	addSaveNoCancelButtons = partialmethod(addButtons, DefaultButtonSet.SAVE_NO_CANCEL)
	addSaveNoCancelButtons.__doc__ = "Add Save, Don't save and Cancel buttons to the dialog."

	def setButtonLabel(self, id: ReturnCode, label: str) -> Self:
		"""Set the label of a button in the dialog.

		:param id: ID of the button whose label you want to change.
		:param label: New label for the button.
		:return: Updated instance for chaining.
		"""
		self._setButtonLabels((id,), (label,))
		return self

	setOkLabel = partialmethod(setButtonLabel, ReturnCode.OK)
	setOkLabel.__doc__ = "Set the label of the OK button in the dialog, if there is one."
	setHelpLabel = partialmethod(setButtonLabel, ReturnCode.HELP)
	setHelpLabel.__doc__ = "Set the label of the help button in the dialog, if there is one."

	def setOkCancelLabels(self, okLabel: str, cancelLabel: str) -> Self:
		"""Set the labels of the ok and cancel buttons in the dialog, if they exist."

		:param okLabel: New label for the ok button.
		:param cancelLabel: New label for the cancel button.
		:return: Updated instance for chaining.
		"""
		self._setButtonLabels((ReturnCode.OK, ReturnCode.CANCEL), (okLabel, cancelLabel))
		return self

	def setYesNoLabels(self, yesLabel: str, noLabel: str) -> Self:
		"""Set the labels of the yes and no buttons in the dialog, if they exist."

		:param yesLabel: New label for the yes button.
		:param noLabel: New label for the no button.
		:return: Updated instance for chaining.
		"""
		self._setButtonLabels((ReturnCode.YES, ReturnCode.NO), (yesLabel, noLabel))
		return self

	def setYesNoCancelLabels(self, yesLabel: str, noLabel: str, cancelLabel: str) -> Self:
		"""Set the labels of the yes and no buttons in the dialog, if they exist."

		:param yesLabel: New label for the yes button.
		:param noLabel: New label for the no button.
		:param cancelLabel: New label for the cancel button.
		:return: Updated instance for chaining.
		"""
		self._setButtonLabels(
			(ReturnCode.YES, ReturnCode.NO, ReturnCode.CANCEL),
			(yesLabel, noLabel, cancelLabel),
		)
		return self

	def setMessage(self, message: str) -> Self:
		"""Set the textual message to display in the dialog.

		:param message: New message to show.
		:return: Updated instance for chaining.
		"""
		# Use SetLabelText to avoid ampersands being interpreted as accelerators.
		self._messageControl.SetLabelText(message)
		self._isLayoutFullyRealized = False
		return self

	def setDefaultFocus(self, id: ReturnCode) -> Self:
		"""Set the button to be focused when the dialog first opens.

		:param id: The id of the button to set as default.
		:raises KeyError: If no button with id exists.
		:return: The updated dialog.
		"""
		if (win := self.FindWindow(id)) is not None:
			self.SetDefaultItem(win)
		else:
			raise KeyError(f"Unable to find button with {id=}.")
		return self

	def SetEscapeId(self, id: ReturnCode | EscapeCode) -> Self:
		"""Set the action to take when closing the dialog by any means other than a button in the dialog.

		:param id: The ID of the action to take.
			This should be the ID of the button that the user can press to explicitly perform this action.
			The action should have `closesDialog=True`.

			The following special values are also supported:
				* EscapeCode.NONE: If the dialog should only be closable via presses of internal buttons.
				* EscapeCode.DEFAULT: If the cancel or affirmative (usually OK) button should be used.
					If no Cancel or affirmative button is present, most attempts to close the dialog by means other than via buttons in the dialog wil have no effect.

		:raises KeyError: If no action with the given id has been registered.
		:raises ValueError: If the action with the given id does not close the dialog.
		:return: The updated dialog instance.
		"""
		if id not in (EscapeCode.CANCEL_OR_AFFIRMATIVE, EscapeCode.NO_FALLBACK):
			if id not in self._commands:
				raise KeyError(f"No command registered for {id=}.")
			if not self._commands[id].closesDialog:
				raise ValueError("fallback actions that do not close the dialog are not supported.")
		self.EnableCloseButton(id != EscapeCode.NO_FALLBACK)
		super().SetEscapeId(id)
		return self

	def setFallbackAction(self, id: ReturnCode | EscapeCode) -> Self:
		"""See :meth:`MessageDialog.SetEscapeId`."""
		return self.SetEscapeId(id)

	def Show(self, show: bool = True) -> bool:
		"""Show a non-blocking dialog.

		Attach buttons with :meth:`.addButton`, :meth:`.addButtons`, or any of their more specific helpers.

		:param show: If True, show the dialog. If False, hide it. Defaults to True.
		"""
		if not show:
			return self.Hide()
		self._checkShowable()
		self._realizeLayout()
		log.debug(f"Showing {self!r} as non-modal.")
		shown = super().Show(show)
		if shown:
			log.debug(f"Adding {self!r} to instances.")
			self._instances.append(self)
		return shown

	def ShowModal(self) -> ReturnCode:
		"""Show a blocking dialog.

		Attach buttons with :meth:`.addButton`, :meth:`.addButtons`, or any of their more specific helpers.
		"""
		self._checkShowable()
		self._realizeLayout()

		# We want to call `displayDialogAsModal` from our implementation of ShowModal, so we need to switch our instance out now that it's running and replace it with that provided by :class:`wx.Dialog`.
		self.__ShowModal = self.ShowModal
		self.ShowModal = super().ShowModal
		log.debug(f"Adding {self!r} to instances.")
		self._instances.append(self)
		log.debug(f"Showing {self!r} as modal")
		ret = displayDialogAsModal(self)

		# Restore our implementation of ShowModal.
		self.ShowModal = self.__ShowModal
		return ret

	@property
	def isBlocking(self) -> bool:
		"""Whether or not the dialog is blocking"""
		return self.IsModal() or not self.hasFallback

	@property
	def hasFallback(self) -> bool:
		"""Whether the dialog has a valid fallback action.

		Assumes that any explicit action (i.e. not EscapeCode.NONE or EscapeCode.DEFAULT) is valid.
		"""
		escapeId = self.GetEscapeId()
		return escapeId != EscapeCode.NO_FALLBACK and (
			any(
				id in (ReturnCode.CANCEL, self.GetAffirmativeId()) and command.closesDialog
				for id, command in self._commands.items()
			)
			if escapeId == EscapeCode.CANCEL_OR_AFFIRMATIVE
			else True
		)

	# endregion

	# region Public class methods
	@classmethod
	def closeInstances(cls) -> None:
		"""Close all dialogs with a fallback action.

		This does not force-close all instances, so instances may veto being closed.
		"""
		for instance in cls._instances:
			if not instance.isBlocking:
				instance.Close()

	@classmethod
	def blockingInstancesExist(cls) -> bool:
		"""Check if modal dialogs are open without a fallback action."""
		return any(dialog.isBlocking for dialog in cls._instances)

	@classmethod
	def focusBlockingInstances(cls) -> None:
		"""Raise and focus open modal dialogs without a fallback action."""
		lastDialog: MessageDialog | None = None
		for dialog in cls._instances:
			if dialog.isBlocking:
				lastDialog = dialog
				dialog.Raise()
		if lastDialog:
			lastDialog.SetFocus()

	@classmethod
	def alert(
		cls,
		message: str,
		caption: str = wx.MessageBoxCaptionStr,
		parent: wx.Window | None = None,
		*,
		okLabel: str | None = None,
	):
		"""Display a blocking dialog with an OK button.

		.. note:: This method is thread safe.

		:param message: The message to be displayed in the alert dialog.
		:param caption: The caption of the alert dialog, defaults to wx.MessageBoxCaptionStr.
		:param parent: The parent window of the alert dialog, defaults to None.
		:param okLabel: Override for the label of the OK button, defaults to None.
		"""

		def impl():
			dlg = cls(parent, message, caption, buttons=(DefaultButton.OK,))
			if okLabel is not None:
				dlg.setOkLabel(okLabel)
			dlg.ShowModal()

		wxCallOnMain(impl)

	@classmethod
	def confirm(
		cls,
		message,
		caption=wx.MessageBoxCaptionStr,
		parent=None,
		*,
		okLabel=None,
		cancelLabel=None,
	) -> Literal[ReturnCode.OK, ReturnCode.CANCEL]:
		"""Display a confirmation dialog with OK and Cancel buttons.

		.. note:: This method is thread safe.

		:param message: The message to be displayed in the dialog.
		:param caption: The caption of the dialog window, defaults to wx.MessageBoxCaptionStr.
		:param parent: The parent window for the dialog, defaults to None.
		:param okLabel: Override for the label of the OK button, defaults to None.
		:param cancelLabel: Override for the label of the Cancel button, defaults to None.
		:return: ReturnCode.OK if OK is pressed, ReturnCode.CANCEL if Cancel is pressed.
		"""

		def impl():
			dlg = cls(parent, message, caption, buttons=DefaultButtonSet.OK_CANCEL)
			if okLabel is not None:
				dlg.setOkLabel(okLabel)
			if cancelLabel is not None:
				dlg.setButtonLabel(ReturnCode.CANCEL, cancelLabel)
			return dlg.ShowModal()

		return wxCallOnMain(impl)

	@classmethod
	def ask(
		cls,
		message,
		caption=wx.MessageBoxCaptionStr,
		parent=None,
		yesLabel=None,
		noLabel=None,
		cancelLabel=None,
	) -> Literal[ReturnCode.YES, ReturnCode.NO, ReturnCode.CANCEL]:
		"""Display a query dialog with Yes, No, and Cancel buttons.

		.. note:: This method is thread safe.

		:param message: The message to be displayed in the dialog.
		:param caption: The title of the dialog window, defaults to wx.MessageBoxCaptionStr.
		:param parent: The parent window for the dialog, defaults to None.
		:param yesLabel: Override for the label of the Yes button, defaults to None.
		:param noLabel: Override for the label of the No button, defaults to None.
		:param cancelLabel: Override for the label of the Cancel button, defaults to None.
		:return: ReturnCode.YES, ReturnCode.NO or ReturnCode.CANCEL, according to the user's action.
		"""

		def impl():
			dlg = cls(parent, message, caption, buttons=DefaultButtonSet.YES_NO_CANCEL)
			if yesLabel is not None:
				dlg.setButtonLabel(ReturnCode.YES, yesLabel)
			if noLabel is not None:
				dlg.setButtonLabel(ReturnCode.NO, noLabel)
			if cancelLabel is not None:
				dlg.setButtonLabel(ReturnCode.CANCEL, cancelLabel)
			return dlg.ShowModal()

		return wxCallOnMain(impl)

	# endregion

	# region Methods for subclasses
	def _addButtons(self, buttonHelper: guiHelper.ButtonHelper) -> None:
		"""Adds additional buttons to the dialog, before any other buttons are added.
		Subclasses may implement this method.
		"""

	def _addContents(self, contentsSizer: guiHelper.BoxSizerHelper) -> None:
		"""Adds additional contents to the dialog, before the buttons.
		Subclasses may implement this method.
		"""

	# endregion

	# region Internal API
	def _checkShowable(self, *, checkMainThread: bool | None = None, checkButtons: bool | None = None):
		"""Checks that must pass in order to show a Message Dialog.

		If any of the specified tests fails, an appropriate exception will be raised.
		See test implementations for details.

		:param checkMainThread: Whether to check that we're running on the GUI thread, defaults to True.
			Implemented in :meth:`._checkMainThread`.
		:param checkButtons: Whether to check there is at least one command registered, defaults to True.
			Implemented in :meth:`._checkHasButtons`.
		"""
		self._checkMainThread(checkMainThread)
		self._checkHasButtons(checkButtons)

	def _checkHasButtons(self, check: bool | None = None):
		"""Check that the dialog has at least one button.

		:param check: Whether to run the test or fallback to the class default, defaults to None.
			If `None`, the value set in :const:`._FAIL_ON_NO_BUTTONS` is used.
		:raises RuntimeError: If the dialog does not have any buttons.
		"""
		if check is None:
			check = self._FAIL_ON_NO_BUTTONS
		if check and not self.GetMainButtonIds():
			raise RuntimeError("MessageDialogs cannot be shown without buttons.")

	@classmethod
	def _checkMainThread(cls, check: bool | None = None):
		"""Check that we're running on the main (GUI) thread.

		:param check: Whether to run the test or fallback to the class default, defaults to None
			If `None`, :const:`._FAIL_ON_NONMAIN_THREAD` is used.
		:raises RuntimeError: If running on any thread other than the wxPython GUI thread.
		"""
		if check is None:
			check = cls._FAIL_ON_NONMAIN_THREAD
		if check and not wx.IsMainThread():
			raise RuntimeError("Message dialogs can only be used from the main thread.")

	def _realizeLayout(self) -> None:
		"""Perform layout adjustments prior to showing the dialog."""
		if self._isLayoutFullyRealized:
			return
		if gui._isDebug():
			startTime = time.time()
			log.debug("Laying out message dialog")
		self._messageControl.Wrap(self.scaleSize(self.GetSize().Width))
		self._mainSizer.Fit(self)
		if self.Parent == gui.mainFrame:
			# NVDA's main frame is not visible on screen, so centre on screen rather than on `mainFrame` to avoid the dialog appearing at the top left of the screen.
			self.CentreOnScreen()
		else:
			self.CentreOnParent()
		self._isLayoutFullyRealized = True
		if gui._isDebug():
			log.debug(f"Layout completed in {time.time() - startTime:.3f} seconds")

	def _getFallbackAction(self) -> _Command | None:
		"""Get the fallback action of this dialog.

		:return: The id and command of the fallback action.
		"""
		escapeId = self.GetEscapeId()
		if escapeId == EscapeCode.NO_FALLBACK:
			return None
		elif escapeId == EscapeCode.CANCEL_OR_AFFIRMATIVE:
			affirmativeAction: _Command | None = None
			affirmativeId: int = self.GetAffirmativeId()
			for id, command in self._commands.items():
				if id == ReturnCode.CANCEL:
					return command
				elif id == affirmativeId:
					affirmativeAction = command
			if affirmativeAction is None:
				return None
			else:
				return affirmativeAction
		else:
			return self._commands[escapeId]

	def _getFallbackActionOrFallback(self) -> _Command:
		"""Get a command that is guaranteed to close this dialog.

		Commands are returned in the following order of preference:

		1. The developer-set fallback action.
		2. The developer-set default focus.
		3. The first button in the dialog explicitly set to close the dialog.
		4. The first button in the dialog, regardless of whether it closes the dialog.
		5. A new action, with id=EscapeCode.NONE and no callback.

		In all cases, if the command has `closesDialog=False`, this will be overridden to `True` in the returned copy.

		:return: Id and command of the default command.
		"""

		def getAction() -> _Command:
			# Try using the developer-specified fallback action.
			try:
				if (action := self._getFallbackAction()) is not None:
					return action
			except KeyError:
				log.error("fallback action was not in commands. This indicates a logic error.")

			# fallback action is unavailable. Try using the default focus instead.
			if (defaultFocus := self.GetDefaultItem()) is not None:
				# Default focus does not have to be a command, for instance if a custom control has been added and made the default focus.
				if (action := self._commands.get(defaultFocus.GetId(), None)) is not None:
					return action

			# Default focus is unavailable or not a command. Try using the first registered command that closes the dialog instead.
			if len(self._commands) > 0:
				try:
					return next(command for command in self._commands.values() if command.closesDialog)
				except StopIteration:
					# No commands that close the dialog have been registered. Use the first command instead.
					return next(iter(self._commands.values()))
			else:
				log.error(
					"No commands have been registered. If the dialog is shown, this indicates a logic error.",
				)

			# No commands have been registered. Create one of our own.
			return _Command(callback=None, closesDialog=True, returnCode=wx.ID_NONE)

		command = getAction()
		if not command.closesDialog:
			log.debugWarning(f"Overriding command for {id=} to close dialog.")
			command = command._replace(closesDialog=True)
		return command

	def _setButtonLabels(self, ids: Collection[ReturnCode], labels: Collection[str]):
		"""Set a batch of button labels atomically.

		:param ids: IDs of the buttons whose labels should be changed.
		:param labels: Labels for those buttons.
		:raises ValueError: If the number of IDs and labels is not equal.
		:raises KeyError: If any of the given IDs does not exist in the command registry.
		:raises TypeError: If any of the IDs does not refer to a :class:`wx.Button`.
		"""
		if len(ids) != len(labels):
			raise ValueError("The number of IDs and labels must be equal.")
		buttons: list[wx.Button] = []
		for id in ids:
			if id not in self._commands:
				raise KeyError(f"No button with {id=} registered.")
			elif isinstance((button := self.FindWindow(id)), wx.Button):
				buttons.append(button)
			else:
				raise TypeError(
					f"{id=} exists in command registry, but does not refer to a wx.Button. This indicates a logic error.",
				)
		for button, label in zip(buttons, labels):
			button.SetLabel(label)

	def _setIcon(self, type: DialogType) -> None:
		"""Set the icon to be displayed on the dialog."""
		if (iconID := type._wxIconId) is not None:
			icon = wx.ArtProvider.GetIconBundle(iconID, client=wx.ART_MESSAGE_BOX)
			self.SetIcons(icon)

	def _setSound(self, type: DialogType) -> None:
		"""Set the sound to be played when the dialog is shown."""
		self._soundID = type._windowsSoundId

	def _playSound(self) -> None:
		"""Play the sound set for this dialog."""
		if self._soundID is not None:
			winsound.MessageBeep(self._soundID)

	def _onActivateEvent(self, evt: wx.ActivateEvent):
		evt.Skip()

	def _onShowEvent(self, evt: wx.ShowEvent):
		"""Event handler for when the dialog is shown.

		Responsible for playing the alert sound and focusing the default button.
		"""
		if evt.IsShown():
			self._playSound()
			if (defaultItem := self.GetDefaultItem()) is not None:
				defaultItem.SetFocus()
		self.Raise()
		evt.Skip()

	def _onCloseEvent(self, evt: wx.CloseEvent):
		"""Event handler for when the dialog is asked to close.

		Responsible for calling fallback event handlers and scheduling dialog distruction.
		"""
		if not evt.CanVeto():
			# We must close the dialog, regardless of state.
			self.Hide()
			self._executeCommand(self._getFallbackActionOrFallback(), _canCallClose=False)
			log.debug(f"Removing {self!r} from instances.")
			self._instances.remove(self)
			if self.IsModal():
				self.EndModal(self.GetReturnCode())
			self.Destroy()
			return
		if self.GetReturnCode() == 0:
			# No button has been pressed, so this must be a close event from elsewhere.
			try:
				command = self._getFallbackAction()
			except KeyError:
				log.error("Unable to get fallback action from commands. This indicates incorrect usage.")
				command = None
			if command is None or not command.closesDialog:
				evt.Veto()
				return
			self.Hide()
			self._executeCommand(command, _canCallClose=False)
		self.Hide()
		if self.IsModal():
			self.EndModal(self.GetReturnCode())
		log.debug(f"Queueing {self!r} for destruction")
		self.DestroyLater()
		log.debug(f"Removing {self!r} from instances.")
		self._instances.remove(self)

	def _onButtonEvent(self, evt: wx.CommandEvent):
		"""Event handler for button presses.

		Responsible for executing commands associated with buttons.
		"""
		id = evt.GetId()
		log.debug(f"Got button event on {id=}")
		try:
			self._executeCommand(self._commands[id])
		except KeyError:
			log.debug(f"No command registered for {id=}.")

	def _onDestroyEvent(self, evt: wx.WindowDestroyEvent):
		"""Ensures this instances is removed if the default close event handler is not called."""
		if self in self._instances:
			log.debug(f"Removing {self!r} from instances.")
			self._instances.remove(self)

	def _executeCommand(
		self,
		command: _Command,
		*,
		_canCallClose: bool = True,
	):
		"""Execute a command on this dialog.

		:param command: Command to execute.
		:param _canCallClose: Whether or not to close the dialog if the command says to, defaults to True.
			Set to False when calling from a close handler.
		"""
		callback, close, returnCode = command
		close &= _canCallClose
		if callback is not None:
			if close:
				self.Hide()
			payload = Payload()
			callback(payload)
		if close:
			self.SetReturnCode(returnCode)
			self.Close()

	# endregion


def _messageBoxShim(message: str, caption: str, style: int, parent: wx.Window | None):
	"""Display a message box with the given message, caption, style, and parent window.

	Shim between :fun:`gui.message.messageBox` and :class:`MessageDialog`.
	Must be called from the GUI thread.

	:param message: The message to display.
	:param caption: Title of the message box.
	:param style: See :fun:`wx.MessageBox`.
	:param parent: Parent of the dialog. If None, :data:`gui.mainFrame` will be used.
	:raises Exception: Any exception raised by attempting to create a message box.
	:return: See :fun:`wx.MessageBox`.
	"""
	dialog = MessageDialog(
		parent=parent,
		message=message,
		title=caption,
		dialogType=_messageBoxIconStylesToMessageDialogType(style),
		buttons=_messageBoxButtonStylesToMessageDialogButtons(style),
	)
	return _messageDialogReturnCodeToMessageBoxReturnCode(dialog.ShowModal())


def _messageDialogReturnCodeToMessageBoxReturnCode(returnCode: ReturnCode) -> int:
	"""Map from an instance of :class:`ReturnCode` to an int as returned by :fun:`wx.MessageBox`.

	:param returnCode: Return from :class:`MessageDialog`.
	:raises ValueError: If the return code is not supported by :fun:`wx.MessageBox`.
	:return: Integer as would be returned by :fun:`wx.MessageBox`.
	.. note:: Only YES, NO, OK, CANCEL and HELP returns are supported by :fun:`wx.MessageBox`, and thus by this function.
	"""
	match returnCode:
		case ReturnCode.YES:
			return wx.YES
		case ReturnCode.NO:
			return wx.NO
		case ReturnCode.CANCEL:
			return wx.CANCEL
		case ReturnCode.OK:
			return wx.OK
		case ReturnCode.HELP:
			return wx.HELP
		case _:
			raise ValueError(f"Unsupported return for wx.MessageBox: {returnCode}")


def _messageBoxIconStylesToMessageDialogType(flags: int) -> DialogType:
	"""Map from a bitmask of styles as expected by :fun:`wx.MessageBox` to a :Class:`DialogType`.

	:param flags: Style flags.
	:return: Corresponding dialog type.
	.. note:: This may not be a one-to-one correspondance, as not all icon styles supported by :fun:`wx.MessageBox` are associated with a :class:`DialogType`.
	"""
	# Order of precedence seems to be none, then error, then warning.
	if flags & wx.ICON_NONE:
		return DialogType.STANDARD
	elif flags & wx.ICON_ERROR:
		return DialogType.ERROR
	elif flags & wx.ICON_WARNING:
		return DialogType.WARNING
	else:
		return DialogType.STANDARD


def _messageBoxButtonStylesToMessageDialogButtons(flags: int) -> tuple[Button, ...]:
	"""Map from a bitmask of styles as expected by :fun:`wx.MessageBox` to a list of :class:`Button`s.

	This function will always return a tuple of at least one button, typically an OK button.

	:param flags: Style flags.
	:return: Tuple of :class:`Button` instances.
	.. note:: :fun:`wx.MessageBox` only supports YES, NO, OK, CANCEL and HELP buttons, so this function only supports those buttons too.
		Providing other buttons will fail silently.
	.. note:: Providing `wx.CANCEL_DEFAULT` without `wx.CANCEL`, or `wx.NO_DEFAULT` without `wx.NO` is invalid.
		Wx will raise an assertion error about this, but wxPython will still create the dialog.
		Providing these invalid combinations to this function fails silently.
	"""
	buttons: list[Button] = []
	if flags & (wx.YES | wx.NO):
		# Wx will add yes and no buttons, even if only one of wx.YES or wx.NO is given.
		buttons.extend(
			(DefaultButton.YES, DefaultButton.NO._replace(defaultFocus=bool(flags & wx.NO_DEFAULT))),
		)
	else:
		buttons.append(DefaultButton.OK)
	if flags & wx.CANCEL:
		buttons.append(
			DefaultButton.CANCEL._replace(
				defaultFocus=(flags & wx.CANCEL_DEFAULT) & ~(flags & wx.NO & wx.NO_DEFAULT),
			),
		)
	if flags & wx.HELP:
		buttons.append(DefaultButton.HELP)
	return tuple(buttons)
