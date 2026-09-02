$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$AddonRoot = Join-Path $ProjectRoot "nvdaAddon"
$WorkerExecutable = Join-Path $AddonRoot "globalPlugins\onnxOcrPrototype\workerRuntime\onnxOcrWorker.exe"
$OutputDirectory = Join-Path $ProjectRoot "dist"
$OutputPath = Join-Path $OutputDirectory "onDeviceOcr-0.2.0.nvda-addon"
$RepositoryRoot = (Resolve-Path (Join-Path $ProjectRoot "..\..")).Path
$BundledMsgfmt = Join-Path $RepositoryRoot "miscDeps\tools\msgfmt.exe"

if (Test-Path $BundledMsgfmt) {
	$Msgfmt = $BundledMsgfmt
} else {
	$MsgfmtCommand = Get-Command "msgfmt" -ErrorAction SilentlyContinue
	if ($null -eq $MsgfmtCommand) {
		throw "msgfmt was not found. Initialize NVDA's miscDeps submodule or install GNU gettext."
	}
	$Msgfmt = $MsgfmtCommand.Source
}

$LocaleSources = Get-ChildItem -Path (Join-Path $AddonRoot "locale") -Recurse -File -Filter "*.po"
foreach ($PoFile in $LocaleSources) {
	$MoPath = [System.IO.Path]::ChangeExtension($PoFile.FullName, ".mo")
	& $Msgfmt "--check" "--output-file=$MoPath" $PoFile.FullName
	if ($LASTEXITCODE -ne 0) {
		throw "Failed to compile locale catalog: $($PoFile.FullName)"
	}
}

& (Join-Path $PSScriptRoot "buildWorker.ps1")

New-Item -ItemType Directory -Force $OutputDirectory | Out-Null
if (Test-Path $OutputPath) {
	Remove-Item -Force $OutputPath
}
$Archive = [System.IO.Compression.ZipFile]::Open(
	$OutputPath,
	[System.IO.Compression.ZipArchiveMode]::Create
)
try {
	$AddonRootPrefix = $AddonRoot.TrimEnd("\") + "\"
	$Files = Get-ChildItem -Path $AddonRoot -Recurse -File | Where-Object {
		$_.FullName -notmatch "\\__pycache__\\" -and
		$_.Extension -notin @(".pyc", ".pyo", ".part", ".po") -and
		$_.Name -notin @(".DS_Store", "Thumbs.db")
	} | Sort-Object FullName
	foreach ($File in $Files) {
		$RelativePath = $File.FullName.Substring($AddonRootPrefix.Length).Replace("\", "/")
		[System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
			$Archive,
			$File.FullName,
			$RelativePath,
			[System.IO.Compression.CompressionLevel]::Optimal
		) | Out-Null
	}
} finally {
	$Archive.Dispose()
}
Write-Host "NVDA add-on created at $OutputPath"
