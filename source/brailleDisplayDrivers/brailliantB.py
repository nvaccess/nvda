#brailleDisplayDrivers/brailliantB.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012-2017 NV Access Limited, Babbage B.V.

import time
from typing import List, Union

import serial
import braille
import inputCore
from logHandler import log
import brailleInput
import bdDetect
import hwIo
from hwIo import intToByte, boolToByte

TIMEOUT = 0.2
BAUD_RATE = 115200
PARITY = serial.PARITY_EVEN
DELAY_AFTER_CONNECT = 1.0
INIT_ATTEMPTS = 3
INIT_RETRY_DELAY = 0.2

# Serial
HEADER = b"\x1b"
MSG_INIT = b"\x00"
MSG_INIT_RESP = b"\x01"
MSG_DISPLAY = b"\x02"
MSG_KEY_DOWN = b"\x05"
MSG_KEY_UP = b"\x06"

# HID
HR_CAPS = b"\x01"
HR_KEYS = b"\x04"
HR_BRAILLE = b"\x05"
HR_POWEROFF = b"\x07"

KEY_NAMES = {
	1: "power", # Brailliant BI 32, 40 and 80.
	# Braille keyboard (all devices except Brailliant 80).
	2: "dot1",
	3: "dot2",
	4: "dot3",
	5: "dot4",
	6: "dot5",
	7: "dot6",
	8: "dot7",
	9: "dot8",
	10: "space",
	# Command keys (Brailliant BI 32, 40 and 80).
	11: "c1",
	12: "c2",
	13: "c3",
	14: "c4",
	15: "c5",
	16: "c6",
	# Thumb keys (all devices).
	17: "up",
	18: "left",
	19: "right",
	20: "down",
	# Joystick (Brailliant BI 14).
	21: "stickUp",
	22: "stickDown",
	23: "stickLeft",
	24: "stickRight",
	25: "stickAction",
	# BrailleNote Touch calibration key events.
	30: "calibrationOk",
	31: "calibrationFail",
	32: "calibrationEmpty",
	34: "calibrationReset",
}
FIRST_ROUTING_KEY = 80
DOT1_KEY = 2
DOT8_KEY = 9
SPACE_KEY = 10

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	_dev: Union[hwIo.Serial, hwIo.Hid]
	name = "brailliantB"
	# Translators: The name of a series of braille displays.
	description = _("HumanWare Brailliant BI/B series / BrailleNote Touch")
	isThreadSafe = True

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver, self).__init__()
		self.numCells = 0

		for portType, portId, port, portInfo in self._getTryPorts(port):
			self.isHid = portType == bdDetect.KEY_HID
			# Try talking to the display.
			try:
				if self.isHid:
					self._dev = hwIo.Hid(port, onReceive=self._hidOnReceive)
				else:
					self._dev = hwIo.Serial(port, baudrate=BAUD_RATE, parity=PARITY, timeout=TIMEOUT, writeTimeout=TIMEOUT, onReceive=self._serOnReceive)
			except EnvironmentError:
				log.debugWarning("", exc_info=True)
				continue # Couldn't connect.
			# The Brailliant can fail to init if you try immediately after connecting.
			time.sleep(DELAY_AFTER_CONNECT)
			# Sometimes, a few attempts are needed to init successfully.
			for attempt in range(INIT_ATTEMPTS):
				if attempt > 0: # Not the first attempt
					time.sleep(INIT_RETRY_DELAY) # Delay before next attempt.
				self._initAttempt()
				if self.numCells:
					break # Success!
			if self.numCells:
				# A display responded.
				log.info("Found display with {cells} cells connected via {type} ({port})".format(
					cells=self.numCells, type=portType, port=port))
				break
			# This device can't be initialized. Move on to the next (if any).
			self._dev.close()

		else:
			raise RuntimeError("No display found")

		self._keysDown = set()
		self._ignoreKeyReleases = False

	def _initAttempt(self):
		if self.isHid:
			try:
				data: bytes = self._dev.getFeature(HR_CAPS)
			except WindowsError:
				return # Fail!
			self.numCells = data[24]
		else:
			# This will cause the display to return the number of cells.
			# The _serOnReceive callback will see this and set self.numCells.
			self._serSendMessage(MSG_INIT)
			self._dev.waitForRead(TIMEOUT)

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
		finally:
			# Make sure the device gets closed.
			# If it doesn't, we may not be able to re-open it later.
			self._dev.close()

	def _serSendMessage(self, msgId: bytes, payload: Union[bytes, int, bool] = b""):
		if not isinstance(payload, bytes):
			if isinstance(payload, int):
				payload: bytes = intToByte(payload)
			elif isinstance(payload, bool):
				payload: bytes = boolToByte(payload)
			else:
				raise TypeError("Expected arg 'payload' to be of type 'bytes, int, or bool'")
		data = b''.join([
			HEADER,
			msgId,
			intToByte(len(payload)),
			payload
		])
		self._dev.write(data)

	def _serOnReceive(self, data: bytes):
		if data != HEADER:
			log.debugWarning("Ignoring byte before header: %r" % data)
			return
		msgId = self._dev.read(1)
		length = ord(self._dev.read(1))
		payload = self._dev.read(length)
		self._serHandleResponse(msgId, payload)

	def _serHandleResponse(self, msgId: bytes, payload: bytes):
		if msgId == MSG_INIT_RESP:
			if payload[0] != 0:
				# Communication not allowed.
				log.debugWarning("Display at %r reports communication not allowed" % self._dev.port)
				return
			self.numCells = payload[2]

		elif msgId == MSG_KEY_DOWN:
			payload = ord(payload)
			self._keysDown.add(payload)
			# This begins a new key combination.
			self._ignoreKeyReleases = False

		elif msgId == MSG_KEY_UP:
			payload = ord(payload)
			self._handleKeyRelease()
			self._keysDown.discard(payload)

		else:
			log.debugWarning("Unknown message: id {id!r}, payload {payload!r}".format(id=msgId, payload=payload))

	def _hidOnReceive(self, data: bytes):
		# Indexing bytes gives an int, where slicing gives a byte, so 0:1 will return a bytes of length 1
		rId: bytes = data[0:1]
		if rId == HR_KEYS:
			keys = data[1:].split(b"\x00", 1)[0]
			keys = {keyInt for keyInt in keys}
			if len(keys) > len(self._keysDown):
				# Press. This begins a new key combination.
				self._ignoreKeyReleases = False
			elif len(keys) < len(self._keysDown):
				self._handleKeyRelease()
			self._keysDown = keys

		elif rId == HR_POWEROFF:
			log.debug("Powering off")
		else:
			log.debugWarning("Unknown report: %r" % data)

	def _handleKeyRelease(self):
		if self._ignoreKeyReleases or not self._keysDown:
			return
		try:
			inputCore.manager.executeGesture(InputGesture(self._keysDown))
		except inputCore.NoInputGestureAction:
			pass
		# Any further releases are just the rest of the keys in the combination being released,
		# so they should be ignored.
		self._ignoreKeyReleases = True

	def display(self, cells: List[int]):
		# cells will already be padded up to numCells.
		cellBytes = b"".join(intToByte(cell) for cell in cells)
		if self.isHid:
			outputReport: bytes = b"".join([
				HR_BRAILLE,  # id
				b"\x01\x00",  # Module 1, offset 0
				intToByte(self.numCells),  # length
				cellBytes
			])
			#: Humanware HID devices require the use of HidD_SetOutputReport when
			# sending data to the device via HID, as WriteFile seems to block forever
			# or fail to reach the device at all.
			self._dev.setOutputReport(outputReport)
		else:
			self._serSendMessage(MSG_DISPLAY, cellBytes)

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(brailliantB):left",),
			"braille_scrollForward": ("br(brailliantB):right",),
			"braille_previousLine": ("br(brailliantB):up",),
			"braille_nextLine": ("br(brailliantB):down",),
			"braille_routeTo": ("br(brailliantB):routing",),
			"braille_toggleTether": ("br(brailliantB):up+down",),
			"kb:upArrow": ("br(brailliantB):space+dot1", "br(brailliantB):stickUp"),
			"kb:downArrow": ("br(brailliantB):space+dot4", "br(brailliantB):stickDown"),
			"kb:leftArrow": ("br(brailliantB):space+dot3", "br(brailliantB):stickLeft"),
			"kb:rightArrow": ("br(brailliantB):space+dot6", "br(brailliantB):stickRight"),
			"showGui": (
				"br(brailliantB):c1+c3+c4+c5",
				"br(brailliantB):space+dot1+dot3+dot4+dot5",
			),
			"kb:shift+tab": ("br(brailliantB):space+dot1+dot3",),
			"kb:tab": ("br(brailliantB):space+dot4+dot6",),
			"kb:alt": ("br(brailliantB):space+dot1+dot3+dot4",),
			"kb:escape": ("br(brailliantB):space+dot1+dot5",),
			"kb:enter": ("br(brailliantB):stickAction"),
			"kb:windows+d": (
				"br(brailliantB):c1+c4+c5",
				"br(brailliantB):Space+dot1+dot4+dot5",
			),
			"kb:windows": ("br(brailliantB):space+dot3+dot4",),
			"kb:alt+tab": ("br(brailliantB):space+dot2+dot3+dot4+dot5",),
			"sayAll": (
				"br(brailliantB):c1+c2+c3+c4+c5+c6",
				"br(brailliantB):Space+dot1+dot2+dot3+dot4+dot5+dot6",
			),
		},
	})

class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, keys):
		super(InputGesture, self).__init__()
		self.keyCodes = set(keys)

		self.keyNames = names = []
		isBrailleInput = True
		for key in self.keyCodes:
			if isBrailleInput:
				if DOT1_KEY <= key <= DOT8_KEY:
					self.dots |= 1 << (key - DOT1_KEY)
				elif key == SPACE_KEY:
					self.space = True
				else:
					# This is not braille input.
					isBrailleInput = False
					self.dots = 0
					self.space = False
			if key >= FIRST_ROUTING_KEY:
				names.append("routing")
				self.routingIndex = key - FIRST_ROUTING_KEY
			else:
				try:
					names.append(KEY_NAMES[key])
				except KeyError:
					log.debugWarning("Unknown key with id %d" % key)

		self.id = "+".join(names)
