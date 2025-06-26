# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-25 NV Access Limited, Burman's Computer and Education Ltd., Leonard de Ruijter

"""Main code for Tivomatic Caiku Albatross braille display driver.
Communication with display is done here. See class L{BrailleDisplayDriver}
for description of most important functions.
"""

import serial
import time

from collections import deque
from bdDetect import DriverRegistrar, ProtocolType
from logHandler import log
from serial.win32 import (
	PURGE_RXABORT,
	PURGE_TXABORT,
	PURGE_RXCLEAR,
	PURGE_TXCLEAR,
	PurgeComm,
)
from threading import (
	Event,
	Lock,
)
from typing import (
	List,
	Optional,
)

import braille
import inputCore
import ui

from . import gestures
from . import _threading

from .constants import (
	BAUD_RATE,
	READ_TIMEOUT,
	WRITE_TIMEOUT,
	SLEEP_TIMEOUT,
	MAX_INIT_RETRIES,
	RESET_COUNT,
	RESET_SLEEP,
	WRITE_QUEUE_LENGTH,
	MAX_COMBINATION_KEYS,
	CONTROL_KEY_CODES,
	LEFT_RIGHT_KEY_CODES,
	KEY_LAYOUT_MASK,
	KeyLayout,
	ESTABLISHED,
	INIT_START_BYTE,
	MAX_SETTINGS_BYTE,
	MAX_STATUS_CELLS_ALLOWED,
	START_BYTE,
	END_BYTE,
	BOTH_BYTES,
	KC_INTERVAL,
	BUS_DEVICE_DESC,
	VID_AND_PID,
)
from .gestures import _gestureMap


