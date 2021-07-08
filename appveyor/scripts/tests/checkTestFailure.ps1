$ErrorActionPreference = "Stop";
if($env:testFailExitCode -ne 0) { $host.SetShouldExit($env:testFailExitCode) }
