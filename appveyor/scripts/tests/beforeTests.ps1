New-Item -ItemType directory -Path testOutput
New-Item -ItemType directory -Path testOutput\unit
New-Item -ItemType directory -Path testOutput\system
New-Item -ItemType directory -Path testOutput\lint
# The first system test to run that requires chrome occasionally fails.
# This has been replicated on developer machines after chrome updates,
# however it is difficult to reproduce, and difficult to detect/recover-from
# in an automated way.
# It may be possible to handle this better within NVDA, however it seems to actually affect users
# infrequently, and they seem to be able to recover by waiting a few seconds and de/refocus chrome.
# In the mean time, the system tests failing delays development.
#
# Theory: Chrome is busy with post install tasks, so start chrome in the background ahead of the tests.
# Use the same arguments to start Chrome as the system tests, some arguments are only observed for the first
# start of Chrome.
$chromeStartArgsString = $(py tests/system/libraries/_chromeArgs.py)
$chromeStartArgsArray = $chromeStartArgsString -split " "

cmd /c start /min $chromeStartArgsArray
Set-AppveyorBuildVariable "testFailExitCode" 0
