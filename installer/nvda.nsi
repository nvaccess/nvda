;Installer for NVDA, a free and open source screen reader for Windows
; This script requires NSIS 2.0 and above
; http://nsis.sf.net
;
; Written by Victor Tsaran, vtsaran@yahoo.com
;--------------------------------

!define VERSION "SVN-trunk"
Name "NVDA (Non-visual Desktop Access), v${VERSION}"
!define PRODUCT "NVDA"	; Don't change this for no reason, other instructions depend on this constant
!define WEBSITE "www.nvda-project.org"
!define READMEFILE "documentation\readme.txt"
!define NVDAWindowClass "wxWindowClassNR"
!define NVDAWindowTitle "NVDA"
!define NVDAApp "nvda.exe"
!define NVDATempDir "_nvda_temp_"
!define NVDASourceDir "..\source\dist"
!define SND_NAME_Welcome "NVDA_Welcome.wav"
!define SND_NAME_PleaseWait "NVDA_PleaseWait.wav"

;Include Modern UI Macro's
!include "MUI.nsh"
!include "WinMessages.nsh"
SetCompressor /SOLID LZMA
CRCCheck On
ShowInstDetails hide
ShowUninstDetails hide
SetOverwrite On
SetDateSave on
XPStyle on
InstProgressFlags Smooth

!define MUI_WELCOMEPAGE_TITLE "Welcome to the installation of ${PRODUCT}, a free and open source screen reader for Windows"
!define MUI_WELCOMEPAGE_TEXT "Copyright 2006 - 2007 by Michael Curran\n\
This wizard will guide you through the installation of ${PRODUCT}\n\
It is recommended that you close all other applications before starting Setup. This will allow Setup to update certain \
system files without rebooting your computer.$\n"

!define MUI_FINISHPAGE_TEXT_LARGE
!define MUI_FINISHPAGE_SHOWREADME $INSTDIR\${READMEFILE}
!define MUI_FINISHPAGE_SHOWREADME_TEXT "View README file (recommended)"
!define MUI_FINISHPAGE_LINK "Visit the official NVDA web site"
!define MUI_FINISHPAGE_LINK_LOCATION ${WEBSITE}
!define MUI_FINISHPAGE_NOREBOOTSUPPORT

!define MUI_UNINSTALLER
!define MUI_CUSTOMPAGECOMMANDS

;--------------------------------
;Pages
!InsertMacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\copying.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!InsertMacro MUI_UNPAGE_FINISH
 
 !define MUI_HEADERBITMAP "${NVDASourceDir}\images\icon.png"
 !define MUI_ABORTWARNING

 
;--------------------------------
 ;Language
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
;!insertmacro MUI_LANGUAGE "Swedish"
;!insertmacro MUI_LANGUAGE "Norwegian"
;!insertmacro MUI_LANGUAGE "NorwegianNynorsk"
!insertmacro MUI_LANGUAGE "Finnish"
;!insertmacro MUI_LANGUAGE "Greek"
;!insertmacro MUI_LANGUAGE "Russian"
!insertmacro MUI_LANGUAGE "Portuguese"
!insertmacro MUI_LANGUAGE "PortugueseBR"
;!insertmacro MUI_LANGUAGE "Polish"
;!insertmacro MUI_LANGUAGE "Ukrainian"
;!insertmacro MUI_LANGUAGE "Czech"
!insertmacro MUI_LANGUAGE "Slovak"
;!insertmacro MUI_LANGUAGE "Croatian"
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
;!insertmacro MUI_LANGUAGE "Galician"
;--------------------------------

;----------------------------
; Language strings
!include "langstrings.txt"

;--------------------------------
;Configuration
OutFile "${PRODUCT}_${VERSION}.exe"

;Folder selection page
 InstallDir "$PROGRAMFILES\${PRODUCT}"

;Remember install folder
InstallDirRegKey HKLM "Software\${PRODUCT}" ""

;--------------------------------
;Reserve Files
!insertmacro MUI_RESERVEFILE_LANGDLL
;ReserveFile "${INIFILE}"
ReserveFile "${NSISDIR}\Plugins\system.dll"
ReserveFile "waves\${SND_NAME_Welcome}"
ReserveFile "waves\${SND_NAME_PleaseWait}"
;!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

