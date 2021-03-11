@echo off
setlocal
if "%VIRTUAL_ENV%" == "" (
	call "%~dp0\ensureAndActivate.bat"
	if ERRORLEVEL 1 goto :EOF
)
py -m pip freeze >%1
endlocal
