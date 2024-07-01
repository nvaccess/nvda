$lintOutput = (Resolve-Path .\testOutput\lint\)
$lintOutput = "$lintOutput\PR-lint.xml"
.\runlint.bat "$lintOutput"
if ($LastExitCode -ne 0) {
	Set-AppveyorBuildVariable "testFailExitCode" $LastExitCode
	Add-AppveyorMessage "FAIL: Lint check. See test results for more information."
} else {
	Add-AppveyorMessage "PASS: Lint check."
}
Push-AppveyorArtifact $lintOutput
$wc = New-Object 'System.Net.WebClient'
$wc.UploadFile("https://ci.appveyor.com/api/testresults/junit/$($env:APPVEYOR_JOB_ID)", $lintOutput)
