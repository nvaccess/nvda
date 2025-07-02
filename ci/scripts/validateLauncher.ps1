$launcherName="output\nvda*.exe"
if (-not (Test-Path -Path $launcherName -PathType Leaf)) {
	Write-Output "FAIL: Launcher verification. The launcher does not exist." >> $env:GITHUB_STEP_SUMMARY
	exit 1
}
if ($env:apiSigningToken) {
	$authenticodeSignature = Get-AuthenticodeSignature -FilePath $launcherName
	if (($authenticodeSignature).Status -ne 'Valid') {
		Set-PSRepository PSGallery -InstallationPolicy Trusted
		Install-Module -Name FormatMarkdownTable -Force
		Write-Output @"
FAIL: Launcher validation. Expected the launcher to be signed.
<details>
	<summary>Signature details</summary>

	$($authenticodeSignature | Format-MarkdownTableTableStyle -HideStandardOutput -ShowMarkdown -DoNotCopyToClipboard)

</details>
"@ >> $env:GITHUB_STEP_SUMMARY
		exit 1
	}
}
