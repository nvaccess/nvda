;Installer for NVDA, a free and open source screen reader for Windows
; This script requires NSIS 2.0 and above
; http://nsis.sf.net
;
; Written by Victor Tsaran, vtsaran@yahoo.com
;--------------------------------

!define VERSION "unknown"
Name "NVDA"
!define PRODUCT "NVDA"	; Don't change this for no reason, other instructions depend on this constant
!define WEBSITE "www.nvda-project.org"
!define READMEFILE "documentation\en\readme.txt"
!define NVDAWindowClass "wxWindowClassNR"
!define NVDAWindowTitle "NVDA"
!define NVDAApp "nvda.exe"
!define NVDATempDir "_nvda_temp_"
!define NVDASourceDir "..\source\dist"
!define NVDAConfig "nvda.ini"

!define INSTDIR_REG_ROOT "HKLM"
!define INSTDIR_REG_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT}"

SetCompressor /SOLID LZMA
;Include Modern UI Macro's
!include "MUI2.nsh"
!include "AdvUninstLog.nsh"
!include "WinMessages.nsh"
!include "Library.nsh"

CRCCheck On
ShowInstDetails hide
ShowUninstDetails hide
SetOverwrite On
SetDateSave on
XPStyle on
InstProgressFlags Smooth

!define MUI_WELCOMEPAGE_TITLE $(msg_WelcomePageTitle)
!define MUI_WELCOMEPAGE_TEXT $(msg_WelcomePageText)

!define MUI_FINISHPAGE_TEXT_LARGE
!define MUI_FINISHPAGE_SHOWREADME $INSTDIR\documentation\$(path_READMEFile)
!define MUI_FINISHPAGE_SHOWREADME_TEXT $(msg_READMEText)
!define MUI_FINISHPAGE_LINK $(msg_NVDAWebSite)
!define MUI_FINISHPAGE_LINK_LOCATION ${WEBSITE}
!define MUI_FINISHPAGE_NOREBOOTSUPPORT

!define MUI_UNINSTALLER
!define MUI_CUSTOMFUNCTION_GUIINIT NVDA_GUIInit
!define MUI_CUSTOMFUNCTION_UnGUIInit un.NVDA_GUIInit
!define MUI_CUSTOMPAGECOMMANDS

  ;Start Menu Folder Page Configuration
Var StartMenuFolder
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKLM" 
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\${PRODUCT}"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"

; Interactive or unattended uninstallation, i.e. ask to replace/delete/modify files
!insertmacro UNATTENDED_UNINSTALL

;--------------------------------
;Pages
!InsertMacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\copying.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!InsertMacro MUI_UNPAGE_FINISH

 !define MUI_HEADERBITMAP "${NVDASourceDir}\images\icon.png"
 !define MUI_ABORTWARNING



;--------------------------------
 ;Language
!define UNINSTALLOG_LOCALIZE ; necessary for localization of messages from the uninstallation log file

;Remember the installer language
!define MUI_LANGDLL_REGISTRY_ROOT "HKCU"
!define MUI_LANGDLL_REGISTRY_KEY "Software\${PRODUCT}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "Installer Language"

