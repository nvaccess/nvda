# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited, Burman's Computer and Education Ltd.

import ctypes
import serial
import time

from collections import deque
from ctypes import byref
from ctypes.wintypes import DWORD
from logHandler import log
from serial.win32 import (
	ERROR_IO_PENDING,
	EV_RXCHAR,
	PURGE_RXABORT,
	PURGE_TXABORT,
	PURGE_RXCLEAR,
	PURGE_TXCLEAR,
	GetLastError,
	PurgeComm,
	SetCommMask
)
from threading import (
	Event,
	Lock,
	Timer,
	Thread
)
from typing import (
	Callable,
	List,
	Optional,
	Tuple
)

import braille
import inputCore

BAUD_RATE = 19200
TIMEOUT = 0.2
WRITE_TIMEOUT = 0
# How many times initial connection is waited by sleeping TIMEOUT.
# It sounds big value but users should appreciate that braille starts.
# It should not harm other devices with same PID&VID because this device
# is last one.
MAX_INIT_SLEEPS = 20
# Maybe due to writings of other drivers with same PID&VID, device seems
# to send init packets it should not. Although reset do not work well,
# hopefully at least strange packets would be discarded.
# How many times to try to reset I/O buffers
RESET_COUNT = 10
# How long to sleep between I/O buffer resets
RESET_SLEEP = 0.05
WRITE_QUEUE_LENGTH = 20
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
# Maximum number of keys in key combination.
MAX_COMBINATION_KEYS = 4
# These are ctrl keys which may start key combination.
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
# Display requires at least START_BYTE and END_BYTE combination within
# approximately 2 seconds from previous appropriate data packet.
# Otherwise it falls back to "wait for connection" state. This behavior
# is built-in feature of the firmware of device.
# How often BOTH_BYTES should be sent and reconnection tried
KC_INTERVAL = 1.5


# Controls most of read operations and tries to reconnect when needed
# Suspended most of time.
class ReadThread(Thread):
	def __init__(
			self,
			readFunction: Callable,
			disableFunction: Callable,
			event: Event,
			dev: serial.Serial,
			*args,
			**kwargs
	):
		super().__init__(*args, **kwargs)
		self._readFunction = readFunction
		self._disableFunction = disableFunction
		self._event = event
		self._dev = dev

	def run(self):
		data = dwEvtMask = DWORD()
		log.debug(f"{self.name} started")
		while not self._event.isSet():
			# Try to reconnect if port is not open
			if not self._dev.is_open:
				log.debug(
					f"Calling {self._readFunction.__name__}, port {self._dev.name} not open"
				)
				self._readFunction()
				if not self._dev.is_open:
					log.debug(
						f"Sleepin {KC_INTERVAL} seconds, port {self._dev.name} not open"
					)
					self._event.wait(KC_INTERVAL)
					continue
			try:
				if not SetCommMask(self._dev._port_handle, EV_RXCHAR):
					# Exiting
					if self._event.isSet():
						break
					log.debug("SetCommMask failed")
					raise(ctypes.WinError())
				result = ctypes.windll.kernel32.WaitCommEvent(
					self._dev._port_handle,
					byref(dwEvtMask),
					byref(self._dev._overlapped_read)
				)
				if not result and GetLastError() != ERROR_IO_PENDING:
					if self._event.isSet():
						break
					log.debug("WaitCommEvent failed")
					raise ctypes.WinError()
				result = ctypes.windll.kernel32.GetOverlappedResult(
					self._dev._port_handle,
					byref(self._dev._overlapped_read),
					byref(data), True
				)
				if result:
					log.debug(f"Calling function {self._readFunction.__name__} for read")
					self._readFunction()
				else:
					if self._event.isSet():
						break
					log.debug("GetOverLappedResult failed")
					raise(ctypes.WinError())
			# See comment in _somethingToRead
			except (OSError, AttributeError):
				if self._event.isSet():
					break
				else:
					self._disableFunction()
					log.debug("", exc_info=True)
		log.debug(f"Exiting {self.name}")


