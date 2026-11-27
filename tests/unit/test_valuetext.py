# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for aria-valuetext support in web spin controls (#21169)."""

import unittest
from unittest.mock import Mock, patch

import IAccessibleHandler  # noqa: F401  # Break NVDAObjects circular import
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.UIA import UIA


class TestIAccessibleValueText(unittest.TestCase):
	"""Test aria-valuetext resolution in base IAccessible (#21169)."""

	def setUp(self):
		self.obj = IAccessible.__new__(IAccessible)
		self.obj.IAccessibleObject = Mock()
		self.obj.IAccessibleChildID = 0

	def test_ia2_valuetext_present(self):
		self.obj.IA2Attributes = {"valuetext": "12euros"}
		self.assertEqual(self.obj._get_value(), "12euros")

	def test_ia2_aria_valuetext_present(self):
		self.obj.IA2Attributes = {"aria-valuetext": "1,000 $"}
		self.assertEqual(self.obj._get_value(), "1,000 $")

	def test_ia2_valuetext_empty_falls_back(self):
		self.obj.IA2Attributes = {"valuetext": "   "}
		self.obj.IAccessibleObject.accValue.return_value = "12"
		self.assertEqual(self.obj._get_value(), "12")

	def test_ia2_valuetext_absent_falls_back(self):
		self.obj.IA2Attributes = {}
		self.obj.IAccessibleObject.accValue.return_value = "12"
		self.assertEqual(self.obj._get_value(), "12")


class TestUIAValueText(unittest.TestCase):
	"""Test aria-valuetext resolution in base UIA (#21169)."""

	def setUp(self):
		self.obj = UIA.__new__(UIA)

	def test_uia_valuetext_present(self):
		self.obj.ariaProperties = {"valuetext": "12euros"}
		self.assertEqual(self.obj._get_value(), "12euros")

	def test_uia_aria_valuetext_present(self):
		self.obj.ariaProperties = {"aria-valuetext": "1,000 $"}
		self.assertEqual(self.obj._get_value(), "1,000 $")

	def test_uia_valuetext_empty_falls_back(self):
		self.obj.ariaProperties = {"valuetext": "   "}
		with patch.object(UIA, "UIAValue", new="12"):
			self.assertEqual(self.obj._get_value(), "12")

	def test_uia_valuetext_absent_falls_back(self):
		self.obj.ariaProperties = {}
		with patch.object(UIA, "UIAValue", new="12"):
			self.assertEqual(self.obj._get_value(), "12")


class TestSpinbuttonSpeech(unittest.TestCase):
	"""Test getObjectSpeech for spinbutton controls (#21169)."""

	def test_spinbutton_speaks_value_instead_of_raw_text(self):
		import controlTypes
		from speech.speech import OutputReason, getObjectSpeech

		obj = Mock()
		obj.role = controlTypes.Role.SPINBUTTON
		obj.states = {controlTypes.State.FOCUSABLE, controlTypes.State.FOCUSED, controlTypes.State.EDITABLE}
		obj.name = "Amount"
		obj.value = "12euros"
		obj.treeInterceptor = None
		obj.isCurrent = controlTypes.IsCurrent.NO
		obj.annotations = None
		obj.descriptionFrom = controlTypes.DescriptionFrom.UNKNOWN
		obj.description = None
		obj.positionInfo = {}
		obj._speakObjectPropertiesCache = {}
		obj._hasNavigableText = True
		textInfo = Mock()
		textInfo.isCollapsed = False
		textInfo.text = "12"
		obj.makeTextInfo.return_value = textInfo

		seq = getObjectSpeech(obj, reason=OutputReason.FOCUS)
		self.assertIn("12euros", seq)
		self.assertNotIn("12", seq)


class TestChromiumSpinButton(unittest.TestCase):
	"""Test Chromium SpinButton overlay aria-valuetext resolution (#21169)."""

	def test_chromium_spinbutton_overlay_added(self):
		import controlTypes
		from NVDAObjects.IAccessible import chromium

		obj = Mock()
		obj.role = controlTypes.Role.SPINBUTTON
		obj.IA2Attributes = {"id": "amount"}
		obj.parent = None
		clsList = []
		chromium.findExtraOverlayClasses(obj, clsList)
		self.assertIn(chromium.SpinButton, clsList)

	def test_chromium_spinbutton_resolves_from_uia(self):
		from NVDAObjects.IAccessible.chromium import SpinButton

		obj = SpinButton.__new__(SpinButton)
		obj._getValueFromUia = Mock(return_value="12euros")
		self.assertEqual(obj._get_value(), "12euros")


class TestSpinbuttonBraille(unittest.TestCase):
	"""Test NVDAObjectRegion braille rendering for editable spinbuttons (#21169)."""

	def test_spinbutton_braille_includes_valuetext(self):
		import controlTypes
		from braille.regions.NVDAObject import NVDAObjectRegion

		obj = Mock()
		obj.role = controlTypes.Role.SPINBUTTON
		obj.states = {controlTypes.State.FOCUSABLE, controlTypes.State.FOCUSED, controlTypes.State.EDITABLE}
		obj.name = "Amount"
		obj.value = "12euros"
		obj.placeholder = None
		obj._isTextEmpty = False
		obj.errorMessage = None
		obj.description = None
		obj.annotations = None
		obj.roleTextBraille = None
		obj.isCurrent = controlTypes.IsCurrent.NO
		obj.keyboardShortcut = None
		obj.positionInfo = {}
		obj.cellCoordsText = None
		obj._hasNavigableText = True
		obj.TextInfo = Mock

		with patch("braille.regions.NVDAObject.objectBelowLockScreenAndWindowsIsLocked", return_value=False):
			region = NVDAObjectRegion(obj)
			region.update()
		self.assertIn("12euros", region.rawText)