!insertmacro MUI_LANGUAGE "English" ; default language
!insertmacro MUI_LANGUAGE "French"
!insertmacro MUI_LANGUAGE "German"
!insertmacro MUI_LANGUAGE "Spanish"
!insertmacro MUI_LANGUAGE "SimpChinese"
!insertmacro MUI_LANGUAGE "TradChinese"
;!insertmacro MUI_LANGUAGE "Japanese"
;!insertmacro MUI_LANGUAGE "Korean"
!insertmacro MUI_LANGUAGE "Italian"
;!insertmacro MUI_LANGUAGE "Dutch"
;!insertmacro MUI_LANGUAGE "Danish"
!insertmacro MUI_LANGUAGE "Swedish"
;!insertmacro MUI_LANGUAGE "Norwegian"
;!insertmacro MUI_LANGUAGE "NorwegianNynorsk"
!insertmacro MUI_LANGUAGE "Finnish"
;!insertmacro MUI_LANGUAGE "Greek"
!insertmacro MUI_LANGUAGE "Russian"
!insertmacro MUI_LANGUAGE "Portuguese"
!insertmacro MUI_LANGUAGE "PortugueseBR"
!insertmacro MUI_LANGUAGE "Polish"
;!insertmacro MUI_LANGUAGE "Ukrainian"
!insertmacro MUI_LANGUAGE "Czech"
!insertmacro MUI_LANGUAGE "Slovak"
!insertmacro MUI_LANGUAGE "Croatian"
;!insertmacro MUI_LANGUAGE "Bulgarian"
!insertmacro MUI_LANGUAGE "Hungarian"
;!insertmacro MUI_LANGUAGE "Thai"
;!insertmacro MUI_LANGUAGE "Romanian"
;!insertmacro MUI_LANGUAGE "Latvian"
;!insertmacro MUI_LANGUAGE "Macedonian"
;!insertmacro MUI_LANGUAGE "Estonian"
;!insertmacro MUI_LANGUAGE "Turkish"
;!insertmacro MUI_LANGUAGE "Lithuanian"
;!insertmacro MUI_LANGUAGE "Catalan"
;!insertmacro MUI_LANGUAGE "Slovenian"
;!insertmacro MUI_LANGUAGE "Serbian"
;!insertmacro MUI_LANGUAGE "SerbianLatin"
;!insertmacro MUI_LANGUAGE "Arabic"
;!insertmacro MUI_LANGUAGE "Farsi"
;!insertmacro MUI_LANGUAGE "Hebrew"
;!insertmacro MUI_LANGUAGE "Indonesian"
;!insertmacro MUI_LANGUAGE "Mongolian"
;!insertmacro MUI_LANGUAGE "Luxembourgish"
;!insertmacro MUI_LANGUAGE "Albanian"
;!insertmacro MUI_LANGUAGE "Breton"
;!insertmacro MUI_LANGUAGE "Belarusian"
;!insertmacro MUI_LANGUAGE "Icelandic"
;!insertmacro MUI_LANGUAGE "Malay"
;!insertmacro MUI_LANGUAGE "Bosnian"
;!insertmacro MUI_LANGUAGE "Kurdish"
;!insertmacro MUI_LANGUAGE "Irish"
;!insertmacro MUI_LANGUAGE "Uzbek"
!insertmacro MUI_LANGUAGE "Galician"
;--------------------------------

;----------------------------
; Language strings
!include "locale\cs\langstrings.txt"
!include "locale\de\langstrings.txt"
!include "locale\en\langstrings.txt"
!include "locale\es\langstrings.txt"
!include "locale\fi\langstrings.txt"
!include "locale\fr\langstrings.txt"
!include "locale\gl\langstrings.txt"
!include "locale\hu\langstrings.txt"
!include "locale\hr\langstrings.txt"
!include "locale\it\langstrings.txt"
!include "locale\pl\langstrings.txt"
!include "locale\pt_pt\langstrings.txt"
!include "locale\pt_br\langstrings.txt"
!include "locale\ru\langstrings.txt"
!include "locale\se\langstrings.txt"
!include "locale\sk\langstrings.txt"
;!include "locale\th\langstrings.txt"
!include "locale\zh\langstrings.txt"
!include "locale\zh_tw\langstrings.txt"

;--------------------------------
;Configuration
OutFile "${PRODUCT}_${VERSION}.exe"

;Folder selection page
 InstallDir "$PROGRAMFILES\${PRODUCT}"

;Remember install folder
InstallDirRegKey ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "InstallDir"

;--------------------------------
;Reserve Files
!insertmacro MUI_RESERVEFILE_LANGDLL
ReserveFile "${NSISDIR}\Plugins\system.dll"
ReserveFile "${NSISDIR}\Plugins\banner.dll"

Var oldNVDAWindowHandle
 Var NVDAInstalled ;"1" if NVDA has been installed

Function .onInit
; Fix an error from previous installers where the "nvda" file would be left behind after uninstall
IfFileExists "$PROGRAMFILES\NVDA" 0
Delete "$PROGRAMFILES\NVDA"
; Get the locale language ID from kernel32.dll and dynamically change language of the installer
System::Call 'kernel32::GetThreadLocale() i .r0'
StrCpy $LANGUAGE $0

;prepare log always within .onInit function
!insertmacro UNINSTALL.LOG_PREPARE_INSTALL
FunctionEnd

Function NVDA_GUIInit
Banner::show /nounload
BringToFront
InitPluginsDir
CreateDirectory $PLUGINSDIR\${NVDATempDir}
SetOutPath $PLUGINSDIR\${NVDATempDir}
File /r "${NVDASourceDir}\"
;If NVDA is already running, kill it first before starting a new copy
call isNVDARunning
pop $1	; TRUE or FALSE
pop $oldNVDAWindowHandle
; Shut down NVDA
IntCmp $1 1 +1 Continue
MessageBox MB_OK $(msg_NVDARunning)
Continue:
Exec "$PLUGINSDIR\${NVDATempDir}\${NVDAApp} -r -m"
Banner::destroy
FunctionEnd

