# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from enum import Enum, IntEnum, auto
import time
from typing import Any, Callable, Deque, Iterable, NamedTuple, TypeAlias, Self
import winsound

import wx

import gui

from .contextHelp import ContextHelpMixin
from .dpiScalingHelper import DpiScalingHelperMixinWithoutInit
from .guiHelper import SIPABCMeta
from gui import guiHelper
from functools import partialmethod, singledispatchmethod
from collections import deque
from logHandler import log


# TODO: Change to type statement when Python 3.12 or later is in use.
MessageDialogCallback: TypeAlias = Callable[[wx.CommandEvent], Any]


class MessageDialogReturnCode(IntEnum):
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


class MessageDialogEscapeCode(IntEnum):
	"""Enumeration of the behavior of the escape key and programmatic attempts to close a c{MessageDialog}."""

	NONE = wx.ID_NONE
	"""The escape key should have no effect, and programatically attempting to close the dialog should fail."""
	DEFAULT = wx.ID_ANY
	"""The Cancel button should be emulated when closing the dialog by any means other than with a button in the dialog. If no Cancel button is present, the affirmative button should be used."""


class MessageDialogType(Enum):
	"""Types of message dialogs.
	These are used to determine the icon and sound to play when the dialog is shown.
	"""

	STANDARD = auto()
	WARNING = auto()
	ERROR = auto()

	@property
	def _wxIconId(self) -> int | None:
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


class MessageDialogButton(NamedTuple):
	"""A button to add to a message dialog."""

	id: MessageDialogReturnCode
	"""The ID to use for this button."""

	label: str
	"""The label to display on the button."""

	callback: MessageDialogCallback | None = None
	"""The callback to call when the button is clicked."""

	default_focus: bool = False
	"""Whether this button should be the default button."""

	default_action: bool = False
	"""Whether this button is the default action. That is, whether pressing escape, the system close button, or programatically closing the dialog, should simulate pressing this button."""

	closes_dialog: bool = True
	"""Whether this button should close the dialog when clicked."""


class DefaultMessageDialogButton(MessageDialogButton, Enum):
	"""Default buttons for message dialogs."""

	# Translators: An ok button on a message dialog.
	OK = MessageDialogButton(id=MessageDialogReturnCode.OK, label=_("OK"), default_focus=True)
	# Translators: A yes button on a message dialog.
	YES = MessageDialogButton(id=MessageDialogReturnCode.YES, label=_("&Yes"), default_focus=True)
	# Translators: A no button on a message dialog.
	NO = MessageDialogButton(id=MessageDialogReturnCode.NO, label=_("&No"))
	# Translators: A cancel button on a message dialog.
	CANCEL = MessageDialogButton(id=MessageDialogReturnCode.CANCEL, label=_("Cancel"))
	# Translators: A save button on a message dialog.
	SAVE = MessageDialogButton(id=MessageDialogReturnCode.SAVE, label=_("&Save"))
	# Translators: An apply button on a message dialog.
	APPLY = MessageDialogButton(id=MessageDialogReturnCode.APPLY, label=_("&Apply"))
	# Translators: A close button on a message dialog.
	CLOSE = MessageDialogButton(id=MessageDialogReturnCode.CLOSE, label=_("Close"))
	# Translators: A help button on a message dialog.
	HELP = MessageDialogButton(id=MessageDialogReturnCode.HELP, label=_("Help"))


class DefaultMessageDialogButtons(tuple[DefaultMessageDialogButton], Enum):
	OK_CANCEL = (
		DefaultMessageDialogButton.OK,
		DefaultMessageDialogButton.CANCEL,
	)
	YES_NO = (
		DefaultMessageDialogButton.YES,
		DefaultMessageDialogButton.NO,
	)
	YES_NO_CANCEL = (
		DefaultMessageDialogButton.YES,
		DefaultMessageDialogButton.NO,
		DefaultMessageDialogButton.CANCEL,
	)
	SAVE_NO_CANCEL = (
		DefaultMessageDialogButton.SAVE,
		# Translators: A don't save button on a message dialog.
		DefaultMessageDialogButton.NO._replace(label=_("Do&n't save")),
		DefaultMessageDialogButton.CANCEL,
	)


class _MessageDialogCommand(NamedTuple):
	"""Internal representation of a command for a message dialog."""

	callback: MessageDialogCallback | None = None
	"""The callback function to be executed. Defaults to None."""
	closes_dialog: bool = True
	"""Indicates whether the dialog should be closed after the command is executed. Defaults to True."""


