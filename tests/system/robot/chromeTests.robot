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

Test Setup	start NVDA	standard-dontShowWelcomeDialog.ini
Test Teardown	default teardown

*** Keywords ***
default teardown
	${screenshotName}=	create_preserved_test_output_filename	failedTest.png
	Run Keyword If Test Failed	Take Screenshot	${screenShotName}
	quit NVDA

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