#globalVars.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
"""global variables module
@var foregroundObject: holds the current foreground object
@type foregroundObject: L{NVDAObjects.baseType.NVDAObject}
  @var focusObject: holds the current focus object
@type focusObject: L{NVDAObjects.baseType.NVDAObject}
@var mouseObject: holds the object that is at the position of the mouse pointer
@type mouseObject: L{NVDAObjects.baseType.NVDAObject}
@var mouseOldX: the last x coordinate of the mouse pointer before its current position
@type oldMouseX: int
@var mouseOldY: the last y coordinate of the mouse pointer before its current position
@type oldMouseY: int
  @var navigatorObject: holds the current navigator object
@type navigatorObject: L{NVDAObjects.baseType.NVDAObject}
@var navigatorTracksFocus: if true, the navigator object will follow the focus as it changes
@type navigatorTracksFocus: boolean
@var menuMode: menu mode switch
@type menuMode: boolean
@var keyboardHelp: if true, when pressing a key, the name of the script (if any) bound to that key will be reported, rather than the actual script being executed.
@type keyboardHelp: boolean
@var virtualBufferPassThrough: If true, scripts in the current virtualBuffer will be ignored and key presses will go through to the focus object.
@type virtualBufferPassThrough: boolean
@var stayAlive: the core main loop keeps running while this is true.
@type stayAlive: boolean
@var keyCounter: gets incrimented each time a key is pressed.
@type keycounter: boolean
@var lastProgresssValue: Stores the last value from a progress bar
@type lastProgressValue: int
"""
 
desktopObject=None
foregroundObject=None
focusObject=None
mouseObject=None
mouseOldX=None
mouseOldY=None
navigatorObject=None
navigatorTracksFocus=True
menuMode=False
keyboardHelp=False
virtualBufferPassThrough=False
stayAlive=None
keyCounter=0
lastProgressValue=0
