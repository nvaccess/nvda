$ErrorActionPreference = "Stop";
if (!$env:APPVEYOR_PULL_REQUEST_NUMBER -and $env:versionType) {
	# Not a try build.
	# Notify our server.
	$exe = Get-ChildItem -Name output\*.exe
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
		artifacts=$artifacts
	}
	ConvertTo-Json -InputObject $data -Compress | Out-File -FilePath deploy.json
	Push-AppveyorArtifact deploy.json
	# Execute the deploy script on the NV Access server via ssh.
	# Warning: if the server address is changed, 
	# The new address must be also included in appveyor\ssh_known_hosts in this repo
	# Otherwise ssh will freeze on input!
	cat deploy.json | ssh nvaccess@deploy.nvaccess.org nvdaAppveyorHook

	# Upload symbols to Mozilla.
	py -m pip install --no-warn-script-location requests
	Try {
		py appveyor\mozillaSyms.py
	}
	Catch {
		Add-AppveyorMessage "Unable to upload symbols to Mozilla"
	}
}
