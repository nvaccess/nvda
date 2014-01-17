#brailleDisplayDrivers/alvaBC6.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2009-2014 Optelec B.V., NV Access Limited

import _winreg
import itertools
import braille
import queueHandler
from logHandler import log
from ctypes import *
from ctypes.wintypes import *
import time
import config
import inputCore
import bdDetect

ALVA_RELEASE_MASK = 0x8000

ALVA_KEYS = {
	# Thumb keys (FRONT_GROUP)
	0x71: ("t1", "t2", "t3", "t4", "t5",
		# Only for BC680
		"t1", "t2", "t3", "t4", "t5"),
	# eTouch keys (ETOUCH_GROUP)
	0x72: ("etouch1", "etouch2", "etouch3", "etouch4"),
	# Smartpad keys (PDA_GROUP)
	0x73: ("sp1", "sp2", "spLeft", "spEnter", "spUp", "spDown", "spRight", "sp3", "sp4",
		# Only for BC680
		"sp1", "sp2", "spLeft", "spEnter", "spUp", "spDown", "spRight", "sp3", "sp4")
}
ALVA_CR_GROUP = 0x74
ALVA_MODIFIER_GROUP = 0x75
ALVA_ASCII_GROUP = 0x76

ALVA_PKEYCALLBACK = CFUNCTYPE(BOOL, c_int, USHORT, c_void_p)

#Try to load alvaw32.dll
try:
	AlvaLib=windll[r"brailleDisplayDrivers\alvaw32.dll"]
except:
	AlvaLib=None

def _getUsbPaths(usbId):
	try:
		rootKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\HID")
	except WindowsError:
		return
	with rootKey:
		for index in itertools.count():
			try:
				devKeyName = _winreg.EnumKey(rootKey, index)
			except WindowsError:
				break
			if not devKeyName.startswith(usbId):
				continue
			with _winreg.OpenKey(rootKey, devKeyName) as devKey:
				for index in itertools.count():
					try:
						instKeyName = _winreg.EnumKey(devKey, index)
					except WindowsError:
						break
					yield str(r"\\?\hid#%s#%s#{4d1e55b2-f16f-11cf-88cb-001111000030}" % (
						devKeyName, instKeyName))

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "alvaBC6"
	# Translators: The name of a braille display.
	description = _("ALVA BC640/680 series")

	@classmethod
	def check(cls):
		return bool(AlvaLib) and bdDetect.arePossibleDevicesForDriver(cls.name)

	def __init__(self, port=None):
		super(BrailleDisplayDriver,self).__init__()
		AlvaLib.AlvaInit()
		devNum = c_int()
		found = False
		if isinstance(port, bdDetect.UsbDeviceMatch):
			for path in _getUsbPaths(port.id):
				found = AlvaLib.AlvaOpenKnown(1, path, byref(devNum)) == 0
				if found:
					break
		elif isinstance(port, bdDetect.BluetoothComPortMatch):
			found = AlvaLib.AlvaOpenKnown(2, port.port.encode("mbcs"), byref(devNum)) == 0
		if not found:
			raise RuntimeError("No ALVA display found")
		self._devNum = devNum.value
		self._alva_NumCells = 0
		self._keysDown = set()
		self._ignoreKeyReleases = False
		self._keyCallbackInst = ALVA_PKEYCALLBACK(self._keyCallback)
		AlvaLib.AlvaSetKeyCallback(devNum, self._keyCallbackInst, None)

	def terminate(self):
		global AlvaLib
		super(BrailleDisplayDriver, self).terminate()
		AlvaLib.AlvaClose(self._devNum)
		# Drop the ctypes function instance for the key callback,
		# as it is holding a reference to an instance method, which causes a reference cycle.
		self._keyCallbackInst = None
		# HACK: If we connected to Bluetooth first,
		# AlvaOpenKnown subsequently always opens Bluetooth even if we ask for USB.
		# Therefore, completely unload and reload the ALVA library.
		windll.kernel32.FreeLibrary(AlvaLib._handle)
		delattr(windll, AlvaLib._name)
		AlvaLib = windll[AlvaLib._name]

	def _get_numCells(self):
		if self._alva_NumCells==0:
			NumCells = c_int(0)
			AlvaLib.AlvaGetCells(self._devNum, byref(NumCells))
			if NumCells.value==0:
				raise RuntimeError("Cannot obtain number of cells")
			self._alva_NumCells = NumCells.value
			log.info("ALVA BC6xx has %d cells" %self._alva_NumCells)
		return self._alva_NumCells

	def display(self, cells):
		cells="".join([chr(x) for x in cells])
		res = AlvaLib.AlvaSendBraille(self._devNum, cells, 0, len(cells))
		if res != 0:
			raise RuntimeError("Error sending braille: %d" % res)

	def _keyCallback(self, dev, key, userData):
		group = (key >> 8) & 0x7F
		number = key & 0xFF
		if key & ALVA_RELEASE_MASK:
			# Release.
			if not self._ignoreKeyReleases and self._keysDown:
				try:
					inputCore.manager.executeGesture(InputGesture(self._keysDown))
				except inputCore.NoInputGestureAction:
					pass
				# Any further releases are just the rest of the keys in the combination being released,
				# so they should be ignored.
				self._ignoreKeyReleases = True
			self._keysDown.discard((group, number))
		else:
			# Press.
			if group == ALVA_CR_GROUP:
				# Execute routing keys when pressed instead of released.
				try:
					inputCore.manager.executeGesture(InputGesture(((group, number),)))
				except inputCore.NoInputGestureAction:
					pass
			else:
				self._keysDown.add((group, number))
				# This begins a new key combination.
				self._ignoreKeyReleases = False
		return False

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(alvaBC6):t1",),
			"braille_previousLine": ("br(alvaBC6):t2",),
			"braille_nextLine": ("br(alvaBC6):t4",),
			"braille_scrollForward": ("br(alvaBC6):t5",),
			"braille_routeTo": ("br(alvaBC6):routing",),
			"kb:shift+tab": ("br(alvaBC6):sp1",),
			"kb:alt": ("br(alvaBC6):sp2",),
			"kb:escape": ("br(alvaBC6):sp3",),
			"kb:tab": ("br(alvaBC6):sp4",),
			"kb:upArrow": ("br(alvaBC6):spUp",),
			"kb:downArrow": ("br(alvaBC6):spDown",),
			"kb:leftArrow": ("br(alvaBC6):spLeft",),
			"kb:rightArrow": ("br(alvaBC6):spRight",),
			"kb:enter": ("br(alvaBC6):spEnter",),
			"showGui": ("br(alvaBC6):sp1+sp3",),
			"kb:windows+d": ("br(alvaBC6):sp1+sp4",),
			"kb:windows": ("br(alvaBC6):sp2+sp3",),
			"kb:alt+tab": ("br(alvaBC6):sp2+sp4",),
		}
	})

class InputGesture(braille.BrailleDisplayGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, keys):
		super(InputGesture, self).__init__()
		self.keyCodes = set(keys)

		self.keyNames = names = set()
		for group, number in self.keyCodes:
			if group == ALVA_CR_GROUP:
				names.add("routing")
				self.routingIndex = number
			else:
				try:
					names.add(ALVA_KEYS[group][number])
				except (KeyError, IndexError):
					log.debugWarning("Unknown key with group %d and number %d" % (group, number))

		self.id = "+".join(names)
