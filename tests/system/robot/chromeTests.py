# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2022 NV Access Limited, Leonard de Ruijter, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Logic for NVDA + Google Chrome tests
"""

import typing
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

if typing.TYPE_CHECKING:
	from ..libraries.SystemTestSpy.speechSpyGlobalPlugin import NVDASpyLib


#: Double space is used to separate semantics in speech output this typically
# adds a slight pause to the synthesizer.
SPEECH_SEP = "  "
SPEECH_CALL_SEP = '\n'
#: single space is used to separate semantics in braille output.
BRAILLE_SEP = " "

ARIAPatternsDir = os.path.join(
	_NvdaLib._locations.repoRoot,
	"include",
	"w3c-aria-practices",
	"content",
	"patterns",
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


REVIEW_CURSOR_FOLLOW_CARET_KEY = ["reviewCursor", "followCaret"]
REVIEW_CURSOR_FOLLOW_FOCUS_KEY = ["reviewCursor", "followFocus"]
READ_DETAILS_GESTURE = "NVDA+d"


def _getNoVBuf_AriaDetails_sample() -> str:
	return """
		<div role="application">
			<button>focus in app</button>
			<p>this is an application, it contains a button with details</p>
			<button aria-details="button-details">push me</button>
		</div>
		<div id="button-details" role="note">
			<p>Press to self-destruct</p>
		</div>
		"""


def _doTestAriaDetails_NoVBufNoTextInterface(nvdaConfValues: "NVDASpyLib.NVDAConfMods"):
	_chrome.prepareChrome(_getNoVBuf_AriaDetails_sample())
	spy: "NVDASpyLib" = _NvdaLib.getSpyLib()
	spy.modifyNVDAConfig(nvdaConfValues)

	actualSpeech = _NvdaLib.getSpeechAfterKey("tab")
	_builtIn.should_contain(actualSpeech, "focus in app")

	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("tab")
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"push me",
			"button",
			"has details",
		]),
		message="Tab to button"
	)
	_asserts.braille_matches(
		actualBraille,
		"push me btn details",
		message="Tab to button",
	)
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey(READ_DETAILS_GESTURE)
	_asserts.speech_matches(
		actualSpeech,
		"Press to self-destruct",
		message="Report details"
	)
	_asserts.braille_matches(
		actualBraille,
		"Press to self-destruct",
		message="Report details",
	)


def test_aria_details_noVBufNoTextInterface():
	"""The uncommon case, but for completeness, a role=application containing an element that does not have a text
	interface.
	"""
	_doTestAriaDetails_NoVBufNoTextInterface(
		nvdaConfValues=[
			(REVIEW_CURSOR_FOLLOW_CARET_KEY, True),
			(REVIEW_CURSOR_FOLLOW_FOCUS_KEY, True),
	])


def test_aria_details_noVBufNoTextInterface_freeReview():
	"""The uncommon case, but for completeness, a role=application containing an element without a text
	interface. Test with the review cursor configured not to follow focus or caret.
	"""
	_doTestAriaDetails_NoVBufNoTextInterface(
		nvdaConfValues=[
			(REVIEW_CURSOR_FOLLOW_CARET_KEY, False),
			(REVIEW_CURSOR_FOLLOW_FOCUS_KEY, False),
	])


def test_mark_aria_details():
	exercise_mark_aria_details(
		nvdaConfValues=[
			(REVIEW_CURSOR_FOLLOW_CARET_KEY, True),
			(REVIEW_CURSOR_FOLLOW_FOCUS_KEY, True),
	])


def test_mark_aria_details_FreeReviewCursor():
	exercise_mark_aria_details(
		nvdaConfValues=[
			(REVIEW_CURSOR_FOLLOW_CARET_KEY, False),
			(REVIEW_CURSOR_FOLLOW_FOCUS_KEY, False),
	])


def test_mark_aria_details_role():
	_chrome.prepareChrome(
		"""
		<div class="editor" contenteditable spellcheck="false" role="textbox" aria-multiline="true">
			<p>
				<span aria-details="endnote-details">doc-endnote,</span>
				<span aria-details="footnote-details">doc-footnote,</span>
				<span aria-details="comment-details">comment,</span>
				<span aria-details="definition-details-as-tag" role="term">definition,</span>
				<span aria-details="definition-details-as-role" role="term">definition,</span>
				<span aria-details="unknown-details">form</span>
			</p>
		</div>
		<div>
			<p>
				<!-- Supported by Chrome attribute details-roles -->
				<div id="endnote-details" role="doc-endnote">details with role doc-endnote</div>
				<div id="footnote-details" role="doc-footnote">details with role doc-footnote</div>
				<div id="comment-details" role="comment">details with role comment</div>
				<!--
					When using the following syntax, the dfn tag holds the role "term",
					and the accompanying text becomes the "definition".
					Authors may expected the aria-details to target the definition.
					It is uncertain as to which element aria-details
					should point towards, but we assume the dfn tag in this case,
					as the accompanying definition text is not specifically captured by an HTML element.
				-->
				<p>
					<dfn id="definition-details-as-tag">definition</dfn>:
					details with tag definition
				</p>
				<!--
					Authors may expected the aria-details to target the definition.
					As the definition text is specifically captured by an HTML element with role "definition",
					we map to that element.
					This is inconsistent with previous example, using the dfn tag.
				-->
				<p>
					<span role="term">definition</span>:
					<span id="definition-details-as-role" role="definition">details with role definition</span>
				</p>
				<!-- Included as "form" is not supported by Chrome attribute details-roles -->
				<div id="unknown-details" role="form">details with role form</div>
			</p>
		</div>
		"""
	)
	expectedSpeech = SPEECH_SEP.join([
		"edit",
		"multi line",
		# the role doc-endnote is unsupported as an IA2 role
		# The role "ROLE_LIST_ITEM" is used instead
		"has details",
		"doc-endnote,",
		"",  # space between spans
		"has foot note",
		"doc-footnote,",
		"",  # space between spans
		"has comment",
		"comment,",
		"",  # space between spans
		# the role definition is unsupported as an IA2 role
		# The role "ROLE_PARAGRAPH" is used instead
		"has details",
		"definition,",
		"",  # space between spans
		"has details",
		"definition,",
		"",  # space between spans
		# The role "form" is deliberately unsupported
		"has details",
		"form",
	])
	_spy: NVDASpyLib = _NvdaLib.getSpyLib()
	_spy.setBrailleCellCount(400)

	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey('downArrow')

	_asserts.speech_matches(
		actualSpeech,
		expectedSpeech,
		message="Browse mode speech: Read line with different aria details roles."
	)
	_asserts.braille_matches(
		message="Browse mode braille: Read line with different aria details roles.",
		actual=actualBraille,
		expected=" ".join([
			"mln",
			"edt ",
			# the role doc-endnote is unsupported as an IA2 role
			# The role "ROLE_LIST_ITEM" is used instead
			"details",
			"doc-endnote,",
			" ",  # space between spans
			"has fnote",
			"doc-footnote,",
			" ",  # space between spans
			"has cmnt",
			"comment,",
			" ",  # space between spans
			# the role definition is unsupported as an IA2 role
			# The role "ROLE_PARAGRAPH" is used instead
			"details",
			"definition,",
			" ",  # space between spans
			"details",
			"definition,",
			" ",
			"details",
			"form",
			"edt end",
		])
	)
	
	# Reset caret
	actualSpeech = _NvdaLib.getSpeechAfterKey("upArrow")
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"out of edit",
			"Test page load complete",
		]),
		message="reset caret",
	)

	# Force focus mode
	actualSpeech = _NvdaLib.getSpeechAfterKey("NVDA+space")
	_asserts.speech_matches(
		actualSpeech,
		"Focus mode",
		message="force focus mode",
	)

	# Tab into the contenteditable
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("tab")
	_asserts.speech_matches(
		actualSpeech,
		expectedSpeech,
		message="Focus mode speech: Read line with different aria details roles"
	)
	_asserts.braille_matches(
		message="Focus mode braille: Read line with different aria details roles",
		actual=actualBraille,
		expected=" ".join([
			# no "mln edt"
			# the role doc-endnote is unsupported as an IA2 role
			# The role "ROLE_LIST_ITEM" is used instead
			"details",
			"doc-endnote,",
			" ",  # space between spans
			"has fnote",
			"doc-footnote,",
			" ",  # space between spans
			"has cmnt",
			"comment,",
			" ",  # space between spans
			# the role definition is unsupported as an IA2 role
			# The role "ROLE_PARAGRAPH" is used instead
			"details",
			"definition,",
			" ",  # space between spans
			"details",
			"definition,",
			" ",
			"details",
			"form",
			# "edt end",
		])
	)


def exercise_mark_aria_details(nvdaConfValues: "NVDASpyLib.NVDAConfMods"):
	_chrome.prepareChrome(
		"""
		<div class="editor" contenteditable spellcheck="false" role="textbox" aria-multiline="true">
			<p>The word <mark aria-details="cat-details">cat</mark> has a comment tied to it.</p>
		</div>
		<p>Hello <span
			aria-details="link-details"
			role="mark">this is a <a href="https://www.google.com/">test</a></span></p>
		<div>
			<div id="cat-details" role="comment">Cats go woof BTW<br>&mdash;Jonathon Commentor
				<div role="comment">No they don't<br>&mdash;Zara</div>
			</div>
			<div role="form">
				<textarea cols="80" placeholder="Add reply..."></textarea>
				<input type="submit">
			</div>
		</div>
		<div id="link-details" role="note">
			<p>Nested in a container</p>
		</div>
		"""
	)
	spy: "NVDASpyLib" = _NvdaLib.getSpyLib()
	spy.modifyNVDAConfig(nvdaConfValues)

	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey('downArrow')
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"edit",
			"multi line",
			"The word",  # content
			"highlighted",
			"has comment",
			"cat",  # highlighted content
			"out of highlighted",
			"has a comment tied to it.",  # content
		]),
		message="Browse mode: Read line with details."
	)
	_asserts.braille_matches(
		actualBraille,
		"mln edt The word  hlght has cmnt cat hlght end  has a comment tied to it. edt end",
		message="Browse mode: Read line with details.",
	)
	# this word has no details attached
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("control+rightArrow")
	_asserts.speech_matches(
		actualSpeech,
		"word",
		message="Browse mode: Move by word to word without details"
	)
	_asserts.braille_matches(
		actualBraille,
		"mln edt The word  hlght has cmnt cat hlght end  has a comment tied to it. edt end",
		message="Browse mode: Move by word to word without details",
	)

	# check that there is no summary reported
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey(READ_DETAILS_GESTURE)
	_asserts.speech_matches(
		actualSpeech,
		"No additional details",
		message="Browse mode: Report details on word without details"
	)
	_asserts.braille_matches(
		actualBraille,
		"No additional details",
		message="Browse mode: Report details on word without details",
	)
	# this word has a comment attached to it
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("control+rightArrow")
	_asserts.speech_matches(
		actualSpeech,
		"highlighted  has comment  cat  out of highlighted",
		message="Browse mode: Move by word to word with details",
	)
	_asserts.braille_matches(
		actualBraille,
		"mln edt The word  hlght has cmnt cat hlght end  has a comment tied to it. edt end",
		message="Browse mode: Move by word to word with details",
	)
	# read the details summary
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey(READ_DETAILS_GESTURE)
	_asserts.speech_matches(
		actualSpeech,
		"Cats go woof BTW —Jonathon Commentor No they don't —Zara",
		message="Browse mode: Report details on word with details"
	)
	_asserts.braille_matches(
		actualBraille,
		"Cats go woof BTW\n—Jonathon CommentorNo they don't\n—Zara",
		message="Browse mode: Report details on word with details",
	)

	# move down to the link nested in a container with details
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("downArrow")
	_asserts.speech_matches(
		actualSpeech,
		"out of edit  Hello  highlighted  has details  this is a  link  test",
		message="Browse mode: Move by line to paragraph with link nested in a container with details",
	)
	_asserts.braille_matches(
		actualBraille,
		"Hello  hlght details this is a  lnk test hlght end",
		message="Browse mode: Move by line to paragraph with link nested in a container with details",
	)
	# Jump to the link from same line
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("k")
	_asserts.speech_matches(
		actualSpeech,
		"test  link",
		message="Browse mode: From same line jump to link nested in a container with details",
	)
	_asserts.braille_matches(
		actualBraille,
		"Hello  hlght details this is a  lnk test hlght end",
		message="Browse mode: From same line jump to link nested in a container with details",
	)

	# reset to prior line before jump to the link from different line
	actualSpeech = _NvdaLib.getSpeechAfterKey('upArrow')
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"out of highlighted",  # Leaving the highlighted link
			"edit",
			"multi line",
			"The word",  # content
			"highlighted",
			"has comment",
			"cat",  # highlighted content
			"out of highlighted",
			"has a comment tied to it.",  # content
		]),
		message="Browse mode: Reset to prior line before jump to the link."
	)
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("k")
	_asserts.speech_matches(
		actualSpeech,
		"highlighted  has details  test  link",
		message="Browse mode: From prior line jump to link nested in a container with details",
	)
	_asserts.braille_matches(
		actualBraille,
		"Hello  hlght details this is a  lnk test hlght end",
		message="Browse mode: From prior line jump to link nested in a container with details",
	)
	# read the details summary
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey(READ_DETAILS_GESTURE)
	_asserts.speech_matches(
		actualSpeech,
		"No additional details",
		message="Browse mode: Report details on nested link with details"
	)
	_asserts.braille_matches(
		actualBraille,
		"No additional details",
		message="Browse mode: Report details on nested link with details"
	)

	# Reset caret
	actualSpeech = _NvdaLib.getSpeechAfterKey("upArrow")
	actualSpeech = _NvdaLib.getSpeechAfterKey("upArrow")
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"out of edit",
			"Test page load complete",
		]),
		message="reset caret",
	)

	# Force focus mode
	actualSpeech = _NvdaLib.getSpeechAfterKey("NVDA+space")
	_asserts.speech_matches(
		actualSpeech,
		"Focus mode",
		message="force focus mode",
	)

	# Tab into the contenteditable
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("tab")
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"edit",
			"multi line",
			"The word",  # content
			"highlighted",
			"has comment",
			"cat",  # highlighted content
			"out of highlighted",
			"has a comment tied to it.",  # content
		]),
		message="Focus mode: report content editable with details"
	)
	_asserts.braille_matches(
		actualBraille,
		"The word  hlght has cmnt cat hlght end  has a comment tied to it.",
		message="Focus mode: report content editable with details",
	)

	# Try to read the details
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey(READ_DETAILS_GESTURE)
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"No additional details",
		]),
		message="Focus mode: Try to read details, caret not on details word.",
	)
	_asserts.braille_matches(
		actualBraille,
		"No additional details",
		message="Focus mode: Try to read details, caret not on details word.",
	)

	# move to the word with details: "cat"
	_NvdaLib.getSpeechAfterKey("control+rightArrow")
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("control+rightArrow")
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"highlighted",
			"has comment",
			"cat",  # highlighted content
			"out of highlighted",
		]),
		message="Focus mode: Move by word to word with details"
	)
	_asserts.braille_matches(
		actualBraille,
		expected="The word  hlght has cmnt cat hlght end  has a comment tied to it.",
		message="Focus mode: Move by word to word with details",
	)

	# Try to read the details
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey(READ_DETAILS_GESTURE)
	_asserts.speech_matches(
		actualSpeech,
		"Cats go woof BTW —Jonathon Commentor No they don't —Zara",
		message="Focus mode:  Report details on word with details.",
	)
	_asserts.braille_matches(
		actualBraille,
		expected="Cats go woof BTW\n—Jonathon CommentorNo they don't\n—Zara",
		message="Focus mode:  Report details on word with details.",
	)

	# Tab to the link
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("tab")
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_CALL_SEP.join([
			SPEECH_SEP.join([
				"highlighted",
				"has details",
			]),
			SPEECH_SEP.join([
				"test",
				"link",
			])
		]),
		message="Focus mode: tab to link nested in container with details",
	)
	_asserts.braille_matches(
		actualBraille,
		"hlght details test lnk",
		message="Focus mode: tab to link nested in container with details"
	)

	# Try to read the details
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey(READ_DETAILS_GESTURE)
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"No additional details",
		]),
		message="Focus mode: Try to read details, link nested in container with details.",
	)
	_asserts.braille_matches(
		actualBraille,
		"No additional details",
		message="Focus mode: Try to read details, link nested in container with details.",
	)


def test_annotations_multi_target():
	_chrome.prepareChrome(
		"""
		<div class="editor" contenteditable spellcheck="false" role="textbox" aria-multiline="true">
			<span aria-details="footnote-details comment-details form-details">example origin</span>
		</div>
		<div>
			<p>
				<div id="footnote-details" role="doc-footnote">example footnote</div>
				<div id="comment-details" role="comment">example comment</div>
				<div id="form-details" role="form">example form</div>
			</p>
		</div>
		"""
	)
	expectedSpeechParts = [
		"has foot note",
		"has comment",
		"has details",  # The role "form" is deliberately unsupported
		"example origin",
	]
	expectedBrailleParts = [
		"has fnote",
		"has cmnt",
		"details",  # The role "form" is deliberately unsupported
		"example origin",
	]
	_spy: NVDASpyLib = _NvdaLib.getSpyLib()
	_spy.setBrailleCellCount(400)

	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey('downArrow')

	# Order of annotation announcement is non-deterministic, so do not consider order with testing
	_asserts.speech_contains(
		actualSpeech,
		expectedSpeechParts,
		message="Browse mode speech: Read line with different aria details roles."
	)
	_asserts.braille_contains(
		actualBraille,
		expectedBrailleParts,
		message="Browse mode braille: Read line with different aria details roles.",
	)
	
	# Reset caret
	actualSpeech = _NvdaLib.getSpeechAfterKey("upArrow")
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"out of edit",
			"Test page load complete",
		]),
		message="reset caret",
	)

	# Force focus mode
	actualSpeech = _NvdaLib.getSpeechAfterKey("NVDA+space")
	_asserts.speech_matches(
		actualSpeech,
		"Focus mode",
		message="force focus mode",
	)

	# Tab into the contenteditable
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("tab")
	# Order of annotation announcement is non-deterministic, so do not consider order with testing
	_asserts.speech_contains(
		actualSpeech,
		expectedSpeechParts,
		message="Focus mode speech: Read line with different aria details roles"
	)
	_asserts.braille_contains(
		actualBraille,
		expectedBrailleParts,
		message="Focus mode braille: Read line with different aria details roles",
	)

	# Order of annotation announcement is non-deterministic, so do not consider order with testing
	collectedSpeech = []
	collectedBraille = []
	expectedSummaries = [f"example {x}" for x in ("footnote", "comment", "form")]
	for _ in range(len(expectedSummaries)):
		actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey(READ_DETAILS_GESTURE)
		collectedSpeech.append(actualSpeech)
		collectedBraille.append(actualBraille)
	
	_builtIn.should_be_equal(
		sorted(collectedSpeech),
		sorted(expectedSummaries),
	)
	_builtIn.should_be_equal(
		sorted(collectedBraille),
		sorted(expectedSummaries),
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
		SPEECH_CALL_SEP.join([
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
		SPEECH_CALL_SEP.join([
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
	testFile = os.path.join(ARIAPatternsDir, "treegrid", "examples", "treegrid-1.html")
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
		"Treegrid Pattern  link"
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
		"row 1  column 1  Subject"
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
		SPEECH_CALL_SEP.join([
			# focus mode turns on
			"Focus mode",
			# Focus enters the ARIA treegrid (table)
			"Inbox  table",
			# Focus lands on row 2
			SPEECH_SEP.join([
				"level 1",
				"Treegrids are awesome Want to learn how to use them? aaron at thegoogle dot rocks",
				"expanded",
				"1 of 1"
			]),
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
	testFile = os.path.join(ARIAPatternsDir, "checkbox", "examples", "checkbox.html")
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
		"""
			<div>
			  <button id='trigger0'>trigger 0</button>
			  <h4 id='target0' tabindex='-1'>target 0</h4>
			</div>
			<script>
				let trigger0 = document.querySelector('#trigger0');
				trigger0.addEventListener('click', e => {
				  let focusTarget = document.querySelector('#target0');
				  trigger0.remove();
				  focusTarget.focus();
				})
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
		"table  with 2 rows and 2 columns  row 1  column 1  First heading"
	)
	nextActualSpeech = _chrome.getSpeechAfterKey("control+alt+downArrow")
	_asserts.strings_match(
		nextActualSpeech,
		"row 2  First content cell"
	)


