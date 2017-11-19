# -*- coding: UTF-8 -*-
#brailleDisplayDrivers/handyTech.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2008-2017 NV Access Limited, Bram Duvigneau, Leonard de Ruijter (Babbage B.V.), Felix Grützmacher (Handy Tech Elektronik GmbH)
"Braille display driver for Handy Tech braille displays"
from collections import OrderedDict
from cStringIO import StringIO
import serial # pylint: disable=E0401
import weakref
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

# Newer displays have a native HID processor
# pylint: disable=C0330
USB_IDS_HID_NATIVE = {
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
}

# Some older displays use a HID converter and an internal serial interface
USB_IDS_HID_CONVERTER = {
	"VID_1FE4&PID_0003", # USB-HID adapter
	"VID_1FE4&PID_0074", # Braille Star 40
	"VID_1FE4&PID_0044", # Easy Braille
}

USB_IDS_HID = USB_IDS_HID_NATIVE | USB_IDS_HID_CONVERTER

# pylint: disable=C0330
BLUETOOTH_NAMES = {
	"Actilino AL",
	"Active Braille AB",
	"Active Star AS",
	"Basic Braille BB",
	"Braille Star 40 BS",
	"Braille Wave BW",
	"Easy Braille EBR",
}

# Model identifiers
# pylint: disable=C0103
MODEL_BRAILLE_WAVE = "\x05"
MODEL_MODULAR_EVOLUTION_64 = "\x36"
MODEL_MODULAR_EVOLUTION_88 = "\x38"
MODEL_MODULAR_CONNECT_88 = "\x3A"
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
MODEL_BRAILLE_STAR_40 = "\x74"
MODEL_BRAILLE_STAR_80 = "\x78"
MODEL_MODULAR_20 = "\x80"
MODEL_MODULAR_80 = "\x88"
MODEL_MODULAR_40 = "\x89"

