# brailleDisplayDrivers/HID.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited

from dataclasses import dataclass
from typing import List, Optional
import enum
import braille
import inputCore
from logHandler import log
import brailleInput
import bdDetect
import hidpi
import hwIo.hid
from hwIo import intToByte

from bdDetect import HID_USAGE_PAGE_BRAILLE


class BraillePageUsageID(enum.IntEnum):
	UNDEFINED = 0
	BRAILLE_DISPLAY = 0x1
	BRAILLE_ROW = 0x2
	EIGHT_DOT_BRAILLE_CELL = 0x3
	SIX_DOT_BRAILLE_CELL = 0x4
	NUMBER_OF_BRAILLE_CELLS = 0x5
	SCREEN_READER_CONTROL = 0x6
	SCREEN_READER_IDENTIFIER = 0x7
	ROUTER_SET_1 = 0xFA
	ROUTER_SET_2 = 0xFB
	ROUTER_SET_3 = 0xFC
	ROUTER_KEY = 0x100
	ROW_ROUTER_KEY = 0x101
	BRAILLE_BUTTONS = 0x200
	BRAILLE_KEYBOARD_DOT_1 = 0x201
	BRAILLE_KEYBOARD_DOT_2 = 0x202
	BRAILLE_KEYBOARD_DOT_3 = 0x203
	BRAILLE_KEYBOARD_DOT_4 = 0x204
	BRAILLE_KEYBOARD_DOT_5 = 0x205
	BRAILLE_KEYBOARD_DOT_6 = 0x206
	BRAILLE_KEYBOARD_DOT_7 = 0x207
	BRAILLE_KEYBOARD_DOT_8 = 0x208
	BRAILLE_KEYBOARD_SPACE = 0x209
	BRAILLE_KEYBOARD_LEFT_SPACE = 0x20A
	BRAILLE_KEYBOARD_RIGHT_SPACE = 0x20B
	BRAILLE_FACE_CONTROLS = 0x20C
	BRAILLE_LEFT_CONTROLS = 0x20D
	BRAILLE_RIGHT_CONTROLS = 0x20E
	BRAILLE_TOP_CONTROLS = 0x20F
	BRAILLE_JOYSTICK_CENTER = 0x210
	BRAILLE_JOYSTICK_UP = 0x211
	BRAILLE_JOYSTICK_DOWN = 0x212
	BRAILLE_JOYSTICK_LEFT = 0x213
	BRAILLE_JOYSTICK_RIGHT = 0x214
	BRAILLE_DPAD_CENTER = 0x215
	BRAILLE_DPAD_UP = 0x216
	BRAILLE_DPAD_DOWN = 0x217
	BRAILLE_DPAD_LEFT = 0x218
	BRAILLE_DPAD_RIGHT = 0x219
	BRAILLE_PAN_LEFT = 0x21A
	BRAILLE_PAN_RIGHT = 0x21B
	BRAILLE_ROCKER_UP = 0x21C
	BRAILLE_ROCKER_DOWN = 0x21D
	BRAILLE_ROCKER_PRESS = 0x21E


@dataclass
class ButtonCapsInfo:
	buttonCaps: hidpi.HIDP_VALUE_CAPS
	relativeIndexInCollection: int = 0


