[CmdletBinding()]
param(
	[Parameter(ValueFromRemainingArguments = $true)]
	[string[]]$UvArgs
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
[Version]$UvVersion = '0.7.9'

function Invoke-Uv {
	& uv @UvArgs
	exit $LASTEXITCODE
}

function Install-Uv {
	param(
		[Switch]$IsUpdate
	)

	$installAction = if ($IsUpdate) { 'Update' } else { 'Install' }
	$hasWinGet = [bool](Get-Command winget -ErrorAction SilentlyContinue)
	if ($IsUpdate) {
		Write-Host 'Uv is out of date.'
	}
	else {
		Write-Host 'Uv is not installed.'
	}
	Write-Host ''
	Write-Host "Choose how to $($installAction.ToLower()) uv:"

	while ($true) {
		if ($hasWinGet) {
			Write-Host "[1] $installAction using WinGet (recommended)"
		}
		else {
			Write-Host 'WinGet is NOT available.'
		}
		Write-Host "[2] $installAction using the official uv install script"
		Write-Host '[0] Exit'

		$choice = Read-Host 'Enter your choice'

		switch ($choice) {
			'0' { exit }
			'1' {
				if (-not $hasWinGet) {
					Write-Warning 'WinGet is not available. Please choose another option.'
					continue
				}
				$WinGetArgs = @('--accept-source-agreements', '--disable-interactivity' , '-e', 'astral-sh.uv')
				try {
					if ($IsUpdate) {
						Write-Host 'Updating uv using WinGet...'
						& winget update @WinGetArgs
					}
					else {
						Write-Host 'Installing uv using WinGet...'
						& winget install $WinGetArgs
					}
					if ($LASTEXITCODE -ne 0) {
						throw "winget command failed with exit code $LASTEXITCODE"
					}
					return
				}
				catch {
					Write-Error "Failed to $($installAction.ToLower()) uv using WinGet: $_"
				}
			}
			'2' {
				try {
					Write-Host 'Installing uv using the official script...'
					Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
					$env:PATH = "$(Join-Path $env:USERPROFILE '.local bin');$env:PATH"
					return
				}
				catch {
					Write-Error "Failed to install uv via the official script: $_"
				}
			}
			default {
				Write-Warning "Invalid choice: '$choice'. Please try again."
			}
		}
	}
}

# Main Script Logic

$hasUv = [bool](Get-Command uv -ErrorAction SilentlyContinue)

if ($hasUv) {
	try {
		$json = uv self version --output-format json | ConvertFrom-Json
		[Version]$installedVersion = $json.Version
	}
	catch {
		Write-Warning 'Could not retrieve uv version.'
		[Version]$installedVersion = '0.0.0'
	}

	if ($installedVersion -ge $UvVersion) {
		Invoke-Uv
	}
	else {
		Write-Host "uv version $installedVersion is installed, but version $UvVersion or higher is required. Trying to update..."
		uv self update
		if ($LASTEXITCODE -ne 0) {
			Write-Warning 'Prompting for manual install/update.'
			Install-Uv -IsUpdate
		}

	}
}
else {
	Install-Uv
}
Invoke-Uv
