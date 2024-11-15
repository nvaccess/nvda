@echo off
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
set scriptsDir=%here%\venvUtils
set sourceDirPath=%here%\source

call "%scriptsDir%\venvCmd.bat" start pyw "%sourceDirPath%\nvda.pyw" %*
