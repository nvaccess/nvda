# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017-2018 NV Access Limited, Thomas Stivers
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
import os

import gui
import ui
import wx
from logHandler import log




def showHelp(helpId: str, evt):
	"""Display the corresponding section of the user guide when either the Help
	button in an NVDA dialog is pressed or the F1 key is pressed on a
	recognized control.
	"""
	if not helpId:
		# Translators: Message indicating no context sensitive help is available.
		noHelpMessage = _("No context sensitive help is available here at this time.")
		ui.browseableMessage(noHelpMessage)

	helpFile = gui.getDocFilePath("userGuide.html")
	window = evt.GetEventObject()
	windowId = window.GetId()
	helpText = window.GetHelpText()
	label = window.GetLabel()
	log.debug(
		"Opening help:"
		f"helpId = {helpId}"
		f"\nwindowId = {windowId}"
		f"\nlabel = {label}"
	)

	# Translators: The title for an NVDA help window.
	helpTitle = _("NVDA Help")
	try:
		os.startfile(f"file://{helpFile}#{helpId}")
	except KeyError as e:
		ui.browseableMessage(str(e), helpTitle, True)
