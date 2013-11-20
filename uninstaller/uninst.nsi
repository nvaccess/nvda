!include "MUI2.nsh"
!include "..\miscDeps\uninstaller\uac.nsh"

!define appName "NVDA"

!define INSTDIR_REG_ROOT "HKLM"
!define INSTDIR_REG_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${appName}"

SetCompressor /SOLID LZMA
CRCCheck On
XPStyle on
InstProgressFlags Smooth
RequestExecutionLevel user

!addplugindir "..\miscDeps\uninstaller"
ReserveFile "..\miscDeps\uninstaller\UAC.dll"

Name "${appName}"
VIProductVersion "0.0.0.0" ;Needs to be here so other version info shows up
VIAddVersionKey "ProductName" "${appName}"
VIAddVersionKey "LegalCopyright" "${COPYRIGHT}"
VIAddVersionKey "FileDescription" "${appName} installer"
VIAddVersionKey "ProductVersion" "${VERSION}"

;Minimal installer to generate uninstaller
OutFile "${INSTEXE}";

Section "install"
SetAutoClose true
WriteUninstaller "${UNINSTEXE}"
SectionEnd

;Actual uninstaller stuff

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!InsertMacro MUI_UNPAGE_FINISH

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

Function un.onInit
; Get the locale language ID from kernel32.dll and dynamically change language of the installer
System::Call 'kernel32::GetUserDefaultUILanguage() i .r0'
;Force zh-HK to zh-TW as zh-HK uses wrong encoding on Vista/7 #1596 
StrCmp $0 "3076" 0 +2
StrCpy $0 "1028"
StrCpy $LANGUAGE $0
doElevate:
!insertmacro UAC_RunElevated
;If couldn't change user then fail
strcmp 0 $0 +1 elevationFail
;If we are the outer user process, then silently quit
strcmp 1 $1 +1 +2
quit
;If bad login then try again
strcmp 3 $1 doElevate +1
;If admin then success
strcmp 2 $1 elevationSuccess +1
elevationFail:
MessageBox mb_iconstop "Unable to elevate, error $0"
quit
elevationSuccess:
;Odd the uninstaller does not do this?
ReadRegStr $INSTDIR ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "InstallDir"
FunctionEnd

Section "Uninstall"
SetAutoClose true
execWait "$INSTDIR\nvda_slave.exe unregisterInstall"
Rmdir /REBOOTOK /r "$INSTDIR"
SectionEnd
