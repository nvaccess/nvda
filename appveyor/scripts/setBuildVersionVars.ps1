$ErrorActionPreference = "Stop";

# Accessing Windows build worker via Remote Desktop (RDP)
# To enable:
# Set an RDP password (before triggering the build), ensure password requirements are met.
# Remove the password after the RDP connection params are shown in the build output.
# For passwords requirements and instructions for setting, see the appveyor docs:
# https://www.appveyor.com/docs/how-to/rdp-to-build-worker/
if ($env:APPVEYOR_RDP_PASSWORD) {
	$rdpScriptURL = 'https://raw.githubusercontent.com/appveyor/ci/master/scripts/enable-rdp.ps1'
	iex ((new-object net.webclient).DownloadString($rdpScriptURL))
}

$pythonVersion = (py --version)
echo $pythonVersion
if ($env:APPVEYOR_REPO_TAG_NAME -and $env:APPVEYOR_REPO_TAG_NAME.StartsWith("release-")) {
	# Strip "release-" prefix.
	$version = $env:APPVEYOR_REPO_TAG_NAME.Substring(8)
	Set-AppveyorBuildVariable "release" "1"
	if ($env:APPVEYOR_REPO_TAG_NAME.Contains("rc") -or $env:APPVEYOR_REPO_TAG_NAME.Contains("beta")) {
		$versionType = "beta"
	} else {
		$versionType = "stable"
	}
} else {
	$commitVersion = $env:APPVEYOR_REPO_COMMIT.Substring(0, 8)
	if($env:APPVEYOR_PULL_REQUEST_NUMBER) {
		$version = "pr$env:APPVEYOR_PULL_REQUEST_NUMBER-$env:APPVEYOR_BUILD_NUMBER," + $commitVersion
	} elseif($env:APPVEYOR_REPO_BRANCH -eq "master") {
		$version = "alpha-$env:APPVEYOR_BUILD_NUMBER," + $commitVersion
	} else {
		$version = "$env:APPVEYOR_REPO_BRANCH-$env:APPVEYOR_BUILD_NUMBER," + $commitVersion
		if($env:APPVEYOR_REPO_BRANCH.StartsWith("try-release-")) {
			Set-AppveyorBuildVariable "release" "1"
		}
	}
	# The version is unique even for rebuilds, so we can use it for the AppVeyor version.
	Update-AppveyorBuild -Version $version
	if($env:APPVEYOR_REPO_BRANCH -eq "master") {
		$versionType = "snapshot:alpha"
	} elseif (!$env:APPVEYOR_REPO_BRANCH.StartsWith("try-")) {
		$versionType = "snapshot:$env:APPVEYOR_REPO_BRANCH"
	}
}
Set-AppveyorBuildVariable "version" $version
if ($versionType) {
	Set-AppveyorBuildVariable "versionType" $versionType
}