; user vars
var InstallWithSpeech
var hmci

Function .onInit
!insertmacro MUI_LANGDLL_DISPLAY
call isNVDARunning
pop $1	; TRUE or FALSE
pop $2	; if true, will contain the handle of NVDA window
IntCmp $1 1 +1 SpeechInstall
MessageBox MB_OK $(msg_NVDARunning)
; Shut down NVDA
System::Call "user32.dll::PostMessage(i $2, i ${WM_QUIT}, i 0, i 0)"
;IntCmp $3 0 SpeechInstall 0 +1
;MessageBox MB_OK "Could not shut down NVDA process"

SpeechInstall:
InitPluginsDir
SetOutPath $PLUGINSDIR
File "waves\${SND_NAME_Welcome}"
push "$PLUGINSDIR\${SND_NAME_Welcome}"
Call PlaySound

MessageBox MB_OKCANCEL $(msg_SpeechInstall) IDOK +1 IDCANCEL end
SendMessage $hmci ${WM_CLOSE} 0 0
Strcpy $InstallWithSpeech 1

; Tell users to "please wait..."
File "waves\${SND_NAME_PleaseWait}"
push "$PLUGINSDIR\${SND_NAME_PleaseWait}"
Call PlaySound

CreateDirectory $PLUGINSDIR\_nvda_temp_
SetOutPath $PLUGINSDIR\_nvda_temp_
File /r "${NVDASourceDir}\"
exec "$PLUGINSDIR\${NVDATempDir}\${NVDAApp} -m true"

	end:
	SendMessage $hmci ${WM_CLOSE} 0 0
FunctionEnd
 
Section "install" section_install
SetShellVarContext all
SetOutPath "$INSTDIR"

File /r "${NVDASourceDir}\"


SectionEnd

Section Shortcuts
SetShellVarContext all
SetOutPath "$INSTDIR\"

;!insertmacro MUI_STARTMENU_WRITE_BEGIN application
CreateDirectory "$SMPROGRAMS\${PRODUCT}"
CreateShortCut "$SMPROGRAMS\${PRODUCT}\${PRODUCT}.lnk" "$INSTDIR\${PRODUCT}.exe" "" "$INSTDIR\${PRODUCT}.exe" 0 SW_SHOWNORMAL
CreateShortCut "$SMPROGRAMS\${PRODUCT}\Readme.lnk" "$INSTDIR\${READMEFILE}" "" "$INSTDIR\${READMEFILE}" 0 SW_SHOWMAXIMIZED
CreateShortCut "$SMPROGRAMS\${PRODUCT}\User Guide.lnk" "$INSTDIR\documentation\user guide.txt" "" "$INSTDIR\documentation\Users Guide.txt" 0 SW_SHOWMAXIMIZED
WriteIniStr "$INSTDIR\${PRODUCT}.url" "InternetShortcut" "URL" "${WEBSITE}"
CreateShortCut "$SMPROGRAMS\${PRODUCT}\WebSite.lnk" "$INSTDIR\${PRODUCT}.url" "" "$INSTDIR\${PRODUCT}.url" 0
CreateShortCut "$SMPROGRAMS\${PRODUCT}\NVDA Info WIKI.lnk" "http://wiki.nvda-project.org" "" "http://wiki.nvda-project.org" 0
CreateShortCut "$DESKTOP\${PRODUCT}.lnk" "$INSTDIR\${PRODUCT}.exe" "" "$INSTDIR\${PRODUCT}.exe" 0 SW_SHOWNORMAL \
 CONTROL|ALT|N "Shortcut Ctrl+Alt+N"
;!insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section Uninstaller
 SetShellVarContext all
CreateShortCut "$SMPROGRAMS\NVDA\Uninstall.lnk" "$INSTDIR\uninst.exe" "" "$INSTDIR\uninst.exe" 0
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\NVDA" "DisplayName" "${PRODUCT} ${VERSION}"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\NVDA" "DisplayVersion" "${VERSION}"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\NVDA" "URLInfoAbout" "http://www.nvda-project.org/"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\NVDA" "Publisher" "Michael Curran"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\NVDA" "UninstallString" "$INSTDIR\Uninst.exe"
WriteRegStr HKCU "Software\${PRODUCT}" "" $INSTDIR
WriteUninstaller "$INSTDIR\Uninst.exe"
 SectionEnd

