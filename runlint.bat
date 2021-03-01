@echo off
call "%~dp0\venvUtils\venvCmd.bat" py "%~dp0\tests\lint\genDiff.py" %1 "%~dp0\_lint.diff"
  if ERRORLEVEL 1 exit /b %ERRORLEVEL%
  type "%~dp0\_lint.diff" | call "%~dp0\venvUtils\venvCmd.bat" py -Xutf8 -m flake8 --diff --tee --config="%~dp0\tests\lint\flake8.ini"
  
