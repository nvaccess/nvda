# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2022 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from typing import Dict


EXECUTABLE_NAMES_TO_APP_MODS: Dict[str, str] = {
	# Azure Data Studio (both stable and Insiders versions) should use module for Visual Studio Code
	"azuredatastudio": "code",
	"azuredatastudio-insiders": "code",
	# Windows 11 calculator should use module for the Windows 10 one.
	"calculatorapp": "calculator",
	# The Insider version of Visual Studio Code should use the module for the stable version.
	"code - insiders": "code",
	# commsapps is an alias for the Windows 10 mail and calendar.
	"commsapps": "hxmail",
	# DBeaver is based on Eclipse and should use its appModule.
	"dbeaver": "eclipse",
	# Preview version of the Adobe Digital Editions should use the module for the stable version.
	"digitaleditionspreview": "digitaleditions",
	# Esybraille should use module for esysuite.
	"esybraille": "esysuite",
	# hxoutlook is an alias for Windows 10 mail in Creators update.
	"hxoutlook": "hxmail",
	# 64-bit versions of Miranda IM should use module for the 32-bit executable.
	"miranda64": "miranda32",
	# Various incarnations of Media Player Classic.
	"mpc-hc": "mplayerc",
	"mpc-hc64": "mplayerc",
	# The binary file for Notepad++ is named `notepad++` which makes its appModule not importable
	# (Python's import statement cannot deal with `+` in the file name).
	# Therefore the module is named `notepadPlusPlus` and mapped to the right binary below.
	"notepad++": "notepadPlusPlus",
	# searchapp is an alias for searchui in Windows 10 build 18965 and later.
	"searchapp": "searchui",
	# Windows search in Windows 11.
	"searchhost": "searchui",
	# Spring Tool Suite is based on Eclipse and should use its appModule.
	"springtoolsuite4": "eclipse",
	"sts": "eclipse",
	# Various versions of Teamtalk.
	"teamtalk3": "teamtalk4classic",
	# App module for Windows 10/11 Modern Keyboard aka new touch keyboard panel
	# should use Composable Shell modern keyboard app module
	"textinputhost": "windowsinternal_composableshell_experiences_textinput_inputapp",
	# Total Commander X64 should use the module for the 32-bit version.
	"totalcmd64": "totalcmd",
	# The calculator on Windows Server and LTSB versions of Windows 10
	# should use the module for the desktop calculator from the earlier Windows releases.
	"win32calc": "calc",
	# Windows Mail should use module for Outlook Express.
	"winmail": "msimn",
	# Zend Eclipse PHP Developer Tools is based on Eclipse and should use its appModule.
	"zend-eclipse-php": "eclipse",
	# Zend Studio is based on Eclipse and should use its appModule.
	"zendstudio": "eclipse",
}

"""Maps names of the executables to the names of the appModule which should be loaded for the given program.
Note that this map is used only for appModules included in NVDA
and appModules registered by add-ons are placed in a different one.
This mapping is needed since:
- Names of some programs are incompatible with the Python's import system (they contain a dot or a plus)
- Sometimes it is necessary to map one module to multiple executables - this map saves us from adding multiple
 appModules in such cases.
"""
