# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2023 NV Access Limited, Babbage B.V., Eurobraille

from collections import defaultdict
from typing import Dict, Any, List, Union
import re

from io import BytesIO
import serial
import bdDetect
import braille
import inputCore
from logHandler import log
import hwIo
from baseObject import ScriptableObject
import wx
import threading
from globalCommands import SCRCAT_BRAILLE
import ui
import time

from . import constants
from . import gestures


def bytesToInt(byteData: bytes):
	"""Converts bytes to its integral equivalent."""
	return int.from_bytes(byteData, byteorder="big", signed=False)


class BrailleDisplayDriver(braille.BrailleDisplayDriver, ScriptableObject):
	_dev: hwIo.IoBase
	# Used to for error checking.
	_awaitingFrameReceipts: Dict[int, Any]
	name = constants.name
	# Translators: Names of braille displays.
	description = constants.description
	isThreadSafe = True
	supportsAutomaticDetection = True
	timeout = 0.2
	supportedSettings = (braille.BrailleDisplayDriver.HIDInputSetting(useConfig=True),)

	@classmethod
	def registerAutomaticDetection(cls, driverRegistrar: bdDetect.DriverRegistrar):
		driverRegistrar.addUsbDevices(
			bdDetect.ProtocolType.HID,
			{
				"VID_C251&PID_1122",  # Esys (version < 3.0, no SD card
				"VID_C251&PID_1123",  # Esys (version >= 3.0, with HID keyboard, no SD card
				"VID_C251&PID_1124",  # Esys (version < 3.0, with SD card
				"VID_C251&PID_1125",  # Esys (version >= 3.0, with HID keyboard, with SD card
				"VID_C251&PID_1126",  # Esys (version >= 3.0, no SD card
				"VID_C251&PID_1127",  # Reserved
				"VID_C251&PID_1128",  # Esys (version >= 3.0, with SD card
				"VID_C251&PID_1129",  # Reserved
				"VID_C251&PID_112A",  # Reserved
				"VID_C251&PID_112B",  # Reserved
				"VID_C251&PID_112C",  # Reserved
				"VID_C251&PID_112D",  # Reserved
				"VID_C251&PID_112E",  # Reserved
				"VID_C251&PID_112F",  # Reserved
				"VID_C251&PID_1130",  # Esytime
				"VID_C251&PID_1131",  # Reserved
				"VID_C251&PID_1132",  # Reserved
			},
		)
		driverRegistrar.addUsbDevices(
			bdDetect.ProtocolType.SERIAL,
			{
				"VID_28AC&PID_0012",  # b.note
				"VID_28AC&PID_0013",  # b.note 2
				"VID_28AC&PID_0020",  # b.book internal
				"VID_28AC&PID_0021",  # b.book external
			},
		)

		driverRegistrar.addBluetoothDevices(lambda m: m.id.startswith("Esys"))

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	def __init__(self, port="Auto"):
		super().__init__()
		self.numCells = 0
		self.deviceType = None
		self._deviceData = {}
		self._awaitingFrameReceipts = {}
		self._frameLength = None
		self._frame = 0x20
		self._frameLock = threading.Lock()
		self._hidKeyboardInput = False
		self._hidInputBuffer = b""

		for portType, portId, port, portInfo in self._getTryPorts(port):
			# At this point, a port bound to this display has been found.
			# Try talking to the display.
			self.isHid = portType == bdDetect.ProtocolType.HID
			try:
				if self.isHid:
					self._dev = hwIo.Hid(
						port,
						onReceive=self._onReceive,
						# Eurobraille wants us not to block other application's access to this handle.
						exclusive=False,
					)
				else:
					self._dev = hwIo.Serial(
						port,
						baudrate=constants.BAUD_RATE,
						bytesize=serial.EIGHTBITS,
						parity=serial.PARITY_EVEN,
						stopbits=serial.STOPBITS_ONE,
						timeout=self.timeout,
						writeTimeout=self.timeout,
						onReceive=self._onReceive,
					)
			except EnvironmentError:
				log.debugWarning(f"Error while connecting to port {port}", exc_info=True)
				continue

			for i in range(3):
				# Request device identification
				self._sendPacket(constants.EB_SYSTEM, constants.EB_SYSTEM_IDENTITY)
				# Make sure visualisation packets are disabled, as we ignore them anyway.
				self._sendPacket(constants.EB_VISU, constants.EB_VISU_DOT, constants.EB_FALSE)
				# A device identification results in multiple packets.
				# Make sure we've received everything before we continue
				while self._dev.waitForRead(2 * self.timeout):
					continue
				if self.numCells and self.deviceType:
					break
			if self.numCells and self.deviceType:
				# A display responded.
				log.info(
					"Found {device} connected via {type} ({port})".format(
						device=self.deviceType,
						type=portType,
						port=port,
					),
				)
				if self.deviceType.startswith(("bnote", "bbook")):
					# send identifier to bnote / bbook with current COM port
					comportNumber = f"{int(re.match('.*?([0-9]+)$', port).group(1)):02d}"
					identifier = f"NVDA/{comportNumber}".encode()
					log.debug(f"sending {identifier} to eurobraille display")
					self._sendPacket(constants.EB_SYSTEM, constants.EB_CONNECTION_NAME, identifier)
				break
			self._dev.close()

		else:
			raise RuntimeError("No supported Eurobraille display found")

		self.keysDown = defaultdict(int)
		self._ignoreCommandKeyReleases = False

	def terminate(self):
		try:
			if self.deviceType.startswith(("bnote", "bbook")):
				# reset identifier to bnote / bbook with current COM port
				self._sendPacket(constants.EB_SYSTEM, constants.EB_CONNECTION_NAME, b"")
			super().terminate()
		finally:
			# We must sleep before closing the port as not doing this can leave
			# the display in a bad state where it can not be re-initialized.
			time.sleep(self.timeout)
			self._dev.close()
			self._dev = None
			self._deviceData.clear()

	def _prepFirstByteStreamAndData(
		self,
		data: bytes,
	) -> tuple[bytes, Union[BytesIO, hwIo.IoBase], bytes]:
		if self.isHid:
			# data contains the entire packet.
			# HID Packets start with 0x00.
			byte0 = data[0:1]
			assert byte0 == b"\x00", "byte 0 is %r" % byte0
			# Check whether there is an incomplete packet in the buffer
			if self._hidInputBuffer:
				data = self._hidInputBuffer + data[1:]
				self._hidInputBuffer = b""
			byte1 = data[1:2]
			stream = BytesIO(data)
			stream.seek(2)
			return byte1, stream, data
		else:  # is serial
			return data, self._dev, data

	def _onReceive(self, data: bytes):
		byte1, stream, data = self._prepFirstByteStreamAndData(data)

		if byte1 == constants.ACK:
			frame = ord(stream.read(1))
			self._handleAck(frame)
		elif byte1 == constants.STX:
			length = bytesToInt(stream.read(2)) - 2  # length includes the length itself
			packet: bytes = stream.read(length)
			if self.isHid and not stream.read(1) == constants.ETX:
				# Incomplete packet
				self._hidInputbuffer = data
				return
			packetType: bytes = packet[0:1]
			packetSubType: bytes = packet[1:2]
			packetData: bytes = packet[2:] if length > 2 else b""
			if packetType == constants.EB_SYSTEM:
				self._handleSystemPacket(packetSubType, packetData)
			elif packetType == constants.EB_MODE:
				if packetSubType == constants.EB_MODE_DRIVER:
					log.debug("Braille display switched to driver mode, updating display...")
					braille.handler.update()
				elif packetSubType == constants.EB_MODE_INTERNAL:
					log.debug("Braille display switched to internal mode")
			elif packetType == constants.EB_KEY:
				self._handleKeyPacket(packetSubType, packetData)
			elif packetType == constants.EB_IRIS_TEST and packetSubType == constants.EB_IRIS_TEST_sub:
				# Ping command sent by Iris every two seconds, send it back on the main thread.
				# This means that, if the main thread is frozen, Iris will be notified of this.
				log.debug("Received ping from Iris braille display")
				wx.CallAfter(self._sendPacket, packetType, packetSubType, packetData)
			elif packetType == constants.EB_VISU:
				log.debug("Ignoring visualisation packet")
			elif packetType == constants.EB_ENCRYPTION_KEY:
				log.debug("Ignoring encryption key packet")
			else:
				log.debug(f"Ignoring packet: type {packetType}, subtype {packetSubType}, data {packetData}")

	def _handleAck(self, frame: int):
		try:
			super()._handleAck()
		except NotImplementedError:
			log.debugWarning(f"Received ACK for frame {frame} while ACK handling is disabled")
		else:
			try:
				del self._awaitingFrameReceipts[frame]
			except KeyError:
				log.debugWarning(f"Received ACK for unregistered frame {frame}")

	def _handleSystemPacket(self, packetType: bytes, data: bytes):
		if packetType == constants.EB_SYSTEM_TYPE:
			deviceType = ord(data)
			self.deviceType = constants.DEVICE_TYPES[deviceType]
			if 0x01 <= deviceType <= 0x06:  # Iris
				self.keys = constants.KEYS_IRIS
			elif 0x07 <= deviceType <= 0x0D:  # Esys
				self.keys = constants.KEYS_ESYS
			elif 0x0E <= deviceType <= 0x11:  # Esitime
				self.keys = constants.KEYS_ESITIME
			elif 0x12 <= deviceType <= 0x13:
				self.keys = constants.KEYS_BNOTE
			elif 0x14 <= deviceType <= 0x15:
				self.keys = constants.KEYS_BBOOK
			else:
				log.debugWarning(f"Unknown device identifier {data}")
		elif packetType == constants.EB_SYSTEM_DISPLAY_LENGTH:
			self.numCells = ord(data)
		elif packetType == constants.EB_SYSTEM_FRAME_LENGTH:
			self._frameLength = bytesToInt(data)
		elif packetType == constants.EB_SYSTEM_PROTOCOL and self.isHid:
			protocol = data.rstrip(b"\x00 ")
			try:
				version = float(protocol[:4])
			except ValueError:
				pass
			else:
				self.receivesAckPackets = version >= 3.0
		elif packetType == constants.EB_SYSTEM_IDENTITY:
			return  # End of system information
		self._deviceData[packetType] = data.rstrip(b"\x00 ")

	def _handleKeyPacket(self, group: bytes, data: bytes):
		if group == constants.EB_KEY_USB_HID_MODE:
			assert data in [constants.EB_TRUE, constants.EB_FALSE]
			self._hidKeyboardInput = constants.EB_TRUE == data
			return
		if group == constants.EB_KEY_QWERTY:
			log.debug("Ignoring Iris AZERTY/QWERTY input")
			return
		if group == constants.EB_KEY_INTERACTIVE and data[0:1] == constants.EB_KEY_INTERACTIVE_REPETITION:
			log.debug(f"Ignoring routing key {data[1] - 1} repetition")
			return
		arg = bytesToInt(data)
		if arg == self.keysDown[group]:
			log.debug("Ignoring key repetition")
			return
		self.keysDown[group] |= arg
		isIris = self.deviceType.startswith("Iris")
		if not isIris and group == constants.EB_KEY_COMMAND and arg >= self.keysDown[group]:
			# Started a gesture including command keys
			self._ignoreCommandKeyReleases = False
		else:
			if isIris or group != constants.EB_KEY_COMMAND or not self._ignoreCommandKeyReleases:
				try:
					inputCore.manager.executeGesture(gestures.InputGesture(self))
				except inputCore.NoInputGestureAction:
					pass
				self._ignoreCommandKeyReleases = not isIris and (
					group == constants.EB_KEY_COMMAND or self.keysDown[constants.EB_KEY_COMMAND] > 0
				)  # noqa E501
			if not isIris and group == constants.EB_KEY_COMMAND:
				self.keysDown[group] = arg
			else:
				del self.keysDown[group]

	def _sendPacket(self, packetType: bytes, packetSubType: bytes, packetData: bytes = b""):
		packetSize = len(packetData) + 4
		packetBytes = bytearray(
			b"".join(
				[
					constants.STX,
					packetSize.to_bytes(2, "big", signed=False),
					packetType,
					packetSubType,
					packetData,
					constants.ETX,
				],
			),
		)
		if self.receivesAckPackets:
			with self._frameLock:
				frame = self._frame
				# Assumption: frame will only ever be 1 byte, otherwise consider byte order
				packetBytes.insert(-1, frame)
				self._awaitingFrameReceipts[frame] = packetBytes
				self._frame = frame + 1 if frame < 0x7F else 0x20
		packetData = bytes(packetBytes)
		if self.isHid:
			self._sendHidPacket(packetData)
		else:
			self._dev.write(packetData)

	def _sendHidPacket(self, packet: bytes):
		assert self.isHid
		blockSize = self._dev._writeSize - 1
		# When the packet length exceeds C{blockSize}, the packet is split up into several block packets.
		# These blocks are of size C{blockSize}.
		for offset in range(0, len(packet), blockSize):
			bytesToWrite = packet[offset : (offset + blockSize)]
			hidPacket = b"".join(
				[
					b"\x00",
					bytesToWrite,
					b"\x55" * (blockSize - len(bytesToWrite)),  # padding
				],
			)
			self._dev.write(hidPacket)

	def display(self, cells: List[int]):
		# cells will already be padded up to numCells.
		self._sendPacket(
			packetType=constants.EB_BRAILLE_DISPLAY,
			packetSubType=constants.EB_BRAILLE_DISPLAY_STATIC,
			packetData=bytes(cells),
		)

	def _get_hidKeyboardInput(self):
		return self._hidKeyboardInput

	def _set_hidKeyboardInput(self, state: bool):
		self._sendPacket(
			packetType=constants.EB_KEY,
			packetSubType=constants.EB_KEY_USB_HID_MODE,
			packetData=constants.EB_TRUE if state else constants.EB_FALSE,
		)
		for i in range(3):
			self._dev.waitForRead(self.timeout)
			if state is self._hidKeyboardInput:
				break

	scriptCategory = SCRCAT_BRAILLE

	def script_toggleHidKeyboardInput(self, gesture: inputCore.InputGesture):
		def announceUnavailableMessage():
			# Translators: Message when HID keyboard simulation is unavailable.
			ui.message(_("HID keyboard input simulation is unavailable."))

		if not self.isHid:
			announceUnavailableMessage()
			return

		state = not self.hidKeyboardInput
		self.hidKeyboardInput = state

		if state is not self._hidKeyboardInput:
			announceUnavailableMessage()
		elif state:
			# Translators: Message when HID keyboard simulation is enabled.
			ui.message(_("HID keyboard simulation enabled"))
		else:
			# Translators: Message when HID keyboard simulation is disabled.
			ui.message(_("HID keyboard simulation disabled"))

	# Translators: Description of the script that toggles HID keyboard simulation.
	script_toggleHidKeyboardInput.__doc__ = _("Toggle HID keyboard simulation")

	__gestures = {
		"br(eurobraille.esytime):l1+joystick1Down": "toggleHidKeyboardInput",
		"br(eurobraille):switch1Left+joystick1Down": "toggleHidKeyboardInput",
		"br(eurobraille.esytime):l8+joystick1Down": "toggleHidKeyboardInput",
		"br(eurobraille):switch1Right+joystick1Down": "toggleHidKeyboardInput",
	}
	gestureMap = gestures._gestureMap
