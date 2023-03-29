$errorCode=0
$nvdaLauncherFile=".\output\nvda"
if(!$env:release) {
	$nvdaLauncherFile+="_snapshot"
}
$nvdaLauncherFile+="_${env:version}.exe"
Set-AppveyorBuildVariable "nvdaLauncherFile" $nvdaLauncherFile
echo NVDALauncherFile: $NVDALauncherFile
$outputDir=$(resolve-path .\testOutput)
$installerLogFilePath="$outputDir\nvda_install.log"
$installerProcess=start-process -FilePath "$nvdaLauncherFile" -ArgumentList "--install-silent --debug-logging --log-file $installerLogFilePath" -passthru
try {
	$installerProcess | wait-process -Timeout 180 -ErrorAction Stop
	$errorCode=$installerProcess.ExitCode
	$installerLogFilePathToUpload = $installerLogFilePath
} catch {
	echo "NVDA installer process timed out"
	$errorCode=1
	Add-AppveyorMessage "Unable to install NVDA prior to tests."
	# Since installer failed to exit in the specified timeout the log file is still in use.
	# Unfortunately `Push-AppveyorArtifact` is unable to upload a file which is  locked
	# as a work around create a copy of the log and upload that instead.
	$installerLogFileCopiedPath = "nvda_install_copy.log"
	Copy-Item $installerLogFilePath $installerLogFileCopiedPath
	$installerLogFilePathToUpload = $installerLogFileCopiedPath
}
Push-AppveyorArtifact $installerLogFilePathToUpload -FileName "nvda_install.log"
$crashDump = "$outputDir\nvda_crash.dmp"
if (Test-Path -Path $crashDump){
	Push-AppveyorArtifact $crashDump -FileName "nvda_install_crash.dmp"
	Add-AppveyorMessage "Install process crashed"
	$errorCode=1
}
if($errorCode -ne 0) { $host.SetShouldExit($errorCode) }
