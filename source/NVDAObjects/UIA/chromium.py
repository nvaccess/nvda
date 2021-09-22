# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020-2021 NV Access limited, Leonard de Ruijter

import UIAHandler
from . import web
import controlTypes

"""
This module provides UIA behaviour specific to the chromium family of browsers.
Note this is more specialised than UIA.web but less so than browser specific modules such as UIA.spartan_edge
or UIA.anaheim_edge.
"""


class ChromiumUIATextInfo(web.UIAWebTextInfo):

	def expand(self, unit):
		# #12474: Expanding to line breaks when the underlying text range is empty.
		if (
			UIAHandler.NVDAUnitsToUIAUnits.get(unit) == UIAHandler.UIA.TextUnit_Line
			and self.obj.UIATextPattern.documentRange.GetText(1) == ""
		):
			return
		super().expand(unit)

	def _getFormatFieldAtRange(self, textRange, formatConfig, ignoreMixedValues=False):
		formatField = super()._getFormatFieldAtRange(textRange, formatConfig, ignoreMixedValues=ignoreMixedValues)
		# Headings are also exposed in the element tree,
		# And therefore exposing in a formatField is redundant and causes duplicate reporting.
		# So remove heading-level from the formatField if it exists.
		try:
			del formatField.field['heading-level']
		except KeyError:
			pass
		return formatField

	def _getControlFieldForUIAObject(self, obj, isEmbedded=False, startOfNode=False, endOfNode=False):
		field = super()._getControlFieldForUIAObject(
			obj,
			isEmbedded=isEmbedded,
			startOfNode=startOfNode,
			endOfNode=endOfNode
		)
		# use the value of comboboxes as content.
		if obj.role == controlTypes.Role.COMBOBOX:
			field['content'] = obj.value
		# Layout tables do not have the UIA table pattern
		if field['role'] == controlTypes.Role.TABLE:
			if not obj._getUIACacheablePropertyValue(UIAHandler.UIA_IsTablePatternAvailablePropertyId):
				field['table-layout'] = True
		# Currently no way to tell if author has explicitly set name.
		# Therefore always report the name if the control is not of a type that
		# by definition uses its name for content.
		# this may cause some duplicate speaking,
		# But that is currently better than nothing at all.
		if not field.get('nameIsContent') and field.get('name'):
			field['alwaysReportName'] = True
		return field


class ChromiumUIA(web.UIAWeb):
	_TextInfo = ChromiumUIATextInfo


class ChromiumUIATreeInterceptor(web.UIAWebTreeInterceptor):

	def _get_documentConstantIdentifier(self):
		return self.rootNVDAObject.parent._getUIACacheablePropertyValue(UIAHandler.UIA_AutomationIdPropertyId)


class ChromiumUIADocument(ChromiumUIA):
	treeInterceptorClass = ChromiumUIATreeInterceptor

	def _get_shouldCreateTreeInterceptor(self):
		return self.role == controlTypes.Role.DOCUMENT
