# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2021 NV Access Limited, Leonard de Ruijter, pvagner
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Global variables module
"""
import typing
from typing import(
	Optional,
)

if typing.TYPE_CHECKING:
	import NVDAObjects

#: The directory that contains 'nvda.pyw'
appDir = Optional[str]

startTime=0
desktopObject=None

#: Holds the current foreground object. The object for the last foreground event received.
foregroundObject: Optional["NVDAObjects.NVDAObject"] = None

#: Holds the current focus object
focusObject: Optional["NVDAObjects.NVDAObject"] = None

focusAncestors=[]
focusDifferenceLevel=None

#: Holds the object that is at the position of the mouse pointer
mouseObject: Optional["NVDAObjects.NVDAObject"] = None

#: The last x coordinate of the mouse pointer before its current position
mouseOldX: Optional[int] = None

#: The last y coordinate of the mouse pointer before its current position
mouseOldY: Optional[int] = None

#: Holds the current navigator object
navigatorObject: Optional["NVDAObjects.NVDAObject"] = None

reviewPosition=None
reviewPositionObj=None
lastProgressValue=0
appArgs=None
appArgsExtra=None
settingsRing = None
speechDictionaryProcessing=True
exitCode=0
