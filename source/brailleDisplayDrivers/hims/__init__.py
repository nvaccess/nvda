#brailleDisplayDrivers/hims/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2012 Gianluca Casalino <gianluca@spazioausili.net>

from logHandler import log
from ctypes import *
from ctypes.wintypes import *
import braille
import inputCore
from winUser import WNDCLASSEXW, WNDPROC, LRESULT, HCURSOR
import hwPortUtils

HIMS_KEYPRESSED = 0x01
HIMS_KEYRELEASED = 0x02
HIMS_CURSORROUTING = 0x00
HIMS_CODE_DEVICES = {
	1: 'Braille Sense (2 scrools mode)',
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
	0x01: 'Dot1',
	0x02: 'Dot2',
	0x04: 'Dot3',
	0x08: 'Dot4',
	0x010: 'Dot5',
	0x020: 'Dot6',
	0x040: 'Dot7',
	0x080: 'Dot8',
	0x100: 'space',
	0x40000: {'Braille EDGE': 'right_side_scroll_down', 'BrailleSense': 'right_side_scroll_up'},
	0x10000: 'left_side_scroll_up',
	0x20000: {'Braille EDGE': 'right_side_scroll_up', 'BrailleSense': 'left_side_scroll_down'},
	0x80000: {'Braille EDGE': 'left_side_scroll_down', 'BrailleSense': 'right_side_scroll_down'},
	0x200: 'advance 1',
	0x400: 'advance 2',
	0x800: 'advance 3',
	0x1000: 'advance 4',
	0x4000000: 'left_side_left_arrow',
	0x8000000: 'left_side_right_arrow',
	0x1000000: 'left_side_up_arrow',
	0x2000000: 'left_side_down_arrow',
	0x40000000: 'right_side_left_arrow',
	-0x80000000: 'right_side_right_arrow',
	0x10000000: 'right_side_up_arrow',
	0x20000000: 'right_side_down_arrow',
	0x100000: 'Advance 5',
	0x200000: 'Advance 6',
	0x400000: 'Advance 7',
	0x800000: 'Advance 8'
}

pressedKeys = set()
_ignoreKeyPresses = False
deviceFound = None

try:
	himsLib = cdll.LoadLibrary("brailleDisplayDrivers\\HanSoneConnect.dll")
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
					if int(port.split("com")[1]) > 8: port = "\\\\.\\"+port
					code = himsLib.Open(str(port),self._messageWindow,nvdaHIMSBrlWm)
		if code >= 1:
			deviceFound = HIMS_CODE_DEVICES[code]
			log.info(_("%s device found")%deviceFound)
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
			"kb:leftAlt": ("br(hims):Dot1+Dot3+Dot4+space",),
			"kb:capsLock": ("br(hims):Dot1+Dot3+Dot6+space",),
			"kb:tab": ("br(hims):Dot4+Dot5+space",),
			"kb:shift+alt+tab": ("br(hims):advance2+advance3+advance1",),
			"kb:alt+tab": ("br(hims):advance2+advance3",),
			"kb:shift+tab": ("br(hims):Dot1+Dot2+space",),
			"kb:end": ("br(hims):Dot4+Dot6+space",),
			"kb:control+end": ("br(hims):Dot4+Dot5+dot6+space",),
			"kb:home": ("br(hims):Dot1+Dot3+space",),
			"kb:control+home": ("br(hims):Dot1+Dot2+dot3+space",),
			"kb:leftArrow": ("br(hims):Dot3+space",),
			"kb:control+shift+leftArrow": ("br(hims):Dot2+Dot8+space+advance1",),
			"kb:control+leftArrow": ("br(hims):Dot2+space",),
			"kb:shift+alt+leftArrow": ("br(hims):Dot2+Dot7+advance1",),
			"kb:alt+leftArrow": ("br(hims):Dot2+Dot7",),
			"kb:rightArrow": ("br(hims):Dot6+space",),
			"kb:control+shift+rightArrow": ("br(hims):Dot5+Dot8+space+advance1",),
			"kb:control+rightArrow": ("br(hims):Dot5+space",),
			"kb:shift+alt+rightArrow": ("br(hims):Dot5+Dot7+advance1",),
			"kb:alt+rightArrow": ("br(hims):Dot5+Dot7",),
			"kb:pageUp": ("br(hims):Dot1+Dot2+Dot6+space",),
			"kb:control+pageUp": ("br(hims):Dot1+Dot2+Dot6+Dot8+space",),
			"kb:upArrow": ("br(hims):Dot1+space",),
			"kb:control+shift+upArrow": ("br(hims):Dot2+Dot3+Dot8+space+advance1",),
			"kb:control+upArrow": ("br(hims):Dot2+Dot3+space",),
			"kb:shift+alt+upArrow": ("br(hims):Dot2+Dot3+Dot7+advance1",),
			"kb:alt+upArrow": ("br(hims):Dot2+Dot3+Dot7",),
			"kb:shift+upArrow": ("br(hims):left_side_scroll_down+space",),
			"kb:pageDown": ("br(hims):Dot3+Dot4+Dot5+space",),
			"kb:control+pageDown": ("br(hims):Dot3+Dot4+Dot5+Dot8+space",),
			"kb:downArrow": ("br(hims):Dot4+space",),
			"kb:control+shift+downArrow": ("br(hims):Dot5+Dot6+Dot8+space+advance1",),
			"kb:control+downArrow": ("br(hims):Dot5+Dot6+space",),
			"kb:shift+alt+downArrow": ("br(hims):Dot5+Dot6+Dot7+advance1",),
			"kb:alt+downArrow": ("br(hims):Dot5+Dot6+Dot7",),
			"kb:shift+downArrow": ("br(hims):space+right_side_scroll_down",),
			"kb:backspace": ("br(hims):Dot7",),
			"kb:enter": ("br(hims):Dot8",),
			"kb:escape": ("br(hims):Dot1+Dot5+space",),
			"kb:delete": ("br(hims):Dot1+Dot3+Dot5+space",),
			"kb:f1": ("br(hims):Dot1+Dot2+Dot5+space",),
			"kb:f3": ("br(hims):Dot1+Dot2+Dot4+Dot8",),
			"kb:f4": ("br(hims):Dot7+advance3",),
			"kb:windows+b": ("br(hims):Dot1+Dot2+advance1",),
			"kb:windows+d": ("br(hims):Dot1+Dot4+Dot5+advance1",),
			"braille_routeTo": ("br(hims):routing",),
			"braille_previousLine": ("br(hims):left_side_scroll_up",),
			"braille_nextLine": ("br(hims):right_side_scroll_up",),
			"braille_scrollBack": ("br(hims):left_side_scroll_down",),
			"braille_scrollForward": ("br(hims):right_side_scroll_down",),
		}
	})

class InputGesture(braille.BrailleDisplayGesture):
	source = BrailleDisplayDriver.name
	def __init__(self, keys):
		global HIMS_KEYS
		super(InputGesture, self).__init__()
		if isinstance(keys,int):  
			self.routingIndex = keys
			self.id = "routing"
			return
		self.keyCodes = set(keys)
		names = set()
		for value in self.keyCodes: 
			try:
				if type(HIMS_KEYS[value]) == dict: 
					name = (HIMS_KEYS[value][deviceFound] if deviceFound in HIMS_KEYS[value].keys() else HIMS_KEYS[value]['BrailleSense'])
				else:
					name = HIMS_KEYS[value]
				names.add(name)
			except:
				pass
		self.id = "+".join(names)
