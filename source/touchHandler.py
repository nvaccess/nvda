from ctypes import *
from ctypes.wintypes import *
import sys
import globalPluginHandler
import config
import winUser
import speech
import api
import ui
import queueHandler
import inputCore
import screenExplorer
from logHandler import log
import touchTracker

availableTouchModes=['text','object']

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

	def _get_displayName(self):
		return " ".join(self._rawIdentifiers[1][3:].split('_'))

class TouchHandler(object):

	def __init__(self):
		self._curTouchMode='object'
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
		self.gesturePump=self.gesturePumpFunc()
		queueHandler.registerGeneratorObject(self.gesturePump)

	def inputTouchWndProc(self,hwnd,msg,wParam,lParam):
		if msg>=_WM_POINTER_FIRST and msg<=_WM_POINTER_LAST:
			flags=winUser.HIWORD(wParam)
			touching=(flags&POINTER_MESSAGE_FLAG_INRANGE) and (flags&POINTER_MESSAGE_FLAG_FIRSTBUTTON)
			x=winUser.LOWORD(lParam)
			y=winUser.HIWORD(lParam)
			ID=winUser.LOWORD(wParam)
			if touching:
				self.trackerManager.update(ID,x,y,False)
			elif not flags&POINTER_MESSAGE_FLAG_FIRSTBUTTON:
				self.trackerManager.update(ID,x,y,True)
			return 0
		return windll.user32.DefWindowProcW(hwnd,msg,wParam,lParam)

	def terminate(self):
		self.gesturePump.close()
		oledll.oleacc.AccSetRunningUtilityState(self._touchWindow,ANRUS_TOUCH_MODIFICATION_ACTIVE,0)
		windll.user32.UnregisterPointerInputTarget(self._touchWindow,PT_TOUCH)
		windll.user32.DestroyWindow(self._touchWindow)
		windll.user32.UnregisterClassW(self._wca,self._appInstance)

	def setMode(self,mode):
		if mode not in availableTouchModes:
			raise ValueError("Unknown mode %s"%mode)
		self._curTouchMode=mode

	def gesturePumpFunc(self):
		while True:
			for tracker in self.trackerManager.emitTrackers():
				gesture=TouchInputGesture(tracker,self._curTouchMode)
				try:
					inputCore.manager.executeGesture(gesture)
				except inputCore.NoInputGestureAction:
					pass
			yield

handler=None

def initialize():
	global handler
	if not config.isInstalledCopy():
		log.debugWarning("Touch only supported on installed copies")
		raise NotImplementedError
	version=sys.getwindowsversion()
	if (version.major*10+version.minor)<62:
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
