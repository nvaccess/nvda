#brailleDisplayDrivers/alva.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2009-2018 NV Access Limited, Davy Kager, Leonard de Ruijter, Optelec B.V.

from typing import List, Union

import bdDetect
import braille
from logHandler import log
import inputCore
import brailleInput
import hwIo
from hwIo import intToByte, boolToByte, Serial
from globalCommands import SCRCAT_BRAILLE
import ui
from baseObject import ScriptableObject
import time
import datetime

ALVA_RELEASE_MASK = 0x80
ALVA_2ND_CR_MASK = 0x80
ALVA_BRAILLE_OUTPUT_REPORT = b"\x02"
ALVA_BRAILLE_OUTPUT_MAX_SIZE = 40
ALVA_KEY_REPORT = b"\x04"
ALVA_KEY_REPORT_KEY_POS = 1
ALVA_KEY_REPORT_KEY_GROUP_POS = 2
ALVA_KEY_RAW_INPUT_MASK = 0x30
ALVA_DISPLAY_SETTINGS_REPORT = b"\x05"
ALVA_DISPLAY_SETTINGS_STATUS_CELL_SIDE_POS = 2
ALVA_DISPLAY_SETTINGS_CELL_COUNT_POS = 6
ALVA_KEY_SETTINGS_REPORT = b"\x06"
ALVA_KEY_SETTINGS_POS = 1 # key settings are stored as bits in 1 byte
ALVA_RTC_REPORT = b"\x0a"
ALVA_RTC_STR_LENGTH = 7
ALVA_RTC_MAX_DRIFT = 5
ALVA_RTC_MIN_YEAR = 1900
ALVA_RTC_MAX_YEAR = 3000
ALVA_MODEL_BC640 = 0x40
ALVA_MODEL_BC680 = 0x80
ALVA_MODEL_CONVERTER = 0x99
ESCAPE = b"\x1b"

ALVA_MODEL_IDS = {
	ALVA_MODEL_BC640: "BC640",
	ALVA_MODEL_BC680: "BC680",
	ALVA_MODEL_CONVERTER: "ProtocolConverter",
}

ALVA_SER_CMD_LENGTHS = {
	b"T": 2, # Status cells
	b"S": 1, # Splitpoint
	b"D": 1, # Dot pressure
	b"O": 1, # Output Braille table
	b"I": 1, # Input Braille table
	b"F": 4, # Key feedback
	b"P": 1, # Key repeat
	b"2": 3, # 2nd CR row emulation parameters
	b"L": 3, # System language
	b"R": 1, # Bluetooth enable/disable
	b"V": 5, # Hardware and firmware versions
	b"G": 9, # Battery status
	b"H": ALVA_RTC_STR_LENGTH, # Time
	b"?": 1, # Device ID
	b"E": 1, # Braille cell count
	b"N": 12, # Serial numbers
	b"X": 1, # Bluetooth connection state
	b"k": 1, # Standard HID keyboard interface enable/disable
	b"r": 1, # Raw keyboard messages enable/disable
	b"h": 8, # Serial HID input messages
	b"K": 2, # Keys message
}

ALVA_THUMB_GROUP = 0x71
ALVA_ETOUCH_GROUP = 0x72
ALVA_SP_GROUP = 0x73
ALVA_CR_GROUP = 0x74
ALVA_FEATURE_PACK_GROUP = 0x78
ALVA_SPECIAL_KEYS_GROUP = 0x01
ALVA_SPECIAL_SETTINGS_CHANGED = 0x01

DOUBLED_KEY_COUNTS = {
	ALVA_THUMB_GROUP: 5,
	ALVA_SP_GROUP: 9
}

