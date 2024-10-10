# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from enum import Enum, IntEnum, auto
import time
from typing import Any, Callable, Deque, Iterable, NamedTuple, TypeAlias
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

	default: bool = False
	"""Whether this button should be the default button."""

	closes_dialog: bool = True
	"""Whether this button should close the dialog when clicked."""


class DefaultMessageDialogButtons(MessageDialogButton, Enum):
	"""Default buttons for message dialogs."""

	# Translators: An ok button on a message dialog.
	OK = MessageDialogButton(id=MessageDialogReturnCode.OK, label=_("OK"), default=True)
	# Translators: A yes button on a message dialog.
	YES = MessageDialogButton(id=MessageDialogReturnCode.YES, label=_("&Yes"), default=True)
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


class _MessageDialogCommand(NamedTuple):
	callback: MessageDialogCallback | None = None
	closes_dialog: bool = True


class MessageDialog(DpiScalingHelperMixinWithoutInit, ContextHelpMixin, wx.Dialog, metaclass=SIPABCMeta):
	_instances: Deque["MessageDialog"] = deque()

	# region Constructors
	def __init__(
		self,
		parent: wx.Window | None,
		message: str,
		title: str = wx.MessageBoxCaptionStr,
		dialogType: MessageDialogType = MessageDialogType.STANDARD,
	):
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
		default: bool = False,
		closes_dialog: bool = True,
		**kwargs,
	):
		"""Add a button to the dialog.

		Any additional arguments are passed to `ButtonHelper.addButton`.

		:param callback: Function to call when the button is pressed, defaults to None.
		:param default: Whether the button should be the default (first focused) button in the dialog, defaults to False.
		:param closes_dialog: Whether the button should close the dialog when pressed, defaults to True.
			If multiple buttons with `default=True` are added, the last one added will be the default button.
		:return: The dialog instance.
		"""
		button = self.__buttonHelper.addButton(*args, **kwargs)
		# Get the ID from the button instance in case it was created with id=wx.ID_ANY.
		self._commands[button.GetId()] = _MessageDialogCommand(callback=callback, closes_dialog=closes_dialog)
		if default:
			button.SetDefault()
		self.__isLayoutFullyRealized = False
		return self

	@addButton.register
	def _(
		self,
		button: MessageDialogButton,
		*args,
		callback: Callable[[wx.CommandEvent], Any] | None = None,
		default: bool | None = None,
		closes_dialog: bool | None = None,
		**kwargs,
	):
		"""Add a c{MessageDialogButton} to the dialog.

		:param button: The button to add.
		:param callback: Override for the callback specified in `button`, defaults to None.
		:param default: Override for the default specified in `button`, defaults to None.
			If multiple buttons with `default=True` are added, the last one added will be the default button.
		:param closes_dialog: Override for `button`'s `closes_dialog` property, defaults to None.
		:return: The dialog instance.
		"""
		keywords = button._asdict()
		if default is not None:
			keywords["default"] = default
		if callback is not None:
			keywords["callback"] = callback
		if closes_dialog is not None:
			keywords["closes_dialog"] = closes_dialog
		keywords.update(kwargs)
		return self.addButton(self, *args, **keywords)

	addOkButton = partialmethod(addButton, DefaultMessageDialogButtons.OK)
	addOkButton.__doc__ = "Add an OK button to the dialog."
	addCancelButton = partialmethod(addButton, DefaultMessageDialogButtons.CANCEL)
	addCancelButton.__doc__ = "Add a Cancel button to the dialog."
	addYesButton = partialmethod(addButton, DefaultMessageDialogButtons.YES)
	addYesButton.__doc__ = "Add a Yes button to the dialog."
	addNoButton = partialmethod(addButton, DefaultMessageDialogButtons.NO)
	addNoButton.__doc__ = "Add a No button to the dialog."
	addSaveButton = partialmethod(addButton, DefaultMessageDialogButtons.SAVE)
	addSaveButton.__doc__ = "Add a Save button to the dialog."
	addApplyButton = partialmethod(addButton, DefaultMessageDialogButtons.APPLY)
	addApplyButton.__doc__ = "Add an Apply button to the dialog."
	addCloseButton = partialmethod(addButton, DefaultMessageDialogButtons.CLOSE)
	addCloseButton.__doc__ = "Add a Close button to the dialog."
	addHelpButton = partialmethod(addButton, DefaultMessageDialogButtons.HELP)
	addHelpButton.__doc__ = "Add a Help button to the dialog."

	def addButtons(self, *buttons: Iterable[MessageDialogButton]):
		"""Add multiple buttons to the dialog.

		:return: The dialog instance.
		"""

		for button in buttons:
			self.addButton(button)
		return self

	def Show(self) -> None:
		"""Show a non-blocking dialog.
		Attach buttons with button handlers"""
		self._realize_layout()
		log.debug("Showing")
		super().Show()
		log.debug("Adding to instances")
		self._instances.append(self)

	def ShowModal(self):
		"""Show a blocking dialog.
		Attach buttons with button handlers"""
		self._realize_layout()
		self.__ShowModal = self.ShowModal
		self.ShowModal = super().ShowModal
		from .message import displayDialogAsModal

		log.debug("Adding to instances")
		self._instances.append(self)
		log.debug("Showing modal")
		displayDialogAsModal(self)
		self.ShowModal = self.__ShowModal

	def isBlocking(self) -> bool:
		"""Check if the dialog is blocking"""
		return self.IsModal() and self._defaultReturnCode is None

	# endregion

	# region Public class methods
	@staticmethod
	def CloseInstances() -> None:
		"""Close all dialogs with a default action"""
		pass

	@staticmethod
	def BlockingInstancesExist() -> bool:
		"""Check if dialogs are open without a default return code
		(eg Show without `self._defaultReturnCode`, or ShowModal without `wx.CANCEL`)"""
		return any(dialog.isBlocking() for dialog in MessageDialog._instances)

	@staticmethod
	def FocusBlockingInstances() -> None:
		"""Raise and focus open dialogs without a default return code
		(eg Show without `self._defaultReturnCode`, or ShowModal without `wx.CANCEL`)"""
		for dialog in MessageDialog._instances:
			if dialog.isBlocking():
				dialog.Raise()
				dialog.SetFocus()
				break

	# endregion

	# region Methods for subclasses
	def _addButtons(self, buttonHelper):
		"""Adds additional buttons to the dialog, before any other buttons are added.
		Subclasses may implement this method.
		"""

	def _addContents(self, contentsSizer: guiHelper.BoxSizerHelper):
		"""Adds additional contents  to the dialog, before the buttons.
		Subclasses may implement this method.
		"""

	# endregion

	# region Internal API
	def _realize_layout(self):
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
	def _defaultAction(self) -> MessageDialogCallback:
		if (defaultReturnCode := self._defaultReturnCode) is not None:
			try:
				return self._commands[defaultReturnCode]
			except KeyError:
				raise RuntimeError(
					f"Default return code {defaultReturnCode} is not associated with a callback",
				)
		return None

	def __setIcon(self, type: MessageDialogType):
		if (iconID := type._wxIconId) is not None:
			icon = wx.ArtProvider.GetIconBundle(iconID, client=wx.ART_MESSAGE_BOX)
			self.SetIcons(icon)

	def __setSound(self, type: MessageDialogType):
		self.__soundID = type._windowsSoundId

	def __playSound(self):
		if self.__soundID is not None:
			winsound.MessageBeep(self.__soundID)

	def _onDialogActivated(self, evt):
		evt.Skip()

	def _onShowEvt(self, evt: wx.ShowEvent):
		if evt.IsShown():
			self.__playSound()
			if (defaultItem := self.GetDefaultItem()) is not None:
				defaultItem.SetFocus()
		evt.Skip()

	def _onCloseEvent(self, evt: wx.CloseEvent):
		# log.debug(f"{evt.GetId()=}, {evt.GetEventObject().Label=}")
		# self.GetEscapeId()
		# self._onButton(wx.CommandEvent(wx.wxEVT_BUTTON, self.GetEscapeId()))
		# self.EndModal(0)
		# wx.CallAfter(self.Destroy)
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
