$testOutput = (Resolve-Path .\testOutput\)
$systemTestOutput = (Resolve-Path "$testOutput\system")

if ($env:VERBOSE_SYSTEM_TEST_LOGGING) {
	$verboseDebugLogging="True"
} else {
	$verboseDebugLogging=""
}

# This tag is used to exclude system tests.
# If provided to runsystemtests, RF would give an error.
$SKIP_SYS_TESTS = "excluded_from_build"
$tagsForTest = "installer NVDA"  # include the tests tagged with installer, or NVDA
if ($env:INCLUDE_SYSTEM_TEST_TAGS) {
	if ($env:INCLUDE_SYSTEM_TEST_TAGS -eq $SKIP_SYS_TESTS) {
		# Indicate the tests were skipped, and exit early.
		Add-AppveyorMessage "Skipped: System tests."
		return
	}
	$tagsForTest = $env:INCLUDE_SYSTEM_TEST_TAGS

}
$tagsForTestArray = -split $tagsForTest # turn this string into an array
$includeTags = $tagsForTestArray | ForEach-Object {
	# Before every item output '--include'
	# No spaces required.
	# Including spaces will result in automatic quote characters around the string. I.E. "--include "
	"--include", $_
}

.\runsystemtests.bat `
--variable whichNVDA:installed `
--variable installDir:"${env:nvdaLauncherFile}" `
--variable verboseDebugLogging:"${verboseDebugLogging}" `
@includeTags `
# last line inentionally blank, allowing all lines to have line continuations.

if($LastExitCode -ne 0) {
	Set-AppveyorBuildVariable "testFailExitCode" $LastExitCode
	Add-AppveyorMessage "FAIL: System tests (tags: ${tagsForTest}). See test results for more information."
} else {
	Add-AppveyorMessage "PASS: System tests (tags: ${tagsForTest})."
}
Compress-Archive -Path "$systemTestOutput\*" -DestinationPath "$testOutput\systemTestResult.zip"
Push-AppveyorArtifact "$testOutput\systemTestResult.zip"
$wc = New-Object 'System.Net.WebClient'
$wc.UploadFile("https://ci.appveyor.com/api/testresults/junit/$($env:APPVEYOR_JOB_ID)", (Resolve-Path "$systemTestOutput\systemTests.xml"))
