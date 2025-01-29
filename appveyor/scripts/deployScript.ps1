$ErrorActionPreference = "Stop";
if (!$env:APPVEYOR_PULL_REQUEST_NUMBER -and $env:versionType) {
	# Not a try build.
	if ($env:APPVEYOR_REPO_BRANCH -eq "beta" -and $env:feature_crowdinSync) {
		# Upload files to Crowdin for translation
		py -m pip install --no-warn-script-location requests
		py appveyor\crowdinSync.py uploadSourceFile 2 output\nvda.pot 2>&1
	}
	# Notify the NV Access server if this is an NV Access build.
	if ($env:APPVEYOR_REPO_NAME.StartsWith("nvaccess/")) {
		$exe = Get-ChildItem -Name output\nvda_*.exe
		$hash = (Get-FileHash "output\$exe" -Algorithm SHA1).Hash.ToLower()
		$apiVersion = (py -c "import sys; sys.path.append('source'); from addonAPIVersion import CURRENT; print('{}.{}.{}'.format(*CURRENT))")
		echo apiversion: $apiVersion
		$apiCompatTo = (py -c "import sys; sys.path.append('source'); from addonAPIVersion import BACK_COMPAT_TO; print('{}.{}.{}'.format(*BACK_COMPAT_TO))")
		echo apiBackCompatTo: $apiCompatTo

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
		ConvertTo-Json -InputObject $data -Compress | Out-File -FilePath deploy.json
		Push-AppveyorArtifact deploy.json
		
		# Send to the new API endpoint
		try {
			# Debug: Print the JSON payload
			Write-Host "Sending JSON payload to NV Access server:"
			Write-Host (Get-Content deploy.json -Raw)
			
			$response = Invoke-RestMethod -Uri "https://api.nvaccess.org/appveyor-hook" `
				-Method Post `
				-Headers @{
					"Authorization" = "Bearer $env:APPVEYOR_WEBHOOK_TOKEN"
					"Content-Type" = "application/json"
				} `
				-Body (Get-Content deploy.json -Raw)
			Write-Host "Successfully notified NV Access server"
		}
		catch {
			Write-Host "Failed to notify NV Access server: $_"
			throw
		}
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
}
