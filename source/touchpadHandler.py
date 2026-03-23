# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2012-2025 NV Access Limited, Joseph Lee, Babbage B.V， gexgd0419.

"""Handles Windows Precision Touchpad interaction.
Used to provide input gestures for touchpads, touch modes and other support facilities.
This is based on the existing touchscreen support,
and utilizes some touchscreen facilities such as TouchTracker.
"""

import dataclasses
import threading
from ctypes import (
	POINTER,
	Array,
	WinError,
	byref,
	c_void_p,
	create_unicode_buffer,
	sizeof,
	cast,
)
from ctypes.wintypes import (
	BYTE,
	LPCWSTR,
	PCHAR,
	MSG,
	UINT,
	ULONG,
	USHORT,
)
import re
import winBindings.kernel32
from winBindings import user32, hid
import gui
import config
import inputCore
import screenExplorer
from logHandler import log
import touchTracker
import core


availableTouchModes = ["text", "object"]

touchModeLabels = {
	"text": _("text mode"),
	"object": _("object mode"),
}

HWND_MESSAGE = -3

WM_QUIT = 18
WM_INPUT = 0x00FF
WM_INPUT_DEVICE_CHANGE = 0x00FE

# dwFlags in RAWINPUTDEVICE
RIDEV_REMOVE = 0x00000001
RIDEV_INPUTSINK = 0x00000100
RIDEV_DEVNOTIFY = 0x00002000

# Flags for GetRawInputData
RID_INPUT = 0x10000003
RID_HEADER = 0x10000005

# dwType in RAWINPUTHEADER
RIM_TYPEMOUSE = 0
RIM_TYPEKEYBOARD = 1
RIM_TYPEHID = 2

# uiCommand for GetRawInputDeviceInfo
RIDI_PREPARSEDDATA = 0x20000005
RIDI_DEVICENAME = 0x20000007  # the return valus is the character length, not the byte size
RIDI_DEVICEINFO = 0x2000000B

# HID usages

HID_USAGE_PAGE_GENERIC = 0x01
HID_USAGE_GENERIC_X = 0x30  # Mandatory
HID_USAGE_GENERIC_Y = 0x31  # Mandatory

HID_USAGE_PAGE_BUTTON = 0x09  # Optional
# The usage number is the button number, e.g. button 1 = usage 1
# For touchpads, button 1 = touchpad button, button 2 = external primary button, etc.

HID_USAGE_PAGE_DIGITIZER = 0x0D
HID_USAGE_DIGITIZER_TOUCH_PAD = 0x05
HID_USAGE_DIGITIZER_TIP_SWITCH = 0x42  # Mandatory. Set if in contact.
HID_USAGE_DIGITIZER_TOUCH_VALID = 0x47  # Mandatory. Confidence.
HID_USAGE_DIGITIZER_WIDTH = 0x48  # Optional
HID_USAGE_DIGITIZER_HEIGHT = 0x49  # Optional
HID_USAGE_DIGITIZER_CONTACT_IDENTIFIER = 0x51  # Mandatory
HID_USAGE_DIGITIZER_CONTACT_COUNT = 0x54  # Mandatory
HID_USAGE_DIGITIZER_CONTACT_COUNT_MAXIMUM = 0x55
HID_USAGE_DIGITIZER_SCAN_TIME = 0x56  # Mandatory

UINT_MAX = UINT(-1).value  # Returned by some APIs on error


HIDP_STATUS_BUFFER_TOO_SMALL = 0xC0110007

# Human readable names for HIDP NTSTATUS codes, for debugging purposes
_HIDP_STATUS_MAP = {
	0x00110000: "SUCCESS",
	0x80110001: "NULL",
	0xC0110001: "INVALID_PREPARSED_DATA",
	0xC0110002: "INVALID_REPORT_TYPE",
	0xC0110003: "INVALID_REPORT_LENGTH",
	0xC0110004: "USAGE_NOT_FOUND",
	0xC0110005: "VALUE_OUT_OF_RANGE",
	0xC0110006: "BAD_LOG_PHY_VALUES",
	0xC0110007: "BUFFER_TOO_SMALL",
	0xC0110008: "INTERNAL_ERROR",
	0xC0110009: "I8042_TRANS_UNKNOWN",
	0xC011000A: "INCOMPATIBLE_REPORT_ID",
	0xC011000B: "NOT_VALUE_ARRAY",
	0xC011000C: "IS_VALUE_ARRAY",
	0xC011000D: "DATA_INDEX_NOT_FOUND",
	0xC011000E: "DATA_INDEX_OUT_OF_RANGE",
	0xC011000F: "BUTTON_NOT_PRESSED",
	0xC0110010: "REPORT_DOES_NOT_EXIST",
	0xC0110020: "NOT_IMPLEMENTED",
	0xC0110021: "NOT_BUTTON_ARRAY",
}

