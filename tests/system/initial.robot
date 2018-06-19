*** Settings ***
Documentation	Basic *NVDA* and _RobotFramework_ tests
...	Starts NVDA and exits.
...	Run with python -m robot tests/system/initial.robot in CMD.
Library	OperatingSystem
Library	Process
Library	sendKey.py
Library	nvdaRobotLib.py

*** Settings ***
Test Setup	start NVDA
Test Teardown	quit NVDA

*** Test Cases ***
Ensure NVDA runs at all
	process should be running	nvdaAlias

Ensure NVDA quits from keyboard
	send key	insert	q
	wait for foreground	Exit NVDA
	send key	enter
	wait for process	nvdaAlias	timeout=5 sec

Can Start and exit NVDA
	assert last speech	"Welcome to NVDA"