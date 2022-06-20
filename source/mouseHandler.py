#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016-2018 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from dataclasses import dataclass
from typing import Optional
import time
import wx
import gui
import tones
import ctypes
import winUser
import queueHandler
import api
import screenBitmap
import speech
import globalVars
import eventHandler
from logHandler import log
import config
import winInputHook
import core
import ui
from math import floor
from contextlib import contextmanager
import threading

WM_MOUSEMOVE=0x0200
WM_LBUTTONDOWN=0x0201
WM_LBUTTONUP=0x0202
WM_LBUTTONDBLCLK=0x0203
WM_RBUTTONDOWN=0x0204
WM_RBUTTONUP=0x0205
WM_RBUTTONDBLCLK=0x0206

curMousePos=(0,0)
mouseMoved=False
ignoreInjected=False
curMouseShape=""
_shapeTimer=None
scrBmpObj=None
#: The time (in seconds) at which the last mouse event occurred.
#: @type: float
lastMouseEventTime=0

SHAPE_REPORT_DELAY = 100
def updateMouseShape(name):
	global curMouseShape
	if not name or name==curMouseShape:
		return
	curMouseShape=name
	if config.conf["mouse"]["reportMouseShapeChanges"]:
		# Delay reporting to avoid unnecessary/excessive verbosity.
		_shapeTimer.Stop()
		_shapeTimer.Start(SHAPE_REPORT_DELAY, True)

_ignoreInjectionLock = threading.Lock()
@contextmanager
def ignoreInjection():
	"""Context manager that allows ignoring injected mouse events temporarily by using a with statement."""
	global ignoreInjected
	with _ignoreInjectionLock:
		ignoreInjected=True
		yield
		ignoreInjected=False

def playAudioCoordinates(x, y, screenWidth, screenHeight, screenMinPos, detectBrightness=True,blurFactor=0):
	""" play audio coordinates:
	- left to right adjusting the volume between left and right speakers
	- top to bottom adjusts the pitch of the sound
	- brightness adjusts the volume of the sound
	Coordinates (x, y) are absolute, and can be negative.
	"""

	# make relative to (0,0) and positive
	x = x - screenMinPos.x
	y = y - screenMinPos.y

	minPitch=config.conf['mouse']['audioCoordinates_minPitch']
	maxPitch=config.conf['mouse']['audioCoordinates_maxPitch']
	curPitch=minPitch+((maxPitch-minPitch)*((screenHeight-y)/float(screenHeight)))
	if detectBrightness:
		startX=min(max(x-blurFactor,0),screenWidth)+screenMinPos.x
		startY=min(max(y-blurFactor,0),screenHeight)+screenMinPos.y
		width=min(blurFactor+1,screenWidth)
		height=min(blurFactor+1,screenHeight)
		grey=screenBitmap.rgbPixelBrightness(scrBmpObj.captureImage( startX, startY, width, height)[0][0])
		brightness=grey/255.0
		minBrightness=config.conf['mouse']['audioCoordinates_minVolume']
		maxBrightness=config.conf['mouse']['audioCoordinates_maxVolume']
		brightness=(brightness*(maxBrightness-minBrightness))+minBrightness
	else:
		brightness=config.conf['mouse']['audioCoordinates_maxVolume']
	leftVolume=int((85*((screenWidth-float(x))/screenWidth))*brightness)
	rightVolume=int((85*(float(x)/screenWidth))*brightness)
	tones.beep(curPitch,40,left=leftVolume,right=rightVolume)

#Internal mouse event

def internal_mouseEvent(msg,x,y,injected):
	"""Event called by winInputHook when it receives a mouse event.
	"""
	global mouseMoved, curMousePos, lastMouseEventTime
	lastMouseEventTime=time.time()
	if injected and (ignoreInjected or config.conf['mouse']['ignoreInjectedMouseInput']):
		return True
	if not config.conf['mouse']['enableMouseTracking']:
		return True
	try:
		curMousePos=(x,y)
		if msg==WM_MOUSEMOVE: 
			mouseMoved=True
			core.requestPump()
		elif msg in (WM_LBUTTONDOWN,WM_RBUTTONDOWN):
			queueHandler.queueFunction(queueHandler.eventQueue,speech.cancelSpeech)
	except:
		log.error("", exc_info=True)
	return True

def executeMouseEvent(flags, x, y, data=0):
	"""
	Mouse events generated with this rapper for L{winUser.mouse_event}
	will be ignored by NVDA.
	Consult https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-mouse_event
	for detailed parameter documentation.
	@param flags: Controls various aspects of mouse motion and button clicking.
		The supplied value should be one or a combination of the C{winUser.MOUSEEVENTF_*} constants.
	@type flags: int
	@param x: The mouse's absolute position along the x-axis
		or its amount of motion since the last mouse event was generated.
	@type x: int
	@param y: The mouse's absolute position along the y-axis
		or its amount of motion since the last mouse event was generated.
	@type y: int
	@param data: Additional data depending on what flags are specified.
		This defaults to 0.
	@type data: int
	"""
	with ignoreInjection():
		winUser.mouse_event(flags, x, y, data, None)