# Human readable names for usage pages and usages, for debugging purposes
_HID_USAGE_MAP: dict[int, tuple[str, dict[int, str]]] = {
	0x01: (
		"Generic",
		{
			0x30: "X",
			0x31: "Y",
		},
	),
	0x09: (
		"Button",
		{
			0x01: "Touchpad button",
			0x02: "External primary button",
			0x03: "External secondary button",
		},
	),
	0x0D: (
		"Digitizer",
		{
			0x05: "Touchpad",
			0x0E: "Device configuration",
			0x22: "Finger",
			0x30: "Tip pressure",
			0x3F: "Azimuth",
			0x42: "Tip switch",
			0x47: "Touch valid",
			0x48: "Width",
			0x49: "Height",
			0x51: "Contact ID",
			0x54: "Contact count",
			0x55: "Contact count maximum",
			0x56: "Scan time",
		},
	),
	0x20: (
		"Sensor",
		{
			0x494: "Data field Force",
		},
	),
}


touchWindow = None
touchThread = None


class TouchpadInputGesture(inputCore.InputGesture):
	"""
	Represents a gesture performed on a touchpad.
	Mostly the same as TouchInputGesture, except that "touchscreen" (ts:) is replaced with "touchpad" (tp:).
	Possible actions are:
	* Tap: a finger touches the touchpad only for a very short amount of time.
	* Flick{Left|Right|Up|Down}: a finger swipes the touchpad in a particular direction.
	* Tap and hold: a finger taps the touchpad but then again touches the touchpad, this time remaining held.
	* Hover down: A finger touches the touchpad long enough for the gesture to not be a tap, and it is also not already part of a tap and hold.
	* Hover: a finger is still touching the touchpad, and may be moving around. Only the most recent finger to be hovering causes these gestures.
	* Hover up: a finger that was classed as a hover, releases contact with the touchpad.
	All actions accept for Hover down, Hover and Hover up, can be made up of multiple fingers. It is possible to have things such as a 3-finger tap, or a 2-finger Tap and Hold, or a 4 finger Flick right.
	Taps maybe pluralized (I.e. a tap very quickly followed by another tap of the same number of fingers will be represented by a double tap, rather than two separate taps). Currently double, triple and quadruple plural taps are detected.
	Tap and holds can be pluralized also (E.g. a double tap and hold means that there were two taps before the hold).
	Actions also communicate if other fingers are currently held while performing the action. E.g. a hold+tap is when a finger touches the touchpad long enough to become a hover, and a tap with another finger is performed, while the first finger remains on the touchpad. Holds themselves also can be made of multiple fingers.
	Based on all of this, gestures could be as complicated as a 5-finger hold + 5-finger quadruple tap and hold.
	To find out the generalized point on the touchpad at which the gesture was performed, use this gesture's x and y properties.
	If low-level information  about the fingers and sub-gestures making up this gesture is required, the gesture's tracker and preheldTracker properties can be accessed.
	See touchHandler.MultitouchTracker for definitions of the available properties.
	"""

	counterNames = ["single", "double", "triple", "quadruple"]

	pluralActionLabels = {
		# Translators: a touchpad action performed once
		"single": _("single {action}"),
		# Translators: a touchpad action performed twice
		"double": _("double {action}"),
		# Translators: a touchpad action performed 3 times
		"triple": _("triple {action}"),
		# Translators: a touchpad action performed 4 times
		"quadruple": _("quadruple {action}"),
	}

	def _get_speechEffectWhenExecuted(self):
		if self.tracker.action in (touchTracker.action_hover, touchTracker.action_hoverUp):
			return None
		return super(TouchpadInputGesture, self).speechEffectWhenExecuted

	def _get_reportInInputHelp(self):
		return self.tracker.action != touchTracker.action_hover

	def __init__(self, preheldTracker, tracker, mode):
		super(TouchpadInputGesture, self).__init__()
		self.tracker = tracker
		self.preheldTracker = preheldTracker
		self.mode = mode
		self.x = tracker.x
		self.y = tracker.y

	def _get_identifiers(self):
		IDs = []
		for includeHeldFingers in [True, False] if self.preheldTracker else [False]:
			ID = ""
			if self.preheldTracker:
				ID += ("%dfinger_hold+" % self.preheldTracker.numFingers) if includeHeldFingers else "hold+"
			if self.tracker.numFingers > 1:
				ID += "%dfinger_" % self.tracker.numFingers
			if self.tracker.actionCount > 1:
				ID += "%s_" % self.counterNames[min(self.tracker.actionCount, 4) - 1]
			ID += self.tracker.action
			# "tp" is the gesture identifier source prefix for "touchpad".
			IDs.append("tp(%s):%s" % (self.mode, ID))
			IDs.append("tp:%s" % ID)
		return IDs

	RE_IDENTIFIER = re.compile(r"^tp(?:\((.+?)\))?:(.*)$")

	@classmethod
	def getDisplayTextForIdentifier(cls, identifier):
		mode, IDs = cls.RE_IDENTIFIER.match(identifier).groups()
		actions = []
		for ID in IDs.split("+"):
			action = None
			foundAction = foundPlural = False
			for subID in reversed(ID.split("_")):
				if not foundAction:
					action = touchTracker.actionLabels[subID]
					foundAction = True
					continue
				if not foundPlural:
					pluralActionLabel = cls.pluralActionLabels.get(subID)
					if pluralActionLabel:
						action = pluralActionLabel.format(action=action)
						foundPlural = True
						continue
				if subID.endswith("finger"):
					numFingers = int(subID[: 0 - len("finger")])
					if numFingers > 1:
						action = ngettext(
							# Translators: a touchpad action using multiple fingers
							"{numFingers} finger {action}",
							"{numFingers} finger {action}",
							numFingers,
						).format(numFingers=numFingers, action=action)
				break
			actions.append(action)
		# Translators: a touchpad gesture
		source = _("Touchpad")
		if mode:
			source = "{source}, {mode}".format(source=source, mode=touchModeLabels[mode])
		return source, " + ".join(actions)

	def _get__immediate(self):
		# Because touch may produce a hover gesture for every pump, an immediate pump
		# can result in exhaustion of the window message queue. Thus, don't do
		# immediate pumps for hover gestures.
		return not self.tracker.action == touchTracker.action_hover


