# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021-2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from functools import wraps

def apply(mainFrame, winUser, wx):
	"""Patch wx.CallAfter to overcome an execution timing issue.

	In wxPython >= 4.1, wx.CallAfter no longer executes callbacks while NVDA's main thread is within
	a popup menu or message box.
	To work around this, monkeypatch wx.CallAfter to
	post a WM_NULL message to our top-level window after calling the original CallAfter,
	which causes wx's event loop to wake up enough to execute the callback.
	"""
	old_wx_CallAfter = wx.CallAfter

	@wraps(wx.CallAfter)
	def wx_CallAfter_wrapper(func, *args, **kwargs):
		old_wx_CallAfter(func, *args, **kwargs)
		# mainFrame may be None as NVDA could be terminating.
		topHandle = mainFrame.Handle if mainFrame else None
		if topHandle:
			winUser.PostMessage(topHandle, winUser.WM_NULL, 0, 0)

	wx.CallAfter = wx_CallAfter_wrapper
