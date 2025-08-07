# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2012-2023 NV Access Limited, Ulf Beckmann <beckmann@flusoft.de>

"""
Braille display driver for Seika Notetaker, a product from Nippon Telesoft
see www.seika-braille.com for more details
"""

import re
from io import BytesIO
import typing
from typing import Dict, List, Optional, Set

import serial

import braille
from bdDetect import DeviceMatch, DriverRegistrar
import brailleInput
import inputCore
import bdDetect
import hwIo
from serial.win32 import INVALID_HANDLE_VALUE
from logHandler import log

MAX_READ_ATTEMPTS = 30
READ_TIMEOUT_SECS = 0.2

_keyNames = {
	0x000001: "BACKSPACE",
	0x000002: "SPACE",
	0x000004: "LB",
	0x000008: "RB",
	0x000010: "LJ_CENTER",
	0x000020: "LJ_LEFT",
	0x000040: "LJ_RIGHT",
	0x000080: "LJ_UP",
	0x000100: "LJ_DOWN",
	0x000200: "RJ_CENTER",
	0x000400: "RJ_LEFT",
	0x000800: "RJ_RIGHT",
	0x001000: "RJ_UP",
	0x002000: "RJ_DOWN",
}
_dotNames = {
	0x1: "d1",
	0x2: "d2",
	0x4: "d3",
	0x8: "d4",
	0x10: "d5",
	0x20: "d6",
	0x40: "d7",
	0x80: "d8",
}

SEIKA_REQUEST_INFO = b"\x03\xff\xff\xa1"
SEIKA_INFO = b"\xff\xff\xa2"
SEIKA_SEND_TEXT = b"\x2c\xff\xff\xa3"
SEIKA_ROUTING = b"\xff\xff\xa4"
SEIKA_KEYS = b"\xff\xff\xa6"
SEIKA_KEYS_ROU = b"\xff\xff\xa8"

BAUD = 9600
SEIKA_HID_FEATURES = b"".join(
	[
		b"\x50\x00\x00",
		int.to_bytes(BAUD, length=2, byteorder="big", signed=False),  # b"\x25\x80"
		b"\x00\x00\x03\x00",
	],
)
SEIKA_CMD_ON = b"\x41\x01"
""" Unknown why this is required. Used for HID (via setFeature), but not for serial.
"""

vidpid = "VID_10C4&PID_EA80"
hidvidpid = "HID\\VID_10C4&PID_EA80"
SEIKA_NAME = "seikantk"

# Bluetooth name of the Seika devices is "TSM abcd", where the "abcd" is a four-digit
# number, e.g. "TSM 3366", "TSM 0001", etc. There is a space between "TSM" and "abcd".
seikaBluetoothNameRegex = re.compile(r"TSM \d\d\d\d")


def isSeikaBluetoothName(bluetoothName: str) -> bool:
	return bool(seikaBluetoothNameRegex.match(bluetoothName))


def isSeikaBluetoothDeviceInfo(deviceInfo: typing.Dict[str, str]) -> bool:
	# bluetoothName is listed in information from L{hwPortUtils.listComPorts} when 'hwIo' debug logging
	# category is enabled.
	btNameKey = "bluetoothName"
	return btNameKey in deviceInfo and isSeikaBluetoothName(deviceInfo["bluetoothName"])


def isSeikaBluetoothDeviceMatch(match: DeviceMatch) -> bool:
	return isSeikaBluetoothDeviceInfo(match.deviceInfo)