inputCore.registerGestureSource("tp", TouchpadInputGesture)


def _checkHidStatus(ntstatus: int) -> None:
	"""
	Checks the `NTSTATUS` code (assumed unsigned) returned from `HidP_*` functions,
	and raise `OSError` on error.
	"""
	if ntstatus & 0x80000000:
		raise OSError(f"HID error {_HIDP_STATUS_MAP.get(ntstatus, str(ntstatus))}")


def _getRawInputData(lParam: int) -> Array[BYTE]:
	"""
	Returns the bytes of a `RAWINPUT` structure,
	given the `lParam` from `WM_INPUT` message.
	"""
	cbData = UINT(0)
	cbHeader = sizeof(user32.RAWINPUTHEADER)
	user32.GetRawInputData(lParam, RID_INPUT, None, byref(cbData), cbHeader)
	if cbData.value == 0:
		raise WinError()
	inputData = (BYTE * cbData.value)()
	if user32.GetRawInputData(lParam, RID_INPUT, inputData, byref(cbData), cbHeader) == UINT_MAX:
		raise WinError()
	return inputData


def _getPreparsedData(hDevice: int) -> Array[BYTE]:
	"""
	Returns bytes of preparsed data from the specified HID device.
	Preparsed data are needed when parsing HID reports from this device with `HidP_*` functions.
	"""
	cbData = UINT(0)
	user32.GetRawInputDeviceInfo(hDevice, RIDI_PREPARSEDDATA, None, byref(cbData))
	if cbData.value == 0:
		raise WinError()
	prepData = (BYTE * cbData.value)()
	if user32.GetRawInputDeviceInfo(hDevice, RIDI_PREPARSEDDATA, prepData, byref(cbData)) == UINT_MAX:
		raise WinError()
	return prepData


