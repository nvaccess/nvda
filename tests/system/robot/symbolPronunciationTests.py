# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Tests for symbol pronunciation within NVDA.
"""
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
import enum as _enum
import typing as _typing

from SystemTestSpy import (
	_getLib,
)

# Imported for type information
from NotepadLib import NotepadLib as _NotepadLib
from ChromeLib import ChromeLib as _ChromeLib
from AssertsLib import AssertsLib as _AssertsLib
import NvdaLib as _NvdaLib
from robot.libraries.BuiltIn import BuiltIn

_builtIn: BuiltIn = BuiltIn()
_notepad: _NotepadLib = _getLib("NotepadLib")
_asserts: _AssertsLib = _getLib("AssertsLib")


class Move(_enum.Enum):
	"""Gestures to move by different amounts"""
	REVIEW_CHAR = "numpad3"
	REVIEW_WORD = "numpad6"
	REVIEW_LINE = "numpad9"
	REVIEW_HOME = "shift+numpad7"
	SEL_CARET_CHAR = "shift+rightArrow"
	SEL_CARET_WORD = "shift+control+rightArrow"
	SEL_CARET_LINE = "shift+downArrow"
	CARET_HOME = "control+home"
	CARET_CHAR = "rightArrow"
	CARET_CHAR_BACK = "leftArrow"


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
	NONE = None


def _pressKeyAndCollectSpeech(key: str, numberOfTimes: int) -> _typing.List[str]:
	actual = []
	for _ in range(numberOfTimes):
		spoken = _NvdaLib.getSpeechAfterKey(key)
		# collect all output before asserting to show full picture of behavior
		actual.append(spoken)
	return actual


def _getByWordTestSample() -> str:
	return (
		"Test: "  # first word won't be spoken
		'Say (quietly) "Hello, Jim ".'
		" don't"  # test punctuation inside a word.
		# symbols have space before and after, so it is considered a word
		" ➔ 👕 \n"  # test Symbols containing punctuations (right-pointing arrow, t-shirt)
		"1 | 2 || 3 ||| 4\n"  # test single/multiple symbols within a "word" issue #10855
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
		"1 | 2 || 3 ||| 4",  # test single/multiple symbols within a "word" issue #10855
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
	Symbol expectations:
	➔ - When replaced by speech "right-pointing arrow", the dash should not be removed.
	👕 - When replaced by speech "t-shirt", the dash should not be removed, honor the replacement text for
			symbols/punctuation.

	There should not be any "empty" words. E.G. a word made of two bar chars: ||
	Something should be reported, even at symbol level None. Possible:
	- The names of the characters: "bar bar", what if there are many (hundreds) symbols?
	- A placeholder speech UI E.G "symbols". Will it be obvious this is a placeholder?
	"""
	_notepad.prepareNotepad(_getByWordTestSample())
	_doTest(
		navKey=Move.REVIEW_WORD,
		reportedAfterLast=EndSpeech.BOTTOM,
		symbolLevel=SymLevel.NONE,
		expectedSpeech=[
			'Say',
			'(quietly)', 'Hello,', 'Jim', '.',  # Expected: no symbols named
			"don't",  # Expected: mid-word symbol
			'right pointing arrow', 't shirt',  # todo: Expect dash
			'1', 'bar', '2', '', '3', '', '4',  # todo: There should not be any "empty" words.
			# end of first line
			'blank',  # single space and newline
			'',  # tab and newline  todo: There should not be any "empty" words.
			'blank',  # 4 spaces and newline
			'right pointing arrow',
			't shirt',  # todo: Expect dash
			't shirt',  # todo: Expect dash
			'blank',  # end of doc
		],
	)

	_NvdaLib.getSpeechAfterKey(Move.REVIEW_HOME.value)  # reset to start position

	_doTest(
		navKey=Move.REVIEW_WORD,
		reportedAfterLast=EndSpeech.BOTTOM,
		symbolLevel=SymLevel.ALL,
		expectedSpeech=[
			'Say',
			'left paren(quietly right paren)',  # Expect: parenthesis are named
			'quote Hello comma,', 'Jim', 'quote  dot.',  # Expect: quote, comma and dot are named
			'don tick t',  # Expect: mid-word symbol substituted
			'right dash pointing arrow', 't dash shirt',  # todo: Expect dash symbol not to be replaced with word.
			'1', 'bar', '2', 'bar  bar', '3', 'bar  bar  bar', '4',  # Expect no empty words.
			# end of first line
			'blank',  # single space and newline
			'tab',  # tab and newline
			'blank',  # 4 spaces and newline
			'right dash pointing arrow',  # todo: Expect dash symbol not to be replaced with word.
			't dash shirt',  # todo: Expect dash symbol not to be replaced with word.
			't dash shirt',  # todo: Expect dash symbol not to be replaced with word.
			'blank'  # end of doc
		]
	)


