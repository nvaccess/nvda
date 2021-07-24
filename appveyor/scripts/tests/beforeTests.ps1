New-Item -ItemType directory -Path testOutput
New-Item -ItemType directory -Path testOutput\unit
New-Item -ItemType directory -Path testOutput\system
New-Item -ItemType directory -Path testOutput\lint
Set-AppveyorBuildVariable "testFailExitCode" 0
