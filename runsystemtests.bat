@echo off
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
set scriptsDir=%here%\venvUtils
set systemTestsPath=%here%\tests\system

call "%scriptsDir%\venvCmd.bat" py -m robot --argumentfile "%systemTestsPath%\robotArgs.robot" %* "%systemTestsPath%\robot"
