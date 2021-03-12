@echo off
call "%~dp0\venvUtils\venvCmd.bat" py -m nose -sv --traverse-namespace -w "%~dp0\tests\unit" %*