class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = SEIKA_NAME
	# Translators: Name of a braille display.
	description = _("Seika Notetaker")
	isThreadSafe = True
	supportsAutomaticDetection = True

	@classmethod
	def registerAutomaticDetection(cls, driverRegistrar: DriverRegistrar):
		driverRegistrar.addUsbDevices(
			bdDetect.ProtocolType.HID,
			{
				vidpid,  # Seika Notetaker
			},
		)

		driverRegistrar.addBluetoothDevices(isSeikaBluetoothDeviceMatch)

	@classmethod
	def getManualPorts(cls) -> typing.Iterator[typing.Tuple[str, str]]:
		"""@return: An iterator containing the name and description for each port."""
		return braille.getSerialPorts(isSeikaBluetoothDeviceInfo)

	def __init__(self, port: typing.Union[None, str, DeviceMatch]):
		super().__init__()
		self.numCells = 0
		self.numBtns = 0
		self.numRoutingKeys = 0
		self.handle = None
		self._hidBuffer = b""
		self._command: typing.Optional[bytes] = None
		self._argsLen: typing.Optional[int] = None
		self._dev: Optional[hwIo.IoBase] = None

		log.debug(f"Seika Notetaker braille driver: ({port!r})")
		dev: typing.Optional[typing.Union[hwIo.Hid, hwIo.Serial]] = None
		for match in self._getTryPorts(port):
			self.isHid = match.type == bdDetect.ProtocolType.HID
			self.isSerial = match.type == bdDetect.ProtocolType.SERIAL
			try:
				if self.isHid:
					log.info("Trying Seika notetaker on USB-HID")
					self._dev = dev = hwIo.Hid(
						path=match.port,  # for a Hid match type 'port' is actually 'path'.
						onReceive=self._onReceiveHID,
					)
					dev.setFeature(SEIKA_HID_FEATURES)  # baud rate, stop bit usw
					dev.setFeature(SEIKA_CMD_ON)  # device on
				elif self.isSerial:
					log.info(f"Trying Seika notetaker on Bluetooth (serial) port:{match.port}")
					self._dev = dev = hwIo.Serial(
						port=match.port,
						onReceive=self._onReceiveSerial,
						baudrate=BAUD,
						parity=serial.PARITY_NONE,
						bytesize=serial.EIGHTBITS,
						stopbits=serial.STOPBITS_ONE,
					)
					# Note: SEIKA_CMD_ON not sent as per USB-HID, testing from users hasn't indicated any problems.
					# The exact purpose of SEIKA_CMD_ON isn't known/documented here.
				else:
					log.debug(f"Port type not handled: {match.type}")
					continue
			except EnvironmentError:
				log.debugWarning("", exc_info=True)
				continue
			if self._getDeviceInfo(dev):
				break
			elif dev:
				dev.close()
				dev = None

		if not dev:
			RuntimeError("No MINI-SEIKA display found")
		elif self.numCells == 0:
			dev.close()
			dev = None
			raise RuntimeError("No MINI-SEIKA display found, no response")
		else:
			log.info(
				f"Seika notetaker, Cells {self.numCells} Buttons {self.numBtns}",
			)

	def _getDeviceInfo(self, dev: hwIo.IoBase) -> bool:
		if not dev or dev._file == INVALID_HANDLE_VALUE:
			log.debug("No MINI-SEIKA display found, open error")
			return False

		dev.write(SEIKA_REQUEST_INFO)  # Request the Info from the device

		# wait and try to get info from the Braille display
		for i in range(MAX_READ_ATTEMPTS):  # the info-block is about
			dev.waitForRead(READ_TIMEOUT_SECS)
			if self.numCells:
				return True
		return False

	def terminate(self):
		try:
			super().terminate()
		finally:
			if self._dev is None:
				log.debugWarning("Seika Notetaker driver not initialized when attempting to terminate")
				return
			self._dev.close()

	def display(self, cells: List[int]):
		if self._dev is None:
			log.debugWarning("Seika Notetaker driver not initialized when attempting to display")
			return
		# cells will already be padded up to numCells.
		cellBytes = SEIKA_SEND_TEXT + bytes([self.numCells]) + bytes(cells)
		self._dev.write(cellBytes)

	def _onReceiveHID(self, data: bytes):
		"""Three bytes at a time expected, only the middle byte is used to construct the command, the first
		and third byte are discarded.
		"""
		stream = BytesIO(data)
		cmd = stream.read(3)  # Note, first and third bytes are discarded
		newByte: bytes = cmd[1:2]  # use range to return bytes type, containing only index 1
		self._onReceive(newByte)

	def _onReceiveSerial(self, data: bytes):
		"""One byte at a time is expected"""
		self._onReceive(data)

	def _onReceive(self, newByte: bytes):
		"""
		Note: Further insight into this function would be greatly appreciated.
		This function is a very simple state machine, each stage represents the collection of a field, when all
		fields are collected the command they represent can be processed.

		On each call to _onReceive the new byte is appended to a buffer.
		The buffer is accumulated until the buffer has the required number of bytes for the field being collected.
		There are 3 fields to be collected before a command can be processed:
		1: first 3 bytes: command
		2: 1 byte: specify length of subsequent arguments in bytes
		3: variable length: arguments for command type

		After accumulating enough bytes for each phase, the buffer is cleared and the next stage is entered.
		"""
		COMMAND_LEN = 3
		self._hidBuffer += newByte
		hasCommandBeenCollected = self._command is not None
		hasArgLenBeenCollected = self._argsLen is not None
		if (  # still collecting command bytes
			not hasCommandBeenCollected and len(self._hidBuffer) == COMMAND_LEN
		):
			self._command = self._hidBuffer  # command found reset and wait for args length
			self._hidBuffer = b""
		elif (  # next byte gives the command + args length
			hasCommandBeenCollected and not hasArgLenBeenCollected  # argsLen has not
		):
			# the data is sent with the following structure
			# - command name (3 bytes)
			# - number of subsequent bytes to read (1 byte)
			# - Args (variable bytes)
			self._argsLen = ord(newByte)
			self._hidBuffer = b""
		elif (  # now collect the args,
			hasCommandBeenCollected and hasArgLenBeenCollected and len(self._hidBuffer) == self._argsLen
		):
			arg = self._hidBuffer
			command = self._command

			# reset state variables
			self._command = None
			self._argsLen = None
			self._hidBuffer = b""
			self._processCommand(command, arg)

	def _processCommand(self, command: bytes, arg: bytes) -> None:
		if command == SEIKA_INFO:
			self._handleInfo(arg)
		elif command == SEIKA_ROUTING:
			self._handleRouting(arg)
		elif command == SEIKA_KEYS:
			self._handleKeys(arg)
		elif command == SEIKA_KEYS_ROU:
			self._handleKeysRouting(arg)
		else:
			log.warning(f"Seika device has received an unknown command {command}")

	def _handleInfo(self, arg: bytes):
		"""After sending a request for information from the braille device this data is returned to complete
		the handshake.
		"""
		self.numBtns = arg[0]
		self.numCells = arg[1]
		self.numRoutingKeys = arg[2]
		try:
			self._description = arg[3:].decode("ascii")
		except UnicodeDecodeError:
			log.debugWarning(f"Unable to decode Seika Notetaker description {arg[3:]}")

	def _handleRouting(self, arg: bytes):
		routingIndexes = _getRoutingIndexes(arg)
		for routingIndex in routingIndexes:
			gesture = InputGestureRouting(routingIndex)
			try:
				inputCore.manager.executeGesture(gesture)
			except inputCore.NoInputGestureAction:
				log.debug("No action for Seika Notetaker routing command")

	def _handleKeys(self, arg: bytes):
		brailleDots = arg[0]
		key = arg[1] | (arg[2] << 8)
		gestures = []
		if brailleDots:
			if key in (1, 2, 3):  # bk:space+dots
				gestures.append(InputGesture(dots=brailleDots, space=key))
				key = 0
			else:  # bk:dots
				gestures.append(InputGesture(dots=brailleDots, space=0))
		if key:
			if key in (1, 2):  # bk:space
				gestures.append(InputGesture(dots=0, space=key))
			else:  # br(seikantk):XXX
				gestures.append(InputGesture(keys=key))
		for gesture in gestures:
			try:
				inputCore.manager.executeGesture(gesture)
			except inputCore.NoInputGestureAction:
				log.debug("No action for Seika Notetaker keys.")

	def _handleKeysRouting(self, arg: bytes):
		self._handleRouting(arg[3:])
		self._handleKeys(arg[:3])

	gestureMap = inputCore.GlobalGestureMap(
		{
			"globalCommands.GlobalCommands": {
				"braille_routeTo": ("br(seikantk):routing",),
				"braille_scrollBack": ("br(seikantk):LB",),
				"braille_scrollForward": ("br(seikantk):RB",),
				"braille_previousLine": ("br(seikantk):LJ_UP",),
				"braille_nextLine": ("br(seikantk):LJ_DOWN",),
				"braille_toggleTether": ("br(seikantk):LJ_CENTER",),
				"sayAll": ("br(seikantk):SPACE+BACKSPACE",),
				"showGui": ("br(seikantk):RB+LB",),
				"kb:tab": ("br(seikantk):LJ_RIGHT",),
				"kb:shift+tab": ("br(seikantk):LJ_LEFT",),
				"kb:upArrow": ("br(seikantk):RJ_UP",),
				"kb:downArrow": ("br(seikantk):RJ_DOWN",),
				"kb:leftArrow": ("br(seikantk):RJ_LEFT",),
				"kb:rightArrow": ("br(seikantk):RJ_RIGHT",),
				"kb:shift+upArrow": ("br(seikantk):SPACE+RJ_UP", "br(seikantk):BACKSPACE+RJ_UP"),
				"kb:shift+downArrow": ("br(seikantk):SPACE+RJ_DOWN", "br(seikantk):BACKSPACE+RJ_DOWN"),
				"kb:shift+leftArrow": ("br(seikantk):SPACE+RJ_LEFT", "br(seikantk):BACKSPACE+RJ_LEFT"),
				"kb:shift+rightArrow": ("br(seikantk):SPACE+RJ_RIGHT", "br(seikantk):BACKSPACE+RJ_RIGHT"),
				"kb:escape": ("br(seikantk):SPACE+RJ_CENTER",),
				"kb:windows": ("br(seikantk):BACKSPACE+RJ_CENTER",),
				"kb:backspace": ("br(seikantk):d7",),
				"kb:pageup": ("br(seikantk):SPACE+LJ_RIGHT",),
				"kb:pagedown": ("br(seikantk):SPACE+LJ_LEFT",),
				"kb:home": ("br(seikantk):SPACE+LJ_UP",),
				"kb:end": ("br(seikantk):SPACE+LJ_DOWN",),
				"kb:control+home": ("br(seikantk):BACKSPACE+LJ_UP",),
				"kb:control+end": ("br(seikantk):BACKSPACE+LJ_DOWN",),
				"kb:enter": ("br(seikantk):RJ_CENTER", "br(seikantk):d8"),
			},
		},
	)


