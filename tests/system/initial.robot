*** Settings ***
Documentation		Basic *NVDA* and _RobotFramework_ tests
...							Starts NVDA and exits.
...							Run with python -m robot tests/system/initial.robot in CMD.
Library			 OperatingSystem
Library			 Process
Library			 sendKey.py
Library			 nvdaRobotLib.py

*** Test Cases ***

Can Start and exit NVDA
	log to console	start nvda
	start process	py nvda.pyw --debug-logging -r	 cwd=source	shell=true	alias=nvdaAlias
	sleep	4
	log to console	connect to remote server
	Import Library	Remote				 WITH NAME		nvdaSpy
	log to console	process should be running
	process should be running
	log to console	get process object
	log to console	send quit NVDA keys 
	send quit NVDA keys
	log to console	sleep 1
	sleep	1
	log to console	send enter key
	send enter key
	log to console	stop remote server
	nvdaSpy.Stop Remote Server
	log to console	process.wait
	wait for process
	log to console	done


