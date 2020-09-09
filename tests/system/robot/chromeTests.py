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
			<ul style="list-style-type:none">
				<li>xy</li>
				<li>z</li>
			</ul>
		"""
	)
	# Ensure that moving into a list by line, "list item" is not reported.
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"list  with 2 items  xy"
	)
	# Ensure that when moving by character (rightArrow)
	# within the list item, "list item" is not announced.
	actualSpeech = _chrome.getSpeechAfterKey("rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"y"
	)
	# Ensure that when moving by character (rightArrow)
	# onto the next list item, "list item" is reported.
	actualSpeech = _chrome.getSpeechAfterKey("rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"list item  level 1  \nz"
	)
	# Ensure that when moving by character (leftArrow)
	# onto the previous list item, "list item" is reported.
	actualSpeech = _chrome.getSpeechAfterKey("leftArrow")
	_asserts.strings_match(
		actualSpeech,
		"list item  level 1  \ny"
	)
