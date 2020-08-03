# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017-2018 NV Access Limited, Thomas Stivers
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
import os

import gui
import ui
from logHandler import log

def writeRedirect(helpId: str, filePath:str):
	redirect = rf"""
<html><head>
<meta http-equiv="refresh" content="0;url=userGuide.html#{helpId}" />
</head></html>
	"""
	with open(filePath, 'w') as f:
		f.write(redirect)


def showHelp(helpId: str, evt):
	"""Display the corresponding section of the user guide when either the Help
	button in an NVDA dialog is pressed or the F1 key is pressed on a
	recognized control.
	"""
	if not helpId:
		# Translators: Message indicating no context sensitive help is available.
		noHelpMessage = _("No context sensitive help is available here at this time.")
		ui.message(noHelpMessage)
	log.debug(f"Opening help: helpId = {helpId}")

	helpFile = gui.getDocFilePath("userGuide.html")
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
