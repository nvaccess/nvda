#virtualBuffers/IAccessible.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import debug
import winUser
import NVDAObjects
import IAccessibleHandler

runningTable={}

def getVirtualBuffer(obj):
	if len(runningTable)==0:
		return None
	if isinstance(obj,NVDAObjects.IAccessible.IAccessible):
		windowHandle=obj.windowHandle
	elif isinstance(obj,int):
		windowHandle=obj
	else:
		return
	for existingHwnd in runningTable:
		if winUser.isDescendantWindow(existingHwnd,windowHandle):
			return runningTable[existingHwnd]
	return None

def update(obj):
	for w in filter(lambda x: not winUser.isWindow(x),runningTable):
		debug.writeMessage("virtualBuffers.IAccessible.removeVirtualBuffer: removed %s at %s"%(runningTable[w],w))
		del runningTable[w]
	#debug.writeMessage("virtualBuffers.IAccessible.update: trying to update with %s (%s)"%(hwnd,winUser.getClassName(hwnd)))
	if isinstance(obj,NVDAObjects.IAccessible.IAccessible):
		windowHandle=obj.windowHandle
	elif isinstance(obj,int):
		windowHandle=obj
	else:
		return
	if any((winUser.isDescendantWindow(w,windowHandle) for w in runningTable)):
		return
	classString=None
	for curWindow in [windowHandle,winUser.getAncestor(windowHandle,winUser.GA_PARENT)]:
		if not curWindow:
			return 
		className=winUser.getClassName(curWindow)
		possibles=[x for x in _staticMap if x[0]==className]
		if len(possibles)>0:
			obj=NVDAObjects.IAccessible.getNVDAObjectFromEvent(curWindow,IAccessibleHandler.OBJID_CLIENT,0)
			if not obj or not obj.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_READONLY:
				return
			role=obj.IAccessibleRole
			k=(className,obj.IAccessibleRole)
			if _staticMap.has_key(k):
				classString=_staticMap[k]
		if classString:
			modString,classString=os.path.splitext(classString)
			classString=classString[1:]
			mod=__import__(modString,globals(),locals(),[])
			newClass=getattr(mod,classString)
			debug.writeMessage("virtualBuffers.IAccessible.update: adding %s at %s (%s)"%(newClass,obj.windowHandle,className))
			virtualBufferObject=newClass(obj)
			windows=frozenset([curWindow,obj.windowHandle])
			for w in windows:
				runningTable[w]=virtualBufferObject
			return

_staticMap={
	("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):"MSHTML.MSHTML",
	("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"MSHTML.MSHTML",
	("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_PANE):"MSHTML.MSHTML",
	("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):"gecko.Gecko",
}
