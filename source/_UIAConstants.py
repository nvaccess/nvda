# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import enum


class FillType(enum.IntEnum):
	NONE = 0
	COLOR = 1
	GRADIENT = 2
	PICTURE = 3
	PATTERN = 4


FillTypeLabels = {
	# Translators: a style of fill type (to color the inside of a control or text)
	FillType.NONE: pgettext("UIAHandler.FillType", "none"),
	# Translators: a style of fill type (to color the inside of a control or text)
	FillType.COLOR: pgettext("UIAHandler.FillType", "color"),
	# Translators: a style of fill type (to color the inside of a control or text)
	FillType.GRADIENT: pgettext("UIAHandler.FillType", "gradient"),
	# Translators: a style of fill type (to color the inside of a control or text)
	FillType.PICTURE: pgettext("UIAHandler.FillType", "picture"),
	# Translators: a style of fill type (to color the inside of a control or text)
	FillType.PATTERN: pgettext("UIAHandler.FillType", "pattern"),
}


# Some newer UIA constants that could be missing
class UIAutomationType(enum.IntEnum):
	INT = 1
	BOOL = 2
	STRING = 3
	DOUBLE = 4
	POINT = 5
	RECT = 6
	ELEMENT = 7
	ARRAY = 8
	OUT = 9
	INT_ARRAY = 10
	BOOL_ARRAY = 11
	STRING_ARRAY = 12
	DOUBLE_ARRAY = 13
	POINT_ARRAY = 14
	RECT_ARRAY = 15
	ELEMENT_ARRAY = 16
	OUT_INT = 17
	OUT_BOOL = 18
	OUT_STRING = 19
	OUT_DOUBLE = 20
	OUT_POINT = 21
	OUT_RECT = 22
	OUT_ELEMENT = 23
	OUT_INT_ARRAY = 24
	OUT_BOOL_ARRAY = 25
	OUT_STRING_ARRAY = 26
	OUT_DOUBLE_ARRAY = 27
	OUT_POINT_ARRAY = 28
	OUT_RECT_ARRAY = 29
	OUT_ELEMENT_ARRAY = 30


class WinConsoleAPILevel(enum.IntEnum):
	"""
	Defines actively used Windows Console versions and the levels of custom code required
	for each.
	"""
	# Represents a console before microsoft/terminal#4018 was merged.
	# These consoles do not support UIA word navigation and require a number
	# of text range workarounds.
	END_INCLUSIVE = 0
	# Represents a console with microsoft/terminal#4018, but without
	# resolution of microsoft/terminal#2161 (text formatting)
	# or microsoft/terminal#6986 (extraneous empty lines).
	# This is a significant improvement over END_INCLUSIVE, so fewer workarounds
	# are required. However, these consoles lack some information
	# (such as text formatting) and require bounding, so are unsuitable for
	# usage by default.
	IMPROVED = 1
	# Represents an IMPROVED console that exposes text formatting and a
	# buffer that does not contain extraneous empty lines.
	FORMATTED = 2
