# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2012-2021 NV Access Limited, Joseph Lee, Babbage B.V.

"""handles touchscreen interaction (Windows 8 and later).
Used to provide input gestures for touchscreens, touch modes and other support facilities.
In order to use touch features, NVDA must be installed on a touchscreen computer running Windows 8 and later.
"""

import threading
from ctypes import *
from ctypes.wintypes import *
import re
import gui
import winVersion
import config
import winUser
import inputCore
import screenExplorer
from logHandler import log
import touchTracker
import core
import systemUtils


availableTouchModes=['text','object']

touchModeLabels={
	"text":_("text mode"),
	"object":_("object mode"),
}

SM_MAXIMUMTOUCHES=95
HWND_MESSAGE=-3

WM_QUIT=18

PT_TOUCH=0x02

_WM_POINTER_FIRST=WM_NCPOINTERUPDATE=0x0241
WM_NCPOINTERDOWN=0x0242
WM_NCPOINTERUP=0x0243
WM_NCPOINTERCANCEL=0x0244
WM_POINTERUPDATE=0x0245
WM_POINTERDOWN=0x0246
WM_POINTERUP=0x0247
WM_POINTERCANCEL=0x0248
WM_POINTERENTER=0x0249
WM_POINTERLEAVE=0x024A
WM_POINTERACTIVATE=0x024B
WM_POINTERCAPTURECHANGED=0x024C
WM_TOUCHHITTESTING=0x024D
WM_POINTERWHEEL=0x024E
_WM_POINTER_LAST=WM_POINTERHWHEEL=0x024F

POINTER_FLAG_CANCELED=0x400
POINTER_FLAG_UP=0x40000

POINTER_MESSAGE_FLAG_NEW=0x1
POINTER_MESSAGE_FLAG_INRANGE=0x2
POINTER_MESSAGE_FLAG_INCONTACT=0x4
POINTER_MESSAGE_FLAG_FIRSTBUTTON=0x10
POINTER_MESSAGE_FLAG_PRIMARY=0x100
POINTER_MESSAGE_FLAG_CONFIDENCE=0x200
POINTER_MESSAGE_FLAG_CANCELED=0x400

class POINTER_INFO(Structure):
	_fields_=[
		('pointerType',DWORD),
		('pointerId',c_uint32),
		('frameId',c_uint32),
		('pointerFlags',c_uint32),
		('sourceDevice',HANDLE),
		('hwndTarget',HWND),
		('ptPixelLocation',POINT),
		('ptHimetricLocation',POINT),
		('ptPixelLocationRaw',POINT),
		('ptHimetricLocationRaw',POINT),
		('dwTime',DWORD),
		('historyCount',c_uint32),
		('inputData',c_int),
		('dwKeyStates',DWORD),
		('PerformanceCount',c_uint64),
	]

class POINTER_TOUCH_INFO(Structure):
	_fields_=[
		('pointerInfo',POINTER_INFO),
		('touchFlags',c_uint32),
		('touchMask',c_uint32),
		('rcContact',RECT),
		('rcContactRaw',RECT),
		('orientation',c_uint32),
		('pressure',c_uint32),
	]

ANRUS_TOUCH_MODIFICATION_ACTIVE=2

touchWindow=None
touchThread=None

