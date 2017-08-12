# -*- coding: UTF-8 -*-
#brailleDisplayDrivers/handyTech.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2008-2017 NV Access Limited, Bram Duvigneau, Leonard de Ruijter

from collections import OrderedDict
from cStringIO import StringIO
import serial # pylint: disable=E0401
import hwPortUtils
import hwIo
import braille
import brailleInput
import inputCore
import ui
from baseObject import ScriptableObject, AutoPropertyObject
from globalCommands import SCRCAT_BRAILLE
from logHandler import log


TIMEOUT = 0.2
BAUD_RATE = 19200
PARITY = serial.PARITY_ODD

# pylint: disable=C0330
USB_IDS_SER = {
	"VID_0403&PID_6001", # FTDI chip
	"VID_0921&PID_1200", # GoHubs chip
}

# pylint: disable=C0330
USB_IDS_HID = {
	"VID_1FE4&PID_0054", # Active Braille
	"VID_1FE4&PID_0081", # Basic Braille 16
	"VID_1FE4&PID_0082", # Basic Braille 20
	"VID_1FE4&PID_0083", # Basic Braille 32
	"VID_1FE4&PID_0084", # Basic Braille 40
	"VID_1FE4&PID_008A", # Basic Braille 48
	"VID_1FE4&PID_0086", # Basic Braille 64
	"VID_1FE4&PID_0087", # Basic Braille 80
	"VID_1FE4&PID_008B", # Basic Braille 160
	"VID_1FE4&PID_0061", # Actilino
	"VID_1FE4&PID_0064", # Active Star 40
	"VID_1FE4&PID_0003", # USB-HID adapter
	"VID_1FE4&PID_0074", # Braille Star 40
	"VID_1FE4&PID_0044", # Easy Braille
}

# pylint: disable=C0330
BLUETOOTH_NAMES = {

}

# Model identifiers
MODEL_BRAILLE_WAVE = "\x05"
MODEL_MODULAR_EVOLUTION_64 = "\x36"
MODEL_MODULAR_EVOLUTION_88 = "\x38"
MODEL_EASY_BRAILLE = "\x44"
MODEL_ACTIVE_BRAILLE = "\x54"
MODEL_CONNECT_BRAILLE_40 = "\x55"
MODEL_ACTILINO = "\x61"
MODEL_ACTIVE_STAR_40 = "\x64"
MODEL_BASIC_BRAILLE_16 = "\x81"
MODEL_BASIC_BRAILLE_20 = "\x82"
MODEL_BASIC_BRAILLE_32 = "\x83"
MODEL_BASIC_BRAILLE_40 = "\x84"
MODEL_BASIC_BRAILLE_48 = "\x8A"
MODEL_BASIC_BRAILLE_64 = "\x86"
MODEL_BASIC_BRAILLE_80 = "\x87"
MODEL_BASIC_BRAILLE_160 = "\x8B"
MODEL_BRAILLINO = "\x72"
MODEL_BRAILLE_STAR_40 = "\x74"
MODEL_BRAILLE_STAR_80 = "\x78"
MODEL_MODULAR_20 = "\x80"
MODEL_MODULAR_80 = "\x88"
MODEL_MODULAR_40 = "\x89"
MODEL_BOOKWORM = "\x90"

# Key constants
KEY_B1 = 0x03
KEY_B2 = 0x07
KEY_B3 = 0x0B
KEY_B4 = 0x0F
KEY_B5 = 0x13
KEY_B6 = 0x17
KEY_B7 = 0x1B
KEY_B8 = 0x1F
KEY_LEFT_SPACE = 0x10
KEY_RIGHT_SPACE = 0x18
KEY_ROUTING = 0x20
KEY_RELEASE = 0x80

# Braille dot mapping
KEY_DOTS = {
	KEY_B4: 1,
	KEY_B3: 2,
	KEY_B2: 3,
	KEY_B5: 4,
	KEY_B6: 5,
	KEY_B7: 6,
	KEY_B1: 7,
	KEY_B8: 8,
}

