param(
	[Parameter(Mandatory)]
	[string]$branchName
)

$PSNativeCommandUseErrorActionPreference = $false

git checkout -b $branchName
git config --local user.name "GitHub Actions"
git config --local user.email "github-actions@github.com"

# Temporary file to store all collected reports.
$tempfile = New-TemporaryFile

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
		Add-Content -Path $tempfile -Value $output -PassThru | Out-String | Write-Error
		Add-Content -Path $tempfile -Value "----------"

		# Get the language code by stripping the last 2 segments (LC_MESSAGES\nvda.po),
		# and getting the leaf (the trailing path component),
		# and push it down the pipeline
		$path | Split-Path | Split-Path | Split-Path -Leaf
	}
})

if ($failures.Count -gt 0) {
	# $At least one language failed validation.
	Add-Content -Path $env:GITHUB_OUTPUT -Value "has_failures=true
		invalid_pofile_locales=$($failures -join ", ")
		invalid_pofile_reports<<EOF
		$((Get-Content -Path $tempfile -Raw).TrimEnd())
		EOF"
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
