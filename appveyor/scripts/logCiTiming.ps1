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
}

$entries | Export-Csv -Append -Path timingWithElapsed.csv

Add-AppveyorMessage "CI timing:\n$entries"
