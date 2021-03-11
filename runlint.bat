@echo off
rem runlint <base commit> [<output file>]
rem Lints any changes after base commit up to and including current HEAD, plus any uncommitted changes.
call "%~dp0\venvUtils\venvCmd.bat" py "%~dp0\tests\lint\genDiff.py" %1 "%~dp0\tests\lint\_lint.diff"
  if ERRORLEVEL 1 exit /b %ERRORLEVEL%
  set flake8Args=--diff --config="%~dp0\tests\lint\flake8.ini"
  if "%2" NEQ "" set flake8Args=%flake8Args%  --tee --output-file=%2
  type "%~dp0\tests\lint\_lint.diff" | call "%~dp0\venvUtils\venvCmd.bat" py -Xutf8 -m flake8 %flake8Args%
  
