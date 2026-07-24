param(
	[Parameter(Mandatory)]
	[string]$branchName
)

$PSNativeCommandUseErrorActionPreference = $false
$ErrorActionPreference= "Continue"

git checkout -b $branchName
git config --local user.name "GitHub Actions"
git config --local user.email "github-actions@github.com"

# Temporary file to store all collected reports.
$tempfile = New-TemporaryFile
$errordir = New-Item -ItemType "Directory" -Path "$env:TEMP" -Name $((New-Guid).ToString("N"))
$errorfiles = @()

# Check each modified tracked po file,
# and collect language codes pushed down the pipeline in an array.
$failures = @(git ls-files --modified "source/locale/**.po" | ForEach-Object {
	Write-Host -NoNewline "Checking $_ ... "
	$output = uv run source/l10nutil.py checkPo "$_"
	if ($LASTEXITCODE -eq 0) {
		# Add files that don't produce errors.
		Write-Host "Ok"
		git add "$_"
	} else {
		# This file produced errors.
		Write-Host "Failed"
		# Get the language code by stripping the last 2 segments (LC_MESSAGES\nvda.po),
		# and getting the leaf (the trailing path component),
		$lang = $_ | Split-Path | Split-Path | Split-Path -Leaf
		Write-Host "::error file=${_}::[$lang] Validation errors in user interface translations"
		$errorfile = New-Item -ItemType "File" -Path $errordir -Name "$lang.txt"
		Add-Content -Path $tempfile -Value "`n<details><summary><code>$_</code></summary>`n`n``````"
		Write-Host "::group::Validation results for $_"
		Add-Content -Path $tempfile,$errorfile -Value $output -PassThru | Out-String | Write-host
		Write-Host "::endgroup::"
		Add-Content -Path $tempfile -Value "```````n`n</details>`n"
		$errorfiles += $errorfile

		# and push it down the pipeline
		$lang
	}
})

if ($failures.Count -gt 0) {
	# $At least one language failed validation.
	Add-Content -Path $env:GITHUB_OUTPUT -Value "has_failures=true"
	Add-Content -Path $env:GITHUB_OUTPUT -Value "invalid_pofile_locales=$($failures -join ", ")"
	Add-Content -Path $env:GITHUB_OUTPUT -Value "report_files=$($errorfiles.FullName | ConvertTo-Json -Compress)"
	# Add-Content -Path $env:GITHUB_OUTPUT -Value "invalid_pofile_reports<<EOF"
	# Add-Content -Path $env:GITHUB_OUTPUT -Value (Get-Content -Path $tempfile -Raw).TrimEnd()
	# Add-Content -Path $env:GITHUB_OUTPUT -Value "EOF"
	# Add-Content -Path $env:GITHUB_STEP_SUMMARY -Value "### Validation errors`n",(Get-Content -Path $tempfile)
} else {
	Add-Content -Path $env:GITHUB_OUTPUT -Value "has_failures=false"
}

# Add modified tracked xliff files.
git add -u user_docs

# Check if there are any changes to commit
git diff --staged --quiet
if ($LASTEXITCODE -eq 0) {
	Write-Host "No changes to commit"
	Add-Content -Path $env:GITHUB_OUTPUT -Value "has_changes=false"
} else {
	git commit -m "Update tracked translations from Crowdin"
	Add-Content -Path $env:GITHUB_OUTPUT -Value "has_changes=true"
}
