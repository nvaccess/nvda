# -*- coding: UTF-8 -*-
#brailleDisplayDrivers/handyTech.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2008-2017 NV Access Limited and NVDA contrributors

from collections import OrderedDict
from cStringIO import StringIO
import serial # pylint: disable=E0401
import hwPortUtils
import hwIo
import braille
import brailleInput
import inputCore
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
MODEL_MODULAR_88 = "\x88"
MODEL_MODULAR_40 = "\x89"
MODEL_BOOKWORM = "\x90"


class Model(object):
	# Device identifier, used in the protocol to identify the device
	device_id = None

	def __init__(self, display):
		self._display = display

	def get_keys(self):
		"""Basic keymap

		This returns a basic keymap with sensible defaults for all devices.
		Subclasses should override this method to add model specific keys, 
		or relabel keys. Even if a key isn't available on all devices, add it here
		if it would make sense for most devices.
		"""
		return {
			# Braille input keys
			# Numbered from left to right, might be used for braille input on some models
			0x03: "b1",
			0x07: "b2",
			0x0B: "b3",
			0x0F: "b4",
			0x13: "b5",
			0x17: "b6",
			0x1B: "b7",
			0x1F: "b8",

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

			# Actilino
			0x74: "joystickLeft",
			0x75: "joystickRight",
			0x76: "joystickUp",
			0x77: "joystickDown",
			0x78: "joystickAction",
		}


class ModularEvolution(Model):
	pass


class ModularEvolution88(ModularEvolution):
	device_id = MODEL_MODULAR_EVOLUTION_88
	num_cells = 88
	name = "Modular Evolution 88"


class ModularEvolution64(ModularEvolution):
	device_id = MODEL_MODULAR_EVOLUTION_64
	num_cells = 64
	name = "Modular Evolution 64"

# Model dict for easy lookup
def _all_subclasses(cls):
	return cls.__subclasses__() + [g for s in cls.__subclasses__()
		for g in _all_subclasses(s)]

MODELS = {
	m.device_id: m for m in _all_subclasses(Model) if hasattr(m, 'device_id')
}


# Key ranges
KEY_ROUTING = 0x20
KEY_RELEASE = 0x80

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

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
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
			# self._sendPacket(HT_PKT_RESET)
			for i in xrange(3):
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
			self._sendHidPacket(HT_HID_RPT_OutData, packet_type, data)
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
			inputCore.manager.executeGesture(InputGesture(self._model, self._keysDown))
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

		# log.debug("Got packet of type: %r" % ser_packet_type)
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
				log.debug("Extended confirmation received")
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
				log.debug("Extended packet of type %r: %r" % (ext_packet_type, packet))
		else:
			log.warning("Unhandled packet of type %r" % ser_packet_type)


	def display(self, cells):
		# cells will already be padded up to numCells.
		self._sendExtendedPacket(HT_EXTPKT_BRAILLE, "".join(chr(cell) for cell in cells))

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_routeTo": ("br(handyTech):routing",),
		},
	})


class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, model, keys):
		super(InputGesture, self).__init__()
		self.keys = set(keys)

		self.keyNames = names = []
		for key in keys:
			if key >= KEY_ROUTING:
				self.routingIndex = key - KEY_ROUTING
				names.append("routing")
			else:
				try:
					names.append(model.get_keys()[key])
				except KeyError:
					log.debugWarning("Unknown key %d" % key)

		self.id = "+".join(names)
