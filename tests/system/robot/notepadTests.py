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

_notepad: _NotepadLib = _getLib("NotepadLib")
_asserts: _AssertsLib = _getLib("AssertsLib")


# unlike other symbols used, symbols.dic doesn't preserve quote symbols with SYMPRES_ALWAYS
_wordsToExpectedSymbolLevelAllSpeech = {
	'Say': 'Say',
	'(quietly)': 'left paren(quietly right paren)',
	'"Hello,': 'quote Hello comma,',
	'Jim".': 'Jim quote  dot.',
	'➔': 'right-pointing arrow',
	'👕': 't-shirt',  # fails, actual text:  "t dash shirt"
}
_wordsToExpectedSymbolLevelDefaultSpeech = {
	'Say': 'Say',
	'(quietly)': '(quietly)',
	'"Hello,': 'Hello,',
	'Jim".': 'Jim .',
	'➔': 'right-pointing arrow',
	'👕': 't-shirt',  # fails, actual text:  "t shirt"
}


def test_symbolLevelWord_all():
	textStr = ' '.join(_wordsToExpectedSymbolLevelAllSpeech.keys())
	_notepad.prepareNotepad(f"Test: {textStr}")
	for expectedWord in _wordsToExpectedSymbolLevelAllSpeech.values():
		wordSpoken = _notepad.getSpeechAfterKey("numpad6")  # navigate to next word
		_asserts.strings_match(wordSpoken, expectedWord)


def test_symbolLevelWord_default():
	textStr = ' '.join(_wordsToExpectedSymbolLevelDefaultSpeech.keys())
	_notepad.prepareNotepad(f"Test: {textStr}")
	for expectedWord in _wordsToExpectedSymbolLevelDefaultSpeech.values():
		wordSpoken = _notepad.getSpeechAfterKey("numpad6")  # navigate to next word
		_asserts.strings_match(wordSpoken, expectedWord)
