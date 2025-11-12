# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019-2025 NV Access Limited, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

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
	logForegroundWindowTitle
	${screenshotName}=	create_preserved_test_output_filename	failedTest.png
	Run Keyword If Test Failed	Take Screenshot	${screenShotName}
	dump_speech_to_log
	dump_braille_to_log
	# leaving the chrome tabs open may slow down / cause chrome to crash
	close_chrome_tab
	quit NVDA

default setup
	logForegroundWindowTitle
	start NVDA	standard-dontShowWelcomeDialog.ini
	logForegroundWindowTitle
	enable_verbose_debug_logging_if_requested

*** Test Cases ***
# Ensure every test case is sub-grouped by a tag and added to CI/CD

## chrome_list tests

Announce list item when moving by word or character
	[Documentation]	Entering a list item when moving by word or character should be announced, but not by line.
	[Tags]	chrome_list
	announce_list_item_when_moving_by_word_or_character
i7562
	[Documentation]	List should not be announced on every line of a ul in a contenteditable
	[Tags]	chrome_list
	test_i7562
pr11606
	[Documentation]	Announce the correct line when placed at the end of a link at the end of a list item in a contenteditable
	[Tags]	chrome_list
	test_pr11606
focus mode is turned on on focused read-only list item
	[Documentation]	Focused list items with a focusable list container should cause focus mode to be turned on automatically.
	[Tags]	chrome_list
	test_focus_mode_on_focusable_read_only_lists

## chrome_annotations tests
### ARIA annotations: details, descriptions, etc

ARIA details
	[Documentation]	Ensure a summary of aria-details is read on command from a mark element
	[Tags]	chrome_annotations
	test_mark_aria_details
ARIA details with free review and nav
	[Documentation]	Variation on the ARIA details test with the config changed so the review cursor does not follow the caret and the nav object doesn't follow focus.
	[Tags]	chrome_annotations
	test_mark_aria_details_FreeReviewCursor
ARIA details noVbuf
	[Documentation]	Test for retrieving ARIA details from a button inside a role=application
	[Tags]	chrome_annotations
	test_aria_details_noVBufNoTextInterface
ARIA details noVbuf with free review and nav
	[Documentation]	Test for retrieving ARIA details from a button inside a role=application with the config changed so the review cursor does not follow the caret and the nav object doesn't follow focus.
	[Tags]	chrome_annotations
	test_aria_details_noVBufNoTextInterface
ARIA description Focus Mode
	[Documentation]	Navigate to a span with aria-description in focus mode
	[Tags]	chrome_annotations
	test_ariaDescription_focusMode
ARIA description Browse Mode
	[Documentation]	Navigate (down arrow, in browse mode) aria-description is read, other sources of description are not.
	[Tags]	chrome_annotations
	test_ariaDescription_browseMode
ARIA description Say All
	[Documentation]	Say all, contents includes aria-description
	[Tags]	chrome_annotations
	test_ariaDescription_sayAll
ARIA details role
	[Documentation]	Test aria details roles being announced on discovery
	[Tags]	chrome_annotations
	test_mark_aria_details_role
multiple ARIA details targets
	[Documentation]	Test multiple aria details targets being announced
	[Tags]	chrome_annotations
	test_annotations_multi_target
i13307
	[Documentation]	ensure aria-labelledby on a landmark or region is automatically spoken when jumping inside from outside using focus in browse mode
	[Tags]	chrome_annotations
	test_i13307

## chrome_table tests

Table navigation with merged columns
	[Documentation]	When navigating through a merged cell, preserve the column/row position from the previous cell.
	[Tags]	chrome_table
	test_tableNavigationWithMergedColumns
Table sayAll commands
	[Documentation]	Table sayAll commands
	[Tags]	chrome_table
	test_tableSayAllCommands
Table Speak All commands
	[Documentation]	Table speak entire row/column commands
	[Tags]	chrome_table
	test_tableSpeakAllCommands
Table sayAll axis caching for merged cells
	[Documentation]	Tests that axis caching for merged cells in table sayAll commands works.
	[Tags]	chrome_table
	test_tableSayAllAxisCachingForMergedCells
Table in style display: table
	[Documentation]	Properly announce table row/column count and working table navigation for a HTML table in a div with style display: table
	[Tags]	chrome_table
	test_tableInStyleDisplayTable
i10840
	[Documentation]	The name of table header cells should only be conveyed once when navigating directly to them in browse mode (chrome self-references a header cell as its own header, which used to cause the name to be announced twice)
	[Tags]	chrome_table
	test_i10840

## chrome_language tests
### Language changing related tests

Report language disabled
	[Documentation]	Read a sentence with different languages without reporting none of them.
	[Tags]	chrome_language
	test_reportLanguageDisabled
