# -*- coding: UTF-8 -*-
#brailleDisplayDrivers/handyTech.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2008-2017 NV Access Limited and NVDA contrributors

from collections import OrderedDict
import serial # pylint: disable=E0401
import hwPortUtils
import braille
import inputCore
from logHandler import log
import brailleInput
import hwIo

TIMEOUT = 0.2
BAUD_RATE = 19200
PARITY = serial.PARITY_ODD

USB_IDS_SER = {
	"VID_0403&PID_6001", # FTDI chip
	"VID_0921&PID_1200", # GoHubs chip
}

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

BLUETOOTH_NAMES = {

}

MODELS = {
	"\x05": ("Braille Wave", 40),
	"\x36": ("Modular Evolution 64", 64),
	"\x38": ("Modular Evolution 88", 88),
	"\x44": ("Easy Braille", 40),
	"\x54": ("Active Braille", 40),
	"\x55": ("Connect Braille 40", 40),
	"\x61": ("Actilino", 20),
	"\x64": ("Active Star 40", 40),
	"\x81": ("Basic Braille 16", 16),
	"\x82": ("Basic Braille 20", 20),
	"\x83": ("Basic Braille 32", 32),
	"\x84": ("Basic Braille 40", 40),
	"\x8A": ("Basic Braille 48", 48),
	"\x86": ("Basic Braille 64", 64),
	"\x87": ("Basic Braille 80", 80),
	"\x8B": ("Basic Braille 160", 160),
	"\x72": ("Braillino", 20),
	"\x74": ("Braille Star 40", 40),
	"\x78": ("Braille Star 80", 80),
	"\x80": ("Modular 20", 20),
	"\x88": ("Modular 88", 88),
	"\x89": ("Modular 40", 40),
	"\x90": ("Bookworm", 20),
}

# Keys
KEYS = {
	# Braille input keys
	# Numbered from left to right, might be used for braille input on some models
	"\x03": "b1",
	"\x07": "b2",
	"\x0B": "b3",
	"\x0F": "b4",
	"\x13": "b5",
	"\x17": "b6",
	"\x1B": "b7",
	"\x1F": "b8",

	# Up/down
	# TODO: Find out which keys this are exactly
	"\x04": "up",
	"\x08": "down",

	# Modular/BS80 keypad
	"\x01": "b12",
	"\x09": "b13",
	"\x05": "n0",
	"\x0D": "b14",

	"\x11": "b11",
	"\x15": "n1",
	"\x19": "n2",
	"\x1D": "n3",

	"\x02": "b10",
	"\x06": "n4",
	"\x0A": "n5",
	"\x0E": "n6",

	"\x12": "b9",
	"\x16": "n7",
	"\x1A": "n8",
	"\x1E": "n9",

	# BrailleWave/Star
	# TODO: Check which names are used by current driver
	"\x0C": "escape",
	"\x10": "space",
	"\x14": "return",

	# BrailleStar
	"\x18": "spaceRight",

	# Actilino
	"\x74": "joystickLeft",
	"\x75": "joystickRight",
	"\x76": "joystickUp",
	"\x77": "joystickDown",
	"\x78": "joystickAction",
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
		super(BrailleDisplayDriver, self).__init__	()
		self.numCells = 0
		self._deviceID = None
		self._deviceName = None

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
				if self.numCells and self._deviceID:
					break

			if self.numCells:
				# A display responded.
				log.info("Found {device} connected via {type} ({port})".format(
					device=self._deviceName, type=portType, port=port))
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
		self._dev.write(packet_type)
		if self._deviceID:
			self._dev.write(self._deviceID)
		self._dev.write(data)

	def _sendExtendedPacket(self, packet_type, data):
		packet = "{length}{ext_type}{data}\x16".format(
			model=self._deviceID, ext_type=packet_type, data=data,
			length=chr(len(data) + 1)         # Length is including packet_type
		)
		self._sendPacket(HT_PKT_EXTENDED, packet)

	def _onReceive(self, data):
		if self.isHid:
			# data contains the entire packet.
			stream = StringIO(data)
			packet_type = data[0]
			# Skip the packet_type, so reading the stream will only give the rest of the data
			stream.seek(1)
		else:
			packet_type = data
			# data only contained the packet type. Read the rest from the device.
			stream = self._dev

		# log.debug("Got packet of type: %r" % packet_type)
		model_id = stream.read(1)
		if not self._deviceID:
			if not model_id in MODELS:
				log.debug("Unknown model: %r" % model_id)
				return
			model = MODELS.get(model_id)
			self.numCells = model[1]
			self._deviceName = model[0]
			self._deviceID = model_id

		if packet_type == HT_PKT_OK:
			pass
		elif packet_type == HT_PKT_ACK:
			log.debug("ACK received")
		elif packet_type == HT_PKT_NAK:
			log.info("NAK received!")
		elif packet_type == HT_PKT_EXTENDED:
			packet_length = ord(stream.read(1))
			packet = stream.read(packet_length)
			assert stream.read(1) == "\x16"    # It seems packets are terminated with \x16
			ext_packet_type = packet[0]
			if ext_packet_type == HT_EXTPKT_CONFIRMATION:
				log.debug("Extended confirmation received")
			elif ext_packet_type == HT_EXTPKT_KEY:
				key = packet[1]
				release = (ord(key) & ord("\x80")) != 0
				if release:
					key = chr(ord(key) ^ ord("\x80"))
				if key in KEYS:
					log.debug("Got key {key}, release {release}".format(
						key=KEYS[key], release=release))
				else:
					log.debug("Got unknown key %r" % key)
			else:
				log.debug("Extended packet of type %r: %r" % (ext_packet_type, packet))
		else:
			log.warning("Unhandled packet of type %r" % packet_type)


	def display(self, cells):
		# cells will already be padded up to numCells.
		self._sendExtendedPacket(HT_EXTPKT_BRAILLE, "".join(chr(cell) for cell in cells))
