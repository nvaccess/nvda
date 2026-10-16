# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021-2026 NV Access Limited, Christos Bouronikos
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

	wx runs all pending callbacks once the main thread retrieves any message after a wake-up request,
	so only one WM_NULL needs to be waiting in the queue at a time.
	Posting one per call can fill the main thread's message queue while it is frozen (#20846).
	The WM_NULL is only a wake-up hint, as the callback has already been queued by wx,
	so failing to post it must not make wx.CallAfter fail.
	"""
	old_wx_CallAfter = wx.CallAfter
	isWakeUpPending = False
	isWakeUpFailing = False

	def callAfterCallback(func, /, *args, **kwargs):
		nonlocal isWakeUpPending
		# wx is now running pending callbacks, including any queued after the last WM_NULL was posted.
		isWakeUpPending = False
		return func(*args, **kwargs)

	@wraps(wx.CallAfter)
	def wx_CallAfter_wrapper(func, /, *args, **kwargs):
		nonlocal isWakeUpPending, isWakeUpFailing
		old_wx_CallAfter(callAfterCallback, func, *args, **kwargs)
		# mainFrame may be None as NVDA could be terminating.
		topHandle = mainFrame.Handle if mainFrame else None
		if not topHandle or isWakeUpPending:
			return
		isWakeUpPending = True
		try:
			winUser.PostMessage(topHandle, winUser.WM_NULL, 0, 0)
		except OSError as e:
			# Usually the main thread's message queue is full,
			# in which case it already has messages which will wake it up.
			if not isWakeUpFailing:
				isWakeUpFailing = True
				from logHandler import log

				log.warning(f"Could not post wake-up message to the main thread: {e}")
		else:
			isWakeUpFailing = False

	wx.CallAfter = wx_CallAfter_wrapper
