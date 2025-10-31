# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024-2025 NV Access Limited, Dot Incorporated, Bram Duvigneau
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import struct
import functools
import operator
import enum
from dataclasses import dataclass
import serial
import hwIo.ble
import inputCore
import braille
import winBindings.kernel32
import bdDetect
from logHandler import log
from autoSettingsUtils.driverSetting import DriverSetting
from autoSettingsUtils.utils import StringParameterInfo
from tactile import TactileGraphicsBuffer
from tactile.braille import drawBrailleCells
from .defs import (
	DP_Command,
	DP_DisplayResponse,
	DP_Features,
	DP_PacketSeqFlag,
	DP_PacketSyncByte,
	DP_PerkinsKey,
	DP_BoardInformation,
	DP_CHECKSUM_BASE,
	BLE_SERVICE_UUID,
	BLE_READ_CHARACTERISTIC_UUID,
	BLE_WRITE_CHARACTERISTIC_UUID,
)


class DpTactileGraphicsBuffer(TactileGraphicsBuffer):
	cellWidth = 2
	cellHeight = 4

	def __init__(self, hCellCount: int, vCellCount: int):
		self.hCellCount = hCellCount
		self.vCellCount = vCellCount
		self._cellBuffer = bytearray(hCellCount * vCellCount)
		hPixelCount = hCellCount * self.cellWidth
		vPixelCount = vCellCount * self.cellHeight
		super().__init__(hPixelCount, vPixelCount)

	def setDot(self, x: int, y: int):
		if not (0 <= x < self.width) or not (0 <= y < self.height):
			return
		vCellIndex = int(y / self.cellHeight)
		hCellIndex = int(x / self.cellWidth)
		cellIndex = (vCellIndex * self.hCellCount) + hCellIndex
		bit = (y % self.cellHeight) + ((x % self.cellWidth) * self.cellHeight)
		self._cellBuffer[cellIndex] |= 2**bit

	def getRowCells(self, row: int):
		startIndex = row * self.hCellCount
		return self._cellBuffer[startIndex : startIndex + self.hCellCount]


@dataclass
class CommandResponse:
	cmd: DP_Command
	data: bytes
	dest: int
	seqNum: int


class BrailleDestination(enum.StrEnum):
	TEXT = "text"
	GRAPHIC = "graphic"


