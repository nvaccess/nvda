$lintOutput = (Resolve-Path .\testOutput\lint\)
.\runlint.bat "$lintOutput"
if ($LastExitCode -ne 0) {
	Set-AppveyorBuildVariable "testFailExitCode" $LastExitCode
	Add-AppveyorMessage "FAIL: Lint check. See test results and lint artifacts for more information."
} else {
	Add-AppveyorMessage "PASS: Lint check."
}
Push-AppveyorArtifact "$lintOutput/PR-lint.xml"
Push-AppveyorArtifact "$lintOutput/lint-diff.diff"
$wc = New-Object 'System.Net.WebClient'
$wc.UploadFile("https://ci.appveyor.com/api/testresults/junit/$($env:APPVEYOR_JOB_ID)", "$lintOutput/PR-lint.xml")
