$licenseOutput = (Resolve-Path .\testOutput\license\)
$licenseOutput = "$licenseOutput\licenseCheckResults.md"
cmd.exe /c "runlicensecheck.bat $licenseOutput"
if ($LastExitCode -ne 0) {
	$message = "FAIL: License check. See $licenseOutput for more information."
} else {
	$message = "PASS: License check."
}
$message >> $env:GITHUB_STEP_SUMMARY
