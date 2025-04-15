$ErrorActionPreference = "Stop";
if (!$env:APPVEYOR_PULL_REQUEST_NUMBER -and $env:versionType) {
	# Not a pr build 
	if ($env:APPVEYOR_REPO_BRANCH -eq "beta" -and $env:feature_crowdinSync) {
		# Upload files to Crowdin for translation
		py -m pip install --no-warn-script-location requests
		py appveyor\crowdinSync.py uploadSourceFile 2 output\nvda.pot 2>&1
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

# Save an exact list of the actual Python packages and their versions that got installed, to aide in reproducing a build
.\venvUtils\exportPackageList.bat installed_python_packages.txt
Push-AppveyorArtifact installed_python_packages.txt
$appVeyorUrl = "https://ci.appveyor.com"
$exe = Get-ChildItem -Name output\nvda_*.exe
if($?){
	$exeUrl="$appVeyorUrl/api/buildjobs/$env:APPVEYOR_JOB_ID/artifacts/output/$exe"
	if ($env:APPVEYOR_PULL_REQUEST_NUMBER -ne $null) {
		Add-AppveyorMessage "Build (for testing PR): $exeUrl"
	} else {
		Add-AppveyorMessage "Build (for testing branch): $exeUrl"
	}
}
