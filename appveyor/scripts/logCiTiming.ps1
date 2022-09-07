# Input: ../timing.csv
# Expect two cols:
#   - Build-stage name
#   - Time [Get-Date -o] (Round trip format)
# Process: add elapsed minutes between entries
# Output:
# - timingWithElapsed.csv
# - CI Timing message to Appveyor messages.

$entries = Import-Csv -Path ../timing.csv -Header Stage, Time
$lastTime = Get-Date -Date $entries[0].Time

foreach ($e in $entries) {
	$nextTime = Get-Date -Date $e.Time
	$elapsedMin = ($nextTime - $lastTime).TotalMinutes
	$e | Add-Member -NotePropertyName ElapsedMin -NotePropertyValue $elapsedMin
	$lastTime = $nextTime
}

$processedTimesFile = "BuildStageTimingWithElapsed.csv"
$entries | Export-Csv -Path $processedTimesFile
$mesg = $entries | Format-Table | out-string
Add-AppveyorMessage ("CI timing: " + $mesg)

if (Test-Path -Path $processedTimesFile){
	Push-AppveyorArtifact $processedTimesFile -FileName $processedTimesFile
}
