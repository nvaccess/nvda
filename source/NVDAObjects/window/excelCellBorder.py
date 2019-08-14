#NVDAObjects/window/excelCellBorder.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016 Takuya Nishimoto
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from collections import OrderedDict
import colors
# XlBordersIndex Enumeration
# see https://msdn.microsoft.com/en-us/library/office/ff835915.aspx
xlDiagonalDown = 5
xlDiagonalUp = 6
xlEdgeBottom = 9
xlEdgeLeft = 7
xlEdgeRight = 10
xlEdgeTop = 8
xlInsideHorizontal = 12
xlInsideVertical = 11
bordersIndexLabels=OrderedDict((
	# Translators: border positions in Microsoft Excel.
	(xlEdgeTop, _("top edge")),
	# Translators: border positions in Microsoft Excel.
	(xlEdgeBottom, _("bottom edge")),
	# Translators: border positions in Microsoft Excel.
	(xlEdgeLeft, _("left edge")),
	# Translators: border positions in Microsoft Excel.
	(xlEdgeRight, _("right edge")),
	# Translators: border positions in Microsoft Excel.
	(xlDiagonalUp, _("up-right diagonal line")),
	# Translators: border positions in Microsoft Excel.
	(xlDiagonalDown, _("down-right diagonal line")),
	# Translators: border positions in Microsoft Excel.
	(xlInsideHorizontal, _("horizontal borders except outside")),
	# Translators: border positions in Microsoft Excel.
	(xlInsideVertical, _("vertical borders except outside")),
))
# XlLineStyle Enumeration
# see https://msdn.microsoft.com/en-us/library/office/ff821622.aspx
xlContinuous = 1
xlDash = -4115
xlDashDot = 4
xlDashDotDot = 5
xlDot = -4118
xlDouble = -4119
xlLineStyleNone = -4142
xlSlantDashDot = 13
borderStyleLabels={
	# Translators: border styles in Microsoft Excel.
	xlContinuous:_("continuous"),
	# Translators: border styles in Microsoft Excel.
	xlDash:_("dashed"),
	# Translators: border styles in Microsoft Excel.
	xlDashDot:_("dash dot"),
	# Translators: border styles in Microsoft Excel.
	xlDashDotDot:_("dash dot dot"),
	# Translators: border styles in Microsoft Excel.
	xlDot:_("dotted"),
	# Translators: border styles in Microsoft Excel.
	xlDouble:_("double"),
	# Translators: border styles in Microsoft Excel.
	xlSlantDashDot:_("slanted dash dot"),
}
# XlBorderWeight Enumeration
# see https://msdn.microsoft.com/en-us/library/office/ff197515.aspx
xlHairline = 1 # thinnest border
xlThin = 2
xlMedium = -4138
xlThick = 4 # widest border
borderWeightLabels={
	# Translators: border styles in Microsoft Excel.
	xlHairline:_("hair"),
	# Translators: border styles in Microsoft Excel.
	xlThin:_("thin"),
	# Translators: border styles in Microsoft Excel.
	xlMedium:_("medium"),
	# Translators: border styles in Microsoft Excel.
	xlThick:_("thick"),
}
borderStyleAndWeightLabels={
	# Translators: border styles in Microsoft Excel.
	(xlContinuous, xlHairline):_("hair"),
	# Translators: border styles in Microsoft Excel.
	(xlDot, xlThin):_("dotted"),
	# Translators: border styles in Microsoft Excel.
	(xlDashDotDot, xlThin):_("dash dot dot"),
	# Translators: border styles in Microsoft Excel.
	(xlDashDot, xlThin):_("dash dot"),
	# Translators: border styles in Microsoft Excel.
	(xlDash, xlThin):_("dashed"),
	# Translators: border styles in Microsoft Excel.
	(xlContinuous, xlThin):_("thin"),
	# Translators: border styles in Microsoft Excel.
	(xlDashDotDot, xlMedium):_("medium dash dot dot"),
	# Translators: border styles in Microsoft Excel.
	(xlSlantDashDot, xlMedium):_("slanted dash dot"),
	# Translators: border styles in Microsoft Excel.
	(xlDashDot, xlMedium):_("medium dash dot"),
	# Translators: border styles in Microsoft Excel.
	(xlDash, xlMedium):_("medium dashed"),
	# Translators: border styles in Microsoft Excel.
	(xlContinuous, xlMedium):_("medium"),
	# Translators: border styles in Microsoft Excel.
	(xlContinuous, xlThick):_("thick"),
	# Translators: border styles in Microsoft Excel.
	(xlDouble, xlThick):_("double"),
}

def getCellBorderStyleDescription(bordersObj,reportBorderColor=False):
	d=OrderedDict()
	for pos in bordersIndexLabels:
		border=bordersObj[pos]
		if border.lineStyle != xlLineStyleNone:
			style=border.lineStyle
			weight=border.weight
			desc=borderStyleAndWeightLabels.get((style,weight))
			if not desc:
				# Translators: border styles in Microsoft Excel.
				desc=_("{weight} {style}").format(
					style=borderStyleLabels.get(style),
					weight=borderWeightLabels.get(weight)
				)
			if reportBorderColor:
				# Translators: border styles in Microsoft Excel.
				d[pos]=_("{color} {desc}").format(
					color=colors.RGB.fromCOLORREF(int(border.color)).name,
					desc=desc
				)
			else:
				d[pos]=desc
	s=[]
	if d.get(xlEdgeTop) == d.get(xlEdgeBottom) == d.get(xlEdgeLeft) == d.get(xlEdgeRight) and d.get(xlEdgeTop) is not None:
		# Translators: border styles in Microsoft Excel.
		s.append(_("{desc} surrounding border").format(desc=d.get(xlEdgeTop)))
		del d[xlEdgeTop]
		del d[xlEdgeBottom]
		del d[xlEdgeLeft]
		del d[xlEdgeRight]
	if d.get(xlEdgeTop) == d.get(xlEdgeBottom) and d.get(xlEdgeTop) is not None:
		# Translators: border styles in Microsoft Excel.
		s.append(_("{desc} top and bottom edges").format(desc=d.get(xlEdgeTop)))
		del d[xlEdgeTop]
		del d[xlEdgeBottom]
	if d.get(xlEdgeLeft) == d.get(xlEdgeRight) and d.get(xlEdgeLeft) is not None:
		# Translators: border styles in Microsoft Excel.
		s.append(_("{desc} left and right edges").format(desc=d.get(xlEdgeLeft)))
		del d[xlEdgeLeft]
		del d[xlEdgeRight]
	if d.get(xlDiagonalUp) == d.get(xlDiagonalDown) and d.get(xlDiagonalUp) is not None:
		# Translators: border styles in Microsoft Excel.
		s.append(_("{desc} up-right and down-right diagonal lines").format(desc=d.get(xlDiagonalUp)))
		del d[xlDiagonalUp]
		del d[xlDiagonalDown]
	for pos,desc in d.items():
		# Translators: border styles in Microsoft Excel.
		s.append(_("{desc} {position}").format(
			desc=desc,
			position=bordersIndexLabels.get(pos)
		))
	return ', '.join(s)