Section "install" section_install
SetShellVarContext all
SetOutPath "$INSTDIR"
; open and close uninstallation log after ennumerating all the files being copied
!insertmacro UNINSTALL.LOG_OPEN_INSTALL
File /r /x lib "${NVDASourceDir}\"
CreateDirectory "$INSTDIR\lib"
!insertmacro UNINSTALL.LOG_CLOSE_INSTALL

; Install libraries
!insertmacro InstallLib DLL NOTSHARED REBOOT_NOTPROTECTED "${NVDASourceDir}\lib\charHook.dll" "$INSTDIR\lib\charHook.dll" "$INSTDIR\lib"
!insertmacro InstallLib DLL NOTSHARED REBOOT_NOTPROTECTED "${NVDASourceDir}\lib\keyHook.dll" "$INSTDIR\lib\keyHook.dll" "$INSTDIR\lib"
!insertmacro InstallLib DLL NOTSHARED REBOOT_NOTPROTECTED "${NVDASourceDir}\lib\mouseHook.dll" "$INSTDIR\lib\mouseHook.dll" "$INSTDIR\lib"
!insertmacro InstallLib DLL NOTSHARED REBOOT_NOTPROTECTED "${NVDASourceDir}\lib\virtualBuffer.dll" "$INSTDIR\lib\virtualBuffer.dll" "$INSTDIR\lib"
!insertmacro InstallLib DLL NOTSHARED REBOOT_NOTPROTECTED "${NVDASourceDir}\lib\VBufBackend_gecko_ia2.dll" "$INSTDIR\lib\VBufBackend_gecko_ia2.dll" "$INSTDIR\lib"
!insertmacro InstallLib REGDLL NOTSHARED REBOOT_NOTPROTECTED "${NVDASourceDir}\lib\ia2.dll" "$INSTDIR\lib\ia2.dll" "$INSTDIR\lib"

strcpy $NVDAInstalled "1"
SectionEnd

Section Shortcuts
SetShellVarContext all
SetOutPath "$INSTDIR\"
!insertmacro MUI_STARTMENU_WRITE_BEGIN application
CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
CreateShortCut "$SMPROGRAMS\$StartMenuFolder\${PRODUCT}.lnk" "$INSTDIR\${PRODUCT}.exe" "" "$INSTDIR\${PRODUCT}.exe" 0 SW_SHOWNORMAL
CreateShortCut "$SMPROGRAMS\$StartMenuFolder\$(shortcut_readme).lnk" "$INSTDIR\documentation\$(path_readmefile)" "" "$INSTDIR\documentation\$(path_readmefile)" 0 SW_SHOWMAXIMIZED
CreateShortCut "$SMPROGRAMS\$StartMenuFolder\$(shortcut_userguide).lnk" "$INSTDIR\documentation\$(path_userguide)" "" "$INSTDIR\documentation\$(path_userguide)" 0 SW_SHOWMAXIMIZED
WriteIniStr "$INSTDIR\${PRODUCT}.url" "InternetShortcut" "URL" "${WEBSITE}"
CreateShortCut "$SMPROGRAMS\$StartMenuFolder\$(shortcut_website).lnk" "$INSTDIR\${PRODUCT}.url" "" "$INSTDIR\${PRODUCT}.url" 0
!insertmacro MUI_STARTMENU_WRITE_END
CreateShortCut "$DESKTOP\${PRODUCT}.lnk" "$INSTDIR\${PRODUCT}.exe" "" "$INSTDIR\${PRODUCT}.exe" 0 SW_SHOWNORMAL \
 CONTROL|ALT|N "Shortcut Ctrl+Alt+N"
SectionEnd

Section Uninstaller
 SetShellVarContext all
CreateShortCut "$SMPROGRAMS\${PRODUCT}\$(shortcut_uninstall).lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
WriteRegStr ${INSTDIR_REG_ROOT} ${INSTDIR_REG_KEY} "DisplayName" "${PRODUCT} ${VERSION}"
WriteRegStr ${INSTDIR_REG_ROOT} ${INSTDIR_REG_KEY} "URLInfoAbout" "http://www.nvda-project.org/"
WriteRegStr ${INSTDIR_REG_ROOT} ${INSTDIR_REG_KEY} "Publisher" "Michael Curran"
WriteRegStr ${INSTDIR_REG_ROOT} ${INSTDIR_REG_KEY} "UninstallString" "$INSTDIR\Uninstall.exe"
WriteRegStr ${INSTDIR_REG_ROOT} "Software\${PRODUCT}" "" $INSTDIR
 SectionEnd

