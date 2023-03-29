# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2008-2021 NV Access Limited, Bram Duvigneau, Babbage B.V.,
# Felix Grützmacher (Handy Tech Elektronik GmbH), Leonard de Ruijter

"""
Braille display driver for Handy Tech braille displays.
"""

from collections import OrderedDict
from io import BytesIO
import serial
import weakref
import hwIo
from hwIo import intToByte, boolToByte
import braille
import brailleInput
import inputCore
import ui
from baseObject import ScriptableObject, AutoPropertyObject
from globalCommands import SCRCAT_BRAILLE
from logHandler import log
import bdDetect
import time
import datetime
from ctypes import windll
import windowUtils

import wx
from typing import List, Any, Union, Optional


class InvisibleDriverWindow(windowUtils.CustomWindow):
	className = u"Handy_Tech_Server"
	HT_SLEEP = 100
	HT_INCREMENT = 1
	HT_DECREMENT = 0

	def __init__(self):
		super().__init__("Handy Tech Server")
		# Register shared window message.
		# Note: There is no corresponding unregister function.
		# Still this does no harm if done repeatedly.
		self.window_message = windll.user32.RegisterWindowMessageW("Handy_Tech_Server")

	def windowProc(self, hwnd: int, msg: int, wParam: int, lParam: int):
		if msg == self.window_message:
			instanceCount = len(BrailleDisplayDriver._instances)
			if instanceCount == 0:
				log.error(
					"Received Handy_Tech_Server window message while no driver instances are alive"
				)
				wx.CallAfter(BrailleDisplayDriver.destroyMessageWindow)
			elif wParam == self.HT_SLEEP:
				if instanceCount > 1:
					log.error(
						"Received Handy_Tech_Server window message while multiple driver instances are alive"
					)
				driver = next(d for d in BrailleDisplayDriver._instances)
				if lParam == self.HT_INCREMENT:
					driver.goToSleep()
				elif lParam == self.HT_DECREMENT:
					driver.wakeUp()
			return 0  # success, bypass default window procedure


BAUD_RATE = 19200
PARITY = serial.PARITY_ODD

# Some older Handy Tech displays use a HID converter and an internal serial interface.
# We need to keep these IDS around here to send additional data upon connection.
USB_IDS_HID_CONVERTER = {
	"VID_1FE4&PID_0003", # USB-HID adapter
	"VID_1FE4&PID_0074", # Braille Star 40
	"VID_1FE4&PID_0044", # Easy Braille
}

# Model identifiers
MODEL_BRAILLE_WAVE = b"\x05"
MODEL_MODULAR_EVOLUTION_64 = b"\x36"
MODEL_MODULAR_EVOLUTION_88 = b"\x38"
MODEL_MODULAR_CONNECT_88 = b"\x3A"
MODEL_EASY_BRAILLE = b"\x44"
MODEL_ACTIVE_BRAILLE = b"\x54"
MODEL_CONNECT_BRAILLE = b"\x55"
MODEL_ACTILINO = b"\x61"
MODEL_ACTIVE_STAR_40 = b"\x64"
MODEL_BASIC_BRAILLE_16 = b"\x81"
MODEL_BASIC_BRAILLE_20 = b"\x82"
MODEL_BASIC_BRAILLE_32 = b"\x83"
MODEL_BASIC_BRAILLE_40 = b"\x84"
MODEL_BASIC_BRAILLE_48 = b"\x8A"
MODEL_BASIC_BRAILLE_64 = b"\x86"
MODEL_BASIC_BRAILLE_80 = b"\x87"
MODEL_BASIC_BRAILLE_160 = b"\x8B"
MODEL_BASIC_BRAILLE_84 = b"\x8C"
MODEL_BASIC_BRAILLE_PLUS_32 = b"\x93"
MODEL_BASIC_BRAILLE_PLUS_40 = b"\x94"
MODEL_BRAILLINO = b"\x72"
MODEL_BRAILLE_STAR_40 = b"\x74"
MODEL_BRAILLE_STAR_80 = b"\x78"
MODEL_MODULAR_20 = b"\x80"
MODEL_MODULAR_80 = b"\x88"
MODEL_MODULAR_40 = b"\x89"

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
KEY_RELEASE_MASK = 0x80

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

	def display(self, cells: List[int]):
		"""Display cells on the braille display

		This is the modern protocol, which uses an extended packet to send braille
		cells. Some displays use an older, simpler protocol. See OldProtocolMixin.
		"""
		cellBytes: bytes = bytes(cells)
		self._display.sendExtendedPacket(
			HT_EXTPKT_BRAILLE,
			cellBytes
		)

