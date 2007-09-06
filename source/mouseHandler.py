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
import NVDAObjects.JAB
import NVDAObjects.IAccessible
import globalVars
import config
import IAccessibleHandler
import JABHandler

WM_MOUSEMOVE=0x0200
WM_LBUTTONDOWN=0x0201
WM_LBUTTONUP=0x0202
WM_LBUTTONDBLCLK=0x0203
WM_RBUTTONDOWN=0x0204
WM_RBUTTONUP=0x0205
WM_RBUTTONDBLCLK=0x0206

curMousePos=(0,0)
mouseMoved=False
curMouseShape=""
mouseShapeChanged=0

def updateMouseShape(name):
	global curMouseShape, mouseShapeChanged
	if not name or name==curMouseShape:
		return
	curMouseShape=name
	mouseShapeChanged=1

def playAudioCoordinates(x, y,screenWidth=None,screenHeight=None):
	(screenLeft,screenTop,screenWidth,screenHeight)=api.getDesktopObject().location
	screenRight=screenLeft+screenWidth
	screenBottom=screenTop+screenHeight
	minPitch=220
	maxPitch=880
	curPitch=minPitch+((maxPitch-minPitch)*((screenHeight-y)/float(screenHeight)))
	hdc=ctypes.windll.user32.GetDC(0)
	brightness=0
	for i in range(x-4,x+5):
		for j in range(y-4,y+5):
			if i>=screenLeft and i<screenRight and j>=screenTop and j<screenBottom:
				p=ctypes.windll.gdi32.GetPixel(hdc,i,j)
				grey=0.3*((p>>16)&0xff)+0.59*((p>>8)&0xff)+0.11*(p&0xff)
				brightness=(brightness+(grey/255))/2
	minBrightness=0.1
	maxBrightness=1
	brightness=(brightness*(maxBrightness-minBrightness))+minBrightness
	leftVolume=(85*((screenWidth-float(x))/screenWidth))*brightness
	rightVolume=(85*(float(x)/screenWidth))*brightness
	tones.beep(curPitch,40,left=leftVolume,right=rightVolume)

#Internal mouse event

@ctypes.CFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)
def internal_mouseEvent(msg,x,y,injected):
	global mouseMoved, curMousePos
	try:
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
	mouseObject=oldMouseObject
	windowAtPoint=ctypes.windll.user32.WindowFromPoint(x,y)
	if JABHandler.isJavaWindow(windowAtPoint):
		if not isinstance(oldMouseObject,NVDAObjects.JAB.JAB) or x<oldLeft or x>(oldLeft+oldWidth) or y<oldTop or y>(oldTop+oldHeight):
			oldJabContext=JABHandler.JABContext(hwnd=windowAtPoint)
		else:
			oldJabContext=oldMouseObject.jabContext
		res=oldJabContext.getAccessibleContextAt(x,y)
		if res:
			mouseObject=NVDAObjects.JAB.JAB(jabContext=res)
	else: #not a java window
		if not isinstance(oldMouseObject,NVDAObjects.IAccessible.IAccessible) or x<oldLeft or x>(oldLeft+oldWidth) or y<oldTop or y>(oldTop+oldHeight):
			mouseObject=NVDAObjects.IAccessible.getNVDAObjectFromPoint(x,y)
		else:
			res=IAccessibleHandler.accHitTest(oldMouseObject.IAccessibleObject,oldMouseObject.IAccessibleChildID,x,y)
			if res:
				mouseObject=NVDAObjects.IAccessible.IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])
	if not mouseObject:
		return
	try:
		(left,top,width,height)=mouseObject.location
	except:
		left=top=width=height=0
	if x<left or x>(left+width) or y<top or y>(top+height):
		return
	api.setMouseObject(mouseObject)
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
	global mouseMoved, curMousePos, mouseShapeChanged, curMouseShape
	if mouseMoved:
		mouseMoved=False
		(screenLeft,screenTop,screenWidth,screenHeight)=api.getDesktopObject().location
		(x,y)=curMousePos
		x=min(max(x,screenLeft),(screenLeft+screenWidth))
		y=min(max(y,screenTop),(screenTop+screenHeight))
		if config.conf["mouse"]["audioCoordinatesOnMouseMove"]:
			playAudioCoordinates(x,y,screenWidth=screenWidth,screenHeight=screenHeight)
		executeMouseMoveEvent(x,y)
	if mouseShapeChanged>0:
		if mouseShapeChanged==10:
			mouseShapeChanged=0
			speech.speakMessage(_("%s cursor")%curMouseShape)
		else:
			mouseShapeChanged+=1

def terminate():
	ctypes.cdll.mouseHook.terminate()