def test_ariaRoleDescription_focus():
	"""
	NVDA should report the custom role of an object on focus.
	"""
	_chrome.prepareChrome(
		"""
		<button aria-roledescription="pizza">Cheese</button><br />
		<button aria-roledescription="pizza">Meat</button>
		"""
	)
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		"Cheese  pizza"
	)
	# Force focus mode
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+space")
	_asserts.strings_match(
		actualSpeech,
		"Focus mode"
	)
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		"Meat  pizza"
	)


def test_ariaRoleDescription_inline_browseMode():
	"""
	NVDA should report the custom role for inline elements in browse mode.
	"""
	_chrome.prepareChrome(
		"""
		<p>Start
		<img aria-roledescription="drawing" alt="Our logo" src="https://www.nvaccess.org/images/logo.png" />
		End</p>
		"""
	)
	# When reading the entire line,
	# entering the custom role should be reported,
	# but not exiting
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"Start  drawing  Our logo  End"
	)
	# When reading the line by word,
	# Both entering and exiting the custom role should be reported.
	actualSpeech = _chrome.getSpeechAfterKey("control+rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"drawing  Our"
	)
	actualSpeech = _chrome.getSpeechAfterKey("control+rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"logo  out of drawing"
	)
	actualSpeech = _chrome.getSpeechAfterKey("control+rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"End"
	)


