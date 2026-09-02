$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.IO.Compression.FileSystem
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$AddonRoot = Join-Path $ProjectRoot "nvdaAddon"
$WorkerExecutable = Join-Path $AddonRoot "globalPlugins\onnxOcrPrototype\workerRuntime\onnxOcrWorker.exe"
$OutputDirectory = Join-Path $ProjectRoot "dist"
$OutputPath = Join-Path $OutputDirectory "onDeviceOcr-0.2.0.nvda-addon"

& (Join-Path $PSScriptRoot "buildWorker.ps1")

New-Item -ItemType Directory -Force $OutputDirectory | Out-Null
if (Test-Path $OutputPath) {
	Remove-Item -Force $OutputPath
}
[System.IO.Compression.ZipFile]::CreateFromDirectory($AddonRoot, $OutputPath)
Write-Host "NVDA add-on created at $OutputPath"
