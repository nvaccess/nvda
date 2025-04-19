@echo off
rem Executes SScons within the NVDA build system's Python virtual environment.
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
call "%here%\ensureuv.bat" run --directory "%here%" SCons %*