def test_ariaRoleDescription_block_browseMode():
	"""
	NVDA should report the custom role at start and end for block elements in browse mode.
	"""
	_chrome.prepareChrome(
		"""
		<aside aria-roledescription="warning">
		<p>Wet paint!</p>
		<p>Please be careful.</p>
		</aside>
		<p>End</p>
		"""
	)
	# when reading the page by line,
	# both entering and exiting the custom role should be reported.
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"warning  Wet paint!"
	)
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"Please be careful."
	)
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"out of warning  End"
	)


def test_ariaRoleDescription_inline_contentEditable():
	"""
	NVDA should report the custom role for inline elements in content editables.
	"""
	_chrome.prepareChrome(
		"""
		<div contenteditable="true">
		<p>Top line</p>
		<p>Start
		<img aria-roledescription="drawing" alt="Our logo" src="https://www.nvaccess.org/images/logo.png" />
		End</p>
		</div>
		"""
	)
	# Force focus mode
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+space")
	_asserts.strings_match(
		actualSpeech,
		"Focus mode"
	)
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		"section  multi line  editable  Top line"
	)
	# When reading the entire line,
	# entering the custom role should be reported,
	# but not exiting
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"Start  drawing  Our logo    End"
	)
	# When reading the line by word,
	# Both entering and exiting the custom role should be reported.
	actualSpeech = _chrome.getSpeechAfterKey("control+rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"drawing  Our logo    out of drawing"
	)
	actualSpeech = _chrome.getSpeechAfterKey("control+rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"End"
	)