class MessageDialog(DpiScalingHelperMixinWithoutInit, ContextHelpMixin, wx.Dialog, metaclass=SIPABCMeta):
	_instances: Deque["MessageDialog"] = deque()

	# region Constructors
	def __init__(
		self,
		parent: wx.Window | None,
		message: str,
		title: str = wx.MessageBoxCaptionStr,
		dialogType: MessageDialogType = MessageDialogType.STANDARD,
		*,
		buttons: Iterable[MessageDialogButton] | None = (DefaultMessageDialogButton.OK,),
		helpId: str = "",
	):
		self.helpId = helpId
		super().__init__(parent, title=title)
		self.__isLayoutFullyRealized = False
		self._commands: dict[int, _MessageDialogCommand] = {}
		self._defaultReturnCode: MessageDialogReturnCode | None = None

		self.__setIcon(dialogType)
		self.__setSound(dialogType)
		self.Bind(wx.EVT_SHOW, self._onShowEvt, source=self)
		self.Bind(wx.EVT_ACTIVATE, self._onDialogActivated, source=self)
		self.Bind(wx.EVT_CLOSE, self._onCloseEvent)
		self.Bind(wx.EVT_BUTTON, self._onButton)

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		contentsSizer = guiHelper.BoxSizerHelper(parent=self, orientation=wx.VERTICAL)
		self.__contentsSizer = contentsSizer
		self.__mainSizer = mainSizer

		# Use SetLabelText to avoid ampersands being interpreted as accelerators.
		text = wx.StaticText(self)
		text.SetLabelText(message)
		text.Wrap(self.scaleSize(self.GetSize().Width))
		contentsSizer.addItem(text)
		self._addContents(contentsSizer)

		buttonHelper = guiHelper.ButtonHelper(wx.HORIZONTAL)
		contentsSizer.addDialogDismissButtons(buttonHelper)
		self.__buttonHelper = buttonHelper
		self._addButtons(buttonHelper)
		if buttons is not None:
			self.addButtons(*buttons)

		mainSizer.Add(
			contentsSizer.sizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL,
		)
		# mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		# Import late to avoid circular import
		from gui import mainFrame

		if parent == mainFrame:
			# NVDA's main frame is not visible on screen, so centre on screen rather than on `mainFrame` to avoid the dialog appearing at the top left of the screen.
			self.CentreOnScreen()
		else:
			self.CentreOnParent()

	# endregion

	# region Public object API
	@singledispatchmethod
	def addButton(
		self,
		*args,
		callback: Callable[[wx.CommandEvent], Any] | None = None,
		default_focus: bool = False,
		default_action: bool = False,
		closes_dialog: bool = True,
		**kwargs,
	) -> Self:
		"""Add a button to the dialog.

		Any additional arguments are passed to `ButtonHelper.addButton`.

		:param callback: Function to call when the button is pressed, defaults to None.
		:param default_focus: Whether the button should be the default (first focused) button in the dialog, defaults to False.
		:param closes_dialog: Whether the button should close the dialog when pressed, defaults to True.
			If multiple buttons with `default=True` are added, the last one added will be the default button.
		:return: The dialog instance.
		"""
		button = self.__buttonHelper.addButton(*args, **kwargs)
		# Get the ID from the button instance in case it was created with id=wx.ID_ANY.
		buttonId = button.GetId()
		self.AddMainButtonId(buttonId)
		self._commands[buttonId] = _MessageDialogCommand(callback=callback, closes_dialog=closes_dialog)
		if default_focus:
			button.SetDefault()
		if default_action:
			self.SetEscapeId(buttonId)
		self.__isLayoutFullyRealized = False
		return self

	@addButton.register
	def _(
		self,
		button: MessageDialogButton,
		*args,
		callback: Callable[[wx.CommandEvent], Any] | None = None,
		default_focus: bool | None = None,
		closes_dialog: bool | None = None,
		**kwargs,
	) -> Self:
		"""Add a c{MessageDialogButton} to the dialog.

		:param button: The button to add.
		:param callback: Override for the callback specified in `button`, defaults to None.
		:param default_focus: Override for the default specified in `button`, defaults to None.
			If multiple buttons with `default=True` are added, the last one added will be the default button.
		:param closes_dialog: Override for `button`'s `closes_dialog` property, defaults to None.
		:return: The dialog instance.
		"""
		keywords = button._asdict()
		if default_focus is not None:
			keywords["default_focus"] = default_focus
		if callback is not None:
			keywords["callback"] = callback
		if closes_dialog is not None:
			keywords["closes_dialog"] = closes_dialog
		keywords.update(kwargs)
		return self.addButton(self, *args, **keywords)

	addOkButton = partialmethod(addButton, DefaultMessageDialogButton.OK)
	addOkButton.__doc__ = "Add an OK button to the dialog."
	addCancelButton = partialmethod(addButton, DefaultMessageDialogButton.CANCEL)
	addCancelButton.__doc__ = "Add a Cancel button to the dialog."
	addYesButton = partialmethod(addButton, DefaultMessageDialogButton.YES)
	addYesButton.__doc__ = "Add a Yes button to the dialog."
	addNoButton = partialmethod(addButton, DefaultMessageDialogButton.NO)
	addNoButton.__doc__ = "Add a No button to the dialog."
	addSaveButton = partialmethod(addButton, DefaultMessageDialogButton.SAVE)
	addSaveButton.__doc__ = "Add a Save button to the dialog."
	addApplyButton = partialmethod(addButton, DefaultMessageDialogButton.APPLY)
	addApplyButton.__doc__ = "Add an Apply button to the dialog."
	addCloseButton = partialmethod(addButton, DefaultMessageDialogButton.CLOSE)
	addCloseButton.__doc__ = "Add a Close button to the dialog."
	addHelpButton = partialmethod(addButton, DefaultMessageDialogButton.HELP)
	addHelpButton.__doc__ = "Add a Help button to the dialog."

	def addButtons(self, *buttons: Iterable[MessageDialogButton]) -> Self:
		"""Add multiple buttons to the dialog.

		:return: The dialog instance.
		"""

		for button in buttons:
			self.addButton(button)
		return self

	def Show(self) -> bool:
		"""Show a non-blocking dialog.
		Attach buttons with button handlers"""
		if not self.GetMainButtonIds():
			raise RuntimeError("MessageDialogs cannot be shown without buttons.")
		self._realize_layout()
		log.debug("Showing")
		ret = super().Show()
		if ret:
			log.debug("Adding to instances")
			self._instances.append(self)
		return ret

	def ShowModal(self) -> MessageDialogReturnCode:
		"""Show a blocking dialog.
		Attach buttons with button handlers"""
		if not self.GetMainButtonIds():
			raise RuntimeError("MessageDialogs cannot be shown without buttons.")
		self._realize_layout()
		self.__ShowModal = self.ShowModal
		self.ShowModal = super().ShowModal
		from .message import displayDialogAsModal

		log.debug("Adding to instances")
		self._instances.append(self)
		log.debug("Showing modal")
		ret = displayDialogAsModal(self)
		self.ShowModal = self.__ShowModal
		return MessageDialogReturnCode(ret)

	@property
	def isBlocking(self) -> bool:
		"""Whether or not the dialog is blocking"""
		return self.IsModal() and self._defaultReturnCode is None

	# endregion

	# region Public class methods
	@classmethod
	def CloseInstances(cls) -> None:
		"""Close all dialogs with a default action"""
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
		for dialog in cls._instances:
			if dialog.isBlocking:
				dialog.Raise()
				dialog.SetFocus()
				break

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
	def _realize_layout(self) -> None:
		if self.__isLayoutFullyRealized:
			return
		if gui._isDebug():
			startTime = time.time()
			log.debug("Laying out message dialog")
		self.__mainSizer.Fit(self)
		self.__isLayoutFullyRealized = True
		if gui._isDebug():
			log.debug(f"Layout completed in {time.time() - startTime:.3f} seconds")

	@property
	def _defaultAction(self) -> MessageDialogCallback | None:
		if (defaultReturnCode := self._defaultReturnCode) is not None:
			try:
				return self._commands[defaultReturnCode]
			except KeyError:
				raise RuntimeError(
					f"Default return code {defaultReturnCode} is not associated with a callback",
				)
		return None

	def __setIcon(self, type: MessageDialogType) -> None:
		if (iconID := type._wxIconId) is not None:
			icon = wx.ArtProvider.GetIconBundle(iconID, client=wx.ART_MESSAGE_BOX)
			self.SetIcons(icon)

	def __setSound(self, type: MessageDialogType) -> None:
		self.__soundID = type._windowsSoundId

	def __playSound(self) -> None:
		if self.__soundID is not None:
			winsound.MessageBeep(self.__soundID)

	def _onDialogActivated(self, evt: wx.ActivateEvent):
		evt.Skip()

	def _onShowEvt(self, evt: wx.ShowEvent):
		if evt.IsShown():
			self.__playSound()
			if (defaultItem := self.GetDefaultItem()) is not None:
				defaultItem.SetFocus()
		evt.Skip()

	def _onCloseEvent(self, evt: wx.CloseEvent):
		self.Hide()
		if self.IsModal():
			self.EndModal(self.GetReturnCode())
		log.debug("Queueing destroy")
		self.DestroyLater()
		log.debug("Removing from instances")
		self._instances.remove(self)

	def _onButton(self, evt: wx.CommandEvent):
		id = evt.GetId()
		command = self._commands.get(id)
		if command is None:
			return
		callback, close = command
		if callback is not None:
			if close:
				self.Hide()
			callback(evt)
		if close:
			closeEvent = wx.PyEvent(0, wx.EVT_CLOSE.typeId)
			closeEvent.SetEventObject(evt.GetEventObject())
			self.SetReturnCode(id)
			self.GetEventHandler().QueueEvent(closeEvent)

	# endregion
