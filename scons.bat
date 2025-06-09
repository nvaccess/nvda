@echo off
rem Executes SScons within the NVDA build system's Python virtual environment.
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
powershell -ExecutionPolicy Bypass -NoProfile -File "%here%\ensureuv.ps1" run --directory "%here%" SCons %*