def test_ariaRoleDescription_block_contentEditable():
	"""
	NVDA should report the custom role at start and end for block elements in content editables.
	"""
	_chrome.prepareChrome(
		"""
		<div contenteditable="true">
		<p>Top line</p>
		<aside aria-roledescription="warning">
		<p>Wet paint!</p>
		<p>Please be careful.</p>
		</aside>
		<p>End</p>
		</div>
		"""
	)
	# Force focus mode
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+space")
	_asserts.strings_match(
		actualSpeech,
		"Focus mode"
	)
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		"section  multi line  editable  Top line"
	)
	# when reading the page by line,
	# both entering and exiting the custom role should be reported.
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"warning  Wet paint!"
	)
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"Please be careful."
	)
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"out of warning  End"
	)


def _getAriaDescriptionSample() -> str:
	annotation = "User nearby, Aaron"
	linkDescription = "opens in a new tab"
	# link title should be read in focus
	linkTitle = "conduct a search"
	linkContents = "to google's"
	return f"""
			<div>
				<div
					contenteditable=""
					spellcheck="false"
					role="textbox"
					aria-multiline="true"
				><p>This is a line with no annotation</p>
				<p><span
						aria-description="{annotation}"
					>Here is a sentence that is being edited by someone else.</span>
					<b>Multiple can edit this.</b></p>
				<p>An element with a role, follow <a
					href="www.google.com"
					aria-description="{linkDescription}"
					>{linkContents}</a
				> website</p>
				<p>Testing the title attribute, <a
					href="www.google.com"
					title="{linkTitle}"
					>{linkContents}</a
				> website</p>
				</div>
			</div>
		"""


def test_ariaDescription_focusMode():
	""" Ensure aria description is read in focus mode.
	Settings which may affect this:
	- speech.reportObjectDescriptions default:True
	- annotations.reportAriaDescription default:True
	"""
	_chrome.prepareChrome(_getAriaDescriptionSample())
	# Focus the contenteditable and automatically switch to focus mode (due to contenteditable)
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		"edit  multi line  This is a line with no annotation\nFocus mode"
	)

	actualSpeech = _chrome.getSpeechAfterKey('downArrow')
	# description-from hasn't reached Chrome stable yet.
	# reporting aria-description only supported in Chrome canary 92.0.4479.0+
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"User nearby, Aaron",  # annotation
			"Here is a sentence that is being edited by someone else.",  # span text
			"Multiple can edit this.",  # bold paragraph text
		])
	)

	actualSpeech = _chrome.getSpeechAfterKey('downArrow')
	# description-from hasn't reached Chrome stable yet.
	# reporting aria-description only supported in Chrome canary 92.0.4479.0+
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([  # two space separator
			"An element with a role, follow",  # paragraph text
			"link",  # link role
			"opens in a new tab",  # link description
			"to google's",  # link contents (name)
			"website"  # paragraph text
		])
	)

	# 'title' attribute for link ("conduct a search") should not be announced.
	# too often title is used without screen reader users in mind, and is overly verbose.
	actualSpeech = _chrome.getSpeechAfterKey('downArrow')
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Testing the title attribute,",  # paragraph text
			"link",  # link role
			"to google's",  # link contents (name)
			"website"  # paragraph text
		])
	)


def test_ariaDescription_browseMode():
	""" Ensure aria description is read in browse mode.
	Settings which may affect this:
	- speech.reportObjectDescriptions default:True
	- annotations.reportAriaDescription default:True
	"""
	_chrome.prepareChrome(_getAriaDescriptionSample())
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(
		actualSpeech,
		"edit  multi line  This is a line with no annotation"
	)

	actualSpeech = _chrome.getSpeechAfterKey('downArrow')
	# description-from hasn't reached Chrome stable yet.
	# reporting aria-description only supported in Chrome canary 92.0.4479.0+
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"User nearby, Aaron",  # annotation
			"Here is a sentence that is being edited by someone else.",  # span text
			"Multiple can edit this.",  # bold paragraph text
		])
	)

	actualSpeech = _chrome.getSpeechAfterKey('downArrow')
	# description-from hasn't reached Chrome stable yet.
	# reporting aria-description only supported in Chrome canary 92.0.4479.0+
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([  # two space separator
			"An element with a role, follow",  # paragraph text
			"link",  # link role
			"opens in a new tab",  # link description
			"to google's",  # link contents (name)
			"website"  # paragraph text
		])
	)

	# 'title' attribute for link ("conduct a search") should not be announced.
	# too often title is used without screen reader users in mind, and is overly verbose.
	actualSpeech = _chrome.getSpeechAfterKey('downArrow')
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Testing the title attribute,",  # paragraph text
			"link",  # link role
			"to google's",  # link contents (name)
			"website"  # paragraph text
		])
	)


def test_ariaDescription_sayAll():
	""" Ensure aria description is read by say all.
	# Historically, description was not announced at all in browse mode with arrow navigation,
	# annotations are now a special case.

	Settings which may affect this:
	- speech.reportObjectDescriptions default:True
	- annotations.reportAriaDescription default:True
	"""
	_chrome.prepareChrome(_getAriaDescriptionSample())
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+downArrow")

	# Reporting aria-description only supported in:
	# - Chrome 92.0.4479.0+
	_asserts.strings_match(
		actualSpeech,
		SPEECH_CALL_SEP.join([
			"Test page load complete",
			"edit  multi line  This is a line with no annotation",
			SPEECH_SEP.join([
				"User nearby, Aaron",  # annotation
				"Here is a sentence that is being edited by someone else.",  # span text
				"Multiple can edit this.",  # bold paragraph text
			]),
			SPEECH_SEP.join([  # two space separator
				"An element with a role, follow",  # paragraph text
				"link",  # link role
				"opens in a new tab",  # link description
				"to google's",  # link contents (name)
				"website",  # paragraph text
			]),
			# 'title' attribute for link ("conduct a search") should not be announced.
			# too often title is used without screen reader users in mind, and is overly verbose.
			SPEECH_SEP.join([
				"Testing the title attribute,",  # paragraph text
				"link",  # link role
				# note description missing when sourced from title attribute
				"to google's",  # link contents (name)
				"website",  # paragraph text
				"out of edit"
			]),
			"After Test Case Marker"
		])
	)


def test_i10840():
	"""
	The name of table header cells should only be conveyed once when navigating directly to them in browse mode
	Chrome self-references a header cell as its own header, which used to cause the name to be announced twice
	"""
	_chrome.prepareChrome(
		"""
			<table>
				<thead>
					<tr>
						<th>Month</th>
						<th>items</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>January</td>
						<td>100</td>
					</tr>
					<tr>
						<td>February</td>
						<td>80</td>
					</tr>
				</tbody>
				<tfoot>
					<tr>
						<td>Sum</td>
						<td>180</td>
					</tr>
				</tfoot>
				</table>
		"""
	)
	# Jump to the table
	actualSpeech = _chrome.getSpeechAfterKey("t")
	_asserts.strings_match(
		actualSpeech,
		"table  with 4 rows and 2 columns  row 1  column 1  Month"
	)
	nextActualSpeech = _chrome.getSpeechAfterKey("control+alt+rightArrow")
	_asserts.strings_match(
		nextActualSpeech,
		"column 2  items"
	)


def test_mark_browse():
	_chrome.prepareChrome(
		"""
		<div>
			<p>The word <mark>Kangaroo</mark> is important.</p>
		</div>
		"""
	)
	actualSpeech = _chrome.getSpeechAfterKey('downArrow')
	_asserts.strings_match(
		actualSpeech,
		"The word  highlighted  Kangaroo  out of highlighted  is important."
	)
	# Test moving by word
	actualSpeech = _chrome.getSpeechAfterKey("numpad6")
	_asserts.strings_match(
		actualSpeech,
		"word"
	)
	actualSpeech = _chrome.getSpeechAfterKey("numpad6")
	_asserts.strings_match(
		actualSpeech,
		"highlighted  Kangaroo  out of highlighted"
	)