class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	_dev: hwIo.hid.Hid
	name = "hid"
	# Translators: The name of a series of braille displays.
	description = _("Standard HID Braille Display")
	isThreadSafe = True

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver, self).__init__()
		self.numCells = 0

		for portType, portId, port, portInfo in self._getTryPorts(port):
			if portType != bdDetect.KEY_HID:
				continue
			# Try talking to the display.
			try:
				self._dev = hwIo.hid.Hid(port, onReceive=self._hidOnReceive)
			except EnvironmentError:
				log.debugWarning("", exc_info=True)
				continue  # Couldn't connect.
			if self._dev.usagePage != HID_USAGE_PAGE_BRAILLE:
				log.debug("Not braille")
				continue
			cellValueCaps = self._findCellValueCaps()
			if cellValueCaps:
				self._cellValueCaps = cellValueCaps
				self.numCells = cellValueCaps.ReportCount
				# A display responded.
				log.info("Found display with {cells} cells connected via {type} ({port})".format(
					cells=self.numCells, type=portType, port=port))
				break
			# This device can't be initialized. Move on to the next (if any).
			self._dev.close()
		else:
			raise RuntimeError("No display found")
		self._inputButtonCapsByDataIndex = self._collectInputButtonCapsByDataIndex()
		self._keysDown = set()
		self._ignoreKeyReleases = False

	def _findCellValueCaps(self) -> Optional[hidpi.HIDP_VALUE_CAPS]:
		for valueCaps in self._dev.outputValueCaps:
			if (
				valueCaps.LinkUsagePage == HID_USAGE_PAGE_BRAILLE
				and valueCaps.LinkUsage == BraillePageUsageID.BRAILLE_ROW
				and valueCaps.u1.NotRange.Usage in (
					BraillePageUsageID.EIGHT_DOT_BRAILLE_CELL,
					BraillePageUsageID.SIX_DOT_BRAILLE_CELL
				)
				and valueCaps.ReportCount > 0
			):
				return valueCaps
		return None

	def _collectInputButtonCapsByDataIndex(self):
		capsByDataIndex = {}
		relativeIndexInCollection = 0
		lastLinkCollection = None
		for buttonCaps in self._dev.inputButtonCaps:
			if buttonCaps.LinkCollection != lastLinkCollection:
				lastLinkCollection = buttonCaps.LinkCollection
				relativeIndexInCollection = 0
			else:
				relativeIndexInCollection += 1
			if buttonCaps.IsRange:
				r = buttonCaps.u1.Range
				for index in range(r.DataIndexMin, r.DataIndexMax + 1):
					capsByDataIndex[index] = ButtonCapsInfo(buttonCaps, relativeIndexInCollection=relativeIndexInCollection)
			else:
				nr = buttonCaps.u1.NotRange
				index = nr.DataIndex
				capsByDataIndex[index] = ButtonCapsInfo(buttonCaps, relativeIndexInCollection=relativeIndexInCollection)
		return capsByDataIndex

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
		finally:
			# Make sure the device gets closed.
			# If it doesn't, we may not be able to re-open it later.
			self._dev.close()

	def _hidOnReceive(self, data: bytes):
		report = hwIo.hid.HidInputReport(self._dev, data)
		keys = []
		for dataItem in report.getDataItems():
			if dataItem.DataIndex in self._inputButtonCapsByDataIndex and dataItem.u1.On:
				keys.append(dataItem.DataIndex)
		if len(keys) > len(self._keysDown):
			# Press. This begins a new key combination.
			self._ignoreKeyReleases = False
		elif len(keys) < len(self._keysDown):
			self._handleKeyRelease()
		self._keysDown = keys

	def _handleKeyRelease(self):
		if self._ignoreKeyReleases or not self._keysDown:
			return
		try:
			inputCore.manager.executeGesture(InputGesture(self, self._keysDown))
		except inputCore.NoInputGestureAction:
			pass
		# Any further releases are just the rest of the keys in the combination being released,
		# so they should be ignored.
		self._ignoreKeyReleases = True

	def display(self, cells: List[int]):
		# cells will already be padded up to numCells.
		cellBytes = b"".join(intToByte(cell) for cell in cells)
		report = hwIo.hid.HidOutputReport(self._dev, reportID=self._cellValueCaps.ReportID)
		report.setUsageValueArray(
			HID_USAGE_PAGE_BRAILLE,
			self._cellValueCaps.LinkCollection,
			self._cellValueCaps.u1.NotRange.Usage,
			cellBytes
		)
		self._dev.write(report.data)

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(HID):panLeft",),
			"braille_scrollForward": ("br(HID):panRight",),
			"braille_previousLine": ("br(HID):space+dot1",),
			"braille_nextLine": ("br(HID):space+dot4",),
			"braille_routeTo": ("br(HID):routerSet1_routerKey",),
			"braille_toggleTether": ("br(HID):up+down",),
			"kb:upArrow": ("br(HID):joystickUp",),
			"kb:downArrow": ("br(HID):joystickDown",),
			"kb:leftArrow": ("br(HID):space+dot3", "br(HID):joystickLeft"),
			"kb:rightArrow": ("br(HID):space+dot6", "br(HID):joystickRight"),
			"showGui": (
				"br(HID):space+dot1+dot3+dot4+dot5",
			),
			"kb:shift+tab": ("br(HID):space+dot1+dot3",),
			"kb:tab": ("br(HID):space+dot4+dot6",),
			"kb:alt": ("br(HID):space+dot1+dot3+dot4",),
			"kb:escape": ("br(HID):space+dot1+dot5",),
			"kb:enter": ("br(HID):joystickCenter"),
			"kb:windows+d": (
				"br(HID):Space+dot1+dot4+dot5",
			),
			"kb:windows": ("br(HID):space+dot3+dot4",),
			"kb:alt+tab": ("br(HID):space+dot2+dot3+dot4+dot5",),
			"sayAll": (
				"br(HID):Space+dot1+dot2+dot3+dot4+dot5+dot6",
			),
		},
	})


