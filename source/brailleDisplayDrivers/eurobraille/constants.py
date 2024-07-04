# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2023 NV Access Limited, Babbage B.V., Eurobraille

from typing import OrderedDict, Dict

name = "eurobraille"
# Translators: Names of braille displays.
description = _("Eurobraille displays")

BAUD_RATE: int = 9600

STX = b"\x02"
ETX = b"\x03"
ACK = b"\x06"
EB_SYSTEM = b"S"  # 0x53
EB_MODE = b"R"  # 0x52
EB_KEY = b"K"  # 0x4b
EB_BRAILLE_DISPLAY = b"B"  # 0x42
EB_KEY_INTERACTIVE = b"I"  # 0x49
EB_KEY_INTERACTIVE_SINGLE_CLICK = b"\x01"
EB_KEY_INTERACTIVE_REPETITION = b"\x02"
EB_KEY_INTERACTIVE_DOUBLE_CLICK = b"\x03"
EB_KEY_BRAILLE = b"B"  # 0x42
EB_KEY_COMMAND = b"C"  # 0x43
EB_KEY_QWERTY = b"Z"  # 0x5a
EB_KEY_USB_HID_MODE = b"U"  # 0x55
EB_BRAILLE_DISPLAY_STATIC = b"S"  # 0x53
EB_SYSTEM_IDENTITY = b"I"  # 0x49
EB_SYSTEM_DISPLAY_LENGTH = b"G"  # 0x47
EB_SYSTEM_TYPE = b"T"  # 0x54
EB_SYSTEM_PROTOCOL = b"P"  # 0x50
EB_SYSTEM_FRAME_LENGTH = b"M"  # 0x4d
EB_ENCRYPTION_KEY = b"Z"  # 0x5a
EB_MODE_DRIVER = b"P"  # 0x50
EB_MODE_INTERNAL = b"I"  # 0x49
EB_MODE_MENU = b"M"  # 0x4d
EB_IRIS_TEST = b"T"  # 0x54
EB_IRIS_TEST_sub = b"L"  # 0x4c
EB_VISU = b"V"  # 0x56
EB_VISU_DOT = b"D"  # 0x44
EB_CONNECTION_NAME = b"n"

# The eurobraille protocol uses real number characters as boolean values, so 0 (0x30) and 1 (0x31)
EB_FALSE = b"0"  # 0x30
EB_TRUE = b"1"  # 0x31

KEYS_STICK: Dict[int, str] = OrderedDict(
	{
		0x10000: "joystick1Up",
		0x20000: "joystick1Down",
		0x40000: "joystick1Right",
		0x80000: "joystick1Left",
		0x100000: "joystick1Center",
		0x1000000: "joystick2Up",
		0x2000000: "joystick2Down",
		0x4000000: "joystick2Right",
		0x8000000: "joystick2Left",
		0x10000000: "joystick2Center",
	},
)
KEYS_ESYS: Dict[int, str] = OrderedDict(
	{
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
	},
)
KEYS_ESYS.update(KEYS_STICK)
KEYS_IRIS: Dict[int, str] = OrderedDict(
	{
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
	},
)

KEYS_ESITIME: Dict[int, str] = OrderedDict(
	{
		0x01: "l1",
		0x02: "l2",
		0x04: "l3",
		0x08: "l4",
		0x10: "l5",
		0x20: "l6",
		0x40: "l7",
		0x80: "l8",
	},
)
KEYS_ESITIME.update(KEYS_STICK)

KEYS_BNOTE = KEYS_ESYS
KEYS_BBOOK = KEYS_ESITIME

DEVICE_TYPES: Dict[int, str] = {
	0x01: "Iris 20",
	0x02: "Iris 40",
	0x03: "Iris S20",
	0x04: "Iris S32",
	0x05: "Iris KB20",
	0x06: "IrisKB 40",
	0x07: "Esys 12",
	0x08: "Esys 40",
	0x09: "Esys Light 40",
	0x0A: "Esys 24",
	0x0B: "Esys 64",
	0x0C: "Esys 80",
	# 0x0d:"Esys", reserved in protocol
	0x0E: "Esytime 32",
	0x0F: "Esytime 32 standard",
	0x10: "Esytime evo 32",
	0x11: "Esytime evo 32 standard",
	0x12: "bnote",
	0x13: "bnote 2",
	0x14: "bbook",
	0x15: "bbook 2",
}
