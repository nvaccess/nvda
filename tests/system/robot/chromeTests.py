# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2021 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Logic for NVDA + Google Chrome tests
"""

import os
from robot.libraries.BuiltIn import BuiltIn
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from SystemTestSpy import (
	_getLib,
)

# Imported for type information
from ChromeLib import ChromeLib as _ChromeLib
from AssertsLib import AssertsLib as _AssertsLib
import NvdaLib as _NvdaLib

_builtIn: BuiltIn = BuiltIn()
_chrome: _ChromeLib = _getLib("ChromeLib")
_asserts: _AssertsLib = _getLib("AssertsLib")


ARIAExamplesDir = os.path.join(
	_NvdaLib._locations.repoRoot, "include", "w3c-aria-practices", "examples"
)


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


def test_aria_details():
	_chrome.prepareChrome(
		"""
		<div>
			<p>The word <mark aria-details="cat-details">cat</mark> has a comment tied to it.</p>
			<div id="cat-details" role="comment">
				Cats go woof BTW<br>&mdash;Jonathon Commentor
				<div role="comment">
				No they don't<br>&mdash;Zara
				</div>
				<div role="form">
				<textarea cols="80" placeholder="Add reply..."></textarea>
				<input type="submit">
				</div>
			</div>
		</div>
		"""
	)
	actualSpeech = _chrome.getSpeechAfterKey('downArrow')
	_asserts.strings_match(
		actualSpeech,
		"The word  marked content  cat  out of marked content  has a comment tied to it."
	)
	# this word has no details attached
	actualSpeech = _chrome.getSpeechAfterKey("control+rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"word"
	)
	# check that there is no summary reported
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+\\")
	_asserts.strings_match(
		actualSpeech,
		"No additional details"
	)
	# this word has details attached to it
	actualSpeech = _chrome.getSpeechAfterKey("control+rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"marked content  cat  out of marked content"
	)
	# read the details summary
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+\\")
	_asserts.strings_match(
		actualSpeech,
		"Cats go woof BTW  Jonathon Commentor No they don't  Zara Submit"
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
			"list item  level 1",
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
			"out of link",
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


def test_ariaTreeGrid_browseMode():
	"""
	Ensure that ARIA treegrids are accessible as a standard table in browse mode.
	"""
	_asserts.strings_match("foo", "bar")
	testFile = os.path.join(ARIAExamplesDir, "treegrid", "treegrid-1.html")
	_chrome.prepareChrome(
		f"""
			<iframe src="{testFile}"></iframe>
		"""
	)
	# Jump to the first heading in the iframe.
	actualSpeech = _chrome.getSpeechAfterKey("h")
	_asserts.strings_match(
		actualSpeech,
		"frame  main landmark  Treegrid Email Inbox Example  heading  level 1"
	)
	# Tab to the first link.
	# This ensures that focus is totally within the iframe
	# so as to not cause focus to hit the iframe's document
	# when entering focus mode on the treegrid later.
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		"issue 790.  link"
	)
	# Jump to the ARIA treegrid with the next table quicknav command.
	# The browse mode caret will be inside the table on the caption before the first row.
	actualSpeech = _chrome.getSpeechAfterKey("t")
	_asserts.strings_match(
		actualSpeech,
		"Inbox  table  clickable  with 5 rows and 3 columns  Inbox"
	)
	# Move past the caption onto row 1 with downArrow
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"row 1  Subject  column 1  Subject"
	)
	# Navigate to row 2 column 1 with NVDA table navigation command
	actualSpeech = _chrome.getSpeechAfterKey("control+alt+downArrow")
	_asserts.strings_match(
		actualSpeech,
		"expanded  level 1  row 2  Treegrids are awesome"
	)
	# Press enter to activate NVDA focus mode and focus the current row
	actualSpeech = _chrome.getSpeechAfterKey("enter")
	_asserts.strings_match(
		actualSpeech,
		"\n".join([
			# focus mode turns on
			"Focus mode",
			# Focus enters the ARIA treegrid (table)
			"Inbox  table",
			# Focus lands on row 2
			"level 1  Treegrids are awesome Want to learn how to use them? aaron at thegoogle dot rocks  expanded",
		])
	)


def ARIAInvalid_spellingAndGrammar():
	"""
	Tests ARIA invalid values of "spelling", "grammar" and "spelling, grammar".
	Please note that although IAccessible2 allows multiple values for invalid,
	multiple values to aria-invalid is not yet standard.
	And even if it were, they would be separated by space, not comma
