# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Structs, constants and macros from CommCtrl.h."""

from ctypes import POINTER, Structure, c_int
from ctypes.wintypes import LPARAM, LPWSTR, POINT, PUINT, UINT
from enum import IntEnum

from .user32 import NMHDR


class LVM(IntEnum):
	"""List-view control window messages."""

	SETITEMSTATE = 0x102B
	"""https://learn.microsoft.com/en-us/windows/win32/controls/lvm-setitemstate"""
	SETITEM = 0x104C


class LVIS(IntEnum):
	"""https://learn.microsoft.com/en-us/windows/win32/controls/list-view-item-states"""

	STATEIMAGEMASK = 0xF000


class LVIF(IntEnum):
	STATE = 0x8


class LVITEM(Structure):
	"""https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-lvitemw"""

	_fields_ = (
		("mask", UINT),
		("iItem", c_int),
		("iSubItem", c_int),
		("state", UINT),
		("stateMask", UINT),
		("pszText", LPWSTR),
		("cchTextMax", c_int),
		("iImage", c_int),
		("lParam", LPARAM),
		("iIndent", c_int),
		("iGroupId", c_int),
		("cColumns", UINT),
		("puColumns", PUINT),
		("piColFmt", POINTER(c_int)),
		("iGroup", c_int),
	)


def INDEXTOSTATEIMAGEMASK(i: int) -> int:
	"""https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-indextostateimagemask"""
	return i << 12


class NMLISTVIEW(Structure):
	_fields_ = (
		("hdr", NMHDR),
		("iItem", c_int),
		("iSubItem;", c_int),
		("uNewState", UINT),
		("uOldState", UINT),
		("uChanged", UINT),
		("ptAction", POINT),
		("lParam", LPARAM),
	)