def _HIDUnitsToString(units: int) -> str | None:
	"""
	Converts HID units to human-readable units, for debugging purposes.
	Returns `None` when units == 0.
	Supports complex units built with basic units, such as `centimeter * seconds^-1`.

	See: https://www.usb.org/sites/default/files/documents/hid1_11.pdf
	"""

	# HID units can be divided into nibbles (4-bit groups).
	# The lowest nibble (Nibble 0) is the system nibble, which selects the unit system.
	# 0: None, 1: SI Linear, 2: SI Rotation, 3: English Linear, 4: English Rotation, 0xF: Vendor-defined
	nib_sys = units & 0xF
	if nib_sys == 0:
		return None
	elif nib_sys == 0xF:
		return "vendor-defined"
	elif nib_sys > 4:
		return "reserved"

	# The other nibbles represent the exponent of different unit parts.
	# Nibble 1: Length, 2: Mass, 3: Time, 4: Temperature, 5: Current, 6: Luminous intensity
	# Each nibble is a 4-bit signed integer of exponent.
	units_table = (
		("centimeter", "radians", "inch", "degrees"),
		("gram", "gram", "slug", "slug"),
		("seconds",) * 4,
		("kelvin", "kelvin", "fahrenheit", "fahrenheit"),
		("ampere",) * 4,
		("candela",) * 4,
	)

	# Iterate each nibble and construct a unit string
	units_strings = []
	for i in range(1, 7):
		nib = (units >> (i * 4)) & 0xF
		if nib == 0:
			continue
		unit_name = units_table[i - 1][nib_sys - 1]
		if nib == 1:
			units_strings.append(unit_name)
		else:
			# Convert 4-bit exponent to normal integer
			nib = (nib ^ 0x8) - 0x8
			units_strings.append(f"{unit_name}^{nib}")

	return " * ".join(units_strings)


def _HIDCapsToString(
	caps: Array[hid.HIDP_BUTTON_CAPS | hid.HIDP_VALUE_CAPS],
	headerIndent: int = 2,
	contentIndent: int = 4,
) -> str:
	"""Converts a button/value caps list to string, for debugging purposes."""
	capStrings = []
	headerIndentStr = " " * headerIndent
	contentIndentStr = " " * contentIndent
	for i, cap in enumerate(caps):
		capStrings.append(headerIndentStr + f"{type(cap).__name__}[{i}]:")
		fields = []
		for field, typ in cap._fields_:
			if field == "u1" or field.startswith("Reserved"):
				continue
			val = getattr(cap, field)
			valstr = f"{val:#x}"
			if field.endswith("UsagePage"):
				if val in _HID_USAGE_MAP:
					valstr += f" ({_HID_USAGE_MAP[val][0]})"
			elif field == "LinkUsage":
				page = cap.LinkUsagePage
				if page in _HID_USAGE_MAP:
					usages = _HID_USAGE_MAP[page][1]
					if val in usages:
						valstr += f" ({usages[val]})"
			elif field == "UnitsExp":
				# UnitsExp is a 4-bit signed integer, base-10 exponent
				unitsExp = (val ^ 0x8) - 0x8
				valstr += f" ({unitsExp})"
			elif field == "Units":
				unitsStr = _HIDUnitsToString(val)
				if unitsStr:
					valstr += f" ({unitsStr})"
			elif field.startswith("Physical") and unitsStr:
				valstr = f"{val} ({val * (10**unitsExp)} {unitsStr})"
			else:
				# for other data, still use decimal
				valstr = str(val)
			fields.append(f"{field}: {valstr}")
		u1 = getattr(cap.u1, "Range" if cap.IsRange else "NotRange")
		for field, typ in u1._fields_:
			if field.startswith("Reserved"):
				continue
			val = getattr(u1, field)
			valstr = f"{val:#x}"
			if field == "Usage":
				page = cap.UsagePage
				if page in _HID_USAGE_MAP:
					usages = _HID_USAGE_MAP[page][1]
					if val in usages:
						valstr += f" ({usages[val]})"
			else:
				# for other data, still use decimal
				valstr = str(val)
			fields.append(f"{field}: {valstr}")
		capStrings.append(contentIndentStr + (f"\n{contentIndentStr}".join(fields)))
	return "\n".join(capStrings)


def _getHIDCapsIndexToUsageMap(
	buttonCaps: Array[hid.HIDP_BUTTON_CAPS],
	valueCaps: Array[hid.HIDP_VALUE_CAPS],
) -> dict[int, tuple[int, int, int]]:
	"""
	Build a dict that maps data indexes in HID button & value caps to tuples of (link collection, usage page, usage).
	The dict can then be used to translate data indexes returned from `HidP_GetData` to usages.
	"""
	result = {}
	for caps in buttonCaps, valueCaps:
		for cap in caps:
			if cap.IsRange:
				usage = cap.u1.Range.UsageMin
				index = cap.u1.Range.DataIndexMin
				count = cap.u1.Range.UsageMax - cap.u1.Range.UsageMin + 1
				for i in range(count):
					result[index] = (cap.LinkCollection, cap.UsagePage, usage)
					usage += 1
					index += 1
			else:
				result[cap.u1.NotRange.DataIndex] = (cap.LinkCollection, cap.UsagePage, cap.u1.NotRange.Usage)
	return result