class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	"""
	Driver for DotPad Braille / Tactile Graphic display.
	"""

	name = "dotPad"
	isThreadSafe = True
	# Translators: Description of the DotPad Braille / Tactile Graphic display.
	description = _("DotPad Braille / Tactile Graphic display")
	supportsAutomaticDetection = True
	receivesAckPackets = False
	timeout = 0.2
	_boardInformation: DP_BoardInformation | None = None
	cellWidth = 2
	cellHeight = 4
	hCellPadding = 1
	vCellPadding = 1
	_brailleDestination: BrailleDestination
	SERIAL_BAUD_RATE = 115200
	SERIAL_PARITY = serial.PARITY_NONE

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	@classmethod
	def check(cls) -> bool:
		"""DotPad is available if BLE is supported or manual ports exist.

		This allows DotPad to appear in the braille display list even when
		no devices are currently detected, enabling users to manually select
		BLE devices after the GUI triggers a scan.
		"""
		# Check if BLE is available on this system
		if hwIo.ble.isAvailable():
			return True

		# Fallback: check if manual serial ports exist
		try:
			next(cls.getManualPorts())
			return True
		except (StopIteration, NotImplementedError):
			pass

		return False

	@classmethod
	def registerAutomaticDetection(cls, driverRegistrar: bdDetect.DriverRegistrar):
		driverRegistrar.addUsbDevices(
			bdDetect.ProtocolType.SERIAL,
			{
				"VID_0403&PID_6010",  # FTDI Dual RS232 as used in DotPad320A
			},
		)
		driverRegistrar.addBleDevices(cls._isBleDotPad)

	@staticmethod
	def _isBleDotPad(match: bdDetect.DeviceMatch) -> bool:
		"""Check if a BLE device is a DotPad display.

		:param match: DeviceMatch object containing BLE device information
		:return: True if device ID (name or address) starts with "DotPad"
		"""
		return match.id.startswith("DotPad")

	supportedSettings = [
		DriverSetting(
			"brailleDestination",
			# Translators: Label for a setting that allows the user to choose the destination for braille output.
			_("Braille destination"),
			useConfig=True,
		),
	]

	_lastResponse: dict[int, CommandResponse] = {}
	_receiveBuffer: bytearray = bytearray()
	MAX_PACKET_SIZE = 512  # Safety limit to prevent memory issues with malformed streams

	def _sendCommand(
		self,
		cmd: DP_Command,
		data: bytes = b"",
		dest: int = 0,
		seqNum: int = 0,
		rspCmd: DP_Command | None = None,
	) -> bytes:
		log.debug(f"Sending command  {cmd.name}, {dest=}, {seqNum=}, data={bytes(data)}")
		packetBody = bytearray(
			[
				dest,
				*struct.pack(">H", cmd.value),
				seqNum,
				*data,
			],
		)
		checksum = functools.reduce(operator.xor, packetBody, DP_CHECKSUM_BASE)
		packetBody.append(checksum)
		packet = bytearray(
			[
				DP_PacketSyncByte.SYNC1,
				DP_PacketSyncByte.SYNC2,  # header
				# Length of packet body
				*struct.pack(">H", len(packetBody)),
				*packetBody,
			],
		)
		self._dev.write(packet)
		if rspCmd is not None:
			for x in range(20, -1, -1):
				response = self._lastResponse.pop(dest, None)
				if response is not None and response.cmd == rspCmd and response.dest == dest:
					break
				if x > 0:
					winBindings.kernel32.SleepEx(50, True)
			else:
				raise RuntimeError(f"No response to {cmd.name}")
			return response.data
		return b""

	def _onReceive(self, data: bytes):
		"""Handle received data from either Serial (1 byte) or BLE (full packets).

		This method buffers incoming data and extracts complete packets as they arrive.
		It works with both byte-at-a-time delivery (Serial) and packet-based delivery (BLE).

		:param data: Received data (1 byte for Serial, variable length for BLE)
		"""
		self._receiveBuffer.extend(data)

		# Safety check: prevent unbounded buffer growth from malformed streams
		if len(self._receiveBuffer) > self.MAX_PACKET_SIZE:
			log.warning(
				f"Receive buffer exceeded {self.MAX_PACKET_SIZE} bytes, discarding data and resyncing",
			)
			self._receiveBuffer.clear()
			return

		# Extract and process all complete packets from the buffer
		while len(self._receiveBuffer) >= 4:  # Minimum: SYNC1 + SYNC2 + length (2 bytes)
			# Check for first sync byte
			if self._receiveBuffer[0] != DP_PacketSyncByte.SYNC1:
				# Discard bad byte and try to resynchronize
				log.debug(f"Bad first sync byte: 0x{self._receiveBuffer[0]:02x}, discarding")
				self._receiveBuffer.pop(0)
				continue

			# Check for second sync byte
			if self._receiveBuffer[1] != DP_PacketSyncByte.SYNC2:
				# Discard first byte and try again
				log.debug(f"Bad second sync byte: 0x{self._receiveBuffer[1]:02x}, discarding")
				self._receiveBuffer.pop(0)
				continue

			# Extract packet length from header
			packetLength = struct.unpack(">H", bytes(self._receiveBuffer[2:4]))[0]
			totalLength = 4 + packetLength  # header (4 bytes) + body

			# Check if we have the complete packet
			if len(self._receiveBuffer) < totalLength:
				# Not enough data yet, wait for more
				break

			# Extract complete packet
			packet = bytes(self._receiveBuffer[:totalLength])
			self._receiveBuffer = self._receiveBuffer[totalLength:]

			# Process the packet body (skip 4-byte header: SYNC1, SYNC2, length)
			try:
				self._processPacket(packet[4:])
			except Exception:
				log.error("Error processing packet", exc_info=True)

	def _processPacket(self, packetBody: bytes):
		"""Process a complete packet body (after sync bytes and length header).

		:param packetBody: The packet body containing dest, command, sequence, data, and checksum
		"""
		dest, cmdHigh, cmdLow, seqNum, *data, checksum = packetBody
		data = bytes(data)

		# Verify checksum
		if checksum != functools.reduce(operator.xor, packetBody[:-1], DP_CHECKSUM_BASE):
			raise RuntimeError("bad checksum")

		# Parse command
		cmd = DP_Command(struct.unpack(">H", bytes([cmdHigh, cmdLow]))[0])
		log.debug(f"Received response  {cmd.name}, {dest=}, {seqNum=}, data={bytes(data)}")

		# Route to appropriate handler
		if cmd.name.startswith("RSP_"):
			self._recordCommandResponse(cmd, data, dest, seqNum)
		elif cmd.name.startswith("NTF_"):
			self._handleNotification(cmd, data, dest, seqNum)

	def _recordCommandResponse(self, cmd: DP_Command, data: bytes, dest: int = 0, seqNum: int = 0):
		self._lastResponse[dest] = CommandResponse(cmd, data, dest, seqNum)

	def _requestDeviceName(self) -> str:
		data = self._sendCommand(DP_Command.REQ_DEVICE_NAME, rspCmd=DP_Command.RSP_DEVICE_NAME)
		return data.decode("ascii")

	def _requestBoardInformation(self) -> DP_BoardInformation:
		data = self._sendCommand(DP_Command.REQ_BOARD_INFORMATION, rspCmd=DP_Command.RSP_BOARD_INFORMATION)
		return DP_BoardInformation.from_buffer_copy(data)

	_displayLineCache: dict[int, bytes] = {}

	def _requestDisplayLine(self, dest: int, data: bytes, seqNum: int = 0):
		oldData = self._displayLineCache.get(dest)
		if oldData == data:
			return
		code = self._sendCommand(
			DP_Command.REQ_DISPLAY_LINE,
			data,
			dest,
			seqNum,
			rspCmd=DP_Command.RSP_DISPLAY_LINE,
		)
		code = DP_DisplayResponse(ord(code))
		if code == DP_DisplayResponse.ACK:
			self._displayLineCache[dest] = data
			return
		elif code == DP_DisplayResponse.NACK:
			log.debug("Request not acknowledged")
		elif code == DP_DisplayResponse.CHECKSUM:
			raise RuntimeError("Bad checksum")

	def _handleNotification(self, cmd: DP_Command, data: bytes, dest: int = 0, seqNum: int = 0):
		if cmd == DP_Command.NTF_KEYS_PERKINS:
			log.debug(f"Perkins keys {data}")
		if cmd in (DP_Command.NTF_KEYS_FUNCTION, DP_Command.NTF_KEYS_PERKINS):
			try:
				gesture = DPKeyGesture(self.model, cmd, data)
			except ValueError:
				return
			if inputCore.manager is not None:
				try:
					inputCore.manager.executeGesture(gesture)
				except inputCore.NoInputGestureAction:
					pass

	def __init__(self, port: str = "auto"):
		# _getTryPorts handles all port types: "auto", "ble:DeviceName@Address", COM ports, etc.
		# It yields DeviceMatch objects with type, id, port, and deviceInfo fields
		for match in self._getTryPorts(port):
			if self._tryConnect(match.port, match.type, match.deviceInfo):
				break
		else:
			raise RuntimeError("No DotPad device found")

		super().__init__()

	def _tryConnect(self, port: str, portType: str, portInfo: dict) -> bool:
		"""Try to connect to a DotPad device on the given port.

		:param port: The port to connect to (COM port or BLE address).
		:param portType: The protocol type (from bdDetect.ProtocolType).
		:param portInfo: Additional port information dictionary.
		:return: True if connection successful, False otherwise.
		"""
		try:
			if portType == bdDetect.ProtocolType.BLE:
				address = portInfo.get("address") or port

				# Try to get BLEDevice from scanner first (preferred - avoids implicit discovery)
				device = hwIo.ble.findDeviceByAddress(address)

				if device is None:
					# Fallback: Use address string directly
					# Note: This triggers implicit discovery in Bleak, but ensures connection succeeds
					log.debug(f"BLE device {address} not in scan results, using address for connection")
					device = address  # Pass string address to Ble class

				self._dev = hwIo.ble.Ble(
					device=device,  # Can be BLEDevice or str
					writeServiceUuid=BLE_SERVICE_UUID,
					writeCharacteristicUuid=BLE_WRITE_CHARACTERISTIC_UUID,
					readServiceUuid=BLE_SERVICE_UUID,
					readCharacteristicUuid=BLE_READ_CHARACTERISTIC_UUID,
					onReceive=self._onReceive,
				)
			else:
				self._dev = hwIo.Serial(
					port=port,
					baudrate=self.SERIAL_BAUD_RATE,
					parity=self.SERIAL_PARITY,
					timeout=self.timeout,
					writeTimeout=self.timeout,
					onReceive=self._onReceive,
				)

			# Verify this is actually a DotPad device
			self.model = self._requestDeviceName()
			self._boardInformation = self._requestBoardInformation()
			if self._boardInformation.features & DP_Features.HAS_TEXT_DISPLAY:
				self._brailleDestination = BrailleDestination.TEXT
			elif self._boardInformation.features & DP_Features.HAS_GRAPHIC_DISPLAY:
				self._brailleDestination = BrailleDestination.GRAPHIC
			else:
				raise RuntimeError("No text or graphics displays")
			return True
		except Exception:
			# Clean up on failure
			log.debugWarning("Failed to connect", exc_info=True)
			try:
				self._dev.close()
			except Exception:
				pass
			return False

	def terminate(self):
		try:
			super().terminate()
		finally:
			# Make sure the device gets closed.
			# If it doesn't, we may not be able to re-open it later.
			self._dev.close()

	def _get_availableBrailledestinations(self):
		if self._boardInformation is None:
			return {}
		dests = {}
		if self._boardInformation.features & DP_Features.HAS_TEXT_DISPLAY:
			dests[BrailleDestination.TEXT.value] = StringParameterInfo(
				BrailleDestination.TEXT.value,
				# Translators: A destination for braille output.
				_("Text"),
			)
		if self._boardInformation.features & DP_Features.HAS_GRAPHIC_DISPLAY:
			dests[BrailleDestination.GRAPHIC.value] = StringParameterInfo(
				BrailleDestination.GRAPHIC.value,
				# Translators: A destination for braille output.
				_("Graphic"),
			)
		return dests

	def _get_brailleDestination(self) -> str:
		return self._brailleDestination.value

	def _set_brailleDestination(self, value: str):
		value = BrailleDestination(value)
		if self._boardInformation is None:
			raise RuntimeError("No board information")
		if value != self._brailleDestination:
			self.display([0] * self.numRows * self.numCols)
		if (
			value == BrailleDestination.TEXT
			and self._boardInformation.features & DP_Features.HAS_TEXT_DISPLAY
		):
			self._brailleDestination = value
		elif (
			value == BrailleDestination.GRAPHIC
			and self._boardInformation.features & DP_Features.HAS_GRAPHIC_DISPLAY
		):
			self._brailleDestination = value
		else:
			raise ValueError(f"Unsupported destination {value}")

	def _get_numRows(self) -> int:
		if self._boardInformation is None:
			return 0
		if self._brailleDestination == BrailleDestination.GRAPHIC:
			return (self._boardInformation.graphic.rowCount * self.cellHeight) // (
				self.cellHeight + self.vCellPadding
			)
		else:
			return self._boardInformation.text.rowCount

	def _get_numCols(self) -> int:
		if self._boardInformation is None:
			return 0
		if self._brailleDestination == BrailleDestination.GRAPHIC:
			return (self._boardInformation.graphic.columnCount * self.cellWidth) // (
				self.cellWidth + self.hCellPadding
			)
		else:
			return self._boardInformation.text.columnCount

	_inDisplay = False
	_pendingCells: list[int] | None = None

	def display(self, cells: list[int]):
		if self._boardInformation is None:
			return
		self._pendingCells = cells
		if self._inDisplay:
			return
		self._inDisplay = True
		try:
			while self._pendingCells is not None:
				cells = self._pendingCells
				self._pendingCells = None
				if self._brailleDestination == BrailleDestination.GRAPHIC:
					tgBuf = DpTactileGraphicsBuffer(
						hCellCount=self._boardInformation.graphic.columnCount,
						vCellCount=self._boardInformation.graphic.rowCount,
					)
					for y in range(self.numRows):
						cellOffset = y * self.numCols
						lineCells = cells[cellOffset : cellOffset + self.numCols]
						drawBrailleCells(
							tgBuf,
							0,
							y * (self.cellHeight + self.vCellPadding),
							lineCells,
							hCellPadding=self.hCellPadding,
						)
					firstGraphicRow = 0
					if self._boardInformation.features & DP_Features.HAS_TEXT_DISPLAY:
						firstGraphicRow = self._boardInformation.text.rowCount
					for y in range(tgBuf.vCellCount):
						self._requestDisplayLine(
							dest=firstGraphicRow + y,
							data=b"\x00" + bytes(tgBuf.getRowCells(y)),
						)
				else:  # text destination
					for y in range(self.numRows):
						self._requestDisplayLine(
							dest=y,
							data=b"\x00" + bytes(cells[y * self.numCols : (y + 1) * self.numCols]),
							seqNum=DP_PacketSeqFlag.SEQ_TEXT,
						)
		finally:
			self._inDisplay = False

	gestureMap = inputCore.GlobalGestureMap(
		{
			"globalCommands.GlobalCommands": {
				"braille_scrollBack": ("br(dotPad):pan_left",),
				"braille_scrollForward": ("br(dotPad):pan_right",),
			},
		},
	)


class DPKeyGesture(braille.BrailleDisplayGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, model: str, cmd: DP_Command, data: bytes):
		self.model = model
		if cmd == DP_Command.NTF_KEYS_FUNCTION:
			functionNum = 0
			for dataByte in data:
				for bit in range(7, -1, -1):
					functionNum += 1
					if dataByte & 1 << bit:
						self.id = f"function{functionNum}"
						return
			else:
				raise ValueError("No function key")
		elif cmd == DP_Command.NTF_KEYS_PERKINS:
			for key in DP_PerkinsKey:
				dataIndex, bitIndex = divmod(key.value, 8)
				bitIndex = 7 - bitIndex
				if data[dataIndex] & 1 << bitIndex:
					self.id = key.name.lower()
					return
		raise ValueError(f"Unsupported command {cmd.name}")
