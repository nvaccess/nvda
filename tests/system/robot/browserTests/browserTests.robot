# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

*** Settings ***
Documentation	Test behaviour in web browsers
Force Tags	NVDA	browser	browser_generic

# for start & quit in Test Setup and Test Test Teardown
Library	NvdaLib.py
# for test cases (generic runner across browsers)
Library	webBrowsers/WebBrowserGenericLib.py
Library	browserTests/browerTests.py
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
	close_browser_windows
	quit NVDA

default setup
	logForegroundWindowTitle
	start NVDA	standard-dontShowWelcomeDialog.ini
	logForegroundWindowTitle
	enable_verbose_debug_logging_if_requested

*** Test Cases ***
Read window title
	read window title

Browse mode: Landmarks general principles
	Start all browsers
	Open W3C example	patterns/landmarks/examples/general-principles.html
	browse mode landmarks general principles

Focus mode: Simple form interaction
	Start all browsers
	Open W3C example	patterns/landmarks/examples/form.html
	focus mode form fields

Interactive elements: Buttons
	Start all browsers
	Open W3C example	patterns/button/examples/index.html
	interactive elements buttons

Dynamic content: Live regions
	Start all browsers
	# Uses hosted W3C examples for live regions
	dynamic content live regions

Browser UI: Menus, bookmarks, settings
	Start all browsers
	browser ui menu bookmarks settings
