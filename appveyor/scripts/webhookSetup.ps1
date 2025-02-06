$ErrorActionPreference = "Stop";
# Notify the NV Access server if this is an NV Access build.
if ($env:APPVEYOR_REPO_NAME.StartsWith("nvaccess/")) {
	$exe = Get-ChildItem -Name output\nvda_*.exe
	$hash = (Get-FileHash "output\$exe" -Algorithm SHA1).Hash.ToLower()
	$apiVersion = (py -c "import sys; sys.path.append('source'); from addonAPIVersion import CURRENT; print('{}.{}.{}'.format(*CURRENT))")
	echo apiversion: $apiVersion
	$apiCompatTo = (py -c "import sys; sys.path.append('source'); from addonAPIVersion import BACK_COMPAT_TO; print('{}.{}.{}'.format(*BACK_COMPAT_TO))")
	echo apiBackCompatTo: $apiCompatTo

	# Set environment variables that will be included in the webhook payload
	$env:NVDA_EXE = $exe
	$env:NVDA_HASH = $hash
	$env:NVDA_API_VERSION = $apiVersion
	$env:NVDA_API_COMPAT_TO = $apiCompatTo
	$env:NVDA_VERSION = $env:version
	$env:NVDA_VERSION_TYPE = $env:versionType

	Write-Host "Set NVDA environment variables for webhook"
	Write-Host "NVDA_EXE: $env:NVDA_EXE"
	Write-Host "NVDA_HASH: $env:NVDA_HASH"
	Write-Host "NVDA_API_VERSION: $env:NVDA_API_VERSION"
	Write-Host "NVDA_API_COMPAT_TO: $env:NVDA_API_COMPAT_TO"
	Write-Host "NVDA_VERSION: $env:NVDA_VERSION"
	Write-Host "NVDA_VERSION_TYPE: $env:NVDA_VERSION_TYPE"

	# Show what the webhook payload will look like
	Write-Host "`nWebhook payload will include:"
	Write-Host "accountName: $env:APPVEYOR_ACCOUNT_NAME"
	Write-Host "projectId: $env:APPVEYOR_PROJECT_ID"
	Write-Host "projectName: $env:APPVEYOR_PROJECT_NAME"
	Write-Host "buildId: $env:APPVEYOR_BUILD_ID"
	Write-Host "buildNumber: $env:APPVEYOR_BUILD_NUMBER"
	Write-Host "buildVersion: $env:APPVEYOR_BUILD_VERSION"
	Write-Host "branch: $env:APPVEYOR_REPO_BRANCH"
	Write-Host "commitId: $env:APPVEYOR_REPO_COMMIT"
	Write-Host "commitAuthor: $env:APPVEYOR_REPO_COMMIT_AUTHOR"
	Write-Host "commitMessage: $env:APPVEYOR_REPO_COMMIT_MESSAGE"
	Write-Host "jobId: $env:APPVEYOR_JOB_ID"

	Write-Host "`nArtifacts that will be included:"
	Get-ChildItem output\* | ForEach-Object {
		Write-Host "- $($_.Name)"
	}
}