class TouchInputGesture(inputCore.InputGesture):
	"""
	Represents a gesture performed on a touch screen.
	Possible actions are:
	* Tap: a finger touches the screen only for a very short amount of time.
	* Flick{Left|Right|Up|Down}: a finger swipes the screen in a particular direction.
	* Tap and hold: a finger taps the screen but then again touches the screen, this time remaining held.
	* Hover down: A finger touches the screen long enough for the gesture to not be a tap, and it is also not already part of a tap and hold. 
	* Hover: a finger is still touching the screen, and may be moving around. Only the most recent finger to be hovering causes these gestures.
	* Hover up: a finger that was classed as a hover, releases contact with the screen.
	All actions accept for Hover down, Hover and Hover up, can be made up of multiple fingers. It is possible to have things such as a 3-finger tap, or a 2-finger Tap and Hold, or a 4 finger Flick right.
	Taps maybe pluralized (I.e. a tap very quickly followed by another tap of the same number of fingers will be represented by a double tap, rather than two separate taps). Currently double, tripple and quadruple plural taps are detected.
	Tap and holds can be pluralized also (E.g. a double tap and hold means that there were two taps before the hold).
	Actions also communicate if other fingers are currently held while performing the action. E.g. a hold+tap is when a finger touches the screen long enough to become a hover, and a tap with another finger is performed, while the first finger remains on the screen. Holds themselves also can be made of multiple fingers.
	Based on all of this, gestures could be as complicated as a 5-finger hold + 5-finger quadruple tap and hold.
	To find out the generalized point on the screen at which the gesture was performed, use this gesture's x and y properties.
	If low-level information  about the fingers and sub-gestures making up this gesture is required, the gesture's tracker and preheldTracker properties can be accessed. 
	See touchHandler.MultitouchTracker for definitions of the available properties.
	"""

	counterNames=["single","double","tripple","quodruple"]

	pluralActionLabels={
		# Translators: a touch screen action performed once 
		"single":_("single {action}"),
		# Translators: a touch screen action performed twice
		"double":_("double {action}"),
		# Translators: a touch screen action performed 3 times
		"tripple":_("tripple {action}"),
		# Translators: a touch screen action performed 4 times
		"quodruple":_("quadruple {action}"),
	}

	# Translators: a touch screen action using multiple fingers
	multiFingerActionLabel=_("{numFingers} finger {action}")

	def _get_speechEffectWhenExecuted(self):
		if self.tracker.action in (touchTracker.action_hover,touchTracker.action_hoverUp): return None
		return super(TouchInputGesture,self).speechEffectWhenExecuted

	def _get_reportInInputHelp(self):
		return self.tracker.action!=touchTracker.action_hover

	def __init__(self,preheldTracker,tracker,mode):
		super(TouchInputGesture,self).__init__()
		self.tracker=tracker
		self.preheldTracker=preheldTracker
		self.mode=mode
		self.x=tracker.x
		self.y=tracker.y

	def _get_identifiers(self):
		IDs=[]
		for includeHeldFingers in ([True,False] if self.preheldTracker else [False]):
			ID=""
			if self.preheldTracker:
				ID+=("%dfinger_hold+"%self.preheldTracker.numFingers) if includeHeldFingers else "hold+"
			if self.tracker.numFingers>1:
				ID+="%dfinger_"%self.tracker.numFingers
			if self.tracker.actionCount>1:
				ID+="%s_"%self.counterNames[min(self.tracker.actionCount,4)-1]
			ID+=self.tracker.action
			# "ts" is the gesture identifier source prefix for "touch screen".
			IDs.append("ts(%s):%s"%(self.mode,ID))
			IDs.append("ts:%s"%ID)
		return IDs

	RE_IDENTIFIER = re.compile(r"^ts(?:\((.+?)\))?:(.*)$")

	@classmethod
	def getDisplayTextForIdentifier(cls, identifier):
		mode,IDs=cls.RE_IDENTIFIER.match(identifier).groups()
		actions=[]
		for ID in IDs.split('+'):
			action=None
			foundAction=foundPlural=False
			for subID in reversed(ID.split('_')):
				if not foundAction:
					action=touchTracker.actionLabels[subID]
					foundAction=True
					continue
				if not foundPlural:
					pluralActionLabel=cls.pluralActionLabels.get(subID)
					if pluralActionLabel:
						action=pluralActionLabel.format(action=action)
						foundPlural=True
						continue
				if subID.endswith('finger'):
					numFingers=int(subID[:0-len('finger')])
					if numFingers>1:
						action=cls.multiFingerActionLabel.format(numFingers=numFingers,action=action)
				break
			actions.append(action)
		# Translators: a touch screen gesture
		source=_("Touch screen")
		if mode:
			source=u"{source}, {mode}".format(source=source,mode=touchModeLabels[mode])
		return source,u" + ".join(actions)

inputCore.registerGestureSource("ts", TouchInputGesture)

