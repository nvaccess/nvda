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
	# Excluded due to regular failures.
	test_ariaTreeGrid_browseMode
ARIA invalid spelling and grammar
	[Documentation]	Tests ARIA invalid values of "spelling", "grammar" and "spelling, grammar".
	ARIAInvalid_spellingAndGrammar
ARIA checkbox
	[Documentation]	Navigate to an unchecked checkbox in reading mode.
	[Tags]	aria-at
	test_ariaCheckbox_browseMode
ARIA details
	[Documentation]	Ensure a summary of aria-details is read on command.
	[Tags]	annotations
	test aria details
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
	[Documentation]	Navigate to a span with aria-description in browse mode
	test_ariaDescription_browseMode
ARIA description Say All
	[Documentation]	Say all, contents includes aria-description
	test_ariaDescription_sayAll
i10840
	[Documentation]	The name of table header cells should only be conveyed once when navigating directly to them in browse mode (chrome self-references a header cell as its own header, which used to cause the name to be announced twice)
	test_i10840