class InputGestureRouting(braille.BrailleDisplayGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, index):
		super().__init__()
		self.id = "routing"
		self.routingIndex = index


def _getKeyNames(keys: int, names: Dict[int, str]) -> Set[str]:
	"""Converts a bitset of hardware buttons and keys to their equivalent names"""
	return {keyName for bitFlag, keyName in names.items() if bitFlag & keys}


def _getRoutingIndexes(routingKeyBytes: bytes) -> Set[int]:
	"""Converts a bitset of routing keys to their 0-index, up to 15 or 39 depending on the device"""
	bitsPerByte = 8
	# Convert bytes into a single bitset int
	combinedRoutingKeysBitSet = sum(
		[value << (bitsPerByte * bitIndex) for bitIndex, value in enumerate(routingKeyBytes)],
	)
	numRoutingKeys = len(routingKeyBytes) * bitsPerByte
	return {i for i in range(numRoutingKeys) if (1 << i) & combinedRoutingKeysBitSet}


class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, keys=None, dots=None, space=0, routing=None):
		super(braille.BrailleDisplayGesture, self).__init__()
		# see what thumb keys are pressed:
		names = set()
		if keys is not None:
			names.update(_getKeyNames(keys, _keyNames))
		elif dots is not None:
			self.dots = dots
			if space:
				self.space = bool(space)
				names.update(_getKeyNames(space, _keyNames))
			names.update(_getKeyNames(dots, _dotNames))
		elif routing is not None:
			self.routingIndex = routing
			names.add("routing")
		self.id = "+".join(names)
