# -*- coding: utf-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2020 NV Access Limited, James Teh, Dinesh Kaushal, Davy Kager, André-Abush Clause,
# Babbage B.V., Leonard de Ruijter, Michael Curran, Accessolutions, Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""User interface functionality.
This refers to the user interface presented by the screen reader alone, not the graphical user interface.
See L{gui} for the graphical user interface.
"""

import os
import sys
from ctypes import windll, byref, POINTER, addressof
from comtypes import IUnknown
from comtypes import automation 
from html import escape
from logHandler import log
import gui
import speech
import braille
import globalVars
from typing import Optional


# From urlmon.h
URL_MK_UNIFORM = 1

# Dialog box properties
DIALOG_OPTIONS = "resizable:yes;help:no"

#dwDialogFlags for ShowHTMLDialogEx from mshtmhst.h
HTMLDLG_NOUI = 0x0010 
HTMLDLG_MODAL = 0x0020 
HTMLDLG_MODELESS = 0x0040 
HTMLDLG_PRINT_TEMPLATE = 0x0080 
HTMLDLG_VERIFY = 0x0100 


def browseableMessage(message,title=None,isHtml=False):
	"""Present a message to the user that can be read in browse mode.
	The message will be presented in an HTML document.
	@param message: The message in either html or text.
	@type message: str
	@param title: The title for the message.
	@type title: str
	@param isHtml: Whether the message is html
	@type isHtml: boolean
	"""
	htmlFileName = os.path.join(globalVars.appDir, 'message.html')
	if not os.path.isfile(htmlFileName ): 
		raise LookupError(htmlFileName )
	moniker = POINTER(IUnknown)()
	windll.urlmon.CreateURLMonikerEx(0, htmlFileName, byref(moniker), URL_MK_UNIFORM)
	if not title:
		# Translators: The title for the dialog used to present general NVDA messages in browse mode.
		title = _("NVDA Message")
	if not isHtml:
		message = f"<pre>{escape(message)}</pre>"
	dialogString = f"{title};{message}"
	dialogArguements = automation.VARIANT( dialogString )
	gui.mainFrame.prePopup() 
	windll.mshtml.ShowHTMLDialogEx( 
		gui.mainFrame.Handle , 
		moniker , 
		HTMLDLG_MODELESS , 
		addressof( dialogArguements ) , 
		DIALOG_OPTIONS, 
		None
	)
	gui.mainFrame.postPopup() 


def message(
		text: str,
		speechPriority: Optional[speech.Spri] = None,
		brailleText: Optional[str] = None,
):
	"""Present a message to the user.
	The message will be presented in both speech and braille.
	@param text: The text of the message.
	@param speechPriority: The speech priority.
	@param brailleText: If specified, present this alternative text on the braille display.
	"""
	speech.speakMessage(text, priority=speechPriority)
	braille.handler.message(brailleText if brailleText is not None else text)


def reviewMessage(text: str, speechPriority: Optional[speech.Spri] = None):
	"""Present a message from review or object navigation to the user.
	The message will always be presented in speech, and also in braille if it is tethered to review or when auto tethering is on.
	@param text: The text of the message.
	@param speechPriority: The speech priority.
	"""
	speech.speakMessage(text, priority=speechPriority)
	if braille.handler.shouldAutoTether or braille.handler.getTether() == braille.handler.TETHER_REVIEW:
		braille.handler.message(text)


def reportTextCopiedToClipboard(text: Optional[str] = None):
	"""Notify about the result of a "Copy to clipboard" operation.
	@param text: The text that has been copied. Set to `None` to notify of a failed operation.
	See: `api.copyToClip`
	"""
	if not text:
		# Translators: Presented when unable to copy to the clipboard because of an error
		# or the clipboard content did not match what was just copied.
		message(_("Unable to copy"))
		return
	# Depending on the speech synthesizer, large amount of spoken text can freeze NVDA (#11843)
	if len(text) < 1024:
		spokenText = text
	else:
		# Translators: Spoken instead of a lengthy text when copied to clipboard.
		spokenText = _("%d characters") % len(text)
	message(
		# Translators: Announced when a text has been copied to clipboard.
		# {text} is replaced by the copied text.
		text=_("Copied to clipboard: {text}").format(text=spokenText),
		# Translators: Displayed in braille when a text has been copied to clipboard.
		# {text} is replaced by the copied text.
		brailleText=_("Copied: {text}").format(text=text)
	)
