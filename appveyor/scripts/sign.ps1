# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2010-2024 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

param(
    [string]$ApiToken,
    [string]$FileToSign
)

Import-Module -Name SignPath
Submit-SigningRequest -ApiToken $ApiToken -InputArtifactPath $FileToSign -OutputArtifactPath $FileToSign -OrganizationId "12147e94-bba9-4fef-b29b-300398e90c5a" -ProjectSlug "NVDA" -SigningPolicySlug "release_signing_policy" -WaitForCompletion -Force
