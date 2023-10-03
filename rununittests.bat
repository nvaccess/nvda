@echo off
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
set scriptsDir=%here%\venvUtils
set unitTestsPath=%here%\tests\unit

call "%scriptsDir%\venvCmd.bat" py -m unittest discover -v -s "%unitTestsPath%" -t "%here%" %*
