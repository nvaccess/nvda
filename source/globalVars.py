#globalVars.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
"""global variables module
@var foregroundObject: holds the current foreground object
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
@var navigatorTracksFocus: if true, the navigator object will follow the focus as it changes
@type navigatorTracksFocus: boolean
"""
 
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
appArgs=None
appArgsExtra=None
settingsRing = None
speechDictionaryProcessing=True
exitCode=0
