#mouseHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import pyHook
import winUser
import core
import api
import debug
import audio
import NVDAObjects
import globalVars
import config
import IAccessibleHandler

mouseOldX=None
mouseOldY=None


#Internal mouse event

def internal_mouseEvent(event):
	if not config.conf["mouse"]["reportObjectUnderMouse"]:
		return True
	try:
		if event.MessageName=="mouse move":
			core.executeFunction(core.EXEC_MOUSE,executeMouseMoveEvent,event.Position[0],event.Position[1])
		elif event.MessageName.endswith("down"):
			core.executeFunction(core.EXEC_SPEECH,audio.cancel)
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
		obj=NVDAObjects.IAccessible.NVDAObject_IAccessible(newPacc,newChild)
		if obj:
			mouseObject=obj
			isEntering=True
			api.setMouseObject(obj)
	if hasattr(mouseObject,"event_mouseMove"):
		try:
			mouseObject.event_mouseMove(isEntering,x,y,mouseOldX,mouseOldY)
		except:
			debug.writeException("api.notifyMouseMoved")
	mouseOldX=x
	mouseOldY=y

#Register internal mouse event

def initialize():
	hookManager=pyHook.HookManager()
	hookManager.MouseAll=internal_mouseEvent
	hookManager.HookMouse()
