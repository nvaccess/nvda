# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
*** Settings ***
Documentation	Basic start and exit tests
Force Tags	NVDA	smoke test

# for start & quit in Test Setup and Test Test Teardown
Library	NvdaLib.py
Library	startupShutdownNVDA.py
Library	ScreenCapLibrary

Test Setup	start NVDA	standard-dontShowWelcomeDialog.ini
Test Teardown	default teardown

*** Keywords ***
default teardown
	${screenshotName}=	create_preserved_test_output_filename	failedTest.png
	Run Keyword If Test Failed	Take Screenshot	${screenShotName}
	quit NVDA

*** Test Cases ***
Starts
	[Documentation]	Ensure that NVDA can start
	NVDA_Starts	# run test

Quits from keyboard
	[Documentation]	Starts NVDA and ensures that it can be quit using the keyboard
	[Setup]	start NVDA	standard-doShowWelcomeDialog.ini
	quits_from_keyboard	# run test

Read welcome dialog
	[Documentation]	Ensure that the welcome dialog can be read in full
	[Setup]	start NVDA	standard-doShowWelcomeDialog.ini
	read_welcome_dialog	# run test
