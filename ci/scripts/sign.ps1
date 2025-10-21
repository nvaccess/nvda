# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2010-2024 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

param(
	[string]$ApiToken,
	[string]$FileToSign
)

Write-Host "Signing $FileToSign ... " -NoNewline

Submit-SigningRequest -ApiToken $ApiToken -InputArtifactPath $FileToSign -OutputArtifactPath $FileToSign -OrganizationId "12147e94-bba9-4fef-b29b-300398e90c5a" -ProjectSlug "NVDA" -SigningPolicySlug "release_signing_policy" -WaitForCompletion -Force

$authenticodeSignature = Get-AuthenticodeSignature -FilePath $FileToSign
if (($authenticodeSignature).Status -ne 'Valid') {
	Write-Host "Failure"
	Write-Output @"
FAIL: Signature is not valid.

<details>
<summary>Signature details</summary>

$($authenticodeSignature | ConvertTo-Html -fragment -Property Path, SignatureType, Status, StatusMessage)

Signer certificate:
$(
	if ($null -eq $authenticodeSignature.SignerCertificate) {
		"None"
	} else {
		$authenticodeSignature.SignerCertificate | ConvertTo-Html -fragment -Property Subject, Issuer,  SerialNumber,  Thumbprint, `
		@{Name='NotBefore'; Expr={$_.NotBefore.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")}},`
		@{Name='NotAfter'; Expr={$_.NotAfter.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")}}
	}
)

Timestamper certificate:
$(
	if ($null -eq $authenticodeSignature.TimestamperCertificate) {
		"None"
	} else {
		$authenticodeSignature.TimestamperCertificate | ConvertTo-Html -fragment -Property Subject, Issuer,  SerialNumber,  Thumbprint,`
		@{Name='NotBefore'; Expr={$_.NotBefore.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")}},`
		@{Name='NotAfter'; Expr={$_.NotAfter.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")}}
	}
)

</details>
"@ >> $env:GITHUB_STEP_SUMMARY
	exit 1
} else {
	Write-Host "Success"
}
