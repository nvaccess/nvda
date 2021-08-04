# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Logic for reading text using NVDA in the notepad text editor.
"""
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
import typing as _typing

from SystemTestSpy import (
	_getLib,
)

# Imported for type information
from NotepadLib import NotepadLib as _NotepadLib
from AssertsLib import AssertsLib as _AssertsLib
import NvdaLib as _NvdaLib
from robot.libraries.BuiltIn import BuiltIn

_builtIn: BuiltIn = BuiltIn()
_notepad: _NotepadLib = _getLib("NotepadLib")
_asserts: _AssertsLib = _getLib("AssertsLib")

navToNextCharKey = "numpad3"
navToNextWordKey = "numpad6"
navToNextLineKey = "numpad9"


def _pressKeyAndCollectSpeech(key: str, numberOfTimes: int) -> _typing.List[str]:
	actual = []
	for _ in range(numberOfTimes):
		spoken = _NvdaLib.getSpeechAfterKey(key)
		# collect all output before asserting to show full picture of behavior
		actual.append(spoken)
	return actual


def _doMoveByWordTest(expected: _typing.List[str]):
	_moveByWordData = (
		'Say (quietly) "Hello, Jim ". ➔ 👕 \n'
		' \n'  # single space
		'\t\n'
		'    \n'  # 4 spaces
		'➔\n'
		'👕\n'  # no space after symbol
		'👕'  # no character (no newline) after symbol
	)
	_notepad.prepareNotepad(f"Test: {_moveByWordData}")
	actual = _pressKeyAndCollectSpeech(navToNextWordKey, numberOfTimes=len(expected))
	_builtIn.should_be_equal(actual, expected)
	# ensure all words tested
	actual = _pressKeyAndCollectSpeech(navToNextWordKey, 1)
	_builtIn.should_be_equal(actual, [f"Bottom\n{expected[-1]}", ])


def test_moveByWord_symbolLevelWord():
	"""Disabled due to revert of PR #11856 is: "Speak all symbols when moving by words (#11779)
	"""
	spy = _NvdaLib.getSpyLib()
	spy.set_configValue(["speech", "symbolLevelWordAll"], True)

	# unlike other symbols used, symbols.dic doesn't preserve quote symbols with SYMPRES_ALWAYS
	_doMoveByWordTest(expected=[
		'Say',
		'(quietly)',
		'Hello,',
		'Jim',
		'.',
		'right pointing arrow',  # has space before and after symbol
		't shirt',  # has space before and after symbol
		# end of first line
		'blank',  # single space and newline
		'',  # tab and newline
		'blank',  # 4 spaces and newline
		'right pointing arrow',  # no space before or after symbol
		't shirt',  # no space before or after symbol
		't shirt',  # no character before or after symbol (no newline)
		'blank',  # end of doc
	])


def test_moveByWord():
	spy = _NvdaLib.getSpyLib()
	spy.set_configValue(["speech", "symbolLevelWordAll"], False)

	_doMoveByWordTest(expected=[
		'Say',
		'(quietly)',
		'Hello,',
		'Jim',
		'.',
		'right pointing arrow',  # has space before and after symbol
		't shirt',  # has space before and after symbol
		# end of first line
		'blank',  # single space and newline
		'',  # tab and newline
		'blank',  # 4 spaces and newline
		'right pointing arrow',  # no space before or after symbol
		't shirt',  # no space before or after symbol
		't shirt',  # no character before or after symbol (no newline)
		'blank',  # end of doc
	])


def _doMoveByLineTest():
	testData = [
		'Say',
		'(quietly)',
		'"Hello,',
		'Jim".',
		'➔',
		'👕',
		'➔ ',
		'👕 ',
		'➔👕',
		' ',
		'\t',
		'    ',
		'',
	]

	expected = [
		'Say',
		'(quietly)',
		'Hello,',
		'Jim .',
		'right-pointing arrow',
		't-shirt',
		'right-pointing arrow',
		't-shirt',
		'right-pointing arrow  t-shirt',
		'blank',  # single space
		'',  # tab
		'blank',  # four spaces
		'blank',  # end of doc
	]

	textStr = '\n'.join(testData)

	_notepad.prepareNotepad(f"Test:\n{textStr}")  # initial new line which isn't spoken
	actual = _pressKeyAndCollectSpeech(navToNextLineKey, numberOfTimes=len(expected))
	_builtIn.should_be_equal(actual, expected)
	# ensure all lines tested
	actual = _pressKeyAndCollectSpeech(navToNextLineKey, 1)
	_builtIn.should_be_equal(actual, [f"Bottom\n{expected[-1]}", ])


def test_moveByLine():
	spy = _NvdaLib.getSpyLib()
	spy.set_configValue(["speech", "symbolLevelWordAll"], False)
	_doMoveByLineTest()


def test_moveByLine_symbolLevelWord():
	spy = _NvdaLib.getSpyLib()
	spy.set_configValue(["speech", "symbolLevelWordAll"], True)
	_doMoveByLineTest()


def _doMoveByCharTest(expected: _typing.List[str]):
	_text = 'S ()e,➔👕\t\na'  # note, 'a' is on next line and won't be spoken

	_notepad.prepareNotepad(f" {_text}")
	actual = _pressKeyAndCollectSpeech(navToNextCharKey, numberOfTimes=len(expected))
	_builtIn.should_be_equal(actual, expected)
	# ensure all chars tested
	actual = _pressKeyAndCollectSpeech(navToNextCharKey, 1)
	_builtIn.should_be_equal(actual, [f"Right\n{expected[-1]}", ])


def test_moveByChar():
	spy = _NvdaLib.getSpyLib()
	spy.set_configValue(["speech", "symbolLevelWordAll"], False)

	_doMoveByCharTest(expected=[
		'S',
		'space',
		'left paren',
		'right paren',
		'e',
		'comma',
		'right pointing arrow',
		't shirt',
		'tab',
		'carriage return',  # on Windows/notepad newline is \r\n
		'line feed',  # on Windows/notepad newline is \r\n
	])


def test_moveByChar_symbolLevelWord():
	spy = _NvdaLib.getSpyLib()
	spy.set_configValue(["speech", "symbolLevelWordAll"], True)

	_doMoveByCharTest([
		'S',
		'space',
		'left paren',
		'right paren',
		'e',
		'comma',
		'right pointing arrow',
		't shirt',
		'tab',
		'carriage return',  # on Windows/notepad newline is \r\n
		'line feed',  # on Windows/notepad newline is \r\n
	])
