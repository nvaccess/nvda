# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, James Teh, Dinesh Kaushal, Davy Kager, André-Abush Clause,
# Babbage B.V., Leonard de Ruijter, Michael Curran, Accessolutions, Julien Cochuyt, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""User interface functionality.
This refers to the user interface presented by the screen reader alone, not the graphical user interface.
See L{gui} for the graphical user interface.
"""

import os
from collections.abc import Callable
from html import escape
from typing import Final

import braille
import core
import globalVars
import gui
import nh3
import speech
import wx
from config.configFlags import TetherTo
from gui.message import HtmlMessageDialog
from logHandler import log
from utils._deprecate import handleDeprecations, RemovedSymbol
from utils.security import isRunningOnSecureDesktop

_COM_HTML_DIALOG_DEPRECATION_MSG = (
	"The COM-based HTML dialog infrastructure has been removed. Use gui.message.HtmlMessageDialog instead."
)

__getattr__ = handleDeprecations(
	# Deprecated in 2026.3, remove in 2027.1
	RemovedSymbol("URL_MK_UNIFORM", 1, message=_COM_HTML_DIALOG_DEPRECATION_MSG),
	RemovedSymbol("DIALOG_OPTIONS", "resizable:yes;help:no", message=_COM_HTML_DIALOG_DEPRECATION_MSG),
	RemovedSymbol("HTMLDLG_NOUI", 0x0010, message=_COM_HTML_DIALOG_DEPRECATION_MSG),
	RemovedSymbol("HTMLDLG_MODAL", 0x0020, message=_COM_HTML_DIALOG_DEPRECATION_MSG),
	RemovedSymbol("HTMLDLG_MODELESS", 0x0040, message=_COM_HTML_DIALOG_DEPRECATION_MSG),
	RemovedSymbol("HTMLDLG_PRINT_TEMPLATE", 0x0080, message=_COM_HTML_DIALOG_DEPRECATION_MSG),
	RemovedSymbol("HTMLDLG_VERIFY", 0x0100, message=_COM_HTML_DIALOG_DEPRECATION_MSG),
)
"""Module level `__getattr__` used to preserve backward compatibility."""

_DELAY_BEFORE_MESSAGE_MS: Final[int] = 1
"""Duration in milliseconds for which to delay speaking and brailling a message, so that any UI changes don't interrupt it.
1ms is a magic number. It can be increased if it is found to be too short, but it should be kept to a minimum.
"""


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

	log.debug("Presenting browsable message unavailable warning.")
	wx.CallAfter(
		gui.messageBox,
		browsableMessageUnavailableMsg,
		# Translators: This is the title for a warning dialog, shown if NVDA cannot open a browsable message.
		caption=_("Feature unavailable."),
		style=wx.ICON_ERROR | wx.OK,
	)


def _copyBrowseableMessageToClipboard(text: str) -> None:
	import api  # Late import to avoid a circular dependency (api imports ui).

	api.copyToClip(text)
	# Translators: Reported when the content of a browseable message is copied to the clipboard.
	message(_("Copied to clipboard"))


def browseableMessage(
	message: str,
	title: str | None = None,
	isHtml: bool = False,
	closeButton: bool = False,
	copyButton: bool = False,
	sanitizeHtmlFunc: Callable[[str], str] = nh3.clean,
) -> None:
	"""Present a message to the user that can be read in browse mode.
	The message will be presented in an HTML document.

	:param message: The message in either html or text.
	:param title: The title for the message, defaults to "NVDA Message".
	:param isHtml: Whether the message is html, defaults to False.
	:param closeButton: Whether to include a "close" button, defaults to False.
	:param copyButton: Whether to include a "copy" (to clipboard) button, defaults to False.
	:param sanitizeHtmlFunc: How to sanitize the html message, if isHtml is True.
		Defaults to `nh3.clean` with default arguments.
		Ensure to sanitize the html message if the source of it could be untrusted.
		Any translatable string, or user generated content should be sanitized.
	"""
	if isRunningOnSecureDesktop():
		_warnBrowsableMessageNotAvailableOnSecureScreens(title)
		return

	if title is None:
		# Translators: The title for the dialog used to present general NVDA messages in browse mode.
		title = _("NVDA Message")

	htmlPath = os.path.join(globalVars.appDir, "message.html")

	# Sanitize/prepare HTML
	if not isHtml:
		messageSanitized = f"<pre>{escape(message)}</pre>"
	else:
		messageSanitized = sanitizeHtmlFunc(message)

	with open(htmlPath, encoding="utf-8") as f:
		templatedMessage = (
			f.read().replace("{{TITLE}}", escape(title)).replace("{{MESSAGE}}", messageSanitized)
		)

	# --- build the dialog ---
	dialog = HtmlMessageDialog(gui.mainFrame, templatedMessage, title, buttons=None)

	if copyButton:
		dialog.addButton(
			wx.ID_COPY,
			# Translators: The label of a button to copy the text of the window to the clipboard.
			label=_("&Copy"),
			callback=lambda evt: _copyBrowseableMessageToClipboard(dialog._messageControl.GetPageText()),
			closesDialog=False,
		)
		# The WebView captures keyboard input, so the button's accelerator never reaches it. The HTML
		# routes Alt+C to the same handler via the nvda-action://copy URL (see HtmlMessageDialog).
		dialog.registerAction(
			"copy",
			lambda: _copyBrowseableMessageToClipboard(dialog._messageControl.GetPageText()),
		)
	if closeButton:
		dialog.addCloseButton(fallbackAction=True)

	gui.mainFrame.prePopup()
	dialog.Show()
	gui.mainFrame.postPopup()


def message(
	text: str,
	speechPriority: speech.Spri | None = None,
	brailleText: str | None = None,
):
	"""Present a message to the user.
	The message will be presented in both speech and braille.
	@param text: The text of the message.
	@param speechPriority: The speech priority.
	@param brailleText: If specified, present this alternative text on the braille display.
	"""
	speech.speakMessage(text, priority=speechPriority)
	braille.handler.message(brailleText if brailleText is not None else text)


def delayedMessage(
	text: str,
	speechPriority: speech.Spri | None = speech.Spri.NOW,
	brailleText: str | None = None,
) -> None:
	"""Present a message to the user, delayed by a short amount so it isn't interrupted by UI changes.

	In most cases, :func:`ui.message` should be preferred.
	However, in cases where a message is presented at the same time as a UI change
	(for instance as confirmation that the action performed by an item in the NVDA menu has been performed),
	this function may be needed so that the message is not immediately interrupted by the UI changing.

	The message will be presented in both speech and braille.

	:param text: The text of the message.
	:param speechPriority: The speech priority, defaults to SpeechPriority.NOW.
	:param brailleText: If specified, present this alternative text on the braille display., defaults to None
	"""
	core.callLater(
		_DELAY_BEFORE_MESSAGE_MS,
		message,
		text=text,
		speechPriority=speechPriority,
		brailleText=brailleText,
	)


def reviewMessage(text: str, speechPriority: speech.Spri | None = None):
	"""Present a message from review or object navigation to the user.
	The message will always be presented in speech, and also in braille if it is tethered to review or when auto tethering is on.
	@param text: The text of the message.
	@param speechPriority: The speech priority.
	"""
	speech.speakMessage(text, priority=speechPriority)
	if braille.handler.shouldAutoTether or braille.handler.getTether() == TetherTo.REVIEW:
		braille.handler.message(text)


def reportTextCopiedToClipboard(text: str | None = None):
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
