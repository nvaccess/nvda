# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2017-2020 NV Access Limited, Thomas Stivers
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import os
import typing

import gui
import ui
import wx
from logHandler import log


def writeRedirect(helpId: str, filePath: str):
	redirect = rf"""
<html><head>
<meta http-equiv="refresh" content="0;url=userGuide.html#{helpId}" />
</head></html>
	"""
	with open(filePath, 'w') as f:
		f.write(redirect)


def showHelp(helpId: str):
	"""Display the corresponding section of the user guide when either the Help
	button in an NVDA dialog is pressed or the F1 key is pressed on a
	recognized control.
	"""
	if not helpId:
		# Translators: Message indicating no context sensitive help is available.
		noHelpMessage = _("No context sensitive help is available here at this time.")
		ui.message(noHelpMessage)
	helpFile = gui.getDocFilePath("userGuide.html")
	log.debug(f"Opening help: helpId = {helpId}, userGuidePath: {helpFile}")

	contextHelpRedirect = os.path.join(os.path.dirname(helpFile), "contextHelp.html")
	try:
		writeRedirect(helpId, contextHelpRedirect)
	except Exception:
		log.error("Unable to write context help redirect file.", exc_info=True)
		return

	try:
		os.startfile(f"file://{contextHelpRedirect}")
	except Exception:
		log.error("Unable to launch context help.", exc_info=True)


def bindHelpEvent(helpId: str, window: wx.Window):
	window.Unbind(wx.EVT_HELP)
	window.Bind(
		wx.EVT_HELP,
		lambda evt: _onEvtHelp(helpId, evt),
	)
	log.debug(f"did binding for {window.__class__.__qualname__}")


def _onEvtHelp(helpId: str, evt: wx.HelpEvent):
	# Don't call evt.skip. Whe want more specific bindings to override less specific.
	showHelp(helpId)


class ContextHelpMixin:
	def __init__(self, *args, **kwargs):
		log.debug("reef")
		super().__init__(*args, **kwargs)
		helpId = getattr(self, "helpId", None)
		if not helpId or not isinstance(helpId, str):
			log.warning(f"No helpId (or incorrect type) for: {self.__class__.__qualname__}")
			return
		window = typing.cast(wx.Window, self)
		bindHelpEvent(helpId, window)
		log.debug(f"ContextHelpMixin for {self.__class__.__qualname__}")

	def bindHelpEvent(self, helpId: str, window: wx.Window):
		bindHelpEvent(helpId, window)
