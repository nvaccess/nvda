# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import struct
import functools
import operator
import enum
from dataclasses import dataclass
import ctypes
import serial
import inputCore
import braille
import hwIo
from logHandler import log
from autoSettingsUtils.driverSetting import DriverSetting
from autoSettingsUtils.utils import StringParameterInfo
from tactile import TactileGraphicsBuffer
from tactile.braille import drawBrailleCells


BAUD_RATE = 115200
PARITY = serial.PARITY_NONE


class DP_Command(enum.IntEnum):
	REQ_FIRMWARE_VERSION = 0x0000
	RSP_FIRMWARE_VERSION = 0x0001
	REQ_DEVICE_NAME = 0x0100
	RSP_DEVICE_NAME = 0x0101
	REQ_BOARD_INFORMATION = 0x0110
	RSP_BOARD_INFORMATION = 0x0111
	REQ_DISPLAY_LINE = 0x0200
	RSP_DISPLAY_LINE = 0x0201
	NTF_DISPLAY_LINE = 0x0202
	REQ_DISPLAY_CURSOR = 0x0210
	RSP_DISPLAY_CURSOR = 0x0211
	NTF_DISPLAY_CURSOR = 0x0212
	NTF_KEYS_SCROLL = 0x0302
	NTF_KEYS_PERKINS = 0x0312
	NTF_KEYS_ROUTING = 0x0322
	NTF_KEYS_FUNCTION = 0x0332
	NTF_ERROR = 0x9902


class DP_ErrorCode(enum.IntEnum):
	LENGTH = 1
	COMMAND = 2
	CHECKSUM = 3
	PARAMETER = 4
	TIMEOUT = 5


class DP_DisplayResponse(enum.IntEnum):
	ACK = 0
	NACK = 1
	WAIT = 2
	CHECKSUM = 3


class DP_Features(enum.IntFlag):
	HAS_GRAPHIC_DISPLAY = 0x80
	HAS_TEXT_DISPLAY = 0x40
	HAS_PERKINS_KEYS = 0x20
	HAS_ROUTING_KEYS = 0x10
	HAS_NAVIGATION_KEYS = 0x08
	HAS_PANNING_KEYS = 0x04
	HAS_FUNCTION_KEYS = 0x02


class DP_DisplayDescriptor(ctypes.Structure):
	_fields_ = [
		("rowCount", ctypes.c_ubyte),
		("columnCount", ctypes.c_ubyte),
		("dividedLine", ctypes.c_ubyte),
		("refreshTime", ctypes.c_ubyte),
	]


class DP_BoardInformation(ctypes.Structure):
	_fields_ = [
		("features", ctypes.c_ubyte),
		("dotsPerCell", ctypes.c_ubyte),
		("distanceBetweenPins", ctypes.c_ubyte),
		("functionKeyCount", ctypes.c_ubyte),
		("text", DP_DisplayDescriptor),
		("graphic", DP_DisplayDescriptor),
	]


class DP_PacketSeqFlag(enum.IntEnum):
	SEQ_TEXT = 0x80


class DP_PacketSyncByte(enum.IntEnum):
	SYNC1 = 0xAA
	SYNC2 = 0x55


class DP_PerkinsKey(enum.IntEnum):
	DOT7 = 0
	DOT3 = 1
	DOT2 = 2
	DOT1 = 3
	DOT4 = 4
	DOT5 = 5
	DOT6 = 6
	DOT8 = 7
	SPACE = 8
	SHIFT_LEFT = 9
	CONTROL_LEFT = 10
	SHIFT_RIGHT = 11
	CONTROL_RIGHT = 12
	PAN_LEFT = 13
	PAN_RIGHT = 14
	NAV_CENTER = 16
	NAV_UP = 17
	NAV_RIGHT = 18
	NAV_DOWN = 19
	NAV_LEFT = 20


DP_CHECKSUM_BASE = 0xA5


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
	supportsAutomaticDetection = False
	receivesAckPackets = False
	timeout = 0.2
	_boardInformation: DP_BoardInformation | None = None
	cellWidth = 2
	cellHeight = 4
	hCellPadding = 1
	vCellPadding = 1
	_brailleDestination: BrailleDestination

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	supportedSettings = [
		DriverSetting(
			"brailleDestination",
			# Translators: Label for a setting that allows the user to choose the destination for braille output.
			_("Braille destination"),
			useConfig=True,
		),
	]

	_lastResponse: dict[int, CommandResponse] = {}

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
					ctypes.windll.kernel32.SleepEx(50, True)
			else:
				raise RuntimeError(f"No response to {cmd.name}")
			return response.data
		return b""

	def _onReceive(self, header1: bytes):
		if ord(header1) != DP_PacketSyncByte.SYNC1:
			raise RuntimeError(f"Bad {header1=}")
		header2 = self._dev.read(1)
		if ord(header2) != DP_PacketSyncByte.SYNC2:
			raise RuntimeError(f"bad {header2=}")
		length = struct.unpack(">H", self._dev.read(2))[0]
		packetBody = self._dev.read(length)
		dest, cmdHigh, cmdLow, seqNum, *data, checksum = packetBody
		data = bytes(data)
		if checksum != functools.reduce(operator.xor, packetBody[:-1], DP_CHECKSUM_BASE):
			raise RuntimeError("bad checksum")
		cmd = DP_Command(struct.unpack(">H", bytes([cmdHigh, cmdLow]))[0])
		log.debug(f"Received responce  {cmd.name}, {dest=}, {seqNum=}, data={bytes(data)}")
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

	_displayLineCache = {}

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

	def __init__(self, port: str):
		self._dev = hwIo.Serial(
			port=port,
			baudrate=BAUD_RATE,
			parity=PARITY,
			timeout=self.timeout,
			writeTimeout=self.timeout,
			onReceive=self._onReceive,
		)
		self.model = self._requestDeviceName()
		self._boardInformation = self._requestBoardInformation()
		if self._boardInformation.features & DP_Features.HAS_TEXT_DISPLAY:
			self._brailleDestination = BrailleDestination.TEXT
		elif self._boardInformation.features & DP_Features.HAS_GRAPHIC_DISPLAY:
			self._brailleDestination = BrailleDestination.GRAPHIC
		else:
			raise RuntimeError("No text or graphics displays")
		super().__init__()

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
	_pendingCells = None

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
