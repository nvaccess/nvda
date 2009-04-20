#mouseHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import tones
import ctypes
import winUser
import queueHandler
import api
import speech
import globalVars
import eventHandler
from logHandler import log
import config
import mouseHook

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

def playAudioCoordinates(x, y, screenWidth, screenHeight, detectBrightness=True,blurFactor=0):
	minPitch=config.conf['mouse']['audioCoordinates_minPitch']
	maxPitch=config.conf['mouse']['audioCoordinates_maxPitch']
	curPitch=minPitch+((maxPitch-minPitch)*((screenHeight-y)/float(screenHeight)))
	if detectBrightness:
		screenDC=ctypes.windll.user32.GetDC(0)
		brightness=0
		for i in range(x-blurFactor,x+blurFactor+1):
			for j in range(y-blurFactor,y+blurFactor+1):
				if i>=0 and i<screenWidth and j>=0 and j<screenHeight:
					p=ctypes.windll.gdi32.GetPixel(screenDC,i,j)
					grey=0.3*((p>>16)&0xff)+0.59*((p>>8)&0xff)+0.11*(p&0xff)
					brightness=(brightness+(grey/255))/2
		minBrightness=config.conf['mouse']['audioCoordinates_minVolume']
		maxBrightness=config.conf['mouse']['audioCoordinates_maxVolume']
		brightness=(brightness*(maxBrightness-minBrightness))+minBrightness
		ctypes.windll.user32.ReleaseDC(0,screenDC)
	else:
		brightness=config.conf['mouse']['audioCoordinates_maxVolume']
	leftVolume=(85*((screenWidth-float(x))/screenWidth))*brightness
	rightVolume=(85*(float(x)/screenWidth))*brightness
	tones.beep(curPitch,40,left=leftVolume,right=rightVolume)

#Internal mouse event

def internal_mouseEvent(msg,x,y,injected):
	global mouseMoved, curMousePos
	if injected:
		return True
	if not config.conf['mouse']['enableMouseTracking']:
		return True
	try:
		curMousePos=(x,y)
		if msg==WM_MOUSEMOVE and (config.conf['mouse']['reportTextUnderMouse'] or config.conf['mouse']['reportObjectRoleOnMouseEnter'] or config.conf['mouse']['audioCoordinatesOnMouseMove']):
			mouseMoved=True
		elif msg in (WM_LBUTTONDOWN,WM_RBUTTONDOWN):
			queueHandler.queueFunction(queueHandler.eventQueue,speech.cancelSpeech)
	except:
		log.error("", exc_info=True)
	return True

def executeMouseMoveEvent(x,y):
	global currentMouseWindow
	desktopObject=api.getDesktopObject()
	screenLeft,screenTop,screenWidth,screenHeight=desktopObject.location
	x=min(max(screenLeft,x),(screenLeft+screenWidth)-1)
	y=min(max(screenTop,y),(screenTop+screenHeight)-1)
	if config.conf["mouse"]["audioCoordinatesOnMouseMove"]:
		playAudioCoordinates(x,y,screenWidth,screenHeight,config.conf['mouse']['audioCoordinates_detectBrightness'],config.conf['mouse']['audioCoordinates_blurFactor'])
	oldMouseObject=api.getMouseObject()
	mouseObject=desktopObject.objectFromPoint(x,y,oldNVDAObject=oldMouseObject)
	while mouseObject and mouseObject.beTransparentToMouse:
		mouseObject=mouseObject.parent
	if not mouseObject:
		return
	api.setMouseObject(mouseObject)
	try:
		eventHandler.executeEvent("mouseMove",mouseObject,x=x,y=y)
		oldMouseObject=mouseObject
	except:
		log.error("api.notifyMouseMoved", exc_info=True)

#Register internal mouse event

def initialize():
	global curMousePos, screenDC, screenWidth, screenHeight
	(x,y)=winUser.getCursorPos()
	import NVDAObjects.window
	mouseObj=NVDAObjects.window.Window.objectFromPoint(x,y)
	if not mouseObj:
		mouseObj=api.getDesktopObject()
	api.setMouseObject(mouseObj)
	curMousePos=(x,y)
	screenWidth,screenHeight=api.getDesktopObject().location[2:]
	mouseHook.initialize(internal_mouseEvent)

def pumpAll():
	global mouseMoved, curMousePos, mouseShapeChanged, curMouseShape
	if mouseMoved:
		mouseMoved=False
		(x,y)=curMousePos
		executeMouseMoveEvent(x,y)
	if config.conf["mouse"]["reportMouseShapeChanges"] and mouseShapeChanged>0:
		if mouseShapeChanged==10:
			mouseShapeChanged=0
			speech.speakMessage(_("%s cursor")%curMouseShape)
		else:
			mouseShapeChanged+=1

def terminate():
	mouseHook.terminate()