def _HIDDataDictToString(dataDict: dict[tuple[int, int, int], int]) -> str:
	"""Converts an HID data dict (usage to value map) to string, for debugging purposes."""
	strings = []
	for (linkCollection, usagePage, usage), value in dataDict.items():
		usagePageStr = f"{usagePage:#x}"
		usageStr = f"{usage:#x}"
		if usagePage in _HID_USAGE_MAP:
			usagePageName, usages = _HID_USAGE_MAP[usagePage]
			usagePageStr += f" ({usagePageName})"
			if usage in usages:
				usageStr += f" ({usages[usage]})"
		strings.append(
			f"Link collection: {linkCollection}, "
			f"Usage page: {usagePageStr}, "
			f"Usage: {usageStr}, "
			f"Value: {value}",
		)
	return "\n".join(strings)


@dataclasses.dataclass
class _TouchpadContact:
	"""Represents a single contact point."""

	id: int = 0
	x: int = 0
	y: int = 0
	isInContact: bool = False
	isValid: bool = False


@dataclasses.dataclass
class _TouchpadFrame:
	"""Represents a touchpad frame, consisting of multiple contact points."""

	scanTime: int = 0
	isButtonDown: bool = False
	contactCount: int = 0
	contacts: list[_TouchpadContact] = dataclasses.field(default_factory=list)

	def clear(self):
		self.scanTime = 0
		self.isButtonDown = False
		self.contactCount = 0
		self.contacts.clear()


def _isUsage(cap: hid.HIDP_BUTTON_CAPS | hid.HIDP_VALUE_CAPS, usage: int) -> bool:
	"""Check if the specified button/value caps matches the specified usage."""
	if cap.IsRange:
		return cap.u1.Range.UsageMin <= usage <= cap.u1.Range.UsageMax
	else:
		return cap.u1.NotRange.Usage == usage