Function .onGUIEnd
intCMP $NVDAInstalled 1 +1 NotInstalled
Exec "$INSTDIR\${NVDAApp} -r"
goto End
NotInstalled:
call isNVDARunning
pop $1
pop $2
intcmp $1 1 +1 End
intcmp $2 $oldNVDAWindowHandle End +1
System::Call "user32.dll::PostMessage(i $2, i ${WM_QUIT}, i 0, i 0)"
end:
; Clean up the temporary folder
rmdir /R /REBOOTOK $PLUGINSTDIR\${NVDATempDir}
FunctionEnd

Function .onInstSuccess
;create/update log always within .onInstSuccess function
!insertmacro UNINSTALL.LOG_UPDATE_INSTALL
FunctionEnd

; Uninstall functions
var PreserveConfig
Function un.onInit
;!insertmacro MUI_UNGETLANGUAGE
; Get the locale language ID from kernel32.dll and dynamically change language of the installer
System::Call 'kernel32::GetThreadLocale() i .r0'
StrCpy $LANGUAGE $0

; Start uninstalling with a log
!insertmacro UNINSTALL.LOG_BEGIN_UNINSTALL
FunctionEnd

Function un.NVDA_GUIInit
MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON1 $(msg_RemoveNVDA)  IDYES +2
Abort
FunctionEnd

Section "Uninstall"
SetShellVarContext all

; Uninstall libraries
!insertmacro UninstallLib DLL NOTSHARED REBOOT_NOTPROTECTED "$INSTDIR\lib\charHook.dll"
!insertmacro UninstallLib DLL NOTSHARED REBOOT_NOTPROTECTED "$INSTDIR\lib\keyHook.dll"
!insertmacro UninstallLib DLL NOTSHARED REBOOT_NOTPROTECTED "$INSTDIR\lib\mouseHook.dll"
!insertmacro UninstallLib DLL NOTSHARED REBOOT_NOTPROTECTED "$INSTDIR\lib\virtualBuffer.dll"
!insertmacro UninstallLib DLL NOTSHARED REBOOT_NOTPROTECTED "$INSTDIR\lib\VBufBackend_gecko_ia2.dll"
!insertmacro UninstallLib REGDLL NOTSHARED REBOOT_NOTPROTECTED "$INSTDIR\lib\ia2.dll"

;uninstall from path, must be repeated for every install logged path individual
!insertmacro UNINSTALL.LOG_UNINSTALL "$INSTDIR"

;uninstall from path, must be repeated for every install logged path individual
;!insertmacro UNINSTALL.LOG_UNINSTALL "$APPDATA\${PRODUCT}"

;end uninstall, after uninstall from all logged paths has been performed
!insertmacro UNINSTALL.LOG_END_UNINSTALL

; Warn about configuration file
IfFileExists "$INSTDIR\${NVDAConfig}" +1 +2
MessageBox MB_ICONQUESTION|MB_YESNO|MB_DefButton2 $(msg_NVDAConfigFound) IDYES +1 IDNO PreserveConfiguration
goto Continue
PreserveConfiguration:
CopyFiles /SILENT "$INSTDIR\${NVDAConfig}" "$PLUGINSDIR\${NVDAConfig}"
strcpy $preserveConfig "1"
Continue:
!insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
Delete "$SMPROGRAMS\$StartMenuFolder\*.*"
RmDir "$SMPROGRAMS\$StartMenuFolder"
Delete $DESKTOP\${PRODUCT}.lnk"
Delete $INSTDIR\${PRODUCT}.url"
DeleteRegKey ${INSTDIR_REG_ROOT} "SOFTWARE\${PRODUCT}"
DeleteRegKey ${INSTDIR_REG_ROOT} ${INSTDIR_REG_KEY}
StrCmp $PreserveConfig 1 +1 NoPreserveConfig
CreateDirectory $INSTDIR
CopyFiles /SILENT "$PLUGINSDIR\${NVDAConfig}" "$INSTDIR\${NVDAConfig}"
goto End
NoPreserveConfig:
Delete $INSTDIR\${NVDAConfig}
Rmdir $INSTDIR
Goto End

End:
SectionEnd

Function un.onUninstSuccess
HideWindow
MessageBox MB_ICONINFORMATION|MB_OK $(msg_NVDASuccessfullyRemoved)
FunctionEnd

Function isNVDARunning
FindWindow $0 "${NVDAWindowClass}" "${NVDAWindowTitle}"
;MessageBox MB_OK "Window handle is $0"
StrCmp $0 "0" +1 +3
push 0
goto end
push $0	; push the handle of NVDA window onto the stack
push 1	; push TRUE onto the stack
end:
FunctionEnd

/*
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
*/
