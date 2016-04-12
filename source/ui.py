#ui.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2008-2016 NV Access Limited, Dinesh Kaushal, Davy Kager
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""User interface functionality.
This refers to the user interface presented by the screen reader alone, not the graphical user interface.
See L{gui} for the graphical user interface.
"""

import os
import sys
from ctypes import windll, byref, POINTER, addressof
from comtypes import IUnknown
from comtypes import automation 
from logHandler import log
import gui
import speech
import braille

# From urlmon.h
URL_MK_UNIFORM = 1

# Dialog box properties
DIALOG_OPTIONS = "dialogWidth:350px;dialogHeight:140px;resizable:yes;center:yes;help:no"

#dwDialogFlags for ShowHTMLDialogEx from mshtmhst.h
HTMLDLG_NOUI = 0x0010 
HTMLDLG_MODAL = 0x0020 
HTMLDLG_MODELESS = 0x0040 
HTMLDLG_PRINT_TEMPLATE = 0x0080 
HTMLDLG_VERIFY = 0x0100 

def browseableMessage(message,title=None , isHtml=False):
	"""Present a message to the user that can be read in browse mode.
	The message will be presented in an HTML document.
	@param message: The message in either html or text.
	@type message: unicode
	@param title: The title for the message.
	@type title: unicode
	@param isHtml: Whether the message is html
	@type isHtml: boolean
	"""
	htmlFileName  = os.path.realpath( 'message.html' )
	if not os.path.isfile(htmlFileName ): 
		raise LookupError(htmlFileName )
	moniker = POINTER(IUnknown)()
	windll.urlmon.CreateURLMonikerEx(0, unicode( htmlFileName ) , byref(moniker), URL_MK_UNIFORM)
	if not title:
		# Translators: The title for the dialog used to present general NVDA messages in browse mode.
		title = _("NVDA Message")
	isHtmlArgument = "true" if isHtml else "false"
	dialogString = u"{isHtml};{title};{message}".format( isHtml = isHtmlArgument , title=title , message=message ) 
	dialogArguements = automation.VARIANT( dialogString )
	gui.mainFrame.prePopup() 
	windll.mshtml.ShowHTMLDialogEx( gui.mainFrame.Handle , moniker , HTMLDLG_MODELESS , addressof( dialogArguements ) , unicode(DIALOG_OPTIONS ), None)
	gui.mainFrame.postPopup() 

def message(text):
	"""Present a message to the user.
	The message will be presented in both speech and braille.
	@param text: The text of the message.
	@type text: str
	"""
	speech.speakMessage(text)
	braille.handler.message(text)

def reviewMessage(text):
	"""Present a message from review or object navigation to the user.
	The message will always be presented in speech, and also in braille if it is tethered to review.
	@param text: The text of the message.
	@type text: str
	"""
	speech.speakMessage(text)
	if braille.handler.tether == braille.handler.TETHER_REVIEW:
		braille.handler.message(text)