def test_mark_focus():
	_chrome.prepareChrome(
		"""
		<div>
			<p>The word <mark><a href="#">Kangaroo</a></mark> is important.</p>
		</div>
		"""
	)

	# Force focus mode
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+space")
	_asserts.strings_match(
		actualSpeech,
		"Focus mode"
	)

	actualSpeech = _chrome.getSpeechAfterKey('tab')
	_asserts.strings_match(
		actualSpeech,
		"highlighted\nKangaroo  link"
	)


def test_preventDuplicateSpeechFromDescription_browse_tab():
	"""
	When description matches name/content, it should not be spoken.
	This prevents duplicate speech.
	Settings which may affect this:
	- speech.reportObjectDescriptions default:True
	"""
	_chrome.prepareChrome(
		"""
		<a href="#" title="apple" style="display:block">apple</a>
		<a href="#" title="banana" aria-label="banana" style="display:block">contents</a>
		"""
	)

	spy = _NvdaLib.getSpyLib()
	REPORT_OBJ_DESC_KEY = ["presentation", "reportObjectDescriptions"]
	spy.set_configValue(REPORT_OBJ_DESC_KEY, True)

	# Read in browse
	actualSpeech = _chrome.getSpeechAfterKey('tab')
	_asserts.strings_match(
		actualSpeech,
		"apple  link"
	)
	actualSpeech = _chrome.getSpeechAfterKey('tab')
	_asserts.strings_match(
		actualSpeech,
		"banana  link"
	)


def preventDuplicateSpeechFromDescription_focus():
	"""
	When description matches name/content, it should not be spoken.
	This prevents duplicate speech.
	Settings which may affect this:
	- speech.reportObjectDescriptions default:True
	"""
	_chrome.prepareChrome(
		"""
		<a href="#" title="apple" style="display:block">apple</a>
		<a href="#" title="banana" aria-label="banana" style="display:block">contents</a>
		"""
	)
	spy = _NvdaLib.getSpyLib()
	REPORT_OBJ_DESC_KEY = ["presentation", "reportObjectDescriptions"]
	spy.set_configValue(REPORT_OBJ_DESC_KEY, True)

	# Force focus mode
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+space")
	_asserts.strings_match(
		actualSpeech,
		"Focus mode"
	)
	actualSpeech = _chrome.getSpeechAfterKey('tab')
	_asserts.strings_match(
		actualSpeech,
		"apple  link"
	)
	actualSpeech = _chrome.getSpeechAfterKey('tab')
	_asserts.strings_match(
		actualSpeech,
		"banana  link"
	)


def test_ensureNoBrowseModeDescription():
	"""
	Test that option (speech.reportObjectDescriptions default:True)
	does not result in description in browse mode.
	"""
	_chrome.prepareChrome(
		"\n".join([
			r'<button>something for focus</button>'
			r'<a href="#" style="display:block" title="Cat">Apple</a>',
			# second link to make testing second focus mode tab easier
			r'<a href="#" style="display:block" title="Fish">Banana</a>',
		])
	)

	REPORT_OBJ_DESC_KEY = ["presentation", "reportObjectDescriptions"]
	spy = _NvdaLib.getSpyLib()
	# prevent browse / focus mode messages from interfering, 0 means configFlags.ShowMessages.DISABLED,
	# i.e. don't show.
	spy.set_configValue(["braille", "showMessages"], 0)

	actualSpeech = _NvdaLib.getSpeechAfterKey('tab')
	_builtIn.should_contain(actualSpeech, "something for focus")

	# Test Browse mode
	spy.set_configValue(REPORT_OBJ_DESC_KEY, True)
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey('downArrow')
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"link",  # role description
			# No link description (from title)
			"Apple",  # link name / contents
		]),
		message="Test browse mode with reportObjectDescriptions=True"
	)
	_asserts.braille_matches(
		actualBraille,
		BRAILLE_SEP.join([
			"lnk",  # role description
			# No link description (from title)
			"Apple",  # link name / contents
		]),
		message="Test browse mode with reportObjectDescriptions=True"
	)

	# move virtual cursor back up to reset to start position
	actualSpeech = _NvdaLib.getSpeechAfterKey('upArrow')
	_builtIn.should_contain(actualSpeech, "something for focus")
	spy.set_configValue(REPORT_OBJ_DESC_KEY, False)

	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey('downArrow')
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"link",  # role description
			# No link description (from title)
			"Apple",  # link name / contents
		]),
		message="Test browse mode with reportObjectDescriptions=False"
	)
	_asserts.braille_matches(
		actualBraille,
		BRAILLE_SEP.join([
			"lnk",  # role description
			# No link description (from title)
			"Apple",  # link name / contents
		]),
		message="Test browse mode with reportObjectDescriptions=False"
	)

	# move virtual cursor back up to reset to start position
	actualSpeech = _NvdaLib.getSpeechAfterKey('upArrow')
	_builtIn.should_contain(actualSpeech, "something for focus")
	spy.set_configValue(REPORT_OBJ_DESC_KEY, True)

	# Test focus mode
	actualSpeech = _NvdaLib.getSpeechAfterKey("nvda+space")
	_asserts.speech_matches(actualSpeech, "Focus mode")

	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("tab")
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"Apple",  # link name / contents
			"link",  # role description
			"Cat",  # link description (from title)
		]),
		message="Test focus mode with reportObjectDescriptions=True"
	)
	_asserts.braille_matches(
		actualBraille,
		BRAILLE_SEP.join([
			"Apple",  # link name / contents
			"lnk",  # role description
			"Cat",  # link description (from title)
		]),
		message="Test focus mode with reportObjectDescriptions=True"
	)

	# Use second link to test focus mode when 'reportObjectDescriptions' is off.
	spy.set_configValue(REPORT_OBJ_DESC_KEY, False)
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("tab")
	_asserts.speech_matches(
		actualSpeech,
		SPEECH_SEP.join([
			"Banana",  # link name / contents
			"link",  # role description
			# No link description (from title)
		]),
		message="Test focus mode with reportObjectDescriptions=False"
	)
	_asserts.braille_matches(
		actualBraille,
		BRAILLE_SEP.join([
			"Banana",  # link name / contents
			"lnk",  # role description
			# No link description (from title)
		]),
		message="Test focus mode with reportObjectDescriptions=False"
	)


def test_quickNavTargetReporting():
	"""
	When using quickNav, the target object should be spoken first, inner context should be given before outer
	context.
	"""
	_chrome.prepareChrome(
		"""
		<div
			aria-describedby="descId"
			aria-labelledby="labelId"
			role="article"
		>
			<h1>Quick Nav Target</h1>
			<div id="labelId">
					<div>Some name.</div>
			</div>
			<div id="descId">
					<span>A bunch of text.</span>
			</div>
		</div>
		"""
	)
	spy = _NvdaLib.getSpyLib()
	REPORT_ARTICLES = ["documentFormatting", "reportArticles"]
	spy.set_configValue(REPORT_ARTICLES, False)

	# Quick nav to heading
	actualSpeech = _chrome.getSpeechAfterKey("h")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Quick Nav Target",  # Heading content (quick nav target), should read first
			"heading",  # Heading role
			"level 1",  # Heading level
		])
	)
	# Reset to allow trying again with report articles enabled
	actualSpeech = _chrome.getSpeechAfterKey("control+home")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Before Test Case Marker",
		])
	)

	# Quick nav to heading with report articles enabled
	spy.set_configValue(REPORT_ARTICLES, True)
	actualSpeech = _chrome.getSpeechAfterKey("h")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Quick Nav Target",  # Heading content (quick nav target), should read first
			"heading",  # Heading role
			"level 1",  # Heading level
			"article",  # article role, enabled via report article
			"A bunch of text.",  # article (ancestor) description
		])
	)


