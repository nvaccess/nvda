# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited, Burman's Computer and Education Ltd.

import inspect
import time

from logHandler import log
from threading import Lock, Timer
from typing import List

import braille
import hwIo
import inputCore
import serial

from hwIo import intToByte

# Port settings
BAUD_RATE = 19200
TIMEOUT = 0.2
WRITE_TIMEOUT = None
# Display should send initial packet within 2 seconds, but it may take
# time before it is read.
WAIT_FOR_INIT_TIMEOUT = 6
# For _clearInput function
# Timeout for giving up clearing input buffer
CLEAR_INPUT_BUFFER_TIMEOUT = 1
# Some sleep time so that in_waiting would show correct value of remaining
# bytes of input buffer in function _clearInputBuffer.
IN_WAITING_SLEEP = 0.02
# Keys are key codes sent by display.
MAX_KEY_CODE_VALUE = 216
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
MAX_COMBINATION_KEYS = 4
CONTROL_KEY_CODES: List[int] = [
	1,  # attribute1
	42,  # attribute2
	83,  # f1
	84,  # f2
	89,  # f7
	90,  # f8
	91,  # home1
	92,  # end1
	93,  # eCursor1
	94,  # cursor1
	151,  # attribute3
	192,  # attribute4
	193,  # f9
	194,  # f10
	199,  # f15
	200,  # f16
	201,  # home2
	202,  # end2
	203,  # eCursor2
	204,  # cursor2
]
# Send this to Albatross to confirm that connection is established.
ESTABLISHED = b"\xfe\xfd\xfe\xfd"
# If no connection, Albatross sends continuously byte \xff followed by byte
# containing various settings like number of cells.
INIT_START_BYTE = b"\xff"
# Send information to Albatross enclosed by these bytes.
START_BYTE = b"\xfb"
END_BYTE = b"\xfc"
# To keep connected these both above bytes must be sent periodically.
BOTH_BYTES = b"\xfb\xfc"
# How often BOTH_BYTES should be sent or to try to reconnect if connection lost.
TIMER_INTERVAL = 1


