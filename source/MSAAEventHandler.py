#MSAAEventHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import Queue
import pyAA
import debug
import audio

lastProcessID=None
queue_events=Queue.Queue(10000)
objectEventHandles=[]

eventMap={
pyAA.Constants.EVENT_SYSTEM_FOREGROUND:"foreground",
pyAA.Constants.EVENT_SYSTEM_MENUSTART:"menuStart",
pyAA.Constants.EVENT_SYSTEM_MENUEND:"menuEnd",
pyAA.Constants.EVENT_SYSTEM_MENUPOPUPSTART:"menuStart",
pyAA.Constants.EVENT_SYSTEM_MENUPOPUPEND:"menuEnd",
pyAA.Constants.EVENT_SYSTEM_SWITCHSTART:"switchStart",
pyAA.Constants.EVENT_SYSTEM_SWITCHEND:"switchEnd",
pyAA.Constants.EVENT_OBJECT_FOCUS:"focusObject",
pyAA.Constants.EVENT_OBJECT_SHOW:"showObject",
pyAA.Constants.EVENT_OBJECT_DESCRIPTIONCHANGE:"objectDescriptionChange",
pyAA.Constants.EVENT_OBJECT_HELPCHANGE:"objectHelpChange",
pyAA.Constants.EVENT_OBJECT_LOCATIONCHANGE:"objectLocationChange",
pyAA.Constants.EVENT_OBJECT_NAMECHANGE:"objectNameChange",
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
			try:
				accObject=pyAA.AccessibleObjectFromEvent(window,objectID,childID)
			except:
				return None
		else:
			accObject=event.AccessibleObject
		if not accObject:
			return None
		try:
			objectProcessID=accObject.ProcessID
		except:
			objectProcessID=None
		if (event.EventID==pyAA.Constants.EVENT_SYSTEM_FOREGROUND) and (objectProcessID!=lastProcessID):
			queue_events.put(("appChange",window,objectID,childID))
			lastProcessID=objectProcessID
		elif (event.EventID==pyAA.Constants.EVENT_OBJECT_LOCATIONCHANGE) and (event.ObjectID==pyAA.Constants.OBJID_CARET):
			queue_events.put(("caret",window,objectID,childID))
		else:
			eventName=eventMap.get(event.EventID,None)
			queue_events.put((eventName,window,objectID,childID))
		return False
	except:
		debug.writeException("MSAAEventHandler.internal_objectEvent")

#Register internal object event with MSAA

def initialize():
	global objectEventHandle
	for eventType in eventMap.keys():
		objectEventHandles.append(pyAA.AddWinEventHook(callback=internal_objectEvent,event=eventType,obj_id=pyAA.Constants.OBJID_WINDOW))
		objectEventHandles.append(pyAA.AddWinEventHook(callback=internal_objectEvent,event=eventType,obj_id=pyAA.Constants.OBJID_CLIENT))
		objectEventHandles.append(pyAA.AddWinEventHook(callback=internal_objectEvent,event=eventType,obj_id=pyAA.Constants.OBJID_TITLEBAR))
		objectEventHandles.append(pyAA.AddWinEventHook(callback=internal_objectEvent,event=eventType,obj_id=pyAA.Constants.OBJID_SYSMENU))
		objectEventHandles.append(pyAA.AddWinEventHook(callback=internal_objectEvent,event=eventType,obj_id=pyAA.Constants.OBJID_MENU))
	objectEventHandles.append(pyAA.AddWinEventHook(callback=internal_objectEvent,event=pyAA.Constants.EVENT_OBJECT_LOCATIONCHANGE,obj_id=pyAA.Constants.OBJID_CARET))

def terminate():
	for handle in objectEventHandles:
		pyAA.DeleteWinEventHook(handle)
