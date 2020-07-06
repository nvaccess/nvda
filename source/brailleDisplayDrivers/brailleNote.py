#brailleDisplayDrivers/brailleNote.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
# Copyright (C) 2011-2018 NV access Limited, Rui Batista, Joseph Lee

""" Braille Display driver for the BrailleNote notetakers in terminal mode.
USB, serial and bluetooth communications are supported.
QWERTY keyboard input using basic terminal mode (no PC keyboard emulation) and scroll wheel are supported.
See Brailliant B module for BrailleNote Touch support routines.
"""

from typing import List, Optional

import serial
import braille
import brailleInput
import inputCore
from logHandler import log
import hwIo
from hwIo import intToByte

BAUD_RATE = 38400
TIMEOUT = 0.1

# Tags sent by the BrailleNote
# Combinations of dots 1...6
DOTS_TAG = 0x80
# combinations of dots 1...6 plus the space bar
DOTS_SPACE_TAG = 0x81
# Combinations of dots 1..6 plus space bar and backspace
DOTS_BACKSPACE_TAG = 0x82
# Combinations of dots 1..6 plus space bar and enter
DOTS_ENTER_TAG = 0x83
# Combinations of one or two Thumb keys
THUMB_KEYS_TAG = 0x84
# Cursor Routing keys
CURSOR_KEY_TAG = 0x85
# Status
STATUS_TAG = 0x86
# Scroll Wheel (Apex BT)
SCROLL_WHEEL_TAG = 0x8B
# QWERTY keyboard
QT_LETTER_TAG = 0x8C
QT_MOD_TAG = 0x8D
QT_LETTER = 0x0
QT_FN = 0x1
QT_SHIFT = 0x2
QT_CTRL = 0x4
QT_READ = 0x8 #Alt key

ESCAPE = b'\x1b'
DESCRIBE_TAG = ESCAPE + b"?"
DISPLAY_TAG = ESCAPE + b"B"

# Dots
DOT_1 = 0x1
DOT_2 = 0x2
DOT_3 = 0x4
DOT_4 = 0x8
DOT_5 = 0x10
DOT_6 = 0x20
DOT_7 = 0x40
DOT_8 = 0x80

# Thumb-keys
THUMB_PREVIOUS = 0x01
THUMB_BACK = 0x02
THUMB_ADVANCE = 0x04
THUMB_NEXT = 0x08

_keyNames = {
	THUMB_PREVIOUS : "tprevious",
	THUMB_BACK : "tback",
	THUMB_ADVANCE : "tadvance",
	THUMB_NEXT : "tnext",
	0 : "space"
}

# Scroll wheel components (Apex BT)
_scrWheel = ("wCounterclockwise", "wClockwise", "wUp", "wDown", "wLeft", "wRight", "wCenter")

# Dots:
# Backspace is dot7 and enter dot8
_dotNames = {}
for i in range(1,9):
	key = globals()["DOT_%d" % i]
	_dotNames[key] = "d%d" % i

# QT keys
_qtKeyNames={
	QT_FN : "function",
	QT_SHIFT : "shift",
	QT_CTRL : "ctrl",
	QT_READ : "read"
}

# QT uses various ASCII characters for special keys, akin to scancodes.
_qtKeys= {
	8:"backspace",
	9:"tab",
	13:"enter",
	32:"space",
	37:"leftArrow",
	38:"upArrow",
	39:"rightArrow",
	40:"downArrow",
	46:"delete",
	186:"semi",
	187:"equals",
	188:"comma",
	189:"dash",
	190:"dot",
	191:"slash",
	192:"grave",
	219:"leftBracket",
	220:"backslash",
	221:"rightBracket",
	222:"tick",
}