def test_moveByLine():
	"""
	Symbol expectations:
	➔ - When replaced by speech "right-pointing arrow", the dash should not be removed.
	👕 - When replaced by speech "t-shirt", the dash should not be removed, honor the replacement text for
			symbols/punctuation.

	There should not be any "empty" lines. E.G. a line with only space / tabs
	Something should be reported, even at symbol level None. Possible:
	- The names of the characters: "tab space", what if there are many (hundreds)?
	- A placeholder speech UI E.G "whitespace". Will it be obvious this is a placeholder?
	"""
	_notepad.prepareNotepad(_getMoveByLineTestSample())
	_doTest(
		navKey=Move.REVIEW_LINE,
		reportedAfterLast=EndSpeech.BOTTOM,
		symbolLevel=SymLevel.NONE,
		expectedSpeech=[
			'Say', '(quietly)', 'Hello,', 'Jim .', "don't",  # Expect:
			'',  # todo: Expect 'right-pointing arrow'
			't-shirt',
			'',  # todo: Expect 'right-pointing arrow'
			't-shirt',
			't-shirt',  # todo: Expect 'right-pointing arrow t-shirt'
			'1   2    3     4',  # todo: Should symbols be passed to synth, i.e. "1 | 2 || 3 etc"?
			'blank',  # single space
			'',  # tab  # todo: There should not be any "empty" lines.
			'blank',  # four spaces
			'blank',  # end of doc
		]
	)

	_NvdaLib.getSpeechAfterKey(Move.REVIEW_HOME.value)  # reset to start position

	_doTest(
		navKey=Move.REVIEW_LINE,
		symbolLevel=SymLevel.ALL,
		reportedAfterLast=EndSpeech.BOTTOM,
		expectedSpeech=[
			'Say',
			'left paren(quietly right paren)',  # Expect: parenthesis are named
			'quote Hello comma,', 'Jim quote  dot.',  # Expect: quote, comma and dot are named
			'don tick t',  # Expect: mid-word symbol substituted
			'right-pointing arrow', 't-shirt',  # Expect dash
			'right-pointing arrow', 't-shirt',  # Expect dash
			'right-pointing arrow  t-shirt',  # Expect dash
			'1  bar  2  bar  bar  3  bar  bar  bar  4',  # Expect | symbol replaced with bar.
			'blank',  # single space
			'tab',  # single tab
			'blank',  # 4 spaces
			'blank',  # end of doc
		],
	)


def test_moveByChar():
	"""
	# Symbol level should not affect move by character
	# use the same expected speech with symbol level none and all.
	Symbol expectations:
	➔ - When replaced by speech "right-pointing arrow", the dash should not be removed.
	👕 - When replaced by speech "t-shirt", the dash should not be removed, honor the replacement text for
			symbols/punctuation.

	There should not be any "empty" characters.
	"""
	_notepad.prepareNotepad(_getMoveByCharTestSample())

	_doTest(
		navKey=Move.REVIEW_CHAR,
		reportedAfterLast=EndSpeech.RIGHT,
		symbolLevel=SymLevel.NONE,
		expectedSpeech=[
			'S', 'space',  # Expect whitespace named.
			'left paren', 'right paren',  # Expect parens named
			'quote', 'tick',  # Expect quote and apostrophe named
			'e', 'comma',  # Expect comma named
			'right pointing arrow', 't shirt',   # todo: Expect dash i.e. 'right-pointing arrow', 't-shirt'
			'tab',  # Expect tab named
			'carriage return',  # Expect Windows/notepad newline is \r\n
			'line feed',  # on Windows/notepad newline is \r\n
		],
	)

	_NvdaLib.getSpeechAfterKey(Move.REVIEW_HOME.value)  # reset to start position.

	# todo: Bug, with symbol level ALL text due to a symbol substitution has further substitutions applied:
	#       IE: "t-shirt" either becomes "t shirt" or "t dash shirt" dependent on symbol level.
	_doTest(
		navKey=Move.REVIEW_CHAR,
		reportedAfterLast=EndSpeech.RIGHT,
		symbolLevel=SymLevel.ALL,
		expectedSpeech=[
			'S', 'space',  # Expect whitespace named.
			'left paren', 'right paren',  # Expect parens named
			'quote', 'tick',  # Expect quote and apostrophe named
			'e', 'comma',  # Expect comma named
			# todo: Expect no replacement with word 'dash' i.e. expect 'right-pointing arrow', 't-shirt'
			'right dash pointing arrow', 't dash shirt',
			'tab',  # Expect whitespace named.
			'carriage return',  # on Windows/notepad newline is \r\n
			'line feed',  # on Windows/notepad newline is \r\n
		],
	)


