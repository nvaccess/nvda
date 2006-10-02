#api.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import pyAA
import win32gui
import win32com.client
import debug
import globalVars
from constants import *
import dictionaries
import audio
from config import conf
import appModuleHandler
import gui
import NVDAObjects
import virtualBuffer

# Initialise WMI; required for getProcessName.
_wmi = win32com.client.GetObject('winmgmts:')

#User functions

def quit():
	globalVars.stayAlive=False

def showGui():
	gui.showGui()

def getFocusObject():
	return globalVars.focusObject

def getFocusLocator():
	return globalVars.focus_locator

def setFocusObjectByLocator(window,objectID,childID):
	if (window,objectID,childID)==getFocusLocator():
		return False
	focusObject=NVDAObjects.getNVDAObjectByLocator(window,objectID,childID)
	if not focusObject:
		return False
	globalVars.focus_locator=(window,objectID,childID)
	globalVars.focusObject=focusObject
	if globalVars.navigatorTracksFocus:
		setNavigatorObject(focusObject)
	v=getVirtualBuffer()
	if not v or (v.getWindowHandle()!=globalVars.focusObject.getWindowHandle()):
		setVirtualBuffer(globalVars.focusObject.getWindowHandle())
	setVirtualBufferCursor(getVirtualBuffer().getCaretPosition())
	return True

def getVirtualBuffer():
	return globalVars.virtualBuffer

def setVirtualBuffer(window):
	v=virtualBuffer.makeVirtualBuffer(window)
	globalVars.virtualBuffer=v

def getVirtualBufferCursor():
	return globalVars.virtualBufferCursor


def setVirtualBufferCursor(index):
	globalVars.virtualBufferCursor=index


def isDecendantWindow(parent,child):
	if (parent==child) or win32gui.IsChild(parent,child):
		return True
	else:
		return False


def getNavigatorObject():
	return globalVars.navigatorObject

def setNavigatorObject(obj):
	globalVars.navigatorObject=obj
def keyHasScript(keyPress):
	if appModuleHandler.current.keyMap.has_key(keyPress):
		return True
	if getFocusObject().keyMap.has_key(keyPress):
		return True
	return False

def executeScript(keyPress):
	script=appModuleHandler.current.keyMap.get(keyPress,None)
	if not script:
		script=getFocusObject().keyMap.get(keyPress,None)
	if script:
		try:
			script(keyPress)
			return True
		except:
			audio.speakMessage("Error executing script %s bound to key %s"%(script.__name__,str(keyPress)))
			debug.writeException("Error executing script %s bound to key %s"%(script.__name__,str(keyPress)))
			return False

def eventExists(name,locator):
	if appModuleHandler.current.__dict__.has_key("event_%s"%name):
		return True
	focusLocator=getFocusLocator()
	focusObject=getFocusObject()
	if (locator==focusLocator) and hasattr(focusObject,"event_%s"%name):
		return True
	return False

def executeEvent(name,window,objectID,childID):
	if (name=="caret") and (window!=getFocusLocator()[0]):
		setFocusObjectByLocator(window,OBJID_CLIENT,0)
		executeEvent("focusObject",window,objectID,childID)
	event=appModuleHandler.current.__dict__.get("event_%s"%name,None)
	if event:
		try:
			event(window,objectID,childID)
		except:
			audio.speakMessage("Error executing event %s from appModule"%event.__name__)
			debug.writeException("Error executing event %s from appModule"%event.__name__)
			return False
	thisObj=NVDAObjects.getNVDAObjectByLocator(window,objectID,childID)
	focusLocator=getFocusLocator()
	focusObject=getFocusObject()
	if (window,objectID,childID)==focusLocator and hasattr(focusObject,"event_%s"%name): 
		event=getattr(focusObject,"event_%s"%name)
		try:
			event()
		except:
			audio.speakMessage("Error executing event %s from focusObject"%event.__name__)
			debug.writeException("Error executing event %s from focusObject"%event.__name__)
			return False
	elif thisObj and hasattr(thisObj,"event_%s"%name):
		event=getattr(thisObj,"event_%s"%name)
		try:
			event()
		except:
			audio.speakMessage("Error executing event %s from object"%event.__name__)
			debug.writeException("Error executing event %s from object"%event.__name__)
			return False
	return True

def getObjectGroupName(accObject):
	try:
		(objectLeft,objectTop,objectRight,objectBottom)=accObject.GetLocation()
	except:
		debug.writeError("api.getObjectGrouping: fialed to get location of object %s"%accObject)
		return None
	try:
		while (accObject is not None) and (accObject.GetRole()!=pyAA.Constants.ROLE_SYSTEM_GROUPING):
			accObject=getObjectPrevious(accObject)
			if accObject is None:
				debug.writeError("api.getObjectGroupName: no more previous objects")
				return None
		if accObject.GetRole()==pyAA.Constants.ROLE_SYSTEM_GROUPING:
			(groupLeft,groupTop,groupRight,groupBottom)=accObject.GetLocation()
			if (objectLeft>=groupLeft) and (objectTop>=groupTop) and (objectRight<=groupRight) and (objectBottom<=groupBottom):
				return accObject.GetName()
			else:
				debug.writeError("api.getObjectGroupName: object is not with in bounds of cloest grouping")
				return None
		debug.writeError("api.getObjectGroupName: could not find a grouping on this level")
		return None
	except:
		debug.writeError("api.getObjectGroupName: error finding group name")
		return None

def getForegroundWindow():
	return win32gui.GetForegroundWindow()

def getWindowLocation(window):
	return win32gui.GetClientRect(window)

def getWindowControlID(window):
	return win32gui.GetWindowLong(window)

def getWindowClass(window):
	return win32gui.GetClassName(window)

def makeStateList(stateText):
	stateList=stateText.split("+")
	return stateList

def getProcessName(processID):
	result  =  _wmi.ExecQuery("select * from Win32_Process where ProcessId=%d" % processID[0])
	if len(result) > 0:
		return result[0].Properties_('Name').Value
	else:
		return ""

def setMenuMode(switch):
	globalVars.menuMode=switch

def getMenuMode():
	return globalVars.menuMode
