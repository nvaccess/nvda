!include "fileFunc.nsh"

!define launcher_appExe "nvdaLauncher.exe"

SetCompressor /SOLID LZMA
SilentInstall silent
RequestExecutionLevel user

ReserveFile "${NSISDIR}\Plugins\system.dll"
ReserveFile "${NSISDIR}\Plugins\banner.dll"
ReserveFile "..\installer\waves\nvda_logo.wav"

Name "NVDA"
VIProductVersion "0.0.0.0" ;Needs to be here so other version info shows up
VIAddVersionKey "ProductName" "NVDA"
VIAddVersionKey "LegalCopyright" "Copyright 2006 - 2011 NVDA Contributors"
VIAddVersionKey "FileDescription" "NVDA launcher file"
VIAddVersionKey "ProductVersion" "${VERSION}"

Function .onInit
; Get the locale language ID from kernel32.dll and dynamically change language of the installer
System::Call 'kernel32::GetUserDefaultUILanguage() i .r0'
;Force zh-HK to zh-TW as zh-HK uses wrong encoding on Vista/7 #1596 
StrCmp $0 "3076" 0 +2
StrCpy $0 "1028"
StrCpy $LANGUAGE $0
FunctionEnd

page instfiles

section "install"
SetAutoClose true
initPluginsDir
CreateDirectory "$PLUGINSDIR\app"
setOutPath "$PLUGINSDIR\app"
Banner::show /nounload
BringToFront

;Play NVDA logo sound
File "..\installer\waves\nvda_logo.wav"
Push "$PLUGINSDIR\app\nvda_logo.wav"
Call PlaySound
file /R "${NVDADistDir}\"
${GetParameters} $0
Banner::destroy
exec:
execWait "$PLUGINSDIR\app\nvda_noUIAccess.exe $0 -r --launcher" $1
;If exit code is 2 then execute again (restart)
intcmp $1 2 exec +1
SectionEnd

var hmci

Function PlaySound
; Retrieve the file to play
pop $9
System::Call 'msvfw32.dll::MCIWndCreate(i 0, i 0, i 0x0070, t "$9") i .r0'
StrCpy $hmci $0
; Checks format support
SendMessage $hmci 0x0490 0 0 $0
IntCmp $0 0 nosup
; if you want mci window to be hidden
ShowWindow $hmci SW_HIDE
; you can use "STR:play" or "STR:play repeat", but I saw "repeat" problems with midi files
SendMessage $hmci 0x0465 0 "STR:play"
;SendMessage $hmci ${WM_CLOSE} 0 0

nosup:
FunctionEnd