class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "brailleNote"
	# Translators: Names of braille displays
	description = _("HumanWare BrailleNote")
	isThreadSafe = True

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver, self).__init__()
		self._serial = None
		for portType, portId, port, portInfo in self._getTryPorts(port):
			log.debug("Checking port %s for a BrailleNote", port)
			try:
				self._serial = hwIo.Serial(port, baudrate=BAUD_RATE, timeout=TIMEOUT, writeTimeout=TIMEOUT, parity=serial.PARITY_NONE, onReceive=self._onReceive)
			except EnvironmentError:
				log.debugWarning("", exc_info=True)
				continue
			# Check for cell information
			if self._describe():
				log.debug("BrailleNote found on %s with %d cells", port, self.numCells)
				break
			else:
				self._serial.close()
		else:
			raise RuntimeError("Can't find a braillenote device (port = %s)" % port)

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
		finally:
			self._serial.close()
			self._serial = None

	def _describe(self):
		self.numCells = 0
		log.debug("Writing describe tag")
		self._serial.write(DESCRIBE_TAG)
		self._serial.waitForRead(TIMEOUT)
		# If a valid response was received, _onReceive will have set numCells.
		if self.numCells:
			return True
		log.debug("Not a braillenote")
		return False

	def _onReceive(self, command: bytes):
		assert len(command) == 1
		command: int = ord(command)
		if command == STATUS_TAG:
			arg = self._serial.read(2)
			self.numCells = arg[1]
			return
		arg = self._serial.read(1)
		if not arg:
			log.debugWarning("Timeout reading argument for command 0x%X" % command)
			return
		# #5993: Read the buffer once more if a BrailleNote QT says it's got characters in its pipeline.
		if command == QT_MOD_TAG:
			commandKey: int = self._serial.read(2)[-1]
			arg2 = _qtKeys.get(commandKey, str(commandKey))
		else:
			arg2 = None
		self._dispatch(command, ord(arg), arg2)

	def _dispatch(
			self,
			command: int,
			arg: int,
			arg2: Optional[str] = None
	):
		space = False
		if command == THUMB_KEYS_TAG:
			gesture = InputGesture(keys=arg)
		elif command == SCROLL_WHEEL_TAG:
			gesture = InputGesture(wheel=arg)
		elif command == CURSOR_KEY_TAG:
			gesture = InputGesture(routing=arg)
		elif command in (DOTS_TAG, DOTS_SPACE_TAG, DOTS_ENTER_TAG, DOTS_BACKSPACE_TAG):
			if command != DOTS_TAG:
				space = True
			if command == DOTS_ENTER_TAG:
				# Stupid bug in the implementation
				# Force dot8 here, although it should be already there
				arg |= DOT_8
			gesture = InputGesture(dots=arg, space=space)
		elif command == QT_MOD_TAG:
			# BrailleNote QT
			gesture = InputGesture(qtMod=arg, qtData=arg2)
		else:
			log.debugWarning("Unknown command")
			return
		try:
			inputCore.manager.executeGesture(gesture)
		except inputCore.NoInputGestureAction:
			pass

	def display(self, cells: List[int]):
		# ESCAPE must be quoted because it is a control character
		cellBytesList = [intToByte(cell).replace(ESCAPE, ESCAPE * 2) for cell in cells]
		cellBytesList.insert(0, DISPLAY_TAG)
		self._serial.write(b"".join(cellBytesList))

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(braillenote):tback",),
			"braille_scrollForward": ("br(braillenote):tadvance",),
			"braille_previousLine": ("br(braillenote):tprevious",),
			"braille_nextLine": ("br(braillenote):tnext",),
			"braille_routeTo": ("br(braillenote):routing",),
			"braille_toggleTether": ("br(braillenote):tprevious+tnext",),
			"kb:upArrow": ("br(braillenote):space+d1", "br(braillenote):wUp", "br(braillenote):upArrow",),
			"kb:downArrow": ("br(braillenote):space+d4", "br(braillenote):wDown","br(braillenote):downArrow",),
			"kb:leftArrow": ("br(braillenote):space+d3","br(braillenote):wLeft","br(braillenote):leftArrow",),
			"kb:rightArrow": ("br(braillenote):space+d6","br(braillenote):wRight","br(braillenote):rightArrow",),
			"kb:pageup": ("br(braillenote):space+d1+d3","br(braillenote):function+upArrow",),
			"kb:pagedown": ("br(braillenote):space+d4+d6","br(braillenote):function+downArrow",),
			"kb:home": ("br(braillenote):space+d1+d2","br(braillenote):function+leftArrow",),
			"kb:end": ("br(braillenote):space+d4+d5","br(braillenote):function+rightArrow",),
			"kb:control+home": ("br(braillenote):space+d1+d2+d3","br(braillenote):read+T",),
			"kb:control+end": ("br(braillenote):space+d4+d5+d6","br(braillenote):read+B",),
			"braille_enter": ("br(braillenote):space+d8","br(braillenote):wCenter","br(braillenote):enter",),
			"kb:shift+tab": ("br(braillenote):space+d1+d2+d5+d6","br(braillenote):wCounterclockwise","br(braillenote):shift+tab",),
			"kb:tab": ("br(braillenote):space+d2+d3+d4+d5","br(braillenote):wClockwise","br(braillenote):tab",),
			"braille_eraseLastCell": ("br(braillenote):space+d7","br(braillenote):backspace",),
			"showGui": ("br(braillenote):space+d1+d3+d4+d5","br(braillenote):read+N",),
			"kb:windows": ("br(braillenote):space+d2+d4+d5+d6","br(braillenote):read+W",),
			"kb:alt": ("br(braillenote):space+d1+d3+d4","br(braillenote):read+M",),
			"toggleInputHelp": ("br(braillenote):space+d2+d3+d6","br(braillenote):read+1",),
		},
	})

class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):
	source = BrailleDisplayDriver.name

	def __init__(
			self,
			keys: Optional[int] = None,
			dots: Optional[int] = None,
			space: bool = False,
			routing: Optional[int] = None,
			wheel: Optional[int] = None,
			qtMod: Optional[int] = None,
			qtData:Optional[str] = None
	):
		super(braille.BrailleDisplayGesture, self).__init__()
		# Denotes if we're dealing with a QT model.
		self.qt = qtMod is not None
		# Handle thumb-keys and scroll wheel (wheel is for Apex BT).
		names = set()
		if keys is not None:
			names.update(_keyNames[1 << i] for i in range(4) if (1 << i) & keys)
		elif wheel is not None:
			names.add(_scrWheel[wheel])
		elif dots is not None:
			self.dots = dots
			if space:
				self.space = space
				names.add(_keyNames[0])
			names.update(_dotNames[1 << i] for i in range(8) if (1 << i) & dots)
		elif routing is not None:
			self.routingIndex = routing
			names.add('routing')
		elif qtMod is not None:
			names.update(
				_qtKeyNames[1 << i] for i in range(4)
				if (1 << i) & qtMod
			)
			names.add(qtData)
		self.id = "+".join(names)
