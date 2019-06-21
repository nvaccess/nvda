# -*- coding: UTF-8 -*-
#brailleDisplayDrivers/esys.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017-2019 NV Access Limited, Babbage B.V., Eurobraille

from collections import OrderedDict, defaultdict
from typing import Dict, Any, List, Union

from io import BytesIO
import serial
import bdDetect
import braille
import inputCore
from logHandler import log
import brailleInput
import hwIo
from hwIo import intToByte, boolToByte
from baseObject import AutoPropertyObject, ScriptableObject
import wx
import threading
from globalCommands import SCRCAT_BRAILLE
import ui
import time

BAUD_RATE = 9600

STX = b'\x02'
ETX = b'\x03'
ACK = b'\x06'
EB_SYSTEM = b'S' # 0x53
EB_MODE = b'R' # 0x52
EB_KEY = b'K' # 0x4b
EB_BRAILLE_DISPLAY = b'B' # 0x42
EB_KEY_INTERACTIVE = b'I' # 0x49
EB_KEY_INTERACTIVE_SINGLE_CLICK = b'\x01'
EB_KEY_INTERACTIVE_REPETITION = b'\x02'
EB_KEY_INTERACTIVE_DOUBLE_CLICK = b'\x03'
EB_KEY_BRAILLE=b'B' # 0x42
EB_KEY_COMMAND = b'C' # 0x43
EB_KEY_QWERTY = b'Z' # 0x5a
EB_KEY_USB_HID_MODE = b'U' # 0x55
EB_BRAILLE_DISPLAY_STATIC = b'S' # 0x53
EB_SYSTEM_IDENTITY = b'I' # 0x49
EB_SYSTEM_DISPLAY_LENGTH = b'G' # 0x47
EB_SYSTEM_TYPE = b'T' # 0x54
EB_SYSTEM_PROTOCOL = b'P' #0x50
EB_SYSTEM_FRAME_LENGTH = b'M' # 0x4d
EB_ENCRYPTION_KEY = b'Z' # 0x5a
EB_MODE_DRIVER = b'P' # 0x50
EB_MODE_INTERNAL = b'I' # 0x49
EB_MODE_MENU = b'M' # 0x4d
EB_IRIS_TEST = b'T' # 0x54
EB_IRIS_TEST_sub = b'L' # 0x4c
EB_VISU = b'V' # 0x56
EB_VISU_DOT = b'D' # 0x44

# The eurobraille protocol uses real number characters as boolean values, so 0 (0x30) and 1 (0x31)
EB_FALSE = b'0' # 0x30
EB_TRUE = b'1' # 0x31

KEYS_STICK = OrderedDict({
	0x10000: "joystick1Up",
	0x20000: "joystick1Down",
	0x40000: "joystick1Right",
	0x80000: "joystick1Left",
	0x100000: "joystick1Center",    
	0x1000000: "joystick2Up",
	0x2000000: "joystick2Down",
	0x4000000: "joystick2Right",
	0x8000000: "joystick2Left",
	0x10000000: "joystick2Center"
})
KEYS_ESYS = OrderedDict({
	0x01: "switch1Right",
	0x02: "switch1Left",
	0x04: "switch2Right",
	0x08: "switch2Left",
	0x10: "switch3Right",
	0x20: "switch3Left",
	0x40: "switch4Right",
	0x80: "switch4Left",
	0x100: "switch5Right",
	0x200: "switch5Left",
	0x400: "switch6Right",
	0x800: "switch6Left",
})
KEYS_ESYS.update(KEYS_STICK)
KEYS_IRIS = OrderedDict({
	0x01: "l1",
	0x02: "l2",
	0x04: "l3",
	0x08: "l4",
	0x10: "l5",
	0x20: "l6",
	0x40: "l7",
	0x80: "l8",
	0x100: "upArrow",
	0x200: "downArrow",
	0x400: "rightArrow",
	0x800: "leftArrow",
})

