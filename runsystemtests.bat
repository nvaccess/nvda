@echo off
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
set systemTestsPath=%here%\tests\system

call uv run --group system-tests --directory "%here%" -m robot --argumentfile "%systemTestsPath%\robotArgs.robot" %* "%systemTestsPath%\robot"