# Considered spaces in braille input mode
KEY_SPACES = (KEY_LEFT_SPACE, KEY_RIGHT_SPACE,)


class Model(AutoPropertyObject):
	#: Device identifier, used in the protocol to identify the device
	#: @type: string
	device_id = None

	#: A reference to the driver instance
	#: @type; BrailleDisplayDriver
	_display = None

	#: A generic name that identifies the model/series, used in gesture identifiers
	#: @type: string
	genericName = None

	#: Specific name of this model
	#: @type: string
	name = None

	#: Number of braille cells
	#: @type: int
	num_cells = 0

	def __init__(self, display):
		super(Model, self).__init__()
		self._display = display

	def _get_keys(self):
		"""Basic keymap

		This returns a basic keymap with sensible defaults for all devices.
		Subclasses should override this method to add model specific keys,
		or relabel keys. Even if a key isn't available on all devices, add it here
		if it would make sense for most devices.
		"""
		return OrderedDict({
			# Braille input keys
			# Numbered from left to right, might be used for braille input on some models
			KEY_B1: "b1",
			KEY_B2: "b2",
			KEY_B3: "b3",
			KEY_B4: "b4",
			KEY_B5: "b5",
			KEY_B6: "b6",
			KEY_B7: "b7",
			KEY_B8: "b8",

			KEY_LEFT_SPACE: "leftSpace",
			KEY_RIGHT_SPACE: "rightSpace",
			# Modular/BS80 keypad
			0x01: "b12",
			0x09: "b13",
			0x05: "n0",
			0x0D: "b14",

			0x11: "b11",
			0x15: "n1",
			0x19: "n2",
			0x1D: "n3",

			0x02: "b10",
			0x06: "n4",
			0x0A: "n5",
			0x0E: "n6",

			0x12: "b9",
			0x16: "n7",
			0x1A: "n8",
			0x1E: "n9",
		})

	def display(self, cells):
		"""Display cells on the braille display

		This is the modern protocol, which uses an extended packet to send braille
		cells. Some displays use an older, simpler protocol. See OldProtocolMixin.
		"""
		self._display._sendExtendedPacket(HT_EXTPKT_BRAILLE, "".join(chr(cell) for cell in cells))


class OldProtocolMixin(object):
	def display(self, cells):
		# TODO: Do we have models with status cells? How to handle these?
		return self._display._sendPacket(HT_PKT_BRAILLE, [chr(cell) for cell in cells])


class TripleActionKeysMixin(object):
	"""Triple action keys

	Most Handy Tech models have so called triple action keys. This keys are
	on the left and right side of the cells and can be pressed at the top,
	at the bottom and in the middle.
	"""
	def _get_keys(self):
		keys = super(TripleActionKeysMixin, self).get_keys()
		keys.update({
			0x0C: "leftTakTop",
			0x14: "leftTakBottom",
			0x04: "rightTakTop",
			0x08: "rightTakBottom",
		})
		return keys


class JoystickMixin(object):
	"""Joystick

	Some Handy Tech models have a joystick, which can be moved left, right, up, down or clicked on the center.
	"""

	def _get_keys(self):
		keys = super(JoystickMixin, self).get_keys()
		keys.update({
			0x74: "joystickLeft",
			0x75: "joystickRight",
			0x76: "joystickUp",
			0x77: "joystickDown",
			0x78: "joystickAction",
		})
		return keys

class ModularEvolution(TripleActionKeysMixin, Model):
	genericName = "Modular Evolution"

	def _get_name(self):
		return '{name} {cells}'.format(name=self.genericName, cells=self.num_cells)


class ModularEvolution88(ModularEvolution):
	device_id = MODEL_MODULAR_EVOLUTION_88
	num_cells = 88


class ModularEvolution64(ModularEvolution):
	device_id = MODEL_MODULAR_EVOLUTION_64
	num_cells = 64


