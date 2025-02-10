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

$cppcheckOutput = "$lintOutput\cppcheck.xml"
choco install cppcheck
cppcheck --xml --enable=portability --check-level=exhaustive nvdaHelper 2> "$cppcheckOutput"
if ($LastExitCode -ne 0) {
	Set-AppveyorBuildVariable "testFailExitCode" $LastExitCode
	Add-AppveyorMessage "FAIL: C++ check. See $cppcheckOutput for more information."
} else {
	Add-AppveyorMessage "PASS: C++ check."
}
Push-AppveyorArtifact $cppcheckOutput