# Key constants
KEY_B1 = 0x03
KEY_B2 = 0x07
KEY_B3 = 0x0B
KEY_B4 = 0x0F
KEY_B5 = 0x13
KEY_B6 = 0x17
KEY_B7 = 0x1B
KEY_B8 = 0x1F
KEY_LEFT = 0x04
KEY_RIGHT = 0x08
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
	"""Extend from this base class to define model specific behavior."""
	#: Device identifier, used in the protocol to identify the device
	#: @type: string
	deviceId = None

	#: A generic name that identifies the model/series, used in gesture identifiers
	#: @type: string
	genericName = None

	#: Specific name of this model
	#: @type: string
	name = None

	#: Number of braille cells
	#: @type: int
	numCells = 0

	def __init__(self, display):
		super(Model, self).__init__()
		# A weak reference to the driver instance, used due to a circular reference  between Model and Display
		self._displayRef = weakref.ref(display)

	def postInit(self):
		"""Executed after model initialisation.

		Subclasses may extend this method to perform actions on initialization 
		of the display. Don't use __init__ for this, since the model ID has 
		not been set, which is needed for sending packets to the display.
		"""

	def _get__display(self):
		"""The L{BrailleDisplayDriver} which initialized this Model instance"""
		# self._displayRef is a weakref, call it to get the object
		return self._displayRef()

	# pylint: disable=R0201
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
			# Left and right keys, found on Easy Braille and Braille Wave
			KEY_LEFT: "left",
			KEY_RIGHT: "right",

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
		cells. Some very old displays use an older, simpler protocol
		which is currently not implemented in this driver.
		"""
		self._display.sendExtendedPacket(HT_EXTPKT_BRAILLE,
			"".join(chr(cell) for cell in cells))


class AtcMixin(object):

	def postInit(self):
		super(AtcMixin, self).postInit()
		log.debug("Enabling ATC")
		self._display.sendExtendedPacket(HT_EXTPKT_SET_ATC_MODE, True)		

class TripleActionKeysMixin(AutoPropertyObject):
	"""Triple action keys

	Most Handy Tech models have so called triple action keys. This keys are
	on the left and right side of the cells and can be pressed at the top,
	at the bottom and in the middle.
	"""
	def _get_keys(self):
		"""Add the triple action keys to the keys property"""
		keys = super(TripleActionKeysMixin, self).keys
		keys.update({
			0x0C: "leftTakTop",
			0x14: "leftTakBottom",
			0x04: "rightTakTop",
			0x08: "rightTakBottom",
		})
		return keys


class JoystickMixin(AutoPropertyObject):
	"""Joystick

	Some Handy Tech models have a joystick, which can be moved left, right, up,
	down or clicked on the center.
	"""

	def _get_keys(self):
		"""Add the joystick keys to the keys property"""
		keys = super(JoystickMixin, self).keys
		keys.update({
			0x74: "joystickLeft",
			0x75: "joystickRight",
			0x76: "joystickUp",
			0x77: "joystickDown",
			0x78: "joystickAction",
		})
		return keys


class StatusCellMixin(AutoPropertyObject):
	"""Status cells and routing keys

	Some Handy Tech models have four status cells with corresponding routing keys.
	"""

	def _get_keys(self):
		"""Add the status routing keys to the keys property"""
		keys = super(StatusCellMixin, self).keys
		keys.update({
			0x70: "statusRouting1",
			0x71: "statusRouting2",
			0x72: "statusRouting3",
			0x73: "statusRouting4",
		})
		return keys

	def display(self, cells):
		"""Display braille on the display with empty status cells

		Some displays (e.g. Modular series) have 4 status cells.
		These cells need to be included in the braille data, but since NVDA doesn't
		support status cells, we just send empty cells.
		"""
		cells = [0] * 4 + cells
		super(StatusCellMixin, self).display(cells)


class ModularConnect88(TripleActionKeysMixin, Model):
	deviceId = MODEL_MODULAR_CONNECT_88
	genericName = "Modular Connect"
	name = "Modular Connect 88"
	numCells = 88


# pylint: disable=C0111
class ModularEvolution(AtcMixin, TripleActionKeysMixin, Model):
	genericName = "Modular Evolution"

	def _get_name(self):
		return '{name} {cells}'.format(name=self.genericName, cells=self.numCells)


class ModularEvolution88(ModularEvolution):
	deviceId = MODEL_MODULAR_EVOLUTION_88
	numCells = 88


class ModularEvolution64(ModularEvolution):
	deviceId = MODEL_MODULAR_EVOLUTION_64
	numCells = 64


class EasyBraille(Model):
	deviceId = MODEL_EASY_BRAILLE
	numCells = 40
	genericName = name = "Easy Braille"

class ActiveBraille(AtcMixin, TripleActionKeysMixin, Model):
	deviceId = MODEL_ACTIVE_BRAILLE
	numCells = 40
	genericName = name = 'Active Braille'


class ConnectBraille40(TripleActionKeysMixin, Model):
	deviceId = MODEL_CONNECT_BRAILLE_40
	numCells = 40
	genericName = "Connect Braille"
	name = "Connect Braille 40"


class Actilino(AtcMixin, JoystickMixin, TripleActionKeysMixin, Model):
	deviceId = MODEL_ACTILINO
	numCells = 16
	genericName = name = "Actilino"


class ActiveStar40(AtcMixin, TripleActionKeysMixin, Model):
	deviceId = MODEL_ACTIVE_STAR_40
	numCells = 40
	name = "Active Star 40"
	genericName = "Active Star"


class BrailleWave(Model):
	deviceId = MODEL_BRAILLE_WAVE
	numCells = 40
	genericName = name = "Braille Wave"

	def _get_keys(self):
		keys = super(BrailleWave, self).keys
		keys.update({
			0x0C: "escape",
			0x14: "return",
			KEY_LEFT_SPACE: "space",
		})
		return keys


class BasicBraille(Model):
	genericName = "Basic Braille"

	def _get_name(self):
		return '{name} {cells}'.format(name=self.genericName, cells=self.numCells)


def basicBrailleFactory(numCells, deviceId):
	return type("BasicBraille{cells}".format(cells=numCells), (BasicBraille,), {
		"deviceId": deviceId,
		"numCells": numCells,
	})

BasicBraille16 = basicBrailleFactory(16, MODEL_BASIC_BRAILLE_16)
BasicBraille20 = basicBrailleFactory(20, MODEL_BASIC_BRAILLE_20)
BasicBraille32 = basicBrailleFactory(32, MODEL_BASIC_BRAILLE_32)
BasicBraille40 = basicBrailleFactory(40, MODEL_BASIC_BRAILLE_40)
BasicBraille48 = basicBrailleFactory(48, MODEL_BASIC_BRAILLE_48)
BasicBraille64 = basicBrailleFactory(64, MODEL_BASIC_BRAILLE_64)
BasicBraille80 = basicBrailleFactory(80, MODEL_BASIC_BRAILLE_80)
BasicBraille160 = basicBrailleFactory(160, MODEL_BASIC_BRAILLE_160)


class BrailleStar(TripleActionKeysMixin, Model):
	genericName = "Braille Star"

	def _get_name(self):
		return '{name} {cells}'.format(name=self.genericName, cells=self.numCells)


class BrailleStar40(BrailleStar):
	deviceId = MODEL_BRAILLE_STAR_40
	numCells = 40


class BrailleStar80(BrailleStar):
	deviceId = MODEL_BRAILLE_STAR_80
	numCells = 80


class Modular(StatusCellMixin, TripleActionKeysMixin, Model):
	genericName = "Modular"

	def _get_name(self):
		return '{name} {cells}'.format(name=self.genericName, cells=self.numCells)


class Modular20(Modular):
	deviceId = MODEL_MODULAR_20
	numCells = 20


class Modular40(Modular):
	deviceId = MODEL_MODULAR_40
	numCells = 40


class Modular80(Modular):
	deviceId = MODEL_MODULAR_80
	numCells = 80


def _allSubclasses(cls):
	"""List all direct and indirect subclasses of cls

	This function calls itself recursively to return all subclasses of cls.

	@param cls: the base class to list subclasses of
	@type cls: class
	@rtype: [class]
	"""
	return cls.__subclasses__() + [g for s in cls.__subclasses__()
		for g in _allSubclasses(s)]

# Model dict for easy lookup
MODELS = {
	m.deviceId: m for m in _allSubclasses(Model) if hasattr(m, 'deviceId')
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
			if portInfo.get("usbID") in USB_IDS_HID_CONVERTER:
				yield portInfo["devicePath"], "USB HID serial converter"
			if portInfo.get("usbID") in USB_IDS_HID_NATIVE:
				yield portInfo["devicePath"], "USB HID"
		# Try bluetooth ports last.
		for portInfo in sorted(comPorts, key=lambda item: "bluetoothName" in item):
			port = portInfo["port"]
			hwId = portInfo["hardwareID"]
			if hwId.startswith(r"FTDIBUS\COMPORT"):
				# USB.
				# TODO: It seems there is also another chip (Gohubs) used in some models. See if we can autodetect that as well.
				portType = "USB serial"
				try:
					usbId = hwId.split("&", 1)[1]
				except IndexError:
					continue
				if usbId not in USB_IDS_SER:
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
		self._pendingCells = []
		self._awaitingACK = False
		self._hidSerialBuffer = ""

		if port == "auto":
			tryPorts = self._getAutoPorts(hwPortUtils.listComPorts(onlyAvailable=True))
		else:
			tryPorts = ((port, "serial"),)
		for port, portType in tryPorts:
			# At this point, a port bound to this display has been found.
			# Try talking to the display.
			self.isHid = portType.startswith("USB HID")
			self.isHidSerial = portType == "USB HID serial converter"
			try:
				if self.isHid:
					self._dev = hwIo.Hid(port, onReceive=self._onReceive)
					if self.isHidSerial:
						# This is either the standalone HID adapter cable for older displays,
						# or an older display with a HID - serial adapter built in
						# Send a flush to open the serial channel
						self._dev.write(HT_HID_RPT_InCommand + HT_HID_CMD_FlushBuffers)
				else:
					self._dev = hwIo.Serial(port, baudrate=BAUD_RATE, parity=PARITY,
						timeout=TIMEOUT, writeTimeout=TIMEOUT, onReceive=self._onReceive)
			except EnvironmentError:
				log.debugWarning("", exc_info=True)
				continue

			self.sendPacket(HT_PKT_RESET)
			for _i in xrange(3):
				# An expected response hasn't arrived yet, so wait for it.
				self._dev.waitForRead(TIMEOUT)
				if self.numCells and self._model:
					break

			if self.numCells:
				# A display responded.
				self._model.postInit()
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

	def sendPacket(self, packetType, data=""):
		if type(data) == bool or type(data) == int:
			data = chr(data)
		if self._model:
			data = self._model.deviceId + data
		if self.isHid:
			self._sendHidPacket(packetType+data)
		else:
			self._dev.write(packetType + data)

	def sendExtendedPacket(self, packetType, data=""):
		if type(data) == bool or type(data) == int:
			data = chr(data)
		packet = "{length}{extType}{data}\x16".format(
			extType=packetType, data=data,
			length=chr(len(data) + len(packetType))
		)
		self.sendPacket(HT_PKT_EXTENDED, packet)

	def _sendHidPacket(self, packet):
		assert self.isHid
		maxBlockSize = self._dev._writeSize-3
		# When the packet length exceeds C{writeSize}, the packet is split up into several packets.
		# These packets are of size C{blockSize}.
		# They contain C{HT_HID_RPT_InData}, the length of the data block,
		# the data block itself and a terminating null character.
		bytesRemaining = packet
		while bytesRemaining:
			blockSize = min(maxBlockSize, len(bytesRemaining))
			hidPacket = HT_HID_RPT_InData + chr(blockSize) + bytesRemaining[:blockSize] + "\x00"
			self._dev.write(hidPacket)
			bytesRemaining = bytesRemaining[blockSize:]

	def _handleKeyRelease(self):
		if self._ignoreKeyReleases or not self._keysDown:
			return
		# The first key released executes the key combination.
		try:
			inputCore.manager.executeGesture(
				InputGesture(self._model, self._keysDown, self._brailleInput))
		except inputCore.NoInputGestureAction:
			pass
		# Any further releases are just the rest of the keys in the combination
		# being released, so they should be ignored.
		self._ignoreKeyReleases = True

	def _handleAck(self):
		if not self._awaitingACK:
			return
		self._awaitingACK = False
		if self._pendingCells:
			self.display(self._pendingCells)

	# pylint: disable=R0912
	# Pylint complains about many branches, might be worth refactoring
	def _onReceive(self, data):
		if self.isHidSerial:
			# The HID serial converter seems to wrap one or two bytes into a single HID packet
			hidLength = ord(data[1])
			self._hidSerialBuffer+=data[2:(2+hidLength)]
			currentBufferLength=len(self._hidSerialBuffer)
			# We only support the extended packet based protocol
			# Thus, the only non-extended packet we expect is the device identification, which is of type HT_PKT_OK and two bytes in size
			serPacketType = self._hidSerialBuffer[0]
			if serPacketType!=HT_PKT_EXTENDED:
				if currentBufferLength>2:
					stream = StringIO(self._hidSerialBuffer[:2])
					self._hidSerialBuffer = self._hidSerialBuffer[2:]
				elif currentBufferLength==2:
					stream = StringIO(self._hidSerialBuffer)
					self._hidSerialBuffer = ""
				else:
					# The packet is not yet complete
					return
			# Extended packets are at least 5 bytes in size.
			elif serPacketType==HT_PKT_EXTENDED and currentBufferLength>=5:
				# Check whether our packet is complete
				# The second byte is the model, the third byte is the data length, excluding the terminator
				packet_length = ord(self._hidSerialBuffer[2])+4
				if len(self._hidSerialBuffer)<packet_length:
					# The packet is not yet complete
					return
				# We have a complete packet, but it must be isolated from another packet that could have landed in the buffer
				if len(self._hidSerialBuffer)>packet_length:
					stream = StringIO(self._hidSerialBuffer[:packet_length])
					self._hidSerialBuffer = self._hidSerialBuffer[packet_length:]
				else:
					assert self._hidSerialBuffer.endswith("\x16")	# Extended packets are terminated with \x16
					stream = StringIO(self._hidSerialBuffer)
					self._hidSerialBuffer = ""
			else:
				# The packet is not yet complete
				return
			stream.seek(1)
		elif self.isHid:
			# data contains the entire packet.
			stream = StringIO(data)
			serPacketType = data[2]
			# Skip the header, so reading the stream will only give the rest of the data
			stream.seek(3)
		else:
			serPacketType = data
			# data only contained the packet type. Read the rest from the device.
			stream = self._dev

		modelId = stream.read(1)
		if not self._model:
			if not modelId in MODELS:
				log.debugWarning("Unknown model: %r" % modelId)
				raise RuntimeError(
					"The model with ID %r is not supported by this driver" % modelId)
			self._model = MODELS.get(modelId)(self)
			self.numCells = self._model.numCells
		elif self._model.deviceId != modelId:
			# Somehow the model ID of this display changed, probably another display 
			# plugged in the same (already open) serial port.
			self.terminate()

		if serPacketType==HT_PKT_OK:
			pass
		elif serPacketType == HT_PKT_ACK:
			# This is unexpected, but we need to make sure that we handle old style ack
			self._handleAck()
		elif serPacketType == HT_PKT_NAK:
			log.debugWarning("NAK received!")
		elif serPacketType == HT_PKT_EXTENDED:
			packet_length = ord(stream.read(1))
			packet = stream.read(packet_length)
			terminator = stream.read(1)
			assert terminator == "\x16"	# Extended packets are terminated with \x16
			extPacketType = packet[0]
			if extPacketType == HT_EXTPKT_CONFIRMATION:
				# Confirmation of a command.
				if packet[1] == HT_PKT_ACK:
					self._handleAck()
				elif packet[1] == HT_PKT_NAK:
					log.debugWarning("NAK received!")
			elif extPacketType == HT_EXTPKT_KEY:
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
			elif extPacketType == HT_EXTPKT_ATC_INFO:
				# Ignore ATC packets for now
				pass
			elif extPacketType == HT_EXTPKT_GET_PROTOCOL_PROPERTIES:
				pass
			else:
				# Unknown extended packet, log it
				log.debugWarning("Unhandled extended packet of type %r: %r" %
					(extPacketType, packet))
		else:
			# Unknown packet type, log it
			log.debugWarning("Unhandled packet of type %r" % serPacketType)


	def display(self, cells):
		if not self._awaitingACK:
			# cells will already be padded up to numCells.
			self._model.display(cells)
			self._awaitingACK = True
			self._pendingCells = []
		else:
			self._pendingCells = cells

	scriptCategory = SCRCAT_BRAILLE

	def script_toggleBrailleInput(self, _gesture):
		self._brailleInput = not self._brailleInput
		if self._brailleInput:
			# Translators: message when braille input is enabled
			ui.message(_('Braille input enabled'))
		else:
			# Translators: message when braille input is disabled
			ui.message(_('Braille input disabled'))

	# Translators: description of the script to toggle braille input
	script_toggleBrailleInput.__doc__ = _("Toggle braille input")

	__gestures = {
		'br(handytech):space+b1+b3+b4': 'toggleBrailleInput',
		'br(handytech):leftSpace+b1+b3+b4': 'toggleBrailleInput',
		'br(handytech):rightSpace+b1+b3+b4': 'toggleBrailleInput',
		'br(handytech.easybraille):left+b1+b3+b4': 'toggleBrailleInput',
		'br(handytech.easybraille):right+b1+b3+b4': 'toggleBrailleInput',
		'bk:space+dot1+dot2+dot7': 'toggleBrailleInput',
	}

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_routeTo": ("br(handyTech):routing",),
			"braille_scrollBack": (
				"br(handytech):leftSpace", "br(handytech):leftTakTop",
				"br(handytech):rightTakTop", "br(handytech):b3", "br(handytech):left",),
			"braille_previousLine": ("br(handytech):b4",),
			"braille_nextLine": ("br(handytech):b5",),
			"braille_scrollForward": (
				"br(handytech):rightSpace", "br(handytech):leftTakBottom",
				"br(handytech):rightTakBottom", "br(handytech):b6", "br(handytech):right",
			),
			"braille_toggleTether": ("br(handytech):b2",),
			"braille_toggleFocusContextPresentation": ("br(handytech):b7",),
			"braille_toggleShowCursor": ("br(handytech):b1",),
			"kb:shift+tab": (
				"br(handytech):leftTakTop+leftTakBottom",
				"br(handytech):escape",
			),
			"kb:tab": (
				"br(handytech):rightTakTop+rightTakBottom",
				"br(handytech):return",
			),
			"kb:enter": (
				"br(handytech):leftTakTop+leftTakBottom+rightTakTop+rightTakBottom",
				"br(handytech):b8",
				"br(handytech):escape+return",
				"br(handytech):joystickAction",
			),
			"kb:alt": ("br(handytech):b2+b4+b5",),
			"kb:escape": ("br(handytech):b4+b6",),
			"kb:upArrow": ("br(handytech):joystickUp",),
			"kb:downArrow": ("br(handytech):joystickDown",),
			"kb:leftArrow": ("br(handytech):joystickLeft",),
			"kb:rightArrow": ("br(handytech):joystickRight",),
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


# pylint: disable=W0223, C0301
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
				if key in KEY_SPACES or (key in (KEY_LEFT, KEY_RIGHT) and isinstance(model,EasyBraille)):
					self.space = True
			if KEY_ROUTING <= key < KEY_ROUTING + model.numCells:
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