class EasyBraille(OldProtocolMixin, TripleActionKeysMixin, Model):
	device_id = MODEL_EASY_BRAILLE
	num_cells = 40
	genericName = name = "Easy Braille"


class ActiveBraille(TripleActionKeysMixin, Model):
	device_id = MODEL_ACTIVE_BRAILLE
	num_cells = 40
	genericName = name = 'Active Braille'


class Actilino(JoystickMixin, TripleActionKeysMixin, Model):
	device_id = MODEL_ACTILINO
	num_cells = 16
	genericName = name = "Actilino"


class ActiveStar40(TripleActionKeysMixin, Model):
	device_id = MODEL_ACTIVE_STAR_40
	num_cells = 40
	name = "Active Star 40"
	genericName = "Active Star"


class BrailleWave(OldProtocolMixin, Model):
	device_id = MODEL_BRAILLE_WAVE
	num_cells = 40
	genericName = name = "Braille Wave"

	def _get_keys(self):
		keys = super(BrailleWave, self).keys	# pylint: disable=E1101
		keys.update({
			0x04: "left",
			0x08: "right",
			0x0C: "escape",
			0x14: "return",
			KEY_LEFT_SPACE: "space",
		})
		return keys


class BasicBraille(Model):
	genericName = "Basic Braille"

	def _get_name(self):
		return '{name} {cells}'.format(name=self.genericName, cells=self.num_cells)


def basic_braille_factory(cells, device_id):
	return type("BasicBraille{cells}".format(cells=cells), (BasicBraille,), {
		"device_id": device_id,
		"cells": cells,
	})

BasicBraille16 = basic_braille_factory(16, MODEL_BASIC_BRAILLE_16)
BasicBraille20 = basic_braille_factory(20, MODEL_BASIC_BRAILLE_20)
BasicBraille32 = basic_braille_factory(32, MODEL_BASIC_BRAILLE_32)
BasicBraille40 = basic_braille_factory(40, MODEL_BASIC_BRAILLE_40)
BasicBraille48 = basic_braille_factory(48, MODEL_BASIC_BRAILLE_48)
BasicBraille64 = basic_braille_factory(64, MODEL_BASIC_BRAILLE_64)
BasicBraille80 = basic_braille_factory(80, MODEL_BASIC_BRAILLE_80)
BasicBraille160 = basic_braille_factory(160, MODEL_BASIC_BRAILLE_160)


class BrailleStar(OldProtocolMixin, TripleActionKeysMixin, Model):
	genericName = "Braille Star"

	def _get_name(self):
		return '{name} {cells}'.format(name=self.genericName, cells=self.num_cells)


class BrailleStar40(BrailleStar):
	device_id = MODEL_BRAILLE_STAR_40
	cells = 40


class BrailleStar80(BrailleStar):
	device_id = MODEL_BRAILLE_STAR_80
	cells = 80


class Modular(OldProtocolMixin, TripleActionKeysMixin, Model):
	genericName = "Modular"

	def _get_name(self):
		return '{name} {cells}'.format(name=self.genericName, cells=self.num_cells)


class Modular20(Modular):
	device_id = MODEL_MODULAR_20
	cells = 20


class Modular40(Modular):
	device_id = MODEL_MODULAR_40
	cells = 40


class Modular80(Modular):
	device_id = MODEL_MODULAR_80
	cells = 80


class Bookworm(Model):
	# TODO: uses a different protocol
	device_id = MODEL_BOOKWORM
	cells = 8
	genericName = name = "Bookworm"


# Model dict for easy lookup
def _all_subclasses(cls):
	return cls.__subclasses__() + [g for s in cls.__subclasses__()
		for g in _all_subclasses(s)]

MODELS = {
	m.device_id: m for m in _all_subclasses(Model) if hasattr(m, 'device_id')
}


