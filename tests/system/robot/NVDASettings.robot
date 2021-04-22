# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
*** Settings ***
Documentation	Smoke test the settings panel, use for checking diffs
Force Tags	NVDA	smoke test	excluded_from_build

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

*** Test Cases ***
Read General
	default run read test	General

Read Speech
	default run read test	Speech

Read Braille
	default run read test	Braille

Read Vision
	default run read test	Vision

Read Keyboard
	default run read test	Keyboard

Read Mouse
	default run read test	Mouse

Read Review Cursor
	default run read test	Review Cursor

Read Input Composition
	default run read test	Input Composition

Read Object Presentation
	default run read test	Object Presentation

Read Browse Mode
	default run read test	Browse Mode

Read Document Formatting
	default run read test	Document Formatting

Read Advanced
	default run read test	Advanced
