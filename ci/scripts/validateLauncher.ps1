echo "Validating launcher."
$launcherName="output\nvda*.exe"
echo "launcherName=$launcherName"
echo "Checking existance"
if (-not (Test-Path -Path $launcherName -PathType Leaf)) {
	echo "File doesn't exist."
	Write-Output "FAIL: Launcher verification. The launcher does not exist." >> $env:GITHUB_STEP_SUMMARY
	exit 1
}
echo "File exists."
if ($env:apiSigningToken) {
	echo "Checking signature"
	$authenticodeSignature = Get-AuthenticodeSignature -FilePath $launcherName
	if (($authenticodeSignature).Status -ne 'Valid') {
		echo "Signature not valid."
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
	} else {
		echo "Signature valid."
	}
	echo $authenticodeSignature
} else {
	echo "Not checking signature."
}
echo "Launcher verification passed."
