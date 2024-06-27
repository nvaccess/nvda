# Input: ../timing.csv
# Expect two cols:
#   - Build-stage name
#   - Time [Get-Date -o] (Round trip format)
# Process: add elapsed minutes between entries
# Output:
# - buildStageTimingWithElapsed.csv
# - CI Timing message to Appveyor messages.
$inputFile = "../timing.csv"
$processedTimesFile = "buildStageTimingWithElapsed.csv"

# Don't run if timing record was not created for some reason
if (!(Test-Path -LiteralPath $inputFile)) {
	exit
}

$entries = Import-Csv -Path $inputFile -Header Stage, Time
$lastTime = Get-Date -Date $entries[0].Time

foreach ($e in $entries) {
	$nextTime = Get-Date -Date $e.Time
	$elapsedMin = ($nextTime - $lastTime).TotalMinutes
	$e | Add-Member -NotePropertyName ElapsedMin -NotePropertyValue $elapsedMin
	$lastTime = $nextTime
}

$entries | Export-Csv -Path $processedTimesFile

$mesgs = (
	$entries.foreach({
		($_.Stage, $_.ElapsedMin.tostring('N1')) -join " "
	})
) -join ", `n"

Add-AppveyorMessage ("CI timing (mins): `n" + $mesgs)

if (Test-Path -Path $processedTimesFile){
	Push-AppveyorArtifact $processedTimesFile -FileName $processedTimesFile
}
