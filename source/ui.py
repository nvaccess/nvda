# -*- coding: utf-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2024 NV Access Limited, James Teh, Dinesh Kaushal, Davy Kager, André-Abush Clause,
# Babbage B.V., Leonard de Ruijter, Michael Curran, Accessolutions, Julien Cochuyt, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""User interface functionality.
This refers to the user interface presented by the screen reader alone, not the graphical user interface.
See L{gui} for the graphical user interface.
"""

import os
from ctypes import (
	windll,
	byref,
	POINTER,
)
import comtypes.client
from comtypes import IUnknown
from comtypes import automation
from comtypes import COMError
from html import escape
from logHandler import log
import gui
import speech
import braille
from config.configFlags import TetherTo
import globalVars
from typing import Optional

from utils.security import isRunningOnSecureDesktop


# From urlmon.h
URL_MK_UNIFORM = 1

# Dialog box properties
DIALOG_OPTIONS = "resizable:yes;help:no"

# dwDialogFlags for ShowHTMLDialogEx from mshtmhst.h
HTMLDLG_NOUI = 0x0010
HTMLDLG_MODAL = 0x0020
HTMLDLG_MODELESS = 0x0040
HTMLDLG_PRINT_TEMPLATE = 0x0080
HTMLDLG_VERIFY = 0x0100


def _warnBrowsableMessageNotAvailableOnSecureScreens(title: str | None = None) -> None:
	"""Warn the user that a browsable message could not be shown on a secure screen (sign-on screen / UAC
	prompt).

	:param title: If provided, the title of the browsable message to give the user more context.
	"""
	log.warning(
		"While on secure screens browsable messages can not be used."
		" The browsable message window creates a security risk."
		f" Attempted to open message with title: {title!r}",
	)

	if not title:
		browsableMessageUnavailableMsg: str = _(
			# Translators: This is the message for a warning shown if NVDA cannot open a browsable message window
			# when Windows is on a secure screen (sign-on screen / UAC prompt).
			"This feature is unavailable while on secure screens such as the sign-on screen or UAC prompt.",
		)
	else:
		browsableMessageUnavailableMsg: str = _(
			# Translators: This is the message for a warning shown if NVDA cannot open a browsable message window
			# when Windows is on a secure screen (sign-on screen / UAC prompt). This prompt includes the title
			# of the Window that could not be opened for context.
			# The {title} will be replaced with the title.
			# The title may be something like "Formatting".
			"This feature ({title}) is unavailable while on secure screens"
			" such as the sign-on screen or UAC prompt.",
		).format(title=title)

	import wx  # Late import to prevent circular dependency.
	import gui  # Late import to prevent circular dependency.

	log.debug("Presenting browsable message unavailable warning.")
	wx.CallAfter(
		gui.messageBox,
		browsableMessageUnavailableMsg,
		# Translators: This is the title for a warning dialog, shown if NVDA cannot open a browsable message.
		caption=_("Feature unavailable."),
		style=wx.ICON_ERROR | wx.OK,
	)


def _warnBrowsableMessageComponentFailure(title: str | None = None) -> None:
	"""Warn the user that a browsable message could not be shown because of a component failure.

	:param title: If provided, the title of the browsable message to give the user more context.
	"""
	log.warning(
		"A browsable message could not be shown because of a component failure."
		f" Attempted to open message with title: {title!r}",
	)

	if not title:
		browsableMessageUnavailableMsg: str = _(
			# Translators: This is the message for a warning shown if NVDA cannot open a browsable message window
			# because of a component failure.
			"An error has caused this feature to be unavailable at this time. "
			"Restarting NVDA or Windows may solve this problem.",
		)
	else:
		browsableMessageUnavailableMsg: str = _(
			# Translators: This is the message for a warning shown if NVDA cannot open a browsable message window
			# because of a component failure. This prompt includes the title
			# of the Window that could not be opened for context.
			# The {title} will be replaced with the title.
			# The title may be something like "Formatting".
			"An error has caused this feature ({title}) to be unavailable at this time. "
			"Restarting NVDA or Windows may solve this problem.",
		).format(title=title)

	log.debug("Presenting browsable message unavailable warning.")
	import wx  # Late import to prevent circular dependency.
	import gui  # Late import to prevent circular dependency.

	wx.CallAfter(
		gui.messageBox,
		browsableMessageUnavailableMsg,
		# Translators: This is the title for a warning dialog, shown if NVDA cannot open a browsable message.
		caption=_("Feature unavailable."),
		style=wx.ICON_ERROR | wx.OK,
	)


def browseableMessage(
	message: str,
	title: str | None = None,
	isHtml: bool = False,
	closeButton: bool = False,
	copyButton: bool = False,
) -> None:
	"""Present a message to the user that can be read in browse mode.
	The message will be presented in an HTML document.

	:param message: The message in either html or text.
	:param title: The title for the message, defaults to "NVDA Message".
	:param isHtml: Whether the message is html, defaults to False.
	:param closeButton: Whether to include a "close" button, defaults to False.
	:param copyButton: Whether to include a "copy" (to clipboard) button, defaults to False.
	"""
	if isRunningOnSecureDesktop():
		_warnBrowsableMessageNotAvailableOnSecureScreens(title)
		return

	htmlFileName = os.path.join(globalVars.appDir, "message.html")
	if not os.path.isfile(htmlFileName):
		_warnBrowsableMessageComponentFailure(title)
		raise LookupError(htmlFileName)

	moniker = POINTER(IUnknown)()
	try:
		windll.urlmon.CreateURLMonikerEx(0, htmlFileName, byref(moniker), URL_MK_UNIFORM)
	except OSError as e:
		log.error(f"OS error during URL moniker creation: {e}")
		_warnBrowsableMessageComponentFailure(title)
		return
	except Exception as e:
		log.error(f"Unexpected error during URL moniker creation: {e}")
		_warnBrowsableMessageComponentFailure(title)
		return

	try:
		d = comtypes.client.CreateObject("Scripting.Dictionary")
	except (COMError, OSError):
		log.error("Scripting.Dictionary component unavailable", exc_info=True)
		_warnBrowsableMessageComponentFailure(title)
		return

	if title is None:
		# Translators: The title for the dialog used to present general NVDA messages in browse mode.
		title = _("NVDA Message")
	d.add("title", title)

	if not isHtml:
		message = f"<pre>{escape(message)}</pre>"
	else:
		log.warning("Passing raw HTML to ui.browseableMessage!")
	d.add("message", message)

	# Translators: A notice to the user that a copy operation succeeded.
	d.add("copySuccessfulAlertText", _("Text copied."))
	# Translators: A notice to the user that a copy operation failed.
	d.add("copyFailedAlertText", _("Couldn't copy to clipboard."))
	if closeButton:
		# Translators: The text of a button which closes the window.
		d.add("closeButtonText", _("Close"))
	if copyButton:
		# Translators: The label of a button to copy the text of the window to the clipboard.
		d.add("copyButtonText", _("Copy"))
		# Translators: A portion of an accessibility label for the "Copy" button,
		# describing the key to press to activate the button. Currently, this key may only be Ctrl+Shift+C.
		# Translation makes sense here if the Control or Shift keys are called something else in a
		# given language; or to set this to the empty string if that key combination is unavailable on some keyboard.
		d.add("copyButtonAcceleratorAccessibilityLabel", _("control+shift+c"))

	dialogArgsVar = automation.VARIANT(d)
	gui.mainFrame.prePopup()
	try:
		windll.mshtml.ShowHTMLDialogEx(
			gui.mainFrame.Handle,
			moniker,
			HTMLDLG_MODELESS,
			byref(dialogArgsVar),
			DIALOG_OPTIONS,
			None,
		)
	except Exception as e:
		log.error(f"Failed to show HTML dialog: {e}")
		_warnBrowsableMessageComponentFailure(title)
		return
	finally:
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
	if braille.handler.shouldAutoTether or braille.handler.getTether() == TetherTo.REVIEW:
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
	textLength = len(text)
	if textLength < 1024:
		spokenText = text
	else:
		# Translators: Spoken instead of a lengthy text when copied to clipboard.
		spokenText = ngettext("%d character", "%d characters", textLength) % textLength
	message(
		# Translators: Announced when a text has been copied to clipboard.
		# {text} is replaced by the copied text.
		text=_("Copied to clipboard: {text}").format(text=spokenText),
		# Translators: Displayed in braille when a text has been copied to clipboard.
		# {text} is replaced by the copied text.
		brailleText=_("Copied: {text}").format(text=text),
	)