# Timer is used for that purpose and to reconnect with display (copied from
# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds)
class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self.interval = interval
		self._timer = Timer(self.interval, self._run)
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.is_running = False
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
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

	def __init__(self, port="Auto"):
		log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
		super().__init__()
		# Lock for proper i/o functionality.
		self._readWriteLock = Lock()
		# Number of cells is received when initializing connection.
		self.numCells = 0
		# Keep old display data.
		self._oldCells: List[int] = []
		# After reconnection and when user exits from device menu, display may not
		# update automatically. Keep current cell content for this.
		self._currentCells: List[int] = []
		# Clear input buffer when connected because there is likely data
		# which may cause fake key presses or triggering _exitInternalMenu.
		self._justConnected = False
		# Try to reconnect if needed.
		self._tryReconnect = False
		# Timer to keep connection. Display requires at least START_BYTE
		# and END_BYTE combination within approximately 2 seconds from previous
		# appropriate data packet. Otherwise it falls back to "wait for connection"
		# state. This behavior is built-in feature of the firmware of device.
		# Timer is also used to check if port is available when
		# reconnection is needed.
		self._rt = None
		# How many times _initConnection is called. This is for debugging.
		self._counter = 0
		# Search ports where display can be connected.
		for portType, portId, port, portInfo in self._getTryPorts(port):
			self._readWriteLock.acquire()
			if not self._chkPort(port):
				self._readWriteLock.release()
				continue
			log.debug(
				f"{inspect.stack()[0][3]}: waiting for connection on port {port} "
				f"at most {WAIT_FOR_INIT_TIMEOUT} seconds")
			startTime = time.time()
			while not self.numCells and time.time() - startTime < WAIT_FOR_INIT_TIMEOUT:
				if self._tryReconnect:
					if not self._chkPort(port):
						continue
				self._initConnection(b"\x00")
			self._readWriteLock.release()
			log.debug(
				f"{inspect.stack()[0][3]}: waited for connection on port {port} "
				f"{(time.time() - startTime):.2f} seconds")
			# If numCells > 0, there is working connection.
			if self.numCells:
				# Prepare _oldCells to store last displayed content.
				while len(self._oldCells) < self.numCells:
					self._oldCells.append(0)
				# We may need current connection port to reconnect.
				self._currentPort = port
				log.debug(f"{inspect.stack()[0][3]}: starting timer")
				self._rt = RepeatedTimer(
					TIMER_INTERVAL, self._lockedReadWrite, self._keepConnected)
				log.info(
					f"{inspect.stack()[0][3]}: connected to Caiku Albatross {self.numCells} on {portType} port {port} "
					f"at {BAUD_RATE} bps.")
				break
			# This device initialization failed.
			self._dev.close()
			self._dev = None
			log.info(
				f"{inspect.stack()[0][3]}: connection to Caiku Albatross display on {portType} port {port} "
				f"at {BAUD_RATE} bps failed. Nothing to read in {WAIT_FOR_INIT_TIMEOUT} seconds "
				"or not appropriate init packet received.")
		else:
			raise RuntimeError("No Albatross found")
		log.debug(f"Leaving {inspect.stack()[0][3]}")

	def terminate(self):
		log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
		try:
			super().terminate()
			if self._rt:
				self._rt.stop()
				self._rt = None
			# Possibly already closed.
			if self._dev:
				self._dev.close()
				self._dev = None
		finally:
			self.numCells = 0
		log.debug(f"Leaving {inspect.stack()[0][3]}")

	def _chkPort(self, port: bytes) -> bool:
		log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
		try:
			self._dev = hwIo.Serial(
				port, baudrate=BAUD_RATE, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE,
				timeout=TIMEOUT, writeTimeout=WRITE_TIMEOUT, onReceive=self._onReceive)
			log.debug(f"Leaving {inspect.stack()[0][3]}")
			return True
		except EnvironmentError:
			log.debugWarning("", exc_info=True)
			return False

	# Whole display should be updated at next time.
	def _clearOldCells(self):
		log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
		for i in range(len(self._oldCells)):
			self._oldCells[i] = 0
		log.debug(f"Leaving {inspect.stack()[0][3]}")

	# All write operations are done here.
	def _sendToDisplay(self, data: bytes, fromKeepConnected: bool = False) -> bool:
		log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
		if not self.numCells and data != ESTABLISHED:
			log.debug(
				f"{inspect.stack()[0][3]}: numCells is {self._numCells} and data is "
				f"{data}, leaving {inspect.stack()[0][3]}")
			return True
		try:
			self._dev.write(data)
			self._dev._ser.flush()
		except serial.serialutil.SerialException:
			# Assuming that connection is lost.
			self._disableConnection()
			log.debug(
				f"{inspect.stack()[0][3]}: data write failed {data}, trying to reconnect, "
				f"leaving {inspect.stack()[0][3]}", exc_info=True)
			return False
		# No timer reset if BOTH_BYTES sent from _keepConnected.
		if fromKeepConnected:
			log.debug(
				f"{inspect.stack()[0][3]}: BOTH_BYTES {BOTH_BYTES} sent, "
				f"leaving {inspect.stack()[0][3]}")
			return True
		# Timer may have not yet started.
		if self._rt:
			# Reset timer to avoid sending reduntant BOTH_BYTES packets.
			self._rt.stop()
			self._rt.start()
			log.debug(
				f"{inspect.stack()[0][3]}: data {data} sent and timer reseted, "
				f"leaving {inspect.stack()[0][3]}")
		else:
			log.debug(
				f"{inspect.stack()[0][3]}: data {data} sent, timer not yet started, "
				f"leaving {inspect.stack()[0][3]}")
		return True

	def _clearInputBuffer(self) -> bool:
		log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
		log.debug(
			f"{inspect.stack()[0][3]}: before reset_input_buffer waiting input bytes "
			f"{self._dev._ser.in_waiting}")
		try:
			startTime = time.time()
			while self._dev._ser.in_waiting and time.time() - startTime < CLEAR_INPUT_BUFFER_TIMEOUT:
				self._dev._ser.reset_input_buffer()
				time.sleep(IN_WAITING_SLEEP)
				log.debug(
					f"{inspect.stack()[0][3]}: after reset waiting input bytes "
					f"{self._dev._ser.in_waiting}")
			if self._dev._ser.in_waiting:
				self._justConnected = False
				self._disableConnection()
				log.debug(
					f"{inspect.stack()[0][3]}: clear timed out, "
					f"bytes waiting; trying to reconnect, leaving {inspect.stack()[0][3]}")
				return False
		except serial.serialutil.SerialException:
			self._disableConnection()
			log.debug(
				f"{inspect.stack()[0][3]}: input buffer reset failed, trying to reconnect, "
				f"leaving {inspect.stack()[0][3]}", exc_info=True)
			return False
		self._justConnected = False
		log.debug(f"Leaving {inspect.stack()[0][3]}")
		return True

	def _keepConnected(self):
		log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
		# Trying to reconnect.
		if self._tryReconnect:
			# Can disappeared port be found again?
			if not self._chkPort(self._currentPort):
				if self._dev:
					self._dev.close()
					self._dev = None
				log.debug(
					f"{inspect.stack()[0][3]}: port {self._currentPort} not found, "
					f"leaving {inspect.stack()[0][3]}")
				return
			# Port found.
			self._tryReconnect = False
			log.debug(
				f"{inspect.stack()[0][3]}: port {self._currentPort} found, "
				f"leaving {inspect.stack()[0][3]}")
			return
		# Connected if numCells > 0.
		if self.numCells:
			# Display needs this to keep connection.
			self._sendToDisplay(BOTH_BYTES, True)
		log.debug(f"Leaving {inspect.stack()[0][3]}")

	def _onReceive(self, data: bytes):
		log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
		# Clear input buffer to avoid fake key presses and redundant
		# _initConnection calls.
		if self._justConnected:
			self._lockedReadWrite(self._clearInputBuffer)
			log.debug(
				f"Returned from _clearInputBuffer, leaving {inspect.stack()[0][3]}")
			return
		# Initial connection, reconnection, exit from internal menu of display or
		# delay in sending data to display causing its fall back to
		# "wait for connection" state.
		if not self.numCells or data == INIT_START_BYTE:
			self._lockedReadWrite(self._initConnection, data)
			log.debug(f"Returned from _initConnection, leaving {inspect.stack()[0][3]}")
			return
		# Read display key presses.
		# Blocking most obvious key code values which are not key presses.
		if not len(data) or ord(data) == 0 or ord(data) > MAX_KEY_CODE_VALUE:
			log.debug(
				f"Undefined value {data} for key press, leaving {inspect.stack()[0][3]}")
			return
		self._lockedReadWrite(self._handleKeyPresses, data)
		log.debug(f"Returned from _handleKeyPresses, leaving {inspect.stack()[0][3]}")

	def _initConnection(self, data: bytes):
		log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
		self._counter += 1
		log.debug(f"{inspect.stack()[0][3]}: call {self._counter}")
		# If no connection, Albatross sends continuously byte \xff
		# followed by byte containing various settings like number of cells.
		# This happens also when exited internal menu of display or if delay
		# in sending data to display causing its fallback to "wait for connection"
		# state.
		# There may be garbage before INIT_START_BYTE when initial start or
		# reconnection occurs.
		if data != INIT_START_BYTE:
			try:
				while data != INIT_START_BYTE and len(data):
					data = self._dev.read(1)
			except serial.serialutil.SerialException:
				self._disableConnection()
				log.debug(
					f"{inspect.stack()[0][3]}: init byte read failed, trying to reconnect "
					f"leaving {inspect.stack()[0][3]}", exc_info=True)
				return
		if not len(data):
			log.debug(
				f"{inspect.stack()[0][3]}: no init byte, leaving {inspect.stack()[0][3]}")
			return
		try:
			data = self._dev.read(1)
		except serial.serialutil.SerialException:
			self._disableConnection()
			log.debug(
				f"{inspect.stack()[0][3]}: value byte read failed, trying to reconnect "
				f"leaving {inspect.stack()[0][3]}", exc_info=True)
			return
		if not len(data):
			log.debug(
				f"{inspect.stack()[0][3]}: no value byte, leaving "
				f"{inspect.stack()[0][3]}")
			return
		log.debug(f"{inspect.stack()[0][3]}: value byte {data}")
		# This is safe because read/write lock is locked.
		if not self._sendToDisplay(ESTABLISHED):
			log.debug(
				f"{inspect.stack()[0][3]}: connection establishment failed, "
				f"leaving {inspect.stack()[0][3]}")
			return
		self._justConnected = True
		# If bit 7 (LSB 0 scheme) is 1, there is 80 cells model, else 46 cells model.
		# Other display settings are currently ignored so skipping separate function
		# definition this time.
		self.numCells = 80 if ord(data) >> 7 == 1 else 46
		log.debug(f"{inspect.stack()[0][3]}: numcells {self.numCells}")
		# Reconnected if length of _oldCells is numCells. Show last known content.
		if len(self._oldCells) == self.numCells:
			self._clearOldCells()
			log.debug(f"{inspect.stack()[0][3]}: about to show _currentCells")
			# ReadWriteLock is locked, and _prepareCells is called only from
			# display, and it requires acquiring that same lock.
			self._prepareCells(self._currentCells)
		log.debug(f"Leaving {inspect.stack()[0][3]}")

	def _disableConnection(self):
		log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
		self.numCells = 0
		self._dev.close()
		self._dev = None
		if len(self._oldCells):
			self._clearOldCells()
		self._tryReconnect = True
		log.debug(f"Leaving {inspect.stack()[0][3]}")

	def _handleKeyPresses(self, data: bytes):
		log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
		# If Ctrl-key is pressed, then there is at least one byte to read;
		# in single ctrl-key presses and key combinations the first key is resent as last one.
		if ord(data) in CONTROL_KEY_CODES:
			# at most 4 keys.
			try:
				data += self._dev._ser.read_until(data)
			except serial.serialutil.SerialException:
				# Assuming that connection is lost.
				self._disableConnection()
				log.debug(
					f"{inspect.stack()[0][3]}: ctrl key/key combination read failed, "
					f"trying to reconnect, leaving {inspect.stack()[0][3]}", exc_info=True)
				return
			# Ensuring ctrl key packet is appropriate.
			else:
				if len(data) < 2 or len(data) > MAX_COMBINATION_KEYS + 1 or data[0] != data[len(data) - 1]:
					self._clearInputBuffer()
					log.debug(
						f"{inspect.stack()[0][3]}: no appropriate ctrl key/key combination "
						f"{data}, leaving {inspect.stack()[0][3]}")
					return
		if not self._clearInputBuffer():
			log.debug(
				f"{inspect.stack()[0][3]}: input buffer reset failed, leaving "
				f"{inspect.stack()[0][3]}")
			return
		pressedKeys = set(data)
		log.debug(f"{inspect.stack()[0][3]}: pressedKeys {pressedKeys}")
		try:
			inputCore.manager.executeGesture(InputGestureKeys(pressedKeys))
		# Attribute error which rarely occurs here is something strange.
		except (inputCore.NoInputGestureAction, AttributeError):
			pass
		log.debug(f"Leaving {inspect.stack()[0][3]}")

	def display(self, cells: List[int]):
		log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
		self._lockedReadWrite(self._prepareCells, cells)
		log.debug(f"Leaving {inspect.stack()[0][3]}")

	def _prepareCells(self, cells):
		log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
		# Keep _currentCells up to date.
		self._currentCells = cells.copy()
		# Connection is lost.
		if not self.numCells:
			log.debug(f"{inspect.stack()[0][3]}: no connection, leaving {inspect.stack()[0][3]}")
			return
		writeBytes: List[bytes] = [START_BYTE, ]
		# Only changed content is sent (cell index and data).
		for i, cell in enumerate(cells):
			if cell != self._oldCells[i]:
				self._oldCells[i] = cell
				# display indexing starts from 1
				writeBytes.append(intToByte(i + 1))
				# Bits have to be reversed.
				# Source: https://stackoverflow.com/questions/12681945/reversing-bits-of-python-integer
				writeBytes.append(intToByte(int('{:08b}'.format(cell)[::-1], 2)))
		writeBytes.append(END_BYTE)
		self._sendToDisplay(b"".join(writeBytes))
		log.debug(f"Leaving {inspect.stack()[0][3]}")

	# To avoid i/o conflicts all functions which read or write go
	# directly or indirectly through this.
	def _lockedReadWrite(self, function, *args, **kwargs):
		self._readWriteLock.acquire()
		try:
			log.debug(f"{inspect.stack()[0][3]} started, called by {inspect.stack()[1][3]}")
			log.debug(
				f"{inspect.stack()[0][3]}: about to call function {function.__name__}; args {args}, kwargs {kwargs}")
			res = function(*args, **kwargs)
			log.debug(f"Leaving {inspect.stack()[0][3]}, about to return {res}")
			return res
		finally:
			self._readWriteLock.release()

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"review_top": ("br(albatross):home1", "br(albatross):home2",),
			"review_bottom": ("br(albatross):end1", "br(albatross):end2",),
			"navigatorObject_toFocus": ("br(albatross):eCursor1", "br(albatross):eCursor2",),
			"braille_toFocus": ("br(albatross):cursor1", "br(albatross):cursor2",),
			"moveMouseToNavigatorObject": ("br(albatross):home1+home2",),
			"moveNavigatorObjectToMouse": ("br(albatross):end1+end2",),
			"navigatorObject_moveFocus": ("br(albatross):eCursor1+eCursor2",),
			"braille_toggleTether": ("br(albatross):cursor1+cursor2",),
			"braille_previousLine": ("br(albatross):up1", "br(albatross):up2", "br(albatross):up3",),
			"braille_nextLine": ("br(albatross):down1", "br(albatross):down2", "br(albatross):down3",),
			"braille_scrollBack": ("br(albatross):left", "br(albatross):lWheelLeft", "br(albatross):rWheelLeft",),
			"braille_scrollForward": (
				"br(albatross):right", "br(albatross):lWheelRight", "br(albatross):rWheelRight",),
			"braille_routeTo": ("br(albatross):routing",),
			"braille_reportFormatting": ("br(albatross):secondRouting",),
			"braille_toggleFocusContextPresentation": ("br(albatross):attribute1+attribute3",),
			"speechMode": ("br(albatross):attribute2+attribute4",),
			"reviewMode_previous": ("br(albatross):f1",),
			"reviewMode_next": ("br(albatross):f2",),
			"navigatorObject_parent": ("br(albatross):f3",),
			"navigatorObject_firstChild": ("br(albatross):f4",),
			"navigatorObject_previous": ("br(albatross):f5",),
			"navigatorObject_next": ("br(albatross):f6",),
			"navigatorObject_current": ("br(albatross):f7",),
			"navigatorObject_currentDimensions": ("br(albatross):f8",),
			"review_activate": ("br(albatross):f7+f8",),
			"dateTime": ("br(albatross):f9",),
			"say_battery_status": ("br(albatross):f10",),
			"title": ("br(albatross):f11",),
			"reportStatusLine": ("br(albatross):f12",),
			"reportCurrentLine": ("br(albatross):f13",),
			"sayAll": ("br(albatross):f14",),
			"review_currentCharacter": ("br(albatross):f15",),
			"review_currentLine": ("br(albatross):f16",),
			"review_currentWord": ("br(albatross):f15+f16",),
			"review_previousLine": ("br(albatross):lWheelUp", "br(albatross):rWheelUp",),
			"review_nextLine": ("br(albatross):lWheelDown", "br(albatross):rWheelDown",),
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
		names = []
		for key in self.keyCodes:
			if 2 <= key <= 41 or 111 <= key <= 150:
				names.append("routing")
				self.routingIndex = self._getRoutingIndex(key)
			elif 43 <= key <= 82 or 152 <= key <= 191:
				names.append("secondRouting")
				self.routingIndex = self._getRoutingIndex(key)
			else:
				try:
					names.append(KEY_NAMES[key])
				except KeyError:
					log.debugWarning("Unknown key with id %d" % key)
		self.id = "+".join(names)

	def _getRoutingIndex(self, key) -> int:
		# Indexes start from 0.
		# First 40 routing keys.
		if key <= 41:
			return key - 2
		# First 40 secondRouting keys.
		if key <= 82:
			return key - 43
		# Rest routing keys.
		if key <= 150:
			return key - 71
		# Rest secondRouting keys.
		if key <= 191:
			return key - 112
