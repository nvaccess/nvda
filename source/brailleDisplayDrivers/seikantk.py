# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2021 NV Access Limited, Ulf Beckmann <beckmann@flusoft.de>
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
#
# This file represents the braille display driver for
# Seika Notetaker, a product from Nippon Telesoft
# see www.seika-braille.com for more details
# Driver information can be found in .\devDocs\brailleDrivers\SeikaNotetaker.md

from io import BytesIO
import typing
from typing import List, Set

import braille
import brailleInput
import inputCore
import hwPortUtils
import bdDetect
import hwIo
from serial.win32 import INVALID_HANDLE_VALUE
from logHandler import log

MAX_READ_ATTEMPTS = 30
READ_TIMEOUT_SECS = 0.2

DOT_1 = 0x1
DOT_2 = 0x2
DOT_3 = 0x4
DOT_4 = 0x8
DOT_5 = 0x10
DOT_6 = 0x20
DOT_7 = 0x40
DOT_8 = 0x80


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

SEIKA_REQUEST_INFO = b"\x03\xff\xff\xa1"
SEIKA_INFO = b"\xff\xff\xa2"
SEIKA_SEND_TEXT = b"\x2c\xff\xff\xa3"
SEIKA_ROUTING = b"\xff\xff\xa4"
SEIKA_KEYS = b"\xff\xff\xa6"
SEIKA_KEYS_ROU = b"\xff\xff\xa8"

SEIKA_CONFIG = b"\x50\x00\x00\x25\x80\x00\x00\x03\x00"
SEIKA_CMD_ON = b"\x41\x01"

vidpid = "VID_10C4&PID_EA80"
hidvidpid = "HID\\VID_10C4&PID_EA80"
SEIKA_NAME = "seikantk"


def _getDotNames():
	dotNames = {}
	for dotNum in range(1, 9):
		keyName = globals()[f"DOT_{dotNum}"]
		dotNames[keyName] = f"d{dotNum}"
	return dotNames


_dotNames = _getDotNames()
bdDetect.addUsbDevices(SEIKA_NAME, bdDetect.KEY_HID, {vidpid, })


