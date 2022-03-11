# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Mesar Hameed, Joseph Lee,
# Thomas Stivers, Babbage B.V., Accessolutions, Julien Cochuyt
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import threading
from typing import Optional
import wx

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


def messageBox(
		message: str,
		caption: str = wx.MessageBoxCaptionStr,
		style: int = wx.OK | wx.CENTER,
		parent: Optional[wx.Window] = None
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
	global _messageBoxCounter
	with _messageBoxCounterLock:
		_messageBoxCounter += 1

	try:
		if not parent:
			mainFrame.prePopup()
		res = wx.MessageBox(message, caption, style, parent or mainFrame)
	finally:
		if not parent:
			mainFrame.postPopup()
		with _messageBoxCounterLock:
			_messageBoxCounter -= 1

	return res