ALVA_KEYS = {
	# Thumb keys (FRONT_GROUP)
	ALVA_THUMB_GROUP: ("t1", "t2", "t3", "t4", "t5",
		# Only for BC680
		"t1", "t2", "t3", "t4", "t5"),
	# eTouch keys (ETOUCH_GROUP)
	ALVA_ETOUCH_GROUP: ("etouch1", "etouch2", "etouch3", "etouch4"),
	# Smartpad keys (PDA_GROUP)
	ALVA_SP_GROUP: ("sp1", "sp2", "spLeft", "spEnter", "spUp", "spDown", "spRight", "sp3", "sp4",
		# Only for BC680
		"sp1", "sp2", "spLeft", "spEnter", "spUp", "spDown", "spRight", "sp3", "sp4"),
	# Feature pack keys.
	# Numbers start at 0x01, therefore the first string is an empty placeholder.
	ALVA_FEATURE_PACK_GROUP: ("", "dot1", "dot2", "dot3", "dot4", "dot5", "dot6", "dot7", "dot8",
		"control", "windows", "space", "alt", "enter"),
}

class BrailleDisplayDriver(braille.BrailleDisplayDriver, ScriptableObject):
	_dev: Union[hwIo.Serial, hwIo.Hid]
	name = "alva"
	# Translators: The name of a braille display.
	description = _("Optelec ALVA 6 series/protocol converter")
	isThreadSafe = True
	timeout = 0.2
	supportedSettings = (
		braille.BrailleDisplayDriver.HIDInputSetting(useConfig=False),
	)

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts(filterFunc=lambda info: info.get("bluetoothName","").startswith("ALVA "))

	def _get_model(self):
		if not self._deviceId:
			return ""
		self.model = ALVA_MODEL_IDS[self._deviceId]
		return self.model

	def _updateSettings(self):
		oldNumCells = self.numCells
		if self.isHid:
			displaySettings = self._dev.getFeature(ALVA_DISPLAY_SETTINGS_REPORT)
			if displaySettings[ALVA_DISPLAY_SETTINGS_STATUS_CELL_SIDE_POS] > 1:
				# #8106: The ALVA BC680 is known to return a malformed feature report for the first issued request.
				# Therefore, request another display settings report
				displaySettings = self._dev.getFeature(ALVA_DISPLAY_SETTINGS_REPORT)
			self.numCells = displaySettings[ALVA_DISPLAY_SETTINGS_CELL_COUNT_POS]
			timeBytes: bytes = self._dev.getFeature(ALVA_RTC_REPORT)[1:ALVA_RTC_STR_LENGTH+1]
			try:
				self._handleTime(timeBytes)
			except:
				log.debugWarning("Getting time from ALVA display failed", exc_info=True)
			keySettings = self._dev.getFeature(ALVA_KEY_SETTINGS_REPORT)[ALVA_KEY_SETTINGS_POS]
			self._rawKeyboardInput = bool(keySettings & ALVA_KEY_RAW_INPUT_MASK)
		else:
			# Get cell count
			self._ser6SendMessage(b"E", b"?")
			for i in range(3):
				self._dev.waitForRead(self.timeout)
				if self.numCells: # Display responded
					break
			else: # No response from display, do not send the other requests.
				return
			# Get device date and time
			self._ser6SendMessage(b"H", b"?")
			# Get HID keyboard input state
			self._ser6SendMessage(b"r", b"?")
		if oldNumCells not in (0, self.numCells):
			# In case of splitpoint changes, we need to update the braille handler as well
			braille.handler.displaySize = self.numCells

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver,self).__init__()
		self.numCells = 0
		self._rawKeyboardInput = False
		self._deviceId = None

		for portType, portId, port, portInfo in self._getTryPorts(port):
			self.isHid = portType == bdDetect.KEY_HID
			# Try talking to the display.
			try:
				if self.isHid:
					self._dev = hwIo.Hid(port, onReceive=self._hidOnReceive)
					self._deviceId = int(portId[-2:],16)
				else:
					self._dev = hwIo.Serial(port, timeout=self.timeout, writeTimeout=self.timeout, onReceive=self._ser6OnReceive)
					# Get the device ID
					self._ser6SendMessage(b"?", b"?")
					for i in range(3):
						self._dev.waitForRead(self.timeout)
						if self._deviceId: # Display responded
							break
					else: # No response from display
						continue
			except EnvironmentError:
				log.debugWarning("", exc_info=True)
				continue
			self._updateSettings()
			if self.numCells:
				# A display responded.
				log.info("Found display with {cells} cells connected via {type} ({port})".format(
					cells=self.numCells, type=portType, port=port))
				break
			self._dev.close()

		else:
			raise RuntimeError("No ALVA display found")

		self._keysDown = set()
		self._ignoreKeyReleases = False

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
		finally:
			# Make sure the device gets closed.
			# If it doesn't, we may not be able to re-open it later.
			self._dev.close()
			if not self.isHid:
				# We must sleep after closing the COM port, as it takes some time for the device to disconnect.
				time.sleep(self.timeout)

	def _ser6SendMessage(self, cmd: bytes, value: bytes = b"") -> None:
		if not isinstance(value, bytes):
			raise TypeError("Expected param 'value' to have type 'bytes'")
		self._dev.write(b"".join([ESCAPE, cmd, value]))

	def _ser6OnReceive(self, data: bytes):
		""" Callback for L{self._dev} when it is L{hwIo.Serial}
		"""
		if data != ESCAPE:
			return
		cmd: bytes = self._dev.read(1)
		commandLen = ALVA_SER_CMD_LENGTHS[cmd]
		value: bytes = self._dev.read(commandLen)

		if cmd == b"K":  # Input
			self._handleInput(group=value[0], number=value[1])
		elif cmd == b"E":  # Braille cell count
			self.numCells = ord(value)
		elif cmd == b"?":  # Device ID
			self._deviceId = ord(value)  # this command only gets one byte
		elif cmd == b"r":  # Raw keyboard messages enable/disable
			self._rawKeyboardInput = bool(ord(value))
		elif cmd == b"H":  # Time
			# Handling time for serial displays does not block initialization if it fails.
			self._handleTime(value)

	def _hidOnReceive(self, data: bytes):
		"""Callback for L{self._dev} when it is L{hwIo.Hid}
		"""
		reportID: bytes = data[0:1]
		if reportID == ALVA_KEY_REPORT:
			self._handleInput(
				data[ALVA_KEY_REPORT_KEY_GROUP_POS],
				data[ALVA_KEY_REPORT_KEY_POS]
			)

	def _handleInput(self, group: int, number: int) -> None:
		if group == ALVA_SPECIAL_KEYS_GROUP:
			# ALVA displays communicate setting changes as input messages.
			if number == ALVA_SPECIAL_SETTINGS_CHANGED:
				# Some internal settings have changed.
				# For example, split point could have been set, in which case the number of cells changed.
				# We must handle these properly.
				self._updateSettings()
			return
		isRelease = bool(group & ALVA_RELEASE_MASK)
		group = group & ~ALVA_RELEASE_MASK
		if isRelease:
			if not self._ignoreKeyReleases and self._keysDown:
				try:
					inputCore.manager.executeGesture(InputGesture(self.model, self._keysDown, brailleInput=self._rawKeyboardInput))
				except inputCore.NoInputGestureAction:
					pass
				# Any further releases are just the rest of the keys in the combination being released,
				# so they should be ignored.
				self._ignoreKeyReleases = True
			self._keysDown.discard((group, number))
		else: # Press
			self._keysDown.add((group, number))
			# This begins a new key combination.
			self._ignoreKeyReleases = False

	def _hidDisplay(self, cellBytes: bytes) -> None:
		for offset in range(0, len(cellBytes), ALVA_BRAILLE_OUTPUT_MAX_SIZE):
			cellsToWrite = cellBytes[offset:offset+ALVA_BRAILLE_OUTPUT_MAX_SIZE]
			data = b"".join([
				ALVA_BRAILLE_OUTPUT_REPORT,
				intToByte(offset),
				intToByte(len(cellsToWrite)),
				cellsToWrite
			])
			self._dev.write(data)

	def _ser6Display(self, cellBytes: bytes) -> None:
		if not isinstance(cellBytes, bytes):
			raise TypeError("Expected param 'cells' to be of type 'bytes'")
		value = b"".join([
			b"\x00",
			intToByte(len(cellBytes)),
			cellBytes
		])
		self._ser6SendMessage(b"B", value)

	def display(self, cells: List[int]):
		# cells will already be padded up to numCells.
		cellBytes = bytes(cells)
		if self.isHid:
			self._hidDisplay(cellBytes)
		else:
			self._ser6Display(cellBytes)

	def _handleTime(self, time: bytes):
		"""
		@type time: bytes
		"""
		year = time[0] | time[1] << 8
		if not ALVA_RTC_MIN_YEAR <= year <= ALVA_RTC_MAX_YEAR:
			log.debug("This ALVA display doesn't reveal clock information")
			return
		try:
			displayDateTime = datetime.datetime(
				year=year,
				month=time[2],
				day=time[3],
				hour=time[4],
				minute=time[5],
				second=time[6]
			)
		except ValueError:
			log.debugWarning("Invalid time/date of ALVA display: %r" % time)
			return
		localDateTime = datetime.datetime.today()
		if abs((displayDateTime - localDateTime).total_seconds()) >= ALVA_RTC_MAX_DRIFT:
			log.debugWarning("Display time out of sync: %s"%displayDateTime.isoformat())
			self._syncTime(localDateTime)
		else:
			log.debug("Time not synchronized. Display time %s"%displayDateTime.isoformat())

	def _syncTime(self, dt: datetime.datetime):
		log.debug("Synchronizing braille display date and time...")
		timeList: List[int] = [
			dt.year & 0xFF, dt.year >> 8,
			dt.month,
			dt.day,
			dt.hour,
			dt.minute,
			dt.second
		]
		if self.isHid:
			self._dev.setFeature(ALVA_RTC_REPORT + bytes(timeList))
		else:
			self._ser6SendMessage(b"H", bytes(timeList))

	def _get_hidKeyboardInput(self):
		return not self._rawKeyboardInput

	def _set_hidKeyboardInput(self, state):
		rawState = not state
		if self.isHid:
			# Make sure the device settings are up to date.
			keySettings: int = self._dev.getFeature(
				ALVA_KEY_SETTINGS_REPORT
			)[ALVA_KEY_SETTINGS_POS]
			# Try to update the state
			if rawState:
				newKeySettings = intToByte(keySettings | ALVA_KEY_RAW_INPUT_MASK)
			elif keySettings & ALVA_KEY_RAW_INPUT_MASK:
				newKeySettings = intToByte(keySettings ^ ALVA_KEY_RAW_INPUT_MASK)
			else:
				newKeySettings = intToByte(keySettings)
			self._dev.setFeature(ALVA_KEY_SETTINGS_REPORT + newKeySettings)
			# Check whether the state has been changed successfully.
			# If not, this device does not support this feature.
			keySettings: int = self._dev.getFeature(
				ALVA_KEY_SETTINGS_REPORT
			)[ALVA_KEY_SETTINGS_POS]
			# Save the new state
			self._rawKeyboardInput = bool(keySettings & ALVA_KEY_RAW_INPUT_MASK)
		else:
			self._ser6SendMessage(
				cmd=b"r",
				value=boolToByte(rawState)
			)
			self._ser6SendMessage(b"r", b"?")
			for i in range(3):
				self._dev.waitForRead(self.timeout)
				if rawState is self._rawKeyboardInput:
					break

	scriptCategory = SCRCAT_BRAILLE
	def script_toggleHidKeyboardInput(self, gesture):
		oldHidKeyboardInput = self.hidKeyboardInput
		self.hidKeyboardInput = not self.hidKeyboardInput
		if self.hidKeyboardInput is oldHidKeyboardInput:
			# Translators: Message when setting HID keyboard simulation failed.
			ui.message(_("Setting HID keyboard simulation not supported"))
		elif self.hidKeyboardInput:
			# Translators: Message when HID keyboard simulation is enabled.
			ui.message(_("HID keyboard simulation enabled"))
		else:
			# Translators: Message when HID keyboard simulation is disabled.
			ui.message(_("HID keyboard simulation disabled"))
	# Translators: Description of the script that toggles HID keyboard simulation.
	script_toggleHidKeyboardInput.__doc__ = _("Toggles HID keyboard simulation")

	__gestures = {
		"br(alva):t1+spEnter": "toggleHidKeyboardInput",
	}

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(alva):t1","br(alva):etouch1"),
			"braille_previousLine": ("br(alva):t2",),
			"braille_toFocus": ("br(alva):t3",),
			"braille_nextLine": ("br(alva):t4",),
			"braille_scrollForward": ("br(alva):t5","br(alva):etouch3"),
			"braille_routeTo": ("br(alva):routing",),
			"braille_reportFormatting": ("br(alva):secondRouting",),
			"review_top": ("br(alva):t1+t2",),
			"review_bottom": ("br(alva):t4+t5",),
			"braille_toggleTether": ("br(alva):t1+t3",),
			"braille_cycleCursorShape": ("br(alva):t1+t4",),
			"braille_toggleShowCursor": ("br(alva):t2+t5",),
			"title": ("br(alva):etouch2",),
			"reportStatusLine": ("br(alva):etouch4",),
			"kb:shift+tab": ("br(alva):sp1",),
			"kb:alt": ("br(alva):sp2","br(alva):alt",),
			"kb:escape": ("br(alva):sp3",),
			"kb:tab": ("br(alva):sp4",),
			"kb:upArrow": ("br(alva):spUp",),
			"kb:downArrow": ("br(alva):spDown",),
			"kb:leftArrow": ("br(alva):spLeft",),
			"kb:rightArrow": ("br(alva):spRight",),
			"kb:enter": ("br(alva):spEnter","br(alva):enter",),
			"dateTime": ("br(alva):sp2+sp3",),
			"showGui": ("br(alva):sp1+sp3",),
			"kb:windows+d": ("br(alva):sp1+sp4",),
			"kb:windows+b": ("br(alva):sp3+sp4",),
			"kb:windows": ("br(alva):sp1+sp2","br(alva):windows",),
			"kb:alt+tab": ("br(alva):sp2+sp4",),
			"kb:control+home": ("br(alva):t3+spUp",),
			"kb:control+end": ("br(alva):t3+spDown",),
			"kb:home": ("br(alva):t3+spLeft",),
			"kb:end": ("br(alva):t3+spRight",),
			"kb:control": ("br(alva):control",),
		}
	})

