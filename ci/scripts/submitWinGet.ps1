$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Strip the 'release-' prefix to get the package version
$packageVersion = $env:GITHUB_REF_NAME -replace '^release-', ''

# Determine stable/beta/rc package ID
$isBeta = $env:GITHUB_REF_NAME -match 'beta'
$isRc = $env:GITHUB_REF_NAME -match 'rc'
$wingetPackageId = if ($isBeta) { "NVAccess.NVDA.Beta" } elseif ($isRc) { "NVAccess.NVDA.RC" } else { "NVAccess.NVDA" }

# Get .exe asset URL from GitHub release
$releaseAssets = gh release view $env:GITHUB_REF_NAME `
  --repo $env:GITHUB_REPOSITORY `
  --json assets | ConvertFrom-Json
$installerUrl = ($releaseAssets.assets | Where-Object { $_.name -like "*.exe" }).url

# Sync winget-pkgs repository with upstream master branch before opening a PR
$githubToken = $env:GH_TOKEN
try {
  # We need the user's GitHub token to sync the repository
	$env:GH_TOKEN = $env:WINGET_CREATE_GITHUB_TOKEN
	gh repo sync nvaccessAuto/winget-pkgs -b master
} finally {
	$env:GH_TOKEN = $githubToken
}

# Install wingetcreate and submit PR
winget install --id Microsoft.WingetCreate --installer-type msix --source winget
wingetcreate update $wingetPackageId `
  --version $packageVersion `
  --urls $installerUrl `
  --submit
