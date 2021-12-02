# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
*** Settings ***
Documentation	Smoke test the settings panel
Force Tags	NVDA	smoke test

# for start & quit in Test Setup and Test Test Teardown
Library	NvdaLib.py
Library	NVDASettings.py
Library	ScreenCapLibrary

Test Setup	start NVDA	standard-dontShowWelcomeDialog.ini
Test Teardown	default teardown

*** Keywords ***
default run read test
	[Arguments]	${settingsName}
	navigate to settings	${settingsName}
	Create Directory	${cacheFolder}/${currentVersion}
	Set Screenshot Directory	${cacheFolder}/${currentVersion}
	Take Screenshot	${settingsName}.png
	read settings	${settingsName}	${cacheFolder}	${currentVersion}	${compareVersion}
	Take Screenshot	${settingsName}-end.png

default teardown
	quit NVDA

default screenShot teardown
	${screenshotName}=	create_preserved_test_output_filename	failedTest.png
	Run Keyword If Test Failed	Take Screenshot	${screenShotName}
	Run Keyword If Test Failed	dump_speech_to_log
	quit NVDA

*** Test Cases ***
Read General
	[Tags]	excluded_from_build	readGui
	default run read test	General

Read Speech
	[Tags]	excluded_from_build	readGui
	default run read test	Speech

Read Braille
	[Tags]	excluded_from_build	readGui
	default run read test	Braille

Read Vision
	[Tags]	excluded_from_build	readGui
	default run read test	Vision

Read Keyboard
	[Tags]	excluded_from_build	readGui
	default run read test	Keyboard

Read Mouse
	[Tags]	excluded_from_build	readGui
	default run read test	Mouse

Read Review Cursor
	[Tags]	excluded_from_build	readGui
	default run read test	Review Cursor

Read Input Composition
	[Tags]	excluded_from_build	readGui
	default run read test	Input Composition

Read Object Presentation
	[Tags]	excluded_from_build	readGui
	default run read test	Object Presentation

Read Browse Mode
	[Tags]	excluded_from_build	readGui
	default run read test	Browse Mode

Read Document Formatting
	[Tags]	excluded_from_build	readGui
	default run read test	Document Formatting

Read Advanced
	[Tags]	excluded_from_build	readGui
	default run read test	Advanced

Test 12818 Double Settings Dialog opens
	[Setup]	start NVDA	standard-dontShowWelcomeDialog.ini
	open_general_to_braille_then_speech
	[Teardown]	default screenShot teardown

Test 12818 Single Settings Dialog opens
	[Setup]	start NVDA	standard-dontShowWelcomeDialog.ini	settings-gestures.ini
	open_braille_then_speech
	[Teardown]	default screenShot teardown
