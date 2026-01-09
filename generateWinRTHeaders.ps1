# Script to generate C++/WinRT projection headers for Windows App SDK
# This must be run before building NVDA to generate the necessary WinRT headers

$ErrorActionPreference = 'Stop'

$cppWinRTExe = "Microsoft.Windows.CppWinRT.2.0.250303.1\bin\cppwinrt.exe"
$outputDir = "nvdaHelper\localWin10\Generated"
$aiWinmdDir = "Microsoft.WindowsAppSDK.AI.2.0.20-experimental\metadata"
$mlWinmdDir = "Microsoft.WindowsAppSDK.ML.2.0.36-experimental\metadata"
$foundationWinmdDir = "Microsoft.WindowsAppSDK.Foundation.2.0.2-experimental\metadata"

# Find Windows SDK
$windowsSdkDir = "${env:ProgramFiles(x86)}\Windows Kits\10"
$sdkVersion = Get-ChildItem "$windowsSdkDir\References" -Directory |
    Where-Object { $_.Name -match '^\d+\.\d+\.\d+\.\d+$' } |
    Sort-Object Name -Descending |
    Select-Object -First 1 -ExpandProperty Name

if (-not $sdkVersion) {
    Write-Error "Windows SDK not found"
    exit 1
}

$windowsMetadata = "$windowsSdkDir\References\$sdkVersion\Windows.Foundation.FoundationContract"

if (-not (Test-Path $cppWinRTExe)) {
    Write-Error "C++/WinRT compiler not found at: $cppWinRTExe"
    Write-Host "Please install it with: nuget install Microsoft.Windows.CppWinRT -Source https://api.nuget.org/v3/index.json"
    exit 1
}

if (-not (Test-Path $mlWinmdDir)) {
    Write-Error "Windows App SDK ML metadata not found at: $mlWinmdDir"
    Write-Host "Please install it with: nuget install Microsoft.WindowsAppSDK -Version 2.0.0-experimental2 -Source https://api.nuget.org/v3/index.json"
    exit 1
}

# Create output directory
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

Write-Host "Generating C++/WinRT projection headers..."
Write-Host "Output directory: $outputDir"
Write-Host "Windows SDK: $sdkVersion"

# Generate projections for Windows App SDK Machine Learning
& $cppWinRTExe `
    -in "$windowsSdkDir\UnionMetadata\$sdkVersion" `
    -in "$mlWinmdDir\Microsoft.Windows.AI.MachineLearning.winmd" `
    -in "$foundationWinmdDir\Microsoft.Windows.ApplicationModel.DynamicDependency.winmd" `
    -in "$foundationWinmdDir\Microsoft.Windows.ApplicationModel.WindowsAppRuntime.winmd" `
    -out "$outputDir" `
    -include Windows.Foundation `
    -include Windows.Foundation.Collections `
    -include Microsoft.Windows.ApplicationModel.DynamicDependency `
    -include Microsoft.Windows.ApplicationModel.WindowsAppRuntime `
    -include Microsoft.Windows.AI.MachineLearning `
    -verbose

if ($LASTEXITCODE -eq 0) {
    Write-Host "Successfully generated WinRT headers in $outputDir" -ForegroundColor Green
} else {
    Write-Error "Failed to generate WinRT headers (exit code: $LASTEXITCODE)"
    exit $LASTEXITCODE
}
