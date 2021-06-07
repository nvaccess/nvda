# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited

"""
Required types and defines from Windows SDK's hidpi.h
(Public Interface to the Windows HID parsing library).
"""

import enum
from ctypes import Structure, Union, c_byte
from ctypes.wintypes import USHORT, BOOLEAN, ULONG, LONG


FACILITY_HID_ERROR_CODE = 0x11


def HIDP_ERROR_CODES(sev, code):
	return (sev << 28) | (FACILITY_HID_ERROR_CODE << 16) | code


class HIDP_STATUS(enum.IntEnum):
	SUCCESS = HIDP_ERROR_CODES(0x0, 0)
	NULL = HIDP_ERROR_CODES(0x8, 1)
	INVALID_PREPARSED_DATA = HIDP_ERROR_CODES(0xC, 1)
	INVALID_REPORT_TYPE = HIDP_ERROR_CODES(0xC, 2)
	INVALID_REPORT_LENGTH = HIDP_ERROR_CODES(0xC, 3)
	USAGE_NOT_FOUND = HIDP_ERROR_CODES(0xC, 4)
	VALUE_OUT_OF_RANGE = HIDP_ERROR_CODES(0xC, 5)
	BAD_LOG_PHY_VALUES = HIDP_ERROR_CODES(0xC, 6)
	BUFFER_TOO_SMALL = HIDP_ERROR_CODES(0xC, 7)
	INTERNAL_ERROR = HIDP_ERROR_CODES(0xC, 8)
	I8042_TRANS_UNKNOWN = HIDP_ERROR_CODES(0xC, 9)
	INCOMPATIBLE_REPORT_ID = HIDP_ERROR_CODES(0xC, 0xA)
	NOT_VALUE_ARRAY = HIDP_ERROR_CODES(0xC, 0xB)
	IS_VALUE_ARRAY = HIDP_ERROR_CODES(0xC, 0xC)
	DATA_INDEX_NOT_FOUND = HIDP_ERROR_CODES(0xC, 0xD)
	DATA_INDEX_OUT_OF_RANGE = HIDP_ERROR_CODES(0xC, 0xE)
	BUTTON_NOT_PRESSED = HIDP_ERROR_CODES(0xC, 0xF)
	REPORT_DOES_NOT_EXIST = HIDP_ERROR_CODES(0xC, 0x10)
	NOT_IMPLEMENTED = HIDP_ERROR_CODES(0xC, 0x20)


NTSTATUS = ULONG
USAGE = USHORT
UCHAR = c_byte


class HIDP_REPORT_TYPE(enum.IntEnum):
	INPUT = 0
	OUTPUT = 1
	FEATURE = 2


class _HIDP_DATA_U1(Union):
	_fields_ = [
		('RawValue', ULONG),
		('On', BOOLEAN),
	]


class HIDP_DATA(Structure):
	_fields_ = [
		('DataIndex', USHORT),
		('Reserved', USHORT),
		('u1', _HIDP_DATA_U1),
	]


class _HIDP_VALUE_CAPS_U1_RANGE(Structure):
	_fields_ = [
		('UsageMin', USAGE),
		('UsageMax', USAGE),
		('StringMin', USHORT),
		('StringMax', USHORT),
		('DesignatorMin', USHORT),
		('DesignatorMax', USHORT),
		('DataIndexMin', USHORT),
		('DataIndexMax', USHORT),
	]


class _HIDP_VALUE_CAPS_U1_NOT_RANGE(Structure):
	_fields_ = [
		('Usage', USAGE),
		('Reserved1', USAGE),
		('StringIndex', USHORT),
		('Reserved2', USHORT),
		('DesignatorIndex', USHORT),
		('Reserved3', USHORT),
		('DataIndex', USHORT),
		('Reserved4', USHORT),
	]


class _HIDP_VALUE_CAPS_U1(Union):
	_fields_ = [
		('Range', _HIDP_VALUE_CAPS_U1_RANGE),
		('NotRange', _HIDP_VALUE_CAPS_U1_NOT_RANGE),
	]


class HIDP_VALUE_CAPS(Structure):
	_fields_ = [
		('UsagePage', USAGE),
		('ReportID', UCHAR),
		('IsAlias', BOOLEAN),
		('BitField', USHORT),
		('LinkCollection', USHORT),
		('LinkUsage', USAGE),
		('LinkUsagePage', USAGE),
		('IsRange', BOOLEAN),
		('IsStringRange', BOOLEAN),
		('IsDesignatorRange', BOOLEAN),
		('IsAbsolute', BOOLEAN),
		('HasNull', BOOLEAN),
		('Reserved1', UCHAR),
		('BitSize', USHORT),
		('ReportCount', USHORT),
		('Reserved2', USHORT * 5),
		('UnitsExp', ULONG),
		('Units', ULONG),
		('LogiclMin', LONG),
		('LogicalMax', LONG),
		('PhysicalMin', LONG),
		('PhysicalMax', LONG),
		('u1', _HIDP_VALUE_CAPS_U1),
	]


class HIDP_CAPS (Structure):
	_fields_ = (
		("Usage", USHORT),
		("UsagePage", USHORT),
		("InputReportByteLength", USHORT),
		("OutputReportByteLength", USHORT),
		("FeatureReportByteLength", USHORT),
		("Reserved", USHORT * 17),
		("NumberLinkCollectionNodes", USHORT),
		("NumberInputButtonCaps", USHORT),
		("NumberInputValueCaps", USHORT),
		("NumberInputDataIndices", USHORT),
		("NumberOutputButtonCaps", USHORT),
		("NumberOutputValueCaps", USHORT),
		("NumberOutputDataIndices", USHORT),
		("NumberFeatureButtonCaps", USHORT),
		("NumberFeatureValueCaps", USHORT),
		("NumberFeatureDataIndices", USHORT)
	)
