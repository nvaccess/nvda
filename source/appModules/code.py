# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2024 NV Access Limited, Leonard de Ruijter, Cary-Rowen
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Visual Studio Code."""

import appModuleHandler
import controlTypes
from NVDAObjects.IAccessible.chromium import Document
from NVDAObjects import NVDAObject, NVDAObjectTextInfo


class VSCodeDocument(Document):
	"""The only content in the root document node of Visual Studio code is the application object.
	Creating a tree interceptor on this object causes a major slow down of Code.
	Therefore, forcefully block tree interceptor creation.
	"""

	_get_treeInterceptorClass = NVDAObject._get_treeInterceptorClass


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if Document in clsList and obj.IA2Attributes.get("tag") == "#document":
			clsList.insert(0, VSCodeDocument)

	def event_NVDAObject_init(self, obj: NVDAObject):
		# TODO: This is a specific fix for Visual Studio Code.
		# Once the underlying issue is resolved, this workaround can be removed.
		# See issue #15159 for more details.
		if obj.role != controlTypes.Role.EDITABLETEXT and controlTypes.State.EDITABLE not in obj.states:
			obj.TextInfo = NVDAObjectTextInfo