class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	_dev: hwIo.IoBase
	name = SEIKA_NAME
	# Translators: Name of a braille display.
	description = _("Seika Notetaker")
	path = ""
	isThreadSafe = True
	for d in hwPortUtils.listHidDevices():
		if d["hardwareID"].startswith(hidvidpid):
			path = d["devicePath"]

	@classmethod
	def check(cls):
		return True

	@classmethod
	def getManualPorts(cls):
		return cls.path

	def __init__(self, port="hid"):
		super().__init__()
		self.numCells = 0
		self.numBtns = 0
		self.numRoutingKeys = 0
		self.handle = None

		self._hidBuffer = b""
		self._command: typing.Optional[bytes] = None
		self._argsLen: typing.Optional[int] = None
		log.info(f"Seika Notetaker braille driver path: {self.path}")

		if self.path == "":
			raise RuntimeError("No MINI-SEIKA display found, no path found")
		self._dev = dev = hwIo.Hid(path=self.path, onReceive=self._onReceive)
		if dev._file == INVALID_HANDLE_VALUE:
			raise RuntimeError("No MINI-SEIKA display found, open error")
		dev.setFeature(SEIKA_CONFIG)  # baud rate, stop bit usw
		dev.setFeature(SEIKA_CMD_ON)  # device on
		dev.write(SEIKA_REQUEST_INFO)  # Request the Info from the device

		# wait and try to get info from the Braille display
		for i in range(MAX_READ_ATTEMPTS):  # the info-block is about
			dev.waitForRead(READ_TIMEOUT_SECS)
			if self.numCells:
				log.info(
					f"Seika notetaker on USB-HID,"
					f" Cells {self.numCells}"
					f" Buttons {self.numBtns}"
				)
				break

		if self.numCells == 0:
			dev.close()
			raise RuntimeError("No MINI-SEIKA display found, no response")

	def terminate(self):
		try:
			super().terminate()
		finally:
			self._dev.close()

	def display(self, cells: List[int]):
		# cells will already be padded up to numCells.
		cellBytes = SEIKA_SEND_TEXT + self.numCells.to_bytes(1, 'little') + bytes(cells)
		self._dev.write(cellBytes)

	def _onReceive(self, data: bytes):
		"""
		Note: Further insight into this function would be greatly appreciated.
		This function is a very simple state machine, each stage represents the collection of a field, when all
		fields are collected the command they represent can be processed.

		On each call to _onReceive three bytes are read from the device.
		The first and third bytes are discarded, the second byte is appended to a buffer.
		The buffer is accumulated until the buffer has the required number of bytes for the field being collected.
		There are 3 fields to be collected before a command can be processed:
		1: first 3 bytes: command
		2: 1 byte: specify length of subsequent arguments in bytes
		3: variable length: arguments for command type

		After accumulating enough bytes for each phase, the buffer is cleared and the next stage is entered.
		"""
		COMMAND_LEN = 3
		stream = BytesIO(data)
		cmd = stream.read(3)  # Note, first and third bytes are discarded
		newByte: bytes = cmd[1:2]  # use range to return bytes
		self._hidBuffer += newByte
		hasCommandBeenCollected = self._command is not None
		hasArgLenBeenCollected = self._argsLen is not None
		if (  # still collecting command bytes
			not hasCommandBeenCollected
			and len(self._hidBuffer) == COMMAND_LEN
		):
			self._command = self._hidBuffer  # command found reset and wait for args length
			self._hidBuffer = b""
		elif (  # next byte gives the command + args length
			hasCommandBeenCollected
			and not hasArgLenBeenCollected  # argsLen has not
		):
			# the data is sent with the following structure
			# - command name (3 bytes)
			# - number of subsequent bytes to read (1 byte)
			# - Args (variable bytes)
			self._argsLen = ord(newByte)
			self._hidBuffer = b""
		elif (  # now collect the args,
			hasCommandBeenCollected
			and hasArgLenBeenCollected
			and len(self._hidBuffer) == self._argsLen
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
			self._handInfo(arg)
		elif command == SEIKA_ROUTING:
			self._handRouting(arg)
		elif command == SEIKA_KEYS:
			self._handKeys(arg)
		elif command == SEIKA_KEYS_ROU:
			self._handKeysRouting(arg)
		else:
			log.warning(f"Seika device has received an unknown command {command}")

	def _handInfo(self, arg: bytes):
		self.numBtns = arg[0]
		self.numCells = arg[1]
		self.numRoutingKeys = arg[2]
		self._description = arg[3:].decode("ascii")

	def _handRouting(self, arg: bytes):
		routingIndexes = _getRoutingIndexes(arg)
		for routingIndex in routingIndexes:
			gesture = InputGestureRouting(routingIndex)
			try:
				inputCore.manager.executeGesture(gesture)
			except inputCore.NoInputGestureAction:
				log.debug("No action for Seika Notetaker routing command")

	def _handKeys(self, arg: bytes):
		brailleDots = arg[0]
		key = arg[1] | (arg[2] << 8)
		gestures = []
		if key:
			gestures.append(InputGesture(keys=key))
		if brailleDots:
			gestures.append(InputGesture(dots=brailleDots))
		for gesture in gestures:
			try:
				inputCore.manager.executeGesture(gesture)
			except inputCore.NoInputGestureAction:
				log.debug("No action for Seika Notetaker keys.") 

	def _handKeysRouting(self, arg: bytes):
		self._handRouting(arg[3:])
		self._handKeys(arg[:3])

	gestureMap = inputCore.GlobalGestureMap({
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
			"kb:space": ("br(seikantk):BACKSPACE", "br(seikantk):SPACE",),
			"kb:backspace": ("br(seikantk):d7",),
			"kb:pageup": ("br(seikantk):SPACE+LJ_RIGHT",),
			"kb:pagedown": ("br(seikantk):SPACE+LJ_LEFT",),
			"kb:home": ("br(seikantk):SPACE+LJ_UP",),
			"kb:end": ("br(seikantk):SPACE+LJ_DOWN",),
			"kb:control+home": ("br(seikantk):BACKSPACE+LJ_UP",),
			"kb:control+end": ("br(seikantk):BACKSPACE+LJ_DOWN",),
			"kb:enter": ("br(seikantk):RJ_CENTER", "br(seikantk):d8"),
		},
	})


class InputGestureRouting(braille.BrailleDisplayGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, index):
		super().__init__()
		self.id = "routing"
		self.routingIndex = index


def _getKeyNames(keys: int) -> Set[int]:
	return {_keyNames[1 << i] for i in range(16) if (1 << i) & keys}


def _getDotNames(dots: int) -> Set[int]:
	return {_dotNames[1 << i] for i in range(8) if (1 << i) & dots}


def _getRoutingIndexes(routingKeys: bytes) -> Set[int]:
	return {i * 8 + j for i in range(len(routingKeys)) for j in range(8) if routingKeys[i] & (1 << j)}


class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, keys=None, dots=None, space=False, routing=None):
		super(braille.BrailleDisplayGesture, self).__init__()
		# see what thumb keys are pressed:
		names = set()
		if keys is not None:
			names.update(_getKeyNames(keys))
		elif dots is not None:
			self.dots = dots
			if space:
				self.space = space
				names.add(_keyNames[1])
			names.update(_getDotNames(dots))
		elif routing is not None:
			self.routingIndex = routing
			names.add('routing')
		self.id = "+".join(names)
