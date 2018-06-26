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
	[Setup]	start NVDA	standard-doShowWelcomeDialog.ini
	wait for foreground	Welcome to NVDA
	send key	enter
	send key	insert	q
	wait for foreground	Exit NVDA
	send key	enter
	wait for process	nvdaAlias	timeout=10 sec
	process should be stopped	nvdaAlias

Can read the welcome dialog
	[Setup]	start NVDA	standard-doShowWelcomeDialog.ini
	assert all speech	${WELCOME_DIALOG_TEXT}
	send key	enter
