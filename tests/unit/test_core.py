# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Akash Kakkar
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

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
