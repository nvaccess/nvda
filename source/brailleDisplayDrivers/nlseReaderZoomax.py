# -*- coding: UTF-8 -*-
# brailleDisplayDrivers/nlseReaderZoomax.py
# Description:
# NLS eReader Zoomax driver for NVDA.

import time
from typing import Union, List, Optional

import braille
from hwIo import intToByte, boolToByte
import inputCore
from logHandler import log
import brailleInput
import hwIo
import bdDetect
import serial

TIMEOUT = 0.2
BAUD_RATE = 19200
CONNECT_RETRIES = 5
TIMEOUT_BETWEEN_RETRIES = 2

ESCAPE = b"\x1b"

LOC_DISPLAY_DATA = b"\x01"
LOC_REQUEST_INFO = b"\x02"
LOC_REQUEST_VERSION = b"\x05"
LOC_REPEAT_ALL = b"\x08"
LOC_PROTOCOL_ONOFF = b"\x15"
LOC_ROUTING_KEYS = b"\x22"
LOC_DISPLAY_KEYS = b"\x24"
LOC_ROUTING_KEY = b"\x27"
LOC_BRAILLE_KEYS = b"\x33"
LOC_JOYSTICK_KEYS = b"\x34"
LOC_DEVICE_ID = b"\x84"
LOC_SERIAL_NUMBER = b"\x8a"

LOC_RSP_LENGTHS = {
	LOC_DISPLAY_DATA: 1,
	LOC_DISPLAY_KEYS: 1,
	LOC_ROUTING_KEY: 1,
	LOC_BRAILLE_KEYS: 2,
	LOC_JOYSTICK_KEYS: 1,
	LOC_DEVICE_ID: 16,
	LOC_SERIAL_NUMBER: 8,
}

KEY_NAMES = {
	LOC_ROUTING_KEYS: None,
	LOC_ROUTING_KEY: None,
	LOC_DISPLAY_KEYS: ("d1", "d2", "d3", "d4", "d5", "d6"),
	LOC_BRAILLE_KEYS: (
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
		"b8",
	),  # byte 2
	LOC_JOYSTICK_KEYS: ("up", "left", "down", "right", "select"),
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
				"VID_1A86&PID_7523",  # CH340
			},
		)

		driverRegistrar.addBluetoothDevices(lambda m: m.id.startswith("NLS eReader Z"))

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	def _connect(self, port):
		for portType, portId, port, portInfo in self._getTryPorts(port):
			try:
				self._dev = hwIo.Serial(
					port,
					baudrate=BAUD_RATE,
					bytesize=serial.EIGHTBITS,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					timeout=TIMEOUT,
					writeTimeout=TIMEOUT,
					onReceive=self._onReceive,
				)
			except EnvironmentError:
				log.info("Port not yet available.")
				log.debugWarning("", exc_info=True)
				if self._dev:
					self._dev.close()
				continue

			self._sendRequest(LOC_PROTOCOL_ONOFF, False)
			self._sendRequest(LOC_PROTOCOL_ONOFF, True)
			self._sendRequest(LOC_PROTOCOL_ONOFF, True)
			self._sendRequest(LOC_REPEAT_ALL)

			for i in range(5):
				self._dev.waitForRead(TIMEOUT)
				if self.numCells:
					break

			if self.numCells:
				log.info(
					"Device connected via {type} ({port})".format(
						type=portType,
						port=port,
					),
				)
				return True
			log.info("Device arrival timeout")
			self._dev.close()
		return False

	def __init__(self, port="auto"):
		log.info("nlseReaderZoomax Init")
		super(BrailleDisplayDriver, self).__init__()
		self.numCells = 0
		self._deviceID: Optional[str] = None
		self._dev = None

		for i in range(CONNECT_RETRIES):
			if self._connect(port):
				break
			else:
				time.sleep(TIMEOUT_BETWEEN_RETRIES)

		self._keysDown = {}
		self._ignoreKeyReleases = False

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
			try:
				self._sendRequest(LOC_PROTOCOL_ONOFF, False)
			except EnvironmentError:
				pass
		finally:
			self._dev.close()

	def _sendRequest(self, command: bytes, arg: Union[bytes, bool, int] = b""):
		"""
		:type command: bytes
		:type arg: bytes | bool | int
		"""
		typeErrorString = "Expected param '{}' to be of type '{}', got '{}'"
		if not isinstance(arg, bytes):
			if isinstance(arg, bool):
				arg = boolToByte(arg)
			elif isinstance(arg, int):
				arg = intToByte(arg)
			else:
				raise TypeError(typeErrorString.format("arg", "bytes, bool, or int", type(arg).__name__))

		if not isinstance(command, bytes):
			raise TypeError(typeErrorString.format("command", "bytes", type(command).__name__))

		arg = arg.replace(ESCAPE, ESCAPE * 2)
		data = b"".join(
			[
				ESCAPE,
				command,
				arg,
			],
		)
		self._dev.write(data)

	def _onReceive(self, data: bytes):
		if data != ESCAPE:
			log.debugWarning("Ignoring byte before escape: %r" % data)
			return
		# data only contained the escape. Read the rest from the device.
		stream = self._dev
		command = stream.read(1)
		length = LOC_RSP_LENGTHS.get(command, 0)
		if command == LOC_ROUTING_KEYS:
			length = 10 if self.numCells > 40 else 5
		arg = stream.read(length)
		self._handleResponse(command, arg)

	def _handleResponse(self, command: bytes, arg: bytes):
		if command == LOC_DISPLAY_DATA:
			self.numCells = ord(arg)
		elif command == LOC_DEVICE_ID:
			# Short ids can be padded with either nulls or spaces.
			arg = arg.rstrip(b"\0 ")
			# Assumption: all device IDs can be decoded with latin-1.
			# If not, we wish to know about it, allow decode to raise.
			self._deviceID = arg.decode("latin-1", errors="strict")
		elif command in KEY_NAMES:
			arg = sum(byte << offset * 8 for offset, byte in enumerate(arg))
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
			log.debugWarning("Unknown command {command!r}, arg {arg!r}".format(command=command, arg=arg))

	def display(self, cells: List[int]):
		# cells will already be padded up to numCells.
		arg = bytes(cells)
		self._sendRequest(LOC_DISPLAY_DATA, arg)

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
		super(InputGesture, self).__init__()
		# Model identifiers should not contain spaces.
		if model:
			self.model = model.replace(" ", "")
			assert self.model.isalnum()
		self.keysDown = dict(keysDown)

		self.keyNames = names = []
		for group, groupKeysDown in keysDown.items():
			if group == LOC_BRAILLE_KEYS and len(keysDown) == 1 and not groupKeysDown & 0xF8:
				# This is braille input.
				# 0xfc covers command keys. The space bars are covered by 0x7.
				self.dots = groupKeysDown >> 8
				self.space = groupKeysDown & 0x7
			if group == LOC_ROUTING_KEYS:
				for index in range(braille.handler.display.numCells):
					if groupKeysDown & (1 << index):
						self.routingIndex = index
						names.append("routing")
						break
			elif group == LOC_ROUTING_KEY:
				self.routingIndex = groupKeysDown - 1
				names.append("routing")
			else:
				for index, name in enumerate(KEY_NAMES[group]):
					if groupKeysDown & (1 << index):
						names.append(name)

		self.id = "+".join(names)
