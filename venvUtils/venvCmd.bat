@echo off
rem this script executes the single given command and arguments inside the NVDA build system's Python virtual environment.
rem It activates the environment, creating / updating it first if necessary,
rem then executes the command,
rem and then finally deactivates the environment.

setlocal
call "%~dp0\ensureAndActivate.bat"
call %*
call "%~dp0\..\.venv\scripts\deactivate.bat"
endlocal