class OldProtocolMixin(object):
	"Mixin for displays using an older protocol to send braille cells and handle input"

	def display(self, cells: List[int]):
		"""Write cells to the display according to the old protocol

		This older protocol sends a simple packet starting with HT_PKT_BRAILLE,
		followed by the cells. No model ID or length are included.
		"""
		self._display.sendPacket(HT_PKT_BRAILLE, bytes(cells))


class AtcMixin(object):
	"""Support for displays with Active Tactile Control (ATC)"""

	def postInit(self):
		super(AtcMixin, self).postInit()
		log.debug("Enabling ATC")
		self._display.atc = True


class TimeSyncFirmnessMixin(object):
	"""Functionality for displays that support time synchronization and dot firmness adjustments."""

	supportedSettings=(
		braille.BrailleDisplayDriver.DotFirmnessSetting(defaultVal=1, minVal=0, maxVal=2, useConfig=False),
	)

	def postInit(self):
		super(TimeSyncFirmnessMixin, self).postInit()
		log.debug("Request current display time")
		self._display.sendExtendedPacket(HT_EXTPKT_GET_RTC)
		log.debug("Request current dot firmness")
		self._display.sendExtendedPacket(HT_EXTPKT_GET_FIRMNESS)

	def handleTime(self, timeBytes: bytes):
		try:
			displayDateTime = datetime.datetime(
				year=timeBytes[0] << 8 | timeBytes[1],
				month=timeBytes[2],
				day=timeBytes[3],
				hour=timeBytes[4],
				minute=timeBytes[5],
				second=timeBytes[6]
			)
		except ValueError:
			log.debugWarning("Invalid time/date of Handy Tech display: %r" % timeBytes)
			return
		localDateTime = datetime.datetime.today()
		if abs((displayDateTime - localDateTime).total_seconds()) >= 5:
			log.debugWarning("Display time out of sync: %s"%displayDateTime.isoformat())
			self.syncTime(localDateTime)
		else:
			log.debug("Time in sync. Display time %s"%displayDateTime.isoformat())

	def syncTime(self, dt: datetime.datetime):
		log.debug("Synchronizing braille display date and time...")
		# Setting the time uses a swapped byte order for the year.
		timeList: List[int] = [
			dt.year & 0xFF, dt.year >> 8,
			dt.month, dt.day,
			dt.hour, dt.minute, dt.second
		]
		timeBytes = bytes(timeList)
		self._display.sendExtendedPacket(HT_EXTPKT_SET_RTC, timeBytes)


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

	def display(self, cells: List[int]):
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


class EasyBraille(OldProtocolMixin, Model):
	deviceId = MODEL_EASY_BRAILLE
	numCells = 40
	genericName = name = "Easy Braille"


class ActiveBraille(TimeSyncFirmnessMixin, AtcMixin, JoystickMixin, TripleActionKeysMixin, Model):
	deviceId = MODEL_ACTIVE_BRAILLE
	numCells = 40
	genericName = name = 'Active Braille'


class ConnectBraille(TripleActionKeysMixin, Model):
	deviceId = MODEL_CONNECT_BRAILLE
	numCells = 40
	genericName = "Connect Braille"
	name = "Connect Braille"


class Actilino(TimeSyncFirmnessMixin, AtcMixin, JoystickMixin, TripleActionKeysMixin, Model):
	deviceId = MODEL_ACTILINO
	numCells = 16
	genericName = name = "Actilino"


class ActiveStar40(TimeSyncFirmnessMixin, AtcMixin, TripleActionKeysMixin, Model):
	deviceId = MODEL_ACTIVE_STAR_40
	numCells = 40
	name = "Active Star 40"
	genericName = "Active Star"


class Braillino(TripleActionKeysMixin, OldProtocolMixin, Model):
	deviceId = MODEL_BRAILLINO
	numCells = 20
	genericName = name = 'Braillino'


class BrailleWave(OldProtocolMixin, Model):
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


class BasicBraillePlus(TripleActionKeysMixin, Model):
	genericName = "Basic Braille Plus"

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
BasicBraille84 = basicBrailleFactory(84, MODEL_BASIC_BRAILLE_84)