def test_focusTargetReporting():
	"""
	When moving focus the target object should be spoken first, inner context should be given before outer
	context.
	"""
	_chrome.prepareChrome(
		"""
		<a href="#">before Target</a>
		<div
			aria-describedby="descId"
			aria-labelledby="labelId"
			role="article"
		>
			<a href="#">Focus Target</a>
			<div id="labelId">
					<div>Some name.</div>
			</div>
			<div id="descId">
					<span>A bunch of text.</span>
			</div>
		</div>
		"""
	)

	spy = _NvdaLib.getSpyLib()
	REPORT_ARTICLES = ["documentFormatting", "reportArticles"]
	spy.set_configValue(REPORT_ARTICLES, False)

	# Set focus
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"before Target",
			"link",
		])
	)

	# Focus the link
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Focus Target",  # link content (focus target), should read first
			"link",  # link role
		]),
		message="browse mode - focus with Report Articles disabled"
	)
	# Reset to allow trying again with report articles enabled
	actualSpeech = _chrome.getSpeechAfterKey("shift+tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"before Target",
			"link",
		])
	)

	# Focus the link with report articles enabled
	spy.set_configValue(REPORT_ARTICLES, True)
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Focus Target",  # link content (focus target), should read first
			"link",  # link role
			"article",  # article role, enabled via report article
			"A bunch of text.",  # article (ancestor) description
		]),
		message="browse mode - focus with Report Articles enabled"
	)

	# Reset to allow trying again in focus mode
	actualSpeech = _chrome.getSpeechAfterKey("shift+tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"before Target",
			"link",
		])
	)

	# Force focus mode
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+space")
	_asserts.strings_match(
		actualSpeech,
		"Focus mode"
	)

	spy.set_configValue(REPORT_ARTICLES, False)
	# Focus the link
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_CALL_SEP.join([
			SPEECH_SEP.join([
				"Some name.",  # name for article
				"article",  # article role, enabled via report article
				"A bunch of text.",  # description for article
			]),
			SPEECH_SEP.join([
				"Focus Target",  # link content (focus target), should read first
				"link",  # link role
			]),
		]),
		message="focus mode - focus with Report Articles disabled"
	)
	# Reset to allow trying again with report articles enabled
	actualSpeech = _chrome.getSpeechAfterKey("shift+tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"before Target",
			"link",
		])
	)

	# Focus the link with report articles enabled
	spy.set_configValue(REPORT_ARTICLES, True)
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_CALL_SEP.join([
			SPEECH_SEP.join([
				"Some name.",  # name for article
				"article",  # article role, enabled via report article
				"A bunch of text.",  # description for article
			]),
			SPEECH_SEP.join([
				"Focus Target",  # link content (focus target), should read first
				"link",  # link role
			]),
		]),
		message="focus mode - focus with Report Articles enabled"
	)


def test_tableNavigationWithMergedColumns():
	"""When navigating through a merged cell,
	NVDA should preserve the column/row position from the previous cell.
	Refer to #7278, #11919.
	"""
	_chrome.prepareChrome("""
	<p>This is text</p>
	<table
	 border=0 cellpadding=0 cellspacing=0 width=192
	 style='border-collapse: collapse;table-layout:fixed;width:144pt'
	>
	<col width=64 span=3 style='width:48pt'>
	<tr height=20 style='height:15.0pt'>
		<td height=20 width=64 style='height:15.0pt;width:48pt'>a1</td>
		<td width=64 style='width:48pt'>b1</td>
		<td width=64 style='width:48pt'>c1</td>
	</tr>
	<tr height=20 style='height:15.0pt'>
		<td colspan=2 height=20 style='height:15.0pt'>a2 and b2</td>
		<td>c2</td>
	</tr>
	</table>
	""")
	# Navigate to end of text, this aligns the cursor with column 2
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(actualSpeech, "This is text")

	# Navigate to the table
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(actualSpeech, "table  with 2 rows and 3 columns  row 1  column 1  a 1")

	# Navigate to a cell in row 1, column 2
	actualSpeech = _chrome.getSpeechAfterKey("downArrow")
	_asserts.strings_match(actualSpeech, "column 2  b 1")

	# Navigate to a merged cell below
	actualSpeech = _chrome.getSpeechAfterKey("control+alt+downArrow")
	_asserts.strings_match(actualSpeech, "row 2  column 1  through 2  a 2 and b 2")

	# Return to row 1, column 2
	# In #7278, #11919, NVDA would return to row 1, column 1
	# This caused column position to be lost when navigating through merged cells
	actualSpeech = _chrome.getSpeechAfterKey("control+alt+upArrow")
	_asserts.strings_match(actualSpeech, "row 1  column 2  b 1")


def prepareChromeForTableSayAllTests():
	_chrome.prepareChrome("""
		<p>Hello, world!</p>
		<table border=3>
			<tr>
				<td>A1</td>
				<td>B1</td>
				<td rowspan=2>C1+C2</td>
				<td>D1</td>
				<td>E1</td>
			</tr>
			<tr>
				<td>A2</td>
				<td>B2</td>
				<td>D2</td>
				<td>E2</td>
			</tr>
			<tr>
				<td colspan=2>A3+B3</td>
				<td>C3</td>
				<td colspan=2>D3+E3</td>
			</tr>
			<tr>
				<td>A4</td>
				<td>B4</td>
				<td colspan=2 rowspan=2>C4+D4+<br>C5+D5</td>
				<td>E4</td>
			</tr>
			<tr>
				<td>A5</td>
				<td>B5</td>
				<td>E5</td>
			</tr>
		</table>
		<p>Bye-bye, world!</p>
	""")

	# Jump to table
	actualSpeech = _chrome.getSpeechAfterKey("t")
	_asserts.strings_match(actualSpeech, "table  with 5 rows and 5 columns  row 1  column 1  A 1")


def tableSayAllJumpToB2():
	_chrome.getSpeechAfterKey("control+alt+pageUp")
	_chrome.getSpeechAfterKey("control+alt+home")
	_chrome.getSpeechAfterKey("control+alt+rightArrow")
	actualSpeech = _chrome.getSpeechAfterKey("control+alt+downArrow")
	_asserts.strings_match(actualSpeech, "row 2  B 2")


def test_tableSayAllCommands():
	""" Tests that table sayAll commands work correctly.
	Key bindings: NVDA+control+alt+downArrow/rightArrow
	Refer to #13469.
	"""
	prepareChromeForTableSayAllTests()
	tableSayAllJumpToB2()
	# sayAll column
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+control+alt+downArrow")
	_asserts.strings_match(
		actualSpeech,
		"\n".join([
			"B 2",
			"row 3  column 1  through 2  A 3 plus B 3",
			"row 4  column 2  B 4",
			"row 5  B 5",
		]),
	)

	# Check that cursor has moved to B5
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+upArrow")
	_asserts.strings_match(actualSpeech, "B 5")

	tableSayAllJumpToB2()
	# sayAll row
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+control+alt+rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"\n".join([
			"B 2",
			"row 1  through 2  column 3  C 1 plus C 2",
			"row 2  D 2",
			"column 4  E 2",
		]),
	)

	# Check that cursor has moved to E2
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+upArrow")
	_asserts.strings_match(actualSpeech, "E 2")

	# Jump to A3
	_chrome.getSpeechAfterKey("control+alt+pageUp")
	_chrome.getSpeechAfterKey("control+alt+home")
	_chrome.getSpeechAfterKey("control+alt+downArrow")
	actualSpeech = _chrome.getSpeechAfterKey("control+alt+downArrow")
	_asserts.strings_match(actualSpeech, "row 3  column 1  through 2  A 3 plus B 3")

	# sayAll row with cells merged horizontally
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+control+alt+rightArrow")
	_asserts.strings_match(
		actualSpeech,
		"\n".join([
			"A 3 plus B 3",
			"column 3  C 3",
			"column 4  through 5  D 3 plus E 3",
		]),
	)

	# Check that cursor has moved to E3
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+upArrow")
	_asserts.strings_match(actualSpeech, "D 3 plus E 3")