def test_selByWord():
	"""Select by word with symbol level 'all' then with symbol level 'none'
	Symbol expectations:
	➔ - When replaced by speech "right-pointing arrow", the dash should not be removed.
	👕 - When replaced by speech "t-shirt", the dash should not be removed, honor the replacement text for
			symbols/punctuation.

	There should not be any "empty" words. E.G. a word made of two bar chars: ||
	Something should be reported, even at symbol level None. Possible:
	- The names of the characters: "bar bar", what if there are many (hundreds) symbols?
	- A placeholder speech UI E.G "symbols". Will it be obvious this is a placeholder?
	"""
	_notepad.prepareNotepad(_getByWordTestSample())
	_doTest(
		navKey=Move.SEL_CARET_WORD,
		reportedAfterLast=EndSpeech.NONE,
		symbolLevel=SymLevel.NONE,
		expectedSpeech=list((
			i + (" " if i else "") + "selected" for i in [
				'Test: ',
				'Say ',
				'(quietly) ', 'Hello, ', 'Jim ', '. ',  # Expected: no symbols named
				"don't ",  # Expected: mid-word symbol
				'', 't-shirt  ',  # todo: Expect right-pointing arrow
				# end of first line
				'',  # This is the newline todo: There should not be any "empty" words.
				'1 ', '', '2 ', '', '3 ', '', '4',  # todo: There should not be any "empty" words.
				# end of second line
				'',  # newline and single space todo: There should not be any "empty" words.
				'',  # newline and tab  todo: There should not be any "empty" words.
				'',  # newline and 4 spaces todo: There should not be any "empty" words.
				'',  # newline  todo: There should not be any "empty" words.
				'right pointing arrow',  # todo: Expect dash
				'',  # newline  todo: There should not be any "empty" words.
				't shirt',  # todo: Expect dash
				'',  # newline  todo: There should not be any "empty" words.
				't shirt',  # todo: Expect dash
				# end of doc
			]
		)),
	)

	_NvdaLib.getSpeechAfterKey(Move.CARET_HOME.value)  # reset to start position

	_doTest(
		navKey=Move.SEL_CARET_WORD,
		reportedAfterLast=EndSpeech.NONE,
		symbolLevel=SymLevel.ALL,
		expectedSpeech=list((
			i + (" " if i else "") + "selected" for i in [
				'Test colon: ',
				'Say ',
				'left paren(quietly right paren) ',  # Expect: parenthesis are named
				'quote Hello comma, ', 'Jim ', 'quote  dot. ',  # Expect: quote, comma and dot are named
				'don tick t ',  # Expect: mid-word symbol substituted
				'right-pointing arrow  ', 't-shirt  ',  # Expect dash symbol not to be replaced with word.
				# end of first line
				'',  # newline  todo: There should not be any "empty" words.
				'1 ', 'bar  ', '2 ', 'bar  bar  ', '3 ', 'bar  bar  bar  ', '4',  # Expect no empty words.
				# end of second line
				'',  # newline and single space
				'tab ',  # newline and tab
				'',  # newline and 4 spaces
				'',  # newline
				'right dash pointing arrow',  # todo: Expect dash symbol not to be replaced with word.
				'',  # newline  todo: There should not be any "empty" words.
				't dash shirt',  # todo: Expect dash symbol not to be replaced with word.
				'',  # newline  todo: There should not be any "empty" words.
				't dash shirt',  # todo: Expect dash symbol not to be replaced with word.
				# end of doc
			]
		))
	)


