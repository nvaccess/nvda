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
	${Exit NVDA dialog} =	catenate	SEPARATOR=${SPACE * 2}	Exit NVDA	dialog
	${INDEX} =	wait_for_specific_speech_after_action	${Exit NVDA dialog}	send key	insert	q
	wait for speech to finish
	assert speech since index	${INDEX}	${QUIT_DIALOG_TEXT}
	send key	enter
	wait for process	nvdaAlias	timeout=5 sec

Can read the welcome dialog
	[Setup]	start NVDA	standard-doShowWelcomeDialog.ini
	wait for speech to finish
	assert all speech	${WELCOME_DIALOG_TEXT}