$ErrorActionPreference = "Stop";
$sconsDocsOutTargets = "developerGuide changes userGuide keyCommands user_docs"
$sconsLauncherOutTargets = "launcher client moduleList"
$sconsArgs = "version=$env:version"
$sconsCores = "-j1"
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
Write-Output "sconsDocsOutTargets=$sconsDocsOutTargets" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
Write-Output "sconsLauncherOutTargets=$sconsLauncherOutTargets" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
Write-Output "sconsArgs=$sconsArgs" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
Write-Output "sconsCores=$sconsCores" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
Write-Host "scons args: $sconsArgs"
Write-Host "scons docs output targets: $sconsDocsOutTargets"
Write-Host "scons launcher output targets: $sconsLauncherOutTargets"
Write-Host "scons cores: $sconsCores"
