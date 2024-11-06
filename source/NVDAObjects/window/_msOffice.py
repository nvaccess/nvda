# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from enum import IntEnum


class MsoHyperlink(IntEnum):
	"""Enumeration of hyperlink types in the Microsoft Office object model.
	See https://learn.microsoft.com/en-us/office/vba/api/office.msohyperlinktype
	"""

	RANGE = 0
	SHAPE = 1
	INLINE_SHAPE = 2
