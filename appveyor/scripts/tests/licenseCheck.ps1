$licenseOutput = (Resolve-Path .\testOutput\license\)
$licenseOutput = "$licenseOutput\licenseCheckResults.md"
.\runlicensecheck.bat "$licenseOutput" 
if ($LastExitCode -ne 0) {
	Set-AppveyorBuildVariable "testFailExitCode" $LastExitCode
	Add-AppveyorMessage "FAIL: License check. See $licenseOutput for more information."
} else {
	Add-AppveyorMessage "PASS: License check."
}
Push-AppveyorArtifact $licenseOutput
