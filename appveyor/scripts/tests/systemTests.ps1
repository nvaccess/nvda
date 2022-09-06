$testOutput = (Resolve-Path .\testOutput\)
$systemTestOutput = (Resolve-Path "$testOutput\system")

if ($env:VERBOSE_SYSTEM_TEST_LOGGING) {
	$verboseDebugLogging="True"
} else {
	$verboseDebugLogging=""
}

.\runsystemtests.bat `
--variable whichNVDA:installed `
--variable installDir:"${env:nvdaLauncherFile}" `
--variable verboseDebugLogging:"${verboseDebugLogging}" `
--include installer `
--include NVDA `
# last line inentionally blank, allowing all lines to have line continuations.

if($LastExitCode -ne 0) {
	Set-AppveyorBuildVariable "testFailExitCode" $LastExitCode
	Add-AppveyorMessage "FAIL: System tests. See test results for more information."
} else {
	Add-AppveyorMessage "PASS: System tests."
}
Compress-Archive -Path "$systemTestOutput\*" -DestinationPath "$testOutput\systemTestResult.zip"
Push-AppveyorArtifact "$testOutput\systemTestResult.zip"
$wc = New-Object 'System.Net.WebClient'
$wc.UploadFile("https://ci.appveyor.com/api/testresults/junit/$($env:APPVEYOR_JOB_ID)", (Resolve-Path "$systemTestOutput\systemTests.xml"))
