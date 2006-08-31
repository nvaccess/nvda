#MSAAEventHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import Queue
import pyAA
import debug
from api import *

lastProcessID=None
queue_events=Queue.Queue(10000)
objectEventHandle=None

eventMap={
pyAA.Constants.EVENT_SYSTEM_FOREGROUND:"foreground",
pyAA.Constants.EVENT_MAX:"maximize",
pyAA.Constants.EVENT_MIN:"minimize",
pyAA.Constants.EVENT_SYSTEM_MENUSTART:"menuStart",
pyAA.Constants.EVENT_SYSTEM_MENUEND:"menuEnd",
pyAA.Constants.EVENT_SYSTEM_MENUPOPUPSTART:"menuStart",
pyAA.Constants.EVENT_SYSTEM_MENUPOPUPEND:"menuEnd",
pyAA.Constants.EVENT_SYSTEM_SWITCHSTART:"switchStart",
pyAA.Constants.EVENT_SYSTEM_SWITCHEND:"switchEnd",
pyAA.Constants.EVENT_OBJECT_CREATE:"createObject",
pyAA.Constants.EVENT_OBJECT_DESTROY:"destroyObject",
pyAA.Constants.EVENT_OBJECT_FOCUS:"focusObject",
pyAA.Constants.EVENT_OBJECT_HIDE:"hideObject",
pyAA.Constants.EVENT_OBJECT_SHOW:"showObject",
pyAA.Constants.EVENT_OBJECT_ACCELERATORCHANGE:"objectAcceleratorChange",
pyAA.Constants.EVENT_OBJECT_DESCRIPTIONCHANGE:"objectDescriptionChange",
pyAA.Constants.EVENT_OBJECT_DEFACTIONCHANGE:"objectDefactionChange",
pyAA.Constants.EVENT_OBJECT_HELPCHANGE:"objectHelpChange",
pyAA.Constants.EVENT_OBJECT_LOCATIONCHANGE:"objectLocationChange",
pyAA.Constants.EVENT_OBJECT_NAMECHANGE:"objectNameChange",
pyAA.Constants.EVENT_OBJECT_PARENTCHANGE:"objectParentChange",
pyAA.Constants.EVENT_OBJECT_REORDER:"objectReorder",
pyAA.Constants.EVENT_OBJECT_SELECTION:"objectSelection",
pyAA.Constants.EVENT_OBJECT_SELECTIONADD:"objectSelectionAdd",
pyAA.Constants.EVENT_OBJECT_SELECTIONREMOVE:"objectSelectionRemove",
pyAA.Constants.EVENT_OBJECT_SELECTIONWITHIN:"objectSelectionWithIn",
pyAA.Constants.EVENT_OBJECT_STATECHANGE:"objectStateChange",
pyAA.Constants.EVENT_OBJECT_VALUECHANGE:"objectValueChange"
}

#Internal function for object events

def internal_objectEvent(event):
	global lastProcessID
	try:
		if (event.AccessibleObject is None) or (event.Window==0):
			return False
		window=event.Window
		objectID=event.ObjectID
		childID=event.ChildID
		if (objectID==0) and (childID==0):
			objectID=-4
		if getMSAAObjectFromEvent(window,objectID,childID) is None:
			return None
		accObject=event.AccessibleObject
		objectProcessID=accObject.ProcessID
		if (event.EventID==pyAA.Constants.EVENT_SYSTEM_FOREGROUND) and (objectProcessID!=lastProcessID):
			queue_events.put(("appChange",window,objectID,childID))
			lastProcessID=objectProcessID
		else:
			eventName=eventMap.get(event.EventID,None)
			queue_events.put((eventName,window,objectID,childID))
		return False
	except:
		debug.writeException("MSAAEventHandler.internal_objectEvent")

#Register internal object event with MSAA

def initialize():
	global objectEventHandle
	objectEventHandle=pyAA.AddWinEventHook(callback=internal_objectEvent)

def terminate():
	global objectEventHandle
	pyAA.DeleteWinEventHook(objectEventHandle)
