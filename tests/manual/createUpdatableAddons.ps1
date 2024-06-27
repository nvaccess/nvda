# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

param(
	[string]$addonName = "clock",
	[string]$configFolder = "$env:APPDATA\nvda\userConfig",
	[string]$newVersionMajor = "0",
	[string]$newVersionMinor = "0"
)

# Define paths to the JSON metadata and manifest file
$jsonPath = Join-Path -Path $configFolder -ChildPath "\addons\$addonName.json"
$manifestPath = Join-Path -Path $configFolder -ChildPath "\addons\$addonName\manifest.ini"

# Function to update JSON metadata
function Update-JsonMetadata {
	if (Test-Path $jsonPath) {
		(Get-Content $jsonPath) -replace '"addonVersionName": "[\d+\.]+"', "`"addonVersionName`": `"$newVersionMajor.$newVersionMinor`"" | Set-Content $jsonPath
		(Get-Content $jsonPath) -replace '"addonVersionNumber": {[^}]+}', "`"addonVersionNumber`": {`"major`": $newVersionMajor, `"minor`": $newVersionMinor, `"patch`": 0}" | Set-Content $jsonPath
		Write-Host "Updated JSON metadata at $jsonPath"
	} else {
		Write-Host "JSON metadata file not found at $jsonPath"
	}
}

# Function to update manifest file
function Update-Manifest {
	if (Test-Path $manifestPath) {
		(Get-Content $manifestPath) -replace '^version = [\d+\.]+', "version = $newVersionMajor.$newVersionMinor" | Set-Content $manifestPath
		Write-Host "Updated manifest file at $manifestPath"
	} else {
		Write-Host "Manifest file not found at $manifestPath"
	}
}

# Execute updates
Update-JsonMetadata
Update-Manifest
