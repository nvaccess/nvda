@echo off
rem this script executes the single given command and arguments inside the NVDA build system's Python virtual environment.
rem It activates the environment, creating / updating it first if necessary,
rem then executes the command,
rem and then finally deactivates the environment.

rem This script also supports running in an already fully activated NVDA Python environment.
rem If this is detected, the command is executed directly instead.
if "%VIRTUAL_ENV%" NEQ "" (
	if "%NVDA_VENV%" NEQ "%VIRTUAL_ENV%" (
		echo Warning: Detected a custom Python virtual environment. 
		echo It is recommended to run all NVDA build system commands outside of any existing Python virtual environment, unless you really know what you are doing.
	)
	echo directly calling %*
	call %*
	goto :EOF
)

rem call setlocal to make sure that any environment variable changes made by activating the virtual environment
rem can be completely undone when endlocal is called or this script exits.
setlocal
echo Ensuring NVDA Python virtual environment
call "%~dp0\ensureAndActivate.bat"
if ERRORLEVEL 1 goto :EOF
echo call %*
call %*
rem the virtual environment will now be deactivated as endlocal will be reached.
echo Deactivating NVDA Python virtual environment
endlocal
