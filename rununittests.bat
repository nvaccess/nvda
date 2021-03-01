@echo off
call "%~dp0\venvUtils\venvCmd.bat" py -m unittest discover tests.unit -t . %*
