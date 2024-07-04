# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Mesar Hameed, Joseph Lee,
# Thomas Stivers, Babbage B.V., Accessolutions, Julien Cochuyt
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import threading
from typing import Optional

import wx

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
	"""Display a message dialog.
	Avoid using C{wx.MessageDialog} and C{wx.MessageBox} directly.
	@param message: The message text.
	@param caption: The caption (title) of the dialog.
	@param style: Same as for wx.MessageBox.
	@param parent: The parent window.
	@return: Same as for wx.MessageBox.

	`gui.message.messageBox` is a function which blocks the calling thread,
	until a user responds to the modal dialog.
	This function should be used when an answer is required before proceeding.
	Consider using a custom subclass of a wxDialog if an answer is not required
	or a default answer can be provided.

	It's possible for multiple message boxes to be open at a time.
	Before opening a new messageBox, use `isModalMessageBoxActive`
	to check if another messageBox modal response is still pending.

	Because an answer is required to continue after a modal messageBox is opened,
	some actions such as shutting down are prevented while NVDA is in a possibly uncertain state.
	"""
	from gui import mainFrame
	import core
	from logHandler import log

	global _messageBoxCounter
	with _messageBoxCounterLock:
		_messageBoxCounter += 1

	try:
		if not parent:
			mainFrame.prePopup()
		if not core._hasShutdownBeenTriggered:
			res = wx.MessageBox(message, caption, style, parent or mainFrame)
		else:
			log.debugWarning("Not displaying message box as shutdown has been triggered.", stack_info=True)
			res = wx.ID_CANCEL
	finally:
		if not parent:
			mainFrame.postPopup()
		with _messageBoxCounterLock:
			_messageBoxCounter -= 1

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
