# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
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
	Int = 1
	Bool = 2
	String = 3
	Double = 4
	Point = 5
	Rect = 6
	Element = 7
	Array = 8
	Out = 9
	IntArray = 10
	BoolArray = 11
	StringArray = 12
	DoubleArray = 13
	PointArray = 14
	RectArray = 15
	ElementArray = 16
	OutInt = 17
	OutBool = 18
	OutString = 19
	OutDouble = 20
	OutPoint = 21
	OutRect = 22
	OutElement = 23
	OutIntArray = 24
	OutBoolArray = 25
	OutStringArray = 26
	OutDoubleArray = 27
	OutPointArray = 28
	OutRectArray = 29
	OutElementArray = 30
