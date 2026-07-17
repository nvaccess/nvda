# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Bram Duvigneau, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Braille display driver for Freedom Scientific braille displays.
A c(lang) reference implementation is available in brltty.
"""

import itertools
from io import BytesIO

import bdDetect
import braille
import braille.display.driver
import braille.display.gesture
import brailleInput
import hwIo
import inputCore
import serial
from baseObject import ScriptableObject
from hwIo import intToByte
from logHandler import log
from utils._deprecate import MovedSymbol, handleDeprecations

__getattr__ = handleDeprecations(
	MovedSymbol("RoutingGesture", "brailleDisplayDrivers.freedomScientific", "KeyGesture"),
)
"""Module level `__getattr__` used to preserve backward compatibility."""


BAUD_RATE = 57600
PARITY = serial.PARITY_NONE

#: Model names and number of cells
MODELS = {
	"Focus 14": 14,
	"Focus 40": 40,
	"Focus 44": 44,
	"Focus 70": 70,
	"Focus 80": 80,
	"Focus 84": 84,
	"pm display 20": 20,
	"pm display 40": 40,
}

#: Number of cells of Focus first generation displays
#  The assumption is that any displays with the following cell counts are due to three cells at the
#  beginning/end of the display are used as status cells, and an extra blank cell to separate status
#  from normal cells. These devices require a special translation table: :data:`FOCUS_1_TRANSLATION_TABLE`
#  This line of displays is known as the first generation Focus displays.
FOCUS_1_CELL_COUNTS = (44, 70, 84)

# Packet types
#: Query the display for information such as manufacturer, model and firmware version
FS_PKT_QUERY = b"\x00"
#: Response from the display that acknowledges a packet has been received
FS_PKT_ACK = b"\x01"
#: Negative response from the display indicating a problem
FS_PKT_NAK = b"\x02"
#: The display indicates that one ore more keys on the display are pressed/released. This includes normal buttons and the braille keyboard
FS_PKT_KEY = b"\x03"
#: A routing button on the display is pressed/released
FS_PKT_BUTTON = b"\x04"
#: Indicates a whiz wheel has turned. Please note that on newer models the wheels have been replaced by buttons, but there is no difference in the protocol.
FS_PKT_WHEEL = b"\x05"
#: Set braille dot firmness. Not yet used in this driver.
FS_PKT_HVADJ = b"\x08"
#: Lets the display beep. Not yet used in this driver.
FS_PKT_BEEP = b"\x09"
#: Sends a configuration request to the display. Mainly used to enable extended key mode on newer displays to use all the buttons.
FS_PKT_CONFIG = b"\x0f"
#: Indicates a response to FS_PKT_QUERY from the display
FS_PKT_INFO = b"\x80"
#: Sends braille cells to the display.
FS_PKT_WRITE = b"\x81"
#: Indicates extended keys have been pressed. Newer displays use this for some of their keys, see also the list in KeyGesture.extendedKeyLabels
FS_PKT_EXT_KEY = b"\x82"

# Parts of packets
#: An empty packet argument or null byte
FS_BYTE_NULL = b"\x00"
#: Empty data in the packet payload
FS_DATA_EMPTY = b""
#: Send extended key events, to be used with the FS_PKT_CONFIG
FS_CFG_EXTKEY = b"\x02"

# FS_PKT_INFO payload offsets
#: Start position of manufacturer in FS_PKT_INFO payload
INFO_MANU_START = 0
#: End position of manufacturer in FS_PKT_INFO payload
INFO_MANU_END = 24
#: Start position of model in FS_PKT_INFO payload
INFO_MODEL_START = INFO_MANU_END
#: End position of model in FS_PKT_INFO payload
INFO_MODEL_END = INFO_MODEL_START + 16
#: Start position of firmware version in FS_PKT_INFO payload
INFO_VERSION_START = INFO_MODEL_END
#: End position of firmware version in FS_PKT_INFO payload
INFO_VERSION_END = INFO_MODEL_END + 8

# Braille translation
#: The number of dots in a braille character/cell
DOTS_TABLE_SIZE = 8
#: THe size of a full braille translation table including all possible dot combinations
TRANSLATION_TABLE_SIZE = 2**DOTS_TABLE_SIZE


def _makeTranslationTable(dotsTable: list[int]) -> list[int]:
	"""Create a translation table for braille dot combinations

	:param dotsTable: The list of 8 bitmasks to use for each dot (dot 1 - 8)
	"""

	def isoDot(number: int) -> int:
		"""
		Returns the ISO 11548 formatted braille dot for the given number.

		From least- to most-significant octal digit:

		* the first contains dots 1-3
		* the second contains dots 4-6
		* the third contains dots 7-8

		Based on: https://github.com/brltty/brltty/blob/master/Headers/brl_dots.h

		:param number: The dot to encode (1-8)
		"""
		return 1 << (number - 1)

	outputTable = [0] * TRANSLATION_TABLE_SIZE
	for byte in range(TRANSLATION_TABLE_SIZE):
		cell = 0
		for dot in range(DOTS_TABLE_SIZE):
			if byte & isoDot(dot + 1):
				cell |= dotsTable[dot]
		outputTable[byte] = cell
	return outputTable


def _translate(cells: list[int], translationTable: list[int]) -> list[int]:
	"""Translate cells according to a translation table

	The translation table contains the bytes to encode all the possible dot combinations.
	See :meth:`_makeTranslationTable` as well.

	:param cells: The cells to translate, given in ISO 11548 format (used by most braille displays)
	:param translationTable: A list of all possible braille dot combinations
	"""
	return [translationTable[cell] for cell in cells]


#: Dots table used by first generation Focus displays
FOCUS_1_DOTS_TABLE = [
	0x01,
	0x02,
	0x04,
	0x10,
	0x20,
	0x40,
	0x08,
	0x80,
]

#: Braille translation table used by first generation Focus displays
FOCUS_1_TRANSLATION_TABLE = _makeTranslationTable(FOCUS_1_DOTS_TABLE)


class BrailleDisplayDriver(braille.display.driver.BrailleDisplayDriver, ScriptableObject):
	"""
	Driver for Freedom Scientific braille displays
	"""

	name = "freedomScientific"
	# Translators: Names of braille displays.
	description = _("Freedom Scientific Focus/PAC Mate series")
	isThreadSafe = True
	supportsAutomaticDetection = True
	receivesAckPackets = True
	timeout = 0.2

	wizWheelActions = [
		(
			# Translators: The name of a key on a braille display, that scrolls the display
			# to show previous/next part of a long line.
			_("display scroll"),
			("globalCommands", "GlobalCommands", "braille_scrollBack"),
			("globalCommands", "GlobalCommands", "braille_scrollForward"),
		),
		(
			# Translators: The name of a key on a braille display,
			# that scrolls the display to show the next/previous line.
			_("line scroll"),
			("globalCommands", "GlobalCommands", "braille_previousLine"),
			("globalCommands", "GlobalCommands", "braille_nextLine"),
		),
	]

	@classmethod
	def registerAutomaticDetection(cls, driverRegistrar: bdDetect.DriverRegistrar) -> None:
		driverRegistrar.addUsbDevices(
			bdDetect.ProtocolType.CUSTOM,
			{
				"VID_0F4E&PID_0100",  # Focus 1
				"VID_0F4E&PID_0111",  # PAC Mate
				"VID_0F4E&PID_0112",  # Focus 2
				"VID_0F4E&PID_0114",  # Focus Blue
			},
		)

		driverRegistrar.addBluetoothDevices(
			lambda m: any(
				m.id.startswith(prefix)
				for prefix in (
					"F14",
					"Focus 14 BT",
					"Focus 40 BT",
					"Focus 80 BT",
				)
			),
		)

	def __init__(self, port: str | bdDetect.DeviceMatch = "auto"):
		self.numCells = 0
		self._ackPending = False
		self._pendingCells = []
		self._keyBits = 0
		self._extendedKeyBits = 0
		self._routingKeyBits = 0
		self._topRoutingKeyBits = 0
		self._ignoreKeyReleases = False
		self._model: str | None = None
		self._manufacturer: str | None = None
		self._firmwareVersion: str | None = None
		self.translationTable = None
		self.leftWizWheelActionCycle = itertools.cycle(self.wizWheelActions)
		action = next(self.leftWizWheelActionCycle)
		self.gestureMap.add("br(freedomScientific):leftWizWheelUp", *action[1])
		self.gestureMap.add("br(freedomScientific):leftWizWheelDown", *action[2])
		self.rightWizWheelActionCycle = itertools.cycle(self.wizWheelActions)
		action = next(self.rightWizWheelActionCycle)
		self.gestureMap.add("br(freedomScientific):rightWizWheelUp", *action[1])
		self.gestureMap.add("br(freedomScientific):rightWizWheelDown", *action[2])
		super().__init__()
		for portType, portId, port, portInfo in self._getTryPorts(port):
			self.isUsb = portType == bdDetect.ProtocolType.CUSTOM
			# Try talking to the display.
			try:
				if self.isUsb:
					self._dev = hwIo.Bulk(
						port,
						epIn=1,
						epOut=0,
						onReceive=self._onReceive,
						onReceiveSize=56,
						onReadError=self._handleReadError,
					)
				else:
					self._dev = hwIo.Serial(
						port,
						baudrate=BAUD_RATE,
						parity=PARITY,
						timeout=self.timeout,
						writeTimeout=self.timeout,
						onReceive=self._onReceive,
					)
			except OSError:
				log.debugWarning("", exc_info=True)
				continue

			# Send an identification request
			self._sendPacket(FS_PKT_QUERY)
			for _i in range(3):
				self._dev.waitForRead(self.timeout)
				if self.numCells and self._model:
					break

			if self.numCells and self._model:
				# A display responded.
				log.info(
					f"Found {self._model} connected via {portType} ({port})",
				)
				break
			self._dev.close()

		else:
			raise RuntimeError("No Freedom Scientific display found")

		self._configureDisplay()
		self.gestureMap.add(
			"br(freedomScientific):topRouting1",
			"globalCommands",
			"GlobalCommands",
			"braille_scrollBack",
		)
		self.gestureMap.add(
			f"br(freedomScientific):topRouting{self.numCells}",
			"globalCommands",
			"GlobalCommands",
			"braille_scrollForward",
		)
		self._restarting = False

	def terminate(self) -> None:
		try:
			super().terminate()
		finally:
			# Make sure the device gets closed.
			# If it doesn't, we may not be able to re-open it later.
			self._dev.close()

	def _sendPacket(
		self,
		packetType: bytes,
		arg1: bytes = FS_BYTE_NULL,
		arg2: bytes = FS_BYTE_NULL,
		arg3: bytes = FS_BYTE_NULL,
		data: bytes = FS_DATA_EMPTY,
	) -> None:
		"""Send a packet to the display
		:param packetType: Type of packet (first byte), use one of the FS_PKT constants
		:param arg1: First argument (second byte of packet)
		:param arg2: Second argument (third byte of packet)
		:param arg3: Third argument (fourth byte of packet)
		:param data: Data to send if this is an extended packet, required checksum will
			be added automatically
		"""

		packet = b"".join([packetType, arg1, arg2, arg3, data])
		if data:
			checksum = BrailleDisplayDriver._calculateChecksum(packet)
			packet += intToByte(checksum)
		self._dev.write(packet)

	def _onReceive(self, data: bytes) -> None:
		"""Event handler when data from the display is received

		Formats a packet of four bytes in a packet type and three arguments.
		If the packet is known to have a payload, this is also fetched and the checksum is verified.
		The constructed packet is handed off to :meth:`_handlePacket`.
		"""
		if self.isUsb:
			data = BytesIO(data)
			packetType: bytes = data.read(1)
		else:
			packetType: bytes = data
			data = self._dev

		arg1: bytes = data.read(1)
		arg2: bytes = data.read(1)
		arg3: bytes = data.read(1)
		log.debug("Got packet of type %r with args: %r %r %r", packetType, arg1, arg2, arg3)
		# Info and extended key responses are the only packets with payload and checksum
		if packetType in (FS_PKT_INFO, FS_PKT_EXT_KEY):
			length: int = ord(arg1)
			payload: bytes = data.read(length)
			checksum: int = ord(data.read(1))
			calculatedChecksum = BrailleDisplayDriver._calculateChecksum(
				packetType + arg1 + arg2 + arg3 + payload,
			)
			assert calculatedChecksum == checksum, (
				f"Checksum mismatch, expected {calculatedChecksum} but got {checksum}"
			)
		else:
			payload = FS_DATA_EMPTY

		self._handlePacket(packetType, arg1, arg2, arg3, payload)

	def _handleReadError(self, error: int) -> bool:
		if error == 995:  # Broken I/O pipe, terminate and allow restart
			if not self._restarting:
				# Will not cause a data race since this driver runs on one thread
				self._restarting = True
				log.info("Freedom Scientific display implicitly disconnected by suspend, reinitializing")
				self.terminate()
				self.__init__()
			return True
		return False

	def _handlePacket(
		self,
		packetType: bytes,
		arg1: bytes,
		arg2: bytes,
		arg3: bytes,
		payload: bytes,
	) -> None:
		"""Handle a packet from the device.

		The following packet types are handled:

			* FS_PKT_ACK: See :meth:`_handleAck`
			* FS_PKT_NAK: Logged and handled as an ACK
			* FS_PKT_INFO: Manufacturer, model and firmware version are extracted and set as
				properties on the object. Cell count is determined based on :data:`MODELS`.
				* arg1: length of payload
				* payload: manufacturer, model, firmware version in a fixed width field string
			* FS_PKT_WHEEL: The corresponding :class:`WheelGesture`s are sent for the wheel events.
				* arg1: movement direction (up/down) and number of clicks moved
					Bits: BBBAAA (least significant)
					* A: (bits 1-3) number of clicks the wheel has moved
					* B: (bits 4-6) which wheel (left/right) and what direction (up/down)
			* FS_PKT_BUTTON: the corresponding :class:`KeyGesture` is sent
				* arg1: number of routing button
				* arg2: key press/release
				* arg3: if this is a button on the second row of routing buttons
			* FS_PKT_KEY: a key or button on the display is pressed/released (including the braille keyboard)
				* arg 1, 2, 3, 4:
					These bytes form the value indicating which of the 8 keys are pressed on the device.
					Key releases can be detected by comparing to the previous state, this work is done in :meth:`_handleKeys`.
			* FS_PKT_EXT_KEY: ??
				* payload: The 4 most significant bits from a single byte are used.
					More investigation is required.
		"""
		if packetType == FS_PKT_ACK:
			self._handleAck()
		elif packetType == FS_PKT_NAK:
			log.debugWarning("NAK received!")
			self._handleAck()
		elif packetType == FS_PKT_INFO:
			manuBytes = payload[INFO_MANU_START:INFO_MANU_END].replace(
				FS_BYTE_NULL,
				b"",
			)
			self._manufacturer = manuBytes.decode()
			modelBytes = payload[INFO_MODEL_START:INFO_MODEL_END].replace(
				FS_BYTE_NULL,
				b"",
			)
			self._model = modelBytes.decode()
			firmwareBytes = payload[INFO_VERSION_START:INFO_VERSION_END].replace(
				FS_BYTE_NULL,
				b"",
			)
			self._firmwareVersion = firmwareBytes.decode()
			self.numCells = MODELS.get(self._model, 0)
			if self.numCells in FOCUS_1_CELL_COUNTS:
				# Focus first gen: apply custom translation table
				self.translationTable = FOCUS_1_TRANSLATION_TABLE
			log.debug(
				"Device info: manufacturer: %s model: %s, version: %s",
				self._manufacturer,
				self._model,
				self._firmwareVersion,
			)
		elif packetType == FS_PKT_WHEEL:
			threeLeastSigBitsMask = 0x7
			count = ord(arg1) & threeLeastSigBitsMask
			wheelNumber = (ord(arg1) >> 3) & threeLeastSigBitsMask
			try:
				# There are only two wheels, one on the left, one on the right.
				# Either wheel could have moved up or down.
				isDown, isRight = [
					(False, False),
					(True, False),
					(True, True),
					(False, True),
				][wheelNumber]
			except IndexError:
				log.debugWarning("wheelNumber unknown")
				return
			for _i in range(count):
				self._executeGesture(WizWheelGesture(self._model, isDown, isRight))
		elif packetType == FS_PKT_BUTTON:
			key = ord(arg1)
			# the least significant bit is set when the key is pressed
			leastSigBitMask = 0x01
			isPress = bool(ord(arg2) & leastSigBitMask)
			isTopRow = bool(ord(arg3))
			self._handleRoutingKey(key, isPress, isTopRow)
		elif packetType == FS_PKT_KEY:
			keyBits = ord(arg1) | (ord(arg2) << 8) | (ord(arg3) << 16)
			self._handleKeys(keyBits)
		elif packetType == FS_PKT_EXT_KEY:
			keyBits = payload[0] >> 4
			self._handleExtendedKeys(keyBits)
		else:
			log.debugWarning("Unknown packet of type: %r", packetType)

	@staticmethod
	def _executeGesture(gesture: "InputGesture") -> None:
		"""Execute a gesture, ignoring it if no action is mapped."""
		try:
			inputCore.manager.executeGesture(gesture)
		except inputCore.NoInputGestureAction:
			pass

	def _handleAck(self) -> None:
		"Displays any queued cells after receiving an ACK"
		super()._handleAck()
		if self._pendingCells:
			self.display(self._pendingCells)

	@staticmethod
	def _updateKeyBits(keyBits: int, oldKeyBits: int, keyCount: int) -> tuple[int, bool, int, bool]:
		"""Helper function that reports if keys have been pressed and which keys have been released
		based on old and new keybits.
		"""
		isRelease = False
		keyBitsBeforeRelease = 0
		newKeysPressed = False
		keyBit = 0x1
		keyBits |= oldKeyBits & ~((0x1 << keyCount) - 1)
		while oldKeyBits != keyBits:
			oldKey = oldKeyBits & keyBit
			newKey = keyBits & keyBit

			if oldKey and not newKey:
				# A key has been released
				isRelease = True
				if not keyBitsBeforeRelease:
					keyBitsBeforeRelease = oldKeyBits
				oldKeyBits &= ~keyBit
			elif newKey and not oldKey:
				oldKeyBits |= keyBit
				newKeysPressed = True

			keyBit <<= 1
		return oldKeyBits, isRelease, keyBitsBeforeRelease, newKeysPressed

	def _handleKeys(self, keyBits: int) -> None:
		"""Send gestures if keys are released and update self._keyBits"""
		keyBits, isRelease, keyBitsBeforeRelease, newKeysPressed = self._updateKeyBits(
			keyBits,
			self._keyBits,
			24,
		)
		if newKeysPressed:
			self._ignoreKeyReleases = False
		self._keyBits = keyBits
		if isRelease and not self._ignoreKeyReleases:
			self._executeGesture(
				KeyGesture(
					self._model,
					keyBitsBeforeRelease,
					self._extendedKeyBits,
					self._routingKeyBits,
					self._topRoutingKeyBits,
				),
			)
			self._ignoreKeyReleases = True

	def _handleExtendedKeys(self, keyBits: int) -> None:
		"""Send gestures if keys are released and update self._extendedKeyBits"""
		keyBits, isRelease, keyBitsBeforeRelease, newKeysPressed = self._updateKeyBits(
			keyBits,
			self._extendedKeyBits,
			24,
		)
		if newKeysPressed:
			self._ignoreKeyReleases = False
		self._extendedKeyBits = keyBits
		if isRelease and not self._ignoreKeyReleases:
			self._executeGesture(
				KeyGesture(
					self._model,
					self._keyBits,
					keyBitsBeforeRelease,
					self._routingKeyBits,
					self._topRoutingKeyBits,
				),
			)
			self._ignoreKeyReleases = True

	def _handleRoutingKey(self, key: int, isPress: bool, isTopRow: bool) -> None:
		"""Track routing key presses and fire a gesture on the first release."""
		keyMask = 1 << key
		if isPress:
			if isTopRow:
				self._topRoutingKeyBits |= keyMask
			else:
				self._routingKeyBits |= keyMask
			self._ignoreKeyReleases = False
			return
		# On release: fire gesture while key is still tracked as pressed, then clear bit.
		# Guard against stray release with no preceding press.
		currentBits = self._topRoutingKeyBits if isTopRow else self._routingKeyBits
		if currentBits & keyMask and not self._ignoreKeyReleases:
			self._executeGesture(
				KeyGesture(
					self._model,
					self._keyBits,
					self._extendedKeyBits,
					self._routingKeyBits,
					self._topRoutingKeyBits,
				),
			)
			self._ignoreKeyReleases = True
		if isTopRow:
			self._topRoutingKeyBits &= ~keyMask
		else:
			self._routingKeyBits &= ~keyMask

	@staticmethod
	def _calculateChecksum(data: bytes) -> int:
		"""Calculate the checksum for extended packets"""
		return (-sum(data)) & 0xFF

	def display(self, cells: list[int]) -> None:
		if self.translationTable:
			cells = _translate(cells, FOCUS_1_TRANSLATION_TABLE)
		if not self._awaitingAck:
			self._sendPacket(
				FS_PKT_WRITE,
				intToByte(self.numCells),
				FS_BYTE_NULL,
				FS_BYTE_NULL,
				bytes(cells),
			)
			self._pendingCells = []
		else:
			self._pendingCells = cells

	def _configureDisplay(self) -> None:
		"""Enable extended keys on Focus firmware 3 and up"""
		if not self._model or not self._firmwareVersion:
			return
		if self._model.startswith("Focus") and ord(self._firmwareVersion[0]) >= ord("3"):
			# Focus 2 or later. Make sure extended keys support is enabled.
			log.debug(
				"Activating extended keys on freedom Scientific display. Display name: %s, firmware version: %s.",
				self._model,
				self._firmwareVersion,
			)
			self._sendPacket(FS_PKT_CONFIG, FS_CFG_EXTKEY)

	def script_toggleLeftWizWheelAction(self, _gesture: inputCore.InputGesture) -> None:
		action = next(self.leftWizWheelActionCycle)
		self.gestureMap.add("br(freedomScientific):leftWizWheelUp", *action[1], replace=True)
		self.gestureMap.add("br(freedomScientific):leftWizWheelDown", *action[2], replace=True)
		braille.handler.message(action[0])

	def script_toggleRightWizWheelAction(self, _gesture: inputCore.InputGesture) -> None:
		action = next(self.rightWizWheelActionCycle)
		self.gestureMap.add("br(freedomScientific):rightWizWheelUp", *action[1], replace=True)
		self.gestureMap.add("br(freedomScientific):rightWizWheelDown", *action[2], replace=True)
		braille.handler.message(action[0])

	__gestures = {
		"br(freedomScientific):leftWizWheelPress": "toggleLeftWizWheelAction",
		"br(freedomScientific):rightWizWheelPress": "toggleRightWizWheelAction",
	}

	gestureMap = inputCore.GlobalGestureMap(
		{
			"globalCommands.GlobalCommands": {
				"braille_routeTo": ("br(freedomScientific):routing",),
				"braille_selectRange": ("br(freedomScientific):multiRouting",),
				"braille_scrollBack": (
					"br(freedomScientific):leftAdvanceBar",
					"br(freedomScientific):leftBumperBarUp",
					"br(freedomScientific):rightBumperBarUp",
				),
				"braille_scrollForward": (
					"br(freedomScientific):rightAdvanceBar",
					"br(freedomScientific):leftBumperBarDown",
					"br(freedomScientific):rightBumperBarDown",
				),
				"braille_previousLine": (
					"br(freedomScientific):leftRockerBarUp",
					"br(freedomScientific):rightRockerBarUp",
				),
				"braille_nextLine": (
					"br(freedomScientific):leftRockerBarDown",
					"br(freedomScientific):rightRockerBarDown",
				),
				"kb:shift+tab": ("br(freedomScientific):dot1+dot2+brailleSpaceBar",),
				"kb:tab": ("br(freedomScientific):dot4+dot5+brailleSpaceBar",),
				"kb:upArrow": ("br(freedomScientific):dot1+brailleSpaceBar",),
				"kb:downArrow": ("br(freedomScientific):dot4+brailleSpaceBar",),
				"kb:leftArrow": ("br(freedomScientific):dot3+brailleSpaceBar",),
				"kb:rightArrow": ("br(freedomScientific):dot6+brailleSpaceBar",),
				"kb:control+leftArrow": ("br(freedomScientific):dot2+brailleSpaceBar",),
				"kb:control+rightArrow": ("br(freedomScientific):dot5+brailleSpaceBar",),
				"kb:home": ("br(freedomScientific):dot1+dot3+brailleSpaceBar",),
				"kb:control+home": ("br(freedomScientific):dot1+dot2+dot3+brailleSpaceBar",),
				"kb:end": ("br(freedomScientific):dot4+dot6+brailleSpaceBar",),
				"kb:control+end": ("br(freedomScientific):dot4+dot5+dot6+brailleSpaceBar",),
				"kb:alt": ("br(freedomScientific):dot1+dot3+dot4+brailleSpaceBar",),
				"kb:alt+tab": ("br(freedomScientific):dot2+dot3+dot4+dot5+brailleSpaceBar",),
				"kb:alt+shift+tab": ("br(freedomScientific):dot1+dot2+dot5+dot6+brailleSpaceBar",),
				"kb:windows+tab": ("br(freedomScientific):dot2+dot3+dot4+brailleSpaceBar",),
				"kb:escape": ("br(freedomScientific):dot1+dot5+brailleSpaceBar",),
				"kb:windows": ("br(freedomScientific):dot2+dot4+dot5+dot6+brailleSpaceBar",),
				"kb:windows+d": ("br(freedomScientific):dot1+dot2+dot3+dot4+dot5+dot6+brailleSpaceBar",),
				"reportCurrentLine": ("br(freedomScientific):dot1+dot4+brailleSpaceBar",),
				"showGui": ("br(freedomScientific):dot1+dot3+dot4+dot5+brailleSpaceBar",),
				"braille_toggleTether": ("br(freedomScientific):leftGDFButton+rightGDFButton",),
				# Based on corresponding assignments in JAWS, modifing where Shift goes
				"braille_toggleControl": ("br(freedomscientific):dot3+dot8+brailleSpaceBar",),
				"braille_toggleAlt": ("br(freedomscientific):dot6+dot8+brailleSpaceBar",),
				"braille_toggleWindows": ("br(freedomscientific):dot4+dot8+brailleSpaceBar",),
				"braille_toggleNVDAKey": ("br(freedomscientific):dot5+dot8+brailleSpaceBar",),
				"braille_toggleShift": ("br(freedomscientific):dot7+dot8+brailleSpaceBar",),
				"braille_toggleControlShift": ("br(freedomscientific):dot3+dot7+dot8+brailleSpaceBar",),
				"braille_toggleAltShift": ("br(freedomscientific):dot6+dot7+dot8+brailleSpaceBar",),
				"braille_toggleWindowsShift": ("br(freedomscientific):dot4+dot7+dot8+brailleSpaceBar",),
				"braille_toggleNVDAKeyShift": ("br(freedomscientific):dot5+dot7+dot8+brailleSpaceBar",),
				"braille_toggleControlAlt": ("br(freedomscientific):dot3+dot6+dot8+brailleSpaceBar",),
				"braille_toggleControlAltShift": (
					"br(freedomscientific):dot3+dot6+dot7+dot8+brailleSpaceBar",
				),
			},
		},
	)


class InputGesture(braille.display.gesture.BrailleDisplayGesture):
	"""Base gesture for this braille display"""

	source = BrailleDisplayDriver.name

	def __init__(self, model: str) -> None:
		self.model = model.replace(" ", "")
		super().__init__()


class KeyGesture(InputGesture, brailleInput.BrailleInputGesture):
	"""Handle keys and braille input for Freedom Scientific braille displays"""

	keyLabels = [
		# Braille keys (byte 1)
		"dot1",
		"dot2",
		"dot3",
		"dot4",
		"dot5",
		"dot6",
		"dot7",
		"dot8",
		# Assorted keys (byte 2)
		"leftWizWheelPress",
		"rightWizWheelPress",
		"leftShiftKey",
		"rightShiftKey",
		"leftAdvanceBar",
		"rightAdvanceBar",
		None,
		"brailleSpaceBar",
		# GDF keys (byte 3)
		"leftGDFButton",
		"rightGDFButton",
		None,
		None,
		"leftBumperBarUp",
		"leftBumperBarDown",
		"rightBumperBarUp",
		"rightBumperBarDown",
	]
	extendedKeyLabels = [
		# Rocker bar keys.
		"leftRockerBarUp",
		"leftRockerBarDown",
		"rightRockerBarUp",
		"rightRockerBarDown",
	]

	@staticmethod
	def _bitmaskToIndexes(bitmask: int) -> list[int]:
		"""Return the ascending indexes of the set bits in `bitmask`."""
		return [i for i in range(bitmask.bit_length()) if (bitmask >> i) & 1]

	def __init__(
		self,
		model: str,
		keyBits: int,
		extendedKeyBits: int,
		routingKeyBits: int = 0,
		topRoutingKeyBits: int = 0,
	) -> None:
		super().__init__(model)
		keys = [self.keyLabels[num] for num in range(24) if (keyBits >> num) & 1]
		extendedKeys = [self.extendedKeyLabels[num] for num in range(4) if (extendedKeyBits >> num) & 1]
		idParts = keys + extendedKeys
		# Merge the cells addressed by every routing range into a single cellIndexes list,
		# mirroring other multi-range drivers (e.g. ALVA, Standard HID Braille).
		# Each pressed range contributes its own id part via idForCellCount.
		cellIndexes: list[int] = []
		for rangeName, rangeBits in (("routing", routingKeyBits), ("topRouting", topRoutingKeyBits)):
			if not rangeBits:
				continue
			rangeIndexes = self._bitmaskToIndexes(rangeBits)
			cellIndexes.extend(rangeIndexes)
			idParts.append(self.idForCellCount(len(rangeIndexes), rangeName))
		if cellIndexes:
			self.cellIndexes = cellIndexes
		self.id = "+".join(idParts)
		# Don't say is this a dots gesture if some keys either from dots and space are pressed.
		if not extendedKeyBits and not keyBits & ~(0xFF | (1 << 0xF)):
			self.dots = keyBits & 0xFF
			# Is space?
			if keyBits & (1 << 0xF):
				self.space = True


class WizWheelGesture(InputGesture):
	"""Gesture to handle wiz wheels movements"""

	def __init__(self, model: str, isDown: bool, isRight: bool) -> None:
		which = "right" if isRight else "left"
		direction = "Down" if isDown else "Up"
		self.id = f"{which}WizWheel{direction}"
		super().__init__(model)