def test_tableSpeakAllCommands():
	""" Tests that table speak entire row/column commands work correctly.
	Key bindings: NVDA+control+alt+upArrow/leftArrow
	Refer to #13469.
	"""
	prepareChromeForTableSayAllTests()
	tableSayAllJumpToB2()
	# Speak current column
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("NVDA+control+alt+upArrow")
	_asserts.strings_match(
		actualSpeech,
		"\n".join([
			"row 1  B 1",
			"row 2  B 2",
			"row 3  column 1  through 2  A 3 plus B 3",
			"row 4  column 2  B 4",
			"row 5  B 5",
		])
	)
	_asserts.braille_matches(
		actualBraille,
		"r2 c2 B2",
		message="Speak entire column",
	)

	# Check that cursor still stays at B2
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+upArrow")
	_asserts.strings_match(actualSpeech, "row 2  B 2")

	# Speak current row
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+control+alt+leftArrow")
	_asserts.strings_match(
		actualSpeech,
		"\n".join([
			"column 1  A 2",
			"column 2  B 2",
			"row 1  through 2  column 3  C 1 plus C 2",
			"row 2  D 2",
			"column 4  E 2",
		])
	)

	# Check that cursor stays at B2
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+upArrow")
	_asserts.strings_match(actualSpeech, "column 2  B 2")


def test_tableSayAllAxisCachingForMergedCells():
	""" Tests that axis caching for merged cells in table sayAll commands works.
	Refer to #13469.
	"""
	prepareChromeForTableSayAllTests()

	# Jump to D5
	_chrome.getSpeechAfterKey("control+alt+pageUp")
	_chrome.getSpeechAfterKey("control+alt+end")
	_chrome.getSpeechAfterKey("control+alt+leftArrow")
	_chrome.getSpeechAfterKey("control+alt+downArrow")
	_chrome.getSpeechAfterKey("control+alt+downArrow")
	actualSpeech = _chrome.getSpeechAfterKey("control+alt+downArrow")
	_asserts.strings_match(
		actualSpeech,
		"row 4  column 3  through row 5 column 4  C 4 plus D 4 plus  C 5 plus D 5"
	)

	# Speak current column - should reuse cached column
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+control+alt+upArrow")
	_asserts.strings_match(
		actualSpeech,
		"\n".join([
			"row 1  column 4  D 1",
			"row 2  column 3  D 2",
			"row 3  column 4  through 5  D 3 plus E 3",
			"row 4  column 3  through row 5 column 4  C 4 plus D 4 plus  C 5 plus D 5",
		]),
	)


def test_focus_mode_on_focusable_read_only_lists():
	"""
	If a list is read-only, but is focusable, and a list element receives focus, switch to focus mode.
	"""
	_chrome.prepareChrome(
		"""
		<a href="#">before Target</a>
		<div role="list" aria-label="Messages" tabindex="-1">
			<div role="listitem" tabindex="0" aria-label="Todd Kloots Hello all. At 1:30 PM">
				<div role="document" aria-roledescription="message">
					<a href="/kloots" class="sender">Todd Kloots</a> <a href="/time" class="time">1:30 PM</a>
					<p>Hello all.</p>
				</div>
			</div>
		</div>
		"""
	)
	# Set focus
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"before Target",
			"link",
		])
	)

	# focus the list item
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_CALL_SEP.join([
			SPEECH_SEP.join([
				"Messages",  # name for list container
				"list",  # role for list container
			]),
			SPEECH_SEP.join([
				"level 1",  # Inserted by Chromium even though not explicitly set
				"Todd Kloots Hello all. At 1:30 PM",  # list element name, should read first
				"1 of 1",  # item count, no role expected here
			]),
			"Focus mode",  # Focus mode should be enabled automatically and be indicated
		]),
		message="focus mode - focus list item and turn on focus mode"
	)


def test_i10890():
	"""
	Ensure that sort state is announced on a column header when changed with inner button
	"""
	spy = _NvdaLib.getSpyLib()
	# Chrome sometimes exposes tables as clickable, sometimes not.
	# This test does not need to know, so disable reporting of clickables.
	spy.set_configValue(["documentFormatting", "reportClickable"], False)
	testFile = os.path.join(ARIAPatternsDir, "grid", "examples", "data-grids.html")
	_chrome.prepareChrome(
		f"""
			<iframe src="{testFile}"></iframe>
		"""
	)
	# Jump to the Example 2 heading
	_chrome.getSpeechAfterKey("3")
	actualSpeech = _chrome.getSpeechAfterKey("3")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Example 2: Sortable Data Grid With Editable Cells",
			"heading",
			"level 3",
		])
	)
	# Jump to the table
	actualSpeech = _chrome.getSpeechAfterKey("t")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Transactions January 1 through January 7",
			"table",
			"with 8 rows and 6 columns",
			"row 1",
			"column 1",
			"sorted ascending",
			"Date",
			"button",
		])
	)
	# Press the button
	actualSpeech = _chrome.getSpeechAfterKey("space")
	# and ensure that the new sort state is spoken.
	_asserts.strings_match(
		actualSpeech,
		"sorted descending",
	)


def test_ARIASwitchRole():
	"""
	Ensure that ARIA switch controls have an appropriate role and states in browse mode.
	"""
	testFile = os.path.join(ARIAPatternsDir, "switch", "examples", "switch.html")
	_chrome.prepareChrome(
		f"""
			<iframe src="{testFile}"></iframe>
		"""
	)
	# Jump to the second heading 2 in the iframe.
	_chrome.getSpeechAfterKey("2")
	actualSpeech = _chrome.getSpeechAfterKey("2")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Example",
			"heading  level 2"
		]),
		message="Move to first heading 2 in frame",
	)
	# Tab to the switch control
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Notifications",
			"switch",
			"off",
		]),
		message="tab to switch control",
	)
	# Read the current line
	actualSpeech = _chrome.getSpeechAfterKey("numpad8")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"switch",
			"off",
			"Notifications",
		]),
		message="Read current line",
	)
	# Report the current focus
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Notifications",
			"switch",
			"focused",
			"off",
		]),
		message="Report focus",
	)
	# Toggle the switch on
	actualSpeech = _chrome.getSpeechAfterKey("space")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"on",
		]),
		message="Toggle switch control on",
	)
	# Read the current line
	actualSpeech = _chrome.getSpeechAfterKey("numpad8")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"switch",
			"on",
			"Notifications",
		]),
		message="Read current line",
	)
	# Report the current focus
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Notifications",
			"switch",
			"focused",
			"on",
		]),
		message="Report focus",
	)
	# Toggle the switch off
	actualSpeech = _chrome.getSpeechAfterKey("space")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"off",
		]),
		message="Toggle switch control off",
	)
	# Read the current line
	actualSpeech = _chrome.getSpeechAfterKey("numpad8")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"switch",
			"off",
			"Notifications",
		]),
		message="Read current line",
	)
	# Report the current focus
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"Notifications",
			"switch",
			"focused",
			"off",
		]),
		message="Report focus",
	)