def basicBraillePlusFactory(numCells, deviceId):
	return type("BasicBraillePlus{cells}".format(cells=numCells), (BasicBraillePlus,), {
		"deviceId": deviceId,
		"numCells": numCells,
	})


BasicBraillePlus32 = basicBraillePlusFactory(32, MODEL_BASIC_BRAILLE_PLUS_32)
BasicBraillePlus40 = basicBraillePlusFactory(40, MODEL_BASIC_BRAILLE_PLUS_40)


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


class Modular(StatusCellMixin, TripleActionKeysMixin, OldProtocolMixin, Model):
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
HT_PKT_BRAILLE = b"\x01"
HT_PKT_EXTENDED = b"\x79"
HT_PKT_NAK = b"\x7D"
HT_PKT_ACK = b"\x7E"
HT_PKT_OK = b"\xFE"
HT_PKT_RESET = b"\xFF"
HT_EXTPKT_BRAILLE = HT_PKT_BRAILLE
HT_EXTPKT_KEY = b"\x04"
HT_EXTPKT_CONFIRMATION = b"\x07"
HT_EXTPKT_SCANCODE = b"\x09"
HT_EXTPKT_PING = b"\x19"
HT_EXTPKT_SERIAL_NUMBER = b"\x41"
HT_EXTPKT_SET_RTC = b"\x44"
HT_EXTPKT_GET_RTC = b"\x45"
HT_EXTPKT_BLUETOOTH_PIN = b"\x47"
HT_EXTPKT_SET_ATC_MODE = b"\x50"
HT_EXTPKT_SET_ATC_SENSITIVITY = b"\x51"
HT_EXTPKT_ATC_INFO = b"\x52"
HT_EXTPKT_SET_ATC_SENSITIVITY_2 = b"\x53"
HT_EXTPKT_GET_ATC_SENSITIVITY_2 = b"\x54"
HT_EXTPKT_READING_POSITION = b"\x55"
HT_EXTPKT_SET_FIRMNESS = b"\x60"
HT_EXTPKT_GET_FIRMNESS = b"\x61"
HT_EXTPKT_GET_PROTOCOL_PROPERTIES = b"\xC1"
HT_EXTPKT_GET_FIRMWARE_VERSION = b"\xC2"

# HID specific constants
HT_HID_RPT_OutData = b"\x01" # receive data from device
HT_HID_RPT_InData = b"\x02" # send data to device
HT_HID_RPT_InCommand = b"\xFB" # run USB-HID firmware command
HT_HID_RPT_OutVersion = b"\xFC" # get version of USB-HID firmware
HT_HID_RPT_OutBaud = b"\xFD" # get baud rate of serial connection
HT_HID_RPT_InBaud = b"\xFE" # set baud rate of serial connection
HT_HID_CMD_FlushBuffers = b"\x01" # flush input and output buffers


