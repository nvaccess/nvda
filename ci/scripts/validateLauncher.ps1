$launcherName="output\nvda*.exe"
if (-not (Test-Path -Path $launcherName -PathType Leaf)) {
	Write-Output "The launcher does not exist." >> $env:GITHUB_STEP_SUMMARY
	exit 1
}
if ($env:apiSigningToken -and (Get-AuthenticodeSignature -FilePath $launcherName).Status -ne 'Valid') {
	Write-Output "The launcher was not signed, or the signature was invalid.`n">> $env:GITHUB_STEP_SUMMARY
	exit 1
}
