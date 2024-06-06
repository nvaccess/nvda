# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited, Burman's Computer and Education Ltd.

"""Constants for Tivomatic Caiku Albatross 46 and 80 display driver.

Summary of important constants:

- L{INIT_STARTBYTE} and L{MAX_SETTINGS_BYTE}; when there is no connection,
the display continuously sends L{INIT_START_BYTE} followed by the settings byte.
The number of these packets is arbitrary. L{INIT_START_BYTE} is \xff.
Settings byte can be from \x00 to \xff.
It is limited to be at most L{MAX_SETTINGS_BYTE} to reliably detect init packets.

- L{ESTABLISHED}; driver sends this to confirm connection, and
display stops sending init packets

- all data to show on display has to be enclosed with L{START_BYTE} and
L{END_BYTE}

- L{BOTH_BYTES} is used to keep connection; display falls back to
"wait for connection state" if it does not get appropriate data packet
within approximately 2 seconds. L{KC_INTERVAL} defines suitable time which
in turn is used by timer.

- part of display buttons L{Keys} are control keys used to compose key
combinations. See also L{CONTROL_KEY_CODES}.

- L{LEFT_RIGHT_KEY_CODES} is used when handling custom key layouts.

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
	Dict,
	FrozenSet,
	Tuple,
)

BAUD_RATE: Tuple[int] = (19200, 9600)
"""Possible baud rates.
Because 19200 is the display default, it is tried at first.
"""

READ_TIMEOUT = 0.2
WRITE_TIMEOUT = 0.2
SLEEP_TIMEOUT = 0.2
"""How long to sleep when port cannot be opened or I/O buffers reset fails."""

MAX_INIT_RETRIES = 20
"""
How many times port initialization or opening is tried.
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


class Keys(IntEnum):
	"""Defines key names and values.
	For routing keys see L{RoutingKeyRange}.
	"""
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
	f15 = 199
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

CONTROL_KEY_CODES: FrozenSet[Keys] = frozenset(
	{
		Keys.attribute1,
		Keys.attribute2,
		Keys.f1,
		Keys.f2,
		Keys.f7,
		Keys.f8,
		Keys.home1,
		Keys.end1,
		Keys.eCursor1,
		Keys.cursor1,
		Keys.attribute3,
		Keys.attribute4,
		Keys.f9,
		Keys.f10,
		Keys.f15,
		Keys.f16,
		Keys.home2,
		Keys.end2,
		Keys.eCursor2,
		Keys.cursor2,
	}
)
"""Ctrl keys which may start key combination."""

LEFT_RIGHT_KEY_CODES: Dict[Keys, Keys] = {
	Keys.attribute1: Keys.attribute3,
	Keys.attribute2: Keys.attribute4,
	Keys.f1: Keys.f9,
	Keys.f2: Keys.f10,
	Keys.f3: Keys.f11,
	Keys.f4: Keys.f12,
	Keys.f5: Keys.f13,
	Keys.f6: Keys.f14,
	Keys.f7: Keys.f15,
	Keys.f8: Keys.f16,
	Keys.home1: Keys.home2,
	Keys.end1: Keys.end2,
	Keys.eCursor1: Keys.eCursor2,
	Keys.cursor1: Keys.cursor2,
	Keys.up1: Keys.up3,
	Keys.down1: Keys.down2,
	Keys.lWheelRight: Keys.rWheelRight,
	Keys.lWheelLeft: Keys.rWheelLeft,
	Keys.lWheelUp: Keys.rWheelUp,
	Keys.lWheelDown: Keys.rWheelDown,
}
"""Connects corresponding left and right side keys.
Dictionary keys are left side keys values, and dictionary values are
corresponding right side keys values. Used with custom key layouts.
"""

KEY_LAYOUT_MASK = 5
"""Used to extract bits 1 - 3 from settings byte to determine key layout.
See L{KeyLayout}.
"""


class KeyLayout(IntEnum):
	"""Defines possible key layouts.
	From settings byte bits 1 - 3 (MSB 0 scheme) are extracted and bit 2 is
	set to 0 (it represents side of status cells which NVDA does not use).
	The result is then compared with variables below to determine what key
	layout should be used.

	Switching layout does not affect on Left, right, down3, up2, routing and
	secondRouting keys. Up2 and down3 are also ignored because they are in the
	middle of the front panel of 80 model so they do not logically belong to
	left or right side.

	See also L{KEY_LAYOUT_MASK}.
	"""
	normal = 0
	bothSidesAsRight = 1
	switched = 4
	bothSidesAsLeft = 5


@dataclass(frozen=True)
class RoutingKeyRange:
	"""Defines structure of items in L{ROUTING_KEY_RANGES}.
	Albatross has both routing and secondRouting key rows so L{name} is "routing"
	or "secondRouting". Due to hardware design there are 4 address ranges: 2
	for each rows which means 4 L{start} L{end} pairs. There are also 4
	L{indexOffset} which are used to get real button index on the row.
	See also L{ROUTING_KEY_RANGES}.
	"""
	name: str
	start: int
	end: int
	indexOffset: int


ROUTING_KEY_RANGES: FrozenSet[RoutingKeyRange] = frozenset(
	{
		RoutingKeyRange("routing", 2, 41, indexOffset=2),
		RoutingKeyRange("secondRouting", 43, 82, indexOffset=43),
		RoutingKeyRange("routing", 111, 150, indexOffset=71),
		RoutingKeyRange("secondRouting", 152, 191, indexOffset=112)
	}
)
"""Defines routing key ranges. See L{RoutingKeyRange}."""

ESTABLISHED = b"\xfe\xfd"
"""Send this to Albatross to confirm that connection is established."""

INIT_START_BYTE = b"\xff"
"""Starts every init packet.
If no connection, Albatross sends continuously byte \xff followed by byte
containing various settings like number of cells.
"""

MAX_SETTINGS_BYTE = b"\xfe"
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

Settings byte limitation causes maximum number of status cells to be 14
(with \xff 15) in 80 model. Limitation is applied only if other settings
would make settings byte to be \xff. These are very big values (5 could be
normal maximum value), and NVDA does not utilize status cells.

Although settings like number of status cells are adjusted in display
menu, display itself does not use them. They are just notes for screenreaders.
For example, display has no separate status cells. It is screenreader
or driver job to use them when applicable.

Only display settings which affects on its own functionality are baud rate
and key repeat which can be slow or fast.

There are other devices with same PID&VID. When automatic braille display
detection is used, other displays with same PID&VID are tried before Albatross.
Those drivers try to send queries to the port to detect their own displays.
These queries may cause Albatross to send unexpected init packets which in
turn could disturb this driver - it could get inappropriate settings byte.
This is tried to prevent by resetting I/O buffers so that strange packets
would be discarded.

If however, there are still strange init packets, Albatross should be
manually selected from the display list.
"""

MAX_STATUS_CELLS_ALLOWED = 14
"""To inform user how many status cells can be used.
See L{MAX_SETTINGS_BYTE}.
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

BUS_DEVICE_DESC = "Albatross Braille Display"
"""Bus reported device description
"""

VID_AND_PID = "VID_0403&PID_6001"
"""Vid and pid
"""