class BrailleDisplayDriver(braille.BrailleDisplayDriver, ScriptableObject):
	name = "handyTech"
	# Translators: The name of a series of braille displays.
	description = _("Handy Tech braille displays")
	isThreadSafe = True
	receivesAckPackets = True
	timeout = 0.2
	_sleepcounter = 0
	_messageWindow = None
	_instances = weakref.WeakSet()

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	_dev: Optional[Union[hwIo.Hid, hwIo.Serial]]

	def __new__(cls, *args, **kwargs):
		obj = super().__new__(cls, *args, **kwargs)
		cls._instances.add(obj)
		return obj

	def __init__(self, port="auto"):
		super().__init__()
		self.numCells = 0
		self._model = None
		self._ignoreKeyReleases = False
		self._keysDown = set()
		self.brailleInput = False
		self._dotFirmness = 1
		self._hidSerialBuffer = b""
		self._atc = False

		for portType, portId, port, portInfo in self._getTryPorts(port):
			# At this point, a port bound to this display has been found.
			# Try talking to the display.
			self.isHid = portType == bdDetect.KEY_HID
			self.isHidSerial = portId in USB_IDS_HID_CONVERTER
			self.port = port
			try:
				if self.isHidSerial:
					# This is either the standalone HID adapter cable for older displays,
					# or an older display with a HID - serial adapter built in
					self._dev = hwIo.Hid(port, onReceive=self._hidSerialOnReceive)
					# Send a flush to open the serial channel
					self._dev.write(HT_HID_RPT_InCommand + HT_HID_CMD_FlushBuffers)
				elif self.isHid:
					self._dev = hwIo.Hid(port, onReceive=self._hidOnReceive)
				else:
					self._dev = hwIo.Serial(port, baudrate=BAUD_RATE, parity=PARITY,
						timeout=self.timeout, writeTimeout=self.timeout, onReceive=self._serialOnReceive)
			except EnvironmentError:
				log.debugWarning("", exc_info=True)
				continue

			self.sendPacket(HT_PKT_RESET)
			for _i in range(3):
				# An expected response hasn't arrived yet, so wait for it.
				self._dev.waitForRead(self.timeout)
				if self.numCells and self._model:
					break

			if self.numCells:
				# A display responded.
				self._model.postInit()
				log.info("Found {device} connected via {type} ({port})".format(
					device=self._model.name, type=portType, port=port))
				# Create the message window on the ui thread.
				wx.CallAfter(self.createMessageWindow)
				break
			self._dev.close()

		else:
			raise RuntimeError("No Handy Tech display found")

	@classmethod
	def createMessageWindow(cls):
		if cls._messageWindow:
			return
		try:
			cls._sleepcounter = 0
			cls._messageWindow = InvisibleDriverWindow()
		except WindowsError:
			log.debugWarning("", exc_info=True)

	@classmethod
	def destroyMessageWindow(cls):
		if len(cls._instances) > 1:
			# When switching from automatic detection to manual display selection or vice versa,
			# there could exist more than one driver instance at a time.
			# Ensure that the message window won't be destroyed in these cases.
			return
		cls._sleepcounter = 0
		try:
			cls._messageWindow.destroy()
		except WindowsError:
			log.debugWarning("", exc_info=True)
		cls._messageWindow = None

	def goToSleep(self):
		BrailleDisplayDriver._sleepcounter += 1
		if self._dev is not None:
			# Must sleep before and after closing to ensure the device can be reconnected.
			time.sleep(self.timeout)
			self._dev.close()
			self._dev = None
			time.sleep(self.timeout)

	def wakeUp(self):
		if BrailleDisplayDriver._sleepcounter > 0:
			BrailleDisplayDriver._sleepcounter -= 1
		if BrailleDisplayDriver._sleepcounter > 0:  # Still not zero after decrementing
			return
		# Might throw if device no longer exists.
		# We leave it to autodetection to grab it when it reappears.
		if self.isHidSerial:
			# This is either the standalone HID adapter cable for older displays,
			# or an older display with a HID - serial adapter built in
			self._dev = hwIo.Hid(self.port, onReceive=self._hidSerialOnReceive)
			# Send a flush to open the serial channel
			self._dev.write(HT_HID_RPT_InCommand + HT_HID_CMD_FlushBuffers)
		elif self.isHid:
			self._dev = hwIo.Hid(self.port, onReceive=self._hidOnReceive)
		else:
			self._dev = hwIo.Serial(self.port, baudrate=BAUD_RATE, parity=PARITY,
				timeout=self.timeout, writeTimeout=self.timeout, onReceive=self._serialOnReceive)

	def terminate(self):
		try:
			# Make sure this is called on the ui thread.
			wx.CallAfter(self.destroyMessageWindow)
			super().terminate()
		finally:
			# We must sleep before closing the  connection as not doing this can leave the display in a bad state where it can not be re-initialized.
			# This has been observed for Easy Braille displays.
			time.sleep(self.timeout)
			# Make sure the device gets closed.
			self._dev.close()
			# We also must sleep after closing, as it sometimes takes some time for the device to disconnect.
			# This has been observed for Active Braille displays.
			time.sleep(self.timeout)

	def _get_supportedSettings(self):
		settings = [
			braille.BrailleDisplayDriver.BrailleInputSetting(),
		]
		if self._model:
			# Add the per model supported settings to the list.
			for cls in self._model.__class__.__mro__:
				if hasattr(cls, "supportedSettings"):
					settings.extend(cls.supportedSettings)
		return settings

	def _get_atc(self):
		return self._atc

	def _set_atc(self, state):
		if self._atc is state:
			return
		if isinstance(self._model,AtcMixin):
			self.sendExtendedPacket(HT_EXTPKT_SET_ATC_MODE, boolToByte(state))
		else:
			log.debugWarning("Changing ATC setting for unsupported device %s"%self._model.name)
		# Regardless whether this setting is supported or not, we want to safe its state.
		self._atc = state

	def _get_dotFirmness(self):
		return self._dotFirmness

	def _set_dotFirmness(self, value):
		if self._dotFirmness is value:
			return
		if isinstance(self._model,TimeSyncFirmnessMixin):
			self.sendExtendedPacket(HT_EXTPKT_SET_FIRMNESS, intToByte(value))
		else:
			log.debugWarning("Changing dot firmness setting for unsupported device %s"%self._model.name)
		# Regardless whether this setting is supported or not, we want to safe its state.
		self._dotFirmness = value

	def sendPacket(self, packetType: bytes, data:bytes = b""):
		if BrailleDisplayDriver._sleepcounter > 0:
			return
		if self.isHid:
			self._sendHidPacket(packetType+data)
		else:
			self._dev.write(packetType + data)

	def sendExtendedPacket(self, packetType: bytes, data: bytes = b""):
		if BrailleDisplayDriver._sleepcounter > 0:
			log.debug("Packet discarded as driver was requested to sleep")
			return
		packetBytes: bytes = b"".join([
			intToByte(len(data) + len(packetType)),
			packetType,
			data,
			b"\x16"
		])
		if self._model:
			packetBytes = self._model.deviceId + packetBytes
		self.sendPacket(HT_PKT_EXTENDED, packetBytes)

	def _sendHidPacket(self, packet: bytes):
		assert self.isHid
		maxBlockSize = self._dev._writeSize-3
		# When the packet length exceeds C{writeSize}, the packet is split up into several packets.
		# They contain C{HT_HID_RPT_InData}, the length of the data block,
		# the data block itself and a terminating null character.
		for offset in range(0, len(packet), maxBlockSize):
			block = packet[offset:offset+maxBlockSize]
			hidPacket = HT_HID_RPT_InData + intToByte(len(block)) + block + b"\x00"
			self._dev.write(hidPacket)

	def _handleKeyRelease(self):
		if self._ignoreKeyReleases or not self._keysDown:
			return
		# The first key released executes the key combination.
		try:
			inputCore.manager.executeGesture(
				InputGesture(self._model, self._keysDown, self.brailleInput))
		except inputCore.NoInputGestureAction:
			pass
		# Any further releases are just the rest of the keys in the combination
		# being released, so they should be ignored.
		self._ignoreKeyReleases = True

	def _hidOnReceive(self, data: bytes):
		# data contains the entire packet.
		stream = BytesIO(data)
		htPacketType = data[2:3]
		# Skip the header, so reading the stream will only give the rest of the data
		stream.seek(3)
		self._handleInputStream(htPacketType, stream)

	def _hidSerialOnReceive(self, data: bytes):
		# The HID serial converter wraps one or two bytes into a single HID packet
		hidLength = data[1]
		self._hidSerialBuffer+=data[2:(2+hidLength)]
		self._processHidSerialBuffer()

	def _processHidSerialBuffer(self):
		while self._hidSerialBuffer:
			currentBufferLength=len(self._hidSerialBuffer)
			htPacketType: bytes = self._hidSerialBuffer[0:1]
			if htPacketType!=HT_PKT_EXTENDED:
				packetLength = 2 if htPacketType==HT_PKT_OK else 1
				if currentBufferLength>=packetLength:
					stream = BytesIO(self._hidSerialBuffer[:packetLength])
					self._hidSerialBuffer: bytes = self._hidSerialBuffer[packetLength:]
				else:
					# The packet is not yet complete
					return
			elif htPacketType==HT_PKT_EXTENDED and currentBufferLength>=5:
				# Check whether our packet is complete
				# Extended packets are at least 5 bytes in size.
				# The second byte is the model, the third byte is the data length, excluding the terminator
				packet_length = self._hidSerialBuffer[2]+4
				if len(self._hidSerialBuffer)<packet_length:
					# The packet is not yet complete
					return
				# We have a complete packet.
				# We also isolate it from another packet that could have landed in the buffer,
				stream = BytesIO(self._hidSerialBuffer[:packet_length])
				self._hidSerialBuffer: bytes = self._hidSerialBuffer[packet_length:]
				if len(self._hidSerialBuffer)==packet_length:
					assert self._hidSerialBuffer.endswith(b"\x16"), "Extended packet terminator expected"
			else:
				# The packet is not yet complete
				return
			stream.seek(1)
			self._handleInputStream(htPacketType, stream)

	def _serialOnReceive(self, data: bytes):
		self._handleInputStream(data, self._dev)

	def _handleInputStream(self, htPacketType: bytes, stream):
		if htPacketType in (HT_PKT_OK, HT_PKT_EXTENDED):
			modelId: bytes = stream.read(1)
			if not self._model:
				if modelId not in MODELS:
					log.debugWarning("Unknown model: %r" % modelId)
					raise RuntimeError(
						"The model with ID %r is not supported by this driver" % modelId)
				self._model = MODELS.get(modelId)(self)
				self.numCells = self._model.numCells
			elif self._model.deviceId != modelId:
				# Somehow the model ID of this display changed, probably another display 
				# plugged in the same (already open) serial port.
				self.terminate()

		if htPacketType==HT_PKT_OK:
			pass
		elif htPacketType == HT_PKT_ACK:
			# This is unexpected, but we need to make sure that we handle old style ack
			self._handleAck()
		elif htPacketType == HT_PKT_NAK:
			log.debugWarning("NAK received!")
		elif htPacketType == HT_PKT_EXTENDED:
			packet_length = ord(stream.read(1))
			packet: bytes = stream.read(packet_length)
			terminator: bytes = stream.read(1)
			assert terminator == b"\x16"	# Extended packets are terminated with \x16
			extPacketType = packet[0:1]
			if extPacketType == HT_EXTPKT_CONFIRMATION:
				# Confirmation of a command.
				if packet[1:2] == HT_PKT_ACK:
					self._handleAck()
				elif packet[1:2] == HT_PKT_NAK:
					log.debugWarning("NAK received!")
			elif extPacketType == HT_EXTPKT_KEY:
				self._handleInput(packet[1])
			elif extPacketType == HT_EXTPKT_ATC_INFO:
				# Ignore ATC packets for now
				pass
			elif extPacketType == HT_EXTPKT_GET_PROTOCOL_PROPERTIES:
				pass
			elif isinstance(self._model, TimeSyncFirmnessMixin):
				if extPacketType == HT_EXTPKT_GET_RTC:
					self._model.handleTime(packet[1:])
				elif extPacketType == HT_EXTPKT_GET_FIRMNESS:
					self._dotFirmness = packet[1]
			else:
				# Unknown extended packet, log it
				log.debugWarning("Unhandled extended packet of type %r: %r" %
					(extPacketType, packet))
		else:
			serPacketOrd = ord(htPacketType)
			if isinstance(self._model, OldProtocolMixin) and serPacketOrd&~KEY_RELEASE_MASK < ord(HT_PKT_EXTENDED):
				self._handleInput(serPacketOrd)
			else:
				# Unknown packet type, log it
				log.debugWarning("Unhandled packet of type %r" % htPacketType)


	def _handleInput(self, key: int):
		release = (key & KEY_RELEASE_MASK) != 0
		if release:
			key ^= KEY_RELEASE_MASK
			self._handleKeyRelease()
			self._keysDown.discard(key)
		else:
			# Press.
			# This begins a new key combination.
			self._ignoreKeyReleases = False
			self._keysDown.add(key)


	def display(self, cells: List[int]):
		# cells will already be padded up to numCells.
		self._model.display(cells)

	scriptCategory = SCRCAT_BRAILLE

	def script_toggleBrailleInput(self, _gesture):
		self.brailleInput = not self.brailleInput
		if self.brailleInput:
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
		'br(handytech):space+dot1+dot2+dot7': 'toggleBrailleInput',
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


class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, model, keys, isBrailleInput=False):
		super(InputGesture, self).__init__()
		self.model = model.genericName.replace(" ","")
		self.keys = set(keys)

		self.keyNames = names = []
		if isBrailleInput:
			self.dots = self._calculateDots()
		for key in keys:
			if isBrailleInput and (
				key in KEY_SPACES or (key in (KEY_LEFT, KEY_RIGHT) and isinstance(model,EasyBraille))
			):
				self.space = True
				names.append("space")
			elif isBrailleInput and key in KEY_DOTS:
				names.append("dot%d"%KEY_DOTS[key])
			elif KEY_ROUTING <= key < KEY_ROUTING + model.numCells:
				self.routingIndex = key - KEY_ROUTING
				names.append("routing")
			else:
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
