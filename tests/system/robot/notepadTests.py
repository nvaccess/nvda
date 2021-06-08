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


def test_symbolLevelWord(isSymbolLevelWordAllExpected=True):
	wordsWithSymbols = ['He', 'said', '(quietly),', '"Hello,', 'Jim".']
	symbolMap = {
		'(': 'left paren',
		')': 'right paren',
		',': 'comma',
		'"': 'quote',
		'.': 'dot',
	}
	textStr = ' '.join(wordsWithSymbols)
	_notepad.prepareNotepad(f"Test: {textStr}")
	for expectedWord in wordsWithSymbols:
		wordSpoken = _notepad.getSpeechAfterKey("numpad6")
		for symbol in symbolMap.keys():
			if isSymbolLevelWordAllExpected:
				expectedWord = expectedWord.replace(symbol, f" {symbolMap[symbol]}{symbol}")
		expectedWord = expectedWord.replace('"', ' ').strip()  # always strip quote symbols
		_asserts.strings_match(wordSpoken, expectedWord)
