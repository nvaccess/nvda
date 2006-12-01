#api.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
import os.path
import debug
import winKernel
import winUser
import globalVars
from constants import *
import audio
from config import conf
import appModuleHandler
import gui
from keyboardHandler import key 
import NVDAObjects
import virtualBuffers

# Initialise WMI; required for getProcessName.
#_wmi = win32com.client.GetObject('winmgmts:')

#User functions

def quit():
	gui.exit()

def showGui():
	gui.showGui()
def getFocusObject():
	return globalVars.focusObject

def getForegroundObject():
	return globalVars.foregroundObject

def setForegroundObject(obj):
	if not isinstance(obj,NVDAObjects.baseType.NVDAObject):
		return False
	globalVars.foregroundObject=obj
	return True

def getFocusObject():
	return globalVars.focusObject

def setFocusObject(obj):
	if not isinstance(obj,NVDAObjects.baseType.NVDAObject):
		return False
	if globalVars.focusObject and hasattr(globalVars.focusObject,"event_looseFocus"):
		try:
			globalVars.focusObject.event_looseFocus()
		except:
			debug.writeException("event_looseFocus in focusObject")
	globalVars.focusObject=obj
	return True

def getNavigatorObject():
	return globalVars.navigatorObject

def setNavigatorObject(obj):
	if not isinstance(obj,NVDAObjects.baseType.NVDAObject):
		return False
	globalVars.navigatorObject=obj

def isTypingProtected():
	if getFocusObject().states&STATE_SYSTEM_PROTECTED:
		return True
	else:
		return False

def keyHasScript(keyPress):
	#The keyboard help script is built in to hasScript and executeScript
	if globalVars.keyboardHelp:
		return True
	if keyPress==key("insert+1"):
		return True
	if appModuleHandler.current.getScript(keyPress):
		return True
	virtualBuffer=virtualBuffers.getVirtualBuffer(getFocusObject())
	if not globalVars.virtualBufferPassThrough and virtualBuffer and virtualBuffer.getScript(keyPress):
		return True
	if isinstance(getFocusObject(),NVDAObjects.baseType.NVDAObject) and getFocusObject().getScript(keyPress):
		return True
	return False

def executeScript(keyPress):
	#The keyboard help script is built in to hasScript and executeScript
	if keyPress==key("insert+1"):
		if not globalVars.keyboardHelp:
			globalVars.keyboardHelp=True
			audio.speakMessage(_("keyboard help")+" "+_("on"))
			return True
		else:
			globalVars.keyboardHelp=False
			audio.speakMessage(_("keyboard help")+" "+_("off"))
			return True
	virtualBuffer=virtualBuffers.getVirtualBuffer(getFocusObject())
	if appModuleHandler.current.getScript(keyPress):
		script=appModuleHandler.current.getScript(keyPress)
	elif not globalVars.virtualBufferPassThrough and virtualBuffer and virtualBuffer.getScript(keyPress):
		script=virtualBuffer.getScript(keyPress)
	elif isinstance(getFocusObject(),NVDAObjects.baseType.NVDAObject) and getFocusObject().getScript(keyPress):
		script=getFocusObject().getScript(keyPress)
	else:
		script=None
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
				description=_("no description")
			audio.speakMessage("%s, from %s, %s"%(name,container,description))
		else:
			audio.speakMessage(_("no script"))
		return
	if script:
		try:
			script(keyPress)
			return True
		except:
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

def createStateList(stateBits):
	stateList=[]
	for bitPos in range(32):
		bitVal=1<<bitPos
		if stateBits&bitVal:
			stateList+=[bitVal]
	return stateList

def toggleVirtualBufferPassThrough():
		if globalVars.virtualBufferPassThrough:
			audio.speakMessage(_("virtual buffer pass through")+" "+_("off"))
			globalVars.virtualBufferPassThrough=False
		else:
			audio.speakMessage(_("virtual buffer pass through")+" "+_("on"))
			globalVars.virtualBufferPassThrough=True

def isVirtualBufferPassThrough():
		return globalVars.virtualBufferPassThrough
