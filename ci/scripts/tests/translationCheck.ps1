cmd.exe /c "scons checkPot $sconsArgs --all-cores"
if($LastExitCode -ne 0) {
	$message = "FAIL: Translation comments check. Translation comments missing or unexpectedly included. See build log for more information."
	echo "testFailExitCode=$LastExitCode" | Out-File -FilePath $Env:GITHUB_ENV -Encoding utf8 -Append
} else {
	$message = "PASS: Translation comments check."
}
$message >> $env:GITHUB_STEP_SUMMARY
