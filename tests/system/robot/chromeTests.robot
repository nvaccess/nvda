# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
*** Settings ***
Documentation	HTML test cases in Chrome
Force Tags	NVDA	smoke test	browser	chrome

# for start & quit in Test Setup and Test Test Teardown
Library	NvdaLib.py
# for test cases
Library	chromeTests.py
Library	ScreenCapLibrary

Test Setup	default setup
Test Teardown	default teardown

*** Keywords ***
default teardown
	${screenshotName}=	create_preserved_test_output_filename	failedTest.png
	Run Keyword If Test Failed	Take Screenshot	${screenShotName}
	dump_speech_to_log
	dump_braille_to_log
	exit chrome
	quit NVDA

default setup
	start NVDA	standard-dontShowWelcomeDialog.ini	chrome-gestures.ini

*** Test Cases ***

checkbox labelled by inner element
	[Documentation]	A checkbox labelled by an inner element should not read the label element twice.
	checkbox_labelled_by_inner_element
Announce list item when moving by word or character
	[Documentation]	Entering a list item when moving by word or character should be announced, but not by line.
	announce_list_item_when_moving_by_word_or_character
i7562
	[Documentation]	List should not be announced on every line of a ul in a contenteditable
	test_i7562
pr11606
	[Documentation]	Announce the correct line when placed at the end of a link at the end of a list item in a contenteditable
	test_pr11606
ARIA treegrid
	[Documentation]	Ensure that ARIA treegrids are accessible as a standard table in browse mode.
	test_ariaTreeGrid_browseMode
ARIA invalid spelling and grammar
	[Documentation]	Tests ARIA invalid values of "spelling", "grammar" and "spelling, grammar".
	[Tags]	excluded_from_build
	ARIAInvalid_spellingAndGrammar
ARIA checkbox
	[Documentation]	Navigate to an unchecked checkbox in reading mode.
	[Tags]	aria-at
	test_ariaCheckbox_browseMode
Marked Browse mode
	[Documentation]	Ensure that Marked content is read in browse mode
	test_mark_browse
Marked Focus mode
	[Documentation]	Ensure that Marked content is read in Focus mode
	test_mark_focus
ARIA details
	[Documentation]	Ensure a summary of aria-details is read on command from a mark element
	[Tags]	annotations
	test_mark_aria_details
ARIA details with free review and nav
	[Documentation]	Variation on the ARIA details test with the config changed so the review cursor does not follow the caret and the nav object doesn't follow focus.
	[Tags]	annotations
	test_mark_aria_details_FreeReviewCursor
ARIA details noVbuf
	[Documentation]	Test for retrieving ARIA details from a button inside a role=application
	[Tags]	annotations
	test_aria_details_noVBufNoTextInterface
ARIA details noVbuf with free review and nav
	[Documentation]	Test for retrieving ARIA details from a button inside a role=application with the config changed so the review cursor does not follow the caret and the nav object doesn't follow focus.
	[Tags]	annotations
	test_aria_details_noVBufNoTextInterface
i12147
	[Documentation]	New focus target should be announced if the triggering element is removed when activated
	test_i12147
Table in style display: table
	[Documentation]	Properly announce table row/column count and working table navigation for a HTML table in a div with style display: table
	test_tableInStyleDisplayTable
ARIA roleDescription focus
	[Documentation]	report focusing an element with a custom role	
	test_ariaRoleDescription_focus
ARIA roleDescription inline browse mode
	[Documentation]	Read an inline element with a custom role in browse mode
	test_ariaRoleDescription_inline_browseMode
ARIA roleDescription block browse mode
	[Documentation]	Read a block element with a custom role in browse mode
	test_ariaRoleDescription_block_browseMode
ARIA roleDescription inline content editable
	[Documentation]	Read an inline element with a custom role in content editables 
	test_ariaRoleDescription_inline_contentEditable
ARIA roleDescription block content editable
	[Documentation]	Read an block element with a custom role in content editables 
	test_ariaRoleDescription_block_contentEditable
ARIA description Focus Mode
	[Documentation]	Navigate to a span with aria-description in focus mode
	test_ariaDescription_focusMode
ARIA description Browse Mode
	[Documentation]	Navigate (down arrow, in browse mode) aria-description is read, other sources of description are not.
	test_ariaDescription_browseMode
ARIA description Say All
	[Documentation]	Say all, contents includes aria-description
	test_ariaDescription_sayAll
i10840
	[Documentation]	The name of table header cells should only be conveyed once when navigating directly to them in browse mode (chrome self-references a header cell as its own header, which used to cause the name to be announced twice)
	test_i10840
Prevent Duplicate Speech From Description while in Focus mode
	preventDuplicateSpeechFromDescription_focus
Prevent Duplicate Speech From Description while in Browse mode with tab nav
	test_preventDuplicateSpeechFromDescription_browse_tab
Only report description in focus mode due to reportObjectDescriptions
	[Documentation]	The term object in reportObjectDescriptions (essentially) means focus mode.
	test_ensureNoBrowseModeDescription
Quick Nav reports target first
	[Documentation]	Quick Nav target should always be reported before ancestors. Ancestors should be reported from inner to outer.
	test_quickNavTargetReporting
Focus reports target first
	[Documentation]	Focus target should always be reported before ancestors. Ancestors should be reported from inner to outer.
	test_focusTargetReporting
Table navigation with merged columns
	[Documentation]	When navigating through a merged cell, preserve the column/row position from the previous cell.
	test_tableNavigationWithMergedColumns
focus mode is turned on on focused read-only list item
	[Documentation]	Focused list items with a focusable list container should cause focus mode to be turned on automatically.
	test_focus_mode_on_focusable_read_only_lists
