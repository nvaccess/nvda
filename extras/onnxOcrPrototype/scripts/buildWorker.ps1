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
$WorkerExecutable = Join-Path $RuntimeDirectory "onnxOcrWorker.exe"
$WorkerBytes = [System.IO.File]::ReadAllBytes($WorkerExecutable)
if ($WorkerBytes.Length -lt 64) {
	throw "Worker executable is too small to contain a valid PE header"
}
$PeOffset = [System.BitConverter]::ToInt32($WorkerBytes, 0x3C)
if ($PeOffset -lt 0 -or $PeOffset + 6 -gt $WorkerBytes.Length) {
	throw "Worker executable has an invalid PE header offset"
}
$PeSignature = [System.Text.Encoding]::ASCII.GetString($WorkerBytes, $PeOffset, 4)
$PeMachine = [System.BitConverter]::ToUInt16($WorkerBytes, $PeOffset + 4)
if ($PeSignature -ne "PE`0`0" -or $PeMachine -ne 0x8664) {
	throw ("Worker must be an x64 PE executable; signature={0}, machine=0x{1:X4}" -f $PeSignature, $PeMachine)
}
Write-Host "Worker created at $RuntimeDirectory\onnxOcrWorker.exe"
