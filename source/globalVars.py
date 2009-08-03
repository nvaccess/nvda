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
@var keyboardHelp: if true, when pressing a key, the name of the script (if any) bound to that key will be reported, rather than the actual script being executed.
@type keyboardHelp: boolean
@var keyCounter: gets incrimented each time a key is pressed.
@type keycounter: boolean
@var lastProgresssValue: Stores the last value from a progress bar
@type lastProgressValue: int
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
navigatorTracksFocus=True
keyboardHelp=False
keyCounter=0
lastProgressValue=0
reportDynamicContentChanges=True
caretMovesReviewCursor=True
focusMovesNavigatorObject=True
appArgs=None
settingsRing = None
speechDictionaryProcessing=True
inCaretMovement=False
configFileError=None
