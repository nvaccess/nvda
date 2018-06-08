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
    log to console  send quit NVDA keys 
    send quit NVDA keys
    log to console  sleep 1
    sleep  1
    log to console  send enter key
    send enter key
    log to console  stop remote server
    nvdaSpy.Stop Remote Server
    log to console  wait for process NVDA alias
    Wait For Process  nvdaAlias
    log to console  done