def test_i13307():
	"""
	Even if (to avoid duplication) NVDA may choose to not speak a landmark or region's label
	when arrowing into a landmark or region with an aria-labelledby,
	it should still speak the label when junping inside the landmark or region
	from outside using quicknav or focus.
	"""
	_chrome.prepareChrome(
		"""
		<p>navigation landmark with aria-label</p>
		<nav aria-label="label">
			<button>inner element</button>
		</nav>
		<p>Navigation landmark with aria-labelledby</p>
		<nav aria-labelledby="innerHeading1">
			<h1 id="innerHeading1">labelled by</h1>
			<button>inner element</button>
		</nav>
		<p>Region with aria-label</p>
		<section aria-label="label">
			<button>inner element</button>
		</section>
		<p>Region with aria-labelledby</p>
		<section aria-labelledby="innerHeading2">
			<h1 id="innerHeading2">labelled by</h1>
			<button>inner element</button>
		</section>
		"""
	)
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"label",
			"navigation landmark",
			"inner element",
			"button",
		]),
		message="jumping into landmark with aria-label should speak label",
	)
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"labelled by",
			"navigation landmark",
			"inner element",
			"button",
		]),
		message="jumping into landmark with aria-labelledby should speak label",
	)
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"label",
			"region",
			"inner element",
			"button",
		]),
		message="jumping into region with aria-label should speak label",
	)
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join([
			"labelled by",
			"region",
			"inner element",
			"button",
		]),
		message="jumping into region with aria-labelledby should speak label",
	)


def test_textParagraphNavigation():
	_chrome.prepareChrome("""
		<!-- First a bunch of paragraphs that don't match text regex -->
		<p>Header</p>
		<p>Liberal MP: 1904–1908</p>
		<p>.</p>
		<p>…</p>
		<p>5.</p>
		<p>test....</p>
		<p>a.b</p>
		<p></p>
		<!-- Now a bunch of matching paragraphs -->
		<p>Hello, world!</p>
		<p>He replied, "That's wonderful."</p>
		<p>He replied, "That's wonderful".</p>
		<p>He replied, "That's wonderful."[4]</p>
		<p>Предложение по-русски.</p>
		<p>我不会说中文！</p>
		<p>Bye-bye, world!</p>
	""")

	expectedParagraphs = [
		# Tests exclamation sign
		"Hello, world!",
		# Tests Period with preceding quote
		"He replied,  That's wonderful.",
		# Tests period with trailing quote
		"He replied,  That's wonderful .",
		# Tests wikipedia-style reference
		"He replied,  That's wonderful.  4",
		# Tests compatibility with Russian Cyrillic script
		"Предложение по-русски.",
		# Tests regex condition for CJK full width character terminators
		"我不会说中文",
		"Bye-bye, world!",
	]
	for p in expectedParagraphs:
		actualSpeech = _chrome.getSpeechAfterKey("p")
		_asserts.strings_match(actualSpeech, p)
	actualSpeech = _chrome.getSpeechAfterKey("p")
	_asserts.strings_match(actualSpeech, "no next text paragraph")

	for p in expectedParagraphs[-2::-1]:
		actualSpeech = _chrome.getSpeechAfterKey("shift+p")
		_asserts.strings_match(actualSpeech, p)
	actualSpeech = _chrome.getSpeechAfterKey("shift+p")
	_asserts.strings_match(actualSpeech, "no previous text paragraph")


def test_styleNav():
	""" Tests that same style and different style navigation work correctly in browse mode.
	By default these commands don't have assigned gestures,
	so we will assign temporary gestures just for testing.
	"""
	spy: "NVDASpyLib" = _NvdaLib.getSpyLib()
	spy.assignGesture(
		"kb:s",
		"browseMode",
		"BrowseModeTreeInterceptor",
		"nextSameStyle",
	)

	spy.assignGesture(
		"kb:shift+s",
		"browseMode",
		"BrowseModeTreeInterceptor",
		"previousSameStyle",
	)
	spy.assignGesture(
		"kb:d",
		"browseMode",
		"BrowseModeTreeInterceptor",
		"nextDifferentStyle",
	)

	spy.assignGesture(
		"kb:shift+d",
		"browseMode",
		"BrowseModeTreeInterceptor",
		"previousDifferentStyle",
	)

	_chrome.prepareChrome("""
		<p>Hello world!</p>
		<p>This text is <b>bold</b></p>
		<p>Second line is <font size="15pt">large</font></p>
		<p>Third line is <mark>highlighted</mark></p>
		<p>Fourth line is <b>bold again</b></p>
		<p>End of document.</p>
	""")
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("shift+d")
	_asserts.strings_match(actualSpeech, "No previous different style text")
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("s")
	_asserts.strings_match(actualSpeech, "Second line is")
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("shift+d")
	_asserts.strings_match(actualSpeech, "bold")
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("s")
	_asserts.strings_match(actualSpeech, "bold again")
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("s")
	_asserts.strings_match(actualSpeech, "No next same style text")
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("d")
	_asserts.strings_match(actualSpeech, "End of document.  After Test Case Marker")
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("d")
	_asserts.strings_match(actualSpeech, "No next different style text")
	for s in [
		"Second line is",
		"Third line is",
		"Fourth line is",
	][::-1]:
		actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("shift+s")
		_asserts.strings_match(actualSpeech, s)
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("d")
	_asserts.strings_match(actualSpeech, "large")
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("shift+s")
	_asserts.strings_match(actualSpeech, "No previous same style text")
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("s")
	_asserts.strings_match(actualSpeech, "No next same style text")
	
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("d")
	_asserts.strings_match(actualSpeech, "Third line is")
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("d")
	_asserts.strings_match(actualSpeech, "highlighted  highlighted")
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("shift+s")
	_asserts.strings_match(actualSpeech, "No previous same style text")
	actualSpeech, actualBraille = _NvdaLib.getSpeechAndBrailleAfterKey("s")
	_asserts.strings_match(actualSpeech, "No next same style text")


def test_ariaErrorMessage():
	_chrome.prepareChrome("""
		<h2>Native valid</h2>
		<label for="i1">Input 1</label>
		<input type="text" autocomplete="off" id="i1" aria-errormessage="e1" />
		<p id="e1">Error 1</p>

		<h2>Native invalid</h2>
		<label for="i2">Input 2</label>
		<input type="text" autocomplete="off"  id="i2" pattern="a" value="b" aria-errormessage="e2" />
		<p id="e2">Error 2</p>

		<h2>ARIA valid</h2>
		<label id="l3">Input 3</label>
		<div contenteditable role="textbox" aria-multiline="false" aria-labelledby="l3" aria-errormessage="e3"
		     aria-invalid="false"></div>
		<p id="e3">Error 3</p>

		<h2>ARIA valid</h2>
		<label id="l4">Input 4</label>
		<div contenteditable role="textbox" aria-multiline="false" aria-labelledby="l4" aria-errormessage="e4"
		     aria-invalid="true"></div>
		<p id="e4">Error 4</p>
	""")
	# Force focus mode
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+space")
	_asserts.strings_match(
		actualSpeech,
		"Focus mode"
	)
	# Tab to the native valid field
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join(("Input 1", "edit", "blank"))
	)

	# Tab to the native invalid field
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join(("Input 2", "edit", "invalid entry", "Error 2", "selected b"))
	)

	# Tab to the ARIA valid field
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join(("Input 3", "edit", "blank"))
	)

	# Tab to the native invalid field
	actualSpeech = _chrome.getSpeechAfterKey("tab")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join(("Input 4", "edit", "invalid entry", "Error 4", "blank"))
	)

	# Force browse mode
	actualSpeech = _chrome.getSpeechAfterKey("NVDA+space")
	_asserts.strings_match(
		actualSpeech,
		"Browse mode"
	)
	# Jump to the top of the document
	_chrome.getSpeechAfterKey("control+home")
	# Quick nav to the native valid field
	actualSpeech = _chrome.getSpeechAfterKey("e")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join(("Input 1", "edit"))
	)

	# Quick nav to the native invalid field
	actualSpeech = _chrome.getSpeechAfterKey("e")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join(("Input 2", "edit", "invalid entry", "Error 2", "b"))
	)

	# Quick nav to the ARIA valid field
	actualSpeech = _chrome.getSpeechAfterKey("e")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join(("Input 3", "edit"))
	)

	# Quick nav to the native invalid field
	actualSpeech = _chrome.getSpeechAfterKey("e")
	_asserts.strings_match(
		actualSpeech,
		SPEECH_SEP.join(("Input 4", "edit", "invalid entry", "Error 4"))
	)