class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	"""Communication with display.

	Most important functions:

	- L{_readHandling}; all data from display is read there
	- L{_somethingToWrite}; manages all write operations
	- L{display}; prepares data which should be displayed on braille so
	that display can show it properly
	"""

	name = "albatross"
	# Translators: Names of braille displays.
	description = _("Caiku Albatross 46/80")
	isThreadSafe = True
	supportsAutomaticDetection = True

	@classmethod
	def registerAutomaticDetection(cls, driverRegistrar: DriverRegistrar):
		driverRegistrar.addUsbDevice(
			ProtocolType.SERIAL,
			VID_AND_PID,  # Caiku Albatross 46/80
			# Filter for bus reported device description, which should be "Albatross Braille Display".
			matchFunc=lambda match: match.deviceInfo.get("busReportedDeviceDescription") == BUS_DEVICE_DESC,
		)

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	def __init__(self, port: str = "auto"):
		super().__init__()
		# Number of cells is received when initializing connection.
		self.numCells = 0
		# Used key layout
		self._keyLayout: int
		# Keep old display data, only changed content is sent.
		self._oldCells: List[int] = []
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
		self._baudRate: int
		# When set to True, hopefully blocks some useless write operations during
		# reconnection.
		self._disabledConnection: bool
		# Try to connect or reconnect
		self._tryToConnect = False
		self._readQueue = deque()
		self._writeQueue = deque(maxlen=WRITE_QUEUE_LENGTH)
		self._exitEvent = Event()
		# Thread for read
		self._handleRead = None
		# Display function is called indirectly manually when display is switched
		# back on or exited from internal menu. Ensuring data integrity.
		self._displayLock = Lock()
		# For proper write operations because calls may be from different threads
		self._writeLock = Lock()
		# Timer to keep connection (see L{KC_INTERVAL}).
		self._kc = None
		# When previous write was done (see L{KC_INTERVAL}).
		self._writeTime = 0.0
		self._searchPorts(port)

	def terminate(self):
		"""Destructor.
		Clear display, and close and release all resources before exit.
		"""
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
			log.exception("Error terminating albatross driver")

	def _searchPorts(self, originalPort: str):
		"""Search ports where display can be connected.
		@param originalPort: original port name as string
		@raises: RuntimeError if no display found
		"""
		for self._baudRate in BAUD_RATE:
			for portType, portId, port, portInfo in self._getTryPorts(originalPort):
				# For reconnection
				self._currentPort = port
				self._tryToConnect = True
				self._readHandling()
				if self.numCells:
					# Prepare _oldCells to store last displayed content.
					while len(self._oldCells) < self.numCells:
						self._oldCells.append(0)
					self._kc = _threading.RepeatedTimer(
						KC_INTERVAL,
						self._keepConnected,
					)
					self._handleRead = _threading.ReadThread(
						self._readHandling,
						self._disableConnection,
						self._exitEvent,
						self._dev,
						name="albatross_read",
						daemon=True,
					)
					self._handleRead.start()
					log.info(
						f"Connected to Caiku Albatross {self.numCells} on {portType} port {port} "
						f"at {self._baudRate} bps.",
					)
					break
				# This device initialization failed.
				if self._dev:
					if self._dev.is_open:
						self._dev.close()
					self._dev = None
				log.info(
					f"Connection to {self.description} display on {portType} port {port} "
					f"at {self._baudRate} bps failed.",
				)
			if self.numCells:
				break
		else:
			raise RuntimeError("No Albatross found")

	def _initConnection(self) -> bool:
		"""_initConnection, _initPort, _openPort, _readInitByte and _readSettingsByte
		are helper functions to establish connection.
		If no connection, Albatross sends continuously INIT_START_BYTE
		followed by byte containing various settings like number of cells.

		@raises: RuntimeError if port initialization fails
		@return: C{True} on success, C{False} on connection failure
		"""
		for i in range(MAX_INIT_RETRIES):
			if not self._dev:
				try:
					initState: bool = self._initPort(i)
				except IOError:
					# Port initialization failed. No need to try with 9600 bps,
					# and there is no other port to try.
					log.debug(f"Port {self._currentPort} not initialized", exc_info=True)
					raise RuntimeError(f"Port {self._currentPort} cannot be initialized for Albatross")
				# I/O buffers reset failed, retried again in L{_openPort}
				if not initState:
					continue
			elif not self._dev.is_open:
				if not self._openPort(i):
					continue
			if self._tryToConnect:
				self._tryToConnect = False
			else:
				log.debug(
					f"Sleeping {SLEEP_TIMEOUT} seconds before try {i + 1} / {MAX_INIT_RETRIES}",
				)
				time.sleep(SLEEP_TIMEOUT)
			if not self._readInitByte():
				continue
			if not self._tryToConnect and self.numCells:
				return True
		return False

	def _initPort(self, i: int = MAX_INIT_RETRIES - 1) -> bool:
		"""Initializes port.
		@param i: Just for logging retries.
		@raises: IOError if port initialization fails
		@return: C{True} on success, C{False} on I/O buffers reset failure
		"""
		self._dev = serial.Serial(
			self._currentPort,
			baudrate=self._baudRate,
			stopbits=serial.STOPBITS_ONE,
			parity=serial.PARITY_NONE,
			timeout=READ_TIMEOUT,
			writeTimeout=WRITE_TIMEOUT,
		)
		log.debug(f"Port {self._currentPort} initialized")
		if not self._resetBuffers():
			if i == MAX_INIT_RETRIES - 1:
				return False
			log(
				f"sleeping {SLEEP_TIMEOUT} seconds before try {i + 2} / {MAX_INIT_RETRIES}",
			)
			time.sleep(SLEEP_TIMEOUT)
			return False
		return True

	def _openPort(self, i: int = MAX_INIT_RETRIES - 1) -> bool:
		"""Opens port.
		@param i: Just for logging retries.
		@return: C{True} on success, C{False} on failure
		"""
		try:
			self._dev.open()
			log.debug(f"Port {self._currentPort} opened")
			if not self._resetBuffers():
				if i == MAX_INIT_RETRIES - 1:
					return False
				log(
					f"sleeping {SLEEP_TIMEOUT} seconds before try {i + 2} / {MAX_INIT_RETRIES}",
				)
				time.sleep(SLEEP_TIMEOUT)
				return False
			return True
		except IOError:
			if i == MAX_INIT_RETRIES - 1:
				log.debug(f"Port {self._currentPort} not opened", exc_info=True)
				return False
			log.debug(
				f"Port {self._currentPort} not opened, sleeping {SLEEP_TIMEOUT} seconds "
				f"before try {i + 2} / {MAX_INIT_RETRIES}",
				exc_info=True,
			)
			time.sleep(SLEEP_TIMEOUT)
			return False

	def _readInitByte(self) -> bool:
		"""Reads init byte.
		@return: C{True} on success, C{False} on failure
		"""
		# If ClearCommError fails, in_waiting raises SerialException
		try:
			if not self._dev.in_waiting:
				log.debug("Read: no data")
				return False
		# Considering situation where "albatross_read" thread is about to read
		# but writing to display fails during it - or vice versa - AttributeError
		# might raise.
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
				log.debug(f"Read: INIT_START_BYTE {INIT_START_BYTE} not in {data}")
				return False
		except (IOError, AttributeError):
			self._disableConnection()
			log.debug(
				f"INIT_START_BYTE {INIT_START_BYTE} read failed, trying to reconnect",
				exc_info=True,
			)
			return False

	def _readSettingsByte(self) -> bool:
		"""Reads settings byte.
		@return: C{True} on success, C{False} on failure
		"""
		try:
			# If ClearCommError fails, in_waiting raises SerialException
			if not self._dev.in_waiting:
				self._waitingSettingsByte = True
				log.debug("Read: no data")
				return False
			data = self._dev.read(1)
			log.debug(f"Read: {data}")
			self._writeQueue.append(ESTABLISHED)
			log.debug(f"Write: enqueued {ESTABLISHED}")
			self._somethingToWrite()
			# If write failed
			if self._tryToConnect:
				return False
			self._handleSettingsByte(data)
			return True
		# Considering situation where "albatross_read" thread is about to read
		# but writing to display fails during it - or vice versa - AttributeError
		# might raise.
		except (IOError, AttributeError):
			self._disableConnection()
			log.debug("Settings byte read failed, trying to reconnect", exc_info=True)
			return False

	def _resetBuffers(self) -> bool:
		"""Resets I/O buffers.
		Reset is done L{RESET_COUNT} times to get better results.
		@return: C{True} on success, C{False} on failure
		"""
		try:
			for j in range(RESET_COUNT):
				PurgeComm(
					self._dev._port_handle,
					PURGE_RXCLEAR | PURGE_RXABORT | PURGE_TXCLEAR | PURGE_TXABORT,
				)
				time.sleep(RESET_SLEEP)
			log.debug("I/O buffers reset done")
			return True
		# Considering situation where "albatross_read" thread is about to read
		# but writing to display fails during it - or vice versa - AttributeError
		# might raise.
		except (IOError, AttributeError):
			log.debug(
				f"I/O buffer reset failed on port {self._currentPort}",
				exc_info=True,
			)
			if self._dev.is_open:
				self._dev.close()
			return False

	def _disableConnection(self):
		"""Disables current connection after failure.
		Reconnection retries are started.
		"""
		self._disabledConnection = True
		if self._dev and self._dev.is_open:
			try:
				self._dev.close()
				log.debug(f"Port {self._currentPort} closed")
			except (AttributeError, OSError):
				log.debug(f"Port {self._currentPort} close failed", exc_info=True)
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
		"""Manages all read operations.
		Most of time called from albatross_read thread when there is something to
		read in the port. See L{_threading} module ReadThread class.
		When initial connection is established called from L{_searchPorts} function.
		"""
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

	def _somethingToRead(self) -> Optional[bytes]:
		"""All but connecting/reconnecting related read operations.
		@return: on success returns data, on failure C{None}
		"""
		try:
			# If ClearCommError fails, in_waiting raises SerialException
			if not self._dev.in_waiting:
				return None
			data = self._dev.read(self._dev.in_waiting)
			log.debug(
				f"Read: {data}, length {len(data)}, in_waiting {self._dev.in_waiting}",
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
		"""Filters redundant init packets.
		@param data: Bytes read from display.
		@return: C{True} on success, C{False} on failure
		"""
		settingsByte = None
		for i in data:
			iAsByte = i.to_bytes(1, "big")
			if not self._initByteReceived:
				if iAsByte == INIT_START_BYTE:
					self._initByteReceived = True
					continue
			else:
				if iAsByte <= MAX_SETTINGS_BYTE:
					settingsByte = iAsByte
					self._initByteReceived = False
					continue
				else:
					self._initByteReceived = False
					self._writeQueue.append(ESTABLISHED)
					log.debug(f"Write: enqueued {ESTABLISHED}")
					self._somethingToWrite()
					ui.message(
						_(
							# Translators: A message when number of status cells must be changed
							# for a braille display driver
							"To use an Albatross with NVDA, change the number of status cells in the Albatross's internal menu "
							"to at most {maxCells}, and restart the Albatross and NVDA if needed.",
						).format(maxCells=MAX_STATUS_CELLS_ALLOWED),
					)
					self._disableConnection()
					return False
			self._readQueue.append(iAsByte)
			log.debug(f"Read: enqueued {iAsByte}")
		if settingsByte is not None:
			# Ensuring connection is established also after exit internal menu.
			if not len(self._readQueue):
				self._readQueue.append(INIT_START_BYTE)
				self._readQueue.append(settingsByte)
		return True

	def _somethingToWrite(self):
		"""All write operations."""
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
			# Considering situation where "albatross_read" thread is about to read
			# but writing to display fails during it - or vice versa - AttributeError
			# might raise.
			except (IOError, AttributeError):
				self._disableConnection()
				log.debug(f"Write failed: {data}, trying to reconnect", exc_info=True)

	def _handleReadQueue(self):
		"""Handles data read in L{_readHandling}."""
		log.debug(
			f"_ReadQueue is: {self._readQueue}, length {len(self._readQueue)}",
		)
		while len(self._readQueue):
			try:
				data = self._readQueue.popleft()
				log.debug(f"Read: dequeued {data}, {len(self._readQueue)} items left")
			except IndexError:
				log.debug("Read: _readQueue is empty", exc_info=True)
			else:
				if data == INIT_START_BYTE or self._waitingSettingsByte:
					self._handleInitPackets(data)
				else:
					self._handleKeyPresses(data)

	def _handleInitPackets(self, data: bytes):
		"""Handles init packets.
		Display also starts to send init packets when exited internal menu or when
		delay sending data to display causes its fallback to 'wait for connection'
		state.

		@param data: one byte which can be L{INIT_START_BYTE} or settings byte
		"""
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
					"Read: _readQueue is empty, waiting for settings byte",
					exc_info=True,
				)
				return
			self._writeQueue.appendleft(ESTABLISHED)
			log.debug(f"Write: enqueued {ESTABLISHED}")
			self._somethingToWrite()
			if self._tryToConnect:
				return
		self._handleSettingsByte(data)
		# Reconnected or exited device menu if length of _oldCells is numCells.
		if len(self._oldCells) == self.numCells:
			# Ensure display is updated after reconnection and exit from internal menu.
			self._clearOldCells()
			braille.handler._displayWithCursor()
			log.debug(
				"Updated display content after reconnection or display menu exit",
			)
		if self._waitingSettingsByte:
			self._waitingSettingsByte = False

	def _handleSettingsByte(self, data: bytes):
		"""Extract current settings from settings byte.
		All other settings except number of cells are only notes to screenreader,
		and it is screenreader or driver job to use them when applicable.
		For example, there are no separate status cells in the device but if
		screenreader supports using status cells, it can be notified to use them
		by settings byte.

		Settings byte contain following settings (bits referred by using
		MSB 0 scheme):

		- bit 0: number of cells; 0 = 46, 1 = 80. This is model based value
		which cannot be changed. This is the most important setting, and it
		must be applied.

		- bit 1: switch left side and right side keys; 0 = no, 1 = yes.
		Left, right, down3, up2, routing and secondRouting keys are not affected.
		Up2 and down3 are ignored because they are in the middle of the front
		panel of 80 model so they do not logically belong to left or right side.
		All other keys are switched with corresponding other side keys.

		- bit 2: place of status cells; 0 = left, 1 = right. Not implemented.
		NVDA does not use status cells at the moment.

		- bit 3: all keys act as right side keys; 0 = no, 1 = yes.
		Left, right, down3, up2, routing and secondRouting keys are not affected.
		Up2 and down3 are ignored because they are in the middle of the front
		panel of 80 model so they do not logically belong to left or right side.
		All other left side keys are assigned to corresponding right side keys.

		- bit 1 = 0 and bit 3 = 0: normal key layout.

		- bit 1 = 1 and bit 3 = 1: all keys act as corresponding left side keys.
		Left, right, down3, up2, routing and secondRouting keys are not affected.
		Up2 and down3 are ignored because they are in the middle of the front
		panel of 80 model so they do not logically belong to left or right side.
		All other right side keys are assigned to corresponding left side keys.

		- bits 4 - 7: number of status cells. Not implemented.
		NVDA does not use status cells at the moment.

		@param data: Settings byte
		"""
		self.numCells = 80 if ord(data) >> 7 == 1 else 46
		self._keyLayout = ord(data) >> 4 & KEY_LAYOUT_MASK
		log.debug(
			f"Current settings: number of cells {self.numCells}, "
			f"key layout {KeyLayout(self._keyLayout).name}",
		)
		self._disabledConnection = False

	def _handleKeyPresses(self, data: bytes):
		"""Handles display button presses.
		In single ctrl-key presses and ctrl-key combinations the first key is
		also present as last one. For example, single ctrl-key press F1 is sent
		as "f1 f1", and ctrl-key combination f1 + f2 + f3 + f4 is sent as "f1 f2 f3 f4 f1".
		@param data: single byte which may be whole or partial key press
		"""
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
						f"Read: Ctrl key packet {data} dequeued partially, _readQueue is empty",
						exc_info=True,
					)
					return
				if len(data) > MAX_COMBINATION_KEYS and data[len(data) - 1] != data[0]:
					self._waitingCtrlPacket = False
					self._partialCtrlPacket = None
					log.debug(f"Not valid key combination, ignoring {data}")
					return
		if self._keyLayout != KeyLayout.normal:
			# Using custom key layout
			data = self._changeKeyValues(
				bytearray(data),
			)
		log.debug(f"Keys for key press: {data}")
		pressedKeys = set(data)
		log.debug(f"Forwarding keys {pressedKeys}")
		try:
			inputCore.manager.executeGesture(
				gestures.InputGestureKeys(pressedKeys, self.name),
			)
		# Attribute error which rarely occurs here is something strange.
		except (inputCore.NoInputGestureAction, AttributeError):
			log.debug("", exc_info=True)
		if self._waitingCtrlPacket:
			self._waitingCtrlPacket = False
			self._partialCtrlPacket = None

	def _changeKeyValues(self, data: bytearray) -> bytes:
		"""Changes pressed keys values according to current key layout.
		@param data: pressed keys values.
		@return: pressed keys values based on current key layout.
		"""
		for i, key in enumerate(data):
			if self._keyLayout == KeyLayout.switched:
				if key in LEFT_RIGHT_KEY_CODES.keys():
					data[i] = LEFT_RIGHT_KEY_CODES[key]
				elif key in LEFT_RIGHT_KEY_CODES.values():
					j = list(
						LEFT_RIGHT_KEY_CODES.values(),
					).index(key)
					data[i] = list(
						LEFT_RIGHT_KEY_CODES.keys(),
					)[j]
				continue
			if self._keyLayout == KeyLayout.bothSidesAsRight:
				if key in LEFT_RIGHT_KEY_CODES.keys():
					data[i] = LEFT_RIGHT_KEY_CODES[key]
				continue
			if self._keyLayout == KeyLayout.bothSidesAsLeft:
				if key in LEFT_RIGHT_KEY_CODES.values():
					j = list(
						LEFT_RIGHT_KEY_CODES.values(),
					).index(key)
					data[i] = list(
						LEFT_RIGHT_KEY_CODES.keys(),
					)[j]
		return bytes(data)

	def _keepConnected(self):
		"""Keep display connected if nothing is sent for a while."""
		if self._disabledConnection or self._tryToConnect:
			return
		if time.time() - self._writeTime >= KC_INTERVAL:
			self._writeQueue.append(BOTH_BYTES)
			self._somethingToWrite()

	def _clearOldCells(self):
		"""Whole display should be updated at next time."""
		self._oldCells = [0] * len(self._oldCells)

	def display(self, cells: List[int]):
		"""Prepare cell content for display.
		@param cells: List of cells content
		"""
		# No connection
		if self._tryToConnect or self._disabledConnection:
			log.debug("returning, no connection")
			return
		# Using lock because called also indirectly manually when display is
		# switched back on or exited from internal menu.
		with self._displayLock:
			writeBytes: List[bytes] = [START_BYTE]
			# Only changed content is sent (cell index and data).
			for i, cell in enumerate(cells):
				if cell != self._oldCells[i]:
					self._oldCells[i] = cell
					# display indexing starts from 1
					writeBytes.append((i + 1).to_bytes(1, "big"))
					# Bits have to be reversed.
					writeBytes.append(
						int(
							"{:08b}".format(cell)[::-1],
							2,
						).to_bytes(
							1,
							"big",
						),
					)
			writeBytes.append(END_BYTE)
			if writeBytes == [START_BYTE, END_BYTE]:  # No updated cell content
				return
			self._writeQueue.append(b"".join(writeBytes))
			log.debug(f"Write: enqueued {b''.join(writeBytes)}")
		self._somethingToWrite()

	gestureMap = _gestureMap
