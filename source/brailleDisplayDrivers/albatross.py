# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited, Burman's Computer and Education Ltd.

from typing import List
from threading import Timer
import serial
import braille
import hwIo
from hwIo import intToByte
import time
import inputCore
from logHandler import log

BAUD_RATE = 19200
TIMEOUT = 0.2
WRITE_TIMEOUT = 0
# Indexes are key codes sent by display.
KEY_NAMES = {
	1: "attribute1",
	42: "attribute2",
	83: "f1",
	84: "f2",
	85: "f3",
	86: "f4",
	87: "f5",
	88: "f6",
	89: "f7",
	90: "f8",
	91: "home1",
	92: "end1",
	93: "eCursor1",
	94: "cursor1",
	95: "up1",
	96: "down1",
	97: "left",
	98: "up2",
	103: "lWheelRight",
	104: "lWheelLeft",
	105: "lWheelUp",
	106: "lWheelDown",
	151: "attribute3",
	192: "attribute4",
	193: "f9",
	194: "f10",
	195: "f11",
	196: "f12",
	197: "f13",
	198: "f14",
	199: "f15",
	200: "f16",
	201: "home2",
	202: "end2",
	203: "eCursor2",
	204: "cursor2",
	205: "up3",
	206: "down2",
	207: "right",
	208: "down3",
	213: "rWheelRight",
	214: "rWheelLeft",
	215: "rWheelUp",
	216: "rWheelDown",
}
# These are ctrl-keys which may start key combination.
CONTROL_KEY_CODES: List[int] = [
	1, 42, 83, 84, 89, 90, 91, 92, 93, 94, 151, 192, 193, 194, 199, 200, 201, 202, 203, 204, ]
# Send this to Albatross to confirm that connection is established.
ESTABLISHED = b"\xfe\xfd\xfe\xfd"
# Send information to Albatross enclosed by these bytes.
START_BYTE = b"\xfb"
END_BYTE = b"\xfc"
# To keep connected these both bytes must be sent periodically.
BOTH_BYTES = b"\xfb\xfc"
# Timer is used for that purpose and to reconnect with display (copied from
# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds)


