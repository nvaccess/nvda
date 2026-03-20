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
	"""List-view control window messages.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/controls/bumper-list-view-control-reference-messages
	"""

	SETITEMSTATE = 0x102B
	"""Changes the state of an item in a list-view control.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/controls/lvm-setitemstate
	"""


class LVN(IntEnum):
	"""List-view control notification messages.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/controls/bumper-list-view-control-reference-notifications
	"""

	ITEMCHANGING = 0xFFFFFF9C
	"""Notifies a list-view control's parent window that an item is changing.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/controls/lvn-itemchanging
	"""


class LVIS(IntEnum):
	"""Flags and masks which determine a list item's  appearance and functionality.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/controls/list-view-item-states
	"""

	STATEIMAGEMASK = 0xF000
	"""Mask that can be used to isolate the one-based index of the state image."""


class LVIF(IntEnum):
	"""Flags that specify which members of an :class:`LVITEM` are being set or requested.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-lvitemw
	"""

	STATE = 0x8
	"""The state member is valid or must be set."""


class LVITEM(Structure):
	"""Specifies or receives the attributes of a list-view item.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-lvitemw
	"""

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


class NMLISTVIEW(Structure):
	"""Contains information about a list-view notification message.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/commctrl/ns-commctrl-nmlistview
	"""

	_fields_ = (
		("hdr", NMHDR),
		("iItem", c_int),
		("iSubItem", c_int),
		("uNewState", UINT),
		("uOldState", UINT),
		("uChanged", UINT),
		("ptAction", POINT),
		("lParam", LPARAM),
	)