class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, driver, dataIndices):
		super(InputGesture, self).__init__()
		self.keyCodes = set(dataIndices)

		self.keyNames = names = []
		namePrefix = None
		isBrailleInput = True
		for index in dataIndices:
			buttonCapsInfo = driver._inputButtonCapsByDataIndex.get(index)
			buttonCaps = buttonCapsInfo.buttonCaps
			usagePage = buttonCaps.UsagePage
			if buttonCaps.IsRange:
				r = buttonCaps.u1.Range
				relativeIndex = index - r.DataIndexMin
				usageID = r.UsageMin + relativeIndex
			else:
				usageID = buttonCaps.u1.NotRange.Usage
			linkUsagePage = buttonCaps.LinkUsagePage
			linkUsageID = buttonCaps.LinkUsage
			if usagePage == HID_USAGE_PAGE_BRAILLE and isBrailleInput:
				if BraillePageUsageID.BRAILLE_KEYBOARD_DOT_1 <= usageID <= BraillePageUsageID.BRAILLE_KEYBOARD_DOT_8:
					self.dots |= 1 << (usageID - BraillePageUsageID.BRAILLE_KEYBOARD_DOT_1)
				elif usageID in (
					BraillePageUsageID.BRAILLE_KEYBOARD_SPACE,
					BraillePageUsageID.BRAILLE_KEYBOARD_LEFT_SPACE,
					BraillePageUsageID.BRAILLE_KEYBOARD_RIGHT_SPACE,
				):
					self.space = True
			else:
				# This is not braille input.
				isBrailleInput = False
				self.dots = 0
				self.space = False
			if (
				usagePage == HID_USAGE_PAGE_BRAILLE
				and usageID == BraillePageUsageID.ROUTER_KEY
			):
				self.routingIndex = buttonCapsInfo.relativeIndexInCollection + 1
				# Prefix the gesture name with the specific routing collection name (E.g. routerSet1)
				namePrefix = self._usageIDToGestureName(linkUsagePage, linkUsageID)
		name = self._usageIDToGestureName(usagePage, usageID)
		if namePrefix:
			name = "_".join([namePrefix, name])
		names.append(name)
		self.id = "+".join(names)

	def _usageIDToGestureName(self, usagePage: int, usageID: int):
		if usagePage != HID_USAGE_PAGE_BRAILLE:
			# The usage ID is from another HID usage page
			# Return a generic name with page and ID included
			return "usagePage%d&usageID%d" % (usagePage, usageID)
		try:
			rawName = BraillePageUsageID(usageID).name
		except ValueError:
			# An unknown usage ID within the braille usage page
			# Return a generic name with the unknown ID included
			return "brailleUsage%d" % usageID
		name = rawName.lower()
		# Remove braille_keyboard or braille_ from the beginning of the name
		if name.startswith('braille_keyboard_'):
			name = name[len('braille_keyboard_'):]
		elif name.startswith('braille_'):
			name = name[len('braille_'):]
		# Capitalize the start of all words except the first
		wordList = name.split('_')
		for index in range(1, len(wordList)):
			wordList[index] = wordList[index].title()
		# Join the words together as  camelcase.
		name = "".join(wordList)
		return name
