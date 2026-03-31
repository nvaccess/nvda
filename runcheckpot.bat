@echo off
rem runcheckpot [scons args]
rem Checks that all translatable strings have translator comments.
rem First generates the pot file using scons, then validates it.
rem Any arguments are forwarded to the scons pot command.
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%

call scons pot %*
if ERRORLEVEL 1 exit /b %ERRORLEVEL%
call uv run --directory "%here%" python tests/checkPot.py "%here%\output\nvda.pot"
if ERRORLEVEL 1 exit /b %ERRORLEVEL%
