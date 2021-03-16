@echo off
rem this script ensures the NVDA build system Python virtual environment is created and up to date,
rem and then activates it.
rem This is an internal script and should not be used directly.

rem Ensure the environment is created and up to date
py -3.8-32 "%~dp0\ensureVenv.py"
if ERRORLEVEL 1 goto :EOF
rem unset the PYTHONHOME variable so as to not pick up possible global site-packages
set PYTHONHOME=
rem set the VIRTUAL_ENV variable instructing Python to use a virtual environment
set VIRTUAL_ENV=%~dp0..\.venv
rem Add the virtual environment's scripts directory to the path
set PATH=%VIRTUAL_ENV%\scripts;%PATH%
rem Set an NVDA-specific variable to identify this official NVDA virtual environment from other 3rd party ones
set NVDA_VENV=%VIRTUAL_ENV%
rem mention the environment in the prompt to make it obbvious it is active
rem just in case this script is executed outside of a local block and not cleaned up.
set PROMPT=[NVDA Venv] %PROMPT%
