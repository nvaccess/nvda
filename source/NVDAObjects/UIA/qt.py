# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Overlay classes for Qt applications exposing UI Automation."""

import controlTypes

from NVDAObjects import NVDAObject
from NVDAObjects.behaviors import EditableTextWithAutoSelectDetection

from . import UIA

MUSE_ACCESSIBLE_OBJECT_CLASS_NAME = "muse::accessibility::AccessibleObject"


class MuseAccessibilityObjectWithNoopTextPattern(UIA):
	"""A Muse framework control other than a text field that exposes a no-op UIA text pattern."""

	def initOverlayClass(self):
		self.UIATextPattern = None


def findExtraOverlayClasses(obj: NVDAObject, clsList: list[type[NVDAObject]]) -> None:
	if (
		obj.UIAElement.cachedClassName == MUSE_ACCESSIBLE_OBJECT_CLASS_NAME
		and obj.role != controlTypes.Role.EDITABLETEXT
		and obj.UIATextPattern
	):
		try:
			clsList.remove(EditableTextWithAutoSelectDetection)
		except ValueError:
			pass
		clsList.insert(0, MuseAccessibilityObjectWithNoopTextPattern)
