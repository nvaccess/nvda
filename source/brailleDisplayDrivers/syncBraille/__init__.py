#brailleDisplayDrivers/syncBraille/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2012 Gianluca Casalino, NV Access Limited

from logHandler import log
from ctypes import *
from ctypes.wintypes import *
import braille
import inputCore
from winUser import WNDCLASSEXW, WNDPROC, LRESULT, HCURSOR

HIMS_KEYPRESSED = 0x01
HIMS_KEYRELEASED = 0x02
HIMS_CURSORROUTING = 0x00

#MAP OF KEYS

SYNCBRAILLE_KEYS = {
	4096: 'leftSideScrollUp',
	8192: 'rightSideScrollUp',
	16384: 'rightSideScrollDown',
	32768: 'leftSideScrollDown',
}

pressedKeys = set()
_ignoreKeyPresses = False

try:
	himsSyncBrailleLib = cdll.LoadLibrary("brailleDisplayDrivers\\syncBraille\\SyncBraille.dll")
except:
	himsSyncBrailleLib = None

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
	""" HIMS SyncBraille braille display.
	"""
	name = "syncBraille"
	# Translators: The name of a braille display.
	description = _("HIMS SyncBraille")

	@classmethod
	def check(cls):
		return bool(himsSyncBrailleLib)

	def __init__(self):
		super(BrailleDisplayDriver, self).__init__()
		self._messageWindowClassAtom = windll.user32.RegisterClassExW(byref(nvdaHIMSBrlWndCls))
		self._messageWindow = windll.user32.CreateWindowExW(0,self._messageWindowClassAtom,u"nvdaHIMSBrlWndCls window",0,0,0,0,0,None,None,appInstance,None)
		if himsSyncBrailleLib.OpenSyncBrl(self._messageWindow,nvdaHIMSBrlWm) == 1: return 
		raise RuntimeError("No display found")

	def terminate(self):
		super(BrailleDisplayDriver, self).terminate()
		himsSyncBrailleLib.CloseSyncBrl()
		windll.user32.DestroyWindow(self._messageWindow)
		windll.user32.UnregisterClassW(self._messageWindowClassAtom,appInstance)

	def _get_numCells(self):
		return himsSyncBrailleLib.GetCellCount()

	def display(self, cells):
		cells = "".join([chr(x) for x in cells])
		himsSyncBrailleLib.SendSyncBrl(cells)

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_routeTo": ("br(syncBraille):routing",),
			"brailleScrollBack": ("br(syncBraille):leftSideScrollDown",),
			"brailleScrollForward": ("br(syncBraille):rightSideScrollDown",),
		}
	})

class InputGesture(braille.BrailleDisplayGesture):
	source = BrailleDisplayDriver.name
	def __init__(self, keys):
		global SYNCBRAILLE_KEYS
		super(InputGesture, self).__init__()
		if isinstance(keys,int):  
			self.routingIndex = keys
			self.id = "routing"
			return
		self.keyCodes = set(keys)
		names = set()
		for value in self.keyCodes: 
			try:
				name = SYNCBRAILLE_KEYS[value]
				names.add(name)
			except:
				pass
		self.id = "+".join(names)
