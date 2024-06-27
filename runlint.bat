@echo off
rem runlint <base commit> [<output file>]
rem Lints any changes after base commit up to and including current HEAD, plus any uncommitted changes.
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
set scriptsDir=%here%\venvUtils
set lintFilesPath=%here%\tests\lint

call "%scriptsDir%\venvCmd.bat" py "%lintFilesPath%\genDiff.py" %1 "%lintFilesPath%\_lint.diff"
  if ERRORLEVEL 1 exit /b %ERRORLEVEL%
  set flake8Args=--diff --config="%lintFilesPath%\flake8.ini"
  if "%2" NEQ "" set flake8Args=%flake8Args%  --tee --output-file=%2
  type "%lintFilesPath%\_lint.diff" | call "%scriptsDir%\venvCmd.bat" py -Xutf8 -m flake8 %flake8Args%
  
