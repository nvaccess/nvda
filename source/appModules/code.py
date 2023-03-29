# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

""" App module for Visual Studio Code.
"""

import appModuleHandler
from NVDAObjects.IAccessible.chromium import Document
from NVDAObjects import NVDAObject


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
