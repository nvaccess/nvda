@echo off
rem Executes SScons within the NVDA build system's Python virtual environment.
"%~dp0\venvUtils\venvCmd.bat" py -m SCons %*
