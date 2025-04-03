if ($env:RUNNER_DEBUG) {
	cmd.exe /c "scons checkPot -j1 2> testOutput\translationCheckResults.log"
} else {
	cmd.exe /c "scons checkPot --all-cores 2> testOutput\translationCheckResults.log"
}
Write-Output "Translation check output:"
Get-Content testOutput\translationCheckResults.log

if ($LastExitCode -ne 0) {
	Write-Output "FAIL: Translation comments check." >> $env:GITHUB_STEP_SUMMARY
	Write-Output "<details><summary>Error log</summary>" >> $env:GITHUB_STEP_SUMMARY
	Get-Content testOutput\translationCheckResults.log >> $env:GITHUB_STEP_SUMMARY
	Write-Output "</details>" >> $env:GITHUB_STEP_SUMMARY
	Write-Output "testFailExitCode=$LastExitCode" | Out-File -FilePath $Env:GITHUB_ENV -Encoding utf8 -Append
} else {
	Write-Output "PASS: Translation comments check." >> $env:GITHUB_STEP_SUMMARY
}
exit $LastExitCode
