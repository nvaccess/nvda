@echo off
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
set scriptsDir=%here%\venvUtils
set unitTestsPath=%here%\tests\unit

call "%scriptsDir%\venvCmd.bat" py -m nose -sv --traverse-namespace -w "%unitTestsPath%" %*
