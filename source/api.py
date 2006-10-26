#api.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
import comtypes.client
import os.path
import debug
import winKernel
import globalVars
from constants import *
import dictionaries
import audio
from config import conf
import appModuleHandler
import gui
from keyboardHandler import key 
import NVDAObjects
import virtualBuffer

# Initialise WMI; required for getProcessName.
#_wmi = win32com.client.GetObject('winmgmts:')

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
	if globalVars.focusObject and hasattr(globalVars.focusObject,"event_looseFocus"):
		try:
			globalVars.focusObject.event_looseFocus()
		except:
			debug.writeException("event_looseFocus in focusObject")
			audio.speakMessage("Error in event_looseFocus of focusObject")
	v=getVirtualBuffer()
	if (not v) or (window!=v.getWindowHandle()):
		setVirtualBuffer(window)
	focusObject=NVDAObjects.getNVDAObjectByLocator(window,objectID,childID)
	if not focusObject:
		return False
	globalVars.focus_locator=(window,objectID,childID)
	globalVars.focusObject=focusObject
	if globalVars.navigatorTracksFocus:
		setNavigatorObject(focusObject)
	return True

def getVirtualBuffer():
	return globalVars.virtualBuffer

def setVirtualBuffer(window):
	globalVars.virtualBuffer=virtualBuffer.getVirtualBuffer(window)

def getNavigatorObject():
	return globalVars.navigatorObject

def setNavigatorObject(obj):
	globalVars.navigatorObject=obj
def keyHasScript(keyPress):
	#The keyboard help script is built in to hasScript and executeScript
	if globalVars.keyboardHelp:
		return True
	if keyPress==key("insert+1"):
		return True
	if appModuleHandler.current.keyMap.has_key(keyPress):
		return True
	if getFocusObject().keyMap.has_key(keyPress):
		return True
	return False

def executeScript(keyPress):
	#The keyboard help script is built in to hasScript and executeScript
	if keyPress==key("insert+1"):
		if not globalVars.keyboardHelp:
			globalVars.keyboardHelp=True
			audio.speakMessage("keyboard help on")
			return True
		else:
			globalVars.keyboardHelp=False
			audio.speakMessage("keyboard help off")
			return True
	script=appModuleHandler.current.keyMap.get(keyPress,None)
	if not script:
		script=getFocusObject().keyMap.get(keyPress,None)
	if globalVars.keyboardHelp:
		if script:
			name=script.__name__
			if script.im_self.__class__.__name__=="appModule":
				container="module %s"%script.im_self.__class__.__module__
			else:
				container=script.im_self.__class__.__name__
				container+=" in module %s"%script.im_self.__class__.__module__
			description=script.__doc__
			if not description:
				description="no description"
			audio.speakMessage("%s, from %s, %s"%(name,container,description))
		else:
			audio.speakMessage("no script")
		return
	if script:
		try:
			script(keyPress)
			return True
		except:
			audio.speakMessage("Error executing script %s bound to key %s"%(script.__name__,str(keyPress)))
			debug.writeException("Error executing script %s bound to key %s"%(script.__name__,str(keyPress)))
			return False

def eventExists(name,window,objectID,childID):
	if hasattr(appModuleHandler.current,"event_%s"%name):
		return True
	focusLocator=getFocusLocator()
	focusObject=getFocusObject()
	if ((window,objectID,childID)==focusLocator) and hasattr(focusObject,"event_%s"%name):
		return True
	thisObj=NVDAObjects.getNVDAObjectByLocator(window,objectID,childID)
	if thisObj:
		if hasattr(thisObj,"event_%s"%name):
			return True
	return False

def executeEvent(name,window,objectID,childID):
	if (name=="caret") and (window!=getFocusLocator()[0]):
		setFocusObjectByLocator(window,OBJID_CLIENT,0)
		executeEvent("gainFocus",window,objectID,childID)
	if hasattr(appModuleHandler.current,"event_%s"%name):
		event=getattr(appModuleHandler.current,"event_%s"%name)
		try:
			event(window,objectID,childID)
		except:
			audio.speakMessage("Error executing event %s from appModule"%event.__name__)
			debug.writeException("Error executing event %s from appModule"%event.__name__)
			return False
	v=getVirtualBuffer()
	if v and (v.getWindowHandle()==window) and hasattr(v,"event_%s"%name):
		event=getattr(v,"event_%s"%name)
		try:
			event(objectID,childID)
		except:
			audio.speakMessage("Error in virtualBuffer event")
			debug.writeException("virtualBuffer event")
	focusLocator=getFocusLocator()
	focusObject=getFocusObject()
	if (((window,objectID,childID)==focusLocator) or (name=="caret")) and hasattr(focusObject,"event_%s"%name): 
		event=getattr(focusObject,"event_%s"%name)
		try:
			if name=="looseFocus":
				audio.speakMessage("lost focus",wait=True)
			event()
			return True
		except:
			audio.speakMessage("Error executing event %s from focusObject"%event.__name__)
			debug.writeException("Error executing event %s from focusObject"%event.__name__)
			return False
	thisObj=NVDAObjects.getNVDAObjectByLocator(window,objectID,childID)
	if thisObj and hasattr(thisObj,"event_%s"%name):
		event=getattr(thisObj,"event_%s"%name)
		try:
			event()
			return True
		except:
			audio.speakMessage("Error executing event %s from object"%event.__name__)
			debug.writeException("Error executing event %s from object"%event.__name__)
			return False

def getObjectGroupName(accObject):
	try:
		(objectLeft,objectTop,objectRight,objectBottom)=accObject.GetLocation()
	except:
		debug.writeError("api.getObjectGrouping: fialed to get location of object %s"%accObject)
		return None
	try:
		while (accObject is not None) and (accObject.GetRole()!=ROLE_SYSTEM_GROUPING):
			accObject=getObjectPrevious(accObject)
			if accObject is None:
				debug.writeError("api.getObjectGroupName: no more previous objects")
				return None
		if accObject.GetRole()==ROLE_SYSTEM_GROUPING:
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

def makeStateList(stateText):
	stateList=stateText.split("+")
	return stateList

def getAppName(processID):
	procHandle=winKernel.openProcess(PROCESS_ALL_ACCESS,False,processID[0])
	buf=ctypes.create_unicode_buffer(1024)
	res=ctypes.windll.psapi.GetProcessImageFileNameW(procHandle,buf,1024)
	winKernel.closeHandle(procHandle)
	return os.path.splitext(buf.value.split('\\')[-1])[0].lower()


def setMenuMode(switch):
	globalVars.menuMode=switch

def getMenuMode():
	return globalVars.menuMode

