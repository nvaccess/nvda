$ErrorActionPreference = "Stop";

# Accessing Windows build worker via Remote Desktop (RDP)
# To enable:
# Set an RDP password (before triggering the build), ensure password requirements are met.
# Remove the password after the RDP connection params are shown in the build output.
# For passwords requirements and instructions for setting, see the appveyor docs:
# https://www.appveyor.com/docs/how-to/rdp-to-build-worker/

$pythonVersion = (py --version)
echo $pythonVersion
if ($env:GITHUB_REF_TYPE -eq "tag" -and $env:GITHUB_REF_NAME.StartsWith("release-")) {
	# Strip "release-" prefix.
	$version = $env:GITHUB_REF_NAME.Substring(8)
	echo "release=1" | Out-File -FilePath $Env:GITHUB_ENV -Encoding utf8 -Append
	if ($env:GITHUB_REF_TYPE -eq "tag" -and ($env:GITHUB_REF_NAME.Contains("rc") -or $env:GITHUB_REF_NAME.Contains("beta"))) {
		$versionType = "beta"
	} else {
		$versionType = "stable"
	}
} else {
	$commitVersion = $env:GITHUB_SHA.Substring(0, 8)
	if($env:pullRequestNumber) {
		$version = "pr$env:pullRequestNumber-$commitVersion,$env:github.run_attempt"
	} elseif($env:GITHUB_REF_NAME -eq "master") {
		$version = "alpha-$commitVersion,$env:github.run_attempt"
	} else {
		$version = "$env:GITHUB_REF_NAME-$commitVersion,$env:github.run_attempt"
		if($env:GITHUB_REF_NAME.StartsWith("try-release-")) {
			echo "release=1" | Out-File -FilePath $Env:GITHUB_ENV -Encoding utf8 -Append
		}
	}
	if($env:GITHUB_REF_NAME -eq "master") {
		$versionType = "snapshot:alpha"
	} elseif (!$env:GITHUB_REF_NAME.StartsWith("try-") -and !$env:pullRequestNumber) {
		$versionType = "snapshot:$env:GITHUB_REF_NAME"
	}
}
echo "version=$version" | Out-File -FilePath $Env:GITHUB_ENV -Encoding utf8 -Append
if ($versionType) {
	echo "versionType=$versionType" | Out-File -FilePath $Env:GITHUB_ENV -Encoding utf8 -Append
}