# Timer is used to send BOTH_BYTES regularly to keep connection
# (copied from
# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds)
class RepeatedTimer(object):
	def __init__(
			self,
			interval: float,
			function: Callable,
			*args,
			**kwargs
	):
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
		super().__init__()
		# Number of cells is received when initializing connection.
		self.numCells = 0
		# Keep old display data, only changed content is sent.
		self._oldCells: List[int] = []
		# After reconnection and when user exits from device menu, display may not
		# update automatically. Keep current cell content for this.
		self._currentCells: List[int] = []
		# Set to True if settings byte is INIT_START_BYTE
		self._invalidSettingsByte = False
		# Set to True when filtering redundant init packets when init byte
		# received but not yet settings byte.
		self._initByteReceived = False
		# Set to True if settings byte has not been dequeued yet in
		# _handleInitPackets.
		self._waitingSettingsByte = False
		# Set to True if ctrl key combination is partially dequeued.
		self._waitingCtrlPacket = False
		# Port object
		self._dev = None
		# Try to connect or reconnect
		self._tryToConnect = False
		self._readQueue = deque()
		self._writeQueue = deque(maxlen=WRITE_QUEUE_LENGTH)
		self._exitEvent = Event()
		# Thread for read
		self._handleRead = None
		self._writeLock = Lock()
		# Timer to keep connection (see KC_INTERVAL).
		self._kc = None
		# When previous write was done (see KC_INTERVAL).
		self._writeTime = 0.0
		# Search ports where display can be connected.
		for portType, portId, port, portInfo in self._getTryPorts(port):
			# For reconnection
			self._currentPort = port
			self._tryToConnect = True
			self._readHandling()
			if self.numCells:
				# Prepare _oldCells to store last displayed content.
				while len(self._oldCells) < self.numCells:
					self._oldCells.append(0)
				self._kc = RepeatedTimer(
					KC_INTERVAL,
					self._keepConnected
				)
				self._handleRead = ReadThread(
					self._readHandling,
					self._disableConnection,
					self._exitEvent,
					self._dev,
					name="albatross_read",
					daemon=True
				)
				self._handleRead.start()
				log.info(
					f"Connected to Caiku Albatross {self.numCells} on {portType} port {port} "
					f"at {BAUD_RATE} bps."
				)
				break
			# This device initialization failed.
			if self._dev:
				if self._dev.is_open:
					self._dev.close()
				self._dev = None
			if self._invalidSettingsByte:
				log.info(
					"After checking internal settings, switch display off and on, "
					"and if needed restart NVDA"
				)
			log.info(
				f"Connection to Caiku Albatross display on {portType} port {port} "
				f"at {BAUD_RATE} bps failed."
			)
		else:
			raise RuntimeError("No Albatross found")

	def terminate(self):
		try:
			if self._handleRead:
				self._exitEvent.set()
			super().terminate()
			self.numCells = 0
			if self._dev:
				if self._dev.is_open:
					self._dev.close()
				self._dev = None
			if self._kc:
				self._kc.stop()
				self._kc = None
			if self._readQueue:
				self._readQueue.clear()
			if self._writeQueue:
				self._writeQueue.clear()
			self._readQueue = None
			self._writeQueue = None
			self._handleRead = None
		except Exception:
			# Terminating anyway
			pass

	# _initConnection, _initPort, _openPort, _readInitByte and _readSettingsByte
	# are helper functions to establish connection.
	# If no connection, Albatross sends continuously INIT_START_BYTE
	# followed by byte containing various settings like number of cells.
	def _initConnection(self) -> bool:
		for i in range(MAX_INIT_SLEEPS):
			if not self._dev:
				if not self._initPort(i):
					continue
			elif not self._dev.is_open:
				if not self._openPort(i):
					continue
			if self._tryToConnect:
				self._tryToConnect = False
			else:
				log.debug(
					f"Sleeping {TIMEOUT} seconds before try {i + 1} / {MAX_INIT_SLEEPS}"
				)
				time.sleep(TIMEOUT)
			if not self._readInitByte():
				if self._invalidSettingsByte:
					return False
				else:
					continue
			if not self._tryToConnect and self.numCells:
				return True
		return False

	# Parameter i is just for loggint retries
	def _initPort(self, i=MAX_INIT_SLEEPS - 1) -> bool:
		try:
			self._dev = serial.Serial(
				self._currentPort, baudrate=BAUD_RATE, stopbits=serial.STOPBITS_ONE,
				parity=serial.PARITY_NONE, timeout=TIMEOUT, writeTimeout=WRITE_TIMEOUT)
			log.debug(f"Port {self._currentPort} initialized")
			if not self._resetBuffers():
				if i == MAX_INIT_SLEEPS - 1:
					return False
				log(
					f"sleeping {TIMEOUT} seconds before try {i + 2} / {MAX_INIT_SLEEPS}")
				time.sleep(TIMEOUT)
				return False
			return True
		except IOError:
			if i == MAX_INIT_SLEEPS - 1:
				log.debug(f"Port {self._currentPort} not initialized", exc_info=True)
				return False
			log.debug(
				f"Port {self._currentPort} not initialized, sleeping {TIMEOUT} seconds "
				f"before try {i + 2} / {MAX_INIT_SLEEPS}", exc_info=True
			)
			time.sleep(TIMEOUT)
			return False

	# Parameter i is just for loggint retries
	def _openPort(self, i=MAX_INIT_SLEEPS - 1) -> bool:
		try:
			self._dev.open()
			log.debug(f"Port {self._currentPort} opened")
			if not self._resetBuffers():
				if i == MAX_INIT_SLEEPS - 1:
					return False
				log(
					f"sleeping {TIMEOUT} seconds before try {i + 2} / {MAX_INIT_SLEEPS}")
				time.sleep(TIMEOUT)
				return False
			return True
		except IOError:
			if i == MAX_INIT_SLEEPS - 1:
				log.debug(f"Port {self._currentPort} not opened", exc_info=True)
				return False
			log.debug(
				f"Port {self._currentPort} not opened, sleeping {TIMEOUT} seconds "
				f"before try {i + 2} / {MAX_INIT_SLEEPS}", exc_info=True
			)
			time.sleep(TIMEOUT)
			return False

	def _readInitByte(self) -> bool:
		# Strange but very rarely in_waiting causes exception.
		try:
			if not self._dev.in_waiting:
				log.debug("Read: no data")
				return False
		# See comment in _somethingToRead
		except (IOError, AttributeError):
			self._disableConnection()
			log.debug("Trying to reconnect", exc_info=True)
			return False
		if self._waitingSettingsByte and self._readSettingsByte():
			self._waitingSettingsByte = False
			return True
		try:
			data = self._dev.read_until(INIT_START_BYTE)
			log.debug(f"Read: {data}")
			if INIT_START_BYTE in data:
				return self._readSettingsByte()
			else:
				log.debug(f"Read: INIT_START_BYTE not in {data}")
				return False
		except (IOError, AttributeError):
			self._disableConnection()
			log.debug(
				f"INIT_START_BYTE {INIT_START_BYTE} read failed, "
				"trying to reconnect", exc_info=True
			)
			return False

	def _readSettingsByte(self) -> bool:
		try:
			if not self._dev.in_waiting:
				self._waitingSettingsByte = True
				log.debug("Read: no data")
				return False
		# See comment in _readInitByte
		except (IOError, AttributeError):
			self._disableConnection()
			log.debug("Trying to reconnect", exc_info=True)
			return False
		try:
			data = self._dev.read(1)
			log.debug(f"Read: {data}")
			if data != INIT_START_BYTE:
				self._writeQueue.append(ESTABLISHED)
				log.debug(f"Write: enqueued {ESTABLISHED}")
				self._somethingToWrite()
				if self._tryToConnect:
					return False
				else:
					self._setNumCellCount(data)
					if self._invalidSettingsByte:
						self._invalidSettingsByte = False
					return True
			else:
				# Likely better chance to avoid switching display off and on
				self._writeQueue.append(ESTABLISHED)
				log.debug(f"Write: enqueued {ESTABLISHED}")
				self._somethingToWrite()
				if not self._invalidSettingsByte:
					self._invalidSettingsByte = True
					log.info(
						f"Settings byte cannot be {data}, check display internal settings"
					)
				self._disableConnection()
				return False
		except (IOError, AttributeError):
			self._disableConnection()
			log.debug("Settings byte read failed, trying to reconnect", exc_info=True)
			return False

	def _resetBuffers(self) -> bool:
		try:
			for j in range(RESET_COUNT):
				PurgeComm(
					self._dev._port_handle,
					PURGE_RXCLEAR | PURGE_RXABORT | PURGE_TXCLEAR | PURGE_TXABORT)
				time.sleep(RESET_SLEEP)
			log.debug("I/O buffers reset done")
			return True
		# See comment in _somethingToRead
		except (IOError, AttributeError):
			log.debug(
				f"I/O buffer reset failed on port {self._currentPort}", exc_info=True
			)
			if self._dev.is_open:
				self._dev.close()
			return False

	def _disableConnection(self):
		self.numCells = 0
		if self._dev and self._dev.is_open:
			self._dev.close()
		if len(self._oldCells):
			self._clearOldCells()
		self._waitingCtrlPacket = False
		self._partialCtrlPacket = None
		self._initByteReceived = False
		self._waitingSettingsByte = False
		self._readQueue.clear()
		self._writeQueue.clear()
		self._tryToConnect = True

	def _readHandling(self):
		if self._tryToConnect:
			# Only one try to open port when called from "albatross_read" thread.
			# This is indicated by _dev is not None.
			# ReadThread run function calls _readHandling again if needed.
			if self._dev:
				if not self._openPort():
					return
			if not self._initConnection():
				self._disableConnection()
				return
		data = self._somethingToRead()
		if not data or not self._skipRedundantInitPackets(data):
			return
		self._handleReadQueue()

	# All but connecting/reconnecting related read operations
	def _somethingToRead(self) -> Optional[bytes]:
		try:
			if not self._dev.in_waiting:
				return None
			data = self._dev.read(self._dev.in_waiting)
			log.debug(
				f"Read: {data}, length {len(data)}, in_waiting {self._dev.in_waiting}"
			)
			return data
		# Considering situation where "albatross_read" thread is about to read
		# but writing to display fails during it - or vice versa - AttributeError
		# might raise.
		except (IOError, AttributeError):
			self._disableConnection()
			log.debug("Read failed, trying to reconnect", exc_info=True)
			return None

	def _skipRedundantInitPackets(self, data: bytes) -> bool:
		settingsByte = None
		for i in data:
			if not self._initByteReceived:
				if i.to_bytes(1, 'big') == INIT_START_BYTE:
					self._initByteReceived = True
					continue
			else:
				if i.to_bytes(1, 'big') != INIT_START_BYTE:
					settingsByte = i.to_bytes(1, 'big')
					self._initByteReceived = False
					continue
				else:
					self._initByteReceived = False
					self._writeQueue.append(ESTABLISHED)
					log.debug(f"Write: enqueued {ESTABLISHED}")
					self._somethingToWrite()
					self._invalidSettingsByte = True
					log.info(
						f"Settings byte cannot be {INIT_START_BYTE}, check display internal "
						"settings"
					)
					self._disableConnection()
					return False
			self._readQueue.append(i.to_bytes(1, 'big'))
			log.debug(f"Read: enqueued {i.to_bytes(1, 'big')}")
		if settingsByte is not None:
			# Ensuring connection is established also after exit internal menu.
			if not len(self._readQueue):
				self._readQueue.append(INIT_START_BYTE)
				self._readQueue.append(settingsByte)
		return True

	# All write operations are done here
	def _somethingToWrite(self):
		with self._writeLock:
			data = b""
			while len(self._writeQueue):
				try:
					data += self._writeQueue.popleft()
				except IndexError:
					log.debug("Write: _writeQueue is empty", exc_info=True)
					if not len(data):
						return
			log.debug(f"Write: dequeued {data}, {len(self._writeQueue)} items left")
			try:
				self._dev.write(data)
				self._writeTime = time.time()
				# Reset timer
				if self._kc:
					self._kc.stop()
					self._kc.start()
				log.debug(f"Written: {data}")
			# see comment in _somethingToRead
			except (IOError, AttributeError):
				self._disableConnection()
				log.debug(f"Write failed: {data}, trying to reconnect", exc_info=True)

	def _handleReadQueue(self):
		log.debug(
			f"_ReadQueue is: {self._readQueue}, length {len(self._readQueue)}"
		)
		while len(self._readQueue):
			try:
				data = self._readQueue.popleft()
				log.debug(f"Read: dequeued {data}, {len(self._readQueue)} items left")
			except IndexError:
				log.debug("Read: _readQueue is empty", exc_info=True)
			else:
				if (
					not self.numCells or data == INIT_START_BYTE or self._waitingSettingsByte
				):
					self._handleInitPackets(data)
				else:
					self._handleKeyPresses(data)

	# Display also starts to send init packets when exited internal menu or when
	# delay sending data to display causes its fallback to "wait for connection"
	# state.
	def _handleInitPackets(self, data: bytes):
		if not self._waitingSettingsByte:
			if data != INIT_START_BYTE:
				try:
					while data != INIT_START_BYTE and len(self._readQueue):
						data = self._readQueue.popleft()
						log.debug(f"Read: dequeued {data}, {len(self._readQueue)} items left")
				except IndexError:
					log.debug("Read: _readQueue is empty", exc_info=True)
					return
			# Settings byte
			try:
				data = self._readQueue.popleft()
				log.debug(f"Read: dequeued {data}, {len(self._readQueue)} items left")
			except IndexError:
				self._waitingSettingsByte = True
				log.debug(
					"Read: _readQueue is empty, waiting for settings byte", exc_info=True
				)
				return
			self._writeQueue.appendleft(ESTABLISHED)
			log.debug(f"Write: enqueued {ESTABLISHED}")
			self._somethingToWrite()
			if self._tryToConnect:
				return
		self._setNumCellCount(data)
		# Reconnected or exited device menu if length of _oldCells is numCells.
		# Also checking that _currentCells has sometimes updated.
		# Show last known content.
		if (
			len(self._oldCells) == self.numCells
			and len(self._oldCells) == len(self._currentCells)
		):
			self._clearOldCells()
			with braille._BgThread.queuedWriteLock:
				braille._BgThread.queuedWrite = self._currentCells
			# Queue a call to the background thread.
			braille._BgThread.queueApc(braille._BgThread.executor)
			log.debug(
				"Updating display content after reconnection or display menu exit"
			)
		if self._waitingSettingsByte:
			self._waitingSettingsByte = False

	# If bit 7 (LSB 0 scheme) is 1, there is 80 cells model, else 46 cells model.
	# Other display settings are currently ignored.
	def _setNumCellCount(self, data: bytes):
		self.numCells = 80 if ord(data) >> 7 == 1 else 46

	def _handleKeyPresses(self, data: bytes):
		# in single ctrl-key presses and ctrl-key combinations the first key is
		# resent as last one.
		if ord(data) in CONTROL_KEY_CODES or self._waitingCtrlPacket:
			# at most MAX_COMBINATION_KEYS keys.
			if self._waitingCtrlPacket:
				data = self._partialCtrlPacket + data
			if len(data) > 1 and data[0] == data[len(data) - 1]:
				pass  # enclosed ctrl packet
			else:
				log.debug(f"Partial ctrl packet {data}")
				try:
					while len(data) <= MAX_COMBINATION_KEYS:
						oneKey = self._readQueue.popleft()
						log.debug(f"Read: dequeued key {oneKey}, {len(self._readQueue)} items left")
						# Encloses ctrl packet
						if ord(oneKey) == data[0]:
							# No reason but easier debugging to add oneKey to data
							data += oneKey
							break
						data += oneKey
				except IndexError:
					self._waitingCtrlPacket = True
					self._partialCtrlPacket = data
					log.debug(
						f"Read: Ctrl key packet {data} dequeued partially, "
						"_readQueue is empty", exc_info=True
					)
					return
				if len(data) > MAX_COMBINATION_KEYS and data[len(data) - 1] != data[0]:
					self._waitingCtrlPacket = False
					self._partialCtrlPacket = None
					log.debug(f"Not valid key combination, ignoring {data}")
					return
		log.debug(f"Keys for key press: {data}")
		pressedKeys = set(data)
		try:
			inputCore.manager.executeGesture(InputGestureKeys(pressedKeys))
		# Attribute error which rarely occurs here is something strange.
		except (inputCore.NoInputGestureAction, AttributeError):
			log.debug("", exc_info=True)
		if self._waitingCtrlPacket:
			self._waitingCtrlPacket = False
			self._partialCtrlPacket = None

	# Keep display connected if nothing is sent for a while
	def _keepConnected(self):
		if self._tryToConnect or not self.numCells:
			return
		if time.time() - self._writeTime >= KC_INTERVAL:
			self._writeQueue.append(BOTH_BYTES)
			self._somethingToWrite()

	# Whole display should be updated at next time.
	def _clearOldCells(self):
		for i in range(len(self._oldCells)):
			self._oldCells[i] = 0

	def display(self, cells: List[int]):
		# Keep _currentCells up to date for reconnection regardless
		# of connection state of driver.
		self._currentCells = cells.copy()
		# No connection
		if self._tryToConnect or not self.numCells:
			return
		writeBytes: List[bytes] = [START_BYTE, ]
		# Only changed content is sent (cell index and data).
		for i, cell in enumerate(cells):
			if cell != self._oldCells[i]:
				self._oldCells[i] = cell
				# display indexing starts from 1
				writeBytes.append((i + 1).to_bytes(1, 'big'))
				# Bits have to be reversed.
				# Source: https://stackoverflow.com/questions/12681945/reversing-bits-of-python-integer
				writeBytes.append((int('{:08b}'.format(cell)[::-1], 2).to_bytes(1, 'big')))
		writeBytes.append(END_BYTE)
		if len(writeBytes) < 3:  # Only START_BYTE and END_BYTE
			return
		self._writeQueue.append(b"".join(writeBytes))
		log.debug(f"Write: enqueued {b''.join(writeBytes)}")
		self._somethingToWrite()

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
		# Dictionary keys contain routing and second routing value ranges,
		# and values subtraction required to get actual routing index
		# and corresponding routing name.
		self._routingRanges = {  # range values are inclusive
			(2, 41): (2, "routing"),
			(43, 82): (43, "secondRouting"),
			(111, 150): (71, "routing"),
			(152, 191): (112, "secondRouting"),
		}
		self.keyCodes = set(keys)
		names = []
		for key in self.keyCodes:
			routingTuple = self._getRoutingIndex(key)
			if routingTuple:
				names.append(routingTuple[0])
				self.routingIndex = routingTuple[1]
			else:
				try:
					names.append(KEY_NAMES[key])
				except KeyError:
					log.debugWarning("Unknown key with id %d" % key)
		self.id = "+".join(names)

	def _getRoutingIndex(self, key: int) -> Optional[Tuple[str, int]]:
		""" Get the routing index, if the key is in a routing index range, returns the name of the range and the
		index within that range.
		See _routingRanges
		"""
		for rangeStart, rangeEnd in self._routingRanges:
			value = self._routingRanges[(rangeStart, rangeEnd)]
			indexOffset = value[0]
			routingName = value[1]
			if rangeStart <= key <= rangeEnd:
				return routingName, key - indexOffset
		return None
