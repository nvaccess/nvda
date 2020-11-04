# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 NV Access limited, Leonard de Ruijter

import UIAHandler
from . import web
import controlTypes

"""
This module provides UIA behaviour specific to the chromium family of browsers.
Note this is more specialised than UIA.web but less so than browser specific modules such as UIA.spartan_edge
or UIA.anaheim_edge.
"""


class ChromiumUIATextInfo(web.UIAWebTextInfo):

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


class ChromiumUIA(web.UIAWeb):
	_TextInfo = ChromiumUIATextInfo


class ChromiumUIATreeInterceptor(web.UIAWebTreeInterceptor):

	def _get_documentConstantIdentifier(self):
		return self.rootNVDAObject.parent._getUIACacheablePropertyValue(UIAHandler.UIA_AutomationIdPropertyId)


class ChromiumUIADocument(ChromiumUIA):
	treeInterceptorClass = ChromiumUIATreeInterceptor

	def _get_shouldCreateTreeInterceptor(self):
		return self.role == controlTypes.ROLE_DOCUMENT
