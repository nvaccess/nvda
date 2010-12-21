#brailleDisplayDrivers/alvaBC6.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2009-2010 Optelec B.V. <http://www.optelec.com/>, James Teh <jamie@jantrid.net>

import braille
import queueHandler
from logHandler import log
from ctypes import *
from ctypes.wintypes import *
import time
import config
from keyboardHandler import KeyboardInputGesture
import inputCore

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

class BrailleDisplayDriver(braille.BrailleDisplayDriverWithCursor):
	name = "alvaBC6"
	description = _("ALVA BC640/680 series")

	@classmethod
	def check(cls):
		if AlvaLib:
			log.info("Alva library was loaded")
		else:
			log.info("Alva library was not loaded")

		return bool(AlvaLib)

	def __init__(self):
		super(BrailleDisplayDriver,self).__init__()
		log.debug("ALVA BC6xx Braille init")
		_AlvaNumDevices=c_int(0)
		AlvaLib.AlvaScanDevices(byref(_AlvaNumDevices))
		if _AlvaNumDevices.value==0:
			raise RuntimeError("No ALVA display found")
		log.info("%d devices found" %_AlvaNumDevices.value)
		AlvaLib.AlvaOpen(0)
		self._alva_NumCells = 0
		self._keysDown = set()
		self._keyCallback = ALVA_PKEYCALLBACK(self._keyCallback)
		AlvaLib.AlvaSetKeyCallback(0, self._keyCallback, None)

	def terminate(self):
		super(BrailleDisplayDriver, self).terminate()
		AlvaLib.AlvaClose(1)

	def _get_numCells(self):
		if self._alva_NumCells==0:
			NumCells = c_int(0)
			AlvaLib.AlvaGetCells(0, byref(NumCells))
			if NumCells.value==0:
				raise RuntimeError("Cannot obtain number of cells")
			self._alva_NumCells = NumCells.value
			log.info("ALVA BC6xx has %d cells" %self._alva_NumCells)
		return self._alva_NumCells

	def _display(self, cells):
		#log.info("Display %d cells" %len(cells))
		cells="".join([chr(x) for x in cells])
		AlvaLib.AlvaSendBraille(0, cells, 0, len(cells))

	def _keyCallback(self, dev, key, userData):
		group = (key >> 8) & 0xFF
		number = key & 0xFF
		if key & ALVA_RELEASE_MASK:
			# The key is being released.
			if self._keysDown:
				try:
					inputCore.manager.executeGesture(InputGesture(self._keysDown))
				except inputCore.NoInputGestureAction:
					pass
				self._keysDown.clear()
		else:
			if group == ALVA_CR_GROUP:
				try:
					inputCore.manager.executeGesture(InputGesture(((group, number),)))
				except inputCore.NoInputGestureAction:
					pass
			else:
				self._keysDown.add((group, number))
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