class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, model, keys, brailleInput=False):
		super(InputGesture, self).__init__()
		isNoBC640 = model != ALVA_MODEL_IDS[ALVA_MODEL_BC640]
		# Model identifiers should not contain spaces.
		self.model = model.replace(" ", "")
		assert(self.model.isalnum())
		self.keyCodes = set(keys)
		self.keyNames = names = []
		secondaryNames = []
		dots = 0
		space = False
		for group, number in self.keyCodes:
			if group == ALVA_CR_GROUP:
				if number & ALVA_2ND_CR_MASK:
					keyName = "secondRouting"
					self.routingIndex = number & ~ALVA_2ND_CR_MASK
				else:
					keyName = "routing"
					self.routingIndex = number
				names.append(keyName)
				if isNoBC640:
					secondaryNames.append(keyName)
			else:
				try:
					keyName = ALVA_KEYS[group][number]
				except (KeyError, IndexError):
					log.debugWarning("Unknown key with group %d and number %d" % (group, number))
					return
				names.append(keyName)
				if isNoBC640:
					doubledKeyCount = DOUBLED_KEY_COUNTS.get(group)
					if doubledKeyCount:
						keyName = ("r" if number >= doubledKeyCount else "l") + keyName
					secondaryNames.append(keyName)
			# Braille input
			if brailleInput:
				if group == ALVA_FEATURE_PACK_GROUP:
					if ALVA_KEYS[group][number] == "space":
						space = True
					elif number <= 8:
						dots |= 1 << (number-1)
					else:
						brailleInput = False
				else:
					brailleInput = False

		self.id = "+".join(names)
		self.secondaryId = "+".join(secondaryNames) if isNoBC640 else self.id
		if brailleInput:
			self.dots = dots
			self.space = space

	def _get_identifiers(self):
		ids = [
			u"br({source}.{model}):{id}".format(source=self.source, model=self.model, id=self.secondaryId),
			u"br({source}):{id}".format(source=self.source, id=self.id),
		]
		ids.extend(brailleInput.BrailleInputGesture._get_identifiers(self))
		return ids
