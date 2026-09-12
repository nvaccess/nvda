# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest
from unittest import mock

import mathPres
from gui import settingsDialogs


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
