# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Zoomax
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# NLS eReader Zoomax driver for NVDA.

import bdDetect
import braille
import brailleInput
import hwIo
import inputCore
import serial
import time
from dataclasses import dataclass
from enum import Enum
from logHandler import log
from typing import Optional, Tuple, Dict

TIMEOUT_SEC = 0.2
BAUD_RATE = 19200
CONNECT_RETRIES = 5
TIMEOUT_BETWEEN_RETRIES_SEC = 2

COMMUNICATION_ESCAPE_BYTE = b"\x1b"


class DeviceCommand(bytes, Enum):
	DISPLAY_DATA = b"\x01"
	REQUEST_INFO = b"\x02"
	REQUEST_VERSION = b"\x05"
	REPEAT_ALL = b"\x08"
	PROTOCOL_ONOFF = b"\x15"
	ROUTING_KEYS = b"\x22"
	DISPLAY_KEYS = b"\x24"
	BRAILLE_KEYS = b"\x33"
	JOYSTICK_KEYS = b"\x34"
	DEVICE_ID = b"\x84"
	SERIAL_NUMBER = b"\x8a"


@dataclass(frozen=True)
class DeviceResponseInfo:
	length: int
	keys: Optional[Tuple[str, ...]] = None


COMMAND_RESPONSE_INFO: Dict[DeviceCommand, DeviceResponseInfo] = {
	DeviceCommand.DISPLAY_DATA: DeviceResponseInfo(1),
	DeviceCommand.DISPLAY_KEYS: DeviceResponseInfo(
		1,
		("d1", "d2", "d3", "d4", "d5", "d6"),
	),
	DeviceCommand.BRAILLE_KEYS: DeviceResponseInfo(
		2,
		(
			"bl",
			"br",
			"bs",
			None,
			"s1",
			"s2",
			"s3",
			"s4",  # byte 1
			"b1",
			"b2",
			"b3",
			"b4",
			"b5",
			"b6",
			"b7",
			"b8",  # byte 2
		),
	),
	DeviceCommand.JOYSTICK_KEYS: DeviceResponseInfo(
		1,
		("up", "left", "down", "right", "select"),
	),
	DeviceCommand.ROUTING_KEYS: DeviceResponseInfo(5),
	DeviceCommand.DEVICE_ID: DeviceResponseInfo(16),
	DeviceCommand.SERIAL_NUMBER: DeviceResponseInfo(8),
}


