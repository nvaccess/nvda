# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Logic for reading text using NVDA in the notepad text editor.
"""
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from SystemTestSpy import (
	_getLib,
)

# Imported for type information
from NotepadLib import NotepadLib as _NotepadLib
from AssertsLib import AssertsLib as _AssertsLib
import NvdaLib as _NvdaLib

_notepad: _NotepadLib = _getLib("NotepadLib")
_asserts: _AssertsLib = _getLib("AssertsLib")


def test_moveByWord_symbolLevelWord():
	"""Disabled due to revert of PR #11856 is: "Speak all symbols when moving by words (#11779)
	"""
	# unlike other symbols used, symbols.dic doesn't preserve quote symbols with SYMPRES_ALWAYS
	_wordsToExpected = {
		'Say': 'Say',
		'(quietly)': 'left paren(quietly right paren)',
		'"Hello,': 'quote Hello comma,',
		'Jim".': 'Jim quote  dot.',
		'➔': 'right-pointing arrow',  # Speech for symbols shouldn't change
		'👕': 't-shirt',  # Speech for symbols shouldn't change
	}

	spy = _NvdaLib.getSpyLib()
	spy.set_configValue(["speech", "symbolLevelWordAll"], True)

	textStr = ' '.join(_wordsToExpected.keys())
	_notepad.prepareNotepad(f"Test: {textStr}")
	for expectedWord in _wordsToExpected.values():
		wordSpoken = _NvdaLib.getSpeechAfterKey("numpad6")  # navigate to next word
		_asserts.strings_match(wordSpoken, expectedWord)


def test_moveByWord():
	_wordsToExpected = {
		'Say': 'Say',
		'(quietly)': '(quietly)',
		'"Hello,': 'Hello,',
		'Jim".': 'Jim .',
		'➔': 'right pointing arrow',
		'👕': 't shirt',
	}

	spy = _NvdaLib.getSpyLib()
	spy.set_configValue(["speech", "symbolLevelWordAll"], False)

	textStr = ' '.join(_wordsToExpected.keys())
	_notepad.prepareNotepad(f"Test: {textStr}")
	for expectedWord in _wordsToExpected.values():
		wordSpoken = _NvdaLib.getSpeechAfterKey("numpad6")  # navigate to next word
		_asserts.strings_match(wordSpoken, expectedWord)
