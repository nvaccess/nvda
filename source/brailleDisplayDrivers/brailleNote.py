#brailleDisplayDrivers/brailleNote.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
# Copyright (C) 2011-2016 NV access Limited, Rui Batista, Joseph Lee

""" Braille Display driver for the BrailleNote notetakers in terminal mode.
USB, serial and bluetooth communications are supported.
QWERTY keyboard input and scroll weels support in progress.
"""
from collections import OrderedDict
import itertools
import serial
import wx
import braille
import brailleInput
import hwPortUtils
import inputCore
from logHandler import log

BLUETOOTH_NAMES = ("Braillenote",)
BLUETOOTH_ADDRS = (
	# (first, last),
	(0x0025EC000000, 0x0025EC01869F), # Apex
)
USB_IDS = frozenset((
	"VID_1C71&PID_C004", # Apex
	))

BAUD_RATE = 38400
TIMEOUT = 0.1
READ_INTERVAL = 50

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

DESCRIBE_TAG = "\x1B?"
DISPLAY_TAG = "\x1bB"
ESCAPE = '\x1b'

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
_scrWheel = ("wcounterclockwise", "wclockwise", "wup", "wdown", "wleft", "wright", "wcenter")

# Dots:
# Backspace is dot7 and enter dot8
_dotNames = {}
for i in xrange(1,9):
	key = globals()["DOT_%d" % i]
	_dotNames[key] = "d%d" % i

# QT keys
_qtKeyNames={
	QT_FN : "qfunction",
	QT_SHIFT : "qshift",
	QT_CTRL : "qctrl",
	QT_READ : "qread"
}

# QT uses various ASCII characters for special keys.
_qtKeys= {
	8:"backspace",
	9:"tab",
	13:"enter",
	32:"space",
	37:"leftArrow",
	38:"upArrow",
39:"rightArrow",
40:"downArrow",
}

def _getQTKeys(key):
	if key in _qtKeys:
		return _qtKeys[key]
	elif 65 <= key <= 90:
		return chr(key)


