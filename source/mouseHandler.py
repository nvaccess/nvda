#mouseHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import tones
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

curMousePos=(0,0)
mouseMoved=False

def playAudioCoordinates(x, y,screenWidth=None,screenHeight=None):
	if not screenWidth or not screenHeight:
		(screenLeft,screenTop,screenWidth,screenHeight)=api.getDesktopObject().location
	minPitch=220
	maxPitch=880
	curPitch=minPitch+((maxPitch-minPitch)*((screenHeight-float(y))/screenHeight))
	minVolume=5
	maxVolume=100
	volumeRange=maxVolume-minVolume
	hdc=ctypes.windll.user32.GetDC(0)
	brightness=0
	for i in range(x-4,x+5):
		for j in range(y-4,y+5):
			if i>=0 and j>=0:
				p=ctypes.windll.gdi32.GetPixel(hdc,i,j)
				grey=0.3*((p>>16)&0xff)+0.59*((p>>8)&0xff)+0.11*(p&0xff)
				brightness=(brightness+(grey/255))/2
	leftVolume=minVolume+(volumeRange*((screenWidth-float(x))/screenWidth))*brightness
	rightVolume=minVolume+(volumeRange*(float(x)/screenWidth))*brightness
	tones.beep(curPitch,40,left=leftVolume,right=rightVolume)

#Internal mouse event

@ctypes.CFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)
def internal_mouseEvent(msg,x,y,injected):
	global mouseMoved, curMousePos
	try:
		if injected:
			return True
		curMousePos=(x,y)
		if msg==WM_MOUSEMOVE and config.conf["mouse"]["reportObjectUnderMouse"]:
			mouseMoved=True
		elif msg in (WM_LBUTTONDOWN,WM_RBUTTONDOWN):
			queueHandler.queueFunction(queueHandler.interactiveQueue,speech.cancelSpeech)
		return True
	except:
		debug.writeException("mouseHandler.internal_mouseEvent")

def executeMouseMoveEvent(x,y):
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
			mouseObject.event_mouseMove(x,y)
			oldMouseObject=mouseObject
		except:
			debug.writeException("api.notifyMouseMoved")

#Register internal mouse event

def initialize():
	(x,y)=winUser.getCursorPos()
	api.setMouseObject(NVDAObjects.IAccessible.getNVDAObjectFromPoint(x,y))
	curMousePos=(x,y)
	ctypes.cdll.mouseHook.initialize(internal_mouseEvent)

def pumpAll():
	global mouseMoved, curMousePos
	if mouseMoved:
		mouseMoved=False
		(screenLeft,screenTop,screenWidth,screenHeight)=api.getDesktopObject().location
		(x,y)=curMousePos
		x=min(max(x,screenLeft),(screenLeft+screenWidth))
		y=min(max(y,screenTop),(screenTop+screenHeight))
		if config.conf["mouse"]["audioCoordinatesOnMouseMove"]:
			playAudioCoordinates(x,y,screenWidth=screenWidth,screenHeight=screenHeight)
		executeMouseMoveEvent(x,y)

def terminate():
	ctypes.cdll.mouseHook.terminate()
