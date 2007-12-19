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
		if not runningTable[index].isAlive():
			del runningTable[index]
	#Gecko with IAccessible2 support
	if isinstance(obj,NVDAObjects.IAccessible.IA2.IA2) and obj.windowClassName=='MozillaContentWindowClass' and obj.role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_READONLY in obj.states:
 		classString="gecko.Gecko"
	#Gecko only with IAccessible support
	elif isinstance(obj,NVDAObjects.IAccessible.IAccessible) and obj.windowClassName.startswith('Mozilla') and obj.role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_READONLY in obj.states:
		classString="gecko.Gecko"
	#Adobe documents with IAccessible
 	elif isinstance(obj,NVDAObjects.IAccessible.IAccessible) and obj.windowClassName=="AVL_AVView" and obj.role==controlTypes.ROLE_DOCUMENT and controlTypes.STATE_READONLY in obj.states:
		classString="adobe.Adobe"
	#MSHTML
 	elif isinstance(obj,NVDAObjects.IAccessible.IAccessible) and obj.windowClassName=="Internet Explorer_Server" and controlTypes.STATE_FOCUSED in obj.states: 
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
