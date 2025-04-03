$licenseOutput = (Resolve-Path .\testOutput\license\)
$licenseOutput = "$licenseOutput\licenseCheckResults.md"
cmd.exe /c "runlicensecheck.bat $licenseOutput"
if ($LastExitCode -ne 0) {
	Write-Output "FAIL: License check.`n" >> $env:GITHUB_STEP_SUMMARY
	Write-Output "testFailExitCode=$LastExitCode" | Out-File -FilePath $Env:GITHUB_ENV -Encoding utf8 -Append
} else {
	Write-Output "PASS: License check.`n" >> $env:GITHUB_STEP_SUMMARY
}
Write-Output "<details>`n<summary>License check summary</summary>`n" >> $env:GITHUB_STEP_SUMMARY
Get-Content $licenseOutput >> $env:GITHUB_STEP_SUMMARY
Write-Output "`n</details>`n" >> $env:GITHUB_STEP_SUMMARY
exit $LastExitCode