# Packet types
HT_PKT_BRAILLE = "\x01"
HT_PKT_EXTENDED = "\x79"
HT_PKT_NAK = "\x7D"
HT_PKT_ACK = "\x7E"
HT_PKT_OK = "\xFE"
HT_PKT_RESET = "\xFF"
HT_EXTPKT_BRAILLE = HT_PKT_BRAILLE
HT_EXTPKT_KEY = "\x04"
HT_EXTPKT_CONFIRMATION = "\x07"
HT_EXTPKT_SCANCODE = "\x09"
HT_EXTPKT_PING = "\x19"
HT_EXTPKT_SERIAL_NUMBER = "\x41"
HT_EXTPKT_SET_RTC = "\x44"
HT_EXTPKT_GET_RTC = "\x45"
HT_EXTPKT_BLUETOOTH_PIN = "\x47"
HT_EXTPKT_SET_ATC_MODE = "\x50"
HT_EXTPKT_SET_ATC_SENSITIVITY = "\x51"
HT_EXTPKT_ATC_INFO = "\x52"
HT_EXTPKT_SET_ATC_SENSITIVITY_2 = "\x53"
HT_EXTPKT_GET_ATC_SENSITIVITY_2 = "\x54"
HT_EXTPKT_READING_POSITION = "\x55"
HT_EXTPKT_SET_FIRMNESS = "\x60"
HT_EXTPKT_GET_FIRMNESS = "\x61"
HT_EXTPKT_GET_PROTOCOL_PROPERTIES = "\xC1"
HT_EXTPKT_GET_FIRMWARE_VERSION = "\xC2"

# HID specific constants
HT_HID_RPT_OutData = "\x01" # receive data from device
HT_HID_RPT_InData = "\x02" # send data to device
HT_HID_RPT_InCommand = "\xFB" # run USB-HID firmware command
HT_HID_RPT_OutVersion = "\xFC" # get version of USB-HID firmware
HT_HID_RPT_OutBaud = "\xFD" # get baud rate of serial connection
HT_HID_RPT_InBaud = "\xFE" # set baud rate of serial connection
HT_HID_CMD_FlushBuffers = "\x01" # flush input and output buffers

