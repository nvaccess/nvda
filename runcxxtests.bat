@echo off
rem Builds and runs the C++ unit tests for nvdaHelper components
rem (currently nvdaHelper\winEventLimiter).
rem Requires Visual Studio with the Desktop development with C++ workload,
rem including the C++ Unit Test framework.
rem Extra arguments are passed to vstest.console.exe, e.g.
rem runcxxtests.bat /TestCaseFilter:"FullyQualifiedName~alwaysAllowed"
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
set testOutput=%here%\testOutput\cxx
md "%testOutput%" >nul 2>&1

set vswhere=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe
if not exist "%vswhere%" (
	echo ERROR: vswhere.exe not found. Install Visual Studio with the C++ workload.
	exit /b 1
)
for /f "usebackq tokens=*" %%i in (`"%vswhere%" -latest -products * -requires Microsoft.Component.MSBuild -find MSBuild\**\Bin\MSBuild.exe`) do set msbuild=%%i
if not defined msbuild (
	echo ERROR: MSBuild not found. Install Visual Studio with the C++ workload.
	exit /b 1
)

rem The project files pin the toolchain NVDA currently uses.
rem Set CXXTEST_PLATFORMTOOLSET to override it,
rem e.g. set CXXTEST_PLATFORMTOOLSET=v143 for Visual Studio 2022.
set toolsetArg=
if defined CXXTEST_PLATFORMTOOLSET set toolsetArg=/p:PlatformToolset=%CXXTEST_PLATFORMTOOLSET%

"%msbuild%" "%here%\nvdaHelper\winEventLimiter\winEventLimiter.sln" /m /v:minimal /t:winEventLimiterTests /p:Configuration=Release /p:Platform=x64 %toolsetArg%
if %errorlevel% neq 0 exit /b %errorlevel%

for /f "usebackq tokens=*" %%i in (`"%vswhere%" -latest -products * -find Common7\IDE\Extensions\TestPlatform\vstest.console.exe`) do set vstest=%%i
if not defined vstest (
	echo ERROR: vstest.console.exe not found. Install Visual Studio with the C++ workload.
	exit /b 1
)
"%vstest%" "%here%\nvdaHelper\winEventLimiter\x64\Release\winEventLimiterTests.dll" "/logger:trx;LogFileName=cxxTests.trx" /ResultsDirectory:"%testOutput%" %*
exit /b %errorlevel%
