# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Mesar Hameed, Joseph Lee,
# Thomas Stivers, Babbage B.V., Accessolutions, Julien Cochuyt
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from enum import IntEnum
import threading
from typing import Optional

import wx
import warnings

import extensionPoints

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
	from gui import mainFrame

	global _messageBoxCounter
	with _messageBoxCounterLock:
		_messageBoxCounter += 1

	try:
		if not dialog.GetParent():
			mainFrame.prePopup()
		res = dialog.ShowModal()
	finally:
		if not dialog.GetParent():
			mainFrame.postPopup()
		with _messageBoxCounterLock:
			_messageBoxCounter -= 1

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
		DeprecationWarning(
			"gui.message.messageBox is deprecated. Use gui.message.MessageDialog instead.",
		),
	)
	# Import late to avoid circular import.
	from gui import mainFrame
	from gui.messageDialog import _messageBoxShim
	from gui.guiHelper import wxCallOnMain
	import core
	from logHandler import log

	if not core._hasShutdownBeenTriggered:
		res = wxCallOnMain(_messageBoxShim, message, caption, style, parent=parent or mainFrame)
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