def getMouseRestrictedToScreens(x, y, displays):
	""" Ensures that the mouse position is within the area of one of the displays, relative to (0,0) 
		but not necessarily positive (which is as expected for mouse coordinates)

		We need to first get the closest point on the edge of each display rectangle (if the mouse
		is outside the rectangle). This is done by clamping the mouse position to the extents of each
		screen. The distance from this point to the actual mouse position can then be calculated. The
		smallest adjustment to get the mouse within the screen bounds is desired.
	"""
	mpos =wx.RealPoint(x,y)
	closestDistValue = None
	newXY = None
	for screenRect in displays:
		halfWidth = wx.RealPoint(0.5*screenRect.GetWidth(),0.5*screenRect.GetHeight())
		tl = screenRect.GetTopLeft()
		# tl is an integer based wx.Point, so convert to float based wx.RealPoint
		screenMin =  wx.RealPoint(tl.x, tl.y)
		screenCenter = screenMin + halfWidth
		scrCenterToMouse = mpos - screenCenter
		mouseLimitedToScreen = screenCenter + wx.RealPoint( # relative to origin
			max(min(scrCenterToMouse.x, halfWidth.x), -halfWidth.x),
			max(min(scrCenterToMouse.y, halfWidth.y), -halfWidth.y))
		edgeToMouse = mpos - mouseLimitedToScreen
		distFromRectToMouseSqd = abs(edgeToMouse.x) + abs(edgeToMouse.y)
		if closestDistValue == None or closestDistValue > distFromRectToMouseSqd:
			closestDistValue = distFromRectToMouseSqd
			newXY = mouseLimitedToScreen

	# drop any partial position information. Even the 99% of the way to the edge of a 
	# pixel is still in the pixel.
	return (int(floor(newXY.x)), int(floor(newXY.y)))

def getMinMaxPoints(screenRect):
	screenMin = screenRect.GetTopLeft()
	screenDim = wx.Point(screenRect.GetWidth(),screenRect.GetHeight())
	screenMax = screenMin+screenDim
	return (screenMin, screenMax)

def getTotalWidthAndHeightAndMinimumPosition(displays):
	""" Calculate the total screen width and height.

	Depending on screen layouts the rectangles may overlap on the vertical or 
	horizontal axis. Screens may also have a gap between them. In the case where
	there is a gap in between we count that as contributing to the full virtual
	space """
	smallestX, smallestY, largestX, largestY = (None, None, None, None)
	for screenRect in displays:
		(screenMin, screenMax) = getMinMaxPoints(screenRect)
		if smallestX == None or screenMin.x < smallestX: smallestX = screenMin.x
		if smallestY == None or screenMin.y < smallestY: smallestY = screenMin.y
		if largestX == None or screenMax.x > largestX: largestX = screenMax.x
		if largestY == None or screenMax.y > largestY: largestY = screenMax.y

	# get full range, including any "blank space" between monitors
	totalWidth = largestX - smallestX
	totalHeight = largestY - smallestY

	return (totalWidth, totalHeight, wx.Point(smallestX, smallestY))

def executeMouseMoveEvent(x,y):
	global currentMouseWindow
	desktopObject=api.getDesktopObject()
	displays = [ wx.Display(i).GetGeometry() for i in range(wx.Display.GetCount()) ]
	x, y = getMouseRestrictedToScreens(x, y, displays)
	screenWidth, screenHeight, minPos = getTotalWidthAndHeightAndMinimumPosition(displays)

	if config.conf["mouse"]["audioCoordinatesOnMouseMove"]:
		playAudioCoordinates(x, y, screenWidth, screenHeight, minPos,
			config.conf['mouse']['audioCoordinates_detectBrightness'],
			config.conf['mouse']['audioCoordinates_blurFactor'])

	oldMouseObject=api.getMouseObject()
	mouseObject=desktopObject.objectFromPoint(x, y)
	while mouseObject and mouseObject.beTransparentToMouse:
		mouseObject=mouseObject.parent
	if not mouseObject:
		return
	if oldMouseObject==mouseObject:
		mouseObject=oldMouseObject
	else:
		api.setMouseObject(mouseObject)
	try:
		eventHandler.executeEvent("mouseMove",mouseObject,x=x,y=y)
		oldMouseObject=mouseObject
	except:
		log.error("api.notifyMouseMoved", exc_info=True)

#Register internal mouse event

def initialize():
	global curMousePos, scrBmpObj, _shapeTimer
	scrBmpObj=screenBitmap.ScreenBitmap(1,1)
	(x,y)=winUser.getCursorPos()
	desktopObject=api.getDesktopObject()
	try:
		mouseObject=desktopObject.objectFromPoint(x,y)
	except:
		log.exception("Error retrieving initial mouse object")
		mouseObject=None
	if not mouseObject:
		mouseObject=api.getDesktopObject()
	api.setMouseObject(mouseObject)
	curMousePos=(x,y)
	winInputHook.initialize()
	winInputHook.setCallbacks(mouse=internal_mouseEvent)
	_shapeTimer = gui.NonReEntrantTimer(_reportShape)

