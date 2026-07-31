# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
*** Settings ***
Documentation	Browseable message tests
Force Tags	NVDA	smoke test	browseableMessage

# for start & quit in Test Setup and Test Teardown
Library	NvdaLib.py
# for test cases
Library	browseableMessageTests.py
Library	ScreenCapLibrary

Test Setup	default setup
Test Teardown	default teardown

*** Keywords ***
default teardown
	logForegroundWindowTitle
	${screenshotName}=	create_preserved_test_output_filename	failedTest.png
	Run Keyword If Test Failed	Take Screenshot	${screenshotName}
	dump_speech_to_log
	exit notepad
	quit NVDA

default setup
	logForegroundWindowTitle
	start NVDA	standard-dontShowWelcomeDialog.ini	browseableMessage-gestures.ini
	logForegroundWindowTitle
	enable_verbose_debug_logging_if_requested

*** Test Cases ***

browseableMessageOpens
	[Documentation]	Ensure the browseable message dialog opens and NVDA reads the title and content.
	test_browseableMessage_opens

browseableMessageNavigation
	[Documentation]	Ensure browse mode navigation (arrow keys) works within the browseable message.
	test_browseableMessage_navigation

browseableMessageClose
	[Documentation]	Ensure the browseable message dialog can be closed with Escape.
	test_browseableMessage_close
