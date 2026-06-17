# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""System tests for the browseable message dialog (HtmlMessageDialog).

Uses script_review_currentSymbol (bound to NVDA+0 via browseableMessage-gestures.ini).
Pressing the gesture twice on a known symbol opens a browseableMessage dialog showing:
  title:   "Expanded symbol (English)"
  content: "Character: ➔\\nReplacement: right-pointing arrow"
"""

# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from SystemTestSpy import _getLib

# Imported for type information
from NotepadLib import NotepadLib as _NotepadLib
from AssertsLib import AssertsLib as _AssertsLib
import NvdaLib as _NvdaLib

_notepad: _NotepadLib = _getLib("NotepadLib")
_asserts: _AssertsLib = _getLib("AssertsLib")

_REVIEW_CURRENT_SYMBOL = "NVDA+0"  # matches browseableMessage-gestures.ini
_TEST_SYMBOL = "➔"
_EXPECTED_DIALOG_TITLE = "Expanded symbol (English)"


def _openBrowseableMessage() -> int:
	"""Open the browseable message dialog by double-pressing the review current symbol gesture.
	Returns the speech index of the dialog title, for use in further assertions.
	"""
	spy = _NvdaLib.getSpyLib()
	# First press: report the symbol by speech (don't block so the second press can follow quickly)
	spy.emulateKeyPress(_REVIEW_CURRENT_SYMBOL, blockUntilProcessed=False)
	# Second press: triggers the browse mode dialog
	spy.emulateKeyPress(_REVIEW_CURRENT_SYMBOL)
	# Wait for the dialog title to be spoken
	titleSpeechIndex = spy.wait_for_specific_speech(_EXPECTED_DIALOG_TITLE)
	spy.wait_for_speech_to_finish()
	return titleSpeechIndex


def test_browseableMessage_opens():
	"""Ensure the browseable message dialog opens and NVDA reads the title and content."""
	_notepad.prepareNotepad(_TEST_SYMBOL)
	titleSpeechIndex = _openBrowseableMessage()
	spy = _NvdaLib.getSpyLib()
	actualSpeech = spy.get_speech_at_index_until_now(titleSpeechIndex)
	# The dialog title is announced when it opens, then the WebView content is read in browse mode.
	# The ➔ symbol is spoken as its replacement text "right-pointing arrow" at the default symbol level.
	_asserts.strings_match(
		actualSpeech,
		"\n".join(
			[
				f"{_EXPECTED_DIALOG_TITLE}  dialog",
				f"{_EXPECTED_DIALOG_TITLE}  document",
				"Character:  right-pointing arrow",
			],
		),
	)
	# Close the dialog before teardown
	spy.emulateKeyPress("escape")
	spy.wait_for_speech_to_finish()


def test_browseableMessage_navigation():
	"""Ensure browse mode navigation with downArrow moves through the dialog content."""
	_notepad.prepareNotepad(_TEST_SYMBOL)
	_openBrowseableMessage()
	spy = _NvdaLib.getSpyLib()
	# The dialog content is a <pre> block:
	# Line 1: "Character: ➔"   (➔ spoken as "right-pointing arrow" at default symbol level)
	# Line 2: "Replacement: right-pointing arrow"
	# Arrow down from line 1 to line 2
	secondLineSpeech = _NvdaLib.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		secondLineSpeech,
		"Replacement: right-pointing arrow",
	)
	# Close the dialog before teardown
	spy.emulateKeyPress("escape")
	spy.wait_for_speech_to_finish()


def test_browseableMessage_close():
	"""Ensure the browseable message dialog closes when Escape is pressed."""
	_notepad.prepareNotepad(_TEST_SYMBOL)
	_openBrowseableMessage()
	spy = _NvdaLib.getSpyLib()
	# Escape should close the dialog and return focus to Notepad
	spy.emulateKeyPress("escape")
	spy.wait_for_speech_to_finish()
	# Verify dialog is closed: single-press the gesture to report the symbol by speech.
	# If Notepad has focus on ➔, NVDA speaks "right-pointing arrow".
	# This would fail if the dialog were still open (no symbol under review cursor there).
	symbolSpeech = _NvdaLib.getSpeechAfterKey(_REVIEW_CURRENT_SYMBOL)
	_asserts.strings_match(symbolSpeech, "right-pointing arrow")
