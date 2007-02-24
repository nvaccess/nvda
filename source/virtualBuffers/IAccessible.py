#virtualBuffers/IAccessible.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import debug
import winUser
import NVDAObjects
import IAccessibleHandler
import MSHTML
import gecko

runningTable={}

def getVirtualBuffer(obj):
	if len(runningTable)==0:
		return None
	if isinstance(obj,NVDAObjects.IAccessible.NVDAObject_IAccessible):
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
	if isinstance(obj,NVDAObjects.IAccessible.NVDAObject_IAccessible):
		windowHandle=obj.windowHandle
	elif isinstance(obj,int):
		windowHandle=obj
	else:
		return
	if any((winUser.isDescendantWindow(w,windowHandle) for w in runningTable)):
		return
	curWindow=windowHandle
	virtualBufferClass=None
	while curWindow:
		className=winUser.getClassName(curWindow)
		possibles=[x for x in _staticMap if x[0]==className]
		if len(possibles)>0:
			obj=NVDAObjects.IAccessible.getNVDAObjectFromEvent(curWindow,IAccessibleHandler.OBJID_CLIENT,0)
			if not obj:
				return
			role=obj.role
			k=(className,obj.role)
			if _staticMap.has_key(k):
				virtualBufferClass=_staticMap[k]
		if virtualBufferClass:
			debug.writeMessage("virtualBuffers.IAccessible.update: adding %s at %s (%s)"%(virtualBufferClass,obj.windowHandle,className))
			virtualBufferObject=virtualBufferClass(obj)
			windows=frozenset([curWindow,obj.windowHandle])
			for w in windows:
				runningTable[w]=virtualBufferObject
			return
		curWindow=None #winUser.getAncestor(curWindow,winUser.GA_PARENT)

_staticMap={
("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):MSHTML.virtualBuffer_MSHTML,
("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_CLIENT):MSHTML.virtualBuffer_MSHTML,
("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_PANE):MSHTML.virtualBuffer_MSHTML,
("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):gecko.virtualBuffer_gecko,
}
