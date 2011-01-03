#brailleDisplayDrivers/freedomScientific.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import *
from ctypes.wintypes import *
import braille
import inputCore
from winUser import WNDCLASSEXW, WNDPROC, LRESULT, HCURSOR

#Try to load the fs braille dll
try:
	fsbLib=windll.fsbrldspapi
except:
	fsbLib=None

#Map the needed functions in the fs braille dll
if fsbLib:
	fbOpen=getattr(fsbLib,'_fbOpen@12')
	fbGetCellCount=getattr(fsbLib,'_fbGetCellCount@4')
	fbWrite=getattr(fsbLib,'_fbWrite@16')
	fbClose=getattr(fsbLib,'_fbClose@4')

FB_INPUT=1
FB_DISCONNECT=2

LRESULT=c_long
HCURSOR=c_long

appInstance=windll.kernel32.GetModuleHandleW(None)

nvdaFsBrlWm=windll.user32.RegisterWindowMessageW(u"nvdaFsBrlWm")

inputType_keys=3
inputType_routing=4
inputType_wizWheel=5

@WNDPROC
def nvdaFsBrlWndProc(hwnd,msg,wParam,lParam):
	if msg==nvdaFsBrlWm and wParam==FB_INPUT:
		inputType=lParam&0xff
		if inputType==inputType_keys:
			keyBits=lParam>>8
			if keyBits:
				gesture=KeyGesture(keyBits)
				try:
					inputCore.manager.executeGesture(gesture)
				except inputCore.NoInputGestureAction:
					pass
		elif inputType==inputType_routing:
			routingIndex=(lParam>>8)&0xff
			isRoutingPressed=bool((lParam>>16)&0xff)
			isTopRoutingRow=bool((lParam>>24)&0xff)
			if isRoutingPressed:
				gesture=RoutingGesture(routingIndex,isTopRoutingRow)
				try:
					inputCore.manager.executeGesture(gesture)
				except inputCore.NoInputGestureAction:
					pass
		elif inputType==inputType_wizWheel:
			numUnits=(lParam>>8)&0x7
			isRight=bool((lParam>>12)&1)
			isDown=bool((lParam>>11)&1)
			#Right's up and down are rversed, but NVDA does not want this
			if isRight: isDown=not isDown
			for unit in xrange(numUnits):
				gesture=WizWheelGesture(isDown,isRight)
				try:
					inputCore.manager.executeGesture(gesture)
				except NoInputGestureAction:
					pass
	else:
		return windll.user32.DefWindowProcW(hwnd,msg,wParam,lParam)

nvdaFsBrlWndCls=WNDCLASSEXW()
nvdaFsBrlWndCls.cbSize=sizeof(nvdaFsBrlWndCls)
nvdaFsBrlWndCls.lpfnWndProc=nvdaFsBrlWndProc
nvdaFsBrlWndCls.hInstance=appInstance
nvdaFsBrlWndCls.lpszClassName=u"nvdaFsBrlWndCls"

class BrailleDisplayDriver(braille.BrailleDisplayDriverWithCursor):

	name="freedomScientific"
	description="Freedom Scientific Focus/PAC Mate series"

	@classmethod
	def check(cls):
		return bool(fsbLib)

	def __init__(self):
		super(BrailleDisplayDriver,self).__init__()
		self._messageWindowClassAtom=windll.user32.RegisterClassExW(byref(nvdaFsBrlWndCls))
		self._messageWindow=windll.user32.CreateWindowExW(0,self._messageWindowClassAtom,u"nvdaFsBrlWndCls window",0,0,0,0,0,None,None,appInstance,None)
		fbHandle=-1
		for port in ("usb","serial"):
			fbHandle=fbOpen(port,self._messageWindow,nvdaFsBrlWm)
			if fbHandle!=-1:
				break
		if fbHandle==-1:
			raise RuntimeError("No display found")
		self.fbHandle=fbHandle

	def terminate(self):
		super(BrailleDisplayDriver,self).terminate()
		fbClose(self.fbHandle)
		windll.user32.DestroyWindow(self._messageWindow)
		windll.user32.UnregisterClassW(self._messageWindowClassAtom,appInstance)

	def _get_numCells(self):
		return fbGetCellCount(self.fbHandle)

	def _display(self,cells):
		cells="".join([chr(x) for x in cells])
		fbWrite(self.fbHandle,0,len(cells),cells)

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollForward": ("br(freedomScientific):leftWizWheelDown","br(freedomScientific):rightWizWheelDown"),
			"braille_scrollBack": ("br(freedomScientific):leftWizWheelUp","br(freedomScientific):rightWizWheelUp"),
			"braille_routeTo": ("br(freedomScientific):routing",),
		}
	})

class InputGesture(braille.BrailleDisplayGesture):
	source = BrailleDisplayDriver.name

class KeyGesture(InputGesture):

	keyLabels=[
		#Braille keys (byte 1)
		'dot1','dot2','dot3','dot4','dot5','dot6','dot7','dot8',
		#Assorted keys (byte 2)
		'leftWizWheelPress','rightWizWheelPress',
		'leftShiftKey','rightShiftKey',
		'leftAdvanceBar','rightAdvanceBar',
		None,
		'brailleSpaceBar',
		#GDF keys (byte 3)
		'leftGDFButton','rightGDFButton',
		None,
		'leftBumperBarUp','leftBumperBarDown','rightBumperBarUp','rightBumperBarDown',
	]

	def __init__(self,keyBits):
		self.id="+".join(set(self.keyLabels[num] for num in xrange(24) if (keyBits>>num)&1))
		super(KeyGesture,self).__init__()

class RoutingGesture(InputGesture):

	def __init__(self,routingIndex,topRow=False):
		if topRow:
			self.id="topRouting%d"%(routingIndex+1)
		else:
			self.id="routing"
			self.routingIndex=routingIndex
		super(RoutingGesture,self).__init__()

class WizWheelGesture(InputGesture):

	def __init__(self,isDown,isRight):
		which="right" if isRight else "left"
		direction="Down" if isDown else "Up"
		self.id="%sWizWheel%s"%(which,direction)
		super(WizWheelGesture,self).__init__()
