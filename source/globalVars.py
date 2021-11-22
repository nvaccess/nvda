#globalVars.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
"""global variables module
@var foregroundObject: holds the current foreground object. The object for the last foreground event received.
@type foregroundObject: L{NVDAObjects.NVDAObject}
  @var focusObject: holds the current focus object
@type focusObject: L{NVDAObjects.NVDAObject}
@var mouseObject: holds the object that is at the position of the mouse pointer
@type mouseObject: L{NVDAObjects.NVDAObject}
@var mouseOldX: the last x coordinate of the mouse pointer before its current position
@type oldMouseX: int
@var mouseOldY: the last y coordinate of the mouse pointer before its current position
@type oldMouseY: int
  @var navigatorObject: holds the current navigator object
@type navigatorObject: L{NVDAObjects.NVDAObject}
"""

import argparse
import os
import typing


class DefautAppArgs(argparse.Namespace):
	quit: bool = False
	check_running: bool = False
	logFileName: typing.Optional[os.PathLike] = ""
	logLevel: int = 0
	configPath: typing.Optional[os.PathLike] = None
	language: str = "en"
	minimal: bool = False
	secure: bool = False
	disableAddons: bool = False
	debugLogging: bool = False
	noLogging: bool = False
	changeScreenReaderFlag: bool = True
	install: bool = False
	installSilent: bool = False
	createPortable: bool = False
	createPortableSilent: bool = False
	portablePath: typing.Optional[os.PathLike] = None
	launcher: bool = False
	enableStartOnLogon: typing.Optional[bool] = None
	copyPortableConfig: bool = False
	easeOfAccess: bool = False


startTime=0
desktopObject=None
foregroundObject=None
focusObject=None
focusAncestors=[]
focusDifferenceLevel=None
mouseObject=None
mouseOldX=None
mouseOldY=None
navigatorObject=None
reviewPosition=None
reviewPositionObj=None
lastProgressValue=0
appArgs = DefautAppArgs()
appArgsExtra=None
settingsRing = None
speechDictionaryProcessing=True
exitCode=0
