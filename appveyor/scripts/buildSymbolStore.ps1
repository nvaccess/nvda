$ErrorActionPreference = "Stop";
if (!$env:feature_buildSymbols) {
	exit
}

foreach ($syms in
	# We don't just include source\*.dll because that would include system dlls.
	"source\liblouis.dll", "source\*.pdb",
	"source\lib\*.dll", "source\lib\*.pdb",
	# We include source\lib64\*.exe to cover nvdaHelperRemoteLoader.
	"source\lib64\*.dll", "source\lib64\*.exe", "source\lib64\*.pdb",
	"source\synthDrivers\*.dll", "source\synthDrivers\*.pdb"
) {
	# https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/symstore-command-line-options
	& $env:symstore add /f $syms /s symbols /t NVDA /compress
}