class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	_dev: hwIo.IoBase
	name = "nlseReaderZoomax"
	# Translators: Names of braille displays.
	description = _("NLS eReader Zoomax")
	isThreadSafe = True
	supportsAutomaticDetection = True

	@classmethod
	def registerAutomaticDetection(cls, driverRegistrar: bdDetect.DriverRegistrar):
		driverRegistrar.addUsbDevices(
			bdDetect.DeviceType.SERIAL,
			{
				"VID_1A86&PID_7523",  # CH340 USB to serial chip
			},
		)

		driverRegistrar.addBluetoothDevices(lambda m: m.id.startswith("NLS eReader Z"))

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	def _connect(self, port: str) -> None:
		for portType, portId, port, portInfo in self._getTryPorts(port):
			try:
				self._dev = hwIo.Serial(
					port,
					baudrate=BAUD_RATE,
					bytesize=serial.EIGHTBITS,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					timeout=TIMEOUT_SEC,
					writeTimeout=TIMEOUT_SEC,
					onReceive=self._onReceive,
				)
			except EnvironmentError:
				log.info("Port not yet available.")
				log.debugWarning("", exc_info=True)
				if self._dev:
					self._dev.close()
				continue

			self._sendRequest(DeviceCommand.PROTOCOL_ONOFF.value, False)
			self._sendRequest(DeviceCommand.PROTOCOL_ONOFF.value, True)
			self._sendRequest(DeviceCommand.REPEAT_ALL.value)

			for i in range(CONNECT_RETRIES):
				self._dev.waitForRead(TIMEOUT_SEC)
				if self.numCells:
					break

			if self.numCells:
				log.info(f"Device connected via {portType} ({port})")
				return True
			log.info("Device arrival timeout")
			self._dev.close()
		return False

	def __init__(self, port: str = "auto"):
		log.info("Initializing nlseReaderZoomax driver")
		super().__init__()
		self.numCells = 0
		self._deviceID: str | None = None
		self._dev = None

		for i in range(CONNECT_RETRIES):
			if self._connect(port):
				break
			else:
				time.sleep(TIMEOUT_BETWEEN_RETRIES_SEC)

		self._keysDown = {}
		self._ignoreKeyReleases = False

	def terminate(self):
		try:
			super().terminate()
			self._sendRequest(DeviceCommand.PROTOCOL_ONOFF, False)
		except EnvironmentError:
			pass
		finally:
			self._dev.close()

	def _sendRequest(self, command: bytes, arg: bytes | bool | int = b""):
		typeErrorString = "Expected param '{}' to be of type '{}', got '{}'"
		if not isinstance(arg, bytes):
			if isinstance(arg, bool):
				arg = hwIo.boolToByte(arg)
			elif isinstance(arg, int):
				arg = hwIo.intToByte(arg)
			else:
				raise TypeError(typeErrorString.format("arg", "bytes, bool, or int", type(arg).__name__))

		if not isinstance(command, bytes):
			raise TypeError(typeErrorString.format("command", "bytes", type(command).__name__))

		# doubling the escape characters in the data (arg) part
		# as requried by the device communication protocol
		arg = arg.replace(COMMUNICATION_ESCAPE_BYTE, COMMUNICATION_ESCAPE_BYTE * 2)

		data = b"".join(
			[
				COMMUNICATION_ESCAPE_BYTE,
				command,
				arg,
			],
		)
		self._dev.write(data)

	def _onReceive(self, data: bytes):
		if data != COMMUNICATION_ESCAPE_BYTE:
			log.debugWarning(f"Ignoring byte before escape: {data!r}")
			return
		# data only contained the escape. Read the rest from the device.
		stream = self._dev
		command = stream.read(1)
		length = COMMAND_RESPONSE_INFO.get(command, DeviceResponseInfo(0)).length
		arg = stream.read(length)
		self._handleResponse(command, arg)

	def _handleResponse(self, command: bytes, arg: bytes):
		if command == DeviceCommand.DISPLAY_DATA:
			self.numCells = ord(arg)
		elif command == DeviceCommand.DEVICE_ID:
			# Short ids can be padded with either nulls or spaces.
			arg = arg.rstrip(b"\0 ")
			# Assumption: all device IDs can be decoded with latin-1.
			# If not, we wish to know about it, allow decode to raise.
			self._deviceID = arg.decode("latin-1", errors="strict")
		elif command in COMMAND_RESPONSE_INFO:
			arg = int.from_bytes(reversed(arg))
			if arg < self._keysDown.get(command, 0):
				# Release.
				if not self._ignoreKeyReleases:
					# The first key released executes the key combination.
					try:
						inputCore.manager.executeGesture(InputGesture(self._deviceID, self._keysDown))
					except inputCore.NoInputGestureAction:
						pass
					# Any further releases are just the rest of the keys in the combination being released,
					# so they should be ignored.
					self._ignoreKeyReleases = True
			else:
				# Press.
				# This begins a new key combination.
				self._ignoreKeyReleases = False
			if arg > 0:
				self._keysDown[command] = arg
			elif command in self._keysDown:
				# All keys in this group have been released.
				# #3541: Remove this group so it doesn't count as a group with keys down.
				del self._keysDown[command]
		else:
			log.debugWarning(f"Unknown command {command!r}, arg {arg!r}")

	def display(self, cells: list[int]):
		# cells will already be padded up to numCells.
		arg = bytes(cells)
		self._sendRequest(DeviceCommand.DISPLAY_DATA, arg)

	gestureMap = inputCore.GlobalGestureMap(
		{
			"globalCommands.GlobalCommands": {
				"braille_scrollBack": ("br(nlseReaderZoomax):d2",),
				"braille_scrollForward": ("br(nlseReaderZoomax):d5",),
				"braille_previousLine": ("br(nlseReaderZoomax):d1",),
				"braille_nextLine": ("br(nlseReaderZoomax):d3",),
				"braille_routeTo": ("br(nlseReaderZoomax):routing",),
				"kb:upArrow": ("br(nlseReaderZoomax):up",),
				"kb:downArrow": ("br(nlseReaderZoomax):down",),
				"kb:leftArrow": ("br(nlseReaderZoomax):left",),
				"kb:rightArrow": ("br(nlseReaderZoomax):right",),
				"kb:enter": ("br(nlseReaderZoomax):select",),
			},
		},
	)


class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, model, keysDown):
		super().__init__()
		# Model identifiers should not contain spaces.
		if model:
			self.model = model.replace(" ", "")
			assert self.model.isalnum()
		self.keysDown = dict(keysDown)

		SYSTEM_KEYS_MASK = 0xF8
		SPACEBAR_KEYS_MASK = 0x07

		self.keyNames = names = []
		for group, groupKeysDown in keysDown.items():
			if (
				group == DeviceCommand.BRAILLE_KEYS
				and len(keysDown) == 1
				and not groupKeysDown & SYSTEM_KEYS_MASK
			):
				self.dots = groupKeysDown >> 8
				self.space = groupKeysDown & SPACEBAR_KEYS_MASK
			if group == DeviceCommand.ROUTING_KEYS:
				for index in range(braille.handler.display.numCells):
					if groupKeysDown & (1 << index):
						self.routingIndex = index
						names.append("routing")
						break
			else:
				for index, name in enumerate(COMMAND_RESPONSE_INFO.get(group).keys):
					if groupKeysDown & (1 << index):
						names.append(name)

		self.id = "+".join(names)
