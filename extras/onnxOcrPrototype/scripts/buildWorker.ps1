$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PluginRoot = Join-Path $ProjectRoot "nvdaAddon\globalPlugins\onnxOcrPrototype"
$WorkerMain = Join-Path $PluginRoot "workerMain.py"
$RuntimeDirectory = Join-Path $PluginRoot "workerRuntime"
$BuildDirectory = Join-Path $ProjectRoot "build"
$DistributionDirectory = Join-Path $ProjectRoot "dist"
$VirtualEnvironment = Join-Path $ProjectRoot ".venv-worker"
$WorkerPython = Join-Path $VirtualEnvironment "Scripts\python.exe"
$SpecPath = Join-Path $PSScriptRoot "onnxOcrWorker.spec"

$RequiredSystemRuntime = @(
	"$env:SystemRoot\System32\MSVCP140.dll",
	"$env:SystemRoot\System32\VCRUNTIME140.dll",
	"$env:SystemRoot\System32\VCRUNTIME140_1.dll"
)
foreach ($RuntimePath in $RequiredSystemRuntime) {
	if (-not (Test-Path $RuntimePath)) {
		throw "Microsoft Visual C++ 2015-2022 x64 Redistributable is required: $RuntimePath"
	}
}

if (-not (Test-Path $WorkerPython)) {
	py -3.12 -m venv $VirtualEnvironment
}

& $WorkerPython -m pip install --disable-pip-version-check --upgrade pip
& $WorkerPython -m pip install --disable-pip-version-check -r (Join-Path $ProjectRoot "requirements-build.txt")

New-Item -ItemType Directory -Force $RuntimeDirectory | Out-Null
& $WorkerPython -m PyInstaller `
	--clean `
	--noconfirm `
	--distpath $DistributionDirectory `
	--workpath $BuildDirectory `
	$SpecPath

Copy-Item -Force (Join-Path $DistributionDirectory "onnxOcrWorker.exe") $RuntimeDirectory
Write-Host "Worker created at $RuntimeDirectory\onnxOcrWorker.exe"