Report language enabled
	[Documentation]	Read a sentence with different languages reporting them.
	[Tags]	chrome_language
	test_reportLanguageEnabled
Report language without dialects
	[Documentation]	Read a sentence with different languages without reporting dialects.
	[Tags]	chrome_language
	test_reportLanguageWithoutDialects
Report not supported language without other languages
	[Documentation]	Read a sentence with different languages without reporting supported ones.
	[Tags]	chrome_language
	test_reportNotSupportedLanguageWithoutOtherLanguages
Report not supported language and other languages
	[Documentation]	Read a sentence with different languages reporting them, included the not supported language.
	[Tags]	chrome_language
	test_reportNotSupportedLanguageAndOtherLanguages

## chrome_roleDescription tests

ARIA roleDescription focus
	[Documentation]	report focusing an element with a custom role
	[Tags]	chrome_roleDescription
	test_ariaRoleDescription_focus
ARIA roleDescription inline browse mode
	[Documentation]	Read an inline element with a custom role in browse mode
	[Tags]	chrome_roleDescription
	test_ariaRoleDescription_inline_browseMode
ARIA roleDescription block browse mode
	[Documentation]	Read a block element with a custom role in browse mode
	[Tags]	chrome_roleDescription
	test_ariaRoleDescription_block_browseMode
ARIA roleDescription inline content editable
	[Documentation]	Read an inline element with a custom role in content editables 
	[Tags]	chrome_roleDescription
	test_ariaRoleDescription_inline_contentEditable
ARIA roleDescription block content editable
	[Documentation]	Read an block element with a custom role in content editables 
	[Tags]	chrome_roleDescription
	test_ariaRoleDescription_block_contentEditable

## chrome_misc_aria tests
## No current useful grouping beyond ARIA. Keep to minimum in length.

ARIA treegrid
	[Documentation]	Ensure that ARIA treegrids are accessible as a standard table in browse mode.
	[Tags]	chrome_misc_aria
	test_ariaTreeGrid_browseMode
ARIA invalid spelling and grammar
	[Documentation]	Tests ARIA invalid values of "spelling" and "grammar".
	[Tags]	chrome_misc_aria
	ARIAInvalid_spellingAndGrammar
aria-errormessage
	[Documentation]	Test that aria-errormessage is reported correctly in focus and browse mode
	[Tags]	chrome_misc_aria
	test_ariaErrorMessage
ARIA checkbox
	[Documentation]	Navigate to an unchecked checkbox in reading mode.
	[Tags]	chrome_misc_aria
	test_ariaCheckbox_browseMode
ARIA switch role
	[Documentation]	Test aria switch control has appropriate role and states in browse mode and when focused
	[Tags]	chrome_misc_aria
	test_ARIASwitchRole

# chrome_misc tests
## No current useful grouping. Keep to minimum in length.

Marked Browse mode
	[Documentation]	Ensure that Marked content is read in browse mode
	[Tags]	chrome_misc
	test_mark_browse
Marked Focus mode
	[Documentation]	Ensure that Marked content is read in Focus mode
	[Tags]	chrome_misc
	test_mark_focus
checkbox labelled by inner element
	[Documentation]	A checkbox labelled by an inner element should not read the label element twice.
	[Tags]	chrome_misc
	checkbox_labelled_by_inner_element
i12147
	[Documentation]	New focus target should be announced if the triggering element is removed when activated
	[Tags]	chrome_misc
	test_i12147
Prevent Duplicate Speech From Description while in Focus mode
	[Tags]	chrome_misc
	preventDuplicateSpeechFromDescription_focus
Prevent Duplicate Speech From Description while in Browse mode with tab nav
	[Tags]	chrome_misc
	test_preventDuplicateSpeechFromDescription_browse_tab
Only report description in focus mode due to reportObjectDescriptions
	[Documentation]	The term object in reportObjectDescriptions (essentially) means focus mode.
	[Tags]	chrome_misc
	test_ensureNoBrowseModeDescription
Quick Nav reports target first
	[Documentation]	Quick Nav target should always be reported before ancestors. Ancestors should be reported from inner to outer.
	[Tags]	chrome_misc
	test_quickNavTargetReporting
Focus reports target first
	[Documentation]	Focus target should always be reported before ancestors. Ancestors should be reported from inner to outer.
	[Tags]	chrome_misc
	test_focusTargetReporting
i10890
	[Documentation]	Test sort state is announced on column header when changed with inner button
	[Tags]	chrome_misc
	test_i10890
textParagraphNavigation
	[Documentation]	Text paragraph navigation
	[Tags]	chrome_misc
	test_textParagraphNavigation
styleNav
	[Documentation]	Same style navigation
	[Tags]	chrome_misc
	test_styleNav