class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self._timer = None
		self.interval = interval
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.is_running = False
		self.next_call = time.time()
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self.next_call += self.interval
			self._timer = Timer(self.next_call - time.time(), self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False


class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "albatross"
	# Translators: Names of braille displays.
	description = _("Caiku Albatross 46/80")
	isThreadSafe = True

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	def chkPort(self, port: bytes) -> bool:
		try:
			self._dev = hwIo.Serial(
				port, baudrate=BAUD_RATE, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE,
				timeout=TIMEOUT, writeTimeout=WRITE_TIMEOUT, onReceive=self._onReceive)
		except EnvironmentError:
			log.debugWarning("", exc_info=True)
			return False
		return True

	# Whole display should be updated at next time.
	def clearOldCells(self):
		i = 0
		for cell in self.oldCells:
			self.oldCells[i] = 0
			i += 1

	# All write operations are done here.
	def sendToDisplay(self, data: bytes) -> bool:
		try:
			self._dev.write(data)
		except serial.serialutil.SerialException:
			# Suitable initial values for reconnection.
			# Connection worked before failure.
			if self.numCells:
				self.numCells = 0
				self.clearOldCells()
			self._dev.close()
			self._dev = None
			if not self.currentPort:
				return False
			if not self.chkPort(self.currentPort):
				# Maybe display was unplugged/powered off which causes USB serial port disappearing.
				self.tryReconnect = True
				if self._dev:
					self._dev.close()
			return False
		if data == ESTABLISHED:
			# Actually I/O buffer should be reseted, but poor man's solution now.
			while len(self._dev.read(1024)):
				pass
		return True

	def keepConnected(self):
		# Can disappeared port be found again?
		if self.tryReconnect:
			if not self.currentPort:
				return
			if not self.chkPort(self.currentPort):
				return
			else:
				# Port found.
				self.tryReconnect = False
				return
		if self.timerRunning and self.numCells:
			self.sendToDisplay(BOTH_BYTES)

	def __init__(self, port="Auto"):
		super().__init__()
		# Number of cells is received when initializing connection.
		self.numCells = 0
		# Keep old display data.
		self.oldCells: List[int] = []
		# Try to reconnect if needed.
		self.tryReconnect = False
		# Current portto reconnect.
		self.currentPort = 0
		# Search ports where display can be connected.
		for portType, portId, port, portInfo in self._getTryPorts(port):
			if not self.chkPort(port):
				continue
			# Albatross seems to need some more time.
			while not self._dev.waitForRead(TIMEOUT):
				pass
			# Check for cell information
			if self.numCells:
				while len(self.oldCells) < self.numCells:
					self.oldCells.append(0)
				# We may need current connection port to reconnect.
				self.currentPort = port
				# Start timer to keep connection.
				self.rt = RepeatedTimer(1, self.keepConnected)
				self.timerRunning = True
				log.info(
					"Connected to Caiku Albatross %s on %s port %s at %s bps.",
					self.numCells, portType, port, BAUD_RATE)
				break
			# This device initialization failed.
			self._dev.close()
		else:
			raise RuntimeError("No Albatross found")

	def terminate(self):
		try:
			super().terminate()
			if self.timerRunning:
				self.rt.stop()
				self.rt = None
				self.timerRunning = False
			self._dev.close()
		finally:
			self._dev = None
			self.numCells = 0

	def _onReceive(self, data: bytes):
		if not self.numCells:
			# If no connection, Albatross sends continuously byte \xff
			# followed by byte containing various settings like number of cells.
			if data != b"\xff":
				return
			log.debugWarning("Init byte: %r" % data)
			data = self._dev.read(1)
			if len(data) == 0:
				return
			log.debugWarning("Value byte: %r" % data)
			if not self.sendToDisplay(ESTABLISHED):
				return
			self.numCells = 80 if ord(data) >> 7 == 1 else 46
			return
		# Connected.
		else:
			# It is possible that there is no connection from perspective of display.
			if data == b"\xff":
				if self.sendToDisplay(bytes(ESTABLISHED)):
					self.clearOldCells()
				log.debugWarning("Byte %r, numCells %d, tryReconnect %r" % (data, self.numCells, self.tryReconnect))
				return
			pressedKeys = set()
			# If Ctrl-key is pressed, then there is at least one byte to read;
			# in single ctrl-key presses and key combinations the first key is resent as last one.
			if ord(data) in CONTROL_KEY_CODES:
				# at most 4 keys.
				kPresses = bytearray(data + self._dev.read(4))
				[pressedKeys.add(k) for k in kPresses]
			else:
				pressedKeys.add(ord(data))
			try:
				inputCore.manager.executeGesture(InputGestureKeys(pressedKeys))
			except inputCore.NoInputGestureAction:
				pass

	def display(self, cells: List[int]):
		if not self.numCells:
			return
		writeBytes: List[bytes] = [START_BYTE, ]
		# Only changed content is sent, variable i is used to show position on display.
		i = 1
		j = 0
		for cell in cells:
			if cell != self.oldCells[j]:
				self.oldCells[j] = cell
				writeBytes.append(intToByte(i))
				# Bits have to be reversed.
				writeBytes.append(intToByte(int('{:08b}'.format(cell)[::-1], 2)))
			i += 1
			j += 1
		writeBytes.append(END_BYTE)
		self.sendToDisplay(b"".join(writeBytes))

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(albatross):left",),
			"braille_scrollForward": ("br(albatross):right",),
			"braille_previousLine": ("br(albatross):up1", "br(albatross):up2", "br(albatross):up3",),
			"braille_nextLine": ("br(albatross):down1", "br(albatross):down2", "br(albatross):down3",),
			"braille_routeTo": ("br(albatross):routing",),
			"braille_reportFormatting": ("br(albatross):secondRouting",),
			"braille_toggleTether": ("br(albatross):eCursor1", "br(albatross):eCursor2",),
			"braille_toFocus": ("br(albatross):cursor1", "br(albatross):cursor2",),
			"review_top": ("br(albatross):home1", "br(albatross):home2",),
			"review_bottom": ("br(albatross):end1", "br(albatross):end2",),
			"braille_toggleFocusContextPresentation": ("br(albatross):eCursor1+eCursor2",),
			"reviewMode_previous": ("br(albatross):f1",),
			"reviewMode_next": ("br(albatross):f2",),
			"navigatorObject_parent": ("br(albatross):f3",),
			"navigatorObject_firstChild": ("br(albatross):f4",),
			"navigatorObject_previous": ("br(albatross):f5",),
			"navigatorObject_next": ("br(albatross):f6",),
			"navigatorObject_moveFocus": ("br(albatross):f7",),
			"review_activate": ("br(albatross):f8",),
			"navigatorObject_toFocus": ("br(albatross):f1+f2",),
			"navigatorObject_current": ("br(albatross):f7+f8",),
			"dateTime": ("br(albatross):f9",),
			"showGui": ("br(albatross):f10",),
			"title": ("br(albatross):f11",),
			"reportStatusLine": ("br(albatross):f12",),
			"reportCurrentLine": ("br(albatross):f13",),
			"review_currentCharacter": ("br(albatross):f14",),
			"sayAll": ("br(albatross):f15",),
			"speechMode": ("br(albatross):f16",),
			"kb:windows+d": ("br(albatross):attribute1"),
			"kb:windows+e": ("br(albatross):attribute2"),
			"kb:windows+b": ("br(albatross):attribute3"),
			"kb:windows+i": ("br(albatross):attribute4"),
		},
	})


class InputGestureKeys(braille.BrailleDisplayGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, keys):
		super().__init__()
		self.keyCodes = set(keys)

		self.keyNames = names = []
		for key in self.keyCodes:
			if 2 <= key <= 41 or 111 <= key <= 150:
				names.append("routing")
				if 2 <= key <= 41:
					self.routingIndex = key - 2
				if 111 <= key <= 150:
					self.routingIndex = key - 71
			elif 43 <= key <= 82 or 152 <= key <= 191:
				names.append("secondRouting")
				if 43 <= key <= 82:
					self.routingIndex = key - 43
				if 152 <= key <= 191:
					self.routingIndex = key - 112
			else:
				try:
					names.append(KEY_NAMES[key])
				except KeyError:
					log.debugWarning("Unknown key with id %d" % key)

		self.id = "+".join(names)
