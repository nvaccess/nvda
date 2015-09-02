#touchHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012 NV Access Limited

import wx
import threading
from ctypes import *
from ctypes.wintypes import *
import re
import winVersion
import globalPluginHandler
import config
import winUser
import speech
import api
import ui
import inputCore
import screenExplorer
from logHandler import log
import touchTracker
import gui
import core

availableTouchModes=['text','object']

touchModeLabels={
	"text":_("text mode"),
	"object":_("object mode"),
}

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

	def __init__(self,tracker,mode):
		super(TouchInputGesture,self).__init__()
		self.tracker=tracker
		self.mode=mode

	def _get__rawIdentifiers(self):
		ID=""
		if self.tracker.numHeldFingers>0:
			ID+="%dfinger_hold+"%self.tracker.numHeldFingers
		if self.tracker.numFingers>1:
			ID+="%dfinger_"%self.tracker.numFingers
		if self.tracker.actionCount>1:
			ID+="%s_"%self.counterNames[min(self.tracker.actionCount,4)-1]
		ID+=self.tracker.action
		IDs=[]
		IDs.append("TS(%s):%s"%(self.mode,ID))
		IDs.append("ts:%s"%ID)
		return IDs

	def _get_logIdentifier(self):
		return self._rawIdentifiers[0]

	def _get_identifiers(self):
		return [x.lower() for x in self._rawIdentifiers] 

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
		self.pendingEmitsTimer=wx.PyTimer(core.requestPump)
		super(TouchHandler,self).__init__()
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
			x=winUser.LOWORD(lParam)
			y=winUser.HIWORD(lParam)
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
		for tracker in self.trackerManager.emitTrackers():
			gesture=TouchInputGesture(tracker,self._curTouchMode)
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
		l, t, w, h = obj.location
		oledll.oleacc.AccNotifyTouchInteraction(gui.mainFrame.Handle, obj.windowHandle,
			POINT(l + (w / 2), t + (h / 2)))

handler=None

def initialize():
	global handler
	if not config.isInstalledCopy():
		log.debugWarning("Touch only supported on installed copies")
		raise NotImplementedError
	if (winVersion.winVersion.major*10+winVersion.winVersion.minor)<62:
		log.debugWarning("Touch only supported on Windows 8 and higher")
		raise NotImplementedError
	maxTouches=windll.user32.GetSystemMetrics(95) #maximum touches
	if maxTouches<=0:
		log.debugWarning("No touch devices found")
		raise NotImplementedError
	handler=TouchHandler()
	log.debug("Touch support initialized. maximum touch inputs: %d"%maxTouches) 

def terminate():
	global handler
	if handler:
		handler.terminate()
		handler=None
