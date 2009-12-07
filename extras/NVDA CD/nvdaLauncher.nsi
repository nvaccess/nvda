!include "fileFunc.nsh"

!define SPI_GETSCREENREADER 70

!define launcher_appDir "nvda_2009.1_portable"
!define launcher_appExe "nvdaLauncher.exe"

setcompress off
SilentInstall silent
RequestExecutionLevel user

Outfile ${launcher_appExe}

page instfiles

function .oninit
${GetParameters} $0
${GetOptions} $0 "checkScreenReaderFlag" $1
ifErrors end +1
strcpy $0 "0"
System::Call 'user32.dll::SystemParametersInfoW(i ${SPI_GETSCREENREADER}, i 0, *i .r0, i 0)'
intcmp $0 1 +1 +2
abort
end:
FunctionEnd

section "install"
SetAutoClose true
initPluginsDir
CreateDirectory "$PLUGINSDIR\app"
setOutPath "$PLUGINSDIR\app"
file /R "${launcher_appDir}\"
${GetParameters} $0
execWait "$PLUGINSDIR\app\${launcher_appExe} $0"
SectionEnd
