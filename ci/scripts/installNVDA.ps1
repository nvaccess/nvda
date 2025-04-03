$errorCode=0
$nvdaLauncherFile=$(Resolve-Path "$env:nvdaLauncherDir\nvda*.exe")
$installerLogFilePath="$env:nvdaInstallerLogDir\nvda_install_temp.log"
$installerLogFileCopyPath="$env:nvdaInstallerLogDir\nvda.log"
$installerCrashDumpPath="$env:nvdaInstallerLogDir\nvda_crash.dmp"
$installerProcess=Start-Process -FilePath "$nvdaLauncherFile" -ArgumentList "--install-silent --debug-logging --log-file $installerLogFilePath" -passthru
try {
	$installerProcess | Wait-Process -Timeout 180 -ErrorAction Stop
	$errorCode=$installerProcess.ExitCode
} catch {
	Write-Output "NVDA installer process timed out. `n" >> $env:GITHUB_STEP_SUMMARY
	$errorCode=1
}
# If the installer failed to exit the log file is still in use.
# We can't/shouldn't upload a file which is locked,
# as a work around create a copy of the log and upload that instead.
Copy-Item $installerLogFilePath $installerLogFileCopyPath
if (Test-Path -Path $installerCrashDumpPath){
	Write-Output "NVDA installer process crashed. `n" >> $env:GITHUB_STEP_SUMMARY
	$errorCode=1
}
if ($errorCode -ne 0) { $host.SetShouldExit($errorCode) }
