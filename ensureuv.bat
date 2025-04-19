@echo off
rem Check if 'uv' is available
where uv >nul 2>&1 && goto :runUv

rem Check if WinGet is available
(where winget >nul 2>&1 && set hasWinGet=1) || set hasWinGet=0

:prompt
echo uv is not installed.
echo.
echo Choose how to install uv:
if "%hasWinGet%"=="1" (
	echo [1] Install using WinGet, recommended
) else (
	echo WinGet is NOT available.
)
echo [2] Install using the official uv install script
echo [0] Exit

set /p "choice=Enter your choice: "

if "%choice%"=="0" (
	goto :eof
) else if "%choice%"=="1" (
	if "%hasWinGet%"=="1" (
		echo Installing uv using WinGet...
		winget install --accept-source-agreements --disable-interactivity -e astral-sh.uv
		goto :runUv
	) else (
		echo Invalid option: WinGet is not available.
		goto :prompt
	)
) else if "%choice%"=="2" (
	echo Installing uv using the official script...
	powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
	goto :runUv
) else (
	echo Invalid choice: "%choice%". Exiting.
	exit /B 1
)

:runUv
if "%choice%"=="2" (
	set "UV_BIN=%UserProfile%\.local\bin"
	set "Path=%UV_BIN%;%Path%"
)
uv %*
