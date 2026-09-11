# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Noelia Ruiz Martínez, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

# The first Chrome system test to run occasionally fails.
# This has been observed on developer machines after chrome updates, but is difficult to reproduce.
# When this occurs the NVDA logs indicate that no virtual buffer is created.
# It isn't known if this is a bug in Chrome or NVDA.
# The problem does not seem to affect users frequently, and when it does
# recovery is possible by waiting a few seconds before switching to another app
# and then back to Chrome.
# The system tests failing has an impact on NVDA development, requiring confirmation of the cause of
# failed tests, re-running builds, and lowered confidence in automated testing.
#
# Theory: Chrome is busy with post install tasks, so start Chrome in the background ahead of the tests.
# Use the same arguments to start Chrome as the system tests, some arguments are only observed for the first
# start of Chrome.
$chromeWarmUpTimeoutSeconds = 30
$chromeStartArgsString = & py tests/system/libraries/_chromeArgs.py
if ($LastExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($chromeStartArgsString)) {
	Write-Output "Chrome warm-up: unable to read arguments, skipped."
} else {
	$chromeExe, $chromeStartArgs = $chromeStartArgsString.Trim() -split "\s+"
	Start-Process -FilePath $chromeExe -ArgumentList $chromeStartArgs -WindowStyle Minimized
	$warmUpDeadline = (Get-Date).AddSeconds($chromeWarmUpTimeoutSeconds)
	do {
		$warmedChrome = Get-Process chrome -ErrorAction SilentlyContinue |
			Where-Object MainWindowHandle -ne 0 |
			Select-Object -First 1
		if ($warmedChrome) {
			break
		}
		Start-Sleep -Milliseconds 500
	} while ((Get-Date) -lt $warmUpDeadline)
	if ($warmedChrome) {
		# --keep-alive-for-test holds the process open with no windows.
		$warmedChrome.CloseMainWindow() | Out-Null
		Write-Output "Chrome warm-up: window opened and closed, process kept alive."
	} else {
		Write-Output "Chrome warm-up: no Chrome window within ${chromeWarmUpTimeoutSeconds}s, continuing."
	}
}

if ($env:RUNNER_DEBUG) {
	$verboseDebugLogging="True"
} else {
	$verboseDebugLogging=""
}

# This tag is used to exclude system tests.
# If provided to runsystemtests, RF would give an error.
$SKIP_SYS_TESTS = "excluded_from_build"
$tagsForTest = "installer NVDA"  # include the tests tagged with installer, or NVDA
if ($env:INCLUDE_SYSTEM_TEST_TAGS) {
	if ($env:INCLUDE_SYSTEM_TEST_TAGS -eq $SKIP_SYS_TESTS) {
		# Indicate the tests were skipped, and exit early.
		Write-Output "Skipped: System tests." >> $env:GITHUB_STEP_SUMMARY
		return
	}
	$tagsForTest = $env:INCLUDE_SYSTEM_TEST_TAGS

}
$tagsForTestArray = -split $tagsForTest # turn this string into an array
$includeTags = $tagsForTestArray | ForEach-Object {
	# Before every item output '--include'
	# No spaces required.
	# Including spaces will result in automatic quote characters around the string. i.e. "--include "
	"--include", $_
}

$nvdaLauncherFile=$(Resolve-Path "$env:nvdaLauncherDir\nvda*.exe")
.\runsystemtests.bat `
--variable whichNVDA:installed `
--variable installDir:"${nvdaLauncherFile}" `
--variable verboseDebugLogging:"${verboseDebugLogging}" `
@includeTags `
# last line intentionally blank, allowing all lines to have line continuations.
if ($LastExitCode -ne 0) {
	Write-Output "FAIL: System tests (tags: ${tagsForTest}). See test results for more information."  >> $env:GITHUB_STEP_SUMMARY
	Write-Output "testFailExitCode=$LastExitCode" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
}
exit $LastExitCode
