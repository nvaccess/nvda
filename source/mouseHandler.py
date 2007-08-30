#mouseHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import winsound
import ctypes
import winUser
import queueHandler
import api
import debug
import speech
import NVDAObjects.IAccessible
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
	#Don't run if reportObjectUnderMouse is false
	if not config.conf["mouse"]["reportObjectUnderMouse"]:
		return
	oldMouseObject=api.getMouseObject()
	try:
		(oldLeft,oldTop,oldWidth,oldHeight)=oldMouseObject.location
	except:
		oldLeft=oldTop=oldWidth=oldHeight=0
	mouseObject=None
	#If the old mouse object was not an IAccessible, or the current coordinates are outside the old object
	#Just grab a new object at these coordinates
	if not isinstance(oldMouseObject,NVDAObjects.IAccessible.IAccessible) or x<oldLeft or x>(oldLeft+oldWidth) or y<oldTop or y>(oldTop+oldHeight):
		mouseObject=NVDAObjects.IAccessible.getNVDAObjectFromPoint(x,y)
	else:
		try:
			res=IAccessibleHandler.accHitTest(oldMouseObject.IAccessibleObject,oldMouseObject.IAccessibleChildID,x,y)
		except:
			res=None
		if res is None or (res[0]==oldMouseObject.IAccessibleObject and res[1]==oldMouseObject.IAccessibleChildID):
			return
		else:
			mouseObject=NVDAObjects.IAccessible.IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])
	if not mouseObject:
		return
	try:
		(left,top,width,height)=mouseObject.location
	except:
		left=top=width=height=0
	if (left,top,width,height)==(oldLeft,oldTop,oldWidth,oldHeight) or x<left or x>(left+width) or y<top or y>(top+height):
		return
	api.setMouseObject(mouseObject)
	if hasattr(mouseObject,"event_mouseMove"):
		try:
			mouseObject.event_mouseMove(True,x,y,mouseOldX,mouseOldY)
			oldMouseObject=mouseObject
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
