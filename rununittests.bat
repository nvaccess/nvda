@echo off
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
set scriptsDir=%here%\venvUtils
set unitTestsPath=%here%\tests\unit
set testOutput=%here%\testOutput\unit
md %testOutput%

call "%scriptsDir%\venvCmd.bat" py -m xmlrunner discover -b -s "%unitTestsPath%" -t "%here%" --output-file "%testOutput%\unitTests.xml" %*