var PreserveConfig
Function un.onInit 
!insertmacro MUI_UNGETLANGUAGE
MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 $(msg_RemoveNVDA)  IDYES +2
Abort
InitPluginsDir
FunctionEnd

Section "Uninstall" 
SetShellVarContext all

; Warn about configuration file
IfFileExists "$INSTDIR\nvda.ini" +1 +2
MessageBox MB_ICONQUESTION|MB_YESNO|MB_DefButton2 $(msg_NVDAConfigFound) IDYES +1 IDNO PreserveConfiguration
StrCpy $PreserveConfig 0
goto Continue

PreserveConfiguration:
StrCpy $PreserveConfig 1

Continue:
Delete "$SMPROGRAMS\${PRODUCT}\*.*"
RmDir "$SMPROGRAMS\${PRODUCT}"
Delete $DESKTOP\${PRODUCT}.lnk"
DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\${PRODUCT}"
DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT}"
 SectionEnd

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

Function un.isNVDARunning
FindWindow $0 "${NVDAWindowClass}" "${NVDAWindowTitle}"
;MessageBox MB_OK "Window handle is $0"
StrCmp $0 "0" +1 +3
push 0
goto end
push $0	; push the handle of NVDA window onto the stack
push 1	; push TRUE onto the stack

end:
FunctionEnd

Function RestartNVDA
call isNVDARunning
pop $0
IntCmp $0 0 end +1
pop $0	; pop window handle from the stack
;MessageBox MB_OK "handle is $0"
ExecWait "$PLUGINSDIR\${NVDATempDir}\${NVDAApp} --quit" $1
Exec "$INSTDIR\${NVDAApp}"

end:
FunctionEnd

Function .onGUIEnd
Call RestartNVDA
FunctionEnd

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

Function un.onUninstSuccess
HideWindow
MessageBox MB_ICONINFORMATION|MB_OK $(msg_NVDASuccessfullyRemoved)
FunctionEnd

Function un.onGUIEnd
call un.isNVDARunning
pop $1
pop $2
IntCmp $1 1 +1 end
System::Call "user32.dll::PostMessage(i $2, i ${WM_QUIT}, i 0, i 0)"

end:
sleep 1000
StrCmp $PreserveConfig 0 +1 PreserveConfiguration
;Delete Files 
Delete /RebootOK "$INSTDIR\*.*"
RMDir /RebootOK /r "$INSTDIR\appModules"
RMDir /RebootOK /r "$INSTDIR\comInterfaces"
RMDir /RebootOK /r "$INSTDIR\documentation"
RMDir /RebootOK /r "$INSTDIR\images"
RMDir /RebootOK /r "$INSTDIR\lib"
RMDir /RebootOK /r "$INSTDIR\locale"
RMDir /RebootOK /r "$INSTDIR\synthDrivers"
RMDir /RebootOK /r "$INSTDIR\waves"
;Remove the installation directory
RMDir /RebootOK "$INSTDIR"
goto done

PreserveConfiguration:
CopyFiles /SILENT "$INSTDIR\nvda.ini" "$PLUGINSDIR"
Delete /RebootOK "$INSTDIR\*.*"
RMDir /RebootOK /r "$INSTDIR\appModules"
RMDir /RebootOK /r "$INSTDIR\comInterfaces"
RMDir /RebootOK /r "$INSTDIR\documentation"
RMDir /RebootOK /r "$INSTDIR\images"
RMDir /RebootOK /r "$INSTDIR\lib"
RMDir /RebootOK /r "$INSTDIR\locale"
RMDir /RebootOK /r "$INSTDIR\synthDrivers"
RMDir /RebootOK /r "$INSTDIR\waves"
CopyFiles /SILENT "$PLUGINSDIR\nvda.ini" "$INSTDIR"

done:
FunctionEnd
