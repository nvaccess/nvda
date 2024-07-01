New-Item -ItemType directory -Path testOutput
New-Item -ItemType directory -Path testOutput\unit
New-Item -ItemType directory -Path testOutput\system
New-Item -ItemType directory -Path testOutput\lint
New-Item -ItemType directory -Path testOutput\license

# The first Chrome system test to run occasionally fails.
# This has been observed on developer machines after chrome updates, but is difficult to reproduce.
# When this occur the NVDA logs indicate that a no virtual buffer is created.
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
$chromeStartArgsString = $(py tests/system/libraries/_chromeArgs.py)
$chromeStartArgsArray = $chromeStartArgsString -split " "

cmd /c start /min $chromeStartArgsArray
Set-AppveyorBuildVariable "testFailExitCode" 0
