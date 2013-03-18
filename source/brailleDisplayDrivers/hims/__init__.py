#brailleDisplayDrivers/hims/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2013 Gianluca Casalino, NV Access Limited

from logHandler import log
from ctypes import *
from ctypes.wintypes import *
import braille
import inputCore
from winUser import WNDCLASSEXW, WNDPROC, LRESULT, HCURSOR
import hwPortUtils
from brailleInput import BrailleInputGesture

HIMS_KEYPRESSED = 0x01
HIMS_KEYRELEASED = 0x02
HIMS_CURSORROUTING = 0x00
HIMS_CODE_DEVICES = {
	1: 'Braille Sense (2 scrolls mode)',
	2: 'Braille Sense QWERTY',
	3: 'Braille EDGE',
	4: 'Braille Sense (4 scrolls mode)',
}
HIMS_BLUETOOTH_NAMES = (
	"BrailleSense",
	"BrailleEDGE",
)

#MAP OF KEYS

HIMS_KEYS = {
	0x01: 'dot1',
	0x02: 'dot2',
	0x04: 'dot3',
	0x08: 'dot4',
	0x010: 'dot5',
	0x020: 'dot6',
	0x040: 'dot7',
	0x080: 'dot8',
	0x100: 'space',
	0x40000: {'Braille EDGE': 'rightSideScrollDown', 'BrailleSense': 'rightSideScrollUp'},
	0x10000: 'leftSideScrollUp',
	0x20000: {'Braille EDGE': 'rightSideScrollUp', 'BrailleSense': 'leftSideScrollDown'},
	0x80000: {'Braille EDGE': 'leftSideScrollDown', 'BrailleSense': 'rightSideScrollDown'},
	0x200: 'advance1',
	0x400: 'advance2',
	0x800: 'advance3',
	0x1000: 'advance4',
	0x4000000: 'leftSideLeftArrow',
	0x8000000: 'leftSideRightArrow',
	0x1000000: 'leftsideUpArrow',
	0x2000000: 'leftsideDownArrow',
	0x40000000: 'rightSideLeftArrow',
	-0x80000000: 'rightSideRightArrow',
	0x10000000: 'rightsideUpArrow',
	0x20000000: 'rightSideDownArrow',
	0x100000: 'Advance5',
	0x200000: 'Advance6',
	0x400000: 'Advance7',
	0x800000: 'Advance8'
}
SPACE_KEY = 0x100

pressedKeys = set()
_ignoreKeyPresses = False
deviceFound = None

try:
	himsLib = cdll.LoadLibrary("brailleDisplayDrivers\\hims\\HanSoneConnect.dll")
except:
	himsLib = None

WNDPROC = WINFUNCTYPE(LRESULT,HWND,c_uint,WPARAM,LPARAM)

appInstance=windll.kernel32.GetModuleHandleW(None)

nvdaHIMSBrlWm=windll.user32.RegisterWindowMessageW(u"nvdaHIMSBrlWm")

@WNDPROC
def nvdaHIMSBrlWndProc(hwnd,msg,wParam,lParam):
	global pressedKeys, _ignoreKeyReleases
	if msg == nvdaHIMSBrlWm and wParam==HIMS_KEYRELEASED:
		if not _ignoreKeyReleases and pressedKeys:
			try:
				inputCore.manager.executeGesture(InputGesture(pressedKeys))
			except inputCore.NoInputGestureAction:
				pass
			_ignoreKeyReleases = True
		pressedKeys.discard(lParam)
	elif msg == nvdaHIMSBrlWm and wParam == HIMS_CURSORROUTING:
		try:
			inputCore.manager.executeGesture(InputGesture(lParam))
		except inputCore.NoInputGestureAction:
			pass
	elif msg == nvdaHIMSBrlWm and  wParam == HIMS_KEYPRESSED:
		pressedKeys.add(lParam)
		_ignoreKeyReleases = False
	return windll.user32.DefWindowProcW(hwnd,msg,wParam,lParam)