class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "brailleNote"
	# Translators: Names of braille displays
	description = _("HumanWare BrailleNote")

	@classmethod
	def check(cls):
		return True

	@classmethod
	def _getUSBPorts(cls):
		return (p["port"] for p in hwPortUtils.listComPorts()
				if p["hardwareID"].startswith("USB\\") and any(p["hardwareID"][4:].startswith(id) for id in USB_IDS))

	@classmethod
	def _getBluetoothPorts(cls):
		for p in hwPortUtils.listComPorts():
			try:
				addr = p["bluetoothAddress"]
				name = p["bluetoothName"]
			except KeyError:
				continue
			if (any(first <= addr <= last for first, last in BLUETOOTH_ADDRS)
					or any(name.startswith(prefix) for prefix in BLUETOOTH_NAMES)):
				yield p["port"]

	@classmethod
	def getPossiblePorts(cls):
		ports = OrderedDict()
		usb = bluetooth = False
		# See if we have any USB ports available:
		try:
			cls._getUSBPorts().next()
			usb = True
		except StopIteration:
			pass
		# See if we have any bluetooth ports available:
		try:
			cls._getBluetoothPorts().next()
			bluetooth = True
		except StopIteration:
			pass
		if usb or bluetooth:
			ports.update([cls.AUTOMATIC_PORT])
		if usb:
			ports["usb"] = "USB"
		if bluetooth:
			ports["bluetooth"] = "Bluetooth"
		for p in hwPortUtils.listComPorts():
			# Translators: Name of a serial communications port
			ports[p["port"]] = _("Serial: {portName}").format(portName=p["friendlyName"])
		return ports

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver, self).__init__()
		self._serial = None
		self._buffer = ""
		if port == "auto":
			portsToTry = itertools.chain(self._getUSBPorts(), self._getBluetoothPorts())
		elif port == "usb":
			portsToTry = self._getUSBPorts()
		elif port == "bluetooth":
			portsToTry = self._getBluetoothPorts()
		else:
			portsToTry = (port,)
		found = False
		for port in portsToTry:
			log.debug("Checking port %s for a BrailleNote", port)
			try:
				self._serial = serial.Serial(port, baudrate=BAUD_RATE, timeout=TIMEOUT, writeTimeout=TIMEOUT, parity=serial.PARITY_NONE)
			except serial.SerialException:
				continue
			# Check for cell information
			if self._describe():
				log.debug("BrailleNote found on %s with %d cells", port, self.numCells)
				found = True
				break
			else:
				self._serial.close()
		if not found:
			raise RuntimeError("Can't find a braillenote device (port = %s)" % port)
		# start reading keys
		self._readTimer = wx.PyTimer(self._readKeys)
		self._readTimer.Start(READ_INTERVAL)

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
			self._readTimer.Stop()
			self._readTimer = None
		finally:
			self._closeComPort()

	def _closeComPort(self):
		if self._readTimer is not None:
			self._readTimer.Stop()
			self._readTimer = None
		if self._serial is not None:
			log.debug("Closing port %s", self._serial.port)
			self._serial.close()
			self._serial = None

	def _describe(self):
		log.debug("Writing sdescribe tag")
		self._serial.write(DESCRIBE_TAG)
		# This seems always able to read the three bytes, but if someone complain it might be better to retry
		packet = self._serial.read(3)
		log.debug("Read %d bytes", len(packet))
		if len(packet) != 3 or packet[0] != chr(STATUS_TAG):
			log.debug("Not a braillenote")
			return False
		self._numCells = ord(packet[2])
		return True

	def _get_numCells(self):
		return self._numCells

	def _readKeys(self):
		try:
			while self._serial is not None and self._serial.inWaiting():
				command, arg = self._readPacket()
				if command:
					# BrailleNote QT sends another two bytes to let the receiver know it is a QT letter.
					letter = self._readPacket()[1] if command == QT_MOD_TAG else None
					self._dispatch(command, arg, data=letter)
		except serial.SerialException:
			self._closeComPort()
			# Reraise to be logged
			raise

	def _readPacket(self):
		self._buffer += self._serial.read(2 - len(self._buffer))
		if len(self._buffer) < 2:
			return None, None
		command, arg = ord(self._buffer[0]), ord(self._buffer[1])
		self._buffer = ""
		return command, arg

	# Data is invoked if we're dealing with a BrailleNote QT.
	def _dispatch(self, command, arg, data=None):
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
		elif command == QT_MOD_TAG and data is not None:
			# BrailleNote QT.
			gesture = InputGesture(qtMod=arg, qtData=data)
		else:
			log.debugWarning("Unknown command")
			return
		try:
			inputCore.manager.executeGesture(gesture)
		except inputCore.NoInputGestureAction:
			pass

	def display(self, cells):
		# if the serial port is not open don't even try to write
		if self._serial is None:
			return
		# ESCAPE must be quoted because it is a control character
		cells = [chr(cell).replace(ESCAPE, ESCAPE * 2) for cell in cells]
		try:
			self._serial.write(DISPLAY_TAG + "".join(cells))
		except serial.SerialException, e:
			self._closeComPort()
			raise

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(braillenote):tback",),
			"braille_scrollForward": ("br(braillenote):tadvance",),
			"braille_previousLine": ("br(braillenote):tprevious",),
			"braille_nextLine": ("br(braillenote):tnext",),
			"braille_routeTo": ("br(braillenote):routing",),
			"braille_toggleTether": ("br(braillenote):tprevious+tnext",),
			"kb:upArrow": ("br(braillenote):space+d1",),
			"kb:upArrow": ("br(braillenote):wup",),
			"kb:upArrow": ("br(braillenote):upArrow",),
			"kb:downArrow": ("br(braillenote):space+d4",),
			"kb:downArrow": ("br(braillenote):wdown",),
			"kb:downArrow": ("br(braillenote):downArrow",),
			"kb:leftArrow": ("br(braillenote):space+d3",),
			"kb:leftArrow": ("br(braillenote):wleft",),
			"kb:leftArrow": ("br(braillenote):leftArrow",),
			"kb:rightArrow": ("br(braillenote):space+d6",),
			"kb:rightArrow": ("br(braillenote):wright",),
			"kb:rightArrow": ("br(braillenote):rightArrow",),
			"kb:pageup": ("br(braillenote):space+d1+d3",),
			"kb:pageup": ("br(braillenote):qfunction+upArrow",),
			"kb:pagedown": ("br(braillenote):space+d4+d6",),
			"kb:pagedown": ("br(braillenote):qfunction+downArrow",),
			"kb:home": ("br(braillenote):space+d1+d2",),
			"kb:home": ("br(braillenote):qfunction+leftArrow",),
			"kb:end": ("br(braillenote):space+d4+d5",),
			"kb:end": ("br(braillenote):qfunction+rightArrow",),
			"kb:control+home": ("br(braillenote):space+d1+d2+d3",),
			"kb:control+home": ("br(braillenote):qread+T",),
			"kb:control+end": ("br(braillenote):space+d4+d5+d6",),
			"kb:control+end": ("br(braillenote):qread+B",),
			"kb:enter": ("br(braillenote):space+d8",),
			"kb:enter": ("br(braillenote):wcenter",),
			"kb:enter": ("br(braillenote):enter",),
			"kb:shift+tab": ("br(braillenote):space+d1+d2+d5+d6",),
			"kb:shift+tab": ("br(braillenote):wcounterclockwise",),
			"kb:shift+tab": ("br(braillenote):qshift+tab",),
			"kb:tab": ("br(braillenote):space+d2+d3+d4+d5",),
			"kb:tab": ("br(braillenote):wclockwise",),
			"kb:tab": ("br(braillenote):tab",),
			"kb:backspace": ("br(braillenote):space+d7",),
			"kb:backspace": ("br(braillenote):backspace",),
			"showGui": ("br(braillenote):space+d1+d3+d4+d5",),
			"showGui": ("br(braillenote):qread+N",),
			"kb:windows": ("br(braillenote):space+d2+d4+d5+d6",),
			"kb:windows": ("br(braillenote):qread+W",),
			"kb:alt": ("br(braillenote):space+d1+d3+d4",),
			"kb:alt": ("br(braillenote):qread+M",),
			"toggleInputHelp": ("br(braillenote):space+d2+d3+d6",),
			"toggleInputHelp": ("br(braillenote):qread+1",),
		},
	})

class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, keys=None, dots=None, space=False, routing=None, wheel=None, qtData=None, qtMod=None):
		super(braille.BrailleDisplayGesture, self).__init__()
		# Handle thumb-keys and scroll wheel (wheel is for Apex BT).
		names = set()
		if keys is not None:
			names.update(_keyNames[1 << i] for i in xrange(4) if (1 << i) & keys)
		if wheel is not None:
			names.add(_scrWheel[wheel])
		elif dots is not None:
		# now the dots
			self.dots = dots
			if space:
				self.space = space
				names.add(_keyNames[0])
			names.update(_dotNames[1 << i] for i in xrange(8) if (1 << i) & dots)
		elif routing is not None:
			self.routingIndex = routing
			names.add('routing')
		elif qtMod is not None and qtData is not None:
			names.update(_qtKeyNames[1 << i] for i in xrange(4) if (1 << i) & qtMod)
		# Make sure to display QT identifiers in mod+char format if this is such a case.
		if qtData is None:
			self.id = "+".join(names)
		else:
			print qtData
			self.id = _getQTKeys(qtData) if qtMod == 0 else "+".join(("+".join(names), _getQTKeys(qtData)))