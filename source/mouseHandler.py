#mouseHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import pyHook
import winUser
import queueHandler
import api
import debug
import speech
import NVDAObjects
import globalVars
import config
import IAccessibleHandler

mouseOldX=None
mouseOldY=None
hookManager=None


#Internal mouse event

def internal_mouseEvent(event):
	if not config.conf["mouse"]["reportObjectUnderMouse"]:
		return True
	try:
		if event.MessageName=="mouse move":
			queueHandler.queueFunction(queueHandler.mouseQueue,executeMouseMoveEvent,event.Position[0],event.Position[1])
		elif event.MessageName.endswith("down"):
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
		obj=NVDAObjects.IAccessible.IAccessible(newPacc,newChild)
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
	hookManager=pyHook.HookManager()
	hookManager.MouseAll=internal_mouseEvent
	hookManager.HookMouse()

def terminate():
	hookManager.UnhookMouse()
