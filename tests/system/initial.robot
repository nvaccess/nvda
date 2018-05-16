*** Settings ***
Documentation    An example test suite documentation with *some* _formatting_.
...              See test documentation for more documentation examples.
Library       OperatingSystem
Library       Process
Library       sendKey.py

*** Test Cases ***

Can Start NVDA
    ${nvdaHandle} =  Start Process  python nvda.pyw --debug-logging  cwd=source  shell=true
    Process Should Be Running  ${nvdaHandle}
    sleep  5
    send quit NVDA keys
    ${nvdaResult} =  Wait For Process  ${nvdaHandle}
    Should Be Equal  ${nvdaResult.stdout}  Hello, world!

