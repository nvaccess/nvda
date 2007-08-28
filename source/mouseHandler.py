#mouseHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
import winUser
import queueHandler
import api
import debug
import speech
import NVDAObjects
import globalVars
import config
import IAccessibleHandler

WM_MOUSEMOVE=0x0200
WM_LBUTTONDOWN=0x0201
WM_LBUTTONUP=0x0202
WM_LBUTTONDBLCLK=0x0203
WM_RBUTTONDOWN=0x0204
WM_RBUTTONUP=0x0205
WM_RBUTTONDBLCLK=0x0206

mouseOldX=None
mouseOldY=None

#Internal mouse event

@ctypes.CFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)
def internal_mouseEvent(msg,x,y,injected):
	if not config.conf["mouse"]["reportObjectUnderMouse"]:
		return True
	try:
		if injected:
			return True
		if msg==WM_MOUSEMOVE:
			queueHandler.queueFunction(queueHandler.mouseQueue,executeMouseMoveEvent,x,y)
		elif msg in (WM_LBUTTONDOWN,WM_RBUTTONDOWN):
			queueHandler.queueFunction(queueHandler.mouseQueue,speech.cancelSpeech)
		return True
	except:
		debug.writeException("mouseHandler.internal_mouseEvent")

def executeMouseMoveEvent(x,y):
	global mouseOldX, mouseOldY
	if not config.conf["mouse"]["reportObjectUnderMouse"]:
		return
	isEntering=False
	res=IAccessibleHandler.accessibleObjectFromPoint(x,y)
	if not res:
		return
	(newPacc,newChild)=res
	newLocation=IAccessibleHandler.accLocation(newPacc,newChild)
	if not newLocation:
		return
	(newLeft,newTop,newWidth,newHeight)=newLocation
	mouseObject=api.getMouseObject()
	location=mouseObject.location
	if not location:
		return
	(left,top,width,height)=location
	if (newLeft!=left) or (newTop!=top) or (newWidth!=width) or (newHeight!=height):
		obj=NVDAObjects.IAccessible.IAccessible(IAccessibleObject=newPacc,IAccessibleChildID=newChild)
		if obj:
			mouseObject=obj
			isEntering=True
			api.setMouseObject(obj)
	if hasattr(mouseObject,"event_mouseMove"):
		try:
			mouseObject.event_mouseMove(isEntering,x,y,mouseOldX,mouseOldY)
			mouseOldX=x
			mouseOldY=y
		except:
			debug.writeException("api.notifyMouseMoved")

#Register internal mouse event

def initialize():
	global hookManager
	(x,y)=winUser.getCursorPos()
	api.setMouseObject(NVDAObjects.IAccessible.getNVDAObjectFromPoint(x,y))
	ctypes.cdll.mouseHook.initialize(internal_mouseEvent)

def terminate():
	ctypes.cdll.mouseHook.terminate()
