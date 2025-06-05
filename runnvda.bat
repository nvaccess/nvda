@echo off
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
set sourceDirPath=%here%\source

start uvw run --gui-script --directory "%sourceDirPath%" nvda.pyw %*
