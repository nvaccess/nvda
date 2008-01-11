#virtualBuffers/IAccessible.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import globalVars
import winUser
import NVDAObjects
import NVDAObjects.window
import NVDAObjects.IAccessible
import NVDAObjects.IAccessible.IA2
import controlTypes
import NVDAObjects.window

runningTable=[]

def getVirtualBuffer(obj):
	for v in runningTable:
		if v.isNVDAObjectInVirtualBuffer(obj):
				return v

def update(obj):
	for index in range(len(runningTable)):
		try:
			if not runningTable[index].isAlive():
				del runningTable[index]
		except:
			globalVars.log.warning("Error trying to remove old virtualBuffer at index %s"%index,exc_info=True)
	#Gecko with IAccessible2 support
	windowClassName=obj.windowClassName
	role=obj.role
	states=obj.states
	if isinstance(obj,NVDAObjects.IAccessible.IA2.IA2) and windowClassName=='MozillaContentWindowClass' and role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_READONLY in states and controlTypes.STATE_BUSY not in states:
 		classString="gecko.Gecko"
	#Gecko only with IAccessible support
	elif isinstance(obj,NVDAObjects.IAccessible.IAccessible) and windowClassName.startswith('Mozilla') and role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_READONLY in states and controlTypes.STATE_BUSY in states:
		classString="gecko.Gecko"
	#Adobe documents with IAccessible
 	elif isinstance(obj,NVDAObjects.IAccessible.IAccessible) and windowClassName=="AVL_AVView" and role in (controlTypes.ROLE_DOCUMENT,controlTypes.ROLE_PAGE) and controlTypes.STATE_READONLY in states:
		classString="adobe.Adobe"
	#MSHTML
 	elif isinstance(obj,NVDAObjects.IAccessible.IAccessible) and windowClassName=="Internet Explorer_Server" and controlTypes.STATE_FOCUSED in states: 
		info=winUser.getGUIThreadInfo(winUser.getWindowThreadProcessID(obj.windowHandle)[1])
		if not info.flags&winUser.GUI_CARETBLINKING or info.hwndCaret!=obj.windowHandle:
			classString="MSHTML.MSHTML"
		else:
			return
	else:
		return
	modString,classString=os.path.splitext(classString)
	classString=classString[1:]
	globalVars.log.debug("loading module %s, class %s"%(modString,classString))
	mod=__import__("virtualBuffers.%s"%modString,globals(),locals(),[""])
	globalVars.log.debug("mod contains %s"%dir(mod))
	newClass=getattr(mod,classString)
	globalVars.log.debug("virtualBuffers.IAccessible.update: adding %s at %s (%s)"%(newClass,obj.windowHandle,obj.windowClassName))
	virtualBufferObject=newClass(obj)
	runningTable.append(virtualBufferObject)
	return virtualBufferObject
