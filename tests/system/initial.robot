*** Settings ***
Documentation    Basic *NVDA* and _RobotFramework_ tests
...              Starts NVDA and exits.
...              Run with python -m robot tests/system/initial.robot in CMD.
Library       OperatingSystem
Library       Process
Library       sendKey.py
Library       nvdaRobotLib.py

*** Test Cases ***

Can Start and exit NVDA
    start nvda
    log to console  About to run quit NVDA
    quit NVDA


