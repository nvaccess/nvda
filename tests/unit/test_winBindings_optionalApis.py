# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest
from unittest import mock

from winBindings import magnification, winusb


class TestUnavailableMagnification(unittest.TestCase):
	def test_bindReturnsCallableStub(self):
		with mock.patch.object(magnification, "dll", None):
			binding = magnification._bind("MissingFunction", mock.sentinel.prototype)

		self.assertIs(binding, magnification._unavailable)
		with self.assertRaisesRegex(OSError, "Magnification API is not available"):
			binding(showCursor=True)


class TestUnavailableWinUsb(unittest.TestCase):
	def test_bindReturnsCallableStub(self):
		with mock.patch.object(winusb, "dll", None):
			binding = winusb._bind("MissingFunction", (), None)

		self.assertIs(binding, winusb._unavailable)
		with self.assertRaisesRegex(OSError, "WinUSB is not available"):
			binding(buffer=None)
