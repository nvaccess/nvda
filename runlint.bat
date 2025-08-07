@echo off
rem runlint [<output dir>]
rem Lints and formats all python files
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%

set ruffCheckArgs=
set ruffFormatArgs=
if "%1" NEQ "" set ruffCheckArgs=--output-file=%1/PR-lint.xml --output-format=junit
if "%1" NEQ "" set ruffFormatArgs=--diff > %1/lint-diff.diff
call uv run --group lint --directory "%here%" ruff check --fix %ruffCheckArgs%
if ERRORLEVEL 1 exit /b %ERRORLEVEL%
call uv run --group lint --directory "%here%" ruff format %ruffFormatArgs%
if ERRORLEVEL 1 exit /b %ERRORLEVEL%
call uv run --group lint --directory "%here%" pyright --threads --level warning
if ERRORLEVEL 1 exit /b %ERRORLEVEL%
