# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2021 NV Access Limited, Ulf Beckmann <beckmann@flusoft.de>
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
#
# This file represents the braille display driver for
# Seika Notetaker, a product from Nippon Telesoft
# see www.seika-braille.com for more details
# 29.06.2020 / 12:36

from io import BytesIO
from typing import List
import braille
import brailleInput
import inputCore
import hwPortUtils
import bdDetect
import hwIo
from serial.win32 import INVALID_HANDLE_VALUE
from logHandler import log

TIMEOUT = 0.2

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
	0x002000: "RJ_DOWN"
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

_dotNames = {}
for i in range(1, 9):
	key = globals()["DOT_%d" % i]
	_dotNames[key] = "d%d" % i
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
		self.status = 0
		self.cmdlen = 0
		self.handle = None
		self._hidBuffer = b""
		log.info("path: " + self.path)

		if self.path == "":
			raise RuntimeError("No MINI-SEIKA display found, no path found")
		self._dev = hwIo.Hid(path=self.path, onReceive=self._onReceive)
		if self._dev._file == INVALID_HANDLE_VALUE:
			raise RuntimeError("No MINI-SEIKA display found, open error")
		self._dev.setFeature(SEIKA_CONFIG)  # baudrate, stopbit usw
		self._dev.setFeature(SEIKA_CMD_ON)  # device on
		self._dev.write(SEIKA_REQUEST_INFO)  # Request the Info from the device

		# wait and try to get info from the Braille display
		for i in range(30):  # the info-block is about
			self._dev.waitForRead(TIMEOUT)
			if self.numCells:
				log.info("Seikanotetaker an USB-HID, Cells {c} Buttons {b}".format(c=self.numCells, b=self.numBtns))
				break

		if self.numCells == 0:
			self._dev.close()
			raise RuntimeError("No MINI-SEIKA display found, no response")

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
		finally:
			self._dev.close()

	def display(self, cells: List[int]):
		# cells will already be padded up to numCells.
		cellBytes = SEIKA_SEND_TEXT + self.numCells.to_bytes(1, 'little') + bytes(cells)
		self._dev.write(cellBytes)

	def _onReceive(self, data: bytes):
		stream = BytesIO(data)
		cmd = stream.read(3)
		self._hidBuffer += cmd[1:2]
		if len(self._hidBuffer) == 3:
			self.status = 1
		elif len(self._hidBuffer) == 4:
			self.cmdlen = cmd[1]
			self.status = 2
		elif self.status == 2 and len(self._hidBuffer) == self.cmdlen + 4:
			command = self._hidBuffer[0:3]
			arg = self._hidBuffer[3:self.cmdlen + 4]
			self.status = 0
			self._hidBuffer = b""
			
			if command == SEIKA_INFO:
				self._handInfo(arg)
			elif command == SEIKA_ROUTING:
				self._handRouting(arg)
			elif command == SEIKA_KEYS:
				self._handKeys(arg)
			elif command == SEIKA_KEYS_ROU:
				self._handKeysRouting(arg)
			else:
				log.debug("other data.")

	def _handInfo(self, arg: bytes):
		self.numCells = arg[2]
		self.numBtns = arg[1]

	def _handRouting(self, arg: bytes):
		Rou = 0
		for i in range(arg[0]):
			for j in range(8):
				if arg[i + 1] & (1 << j):
					Rou = i * 8 + j
					
					gesture = InputGestureRouting(Rou)
					try:
						inputCore.manager.executeGesture(gesture)
					except inputCore.NoInputGestureAction:
						log.debug("No Action for routing command")
						pass

	def _handKeys(self, arg: bytes):
		Brl = arg[1]
		Key = arg[2] | (arg[3] << 8)
		Btn = 0  # Seika has no button
		if not (Key or Btn or Brl):
			pass
		if Key:  # Mini Seika has 2 Top and 4 Front ....
			gesture = InputGesture(keys=Key)
		if Btn:  # Mini Seika has no Btn ....
			gesture = InputGesture(keys=Btn)
		if Brl:  # or how to handle Brailleinput?
			gesture = InputGesture(dots=Brl)
		if Key or Btn or Brl:
			try:
				inputCore.manager.executeGesture(gesture)
			except inputCore.NoInputGestureAction:
				log.debug("No Action for keys ")
				pass

	def _handKeysRouting(self, arg: bytes):
		argk = b"\x03" + arg[1:]
		argr = (arg[0] - 3).to_bytes(1, 'little') + arg[4:]
		self._handRouting(argr)
		self._handKeys(argk)

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
		super(InputGestureRouting, self).__init__()
		self.id = "routing"
		self.routingIndex = index


class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, keys=None, dots=None, space=False, routing=None):
		super(braille.BrailleDisplayGesture, self).__init__()
		# see what thumb keys are pressed:
		names = set()
		if keys is not None:
			names.update(_keyNames[1 << i] for i in range(22) if (1 << i) & keys)
		elif dots is not None:
			# now the dots
			self.dots = dots
			if space:
				self.space = space
				names.add(_keyNames[1])
			names.update(_dotNames[1 << i] for i in range(8) if (1 << i) & dots)
		elif routing is not None:
			self.routingIndex = routing
			names.add('routing')
		self.id = "+".join(names)
