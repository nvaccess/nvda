# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
*** Settings ***
Documentation	Plaintext test cases in notepad
Force Tags	NVDA	smoke test	notepad

# for start & quit in Test Setup and Test Test Teardown
Library	NvdaLib.py
# for test cases
Library	notepadTests.py
Library	ScreenCapLibrary

Test Setup	default setup
Test Teardown	default teardown

*** Keywords ***
default teardown
	${screenshotName}=	create_preserved_test_output_filename	failedTest.png
	Run Keyword If Test Failed	Take Screenshot	${screenShotName}
	exit notepad
	quit NVDA

default setup
	start NVDA	standard-dontShowWelcomeDialog.ini

*** Test Cases ***
symbolLevelWord
	[Documentation]	Ensure all symbols are read when navigating by word. 
	test symbolLevelWord all
symbolLevelWord off
	[Documentation]	Use default behaviour of reading symbols when navigating by word.
	test symbolLevelWord default
