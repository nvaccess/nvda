# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
*** Settings ***
Documentation	Basic start and exit tests
Default Tags	NVDA	smoke test

Library	OperatingSystem
Library	Process
Library	sendKey.py
Library	nvdaRobotLib.py
Library	helperLib.py

Test Setup	start NVDA	standard-dontShowWelcomeDialog.ini
Test Teardown	quit NVDA

Variables	variables.py

*** Test Cases ***
Starts
	[Documentation]	Ensure that NVDA can start
	process should be running	nvdaAlias

Quits from keyboard
	[Documentation]	Starts NVDA and ensures that it can be quit using the keyboard
	[Setup]	start NVDA	standard-doShowWelcomeDialog.ini

	${Welcome dialog title} =	catenate double space	Welcome to NVDA
	wait for specific speech	${Welcome dialog title}
	wait for speech to finish
	sleep	1	# the dialog is not always receiving the enter keypress, wait a little longer for it
	send key	enter

	${Exit NVDA dialog} =	catenate double space	Exit NVDA
	send key	insert	q
	${INDEX} =	wait for specific speech	${Exit NVDA dialog}

	wait for speech to finish
	${actual speech} =	get speech from index until now	${INDEX}
	assert strings are equal	${actual speech}	${QUIT_DIALOG_TEXT}
	sleep	1	# the dialog is not always receiving the enter keypress, wait a little longer for it
	send key	enter
	wait for process	nvdaAlias	timeout=10 sec
	process should be stopped	nvdaAlias

Read welcome dialog
	[Documentation]	Ensure that the welcome dialog can be read in full
	[Setup]	start NVDA	standard-doShowWelcomeDialog.ini

	${Welcome dialog title} =	catenate double space	Welcome to NVDA
	${INDEX} =	wait for specific speech	${Welcome dialog title}
	wait for speech to finish
	${actual speech} =	get speech from index until now	${INDEX}
	assert strings are equal	${actual speech}	${WELCOME_DIALOG_TEXT}
	sleep	1	# the dialog is not always receiving the enter keypress, wait a little longer for it
	send key	enter
