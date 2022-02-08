# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Logic for reading text using NVDA in the notepad text editor.
"""
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
import enum as _enum
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


class Move(_enum.Enum):
	"""Gestures to move by different amounts"""
	CHAR = "numpad3"
	WORD = "numpad6"
	LINE = "numpad9"
	HOME = "shift+numpad7"


class SymLevel(_enum.Enum):
	"""Symbol levels, should match characterProcessing.SymbolLevel
	"""
	NONE = 0
	ALL = 300


class EndSpeech(_enum.Enum):
	""" Speech given when reaching the end of the movement direction.
	"""
	BOTTOM = "Bottom"
	RIGHT = "Right"


def _pressKeyAndCollectSpeech(key: str, numberOfTimes: int) -> _typing.List[str]:
	actual = []
	for _ in range(numberOfTimes):
		spoken = _NvdaLib.getSpeechAfterKey(key)
		# collect all output before asserting to show full picture of behavior
		actual.append(spoken)
	return actual


def _getMoveByWordTestSample() -> str:
	return (
		"Test: "  # first word won't be spoken
		'Say (quietly) "Hello, Jim ".'
		" don't"  # test punctuation inside a word.
		# symbols have space before and after, so it is considered a word
		" ➔ 👕 \n"  # test Symbols containing punctuations (right-pointing arrow, t-shirt)
		' \n'  # single space
		'\t\n'  # single tab
		'    \n'  # 4 spaces
		'➔\n'  # no space before, only newline after symbol
		'👕\n'  # no space before, only newline after symbol
		'👕'  # no space before, no newline after symbol
	)


def _getMoveByLineTestSample() -> str:
	testData = [
		"Test:",  # initial new line which isn't spoken
		'Say',
		'(quietly)',  # test parenthesis
		'"Hello,',  # test quote, comma
		'Jim".',  # test quote, dot
		" don't ",  # test punctuation inside a word.
		'➔', '👕',  # test Symbols containing punctuations (right-pointing arrow, t-shirt)
		'➔ ', '👕 ',  # test Symbols containing punctuations with joined space
		'➔👕',  # test Symbols containing punctuations without space
		' ',  # single space
		'\t',  # single tab
		'    ',  # 4 spaces
		'',  # to ensure prior entry ends with newline.
	]
	return '\n'.join(testData)


def _getMoveByCharTestSample() -> str:
	# Intentionally concat the following strings, there should be no trailing commas
	return (
		'T'  # An initial character, that isn't spoken (because it isn't traversed during nav).
		'S ()"'
		"'e,➔👕\t"
		'\na'  # Note: The 'a' character will be on the next line, thus won't be spoken
	)


def test_moveByWord():
	"""Move by word with symbol level 'all' then with symbol level 'none'
	"""
	_notepad.prepareNotepad(_getMoveByWordTestSample())
	_doTest(
		navKey=Move.WORD,
		reportedAfterLast=EndSpeech.BOTTOM,
		symbolLevel=SymLevel.NONE,
		expectedSpeech=[
			'Say',
			'(quietly)', 'Hello,', 'Jim', '.',  # no symbols named
			"don't",  # mid-word symbol
			'right pointing arrow', 't shirt',
			# end of first line
			'blank',  # single space and newline
			'',  # tab and newline
			'blank',  # 4 spaces and newline
			'right pointing arrow',
			't shirt',  # no space before or after symbol
			't shirt',  # no character before or after symbol (no newline)
			'blank',  # end of doc
		],
	)

	_NvdaLib.getSpeechAfterKey(Move.HOME.value)  # reset to start position

	_doTest(
		navKey=Move.WORD,
		reportedAfterLast=EndSpeech.BOTTOM,
		symbolLevel=SymLevel.ALL,
		expectedSpeech=[
			'Say',
			'left paren(quietly right paren)',  # parenthesis are named
			'quote Hello comma,', 'Jim', 'quote  dot.',  # quote, comma and dot are named
			'don tick t',  # mid-word symbol
			'right dash pointing arrow', 't dash shirt',
			# end of first line
			'blank',  # single space and newline
			'tab',  # tab and newline
			'blank',  # 4 spaces and newline
			'right dash pointing arrow',  # no space before or after symbol
			't dash shirt',  # no space before or after symbol
			't dash shirt',  # no character before or after symbol (no newline)
			'blank'  # end of doc
		]
	)


def test_moveByLine():
	_notepad.prepareNotepad(_getMoveByLineTestSample())
	_doTest(
		navKey=Move.LINE,
		reportedAfterLast=EndSpeech.BOTTOM,
		symbolLevel=SymLevel.NONE,
		expectedSpeech=[
			'Say', '(quietly)', 'Hello,', 'Jim .', "don't",
			'',  # right arrow symbol
			't-shirt',
			'',  # right arrow symbol
			't-shirt',
			't-shirt',  # note missing right arrow symbol
			'blank',  # single space
			'',  # tab
			'blank',  # four spaces
			'blank',  # end of doc
		]
	)

	_NvdaLib.getSpeechAfterKey(Move.HOME.value)  # reset to start position

	_doTest(
		navKey=Move.LINE,
		symbolLevel=SymLevel.ALL,
		reportedAfterLast=EndSpeech.BOTTOM,
		expectedSpeech=[
			'Say',
			'left paren(quietly right paren)',
			'quote Hello comma,', 'Jim quote  dot.',
			'don tick t',
			'right-pointing arrow', 't-shirt',  # symbols each on a line
			'right-pointing arrow', 't-shirt',  # symbols and a space each on a line
			'right-pointing arrow  t-shirt',  # symbols joined no space
			'blank',  # single space
			'tab',  # single tab
			'blank',  # 4 spaces
			'blank',  # end of doc
		],
	)


def test_moveByChar():
	_notepad.prepareNotepad(_getMoveByCharTestSample())
	# Symbol level should not affect move by character
	# use the same expected speech with symbol level none and all.
	# Bug: With symbol level ALL text due to a symbol substitution has further substitutions applied:
	# IE: "t-shirt" either becomes "t shirt" or "t dash shirt" dependent on symbol level.

	_doTest(
		navKey=Move.CHAR,
		reportedAfterLast=EndSpeech.RIGHT,
		symbolLevel=SymLevel.NONE,
		expectedSpeech=[
			'S', 'space',
			'left paren', 'right paren',
			'quote', 'tick',
			'e', 'comma',
			'right pointing arrow', 't shirt',   # note no dash, sym level All has
			'tab',
			'carriage return',  # on Windows/notepad newline is \r\n
			'line feed',  # on Windows/notepad newline is \r\n
		],
	)

	_NvdaLib.getSpeechAfterKey(Move.HOME.value)  # reset to start position.

	_doTest(
		navKey=Move.CHAR,
		reportedAfterLast=EndSpeech.RIGHT,
		symbolLevel=SymLevel.ALL,
		expectedSpeech=[
			'S', 'space',
			'left paren', 'right paren',
			'quote', 'tick',
			'e', 'comma',
			'right dash pointing arrow', 't dash shirt',  # note has dash, sym level None doesn't
			'tab',
			'carriage return',  # on Windows/notepad newline is \r\n
			'line feed',  # on Windows/notepad newline is \r\n
		],
	)


def test_symbolInSpeechUI():
	_notepad.prepareNotepad((
		"t"  # Character doesn't matter, we just want to invoke "Right" speech UI.
	))
	_setSymbolLevel(SymLevel.ALL)
	spy = _NvdaLib.getSpyLib()
	expected = "shouldn't sub tick symbol"
	spy.override_translationString(EndSpeech.RIGHT.value, expected)

	# get to the end char
	actual = _pressKeyAndCollectSpeech(Move.CHAR.value, numberOfTimes=1)
	_builtIn.should_be_equal(
		actual,
		["blank", ],
		msg="actual vs expected. Unexpected speech when moving to final character.",
	)

	actual = _pressKeyAndCollectSpeech(Move.CHAR.value, numberOfTimes=1)
	_builtIn.should_be_equal(
		actual,
		# Illustrates a bug in NVDA. The internal speech UI is processed substituting symbols.
		# This can be a major issue in languages other than English.
		[
			# 'tick' is a bug
			"shouldn tick t sub tick symbol"  # intentionally concatenate strings
			"\nblank",
		],
		msg="actual vs expected. NVDA speech UI substitutes symbols",
	)

	# Show that with symbol level None, the speech UI symbols are not substituted.
	_setSymbolLevel(SymLevel.NONE)
	actual = _pressKeyAndCollectSpeech(Move.CHAR.value, numberOfTimes=1)
	_builtIn.should_be_equal(
		actual,
		[f"{expected}\nblank", ],
		msg="actual vs expected. NVDA speech UI substitutes symbols",
	)


def _setSymbolLevel(symbolLevel: SymLevel) -> None:
	spy = _NvdaLib.getSpyLib()
	SYMBOL_LEVEL_KEY = ["speech", "symbolLevel"]
	spy.set_configValue(SYMBOL_LEVEL_KEY, symbolLevel.value)
	_builtIn.log(message=f"Doing test at symbol level: {symbolLevel}")


def _doTest(
		navKey: Move,
		expectedSpeech: _typing.List[str],
		reportedAfterLast: EndSpeech,
		symbolLevel: SymLevel,
) -> None:
	_setSymbolLevel(symbolLevel)

	actual = _pressKeyAndCollectSpeech(navKey.value, numberOfTimes=len(expectedSpeech))
	_builtIn.should_be_equal(
		actual,
		expectedSpeech,
		msg=f"actual vs expected. With symbolLevel {symbolLevel}"
	)

	# ensure all content tested, ie the end of the sample should be reached
	finalItem = expectedSpeech[-1]
	endReached = f"{reportedAfterLast.value}\n{finalItem}"
	actual = _pressKeyAndCollectSpeech(navKey.value, 1)
	_builtIn.should_be_equal(
		actual,
		[endReached, ],
		msg=f"End reached failure. actual vs expected. With symbolLevel {symbolLevel}"
	)
