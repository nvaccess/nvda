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
	# TODO: can we make a better syntax for this? Maybe: 'join two spaces	sample text'
	${Exit NVDA dialog} =	catenate	SEPARATOR=${SPACE * 2}	Exit NVDA	dialog
	send key	insert	q
	${INDEX} =	wait for specific speech	${Exit NVDA dialog}

	wait for speech to finish
	${actual speech} =	get speech from index until now	${INDEX}
	assert strings are equal	${actual speech}	${QUIT_DIALOG_TEXT}

	send key	enter
	wait for process	nvdaAlias	timeout=5 sec

Can read the welcome dialog
	[Setup]	start NVDA	standard-doShowWelcomeDialog.ini
	${Welcome dialog title} =	catenate	SEPARATOR=${SPACE * 2}	Welcome to NVDA	dialog
	${INDEX} =	wait for specific speech	${Welcome dialog title}
	wait for speech to finish
	${actual speech} =	get speech from index until now	${INDEX}
	assert strings are equal	${actual speech}	${WELCOME_DIALOG_TEXT}