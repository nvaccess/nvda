$ErrorActionPreference = "Stop";
if (!$env:APPVEYOR_PULL_REQUEST_NUMBER -and $env:versionType) {
	# Not a pr build
	if ($env:APPVEYOR_REPO_BRANCH -eq "beta" -and $env:feature_crowdinSync) {
		# Upload files to Crowdin for translation
		uv run --with requests --directory appveyor crowdinSync.py uploadSourceFile 2 output\nvda.pot 2>&1
	}
	# Upload symbols to Mozilla if feature enabled.
	if ($env:feature_buildSymbols -and $env:feature_uploadSymbolsToMozilla) {
		Try {
			uv run --with requests --directory appveyor mozillaSyms.py
		}
		Catch {
			Add-AppveyorMessage "Unable to upload symbols to Mozilla"
		}
	}
}

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
