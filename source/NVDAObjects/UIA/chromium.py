# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 NV Access limited, Leonard de Ruijter

import UIAHandler
import cursorManager
from . import UIA, web
from UIABrowseMode import UIABrowseModeDocument, UIABrowseModeDocumentTextInfo
import controlTypes


class ChromiumUIA(web.UIAWeb):
	...


class ChromiumUIATreeInterceptor(web.UIAWebTreeInterceptor):

	def _get_documentConstantIdentifier(self):
		return self.rootNVDAObject.parent._getUIACacheablePropertyValue(UIAHandler.UIA_AutomationIdPropertyId)


class ChromiumUIADocument(ChromiumUIA):
	treeInterceptorClass = ChromiumUIATreeInterceptor

	def _get_shouldCreateTreeInterceptor(self):
		return self.role == controlTypes.ROLE_DOCUMENT
