# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited, Burman's Computer and Education Ltd.

"""Constants for Tivomatic Caiku Albatross 46 and 80 display driver.
Classes:
- Key
"""

from enum import IntEnum
from typing import List, Set

BAUD_RATE: List[int] = [19200, 9600]
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


class Key(IntEnum):
	attribute1 = 1
	attribute2 = 2
	f1 = 83
	f2 = 84
	f3 = 85
	f4 = 86
	f5 = 87
	f6 = 88
	f7 = 89
	f8 = 90
	home1 = 91
	end1 = 92
	eCursor1 = 93
	cursor1 = 94
	up1 = 95
	down1 = 96
	left = 97
	up2 = 98
	lWheelRight = 103
	lWheelLeft = 104
	lWheelUp = 105
	lWheelDown = 106
	attribute3 = 151
	attribute4 = 192
	f9 = 193
	f10 = 194
	f11 = 195
	f12 = 196
	f13 = 197
	f14 = 198
	f15 = 199,
	f16 = 200
	home2 = 201
	end2 = 202
	eCursor2 = 203
	cursor2 = 204
	up3 = 205
	down2 = 206
	right = 207
	down3 = 208
	rWheelRight = 213
	rWheelLeft = 214
	rWheelUp = 215
	rWheelDown = 216


MAX_COMBINATION_KEYS = 4
"""Maximum number of keys in key combination."""
# These are ctrl keys which may start key combination.
CONTROL_KEY_CODES: Set[Key] = {
	Key.attribute1,
	Key.attribute2,
	Key.f1,
	Key.f2,
	Key.f7,
	Key.f8,
	Key.home1,
	Key.end1,
	Key.eCursor1,
	Key.cursor1,
	Key.attribute3,
	Key.attribute4,
	Key.f9,
	Key.f10,
	Key.f15,
	Key.f16,
	Key.home2,
	Key.end2,
	Key.eCursor2,
	Key.cursor2,
}
ESTABLISHED = b"\xfe\xfd\xfe\xfd"
"""Send this to Albatross to confirm that connection is established."""
INIT_START_BYTE = b"\xff"
"""
If no connection, Albatross sends continuously byte \xff followed by byte
containing various settings like number of cells.
"""
MAX_SETTINGS_BYTE = b"\xfd"
"""
Settings byte can be anything from \x00 to \xff. However, \xff
would make connection establishment quite complex. In addition,
\xfe seems to disturb other driver with same PID&VID when using
automatic detection. Note however, that when automatic detection
is started, and settings byte is \xfe, other driver may prevent
process to proceed. So this cannot be regarded as a solution.
Settings byte limitation should not cause additional problems although
Albatross settings handling would be implemented in some future version
because this only limits number of status cells to 13 (with \xff 15).
"""
MAX_STATUS_CELLS_ALLOWED = 13
"""Used to inform user how many status cells can be used
(see L{MAX_SETTINGS_BYTE}).
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