nvdaHIMSBrlWndCls = WNDCLASSEXW()
nvdaHIMSBrlWndCls.cbSize = sizeof(nvdaHIMSBrlWndCls)
nvdaHIMSBrlWndCls.lpfnWndProc = nvdaHIMSBrlWndProc
nvdaHIMSBrlWndCls.hInstance = appInstance
nvdaHIMSBrlWndCls.lpszClassName = u"nvdaHIMSBrlWndCls"

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	""" HIMS Braille Sense/Braille EDGE braille displays.
	"""
	name = "hims"
	# Translators: The name of a series of braille displays.
	description = _("HIMS Braille Sense/Braille EDGE series")

	@classmethod
	def check(cls):
		return bool(himsLib)

	def __init__(self):
		global deviceFound
		super(BrailleDisplayDriver, self).__init__()
		self._messageWindowClassAtom = windll.user32.RegisterClassExW(byref(nvdaHIMSBrlWndCls))
		self._messageWindow = windll.user32.CreateWindowExW(0,self._messageWindowClassAtom,u"nvdaHIMSBrlWndCls window",0,0,0,0,0,None,None,appInstance,None)
		code = himsLib.Open("USB",self._messageWindow,nvdaHIMSBrlWm)
		if  code == 0:
			for portInfo in sorted(hwPortUtils.listComPorts(onlyAvailable=True), key=lambda item: "bluetoothName" in item):
				port = portInfo["port"].lower()
				btName = portInfo.get("bluetoothName")
				if btName and any(btName.startswith(prefix) for prefix in HIMS_BLUETOOTH_NAMES):
					try:
						if int(port.split("com")[1]) > 8:
							port = "\\\\.\\"+port
					except (IndexError, ValueError):
						pass
					code = himsLib.Open(str(port),self._messageWindow,nvdaHIMSBrlWm)
		if code >= 1:
			deviceFound = HIMS_CODE_DEVICES[code]
			log.info("%s device found"%deviceFound)
			return
		raise RuntimeError("No display found")

	def terminate(self):
		super(BrailleDisplayDriver, self).terminate()
		himsLib.Close()
		windll.user32.DestroyWindow(self._messageWindow)
		windll.user32.UnregisterClassW(self._messageWindowClassAtom,appInstance)

	def _get_numCells(self):
		return himsLib.GetBSCellCount()

	def display(self, cells):
		cells = "".join([chr(x) for x in cells])
		himsLib.SendData(cells)

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"kb:leftAlt": ("br(hims):dot1+dot3+dot4+space",),
			"kb:capsLock": ("br(hims):dot1+dot3+dot6+space",),
			"kb:tab": ("br(hims):dot4+dot5+space",),
			"kb:shift+alt+tab": ("br(hims):advance2+advance3+advance1",),
			"kb:alt+tab": ("br(hims):advance2+advance3",),
			"kb:shift+tab": ("br(hims):dot1+dot2+space",),
			"kb:end": ("br(hims):dot4+dot6+space",),
			"kb:control+end": ("br(hims):dot4+dot5+dot6+space",),
			"kb:home": ("br(hims):dot1+dot3+space",),
			"kb:control+home": ("br(hims):dot1+dot2+dot3+space",),
			"kb:leftArrow": ("br(hims):dot3+space",),
			"kb:control+shift+leftArrow": ("br(hims):dot2+dot8+space+advance1",),
			"kb:control+leftArrow": ("br(hims):dot2+space",),
			"kb:shift+alt+leftArrow": ("br(hims):dot2+dot7+advance1",),
			"kb:alt+leftArrow": ("br(hims):dot2+dot7",),
			"kb:rightArrow": ("br(hims):dot6+space",),
			"kb:control+shift+rightArrow": ("br(hims):dot5+dot8+space+advance1",),
			"kb:control+rightArrow": ("br(hims):dot5+space",),
			"kb:shift+alt+rightArrow": ("br(hims):dot5+dot7+advance1",),
			"kb:alt+rightArrow": ("br(hims):dot5+dot7",),
			"kb:pageUp": ("br(hims):dot1+dot2+dot6+space",),
			"kb:control+pageUp": ("br(hims):dot1+dot2+dot6+dot8+space",),
			"kb:upArrow": ("br(hims):dot1+space",),
			"kb:control+shift+upArrow": ("br(hims):dot2+dot3+dot8+space+advance1",),
			"kb:control+upArrow": ("br(hims):dot2+dot3+space",),
			"kb:shift+alt+upArrow": ("br(hims):dot2+dot3+dot7+advance1",),
			"kb:alt+upArrow": ("br(hims):dot2+dot3+dot7",),
			"kb:shift+upArrow": ("br(hims):leftSideScrollDown+space",),
			"kb:pageDown": ("br(hims):dot3+dot4+dot5+space",),
			"kb:control+pageDown": ("br(hims):dot3+dot4+dot5+dot8+space",),
			"kb:downArrow": ("br(hims):dot4+space",),
			"kb:control+shift+downArrow": ("br(hims):dot5+dot6+dot8+space+advance1",),
			"kb:control+downArrow": ("br(hims):dot5+dot6+space",),
			"kb:shift+alt+downArrow": ("br(hims):dot5+dot6+dot7+advance1",),
			"kb:alt+downArrow": ("br(hims):dot5+dot6+dot7",),
			"kb:shift+downArrow": ("br(hims):space+rightSideScrollDown",),
			"kb:backspace": ("br(hims):dot7",),
			"kb:enter": ("br(hims):dot8",),
			"kb:escape": ("br(hims):dot1+dot5+space",),
			"kb:delete": ("br(hims):dot1+dot3+dot5+space",),
			"kb:f1": ("br(hims):dot1+dot2+dot5+space",),
			"kb:f3": ("br(hims):dot1+dot2+dot4+dot8",),
			"kb:f4": ("br(hims):dot7+advance3",),
			"kb:windows+b": ("br(hims):dot1+dot2+advance1",),
			"kb:windows+d": ("br(hims):dot1+dot4+dot5+advance1",),
			"braille_routeTo": ("br(hims):routing",),
			"braille_previousLine": ("br(hims):leftSideScrollUp",),
			"braille_nextLine": ("br(hims):rightSideScrollUp",),
			"braille_scrollBack": ("br(hims):leftSideScrollDown",),
			"braille_scrollForward": ("br(hims):rightSideScrollDown",),
		}
	})

class InputGesture(braille.BrailleDisplayGesture, BrailleInputGesture):
	source = BrailleDisplayDriver.name
	def __init__(self, keys):
		super(InputGesture, self).__init__()
		if isinstance(keys,int):  
			self.routingIndex = keys
			self.id = "routing"
			return
		self.keyCodes = set(keys)
		names = set()
		isBrailleInput = True
		for value in self.keyCodes: 
			if isBrailleInput:
				if 0xff & value:
					self.dots |= value
				elif value == SPACE_KEY:
					self.space = True
				else:
					# This is not braille input.
					isBrailleInput = False
					self.dots = 0
					self.space = False
			try:
				name = HIMS_KEYS[value]
				if isinstance(name, dict):
					try:
						name = name[deviceFound]
					except KeyError:
						name = name['BrailleSense']
				names.add(name)
			except KeyError:
				pass
		self.id = "+".join(names)
