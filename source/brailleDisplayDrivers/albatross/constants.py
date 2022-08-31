# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited, Burman's Computer and Education Ltd.

"""Constants for Tivomatic Caiku Albatross 46 and 80 display driver."""

from typing import Set

BAUD_RATE = 19200
READ_TIMEOUT = 0.2
WRITE_TIMEOUT = 0
SLEEP_TIMEOUT = 0.2
"""How long to sleep between port init or open retries."""
MAX_INIT_RETRIES = 20
"""How many times port initialization or opening is tried.
It sounds big value but users should appreciate that braille starts.
It should not harm other devices with same PID&VID because this device
is detected as last one.
"""
RESET_COUNT = 10
"""
How many times to try to reset I/O buffers
Maybe due to write operations of other drivers with same PID&VID, device seems
to send init packets it should not. Although reset do not work well,
hopefully at least strange packets would be discarded.
"""
RESET_SLEEP = 0.05
"""How long to sleep between I/O buffer resets."""
WRITE_QUEUE_LENGTH = 20
KEY_NAMES = {
	1: "attribute1",
	42: "attribute2",
	83: "f1",
	84: "f2",
	85: "f3",
	86: "f4",
	87: "f5",
	88: "f6",
	89: "f7",
	90: "f8",
	91: "home1",
	92: "end1",
	93: "eCursor1",
	94: "cursor1",
	95: "up1",
	96: "down1",
	97: "left",
	98: "up2",
	103: "lWheelRight",
	104: "lWheelLeft",
	105: "lWheelUp",
	106: "lWheelDown",
	151: "attribute3",
	192: "attribute4",
	193: "f9",
	194: "f10",
	195: "f11",
	196: "f12",
	197: "f13",
	198: "f14",
	199: "f15",
	200: "f16",
	201: "home2",
	202: "end2",
	203: "eCursor2",
	204: "cursor2",
	205: "up3",
	206: "down2",
	207: "right",
	208: "down3",
	213: "rWheelRight",
	214: "rWheelLeft",
	215: "rWheelUp",
	216: "rWheelDown",
}
MAX_COMBINATION_KEYS = 4
"""Maximum number of keys in key combination."""
# These are ctrl keys which may start key combination.
CONTROL_KEY_CODES: Set[int] = {
	1,  # attribute1
	42,  # attribute2
	83,  # f1
	84,  # f2
	89,  # f7
	90,  # f8
	91,  # home1
	92,  # end1
	93,  # eCursor1
	94,  # cursor1
	151,  # attribute3
	192,  # attribute4
	193,  # f9
	194,  # f10
	199,  # f15
	200,  # f16
	201,  # home2
	202,  # end2
	203,  # eCursor2
	204,  # cursor2
}
ESTABLISHED = b"\xfe\xfd\xfe\xfd"
"""Send this to Albatross to confirm that connection is established."""
INIT_START_BYTE = b"\xff"
"""
If no connection, Albatross sends continuously byte \xff followed by byte
containing various settings like number of cells.
"""
START_BYTE = b"\xfb"
END_BYTE = b"\xfc"
"""Send information to Albatross enclosed by these bytes."""
BOTH_BYTES = b"\xfb\xfc"
"""To keep connected these both above bytes must be sent periodically."""
KC_INTERVAL = 1.5
"""
How often BOTH_BYTES should be sent and reconnection tried
Display requires at least START_BYTE and END_BYTE combination within
approximately 2 seconds from previous appropriate data packet.
Otherwise it falls back to "wait for connection" state. This behavior
is built-in feature of the firmware of device.
"""
