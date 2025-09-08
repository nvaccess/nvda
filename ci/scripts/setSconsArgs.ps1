$ErrorActionPreference = "Stop";
$sconsOutTargets = "developerGuide changes userGuide keyCommands client moduleList"
$sconsArgs = "version=$env:version"
if ($env:release) {
	$sconsArgs += " release=1"
}
if ($env:versionType) {
	$sconsArgs += " updateVersionType=$env:versionType"
}
$sconsArgs += " publisher=`"$env:scons_publisher`""
if ($env:GITHUB_EVENT_NAME -eq "push" -and $env:apiSigningToken) {
	$sconsArgs += " apiSigningToken=$env:apiSigningToken"
}
$sconsArgs += " version_build=$([int]$env:GITHUB_RUN_NUMBER + [int]$env:START_BUILD_NUMBER)"
Write-Output "sconsOutTargets=$sconsOutTargets" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
Write-Output "sconsArgs=$sconsArgs" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
Write-Host "scons args: $sconsArgs"
Write-Host "scons output targets: $sconsOutTargets"
