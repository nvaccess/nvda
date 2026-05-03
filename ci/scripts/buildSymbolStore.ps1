$ErrorActionPreference = "Stop";

foreach ($syms in
	# We don't just include source\*.dll because that would include system dlls.
	"source\liblouis.dll",
	"source\*.pdb",
	"source\lib\x64\*.dll",
	"source\lib\x64\*.pdb",
	"source\lib\x86\*.dll",
	"source\lib\x86\*.pdb",
	# We include *.exe to cover nvdaHelperRemoteLoader.
	"source\lib\x86\*.exe",
	"source\lib\arm64\*.dll",
	"source\lib\arm64\*.pdb",
	"source\lib\arm64\*.exe",
	"source\lib\arm64ec\*.dll",
	"source\lib\arm64ec\*.pdb",
	"source\synthDrivers\*.dll",
	"source\synthDrivers\*.pdb"
) {
	# https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/symstore-command-line-options
	& $env:symStore add /f $syms /s symbols /t NVDA /compress
}

Set-Location symbols
7z a -tzip -r ..\output\symbols.zip *.dl_ *.ex_ *.pd_