class BrailleDisplayDriver(braille.BrailleDisplayDriver, ScriptableObject):
	name = "handyTech"
	# Translators: The name of a series of braille displays.
	description = _("Handy Tech braille displays")
	isThreadSafe = True

	@classmethod
	def check(cls):
		# TODO: Probably return False if there is no serial port at all?
		return True

	@classmethod
	def getPossiblePorts(cls):
		ports = OrderedDict()
		comPorts = list(hwPortUtils.listComPorts(onlyAvailable=True))
		try:
			next(cls._getAutoPorts(comPorts))
			ports.update((cls.AUTOMATIC_PORT,))
		except StopIteration:
			pass
		for portInfo in comPorts:
			# Translators: Name of a serial communications port.
			ports[portInfo["port"]] = _("Serial: {portName}").format(
				portName=portInfo["friendlyName"])
		return ports

	@classmethod
	def _getAutoPorts(cls, comPorts):
		for portInfo in hwPortUtils.listHidDevices():
			if portInfo.get("usbID") in USB_IDS_HID:
				yield portInfo["devicePath"], "USB HID"
		# Try bluetooth ports last.
		for portInfo in sorted(comPorts, key=lambda item: "bluetoothName" in item):
			port = portInfo["port"]
			hwID = portInfo["hardwareID"]
			if hwID.startswith(r"FTDIBUS\COMPORT"):
				# USB.
				# TODO: It seems there is also another chip (Gohubs) used in some models?
				portType = "USB serial"
				try:
					usbID = hwID.split("&", 1)[1]
				except IndexError:
					continue
				if usbID not in USB_IDS_SER:
					continue
			elif "bluetoothName" in portInfo:
				# Bluetooth.
				portType = "bluetooth"
				btName = portInfo["bluetoothName"]
				if not any(btName.startswith(prefix) for prefix in BLUETOOTH_NAMES):
					continue
			else:
				continue
			yield port, portType

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver, self).__init__()
		self.numCells = 0
		self._model = None
		self._ignoreKeyReleases = False
		self._keysDown = set()
		self._brailleInput = False

		if port == "auto":
			tryPorts = self._getAutoPorts(hwPortUtils.listComPorts(onlyAvailable=True))
		else:
			tryPorts = ((port, "serial"),)
		for port, portType in tryPorts:
			# At this point, a port bound to this display has been found.
			# Try talking to the display.
			self.isHid = portType == "USB HID"
			try:
				if self.isHid:
					self._dev = hwIo.Hid(port, onReceive=self._onReceive)
				else:
					self._dev = hwIo.Serial(port, baudrate=BAUD_RATE, parity=PARITY,
						timeout=TIMEOUT, writeTimeout=TIMEOUT, onReceive=self._onReceive)
			except EnvironmentError:
				continue

			self._sendPacket(HT_PKT_RESET)
			for _i in xrange(3):
				# An expected response hasn't arrived yet, so wait for it.
				self._dev.waitForRead(TIMEOUT)
				if self.numCells and self._model:
					break

			if self.numCells:
				# A display responded.
				log.info("Found {device} connected via {type} ({port})".format(
					device=self._model.name, type=portType, port=port))
				break
			self._dev.close()

		else:
			raise RuntimeError("No Handy Tech display found")

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
		finally:
			# Make sure the device gets closed.
			# If it doesn't, we may not be able to re-open it later.
			self._dev.close()

	def _sendPacket(self, packet_type, data=""):
		if self.isHid:
			if self._model:
				data = self._model.device_id + data
			self._sendHidPacket(chr(len(packet_type)+len(data)), packet_type, data)
		else:
			self._dev.write(packet_type)
			if self._model:
				self._dev.write(self._model.device_id)
			self._dev.write(data)

	def _sendExtendedPacket(self, packet_type, data):
		packet = "{length}{ext_type}{data}\x16".format(
			ext_type=packet_type, data=data,
			length=chr(len(data) + 1)         # Length is including packet_type
		)
		self._sendPacket(HT_PKT_EXTENDED, packet)

	def _sendHidPacket(self, hid_packet_type, ser_packet_type, data=""):
		assert(self.isHid)
		self._dev.write(HT_HID_RPT_InData+hid_packet_type+ser_packet_type+data)

	def _handleKeyRelease(self):
		if self._ignoreKeyReleases or not self._keysDown:
			return
		# The first key released executes the key combination.
		try:
			inputCore.manager.executeGesture(InputGesture(self._model, self._keysDown, self._brailleInput))
		except inputCore.NoInputGestureAction:
			pass
		# Any further releases are just the rest of the keys in the combination being released,
		# so they should be ignored.
		self._ignoreKeyReleases = True

	def _onReceive(self, data):
		if self.isHid:
			# data contains the entire packet.
			stream = StringIO(data)
			hid_packet_type = data[1]
			ser_packet_type = data[2]
			# Skip the header, so reading the stream will only give the rest of the data
			stream.seek(3)
		else:
			ser_packet_type = data
			# data only contained the packet type. Read the rest from the device.
			stream = self._dev

		model_id = stream.read(1)
		if not self._model:
			if not model_id in MODELS:
				log.debug("Unknown model: %r" % model_id)
				return
			self._model = MODELS.get(model_id)(self)
			self.numCells = self._model.num_cells

		if ser_packet_type == HT_PKT_OK:
			pass
		elif ser_packet_type == HT_PKT_ACK:
			log.debug("ACK received")
		elif ser_packet_type == HT_PKT_NAK:
			log.info("NAK received!")
		elif ser_packet_type == HT_PKT_EXTENDED:
			packet_length = ord(stream.read(1))
			packet = stream.read(packet_length)
			assert stream.read(1) == "\x16"    # It seems packets are terminated with \x16
			ext_packet_type = packet[0]
			if ext_packet_type == HT_EXTPKT_CONFIRMATION:
				# Confirmation of a command, do nothing
				pass
			elif ext_packet_type == HT_EXTPKT_KEY:
				key = ord(packet[1])
				release = (key & KEY_RELEASE) != 0
				if release:
					key = key ^ KEY_RELEASE
					self._handleKeyRelease()
					self._keysDown.discard(key)
				else:
					# Press.
					# This begins a new key combination.
					self._ignoreKeyReleases = False
					self._keysDown.add(key)
			else:
				# Unknown extended packet, log it
				log.warning("Unhandled extended packet of type %r: %r" % (ext_packet_type, packet))
		else:
			# Unknown packet type, log it
			log.warning("Unhandled packet of type %r" % ser_packet_type)


	def display(self, cells):
		# cells will already be padded up to numCells.
		self._model.display(cells)

	scriptCategory = SCRCAT_BRAILLE
	
	def script_toggleBrailleInput(self, gesture):
		self._brailleInput = not self._brailleInput
		if self._brailleInput:
			ui.message(_('Braille input enabled'))
		else:
			ui.message(_('Braille input disabled'))

	script_toggleBrailleInput.__doc__ = _("Toggle braille input")

	__gestures = {
		'br(handytech):space+b1+b3+b4': 'toggleBrailleInput',
		'br(handytech):leftSpace+b1+b3+b4': 'toggleBrailleInput',
		'br(handytech):rightSpace+b1+b3+b4': 'toggleBrailleInput',
		'bk:space+dot1+dot2+dot7': 'toggleBrailleInput',
	}

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_routeTo": ("br(handyTech):routing",),
			"braille_scrollBack": (
				"br(handytech):leftSpace", "br(handytech):leftTakTop", "br(handytech):rightTakTop",
				"br(handytech):b3", "br(handytech):left",),
			"braille_previousLine": ("br(handytech):b4",),
			"braille_nextLine": ("br(handytech):b5",),
			"braille_scrollForward": (
				"br(handytech):rightSpace", "br(handytech):leftTakBottom",
				"br(handytech):rightTakBottom", "br(handytech):b6", "br(handytech):right"),
			"braille_toggleTether": ("br(handytech):b2",),
			"kb:shift+tab": ("br(handytech):leftTakTop+leftTakBottom", 
			"br(handytech):escape",),
			"kb:tab": ("br(handytech):rightTakTop+rightTakBottom",  
				"br(handytech):return",),
			"kb:enter": (
				"br(handytech):leftTakTop+leftTakBottom+rightTakTop+rightTakBottom",
				"br(handytech):b8", "br(handytech):escape+return",),
			"kb:alt": ("br(handytech):b2+b4+b5",),
			"kb:escape": ("br(handytech):b4+b6",),
			"kb:1": ("br(handytech):n1",),
			"kb:2": ("br(handytech):n2",),
			"kb:3": ("br(handytech):n3",),
			"kb:4": ("br(handytech):n4",),
			"kb:5": ("br(handytech):n5",),
			"kb:6": ("br(handytech):n6",),
			"kb:7": ("br(handytech):n7",),
			"kb:8": ("br(handytech):n8",),
			"kb:9": ("br(handytech):n9",),
			"kb:0": ("br(handytech):n0",),
			"showGui": ("br(handytech):b2+b4+b5+b6",),
		},
	})


# pylint: disable=W0223
class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, model, keys, isBrailleInput=False):
		super(InputGesture, self).__init__()
		self.model = model.genericName
		self.keys = set(keys)

		self.keyNames = names = []
		for key in keys:
			if isBrailleInput:
				self.dots = self._calculateDots()
				if key in KEY_SPACES:
					self.space = True
			if key >= KEY_ROUTING:
				self.routingIndex = key - KEY_ROUTING
				names.append("routing")
			elif not isBrailleInput:
				try:
					names.append(model.keys[key])
				except KeyError:
					log.debugWarning("Unknown key %d" % key)

		self.id = "+".join(names)

	def _calculateDots(self):
		dots = 0
		for key in self.keys:
			if key in KEY_DOTS:
				dots |= 1 << (KEY_DOTS[key] - 1)
		return dots

