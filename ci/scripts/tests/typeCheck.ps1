$pyrightOutput = (uv run pyright) -Join "`n"
if ($LastExitCode -ne 0) {
	Write-Output @"
FAIL: Static type analysis. Pyright exited with exit code $LastExitCode.
<details>
<summary>Type analysis errors</summary>

``````
$pyrightOutput
``````

</details>

"@ >> $env:GITHUB_STEP_SUMMARY
}
exit $LastExitCode
