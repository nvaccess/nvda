$ErrorActionPreference = "Stop";
Write-Host "Starting deployment script..."

# Debug: Print initial environment variables
Write-Host "Environment variables:"
Write-Host "APPVEYOR_PULL_REQUEST_NUMBER: $env:APPVEYOR_PULL_REQUEST_NUMBER"
Write-Host "versionType: $env:versionType"
Write-Host "APPVEYOR_REPO_BRANCH: $env:APPVEYOR_REPO_BRANCH"

if ($env:APPVEYOR_REPO_BRANCH -eq "beta" -and $env:feature_crowdinSync) {
	# Upload files to Crowdin for translation
	py -m pip install --no-warn-script-location requests
	py appveyor\crowdinSync.py uploadSourceFile 2 output\nvda.pot 2>&1
}
# Notify the NV Access server for all builds
$exe = Get-ChildItem -Name output\nvda_*.exe
Write-Host "Found executable: $exe"

$hash = (Get-FileHash "output\$exe" -Algorithm SHA1).Hash.ToLower()
Write-Host "File hash: $hash"

$apiVersion = (py -c "import sys; sys.path.append('source'); from addonAPIVersion import CURRENT; print('{}.{}.{}'.format(*CURRENT))")
Write-Host "API Version: $apiVersion"

$apiCompatTo = (py -c "import sys; sys.path.append('source'); from addonAPIVersion import BACK_COMPAT_TO; print('{}.{}.{}'.format(*BACK_COMPAT_TO))")
Write-Host "API Compatibility Version: $apiCompatTo"

$data = @{
	jobId=$env:APPVEYOR_JOB_ID;
	commit=$env:APPVEYOR_REPO_COMMIT;
	version=$env:version; versionType=$env:versionType;
	apiVersion=$apiVersion; apiCompatTo=$apiCompatTo;
	avVersion=$env:APPVEYOR_BUILD_VERSION;
	branch=$env:APPVEYOR_REPO_BRANCH;
	exe=$exe; hash=$hash;
	feature_buildSymbols=$env:feature_buildSymbols
}

Write-Host "Generated deployment data:"
$data | Format-Table | Out-String | Write-Host

ConvertTo-Json -InputObject $data -Compress | Out-File -FilePath deploy.json
Push-AppveyorArtifact deploy.json

# Send to the new API endpoint
try {
	Write-Host "Attempting to send data to NV Access server..."
	$jsonContent = Get-Content deploy.json -Raw
	Write-Host "JSON payload:"
	Write-Host $jsonContent

	$response = Invoke-RestMethod -Uri "https://api.nvaccess.org/appveyor-hook" `
		-Method Post `
		-Headers @{
			"Authorization" = "Bearer $env:APPVEYOR_WEBHOOK_TOKEN"
			"Content-Type" = "application/json"
		} `
		-Body $jsonContent
	Write-Host "Server response:"
	Write-Host ($response | ConvertTo-Json)
	Write-Host "Successfully notified NV Access server"
}
catch {
	Write-Host "Failed to notify NV Access server"
	Write-Host "Error details:"
	Write-Host $_.Exception.Message
	Write-Host $_.Exception.Response.StatusCode.value__
	Write-Host $_.Exception.Response.StatusDescription
	throw
}

# Upload symbols to Mozilla if feature enabled.
if ($env:feature_buildSymbols -and $env:feature_uploadSymbolsToMozilla) {
	py -m pip install --upgrade --no-warn-script-location pip
	py -m pip install --no-warn-script-location requests
	Try {
		py appveyor\mozillaSyms.py
	}
	Catch {
		Add-AppveyorMessage "Unable to upload symbols to Mozilla"
	}
}
