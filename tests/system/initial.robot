*** Settings ***
Documentation	Basic start and exit tests

Library	OperatingSystem
Library	Process
Library	libraries/sendKey.py
Library	libraries/nvdaRobotLib.py

Test Setup	start NVDA	standard-dontShowWelcomeDialog.ini
Test Teardown	quit NVDA

Variables	variables.py

*** Test Cases ***
Ensure NVDA runs at all
	process should be running	nvdaAlias

Ensure NVDA quits from keyboard
	send key	insert	n
	send key	x
	sleep	1
	send key	alt	shift	tab
	send key	enter
	wait for process	nvdaAlias	timeout=5 sec
	process should be stopped	nvdaAlias

Can read the welcome dialog
	[Setup]	start NVDA	standard-doShowWelcomeDialog.ini
	assert all speech	${WELCOME_DIALOG_TEXT}
	send key	enter
