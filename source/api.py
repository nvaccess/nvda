"""General functions for NVDA"""
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
	"""
Instructs the GUI that you want to quit. The GUI responds by bringing up a dialog asking you if you want to exit.
"""
	gui.exit()

def showGui():
	"""Instructs the GUI to become visible and move in to focus."""
	gui.showGui()

def getFocusObject():
	"""
Gets the current object with focus.
@returns: the object with focus
@rtype: L{NVDAObjects.baseType.NVDAObject}
"""
	return globalVars.focusObject

def getForegroundObject():
	"""Gets the current foreground object.
@returns: the current foreground object
@rtype: L{NVDAObjects.baseType.NVDAObject}
"""
	return globalVars.foregroundObject

def setForegroundObject(obj):
	"""Stores the given object as the current foreground object. (Note: it does not physically change the operating system foreground window, but only allows NVDA to keep track of what it is).
@param obj: the object that will be stored as the current foreground object
@type obj: NVDAObjects.baseType.NVDAObject
"""
	if not isinstance(obj,NVDAObjects.baseType.NVDAObject):
		return False
	globalVars.foregroundObject=obj
	debug.writeMessage("setForegroundObject: %s %s %s %s"%(obj.name,obj.typeString,obj.value,obj.description))
	return True

def setFocusObject(obj):
	"""Stores an object as the current focus object. (Note: this does not physically change the window with focus in the operating system, but allows NVDA to keep track of the correct object).
Before overriding the last object, this function calls event_looseFocus on the object to notify it that it is loosing focus. 
@param obj: the object that will be stored as the focus object
@type obj: NVDAObjects.baseType.NVDAObject
"""
	if not isinstance(obj,NVDAObjects.baseType.NVDAObject):
		return False
	if globalVars.focusObject and hasattr(globalVars.focusObject,"event_looseFocus"):
		try:
			globalVars.focusObject.event_looseFocus()
		except:
			debug.writeException("event_looseFocus in focusObject")
	globalVars.focusObject=obj
	debug.writeMessage("setFocusObject: %s %s %s %s"%(obj.name,obj.typeString,obj.value,obj.description))
	return True

def getNavigatorObject():
	"""Gets the current navigator object. Navigator objects can be used to navigate around the operating system (with the number pad) with out moving the focus. 
@returns: the current navigator object
@rtype: L{NVDAObjects.baseType.NVDAObject}
"""
	return globalVars.navigatorObject

def setNavigatorObject(obj):
	"""Sets an object to be the current navigator object. Navigator objects can be used to navigate around the operating system (with the number pad) with out moving the focus.  
@param obj: the object that will be set as the current navigator object
@type obj: NVDAObjects.baseType.NVDAObject  
"""
	if not isinstance(obj,NVDAObjects.baseType.NVDAObject):
		return False
	globalVars.navigatorObject=obj

def isTypingProtected():
	"""Checks to see if key echo should be suppressed because the focus is currently on an object that has its protected state set.
@returns: True if it should be suppressed, False otherwise.
@rtype: boolean
"""
	if getFocusObject().states&STATE_SYSTEM_PROTECTED:
		return True
	else:
		return False

def keyHasScript(keyPress):
	"""Checks to see if a given keyPress has a script associated with it.
The order of checking is keyboardHelp (if keyboard help is on), appModule, virtualBuffer (if virtualBufferPassThrough mode is not on), focus object.
@param keyPress: The key that will be checked
@type keyPress: key
@returns: True if there is a script, False otherwise.
@rtype: boolean
"""
	#The keyboard help script is built in to hasScript and executeScript
	if globalVars.keyboardHelp:
		return True
	if keyPress==key("insert+1"):
		return True
	if appModuleHandler.getActiveModule().getScript(keyPress):
		return True
	virtualBuffer=virtualBuffers.getVirtualBuffer(getFocusObject())
	if not globalVars.virtualBufferPassThrough and virtualBuffer and virtualBuffer.getScript(keyPress):
		return True
	if isinstance(getFocusObject(),NVDAObjects.baseType.NVDAObject) and getFocusObject().getScript(keyPress):
		return True
	return False

def executeScript(keyPress):
	"""executes the script that is associated with a given key. 
The order of checking is keyboardHelp (if keyboard help is on), appModule, virtualBuffer (if virtualBufferPassThrough mode is not on), focus object.
@param keyPress: The key that will be checked
@type keyPress: key
"""
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
	if appModuleHandler.getActiveModule().getScript(keyPress):
		script=appModuleHandler.getActiveModule().getScript(keyPress)
	elif not globalVars.virtualBufferPassThrough and virtualBuffer and virtualBuffer.getScript(keyPress):
		script=virtualBuffer.getScript(keyPress)
	elif isinstance(getFocusObject(),NVDAObjects.baseType.NVDAObject) and getFocusObject().getScript(keyPress):
		script=getFocusObject().getScript(keyPress)
	else:
		script=None
	if globalVars.keyboardHelp:
		if script:
			name=script.__name__[6:]
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

def getAppName(processID):
	"""Finds out the application name of the given process ID.
Currently this function will return a "default_app" string in Windows 2000 or on operating systems with out a psapi.dll.
@param processID: a (processID,threadID) tuple
@type processID: tuple
"""
	try:
		procHandle=winKernel.openProcess(PROCESS_ALL_ACCESS,False,processID[0])
		buf=ctypes.create_unicode_buffer(1024)
		res=ctypes.windll.psapi.GetProcessImageFileNameW(procHandle,buf,1024)
		winKernel.closeHandle(procHandle)
		return os.path.splitext(buf.value.split('\\')[-1])[0].lower()
	except:
		return "default_app"

def setMenuMode(switch):
	"""Turns on or off menu mode according to the given parameter. Menu mode is used for some objects to work out whether or not menu items should be spoken at a certain time.
@param switch: True for on, False for off.
@type switch: boolean
"""
	globalVars.menuMode=switch

def getMenuMode():
	"""Gets the current state of the menu mode. Menu mode is used for some objects to work out whether or not menu items should be spoken at a certain time.
@returns: True for on, False for off.
@rtype: boolean
"""
	return globalVars.menuMode

def createStateList(stateBits):
	"""Creates a list of state integers, given one integer that contains state values bitwised together.
This is useful if you have some states you wish to use in something like a for loop. 
@param stateBits: a bitwised integer of state values
@type stateBits: int
@returns: the list of separate states
@rtype: list
"""
	stateList=[]
	for bitPos in range(32):
		bitVal=1<<bitPos
		if stateBits&bitVal:
			stateList+=[bitVal]
	return stateList

def toggleVirtualBufferPassThrough():
	"""Toggles virtualBufferPassThroughMode on or off. This mode is so that virtualBuffers can either capture, or ignore, key presses.
This function also speaks the state of the mode as it changes.
"""
	if globalVars.virtualBufferPassThrough:
		audio.speakMessage(_("virtual buffer pass through")+" "+_("off"))
		globalVars.virtualBufferPassThrough=False
	else:
		audio.speakMessage(_("virtual buffer pass through")+" "+_("on"))
		globalVars.virtualBufferPassThrough=True

def isVirtualBufferPassThrough():
	"""Gets the current state of the virtualBuffer pass through mode. This mode is so that virtualBuffers can either capture, or ignore, key presses.
@returns: true if on or false if off.
@rtype: boolean
 """
	return globalVars.virtualBufferPassThrough