class TouchHandler(threading.Thread):
	def __init__(self):
		self.pendingEmitsTimer=gui.NonReEntrantTimer(core.requestPump)
		super().__init__(name=f"{self.__class__.__module__}.{self.__class__.__qualname__}")
		self._curTouchMode='object'
		self.initializedEvent=threading.Event()
		self.threadExc=None
		self.start()
		self.initializedEvent.wait()
		if self.threadExc:
			raise self.threadExc

	def terminate(self):
		windll.user32.PostThreadMessageW(self.ident,WM_QUIT,0,0)
		self.join()
		self.pendingEmitsTimer.Stop()

	def run(self):
		try:
			self._appInstance=windll.kernel32.GetModuleHandleW(None)
			self._cInputTouchWindowProc=winUser.WNDPROC(self.inputTouchWndProc)
			self._wc=winUser.WNDCLASSEXW(cbSize=sizeof(winUser.WNDCLASSEXW),lpfnWndProc=self._cInputTouchWindowProc,hInstance=self._appInstance,lpszClassName="inputTouchWindowClass")
			self._wca=windll.user32.RegisterClassExW(byref(self._wc))
			self._touchWindow=windll.user32.CreateWindowExW(0,self._wca,u"NVDA touch input",0,0,0,0,0,HWND_MESSAGE,None,self._appInstance,None)
			windll.user32.RegisterPointerInputTarget(self._touchWindow,PT_TOUCH)
			oledll.oleacc.AccSetRunningUtilityState(self._touchWindow,ANRUS_TOUCH_MODIFICATION_ACTIVE,ANRUS_TOUCH_MODIFICATION_ACTIVE)
			self.trackerManager=touchTracker.TrackerManager()
			self.screenExplorer=screenExplorer.ScreenExplorer()
			self.screenExplorer.updateReview=True
		except Exception as e:
			self.threadExc=e
		finally:
			self.initializedEvent.set()
		msg=MSG()
		while windll.user32.GetMessageW(byref(msg),None,0,0):
			windll.user32.TranslateMessage(byref(msg))
			windll.user32.DispatchMessageW(byref(msg))
		oledll.oleacc.AccSetRunningUtilityState(self._touchWindow,ANRUS_TOUCH_MODIFICATION_ACTIVE,0)
		windll.user32.UnregisterPointerInputTarget(self._touchWindow,PT_TOUCH)
		windll.user32.DestroyWindow(self._touchWindow)
		windll.user32.UnregisterClassW(self._wca,self._appInstance)

	def inputTouchWndProc(self,hwnd,msg,wParam,lParam):
		if msg>=_WM_POINTER_FIRST and msg<=_WM_POINTER_LAST:
			flags=winUser.HIWORD(wParam)
			touching=(flags&POINTER_MESSAGE_FLAG_INRANGE) and (flags&POINTER_MESSAGE_FLAG_FIRSTBUTTON)
			x=winUser.GET_X_LPARAM(lParam)
			y=winUser.GET_Y_LPARAM(lParam)
			ID=winUser.LOWORD(wParam)
			if touching:
				self.trackerManager.update(ID,x,y,False)
				core.requestPump()
			elif not flags&POINTER_MESSAGE_FLAG_FIRSTBUTTON:
				self.trackerManager.update(ID,x,y,True)
				core.requestPump()
			return 0
		return windll.user32.DefWindowProcW(hwnd,msg,wParam,lParam)

	def setMode(self,mode):
		if mode not in availableTouchModes:
			raise ValueError("Unknown mode %s"%mode)
		self._curTouchMode=mode

	def pump(self):
		for preheldTracker,tracker in self.trackerManager.emitTrackers():
			gesture=TouchInputGesture(preheldTracker,tracker,self._curTouchMode)
			try:
				inputCore.manager.executeGesture(gesture)
			except inputCore.NoInputGestureAction:
				pass
		interval=self.trackerManager.pendingEmitInterval
		if interval and interval>0:
			# Ensure we are pumpped again by the time more pending multiTouch trackers are ready
			self.pendingEmitsTimer.Start(interval*1000,True)
		else:
			# Stop the timer in case we were pumpped due to something unrelated but just happened to be at the appropriate time to clear any remaining trackers 
			self.pendingEmitsTimer.Stop()

	def notifyInteraction(self, obj):
		"""Notify the system that UI interaction is occurring via touch.
		This should be called when performing an action on an object.
		@param obj: The NVDAObject with which the user is interacting.
		@type obj: L{NVDAObjects.NVDAObject}
		"""
		oledll.oleacc.AccNotifyTouchInteraction(gui.mainFrame.Handle, obj.windowHandle,
			obj.location.center.toPOINT())

handler=None


def touchSupported(debugLog: bool = False):
	"""Returns if the system and current NVDA session supports touchscreen interaction.
	@param debugLog: Whether to log additional details about touch support to the NVDA log.
	"""
	if not config.isInstalledCopy() and not config.isAppX:
		if debugLog:
			log.debugWarning("Touch only supported on installed copies")
		return False
	if winVersion.getWinVer() < winVersion.WIN8:
		if debugLog:
			log.debugWarning("Touch only supported on Windows 8 and higher")
		return False
	maxTouches=windll.user32.GetSystemMetrics(SM_MAXIMUMTOUCHES)
	if maxTouches<=0:
		if debugLog:
			log.debugWarning("No touch devices found")
		return False
	if not systemUtils.hasUiAccess():
		if debugLog:
			log.debugWarning("NVDA doesn't have UI Access so touch isn't supported.")
		return False
	return True


def setTouchSupport(enable: bool):
	global handler
	if not touchSupported():
		raise NotImplementedError
	if not handler and enable:
		handler = TouchHandler()
		log.debug("Touch support enabled.")
	elif handler and not enable:
		handler.terminate()
		handler = None
		log.debug("Touch support disabled.")


def handlePostConfigProfileSwitch():
	setTouchSupport(config.conf["touch"]["enabled"])


def initialize():
	global handler
	if not touchSupported(debugLog=True):
		raise NotImplementedError
	log.debug(
		"Touchscreen detected, maximum touch inputs: %d" % winUser.user32.GetSystemMetrics(SM_MAXIMUMTOUCHES)
	)
	config.post_configProfileSwitch.register(handlePostConfigProfileSwitch)
	setTouchSupport(config.conf["touch"]["enabled"])

def terminate():
	global handler
	config.post_configProfileSwitch.unregister(handlePostConfigProfileSwitch)
	if handler:
		handler.terminate()
		handler=None
