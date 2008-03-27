#virtualBuffers/IAccessible.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import gc
import os
import globalVars
import winUser
import NVDAObjects
import NVDAObjects.window
import NVDAObjects.IAccessible
import NVDAObjects.IAccessible.IA2
import controlTypes
import NVDAObjects.window
import speech

runningTable=set()

def getVirtualBuffer(obj):
	for v in runningTable:
		if v.isNVDAObjectInVirtualBuffer(obj):
			return v

def update(obj):
	for v in list(runningTable):
		if not v.isAlive():
			killVirtualBuffer(v)
	windowClassName=obj.windowClassName
	role=obj.role
	states=obj.states
	#Gecko with IAccessible2 support
	if isinstance(obj,NVDAObjects.IAccessible.IA2.IA2) and windowClassName.startswith('Mozilla') and role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_READONLY in states:
		classString="virtualBuffers.gecko_ia2.Gecko_ia2"
	#Gecko only with IAccessible support
	elif isinstance(obj,NVDAObjects.IAccessible.IAccessible) and windowClassName.startswith('Mozilla') and role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_READONLY in states:
		classString="virtualBuffers_old.gecko.Gecko"
	#Adobe documents with IAccessible
 	elif isinstance(obj,NVDAObjects.IAccessible.IAccessible) and windowClassName=="AVL_AVView" and role in (controlTypes.ROLE_DOCUMENT,controlTypes.ROLE_PAGE) and controlTypes.STATE_READONLY in states:
		classString="virtualBuffers_old.adobe.Adobe"
	#MSHTML
 	elif isinstance(obj,NVDAObjects.IAccessible.IAccessible) and windowClassName=="Internet Explorer_Server" and controlTypes.STATE_FOCUSED in states: 
		info=winUser.getGUIThreadInfo(winUser.getWindowThreadProcessID(obj.windowHandle)[1])
		if not info.flags&winUser.GUI_CARETBLINKING or info.hwndCaret!=obj.windowHandle:
			classString="virtualBuffers_old.MSHTML.MSHTML"
		else:
			return
	else:
		return
	modString,classString=os.path.splitext(classString)
	classString=classString[1:]
	globalVars.log.debug("loading module %s, class %s"%(modString,classString))
	mod=__import__(modString,globals(),locals(),[""])
	globalVars.log.debug("mod contains %s"%dir(mod))
	newClass=getattr(mod,classString)
	globalVars.log.debug("virtualBuffers.IAccessible.update: adding %s at %s (%s)"%(newClass,obj.windowHandle,obj.windowClassName))
	virtualBufferObject=newClass(obj)
	runningTable.add(virtualBufferObject)
	if hasattr(virtualBufferObject,'unloadBuffer'):
		virtualBufferObject.loadBuffer()
	return virtualBufferObject

def killVirtualBuffer(virtualBufferObject):
	try:
		runningTable.remove(virtualBufferObject)
	except KeyError:
		return
	if hasattr(virtualBufferObject,'unloadBuffer'):
		virtualBufferObject.unloadBuffer()

def reportPassThrough(virtualBuffer):
	"""Speaks the state of virtualBufferPassThroughMode if it has changed.
	@param virtualBuffer: The current virtual buffer.
	@type virtualBuffer: L{virtualBuffers.VirtualBuffer}
	"""
	if virtualBuffer.passThrough != reportPassThrough.last:
		speech.speakMessage(_("virtual buffer pass through") + " " + (_("on") if virtualBuffer.passThrough else _("off")))
		reportPassThrough.last = virtualBuffer.passThrough
reportPassThrough.last = False
