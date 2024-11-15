@echo off
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
set scriptsDir=%here%

setlocal
if "%VIRTUAL_ENV%" == "" (
	call "%scriptsDir%\ensureAndActivate.bat"
	if ERRORLEVEL 1 goto :EOF
)
py -m pip freeze >%1
endlocal
