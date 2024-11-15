$ErrorActionPreference = "Stop";
# Save an exact list of the actual Python packages and their versions that got installed, to aide in reproducing a build
.\venvUtils\exportPackageList.bat installed_python_packages.txt
Push-AppveyorArtifact installed_python_packages.txt
$appVeyorUrl = "https://ci.appveyor.com"
$exe = Get-ChildItem -Name output\*.exe
if($?){
	$exeUrl="$appVeyorUrl/api/buildjobs/$env:APPVEYOR_JOB_ID/artifacts/output/$exe"
	if ($env:APPVEYOR_PULL_REQUEST_NUMBER -ne $null) {
		Add-AppveyorMessage "Build (for testing PR): $exeUrl"
	} else {
		Add-AppveyorMessage "Build (for testing branch): $exeUrl"
	}
}
