# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2021 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Mesar Hameed, Joseph Lee,
# Thomas Stivers, Babbage B.V., Accessolutions, Julien Cochuyt
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import threading
from typing import Optional
import wx

_messageBoxCounterLock = threading.Lock()
_messageBoxCounter = 0


def isInMessageBox() -> bool:
	return _messageBoxCounter != 0


def messageBox(
		message: str,
		caption: str = wx.MessageBoxCaptionStr,
		style: int = wx.OK | wx.CENTER,
		parent: Optional[wx.Window] = None
) -> int:
	"""Display a message dialog.
	This should be used for all message dialogs
	rather than using C{wx.MessageDialog} and C{wx.MessageBox} directly.
	@param message: The message text.
	@param caption: The caption (title) of the dialog.
	@param style: Same as for wx.MessageBox.
	@param parent: The parent window.
	@return: Same as for wx.MessageBox.
	"""
	from gui import mainFrame
	global _messageBoxCounter
	with _messageBoxCounterLock:
		_messageBoxCounter += 1
	try:
		if not parent:
			mainFrame.prePopup()
		res = wx.MessageBox(message, caption, style, parent or mainFrame)
		if not parent:
			mainFrame.postPopup()
	finally:
		with _messageBoxCounterLock:
			_messageBoxCounter -= 1
	return res
