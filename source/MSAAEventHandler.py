#MSAAEventHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import win32gui
import Queue
import ctypes
import comtypes
import debug
import audio
from constants import *

queue_events=Queue.Queue(100)
objectEventHandles=[]

eventMap={
EVENT_SYSTEM_FOREGROUND:"foreground",
EVENT_SYSTEM_MENUSTART:"menuStart",
EVENT_SYSTEM_MENUEND:"menuEnd",
EVENT_SYSTEM_MENUPOPUPSTART:"menuStart",
EVENT_SYSTEM_MENUPOPUPEND:"menuEnd",
EVENT_SYSTEM_SWITCHSTART:"switchStart",
EVENT_SYSTEM_SWITCHEND:"switchEnd",
EVENT_OBJECT_FOCUS:"focusObject",
EVENT_OBJECT_SHOW:"showObject",
EVENT_OBJECT_DESCRIPTIONCHANGE:"objectDescriptionChange",
EVENT_OBJECT_HELPCHANGE:"objectHelpChange",
EVENT_OBJECT_LOCATIONCHANGE:"objectLocationChange",
EVENT_OBJECT_NAMECHANGE:"objectNameChange",
EVENT_OBJECT_REORDER:"objectReorder",
EVENT_OBJECT_SELECTION:"objectSelection",
EVENT_OBJECT_SELECTIONADD:"objectSelectionAdd",
EVENT_OBJECT_SELECTIONREMOVE:"objectSelectionRemove",
EVENT_OBJECT_SELECTIONWITHIN:"objectSelectionWithIn",
EVENT_OBJECT_STATECHANGE:"objectStateChange",
EVENT_OBJECT_VALUECHANGE:"objectValueChange"
}

#Internal function for object events

def objectEventCallback(handle,eventID,window,objectID,childID,threadID,timestamp):
	debug.writeMessage("MSAAEventHandler.objectEventCallback:  handle %s, event %s (%s), window %s, object ID %s, child ID %s, thread ID %s, timestamp %s"%(handle,eventID,eventMap[eventID],window,objectID,childID,threadID,timestamp))
	try:
		#Lets test to see if there is really an object here before dealing with it
		if ctypes.windll.oleacc.AccessibleObjectFromWindow(window,objectID,ctypes.byref(comtypes.GUID(iid_IAccessible)),ctypes.byref(ctypes.c_void_p()))!=0:
			return
		if (objectID==0) and (childID==0):
			objectID=-4
		if (eventID==EVENT_OBJECT_LOCATIONCHANGE) and (objectID==OBJID_CARET):
			while queue_events.full():
				time.sleep(0.001)
			queue_events.put(("caret",window,objectID,childID))
		elif win32gui.IsWindow(window) and (objectID not in [OBJID_CURSOR,OBJID_CARET]):
			eventName=eventMap.get(eventID,None)
			while queue_events.full():
				time.sleep(0.001)
			queue_events.put((eventName,window,objectID,childID))
	except:
		audio.speakMessage("Error in MSAA event callback")
		debug.writeException("MSAAEventHandler.internal_objectEvent")

#Register internal object event with MSAA

def initialize():
	cObjectEventCallback=ctypes.CFUNCTYPE(ctypes.c_voidp,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)(objectEventCallback)
	debug.writeMessage("MSAAEventHandler.initialize: created c callback function %s"%cObjectEventCallback)
	for eventType in eventMap.keys():
		handle=ctypes.windll.user32.SetWinEventHook(eventType,eventType,0,cObjectEventCallback,0,0,0)
		if handle:
			objectEventHandles.append(handle)
			debug.writeMessage("MSAAEventHandler.Initialize: registered 0x%x (%s) as handle %s"%(eventType,eventMap[eventType],handle))
		else:
			debug.writeError("MSAAEventHandler.initialize: could not register callback for event %s (%s)"%(eventType,eventMap[eventType]))

def terminate():
	for handle in objectEventHandles:
		ctypes.windll.user32.UnhookWinEvent(handle)
