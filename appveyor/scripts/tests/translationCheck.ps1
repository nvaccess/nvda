cmd.exe /c "scons checkPot $sconsArgs"
if($LastExitCode -ne 0) {
	Set-AppveyorBuildVariable "testFailExitCode" $LastExitCode
	Add-AppveyorMessage "FAIL: Translation comments check. Translation comments missing or unexpectedly included. See build log for more information."
} else {
	Add-AppveyorMessage "PASS: Translation comments check."
}
