# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited, Burman's Computer and Education Ltd.

"""Constants for Tivomatic Caiku Albatross 46 and 80 display driver.
Classes:
- Key

Summary of important constants:

- L{INIT_STARTBYTE} and L{MAX_SETTINGS_BYTE}; when no connection
display sends continuously L{INIT_START_BYTE} followed by settings byte.
The number of these packets is arbitrary. L{INIT_START_BYTE} is \xff.
Settings byte can be from \x00 to \xff. It is limited to be at most
L{MAX_SETTINGS_BYTE} to reliably detect init packets, and for harm that
value \xfe causes during automatic detection for other driver with
same PID&VID.
- L{ESTABLISHED}; driver sends this to confirm connection, and
display stops sending init packets
- all data to show on display has to be enclosed with L{START_BYTE} and
L{END_BYTE}
- L{BOTH_BYTES} is used to keep connection; display falls back to
"wait for connection state" if it does not get appropriate data packet
within approximately 2 seconds. L{KC_INTERVAL} defines suitable time which
in turn is used by timer.
- part of display buttonss see L{Key} are control keys used to compose
key combinations see L{CONTROL_KEY_CODES}
- L{RESET_COUNT} defines how many times port buffer reset is done before
trying to establish connection.
There are many I/O buffers between device and driver so several
resets are done to ensure all buffers are cleared.
Buffers may contain unexpected packets possibly due to write operations
of other drivers with same PID&VID during automatic detection.
There are also arbitrary number of redundant normal init packets which
can be safely ignored.
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import (
	List,
	Set,
)

BAUD_RATE: List[int] = [19200, 9600]
READ_TIMEOUT = 0.2
WRITE_TIMEOUT = 0
SLEEP_TIMEOUT = 0.2
"""How long to sleep between port init or open retries."""
MAX_INIT_RETRIES = 20

"""How many times port initialization or opening is tried.
This large value is required for braille to start.
This should not effect other devices with the same PID and VID,
because this device is detected as last one.
"""

RESET_COUNT = 10

"""
How many times to try to reset I/O buffers.
Possibly due to write operations of other drivers with same PID&VID,
device appears to send init packets it should not.
Although reset is not ideal, unexpected packets are discarded.
In addition, there are arbitrary number of redundant normal init packets
which can be safely ignored.
"""

RESET_SLEEP = 0.05
"""How long to sleep between I/O buffer resets."""
WRITE_QUEUE_LENGTH = 20


class Key(IntEnum):
	attribute1 = 1
	attribute2 = 42
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
"""Ctrl keys which may start key combination."""


@dataclass(frozen=True)
class RoutingKeyRange:
	name: str
	start: int
	end: int
	indexOffset: int


ROUTING_KEY_RANGES: Set[RoutingKeyRange] = frozenset(
	{
		RoutingKeyRange("routing", 2, 41, indexOffset=2),
		RoutingKeyRange("secondRouting", 43, 82, indexOffset=43),
		RoutingKeyRange("routing", 111, 150, indexOffset=71),
		RoutingKeyRange("secondRouting", 152, 191, indexOffset=112)
	}
)
ESTABLISHED = b"\xfe\xfd\xfe\xfd"
"""Send this to Albatross to confirm that connection is established."""
INIT_START_BYTE = b"\xff"
"""
If no connection, Albatross sends continuously byte \xff followed by byte
containing various settings like number of cells.
"""
MAX_SETTINGS_BYTE = b"\xfd"
"""Maximum value allowed for settings byte.
Settings byte can be anything from \x00 to \xff. However, \xff
would make connection establishment quite complex:

- cannot be sure if the first byte received is L{INIT_START_BYTE} or
settings byte
- if settings byte is not L{INIT_START_BYTE} it is easier
- similarly it is easy to detect if whole init packet is received,
it is possible that the second byte is received during next read operation
- typically there are tens of init packets but the number of packets
varies

In addition, \xfe seems to disturb other driver with same PID&VID when using
automatic detection. It may cause infinite loop in that driver when
it tries to recognize its own displays.

Settings byte limitation should not cause additional problems although
Albatross settings handling would be implemented in some future version
because this only limits number of status cells to 13 (with \xff 15).
These are very big values (5 could be normal maximum value), and NVDA
does not utilize status cells.

Although settings like number of status cells are adjusted in display
menu, display itself does not use them. They are just for screenreaders.
For example, display has no separate status cells. It is screenreader
or driver job to use them when applicable.

Only display settings which affects on its own functionality are baud rate
and key repeat which can be slow or fast.
"""
MAX_STATUS_CELLS_ALLOWED = 13
"""Used to inform user how many status cells can be used
see L{MAX_SETTINGS_BYTE}.
"""
START_BYTE = b"\xfb"
"""Send information to Albatross enclosed by L{START_BYTE} and L{END_BYTE}."""
END_BYTE = b"\xfc"
"""Send information to Albatross enclosed by L{START_BYTE} and L{END_BYTE}."""
BOTH_BYTES = b"\xfb\xfc"
"""To keep connected these both above bytes must be sent periodically."""
KC_INTERVAL = 1.5
"""
How often BOTH_BYTES should be sent and reconnection tried.

Display requires at least L{START_BYTE} and L{END_BYTE} combination within
approximately 2 seconds from previous appropriate data packet.
Otherwise it falls back to "wait for connection" state.
This behavior is built-in feature of the firmware of device.
"""