class _TouchpadDevice:
	"""
	Represents a Windows Precision Touchpad device,
	which is an HID device with usage page = 0x0D and usage = 0x05.

	See also: https://learn.microsoft.com/en-us/windows-hardware/design/component-guidelines/touchpad-windows-precision-touchpad-collection

	The device handle and the preparsed data are assumed not to change
	during the lifetime of this object.
	When receiving `WM_INPUT_DEVICE_CHAGE`,
	existing `_TouchpadDevice` objects should be re-created.
	"""

	def __init__(self, hDevice: int, info: user32.RID_DEVICE_INFO_HID):
		"""
		Initialize the object with a touchpad device handle and a `RID_DEVICE_INFO_HID` structure.
		Device info and preparsed data will be cached.
		"""
		self._handle = hDevice
		self.vendorId: int = info.dwVendorId
		self.productId: int = info.dwProductId
		self.versionNumber: int = info.dwVersionNumber
		# Get preparsed data
		self._prepData = _getPreparsedData(hDevice)
		# Get caps
		caps = hid.HIDP_CAPS()
		_checkHidStatus(hid.HidP_GetCaps(self._prepData, byref(caps)))
		# Get button caps
		num = USHORT(caps.NumberInputButtonCaps)
		buttonCaps = (hid.HIDP_BUTTON_CAPS * caps.NumberInputButtonCaps)()
		_checkHidStatus(
			hid.HidP_GetButtonCaps(
				hid.HIDP_REPORT_TYPE.INPUT,
				buttonCaps,
				byref(num),
				self._prepData,
			),
		)
		# Get value caps
		num = USHORT(caps.NumberInputValueCaps)
		valueCaps = (hid.HIDP_VALUE_CAPS * caps.NumberInputValueCaps)()
		_checkHidStatus(
			hid.HidP_GetValueCaps(
				hid.HIDP_REPORT_TYPE.INPUT,
				valueCaps,
				byref(num),
				self._prepData,
			),
		)
		# Get value ranges and possible link collections from value caps
		self._linkCollections: list[int] = []
		for valueCap in valueCaps:
			if valueCap.UsagePage == HID_USAGE_PAGE_GENERIC:
				if _isUsage(valueCap, HID_USAGE_GENERIC_X):
					self.XMin: int = valueCap.LogicalMin
					self.XMax: int = valueCap.LogicalMax
				elif _isUsage(valueCap, HID_USAGE_GENERIC_Y):
					self.YMin: int = valueCap.LogicalMin
					self.YMax: int = valueCap.LogicalMax
			elif valueCap.UsagePage == HID_USAGE_PAGE_DIGITIZER:
				if _isUsage(valueCap, HID_USAGE_DIGITIZER_CONTACT_IDENTIFIER):
					# Every link collection with contact point info should have a contact ID
					self._linkCollections.append(valueCap.LinkCollection)
		self._linkCollections.sort()
		self._HIDCapsIndexToUsageMap = _getHIDCapsIndexToUsageMap(buttonCaps, valueCaps)
		log.debug(
			f"Initializing touchpad device: {self.getName()}\n"
			f"Vendor ID: {self.vendorId}, "
			f"Product ID: {self.productId}, "
			f"Version = {self.versionNumber}\n"
			f"Button caps: {caps.NumberInputButtonCaps} items\n{_HIDCapsToString(buttonCaps)}\n"
			f"Value caps: {caps.NumberInputValueCaps} items\n{_HIDCapsToString(valueCaps)}"
		)

	def parseHIDReport(self, report: PCHAR, reportLength: int, frame: _TouchpadFrame) -> bool:
		"""
		Parse the specified HID report data with the preparsed data of this device.

		Note that some touchpads may split contact point data across multiple reports,
		so a frame might be unfinished after the first report.
		This function will return `False` when the frame is not finished,
		and the same frame should be passed again when the next report arrives.

		See: https://learn.microsoft.com/en-us/windows-hardware/design/component-guidelines/touchpad-buttons-report-level-usages

		:param report: Pointer to current report data.
		:param reportLength: Length, in bytes, of the report data.
		:param frame: If the previous frame isn't finished, pass in the previous frame.
			Otherwise, pass in a new, empty frame. The frame will be filled with data on return.
		:returns: `True` if the frame is completed, and can be used for further processing.
			`False` if the frame is not yet finished, and should be passed in again with the next report.
		"""
		# Get all HID buttons (that is currently ON) & values in a list
		dataCount = ULONG(0)
		ntstat = hid.HidP_GetData(
			hid.HIDP_REPORT_TYPE.INPUT,
			None,
			byref(dataCount),
			self._prepData,
			report,
			reportLength,
		)
		if ntstat != HIDP_STATUS_BUFFER_TOO_SMALL:
			_checkHidStatus(ntstat)
		dataList = (hid.HIDP_DATA * dataCount.value)()
		_checkHidStatus(
			hid.HidP_GetData(
				hid.HIDP_REPORT_TYPE.INPUT,
				dataList,
				byref(dataCount),
				self._prepData,
				report,
				reportLength,
			),
		)
		# Convert data list to a usage to value map, since we care more about usages
		# Tuple members, in order, are: link collection, usage page, usage
		dataDict: dict[tuple[int, int, int], int] = {
			self._HIDCapsIndexToUsageMap[item.DataIndex]: item.u1.RawValue for item in dataList
		}
		# Sub reports of the same frame should have the same scan time of the first report.
		scanTime = dataDict[0, HID_USAGE_PAGE_DIGITIZER, HID_USAGE_DIGITIZER_SCAN_TIME]
		if frame.contactCount > 0 and frame.scanTime != scanTime:
			log.debugWarning("Touchpad frame dropped due to unmatched scan time")
			frame.clear()
		frame.scanTime = scanTime
		# The first report contains the total contact count.
		# Subsequent sub reports of the same frame have a contact count of zero.
		contactCount = dataDict[0, HID_USAGE_PAGE_DIGITIZER, HID_USAGE_DIGITIZER_CONTACT_COUNT]
		if contactCount > 0:
			frame.contactCount = contactCount
		frame.isButtonDown = (0, HID_USAGE_PAGE_BUTTON, 0x01) in dataDict
		for linkCollection in self._linkCollections:
			contact = _TouchpadContact()
			contact.id = dataDict[
				linkCollection, HID_USAGE_PAGE_DIGITIZER, HID_USAGE_DIGITIZER_CONTACT_IDENTIFIER
			]
			contact.x = dataDict[linkCollection, HID_USAGE_PAGE_GENERIC, HID_USAGE_GENERIC_X]
			contact.y = dataDict[linkCollection, HID_USAGE_PAGE_GENERIC, HID_USAGE_GENERIC_Y]
			contact.isInContact = (
				linkCollection,
				HID_USAGE_PAGE_DIGITIZER,
				HID_USAGE_DIGITIZER_TIP_SWITCH,
			) in dataDict
			contact.isValid = (
				linkCollection,
				HID_USAGE_PAGE_DIGITIZER,
				HID_USAGE_DIGITIZER_TOUCH_VALID,
			) in dataDict
			frame.contacts.append(contact)
			if len(frame.contacts) >= frame.contactCount:
				return True  # This frame is complete.
		# This frame is not complete, and further reports are needed to complete this frame.
		return False

	def getName(self) -> str:
		"""Gets the device interface name of the specified device."""
		cchName = UINT(0)
		user32.GetRawInputDeviceInfo(
			self._handle,
			RIDI_DEVICENAME,
			None,
			byref(cchName),
		)
		if cchName.value == 0:
			raise WinError()
		devName = create_unicode_buffer(cchName.value)
		if (
			user32.GetRawInputDeviceInfo(
				self._handle,
				RIDI_DEVICENAME,
				devName,
				byref(cchName),
			)
			== UINT_MAX
		):
			raise WinError()
		return devName.value