def test_selByLine():
	"""
	Symbol expectations:
	➔ - When replaced by speech "right-pointing arrow", the dash should not be removed.
	👕 - When replaced by speech "t-shirt", the dash should not be removed, honor the replacement text for
			symbols/punctuation.

	There should not be any "empty" lines. E.G. a line with only space / tabs
	Something should be reported, even at symbol level None. Possible:
	- The names of the characters: "tab space", what if there are many (hundreds)?
	- A placeholder speech UI E.G "whitespace". Will it be obvious this is a placeholder?
	"""
	_notepad.prepareNotepad(_getMoveByLineTestSample())
	_doTest(
		navKey=Move.SEL_CARET_LINE,
		reportedAfterLast=EndSpeech.NONE,
		symbolLevel=SymLevel.NONE,
		expectedSpeech=list((
			i + ("   " if i else "") + "selected" for i in [
				'Test:',
				'Say', '(quietly)', 'Hello,', 'Jim .', "don't ",
				'',  # todo: Expect 'right-pointing arrow'
				't-shirt ',
				'',  # todo: Expect 'right-pointing arrow'
				't-shirt  ',
				't-shirt ',  # todo: Expect 'right-pointing arrow t-shirt'
				'1   2    3     4',  # todo: Should symbols be passed to synth, i.e. "1 | 2 || 3 etc"?
				'',  # single space todo: There should not be any "empty" lines.
				'',  # tab todo: There should not be any "empty" lines.
				'',  # four spaces todo: There should not be any "empty" lines.
				# end of doc
			]
		))
	)

	_NvdaLib.getSpeechAfterKey(Move.CARET_HOME.value)  # reset to start position

	_doTest(
		navKey=Move.SEL_CARET_LINE,
		symbolLevel=SymLevel.ALL,
		reportedAfterLast=EndSpeech.NONE,
		expectedSpeech=list((
			i + (" " if i else "") + "selected" for i in [
				'Test colon:  ',
				'Say  ',
				'left paren(quietly right paren)  ',  # Expect: parenthesis are named
				'quote Hello comma,  ', 'Jim quote  dot.  ',  # Expect: quote, comma and dot are named
				'don tick t   ',  # Expect: mid-word symbol substituted
				'right-pointing arrow   ', 't-shirt   ',  # Expect dash
				'right-pointing arrow    ', 't-shirt    ',  # Expect dash
				'right-pointing arrow  t-shirt   ',  # Expect dash
				'1  bar  2  bar  bar  3  bar  bar  bar  4  ',  # Expect | symbol replaced with bar.
				'',  # single space
				'tab   ',  # single tab
				'',  # 4 spaces
				# end of doc
			]
		)),
	)


