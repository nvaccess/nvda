(uv run ty check) -Join "`n" | Tee-Object -Variable tyOutput
if ($LastExitCode -ne 0) {
	Write-Output @"
FAIL: Static type analysis. ty exited with exit code $LastExitCode.
<details>
<summary>Type analysis errors</summary>

``````
$tyOutput
``````

</details>

"@ >> $env:GITHUB_STEP_SUMMARY
}
exit $LastExitCode