def _getTouchpadDevices() -> dict[int, _TouchpadDevice]:
	"""
	Returns all detected touchpad devices in a dict,
	whose keys are device handles and values are _TouchpadDevice objects.
	"""
	numDev = UINT(0)
	cbSize = sizeof(user32.RAWINPUTDEVICELIST)
	user32.GetRawInputDeviceList(None, byref(numDev), cbSize)
	if numDev.value == 0:
		return {}
	devList = (user32.RAWINPUTDEVICELIST * numDev.value)()
	if user32.GetRawInputDeviceList(devList, byref(numDev), cbSize) == UINT_MAX:
		return {}
	result = {}
	for dev in devList:
		if dev.dwType != RIM_TYPEHID:
			continue
		devInfo = user32.RID_DEVICE_INFO()
		devInfo.cbSize = sizeof(devInfo)
		cbSize = UINT(sizeof(devInfo))
		if (
			user32.GetRawInputDeviceInfo(
				dev.hDevice,
				RIDI_DEVICEINFO,
				byref(devInfo),
				byref(cbSize),
			)
			== UINT_MAX
		):
			continue
		hidInfo = devInfo.info.hid
		if not (
			hidInfo.usUsagePage == HID_USAGE_PAGE_DIGITIZER
			and hidInfo.usUsage == HID_USAGE_DIGITIZER_TOUCH_PAD
		):
			continue
		result[dev.hDevice] = _TouchpadDevice(dev.hDevice, hidInfo)
	return result


