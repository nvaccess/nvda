# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest
from unittest import mock

import core
import screenCurtain


class TestInitialBrailleMessage(unittest.TestCase):
	def test_screenCurtainUnavailable(self):
		with mock.patch.object(screenCurtain, "screenCurtain", None):
			self.assertEqual("NVDA started", core._getInitialBrailleMessage())

	def test_screenCurtainEnabled(self):
		with mock.patch.object(
			screenCurtain,
			"screenCurtain",
			mock.Mock(enabled=True),
		):
			self.assertEqual(
				"NVDA started with screen curtain enabled",
				core._getInitialBrailleMessage(),
			)
