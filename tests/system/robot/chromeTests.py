# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Logic for NVDA + Google Chrome tests
"""

from robot.libraries.BuiltIn import BuiltIn
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from SystemTestSpy import (
	_getLib,
)

# Imported for type information
from ChromeLib import ChromeLib as _ChromeLib
from AssertsLib import AssertsLib as _AssertsLib

_builtIn: BuiltIn = BuiltIn()
_chrome: _ChromeLib = _getLib("ChromeLib")
_asserts: _AssertsLib = _getLib("AssertsLib")


def checkbox_labelled_by_inner_element():
	_chrome.prepareChrome(
		r"""
			<div tabindex="0" role="checkbox" aria-labelledby="inner-label">
				<div style="display:inline" id="inner-label">
					Simulate evil cat
				</div>
			</div>
		"""
	)
	actualSpeech = _chrome.getSpeechAfterTab()
	_asserts.strings_match(
		actualSpeech,
		# The name for the element is also in it's content, the name is spoken twice:
		# "Simulate evil cat  Simulate evil cat  check box  not checked"
		# Instead this should be spoken as:
		"Simulate evil cat  check box  not checked"
	)


def announce_list_item_when_moving_by_word_or_character():
	_chrome.prepareChrome(
		r"""
			<div contenteditable="true">
				<p>Before list</p>
				<ul style="list-style-type:none">
					<li>small cat</li>
					<li>big dog</li>
				</ul>
			</div>
		"""
	)
	# Force focus mode
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+space")
	_asserts.strings_match(
		actualSpeech,
		"Focus mode"
	)
	# Tab into the contenteditable
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		"section  multi line  editable  Before list"
	)
	# Ensure that moving into a list by line, "list item" is not reported.
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"list  small cat"
	)
	# Ensure that when moving by word (control+rightArrow)
	# within the list item, "list item" is not announced.
	actualSpeech = _chrome.getSpeechAfterKey("control+rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"cat"
	)
	# Ensure that when moving by character (rightArrow)
	# within the list item, "list item" is not announced.
	actualSpeech = _chrome.getSpeechAfterKey("rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"a"
	)
	# move to the end of the line (and therefore the list item)
	actualSpeech = _chrome.getSpeechAfterKey("end")
	_asserts.strings_match(
		actualSpeech,
		"blank"
	)
	# Ensure that when moving by character (rightArrow)
	# onto the next list item, "list item" is reported.
	actualSpeech = _chrome.getSpeechAfterKey("rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"\n".join([
			"list item  level 1  ",
			"b"
		])
	)
	# Ensure that when moving by character (leftArrow)
	# onto the previous list item, "list item" is reported.
	# Note this places us on the end-of-line insertion point of the previous list item.
	actualSpeech = _chrome.getSpeechAfterKey("leftArrow")
	_asserts.strings_match(
		actualSpeech,
		"list item  level 1"
	)
	# Ensure that when moving by word (control+rightArrow)
	# onto the next list item, "list item" is reported.
	actualSpeech = _chrome.getSpeechAfterKey("control+rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"list item  level 1  big"
	)
	# Ensure that when moving by word (control+leftArrow)
	# onto the previous list item, "list item" is reported.
	# Note this places us on the end-of-line insertion point of the previous list item.
	actualSpeech = _chrome.getSpeechAfterKey("control+leftArrow")
	_asserts.strings_match(
		actualSpeech,
		"list item  level 1"
	)


def test_i7562():
	""" List should not be announced on every line of a ul in a contenteditable """
	_chrome.prepareChrome(
		r"""
			<div contenteditable="true">
				<p>before</p>
				<ul>
					<li>frogs</li>
					<li>birds</li>
				</ul>
				<p>after</p>
			</div>
		"""
	)
	# Force focus mode
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+space")
	_asserts.strings_match(
		actualSpeech,
		"Focus mode"
	)
	# Tab into the contenteditable
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		"section  multi line  editable  before"
	)
	# DownArow into the list. 'list' should be announced when entering.
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"list  bullet  frogs"
	)
	# DownArrow to the second list item. 'list' should not be announced.
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"bullet  birds"
	)
	# DownArrow out of the list. 'out of list' should be announced.
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"out of list  after",
	)


def test_pr11606():
	"""
	Announce the correct line when placed at the end of a link at the end of a list item in a contenteditable
	"""
	_chrome.prepareChrome(
		r"""
			<div contenteditable="true">
				<ul>
					<li><a href="#">A</a> <a href="#">B</a></li>
					<li>C D</li>
				</ul>
			</div>
		"""
	)
	# Force focus mode
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+space")
	_asserts.strings_match(
		actualSpeech,
		"Focus mode"
	)
	# Tab into the contenteditable
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		"section  multi line  editable  list  bullet  link  A    link  B"
	)
	# move past the end of the first link.
	# This should not be affected due to pr #11606.
	actualSpeech = _chrome.getSpeechAfterKey("rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"\n".join([
			"out of link  ",
			"space"
		])
	)
	# Move to the end of the line (which is also the end of the second link)
	# Before pr #11606 this would have announced the bullet on the next line.
	actualSpeech = _chrome.getSpeechAfterKey("end")
	_asserts.strings_match(
		actualSpeech,
		"link"
	)
	# Read the current line.
	# Before pr #11606 the next line ("C D")  would have been read.
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+upArrow")
	_asserts.strings_match(
		actualSpeech,
		"bullet  link  A    link  B"
	)
