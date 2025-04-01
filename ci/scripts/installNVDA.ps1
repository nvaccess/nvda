$errorCode=0
$outputDir=$(resolve-path .\testOutput)
$installerLogFilePath="$outputDir\nvda_install.log"
$installerProcess=start-process -FilePath "$env:nvdaLauncherFile" -ArgumentList "--install-silent --debug-logging --log-file $installerLogFilePath" -passthru
try {
	$installerProcess | wait-process -Timeout 180 -ErrorAction Stop
	$errorCode=$installerProcess.ExitCode
} catch {
	Write-Output "NVDA installer process timed out"
	$errorCode=1
	# Since installer failed to exit in the specified timeout the log file is still in use.
	# Unfortunately `Push-AppveyorArtifact` is unable to upload a file which is  locked
	# as a work around create a copy of the log and upload that instead.
	$installerLogFileCopiedPath = "nvda_install_copy.log"
	Copy-Item $installerLogFilePath $installerLogFileCopiedPath
}
$crashDump = "$outputDir\nvda_crash.dmp"
if (Test-Path -Path $crashDump){
	$errorCode=1
}
if ($errorCode -ne 0) { $host.SetShouldExit($errorCode) }
