# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import enum
import ctypes


class DP_Command(enum.IntEnum):
	REQ_FIRMWARE_VERSION = 0x0000
	RSP_FIRMWARE_VERSION = 0x0001
	REQ_DEVICE_NAME = 0x0100
	RSP_DEVICE_NAME = 0x0101
	REQ_BOARD_INFORMATION = 0x0110
	RSP_BOARD_INFORMATION = 0x0111
	REQ_DISPLAY_LINE = 0x0200
	RSP_DISPLAY_LINE = 0x0201
	NTF_DISPLAY_LINE = 0x0202
	REQ_DISPLAY_CURSOR = 0x0210
	RSP_DISPLAY_CURSOR = 0x0211
	NTF_DISPLAY_CURSOR = 0x0212
	NTF_KEYS_SCROLL = 0x0302
	NTF_KEYS_PERKINS = 0x0312
	NTF_KEYS_ROUTING = 0x0322
	NTF_KEYS_FUNCTION = 0x0332
	NTF_ERROR = 0x9902


class DP_ErrorCode(enum.IntEnum):
	LENGTH = 1
	COMMAND = 2
	CHECKSUM = 3
	PARAMETER = 4
	TIMEOUT = 5


class DP_DisplayResponse(enum.IntEnum):
	ACK = 0
	NACK = 1
	WAIT = 2
	CHECKSUM = 3


class DP_Features(enum.IntFlag):
	HAS_GRAPHIC_DISPLAY = 0x80
	HAS_TEXT_DISPLAY = 0x40
	HAS_PERKINS_KEYS = 0x20
	HAS_ROUTING_KEYS = 0x10
	HAS_NAVIGATION_KEYS = 0x08
	HAS_PANNING_KEYS = 0x04
	HAS_FUNCTION_KEYS = 0x02


class DP_DisplayDescriptor(ctypes.Structure):
	_fields_ = [
		("rowCount", ctypes.c_ubyte),
		("columnCount", ctypes.c_ubyte),
		("dividedLine", ctypes.c_ubyte),
		("refreshTime", ctypes.c_ubyte),
	]


class DP_BoardInformation(ctypes.Structure):
	_fields_ = [
		("features", ctypes.c_ubyte),
		("dotsPerCell", ctypes.c_ubyte),
		("distanceBetweenPins", ctypes.c_ubyte),
		("functionKeyCount", ctypes.c_ubyte),
		("text", DP_DisplayDescriptor),
		("graphic", DP_DisplayDescriptor),
	]


class DP_PacketSeqFlag(enum.IntEnum):
	SEQ_TEXT = 0x80


class DP_PacketSyncByte(enum.IntEnum):
	SYNC1 = 0xAA
	SYNC2 = 0x55


class DP_PerkinsKey(enum.IntEnum):
	DOT7 = 0
	DOT3 = 1
	DOT2 = 2
	DOT1 = 3
	DOT4 = 4
	DOT5 = 5
	DOT6 = 6
	DOT8 = 7
	SPACE = 8
	SHIFT_LEFT = 9
	CONTROL_LEFT = 10
	SHIFT_RIGHT = 11
	CONTROL_RIGHT = 12
	PAN_LEFT = 13
	PAN_RIGHT = 14
	NAV_CENTER = 16
	NAV_UP = 17
	NAV_RIGHT = 18
	NAV_DOWN = 19
	NAV_LEFT = 20


DP_CHECKSUM_BASE = 0xA5