thus the html for this test would need to change,
	but the expected output shouldn't need to.
	"""
	_chrome.prepareChrome(
		r"""
			<p>Big <span aria-invalid="spelling">caat</span> meos</p>
			<p>Small <span aria-invalid="grammar">a dog</span> woofs</p>
			<p>Fat <span aria-invalid="grammar, spelling">a ffrog</span> crokes</p>
		"""
	)
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"Big  spelling error  caat  meos"
	)
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"Small  grammar error  a dog  woofs"
	)
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"Fat  spelling error  grammar error  a ffrog  crokes"
	)


def test_ariaCheckbox_browseMode():
	"""
	Navigate to an unchecked checkbox in reading mode.
	"""
	testFile = os.path.join(ARIAExamplesDir, "checkbox", "checkbox-1", "checkbox-1.html")
	_chrome.prepareChrome(
		f"""
			<iframe src="{testFile}"></iframe>
		"""
	)
	# Jump to the first heading in the iframe.
	actualSpeech = _chrome.getSpeechAfterKey("h")
	_asserts.strings_match(
		actualSpeech,
		"frame  main landmark  Checkbox Example (Two State)  heading  level 1"
	)
	# Navigate to the checkbox.
	actualSpeech = _chrome.getSpeechAfterKey("x")
	_asserts.strings_match(
		actualSpeech,
		"Sandwich Condiments  grouping  list  with 4 items  Lettuce  check box  not checked"
	)


def test_i12147():
	"""
	New focus target should be announced if the triggering element is removed when activated.
	"""
	_chrome.prepareChrome(
		f"""
			<div>
			  <button id='trigger0'>trigger 0</button>
			  <h4 id='target0' tabindex='-1'>target 0</h4>
			</div>
			<script>
				let trigger0 = document.querySelector('#trigger0');
				trigger0.addEventListener('click', e => {{
				  let focusTarget = document.querySelector('#target0');
				  trigger0.remove();
				  focusTarget.focus();
				}})
			</script>
		"""
	)
	# Jump to the first button (the trigger)
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		"trigger 0  button"
	)
	# Activate the button, we should hear the new focus target.
	actualSpeech = _chrome.getSpeechAfterKey("enter")
	_asserts.strings_match(
		actualSpeech,
		"target 0  heading  level 4"
	)


def test_tableInStyleDisplayTable():
	"""
	Chrome treats nodes with `style="display: table"` as tables.
	When a HTML style table is positioned in such a node, NVDA was previously unable to announce
	table row and column count as well as provide table navigation for the inner table.
	"""
	_chrome.prepareChrome(
		"""
			<p>Paragraph</p>
			<div style="display:table">
				<table>
					<thead>
						<tr>
							<th>First heading</th>
							<th>Second heading</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>First content cell</td>
							<td>Second content cell</td>
						</tr>
					</tbody>
				</table>
			</div>
		"""
	)
	# Jump to the table
	actualSpeech = _chrome.getSpeechAfterKey("t")
	_asserts.strings_match(
		actualSpeech,
		"table  with 2 rows and 2 columns  row 1  First heading  column 1  First heading"
	)
	nextActualSpeech = _chrome.getSpeechAfterKey("control+alt+downArrow")
	_asserts.strings_match(
		nextActualSpeech,
		"row 2  First content cell"
	)
