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

Test Setup	start NVDA	standard-doShowWelcomeDialog.ini
Test Teardown	default teardown

*** Keywords ***
default teardown
	${screenshotName}=	create_preserved_test_output_filename	failedTest.png
	Run Keyword If Test Failed	Take Screenshot	${screenShotName}
	quit NVDA

*** Test Cases ***
Starts
	[Documentation]	Ensure that NVDA can start
	[Setup]	start NVDA	standard-dontShowWelcomeDialog.ini
	NVDA_Starts	# run test

Starts from desktop shortcut
	[Documentation]	Ensure that NVDA can start from desktop shortcut
	[Setup]	start NVDA	standard-dontShowWelcomeDialog.ini
	Pass Execution If	"${whichNVDA}"!="installed"	Desktop shortcut only exists on installed copies
	test desktop shortcut

Quits from keyboard
	[Documentation]	Starts NVDA and ensures that it can be quit using the keyboard
	quits_from_keyboard	# run test

Quits from keyboard with welcome dialog open
	[Documentation]	Starts NVDA and ensures that it can be quit with the welcome dialog open
	[Setup]	start NVDA	standard-dontShowWelcomeDialog.ini
	open welcome dialog from menu
	quits from keyboard	# run test

Quits from keyboard with about dialog open
	[Documentation]	Starts NVDA and ensures that it can be quit with the about dialog open
	[Setup]	start NVDA	standard-dontShowWelcomeDialog.ini
	# Excluded to be fixed still (#12976)
	[Tags]	excluded_from_build
	open about dialog from menu
	quits from keyboard	# run test

Quits from menu
	[Documentation]	Starts NVDA and ensures that it can be quit using the keyboard
	[Setup]	start NVDA	standard-dontShowExitDialog.ini
	quits from menu	False	# run test

Read welcome dialog
	[Documentation]	Ensure that the welcome dialog can be read in full
	read_welcome_dialog	# run test

Restarts
	[Documentation]	Ensure that NVDA can restart from keyboard
	NVDA restarts

Restarts on crash
	[Documentation]	Ensure NVDA restarts on crash.
	NVDA restarts on crash

Restarts on braille crash
	[Documentation]	Ensure NVDA restarts on a crash on the braille thread.
	NVDA restarts on braille crash

Restarts on UIAHandler crash
	[Documentation]	Ensure NVDA restarts on crash on the UIAHandler thread.
	NVDA restarts on UIAHandler crash
