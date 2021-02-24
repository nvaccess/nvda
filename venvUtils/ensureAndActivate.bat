@echo off
rem this script ensures the NVDA build system Python virtual environment is created and up to date,
rem and then activates it.
rem this script should be used only in the case where many commands will be executed within the environment and the shell will be eventually thrown away. 
rem E.g. an Appveyor build.
py -3.8-32 "%~dp0\ensureVenv.py"
if ERRORLEVEL 1 exit /b %ERRORLEVEL%
call "%~dp0\..\.venv\scripts\activate.bat"
set NVDA_VENV=%VIRTUAL_ENV%