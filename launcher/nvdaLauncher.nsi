!include "fileFunc.nsh"
!include "mui2.nsh"

!define launcher_appExe "nvdaLauncher.exe"

SetCompressor /SOLID LZMA
SilentInstall silent
RequestExecutionLevel user
CRCCheck on

ReserveFile "${NSISDIR}\Plugins\system.dll"
ReserveFile "${NSISDIR}\Plugins\banner.dll"
ReserveFile "..\miscDeps\launcher\nvda_logo.wav"

Name "NVDA"
VIProductVersion "${VERSION_YEAR}.${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_BUILD}" ;Needs to be here so other version info shows up
VIAddVersionKey "ProductName" "NVDA"
VIAddVersionKey "LegalCopyright" "${COPYRIGHT}"
VIAddVersionKey "FileDescription" "NVDA launcher file"
VIAddVersionKey "ProductVersion" "${VERSION}"

OutFile "${LAUNCHEREXE}"

Function .onInit
; Get the locale language ID from kernel32.dll and dynamically change language of the installer
System::Call 'kernel32::GetUserDefaultUILanguage() i .r0'
;Force zh-HK to zh-TW as zh-HK uses wrong encoding on Vista/7 #1596 
StrCmp $0 "3076" 0 +2
StrCpy $0 "1028"
StrCpy $LANGUAGE $0
FunctionEnd

page instfiles

;Include modern user interface language files
!insertmacro MUI_LANGUAGE "English" ; default language
!insertmacro MUI_LANGUAGE "French"
!insertmacro MUI_LANGUAGE "German"
!insertmacro MUI_LANGUAGE "Spanish"
!insertmacro MUI_LANGUAGE "SpanishInternational"
!insertmacro MUI_LANGUAGE "SimpChinese"
!insertmacro MUI_LANGUAGE "TradChinese"
!insertmacro MUI_LANGUAGE "Japanese"
!insertmacro MUI_LANGUAGE "Italian"
;!insertmacro MUI_LANGUAGE "Swedish"
!insertmacro MUI_LANGUAGE "Finnish"
!insertmacro MUI_LANGUAGE "Russian"
!insertmacro MUI_LANGUAGE "Portuguese"
!insertmacro MUI_LANGUAGE "PortugueseBR"
!insertmacro MUI_LANGUAGE "Polish"
!insertmacro MUI_LANGUAGE "Czech"
!insertmacro MUI_LANGUAGE "Slovak"
!insertmacro MUI_LANGUAGE "Croatian"
!insertmacro MUI_LANGUAGE "Hungarian"
!insertmacro MUI_LANGUAGE "Galician"
!insertmacro MUI_LANGUAGE "Dutch"
!insertmacro MUI_LANGUAGE "Arabic"
!insertmacro MUI_LANGUAGE "Danish"
!insertmacro MUI_LANGUAGE "Icelandic"
!insertmacro MUI_LANGUAGE "Serbian"
!insertmacro MUI_LANGUAGE "Turkish"
!insertmacro MUI_LANGUAGE "Albanian"
!insertmacro MUI_LANGUAGE "Bulgarian"
!insertmacro MUI_LANGUAGE "Norwegian"
  !insertmacro MUI_LANGUAGE "NorwegianNynorsk"

section "install"
SetAutoClose true
initPluginsDir
Banner::show /nounload
BringToFront

setOutPath "$PLUGINSDIR"
;Play NVDA logo sound
File "..\miscDeps\launcher\nvda_logo.wav"
Push "$PLUGINSDIR\nvda_logo.wav"
Call PlaySound
CreateDirectory "$PLUGINSDIR\app"
setOutPath "$PLUGINSDIR\app"
file /R "${NVDADistDir}\"
${GetParameters} $0
Banner::destroy
exec:
execWait "$PLUGINSDIR\app\nvda_noUIAccess.exe $0 -r --launcher" $1
;If exit code is 3 then execute again (restart)
intcmp $1 3 exec +1
SectionEnd


Function PlaySound
; Retrieve the file to play
pop $9
; The code below is derived from the code example at http://nsis.sourceforge.net/WinAPI:winmm:PlaySound
IntOp $0 "SND_ASYNC" || 1
System::Call 'winmm::PlaySound(t r9, i 0, i r0) b'
FunctionEnd
