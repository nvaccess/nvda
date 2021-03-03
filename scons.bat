@echo off
rem Executes SScons within the NVDA build system's Python virtual environment.
call "%~dp0\venvUtils\venvCmd.bat" py -m SCons %*
