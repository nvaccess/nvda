# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from enum import Enum, IntEnum, auto
from typing import Any, Callable
import winsound

import wx

from .contextHelp import ContextHelpMixin
from .dpiScalingHelper import DpiScalingHelperMixinWithoutInit
from .guiHelper import SIPABCMeta
from gui import guiHelper


class MessageDialogReturnCode(IntEnum):
	OK = wx.OK
	YES = wx.YES
	NO = wx.NO
	CANCEL = wx.CANCEL


class MessageDialogType(Enum):
	STANDARD = auto()
	WARNING = auto()
	ERROR = auto()

	@property
	def _wxIconId(self) -> int | None:
		match self:
			case self.ERROR:
				return wx.ART_ERROR
			case self.WARNING:
				return wx.ART_WARNING
			case _:
				return None

	@property
	def _windowsSoundId(self) -> int | None:
		match self:
			case self.ERROR:
				return winsound.MB_ICONHAND
			case self.WARNING:
				return winsound.MB_ICONASTERISK
			case _:
				return None


class MessageDialog(DpiScalingHelperMixinWithoutInit, ContextHelpMixin, wx.Dialog, metaclass=SIPABCMeta):
	# def Show(self) -> None:
	# """Show a non-blocking dialog.
	# Attach buttons with button handlers"""
	# pass

	# def defaultAction(self) -> None:
	# return None

	@staticmethod
	def CloseInstances() -> None:
		"""Close all dialogs with a default action"""
		pass

	@staticmethod
	def BlockingInstancesExist() -> bool:
		"""Check if dialogs are open without a default return code
		(eg Show without `self._defaultReturnCode`, or ShowModal without `wx.CANCEL`)"""
		pass

	@staticmethod
	def FocusBlockingInstances() -> None:
		"""Raise and focus open dialogs without a default return code
		(eg Show without `self._defaultReturnCode`, or ShowModal without `wx.CANCEL`)"""
		pass

	def _addButtons(self, buttonHelper):
		"""Adds ok / cancel buttons. Can be overridden to provide alternative functionality."""
		# ok = buttonHelper.addButton(
		# self,
		# id=wx.ID_OK,
		# Translators: An ok button on a message dialog.
		# label=_("OK"),
		# )
		# ok.SetDefault()
		# ok.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.OK))

		# cancel = buttonHelper.addButton(
		# self,
		# id=wx.ID_CANCEL,
		# Translators: A cancel button on a message dialog.
		# label=_("Cancel"),
		# )
		# cancel.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.CANCEL))
		# cancel.SetDefault()
		# self.SetDefaultItem(cancel)
		self.addOkButton()
		self.addCancelButton()

	def _addContents(self, contentsSizer: guiHelper.BoxSizerHelper):
		"""Adds additional contents  to the dialog, before the buttons.
		Subclasses may implement this method.
		"""

	def __setIcon(self, type: MessageDialogType):
		if (iconID := type._wxIconId) is not None:
			icon = wx.ArtProvider.GetIconBundle(iconID, client=wx.ART_MESSAGE_BOX)
			self.SetIcons(icon)

	def __setSound(self, type: MessageDialogType):
		self.__soundID = type._windowsSoundId

	def __playSound(self):
		if self.__soundID is not None:
			winsound.MessageBeep(self.__soundID)

	def __init__(
		self,
		parent: wx.Window | None,
		message: str,
		title: str = wx.MessageBoxCaptionStr,
		dialogType: MessageDialogType = MessageDialogType.STANDARD,
	):
		super().__init__(parent, title=title)

		self.__setIcon(dialogType)
		self.__setSound(dialogType)
		self.Bind(wx.EVT_SHOW, self._onShowEvt, source=self)
		self.Bind(wx.EVT_ACTIVATE, self._onDialogActivated, source=self)
		self.Bind(wx.EVT_CLOSE, self._onCloseEvent)

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		contentsSizer = guiHelper.BoxSizerHelper(parent=self, orientation=wx.VERTICAL)

		# Use SetLabelText to avoid ampersands being interpreted as accelerators.
		text = wx.StaticText(self)
		text.SetLabelText(message)
		text.Wrap(self.scaleSize(self.GetSize().Width))
		contentsSizer.addItem(text)
		self._addContents(contentsSizer)

		buttonHelper = guiHelper.ButtonHelper(wx.HORIZONTAL)
		self.__buttonHelper = buttonHelper
		self._addButtons(buttonHelper)
		contentsSizer.addDialogDismissButtons(buttonHelper)

		mainSizer.Add(
			contentsSizer.sizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL,
		)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		# Import late to avoid circular import
		from gui import mainFrame

		if parent == mainFrame:
			# NVDA's main frame is not visible on screen, so centre on screen rather than on `mainFrame` to avoid the dialog appearing at the top left of the screen.
			self.CentreOnScreen()
		else:
			self.CentreOnParent()

	def _onDialogActivated(self, evt):
		evt.Skip()

	def _onShowEvt(self, evt: wx.ShowEvent):
		"""
		:type evt: wx.ShowEvent
		"""
		if evt.IsShown():
			self.__playSound()
			if (defaultItem := self.GetDefaultItem()) is not None:
				defaultItem.SetFocus()
		evt.Skip()

	def _onCloseEvent(self, evt: wx.CloseEvent):
		self.Destroy()

	def addButton(
		self,
		*args,
		callback: Callable[[wx.CommandEvent], Any] | None = None,
		default: bool = False,
		**kwargs,
	):
		button = self.__buttonHelper.addButton(*args, **kwargs)
		button.Bind(wx.EVT_BUTTON, callback)
		if default:
			button.SetDefault()
		return self

	def addOkButton(self):
		return self.addButton(
			self,
			id=wx.ID_OK,
			# Translators: An ok button on a message dialog.
			label=_("OK"),
		)

	def addCancelButton(self):
		return self.addButton(
			self,
			id=wx.ID_CANCEL,
			# Translators: A cancel button on a message dialog.
			label=_("Cancel"),
		)
