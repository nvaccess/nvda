!include "fileFunc.nsh"

!define launcher_appExe "nvdaLauncher.exe"

SetCompressor /SOLID LZMA
SilentInstall silent
RequestExecutionLevel user

Name "NVDA"
VIProductVersion "0.0.0.0" ;Needs to be here so other version info shows up
VIAddVersionKey "ProductName" "NVDA"
VIAddVersionKey "LegalCopyright" "Copyright 2006 - 2011 NVDA Contributors"
VIAddVersionKey "FileDescription" "NVDA launcher file"
VIAddVersionKey "ProductVersion" "${VERSION}"

page instfiles

section "install"
SetAutoClose true
initPluginsDir
CreateDirectory "$PLUGINSDIR\app"
setOutPath "$PLUGINSDIR\app"
file /R "${NVDADistDir}\"
${GetParameters} $0
Banner::destroy
exec:
execWait "$PLUGINSDIR\app\nvda.exe $0 --launcher" $1
;If exit code is 2 then execute again (restart)
intcmp $1 2 exec +1
SectionEnd
