@echo off
rem runlicensecheck [<output file>]
rem Runs a license check for python dependencies
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%

set checkArgs=
if "%1" NEQ "" set checkArgs=--file=%1 --format=markdown
call uv run --group license-check --directory "%here%" -m licensecheck -0 --format ansi %checkArgs%
if ERRORLEVEL 1 exit /b %ERRORLEVEL%
