$ErrorActionPreference = "Stop";
$sconsOutTargets = "launcher developerGuide changes userGuide keyCommands client moduleList"
if(!$env:APPVEYOR_PULL_REQUEST_NUMBER -and $env:feature_buildAppx) {
	$sconsOutTargets += " appx"
}
$sconsArgs = "version=$env:version"
if ($env:release) {
	$sconsArgs += " release=1"
}
if ($env:versionType) {
	$sconsArgs += " updateVersionType=$env:versionType"
}
$sconsArgs += " publisher=`"$env:scons_publisher`""
if (!$env:APPVEYOR_PULL_REQUEST_NUMBER -and $env:feature_signing) {
	$sconsArgs += " apiSigningToken=$env:apiSigningToken"
}
$sconsArgs += " version_build=$env:APPVEYOR_BUILD_NUMBER"
# We use cmd to run scons because PowerShell throws exceptions if warnings get dumped to stderr.
# It's possible to work around this, but the workarounds have annoying side effects.
Set-AppveyorBuildVariable "sconsOutTargets" $sconsOutTargets
Set-AppveyorBuildVariable "sconsArgs" $sconsArgs
Write-Host "scons args: $sconsArgs"
Write-Host "scons output targets: $sconsOutTargets"
