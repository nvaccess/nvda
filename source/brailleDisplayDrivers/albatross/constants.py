# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited, Burman's Computer and Education Ltd.

from typing import List

BAUD_RATE = 19200
TIMEOUT = 0.2
WRITE_TIMEOUT = 0
# How many times initial connection is waited by sleeping TIMEOUT.
# It sounds big value but users should appreciate that braille starts.
# It should not harm other devices with same PID&VID because this device
# is last one.
MAX_INIT_SLEEPS = 20
# Maybe due to writings of other drivers with same PID&VID, device seems
# to send init packets it should not. Although reset do not work well,
# hopefully at least strange packets would be discarded.
# How many times to try to reset I/O buffers
RESET_COUNT = 10
# How long to sleep between I/O buffer resets
RESET_SLEEP = 0.05
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
# Maximum number of keys in key combination.
MAX_COMBINATION_KEYS = 4
# These are ctrl keys which may start key combination.
CONTROL_KEY_CODES: List[int] = [
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
]
# Send this to Albatross to confirm that connection is established.
ESTABLISHED = b"\xfe\xfd\xfe\xfd"
# If no connection, Albatross sends continuously byte \xff followed by byte
# containing various settings like number of cells.
INIT_START_BYTE = b"\xff"
# Send information to Albatross enclosed by these bytes.
START_BYTE = b"\xfb"
END_BYTE = b"\xfc"
# To keep connected these both above bytes must be sent periodically.
BOTH_BYTES = b"\xfb\xfc"
# Display requires at least START_BYTE and END_BYTE combination within
# approximately 2 seconds from previous appropriate data packet.
# Otherwise it falls back to "wait for connection" state. This behavior
# is built-in feature of the firmware of device.
# How often BOTH_BYTES should be sent and reconnection tried
KC_INTERVAL = 1.5
