# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from enum import Enum, IntEnum, auto
import time
from typing import Any, Literal, NamedTuple, TypeAlias, Self
import winsound

import wx

import gui

from .contextHelp import ContextHelpMixin
from .dpiScalingHelper import DpiScalingHelperMixinWithoutInit
from .guiHelper import SIPABCMeta, wxCallOnMain
from gui import guiHelper
from functools import partialmethod, singledispatchmethod
from collections import deque
from collections.abc import Collection, Callable
from logHandler import log


# TODO: Change to type statement when Python 3.12 or later is in use.
Callback_T: TypeAlias = Callable[[], Any]


class _Missing_Type:
	def __repr(self):
		return "MISSING"


_MISSING = _Missing_Type()


class ReturnCode(IntEnum):
	"""Enumeration of possible returns from c{MessageDialog}."""

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
	"""Enumeration of the behavior of the escape key and programmatic attempts to close a c{MessageDialog}."""

	NONE = wx.ID_NONE
	"""The escape key should have no effect, and programatically attempting to close the dialog should fail."""
	DEFAULT = wx.ID_ANY
	"""The Cancel button should be emulated when closing the dialog by any means other than with a button in the dialog.
	If no Cancel button is present, the affirmative button should be used.
	"""


class DialogType(Enum):
	"""Types of message dialogs.
	These are used to determine the icon and sound to play when the dialog is shown.
	"""

	STANDARD = auto()
	WARNING = auto()
	ERROR = auto()

	@property
	def _wxIconId(self) -> "wx.ArtID | None":  # type: ignore
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

	callback: Callback_T | None = None
	"""The callback to call when the button is clicked."""

	defaultFocus: bool = False
	"""Whether this button should explicitly be the default focused button.

	:note: This only overrides the default focus.
	If no buttons have this property, the first button will be the default focus.
	"""

	fallbackAction: bool = False
	"""Whether this button is the fallback action.

	The fallback action is called when the user presses escape, the title bar close button, or the system menu close item.
	It is also called when programatically closing the dialog, such as when shutting down NVDA.

	:note: This only sets whether to override the fallback action.
		`EscapeCode.DEFAULT` may still result in this button being the fallback action, even if `fallbackAction=False`.
	"""

	closesDialog: bool = True
	"""Whether this button should close the dialog when clicked.

	:note: Buttons with fallbackAction=True and closesDialog=False are not supported.
		See the documentation of c{MessageDialog} for information on how these buttons are handled.
	"""

	returnCode: ReturnCode | None = None
	"""Override for the default return code, which is the button's ID.

	:note: If None, the button's ID will be used as the return code when closing a modal dialog with this button.
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

	callback: Callback_T | None
	"""The callback function to be executed. Defaults to None."""
	closesDialog: bool
	"""Indicates whether the dialog should be closed after the command is executed. Defaults to True."""
	ReturnCode: ReturnCode


class MessageDialog(DpiScalingHelperMixinWithoutInit, ContextHelpMixin, wx.Dialog, metaclass=SIPABCMeta):
	"""Provides a more flexible message dialog.

	Creating dialogs with this class is extremely flexible. You can create a dialog, passing almost all parameters to the initialiser, and only call `Show` or `ShowModal` on the instance.
	You can also call the initialiser with very few arguments, and modify the dialog by calling methods on the created instance.
	Mixing and matching both patterns is also allowed.

	When subclassing this class, you can override `_addButtons` and `_addContents` to insert custom buttons or contents that you want your subclass to always have.
	"""

	_instances: deque["MessageDialog"] = deque()
	"""Double-ended queue of open instances.
	When programatically closing non-blocking instances or focusing blocking instances, this should operate like a stack (I.E. LIFO behaviour).
	Random access still needs to be supported for the case of non-modal dialogs being closed out of order.
	"""
	_FAIL_ON_NONMAIN_THREAD = True
	_FAIL_ON_NO_BUTTONS = True

	# region Constructors
	def __new__(cls, *args, **kwargs) -> Self:
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
		self._checkMainThread()
		self.helpId = helpId
		super().__init__(parent, title=title)
		self.EnableCloseButton(False)
		self._isLayoutFullyRealized = False
		self._commands: dict[int, _Command] = {}

		self._setIcon(dialogType)
		self._setSound(dialogType)
		self.Bind(wx.EVT_SHOW, self._onShowEvt, source=self)
		self.Bind(wx.EVT_ACTIVATE, self._onDialogActivated, source=self)
		self.Bind(wx.EVT_CLOSE, self._onCloseEvent)
		self.Bind(wx.EVT_BUTTON, self._onButton)

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		contentsSizer = guiHelper.BoxSizerHelper(parent=self, orientation=wx.VERTICAL)
		self._contentsSizer = contentsSizer
		self._mainSizer = mainSizer

		# Use SetLabelText to avoid ampersands being interpreted as accelerators.
		text = wx.StaticText(self)
		text.SetLabelText(message)
		text.Wrap(self.scaleSize(self.GetSize().Width))
		contentsSizer.addItem(text)
		self._addContents(contentsSizer)

		buttonHelper = guiHelper.ButtonHelper(wx.HORIZONTAL)
		contentsSizer.addDialogDismissButtons(buttonHelper)
		self._buttonHelper = buttonHelper
		self._addButtons(buttonHelper)
		if buttons is not None:
			self.addButtons(buttons)

		mainSizer.Add(
			contentsSizer.sizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL,
		)
		# mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		# Import late to avoid circular import
		# from gui import mainFrame

		# if parent == mainFrame:
		# 	# NVDA's main frame is not visible on screen, so centre on screen rather than on `mainFrame` to avoid the dialog appearing at the top left of the screen.
		# 	self.CentreOnScreen()
		# else:
		# 	self.CentreOnParent()

	# endregion

	# region Public object API
	@singledispatchmethod
	def addButton(
		self,
		id: ReturnCode,
		/,
		label: str,
		*args,
		callback: Callback_T | None = None,
		defaultFocus: bool = False,
		fallbackAction: bool = False,
		closesDialog: bool = True,
		returnCode: ReturnCode | None = None,
		**kwargs,
	) -> Self:
		"""Add a button to the dialog.

		:param id: The ID to use for the button.
			If the dialog is to be shown modally, this will also be the return value if the dialog is closed with this button.
		:param label: Text label to show on this button.
		:param callback: Function to call when the button is pressed, defaults to None.
			This is most useful for dialogs that are shown modelessly.
		:param defaultFocus: whether this button should receive focus when the dialog is first opened, defaults to False.
			If multiple buttons with `defaultFocus=True` are added, the last one added will receive initial focus.
		:param fallbackAction: Whether or not this button should be the fallback action for the dialog, defaults to False.
			The fallback action is called when the user closes the dialog with the escape key, title bar close button, system menu close item etc.
			If multiple buttons with `fallbackAction=True` are added, the last one added will be the fallback action.
		:param closesDialog: Whether the button should close the dialog when pressed, defaults to True.
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
			closesDialog=closesDialog or fallbackAction,
			ReturnCode=buttonId if returnCode is None else returnCode,
		)
		if defaultFocus:
			self.SetDefaultItem(button)
		if fallbackAction:
			self.setDefaultAction(buttonId)
		self.EnableCloseButton(self.hasDefaultAction)
		self._isLayoutFullyRealized = False
		return self

	@addButton.register
	def _(
		self,
		button: Button,
		/,
		*args,
		label: str | _Missing_Type = _MISSING,
		callback: Callback_T | _Missing_Type = _MISSING,
		defaultFocus: bool | _Missing_Type = _MISSING,
		fallbackAction: bool | _Missing_Type = _MISSING,
		closesDialog: bool | _Missing_Type = _MISSING,
		returnCode: ReturnCode | None | _Missing_Type = _MISSING,
		**kwargs,
	) -> Self:
		"""Add a :class:`Button` to the dialog.

		:param button: The button to add.
		:param label: Override for `button.label`, defaults to None.
		:param callback: Override for `button.callback`, defaults to None.
		:param defaultFocus: Override for `button.defaultFocus`, defaults to None.
		:param fallbackAction: Override for `button.fallbackAction`, defaults to None
		:param closesDialog: Override for `button.closesDialog`, defaults to None
		:return: Updated dialog instance for chaining.

		.. seealso:: :class:`Button`
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

	def setButtonLabel(self, id: ReturnCode, label: str) -> Self: ...
	def setOkLabel(self, label: str) -> Self: ...
	def setHelpLabel(self, label: str) -> Self: ...
	def setOkCancelLabels(self, okLabel: str, cancelLabel: str) -> Self: ...
	def setYesNoLabels(self, yesLabel: str, noLabel: str) -> Self: ...
	def setYesNoCancelLabels(self, yesLabel: str, noLabel: str, cancelLabel: str) -> Self: ...
	def setMessage(self, message: str) -> Self: ...

	def setDefaultFocus(self, id: ReturnCode) -> Self:
		"""Set the button to be focused when the dialog first opens.

		:param id: The id of the button to set as default.
		:raises KeyError: If no button with id exists.
		:return: The updated dialog.
		"""
		if (win := self.FindWindowById(id)) is not None:
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
		if id not in (EscapeCode.DEFAULT, EscapeCode.NONE):
			if id not in self._commands:
				raise KeyError(f"No command registered for {id=}.")
			if not self._commands[id].closesDialog:
				raise ValueError("fallback actions that do not close the dialog are not supported.")
		self.EnableCloseButton(id != EscapeCode.NONE)
		super().SetEscapeId(id)
		return self

	def setDefaultAction(self, id: ReturnCode | EscapeCode) -> Self:
		"""See MessageDialog.SetEscapeId."""
		return self.SetEscapeId(id)

	def Show(self, show: bool = True) -> bool:
		"""Show a non-blocking dialog.

		Attach buttons with button handlers

		:param show: If True, show the dialog. If False, hide it. Defaults to True.
		"""
		if not show:
			return self.Hide()
		self._checkShowable()
		self._realize_layout()
		log.debug("Showing")
		ret = super().Show(show)
		if ret:
			log.debug("Adding to instances")
			self._instances.append(self)
		return ret

	def ShowModal(self) -> ReturnCode:
		"""Show a blocking dialog.
		Attach buttons with button handlers"""
		self._checkShowable()
		self._realize_layout()
		self.__ShowModal = self.ShowModal
		self.ShowModal = super().ShowModal
		from .message import displayDialogAsModal

		log.debug("Adding to instances")
		self._instances.append(self)
		log.debug("Showing modal")
		ret = displayDialogAsModal(self)
		self.ShowModal = self.__ShowModal
		return ret

	@property
	def isBlocking(self) -> bool:
		"""Whether or not the dialog is blocking"""
		return self.IsModal() and not self.hasDefaultAction

	@property
	def hasDefaultAction(self) -> bool:
		"""Whether the dialog has a valid fallback action."""
		escapeId = self.GetEscapeId()
		return escapeId != EscapeCode.NONE and (
			any(
				id in (ReturnCode.CANCEL, self.GetAffirmativeId()) and command.closesDialog
				for id, command in self._commands.items()
			)
			if escapeId == EscapeCode.DEFAULT
			else True
		)

	# endregion

	# region Public class methods
	@classmethod
	def CloseInstances(cls) -> None:
		"""Close all dialogs with a fallback action"""
		for instance in cls._instances:
			if not instance.isBlocking:
				instance.Close()

	@classmethod
	def BlockingInstancesExist(cls) -> bool:
		"""Check if dialogs are open without a default return code
		(eg Show without `self._defaultReturnCode`, or ShowModal without `wx.CANCEL`)"""
		return any(dialog.isBlocking for dialog in cls._instances)

	@classmethod
	def FocusBlockingInstances(cls) -> None:
		"""Raise and focus open dialogs without a default return code
		(eg Show without `self._defaultReturnCode`, or ShowModal without `wx.CANCEL`)"""
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

		:param message: The message to be displayed in the alert dialog.
		:param caption: The caption of the alert dialog, defaults to wx.MessageBoxCaptionStr.
		:param parent: The parent window of the alert dialog, defaults to None.
		:param okLabel: Override for the label of the OK button, defaults to None.
		"""

		def impl():
			cls(parent, message, caption, buttons=None).addOkButton(label=okLabel).ShowModal()

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

		:param message: The message to be displayed in the dialog.
		:param caption: The caption of the dialog window, defaults to wx.MessageBoxCaptionStr.
		:param parent: The parent window for the dialog, defaults to None.
		:param okLabel: Override for the label of the OK button, defaults to None.
		:param cancelLabel: Override for the label of the Cancel button, defaults to None.
		:return: ReturnCode.OK if OK is pressed, ReturnCode.CANCEL if Cancel is pressed.
		"""

		def impl():
			return (
				cls(parent, message, caption, buttons=None)
				.addOkButton(label=okLabel)
				.addCancelButton(label=cancelLabel)
				.ShowModal()
			)

		return wxCallOnMain(impl)  # type: ignore

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

		:param message: The message to be displayed in the dialog.
		:param caption: The title of the dialog window, defaults to wx.MessageBoxCaptionStr.
		:param parent: The parent window for the dialog, defaults to None.
		:param yesLabel: Override for the label of the Yes button, defaults to None.
		:param noLabel: Override for the label of the No button, defaults to None.
		:param cancelLabel: Override for the label of the Cancel button, defaults to None.
		:return: ReturnCode.YES, ReturnCode.NO or ReturnCode.CANCEL, according to the user's action.
		"""

		def impl():
			return (
				cls(parent, message, caption, buttons=None)
				.addYesButton(label=yesLabel)
				.addNoButton(label=noLabel)
				.addCancelButton(label=cancelLabel)
				.ShowModal()
			)

		return wxCallOnMain(impl)  # type: ignore

	# endregion

	# region Methods for subclasses
	def _addButtons(self, buttonHelper: guiHelper.ButtonHelper) -> None:
		"""Adds additional buttons to the dialog, before any other buttons are added.
		Subclasses may implement this method.
		"""

	def _addContents(self, contentsSizer: guiHelper.BoxSizerHelper) -> None:
		"""Adds additional contents  to the dialog, before the buttons.
		Subclasses may implement this method.
		"""

	# endregion

	# region Internal API
	def _checkShowable(self, *, checkMainThread: bool | None = None, checkButtons: bool | None = None):
		"""Checks that must pass in order to show a Message Dialog.

		If any of the specified tests fails, an appropriate exception will be raised.

		:param checkMainThread: Whether to check that we're running on the GUI thread, defaults to True
		:param checkButtons: Whether to check there is at least one command registered, defaults to True
		:raises RuntimeError: If the main thread check fails.
		:raises RuntimeError: If the button check fails.
		"""
		self._checkMainThread(checkMainThread)
		self._checkHasButtons(checkButtons)

	def _checkHasButtons(self, check: bool | None = None):
		if check is None:
			check = self._FAIL_ON_NO_BUTTONS
		if check and not self.GetMainButtonIds():
			raise RuntimeError("MessageDialogs cannot be shown without buttons.")

	@classmethod
	def _checkMainThread(cls, check: bool | None = None):
		if check is None:
			check = cls._FAIL_ON_NONMAIN_THREAD
		if check and not wx.IsMainThread():
			raise RuntimeError("Message dialogs can only be used from the main thread.")

	def _realize_layout(self) -> None:
		if self._isLayoutFullyRealized:
			return
		if gui._isDebug():
			startTime = time.time()
			log.debug("Laying out message dialog")
		self._mainSizer.Fit(self)
		from gui import mainFrame

		if self.Parent == mainFrame:
			# NVDA's main frame is not visible on screen, so centre on screen rather than on `mainFrame` to avoid the dialog appearing at the top left of the screen.
			self.CentreOnScreen()
		else:
			self.CentreOnParent()
		self._isLayoutFullyRealized = True
		if gui._isDebug():
			log.debug(f"Layout completed in {time.time() - startTime:.3f} seconds")

	def _getFallbackAction(self) -> tuple[int, _Command | None]:
		"""Get the fallback action of this dialog.

		:raises RuntimeError: If attempting to get the default command from commands fails.
		:return: The id and command of the fallback action.
		"""
		escapeId = self.GetEscapeId()
		if escapeId == EscapeCode.NONE:
			return escapeId, None
		elif escapeId == EscapeCode.DEFAULT:
			affirmativeAction: _Command | None = None
			affirmativeId: int = self.GetAffirmativeId()
			for id, command in self._commands.items():
				if id == ReturnCode.CANCEL:
					return id, command
				elif id == affirmativeId:
					affirmativeAction = command
			if affirmativeAction is None:
				return EscapeCode.NONE, None
			else:
				return affirmativeId, affirmativeAction
		else:
			try:
				return escapeId, self._commands[escapeId]
			except KeyError:
				raise RuntimeError(
					f"Escape ID {escapeId} is not associated with a command",
				)

	def _getFallbackActionOrFallback(self) -> tuple[int, _Command]:
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

		def getAction() -> tuple[int, _Command]:
			# Try using the developer-specified fallback action.
			try:
				id, action = self._getFallbackAction()
				if action is not None:
					return id, action
			except KeyError:
				log.debug("fallback action was not in commands. This indicates a logic error.")

			# fallback action is unavailable. Try using the default focus instead.
			try:
				if (defaultFocus := self.GetDefaultItem()) is not None:
					id = defaultFocus.GetId()
					return id, self._commands[id]
			except KeyError:
				log.debug("Default focus was not in commands. This indicates a logic error.")

			# Default focus is unavailable. Try using the first registered command that closes the dialog instead.
			firstCommand: tuple[int, _Command] | None = None
			for id, command in self._commands.items():
				if command.closesDialog:
					return id, command
				if firstCommand is None:
					firstCommand = (id, command)
			# No commands that close the dialog have been registered. Use the first command instead.
			if firstCommand is not None:
				return firstCommand
			else:
				log.debug(
					"No commands have been registered. If the dialog is shown, this indicates a logic error.",
				)

			# No commands have been registered. Create one of our own.
			return EscapeCode.NONE, _Command(callback=None, closesDialog=True, ReturnCode=wx.ID_NONE)

		id, command = getAction()
		if not command.closesDialog:
			log.warn(f"Overriding command for {id=} to close dialog.")
			command = command._replace(closesDialog=True)
		return id, command

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

	def _onDialogActivated(self, evt: wx.ActivateEvent):
		evt.Skip()

	def _onShowEvt(self, evt: wx.ShowEvent):
		if evt.IsShown():
			self._playSound()
			if (defaultItem := self.GetDefaultItem()) is not None:
				defaultItem.SetFocus()
		evt.Skip()

	def _onCloseEvent(self, evt: wx.CloseEvent):
		if not evt.CanVeto():
			# We must close the dialog, regardless of state.
			self.Hide()
			self._execute_command(*self._getFallbackActionOrFallback())
			self._instances.remove(self)
			self.EndModal(self.GetReturnCode())
			self.Destroy()
			return
		if self.GetReturnCode() == 0:
			# No button has been pressed, so this must be a close event from elsewhere.
			id, command = self._getFallbackAction()
			if id == EscapeCode.NONE or command is None or not command.closesDialog:
				evt.Veto()
				return
			self.Hide()
			self._execute_command(id, command, _canCallClose=False)
		self.Hide()
		if self.IsModal():
			self.EndModal(self.GetReturnCode())
		log.debug("Queueing destroy")
		self.DestroyLater()
		log.debug("Removing from instances")
		self._instances.remove(self)

	def _onButton(self, evt: wx.CommandEvent):
		id = evt.GetId()
		log.debug(f"Got button event on {id=}")
		try:
			self._execute_command(id)
		except KeyError:
			log.debug(f"No command registered for {id=}.")

	def _execute_command(
		self,
		id: int,
		command: _Command | None = None,
		*,
		_canCallClose: bool = True,
	):
		"""Execute a command on this dialog.

		:param id: ID of the command to execute.
		:param command: Command to execute, defaults to None
			If None, the command to execute will be looked up in the dialog's registered commands.
		:param _canCallClose: Whether or not to close the dialog if the command says to, defaults to True
			Set to False when calling from a close handler.
		"""
		if command is None:
			command = self._commands[id]
		callback, close, returnCode = command
		close &= _canCallClose
		if callback is not None:
			if close:
				self.Hide()
			callback()
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
	:param parent: Parent of the dialog. If None, `gui.mainFrame` will be used.
	:raises Exception: Any exception raised by attempting to create a message box.
	:return: See :fun:`wx.MessageBox`.
	"""
	dialog = MessageDialog(
		parent=parent,
		message=message,
		title=caption,
		dialogType=_messageBoxIconStylesToMessageDialogType(style),
		buttons=_MessageBoxButtonStylesToMessageDialogButtons(style),
	)
	return _messageDialogReturnCodeToMessageBoxReturnCode(dialog.ShowModal())


def _messageDialogReturnCodeToMessageBoxReturnCode(returnCode: ReturnCode) -> int:
	"""Map from an instance of :class:`ReturnCode` to an int as returned by :fun:`wx.MessageBox`.

	Note that only YES, NO, OK, CANCEL and HELP returns are supported by :fun:`wx.MessageBox`, and thus by this function.`

	:param returnCode: Return from :class:`MessageDialog`.
	:raises ValueError: If the return code is not supported by :fun:`wx.MessageBox`.
	:return: Integer as would be returned by :fun:`wx.MessageBox`.
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

	Note that this may not be a one-to-one correspondance, as not all icon styles supported by :fun:`wx.MessageBox` are associated with a :class:`DialogType`.

	:param flags: Style flags.
	:return: Corresponding dialog type.
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


def _MessageBoxButtonStylesToMessageDialogButtons(flags: int) -> tuple[Button, ...]:
	"""Map from a bitmask of styles as expected by :fun:`wx.MessageBox` to a list of :class:`Button`s.

	Note that :fun:`wx.MessageBox` only supports YES, NO, OK, CANCEL and HELP buttons, so this function only supports those buttons too.
	Providing other buttons will fail silently.

	Note that providing `wx.CANCEL_DEFAULT` without `wx.CANCEL`, or `wx.NO_DEFAULT` without `wx.NO` is invalid.
	Wx will raise an assertion error about this, but wxPython will still create the dialog.
	Providing these invalid combinations to this function fails silently.

	This function will always return a tuple of at least one button, typically an OK button.

	:param flags: Style flags.
	:return: Tuple of :class:`Button` instances.
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
