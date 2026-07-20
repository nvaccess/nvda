# Stop Pyright warning us that we're not running the latest version
$env:PYRIGHT_PYTHON_IGNORE_WARNINGS="1"
(uv run pyright) -Join "`n" | Tee-Object -Variable pyrightOutput
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