KEYS_ESITIME = OrderedDict({
	0x01: "l1",
	0x02: "l2",
	0x04: "l3",
	0x08: "l4",
	0x10: "l5",
	0x20: "l6",
	0x40: "l7",
	0x80: "l8",
})
KEYS_ESITIME.update(KEYS_STICK)

DEVICE_TYPES={
	0x01:"Iris 20",
	0x02:"Iris 40",
	0x03:"Iris S20",
	0x04:"Iris S32",
	0x05:"Iris KB20",
	0x06:"IrisKB 40",
	0x07:"Esys 12",
	0x08:"Esys 40",
	0x09:"Esys Light 40",
	0x0a:"Esys 24",
	0x0b:"Esys 64",
	0x0c:"Esys 80",
	#0x0d:"Esys", # reserved in protocol
	0x0e:"Esytime 32",
	0x0f:"Esytime 32 standard",
	0x10:"Esytime evo 32",
	0x11:"Esytime evo 32 standard",
}


def bytesToInt(byteData: bytes):
	"""Converts bytes to its integral equivalent."""
	return int.from_bytes(byteData, byteorder="big", signed=False)


class BrailleDisplayDriver(braille.BrailleDisplayDriver, ScriptableObject):
	_dev: hwIo.IoBase
	# Used to for error checking.
	_awaitingFrameReceipts: Dict[int, Any]
	name = "eurobraille"
	# Translators: Names of braille displays.
	description = _("Eurobraille Esys/Esytime/Iris displays")
	isThreadSafe = True
	timeout = 0.2
	supportedSettings = (
		braille.BrailleDisplayDriver.HIDInputSetting(useConfig=True),
	)

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	def __init__(self, port="Auto"):
		super(BrailleDisplayDriver, self).__init__()
		self.numCells = 0
		self.deviceType = None
		self._deviceData = {}
		self._awaitingFrameReceipts  = {}
		self._frameLength = None
		self._frame = 0x20
		self._frameLock = threading.Lock()
		self._hidKeyboardInput = False
		self._hidInputBuffer = b""

		for portType, portId, port, portInfo in self._getTryPorts(port):
			# At this point, a port bound to this display has been found.
			# Try talking to the display.
			self.isHid = portType == bdDetect.KEY_HID
			try:
				if self.isHid:
					self._dev = hwIo.Hid(
						port,
						onReceive=self._onReceive,
						# Eurobraille wants us not to block other application's access to this handle.
						exclusive=False
					)
				else:
					self._dev = hwIo.Serial(
						port,
						baudrate=BAUD_RATE,
						bytesize=serial.EIGHTBITS,
						parity=serial.PARITY_EVEN,
						stopbits=serial.STOPBITS_ONE,
						timeout=self.timeout,
						writeTimeout=self.timeout,
						onReceive=self._onReceive
					)
			except EnvironmentError:
				log.debugWarning("Error while connecting to port %r"%port, exc_info=True)
				continue

			for i in range(3):
				# Request device identification
				self._sendPacket(EB_SYSTEM, EB_SYSTEM_IDENTITY)
				# Make sure visualisation packets are disabled, as we ignore them anyway.
				self._sendPacket(EB_VISU, EB_VISU_DOT, EB_FALSE)
				# A device identification results in multiple packets.
				# Make sure we've received everything before we continue
				while self._dev.waitForRead(self.timeout*2):
					continue
				if self.numCells and self.deviceType:
					break
			if self.numCells and self.deviceType:
				# A display responded.
				log.info("Found {device} connected via {type} ({port})".format(
					device=self.deviceType, type=portType, port=port))
				break
			self._dev.close()

		else:
			raise RuntimeError("No supported Eurobraille display found")

		self.keysDown = defaultdict(int)
		self._ignoreCommandKeyReleases = False

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
		finally:
			# We must sleep before closing the port as not doing this can leave the display in a bad state where it can not be re-initialized.
			time.sleep(self.timeout)
			self._dev.close()
			self._dev = None
			self._deviceData.clear()

	def _prepFirstByteStreamAndData(
			self,
			data: bytes
	) -> (bytes, Union[BytesIO, hwIo.IoBase], bytes):
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

		if byte1 == ACK:
			frame = ord(stream.read(1))
			self._handleAck(frame)
		elif byte1 == STX:
			length = bytesToInt(stream.read(2)) - 2  # length includes the length itself
			packet: bytes = stream.read(length)
			if self.isHid and not stream.read(1) == ETX:
				# Incomplete packet
				self._hidInputbuffer = data
				return
			packetType: bytes = packet[0:1]
			packetSubType: bytes = packet[1:2]
			packetData: bytes = packet[2:] if length > 2 else b""
			if packetType == EB_SYSTEM:
				self._handleSystemPacket(packetSubType, packetData)
			elif packetType == EB_MODE:
				if packetSubType == EB_MODE_DRIVER:
					log.debug("Braille display switched to driver mode, updating display...")
					braille.handler.update()
				elif packetSubType == EB_MODE_INTERNAL:
					log.debug("Braille display switched to internal mode")
			elif packetType == EB_KEY:
				self._handleKeyPacket(packetSubType, packetData)
			elif packetType == EB_IRIS_TEST and packetSubType == EB_IRIS_TEST_sub:
				# Ping command sent by Iris every two seconds, send it back on the main thread.
				# This means that, if the main thread is frozen, Iris will be notified of this.
				log.debug("Received ping from Iris braille display")
				wx.CallAfter(self._sendPacket, packetType, packetSubType, packetData)
			elif packetType == EB_VISU:
				log.debug("Ignoring visualisation packet")
			elif packetType == EB_ENCRYPTION_KEY:
				log.debug("Ignoring encryption key packet")
			else:
				log.debug("Ignoring packet: type %r, subtype %r, data %r"%(
					packetType,
					packetSubType,
					packetData
				))

	def _handleAck(self, frame: int):
		try:
			super(BrailleDisplayDriver, self)._handleAck()
		except NotImplementedError:
			log.debugWarning("Received ACK for frame %d while ACK handling is disabled"%frame)
		else:
			try:
				del self._awaitingFrameReceipts[frame]
			except KeyError:
				log.debugWarning("Received ACK for unregistered frame %d"%frame)

	def _handleSystemPacket(self, packetType: bytes, data: bytes):
		if packetType == EB_SYSTEM_TYPE:
			deviceType = ord(data)
			self.deviceType = DEVICE_TYPES[deviceType]
			if 0x01 <= deviceType <= 0x06:  # Iris
				self.keys = KEYS_IRIS
			elif 0x07 <= deviceType <= 0x0d:  # Esys
				self.keys = KEYS_ESYS
			elif 0x0e <= deviceType <= 0x11:  # Esitime
				self.keys = KEYS_ESITIME
			else:
				log.debugWarning("Unknown device identifier %r"%data)
		elif packetType == EB_SYSTEM_DISPLAY_LENGTH:
			self.numCells = ord(data)
		elif packetType == EB_SYSTEM_FRAME_LENGTH:
			self._frameLength = bytesToInt(data)
		elif packetType == EB_SYSTEM_PROTOCOL and self.isHid:
			protocol = data.rstrip(b"\x00 ")
			try:
				version = float(protocol[:4])
			except ValueError:
				pass
			else:
				self.receivesAckPackets = version >= 3.0
		elif packetType == EB_SYSTEM_IDENTITY:
			return  # End of system information
		self._deviceData[packetType] = data.rstrip(b"\x00 ")

	def _handleKeyPacket(self, group: bytes, data: bytes):
		if group == EB_KEY_USB_HID_MODE:
			assert data in [EB_TRUE, EB_FALSE]
			self._hidKeyboardInput = EB_TRUE == data
			return
		if group == EB_KEY_QWERTY:
			log.debug("Ignoring Iris AZERTY/QWERTY input")
			return
		if group == EB_KEY_INTERACTIVE and data[0:1] == EB_KEY_INTERACTIVE_REPETITION:
			log.debug("Ignoring routing key %d repetition" % (data[1] - 1))
			return
		arg = bytesToInt(data)
		if arg == self.keysDown[group]:
			log.debug("Ignoring key repetition")
			return
		self.keysDown[group] |= arg
		isIris = self.deviceType.startswith("Iris")
		if not isIris and group == EB_KEY_COMMAND and arg >= self.keysDown[group]:
			# Started a gesture including command keys
			self._ignoreCommandKeyReleases = False
		else:
			if isIris or group != EB_KEY_COMMAND or not self._ignoreCommandKeyReleases:
				try:
					inputCore.manager.executeGesture(InputGesture(self))
				except inputCore.NoInputGestureAction:
					pass
				self._ignoreCommandKeyReleases = not isIris and (group == EB_KEY_COMMAND or self.keysDown[EB_KEY_COMMAND] > 0)
			if not isIris and group == EB_KEY_COMMAND:
				self.keysDown[group] = arg
			else:
				del self.keysDown[group]

	def _sendPacket(self, packetType: bytes, packetSubType: bytes, packetData: bytes = b""):
		packetSize = len(packetData)+4
		packetBytes = bytearray(
			b"".join([
				STX,
				packetSize.to_bytes(2, "big", signed=False),
				packetType,
				packetSubType,
				packetData,
				ETX
		]))
		if self.receivesAckPackets:
			with self._frameLock:
				frame = self._frame
				# Assumption: frame will only ever be 1 byte, otherwise consider byte order
				packetBytes.insert(-1, frame)
				self._awaitingFrameReceipts[frame] = packetBytes
				self._frame = frame+1 if frame < 0x7F else 0x20
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
			bytesToWrite = packet[offset:(offset+blockSize)]
			hidPacket = b"".join([
				b"\x00",
				bytesToWrite,
				b"\x55" * (blockSize - len(bytesToWrite))  # padding
			])
			self._dev.write(hidPacket)

	def display(self, cells: List[int]):
		# cells will already be padded up to numCells.
		self._sendPacket(
			packetType=EB_BRAILLE_DISPLAY,
			packetSubType=EB_BRAILLE_DISPLAY_STATIC,
			packetData=bytes(cells)
		)

	def _get_hidKeyboardInput(self):
		return self._hidKeyboardInput

	def _set_hidKeyboardInput(self, state: bool):
		self._sendPacket(
			packetType=EB_KEY,
			packetSubType=EB_KEY_USB_HID_MODE,
			packetData=EB_TRUE if state else EB_FALSE
		)
		for i in range(3):
			self._dev.waitForRead(self.timeout)
			if state is self._hidKeyboardInput:
				break

	scriptCategory = SCRCAT_BRAILLE
	def script_toggleHidKeyboardInput(self, gesture):
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
			ui.message(_('HID keyboard simulation enabled'))
		else:
			# Translators: Message when HID keyboard simulation is disabled.
			ui.message(_('HID keyboard simulation disabled'))

	# Translators: Description of the script that toggles HID keyboard simulation.
	script_toggleHidKeyboardInput.__doc__ = _("Toggle HID keyboard simulation")

	__gestures = {
		"br(eurobraille.esytime):l1+joystick1Down": "toggleHidKeyboardInput",
		"br(eurobraille):switch1Left+joystick1Down": "toggleHidKeyboardInput",
		"br(eurobraille.esytime):l8+joystick1Down": "toggleHidKeyboardInput",
		"br(eurobraille):switch1Right+joystick1Down": "toggleHidKeyboardInput",
	}

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_routeTo": ("br(eurobraille):routing",),
			"braille_reportFormatting": ("br(eurobraille):doubleRouting",),
			"braille_scrollBack": (
				"br(eurobraille):switch1Left",
				"br(eurobraille):l1",
			),
			"braille_scrollForward": (
				"br(eurobraille):switch1Right",
				"br(eurobraille):l8",
			),
			"braille_toFocus": (
				"br(eurobraille):switch1Left+switch1Right", "br(eurobraille):switch2Left+switch2Right",
				"br(eurobraille):switch3Left+switch3Right", "br(eurobraille):switch4Left+switch4Right",
				"br(eurobraille):switch5Left+switch5Right", "br(eurobraille):switch6Left+switch6Right",
				"br(eurobraille):l1+l8", 
			),
			"review_previousLine": ("br(eurobraille):joystick1Up",),
			"review_nextLine": ("br(eurobraille):joystick1Down",),
			"review_previousCharacter": ("br(eurobraille):joystick1Left",),
			"review_nextCharacter": ("br(eurobraille):joystick1Right",),
			"reviewMode_previous": ("br(eurobraille):joystick1Left+joystick1Up",),
			"reviewMode_next": ("br(eurobraille):joystick1Right+joystick1Down",),
			# Esys and esytime have a dedicated key for backspace and combines backspace and space to perform a return.
			"braille_eraseLastCell": ("br(eurobraille):backSpace",),
			"braille_enter": ("br(eurobraille):backSpace+space",),
			"kb:insert": (
				"br(eurobraille):dot3+dot5+space",
				"br(eurobraille):l7",
			),
			"kb:delete": ("br(eurobraille):dot3+dot6+space",),
			"kb:home": ("br(eurobraille):dot1+dot2+dot3+space", "br(eurobraille):joystick2Left+joystick2Up",),
			"kb:end": ("br(eurobraille):dot4+dot5+dot6+space", "br(eurobraille):joystick2Right+joystick2Down",),
			"kb:leftArrow": (
				"br(eurobraille):dot2+space",
				"br(eurobraille):joystick2Left",
				"br(eurobraille):leftArrow",
			),
			"kb:rightArrow": (
				"br(eurobraille):dot5+space",
				"br(eurobraille):joystick2Right",
				"br(eurobraille):rightArrow",
			),
			"kb:upArrow": (
				"br(eurobraille):dot1+space",
				"br(eurobraille):joystick2Up",
				"br(eurobraille):upArrow",
			),
			"kb:downArrow": (
				"br(eurobraille):dot6+space",
				"br(eurobraille):joystick2Down",
				"br(eurobraille):downArrow",
			),
			"kb:enter": ("br(eurobraille):joystick2Center",),
			"kb:pageUp": ("br(eurobraille):dot1+dot3+space",),
			"kb:pageDown": ("br(eurobraille):dot4+dot6+space",),
			"kb:numpad1": ("br(eurobraille):dot1+dot6+backspace",),
			"kb:numpad2": ("br(eurobraille):dot1+dot2+dot6+backspace",),
			"kb:numpad3": ("br(eurobraille):dot1+dot4+dot6+backspace",),
			"kb:numpad4": ("br(eurobraille):dot1+dot4+dot5+dot6+backspace",),
			"kb:numpad5": ("br(eurobraille):dot1+dot5+dot6+backspace",),
			"kb:numpad6": ("br(eurobraille):dot1+dot2+dot4+dot6+backspace",),
			"kb:numpad7": ("br(eurobraille):dot1+dot2+dot4+dot5+dot6+backspace",),
			"kb:numpad8": ("br(eurobraille):dot1+dot2+dot5+dot6+backspace",),
			"kb:numpad9": ("br(eurobraille):dot2+dot4+dot6+backspace",),
			"kb:numpadInsert": ("br(eurobraille):dot3+dot4+dot5+dot6+backspace",),
			"kb:numpadDecimal": ("br(eurobraille):dot2+backspace",),
			"kb:numpadDivide": ("br(eurobraille):dot3+dot4+backspace",),
			"kb:numpadMultiply": ("br(eurobraille):dot3+dot5+backspace",),
			"kb:numpadMinus": ("br(eurobraille):dot3+dot6+backspace",),
			"kb:numpadPlus": ("br(eurobraille):dot2+dot3+dot5+backspace",),
			"kb:numpadEnter": ("br(eurobraille):dot3+dot4+dot5+backspace",),
			"kb:escape": (
				"br(eurobraille):dot1+dot2+dot4+dot5+space",
				"br(eurobraille):l2",
			),
			"kb:tab": (
				"br(eurobraille):dot2+dot5+dot6+space",
				"br(eurobraille):l3",
			),
			"kb:shift+tab": ("br(eurobraille):dot2+dot3+dot5+space",),
			"kb:printScreen": ("br(eurobraille):dot1+dot3+dot4+dot6+space",),
			"kb:pause": ("br(eurobraille):dot1+dot4+space",),
			"kb:applications": ("br(eurobraille):dot5+dot6+backspace",),
			"kb:f1": ("br(eurobraille):dot1+backspace",),
			"kb:f2": ("br(eurobraille):dot1+dot2+backspace",),
			"kb:f3": ("br(eurobraille):dot1+dot4+backspace",),
			"kb:f4": ("br(eurobraille):dot1+dot4+dot5+backspace",),
			"kb:f5": ("br(eurobraille):dot1+dot5+backspace",),
			"kb:f6": ("br(eurobraille):dot1+dot2+dot4+backspace",),
			"kb:f7": ("br(eurobraille):dot1+dot2+dot4+dot5+backspace",),
			"kb:f8": ("br(eurobraille):dot1+dot2+dot5+backspace",),
			"kb:f9": ("br(eurobraille):dot2+dot4+backspace",),
			"kb:f10": ("br(eurobraille):dot2+dot4+dot5+backspace",),
			"kb:f11": ("br(eurobraille):dot1+dot3+backspace",),
			"kb:f12": ("br(eurobraille):dot1+dot2+dot3+backspace",),
			"kb:windows": ("br(eurobraille):dot1+dot2+dot3+dot4+backspace",),
			"kb:capsLock": ("br(eurobraille):dot7+backspace", "br(eurobraille):dot8+backspace",),
			"kb:numLock": ("br(eurobraille):dot3+backspace", "br(eurobraille):dot6+backspace",),
			"kb:shift": (
				"br(eurobraille):dot7+space",
				"br(eurobraille):l4",
			),
			"braille_toggleShift": ("br(eurobraille):dot1+dot7+space", "br(eurobraille):dot4+dot7+space",),
			"kb:control": (
				"br(eurobraille):dot7+dot8+space",
				"br(eurobraille):l5",
			),
			"braille_toggleControl": ("br(eurobraille):dot1+dot7+dot8+space", "br(eurobraille):dot4+dot7+dot8+space",),
			"kb:alt": (
				"br(eurobraille):dot8+space",
				"br(eurobraille):l6",
			),
			"braille_toggleAlt": ("br(eurobraille):dot1+dot8+space", "br(eurobraille):dot4+dot8+space",),
		},
	})

class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, display):
		super(InputGesture, self).__init__()
		self.model = display.deviceType.lower().split(" ")[0]
		keysDown = dict(display.keysDown)
		self.keyNames = names = []
		for group, groupKeysDown in keysDown.items():
			if group == EB_KEY_BRAILLE:
				if sum(keysDown.values())==groupKeysDown and not groupKeysDown & 0x100:
					# This is braille input.
					# 0x1000 is backspace, 0x2000 is space
					self.dots = groupKeysDown & 0xff
					self.space = groupKeysDown & 0x200
				names.extend("dot%d" % (i+1) for i in range(8) if (groupKeysDown &0xff) & (1 << i))
				if groupKeysDown & 0x200:
					names.append("space")
				if groupKeysDown & 0x100:
					names.append("backSpace")
			if group == EB_KEY_INTERACTIVE: # Routing
				self.routingIndex = (groupKeysDown & 0xff)-1
				names.append("doubleRouting" if groupKeysDown>>8 ==ord(EB_KEY_INTERACTIVE_DOUBLE_CLICK) else "routing")
			if group == EB_KEY_COMMAND:
				for key, keyName in display.keys.items():
					if groupKeysDown & key:
						# This key is pressed
						names.append(keyName)

		self.id = "+".join(names)