class TouchpadHandler(threading.Thread):
	def __init__(self):
		self.enabled: bool = config.conf["touchpad"]["enabled"]
		self.touchpadTouching: bool = False
		self._touchpadDevices = _getTouchpadDevices()
		self._touchpadFrame = _TouchpadFrame()
		self._currentContactIDs: set[int] = set()
		self.pendingEmitsTimer = gui.NonReEntrantTimer(core.requestPump)
		super().__init__(name=f"{self.__class__.__module__}.{self.__class__.__qualname__}")
		self._curTouchMode = "object"
		self.initializedEvent = threading.Event()
		self.threadExc = None
		self.start()
		self.initializedEvent.wait()
		if self.threadExc:
			raise self.threadExc

	def terminate(self):
		user32.PostThreadMessage(self.ident, WM_QUIT, 0, 0)
		self.join()
		self.pendingEmitsTimer.Stop()

	def run(self):
		try:
			self._appInstance = winBindings.kernel32.GetModuleHandle(None)
			self._cTouchpadRawInputWindowProc = user32.WNDPROC(self.touchpadRawInputWndProc)
			self._wc = user32.WNDCLASSEXW(
				cbSize=sizeof(user32.WNDCLASSEXW),
				lpfnWndProc=self._cTouchpadRawInputWindowProc,
				hInstance=self._appInstance,
				lpszClassName="touchpadRawInputWindowClass",
			)
			self._wca = user32.RegisterClassEx(byref(self._wc))
			self._touchpadWindow = user32.CreateWindowEx(
				0,
				cast(self._wca, LPCWSTR),
				"NVDA touchpad input",
				0,
				0,
				0,
				0,
				0,
				HWND_MESSAGE,
				None,
				self._appInstance,
				None,
			)
			# Register raw input to receive WM_INPUT and WM_INPUT_DEVICE_CHANGE
			rawInputDev = user32.RAWINPUTDEVICE()
			rawInputDev.usUsagePage = HID_USAGE_PAGE_DIGITIZER
			rawInputDev.usUsage = HID_USAGE_DIGITIZER_TOUCH_PAD
			rawInputDev.dwFlags = RIDEV_INPUTSINK | RIDEV_DEVNOTIFY
			rawInputDev.hwndTarget = self._touchpadWindow
			user32.RegisterRawInputDevices(byref(rawInputDev), 1, sizeof(rawInputDev))
			self.trackerManager = touchTracker.TrackerManager()
			self.screenExplorer = screenExplorer.ScreenExplorer()
			self.screenExplorer.updateReview = True
		except Exception as e:
			self.threadExc = e
		finally:
			self.initializedEvent.set()
		msg = MSG()
		while user32.GetMessage(byref(msg), None, 0, 0):
			user32.TranslateMessage(byref(msg))
			user32.DispatchMessage(byref(msg))
		# Unregister raw input
		rawInputDev = user32.RAWINPUTDEVICE()
		rawInputDev.usUsagePage = HID_USAGE_PAGE_DIGITIZER
		rawInputDev.usUsage = HID_USAGE_DIGITIZER_TOUCH_PAD
		rawInputDev.dwFlags = RIDEV_REMOVE
		user32.RegisterRawInputDevices(byref(rawInputDev), 1, sizeof(rawInputDev))
		user32.DestroyWindow(self._touchpadWindow)
		# The class atom should be stored as the low word of the class name string pointer.
		user32.UnregisterClass(cast(c_void_p(self._wca), LPCWSTR), self._appInstance)

	def touchpadRawInputWndProc(self, hwnd: int, msg: int, wParam: int, lParam: int) -> int:
		try:
			if msg == WM_INPUT_DEVICE_CHANGE:
				# Refresh touchpad device list
				self._touchpadDevices = _getTouchpadDevices()
				return 0
			if msg != WM_INPUT:
				return user32.DefWindowProc(hwnd, msg, wParam, lParam)
			if not self.enabled:
				return 0
			# WM_INPUT: wParam = RIM_INPUT or RIM_INPUTSINK; lParam = HRAWINPUT
			inputData = _getRawInputData(lParam)
			rawInput = cast(inputData, POINTER(user32.RAWINPUT)).contents
			if rawInput.header.dwType != RIM_TYPEHID:
				return 0
			if rawInput.header.hDevice not in self._touchpadDevices:
				return 0
			touchpad = self._touchpadDevices[rawInput.header.hDevice]
			hidData: user32.RAWHID = rawInput.data.hid
			pData = cast(hidData.bRawData, c_void_p)
			# Handle each reports
			for i in range(hidData.dwCount):
				frameCompleted = touchpad.parseHIDReport(
					cast(pData, PCHAR), hidData.dwSizeHid, self._touchpadFrame
				)
				pData.value += hidData.dwSizeHid
				if frameCompleted:
					self._processFrame()
		except Exception:
			log.error("Error in touchpad window proc", exc_info=True)
		return 0

	def _processFrame(self) -> None:
		"""Process the current finished frame, and send it to the tracker manager."""
		for contact in self._touchpadFrame.contacts:
			if contact.isValid:
				if contact.isInContact:
					self._currentContactIDs.add(contact.id)
				else:
					self._currentContactIDs.remove(contact.id)
				self.trackerManager.update(
					contact.id,
					contact.x,
					contact.y,
					complete=not contact.isInContact,
				)
			else:
				if contact.id in self._currentContactIDs:
					self._currentContactIDs.remove(contact.id)
					self.trackerManager.update(
						contact.id,
						contact.x,
						contact.y,
						complete=True,
					)
		self.touchpadTouching = self.enabled and self._currentContactIDs
		core.requestPump()
		self._touchpadFrame.clear()

	def setMode(self, mode):
		if mode not in availableTouchModes:
			raise ValueError("Unknown mode %s" % mode)
		self._curTouchMode = mode

	def pump(self):
		for preheldTracker, tracker in self.trackerManager.emitTrackers():
			gesture = TouchpadInputGesture(preheldTracker, tracker, self._curTouchMode)
			try:
				inputCore.manager.executeGesture(gesture)
			except inputCore.NoInputGestureAction:
				pass
		interval = self.trackerManager.pendingEmitInterval
		if interval and interval > 0:
			# Ensure we are pumped again by the time more pending multiTouch trackers are ready
			self.pendingEmitsTimer.Start(int(interval * 1000), True)
		else:
			# Stop the timer in case we were pumpped due to something unrelated but just happened to be at the appropriate time to clear any remaining trackers
			self.pendingEmitsTimer.Stop()


handler = None


def handlePostConfigProfileSwitch():
	handler.enabled = config.conf["touchpad"]["enabled"]


def initialize():
	global handler
	# Unlike the TouchHandler,
	# which disables itself when touchscreen is not supported until NVDA restarts,
	# TouchpadHandler always runs in the background,
	# since it is possible to enable/connect a touchpad device while NVDA is running.
	handler = TouchpadHandler()
	config.post_configProfileSwitch.register(handlePostConfigProfileSwitch)


def terminate():
	global handler
	config.post_configProfileSwitch.unregister(handlePostConfigProfileSwitch)
	if handler:
		handler.terminate()
		handler = None
