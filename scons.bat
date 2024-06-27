@echo off
rem Executes SScons within the NVDA build system's Python virtual environment.
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
set scriptsDir=%here%\venvUtils
call "%scriptsDir%\venvCmd.bat" py -m SCons %*
