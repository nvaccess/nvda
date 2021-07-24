$outDir = (Resolve-Path .\testOutput\unit\)
$unitTestsXml = "$outDir\unitTests.xml"
.\rununittests.bat --with-xunit --xunit-file="$unitTestsXml"
if($LastExitCode -ne 0) {
	Set-AppveyorBuildVariable "testFailExitCode" $LastExitCode
	Add-AppveyorMessage "FAIL: Unit tests. See test results for more information."
} else {
	Add-AppveyorMessage "PASS: Unit tests."
}
Push-AppveyorArtifact $unitTestsXml
$wc = New-Object 'System.Net.WebClient'
$wc.UploadFile("https://ci.appveyor.com/api/testresults/junit/$($env:APPVEYOR_JOB_ID)", $unitTestsXml)
