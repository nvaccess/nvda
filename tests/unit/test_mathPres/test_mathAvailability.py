# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import sys
import unittest
from unittest import mock

import mathPres
from gui import settingsDialogs
from mathPres.MathCAT import MathCAT as mathCATModule


class TestMathSettingsAvailability(unittest.TestCase):
	def test_mathSettingsCategoryFollowsMathCatAvailability(self):
		with (
			mock.patch.object(
				settingsDialogs.NVDASettingsDialog,
				"categoryClasses",
				[settingsDialogs.MathSettingsPanel],
			),
			mock.patch.object(mathPres, "_mathCATAvailable", False),
		):
			self.assertNotIn(
				settingsDialogs.MathSettingsPanel,
				settingsDialogs.NVDASettingsDialog._getCategoryClasses(),
			)

		with (
			mock.patch.object(
				settingsDialogs.NVDASettingsDialog,
				"categoryClasses",
				[settingsDialogs.MathSettingsPanel],
			),
			mock.patch.object(mathPres, "_mathCATAvailable", True),
		):
			self.assertIn(
				settingsDialogs.MathSettingsPanel,
				settingsDialogs.NVDASettingsDialog._getCategoryClasses(),
			)

	def test_mathCatAvailabilityIsCheckedWhenAddOnProvidesAllProviders(self):
		with (
			mock.patch.object(mathPres, "speechProvider", mock.sentinel.provider),
			mock.patch.object(mathPres, "brailleProvider", mock.sentinel.provider),
			mock.patch.object(mathPres, "interactionProvider", mock.sentinel.provider),
			mock.patch.object(mathPres, "_mathCATAvailable", True),
			mock.patch.dict(sys.modules, {"mathPres.MathCAT": None}),
			mock.patch.object(mathPres.log, "warning"),
		):
			mathPres.initialize()

			self.assertFalse(mathPres._mathCATAvailable)

	def test_mathCatInitializationFailureIsPropagated(self):
		with (
			mock.patch.object(mathCATModule.libmathcat, "GetVersion", return_value="test"),
			mock.patch.object(mathCATModule.libmathcat, "SetRulesDir", side_effect=RuntimeError("failed")),
			mock.patch.object(mathCATModule.ui, "message"),
			self.assertRaisesRegex(RuntimeError, "failed"),
		):
			mathCATModule.MathCAT()