def _reportShape():
	# Translators: Reported when mouse cursor shape changes (example output: edit cursor).
	ui.message(_("%s cursor")%curMouseShape)

def pumpAll():
	global mouseMoved, curMousePos
	if mouseMoved:
		mouseMoved=False
		(x,y)=curMousePos
		executeMouseMoveEvent(x,y)

def terminate():
	global scrBmpObj, _shapeTimer
	if isLeftMouseButtonLocked():
		unlockLeftMouseButton()
	if isRightMouseButtonLocked():
		unlockRightMouseButton()
	scrBmpObj=None
	winInputHook.terminate()
	_shapeTimer.Stop()
	_shapeTimer = None


@dataclass
class LogicalButtonFlags:
	"""
	A container for holding the flags denoting the primary and secondary buttons on a mouse.
	See L{GetLogicalButtonFlags}.
	"""
	primaryDown: int
	primaryUp: int
	secondaryDown: int
	secondaryUp: int


def getLogicalButtonFlags() -> LogicalButtonFlags:
	"""
	Fills and returns a LogicalButtonFlags object with the appropriate MOUSEEVENTF_* button flags
	taking into account the Windows user setting
	for which button (left or right) is primary and which is secondary.
	"""
	swappedButtons = ctypes.windll.user32.GetSystemMetrics(winUser.SM_SWAPBUTTON)
	if not swappedButtons:
		return LogicalButtonFlags(
			primaryDown=winUser.MOUSEEVENTF_LEFTDOWN,
			primaryUp=winUser.MOUSEEVENTF_LEFTUP,
			secondaryDown=winUser.MOUSEEVENTF_RIGHTDOWN,
			secondaryUp=winUser.MOUSEEVENTF_RIGHTUP,
		)
	else:
		return LogicalButtonFlags(
			primaryDown=winUser.MOUSEEVENTF_RIGHTDOWN,
			primaryUp=winUser.MOUSEEVENTF_RIGHTUP,
			secondaryDown=winUser.MOUSEEVENTF_LEFTDOWN,
			secondaryUp=winUser.MOUSEEVENTF_LEFTUP,
		)


def _doClick(
		downFlag: int,
		upFlag: int,
		releaseDelay: Optional[float] = None
):
	executeMouseEvent(downFlag, 0, 0)
	if releaseDelay:
		time.sleep(releaseDelay)
	executeMouseEvent(upFlag, 0, 0)


def doPrimaryClick(releaseDelay: Optional[float] = None):
	"""
	Performs a primary mouse click at the current mouse pointer location.
	The primary button is the one that usually activates or selects an item.
	This function honors the Windows user setting
	for which button (left or right) is classed as the primary button.
	@ param releaseDelay: optional float in seconds of how long NVDA should sleep
	between pressing down and then releasing up the primary button.
	"""
	buttonFlags = getLogicalButtonFlags()
	_doClick(buttonFlags.primaryDown, buttonFlags.primaryUp, releaseDelay)


def doSecondaryClick(releaseDelay: Optional[float] = None):
	"""
	Performs a secondary mouse click at the current mouse pointer location.
	The secondary button is the one that usually displays a context menu for an item when clicked.
	This function honors the Windows user setting
	for which button (left or right) is classed as the secondary button.
	@ param releaseDelay: optional float in seconds of how long NVDA should sleep
	between pressing down and then releasing up the primary button.
	"""
	buttonFlags = getLogicalButtonFlags()
	_doClick(buttonFlags.secondaryDown, buttonFlags.secondaryUp, releaseDelay)


def isLeftMouseButtonLocked():
	""" Tests if the left mouse button is locked """
	return winUser.getKeyState(winUser.VK_LBUTTON) & 1 << 15


def lockLeftMouseButton():
	""" Locks the left mouse button """
	# Translators: This is presented when the left mouse button is locked down (used for drag and drop).
	ui.message(_("Left mouse button lock"))
	executeMouseEvent(winUser.MOUSEEVENTF_LEFTDOWN, 0, 0)


def unlockLeftMouseButton():
	""" Unlocks the left mouse button """
	# Translators: This is presented when the left mouse button lock is released (used for drag and drop).
	ui.message(_("Left mouse button unlock"))
	executeMouseEvent(winUser.MOUSEEVENTF_LEFTUP, 0, 0)


def isRightMouseButtonLocked():
	""" Tests if the right mouse button is locked """
	return winUser.getKeyState(winUser.VK_RBUTTON) & 1 << 15


def lockRightMouseButton():
	""" Locks the right mouse button """
	# Translators: This is presented when the right mouse button is locked down (used for drag and drop).
	ui.message(_("Right mouse button lock"))
	executeMouseEvent(winUser.MOUSEEVENTF_RIGHTDOWN, 0, 0)


def unlockRightMouseButton():
	""" Unlocks the right mouse button """
	# Translators: This is presented when the right mouse button lock is released (used for drag and drop).
	ui.message(_("Right mouse button unlock"))
	executeMouseEvent(winUser.MOUSEEVENTF_RIGHTUP, 0, 0)