def test_selByChar():
	"""
	# Symbol level should not affect move by character
	# use the same expected speech with symbol level none and all.
	Symbol expectations:
	➔ - When replaced by speech "right-pointing arrow", the dash should not be removed.
	👕 - When replaced by speech "t-shirt", the dash should not be removed, honor the replacement text for
			symbols/punctuation.

	There should not be any "empty" characters.
	"""
	_notepad.prepareNotepad(_getMoveByCharTestSample())

	_doTest(
		navKey=Move.SEL_CARET_CHAR,
		reportedAfterLast=EndSpeech.NONE,
		symbolLevel=SymLevel.NONE,
		expectedSpeech=list((
			i + (" " if i else "") + "selected" for i in [
				'T',
				'S', 'space',  # Expect whitespace named.
				'left paren', 'right paren',  # Expect parens named
				'quote', 'tick',  # Expect quote and apostrophe named
				'e', 'comma',  # Expect comma named
				'right pointing arrow', 't shirt',   # todo: Expect dash i.e. 'right-pointing arrow', 't-shirt'
				'tab',  # Expect tab named
				'',  # Expect Windows/notepad newline is \r\n
			]
		))
	)

	_NvdaLib.getSpeechAfterKey(Move.CARET_HOME.value)  # reset to start position.

	# todo: Bug, with symbol level ALL text due to a symbol substitution has further substitutions applied:
	#       IE: "t-shirt" either becomes "t shirt" or "t dash shirt" dependent on symbol level.
	_doTest(
		navKey=Move.SEL_CARET_CHAR,
		reportedAfterLast=EndSpeech.NONE,
		symbolLevel=SymLevel.ALL,
		expectedSpeech=list((
			i + (" " if i else "") + "selected" for i in [
				'T', 'S', 'space',  # Expect whitespace named.
				'left paren', 'right paren',  # Expect parens named
				'quote', 'tick',  # Expect quote and apostrophe named
				'e', 'comma',  # Expect comma named
				# todo: Expect no replacement with word 'dash' i.e. expect 'right-pointing arrow', 't-shirt'
				'right dash pointing arrow', 't dash shirt',
				'tab',  # Expect whitespace named.
				'',  # on Windows/notepad newline is \r\n
			]
		))
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
	actual = _pressKeyAndCollectSpeech(Move.REVIEW_CHAR.value, numberOfTimes=1)
	_builtIn.should_be_equal(
		actual,
		["blank", ],
		msg="actual vs expected. Unexpected speech when moving to final character.",
	)

	actual = _pressKeyAndCollectSpeech(Move.REVIEW_CHAR.value, numberOfTimes=1)
	_builtIn.should_be_equal(
		actual,
		# Illustrates a bug in NVDA. The internal speech UI is processed substituting symbols.
		# This can be a major issue in languages other than English.
		[
			# todo: 'tick' is a bug
			"shouldn tick t sub tick symbol"  # intentionally concatenate strings
			"\nblank",
		],
		msg="actual vs expected. NVDA speech UI substitutes symbols",
	)

	# Show that with symbol level None, the speech UI symbols are not substituted.
	_setSymbolLevel(SymLevel.NONE)
	actual = _pressKeyAndCollectSpeech(Move.REVIEW_CHAR.value, numberOfTimes=1)
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

	if reportedAfterLast == EndSpeech.NONE:
		return
	# ensure all content tested, ie the end of the sample should be reached
	finalItem = expectedSpeech[-1]
	endReached = f"{reportedAfterLast.value}\n{finalItem}"
	actual = _pressKeyAndCollectSpeech(navKey.value, 1)
	_builtIn.should_be_equal(
		actual,
		[endReached, ],
		msg=f"End reached failure. actual vs expected. With symbolLevel {symbolLevel}"
	)


def test_tableHeaders():
	"""
	Announce the correct line when placed at the end of a link at the end of a list item in a contenteditable
	"""
	_chrome: _ChromeLib = _getLib("ChromeLib")
	_chrome.prepareChrome(
		r"""
			<table>
				<tr>
					<th>First-name</th>
					<th>➔ 👕</th>
					<th>Don't</th>
				</tr>
				<tr>
					<td>a</td>
					<td>b</td>
					<td>c</td>
				</tr>
			</table>
		"""
	)
	_setSymbolLevel(SymLevel.ALL)
	# Expected to be in browse mode
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		# into the table, describe first column header
		"table  with 2 rows and 3 columns  row 1  column 1  First dash name"
	)
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		# describe second column header
		"column 2  right-pointing arrow   t-shirt"
	)
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		# describe third column header
		"column 3  Don tick t"
	)
	# into the first (non-header) row
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		# describe third column header
		"row 2  First dash name  column 1  a"
	)

	_doTest(
		navKey=Move.CARET_CHAR,
		symbolLevel=SymLevel.NONE,
		reportedAfterLast=EndSpeech.NONE,
		expectedSpeech=[
			't-shirt  column 2\nb',
			"Don't  column 3\nc",
		]
	)
	# reset to start of row.
	_NvdaLib.getSpeechAfterKey(Move.CARET_CHAR_BACK.value)
	_NvdaLib.getSpeechAfterKey(Move.CARET_CHAR_BACK.value)

	_doTest(
		navKey=Move.CARET_CHAR,
		symbolLevel=SymLevel.ALL,
		reportedAfterLast=EndSpeech.NONE,
		expectedSpeech=[
			'right-pointing arrow   t-shirt  column 2\nb',
			"Don tick t  column 3\nc",
		]
	)
