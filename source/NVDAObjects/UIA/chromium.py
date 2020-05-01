# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 NV Access limited, Leonard de Ruijter

import cursorManager
from . import UIA
from UIABrowseMode import UIABrowseModeDocument, UIABrowseModeDocumentTextInfo
import controlTypes


class ChromiumUIA(UIA):
	pass


class ChromiumUIATreeInterceptor(cursorManager.ReviewCursorManager, UIABrowseModeDocument):
	TextInfo = UIABrowseModeDocumentTextInfo


class ChromiumUIARoot(ChromiumUIA):
	treeInterceptorClass = ChromiumUIATreeInterceptor

	def _get_shouldCreateTreeInterceptor(self):
		return self.role == controlTypes.ROLE_DOCUMENT
