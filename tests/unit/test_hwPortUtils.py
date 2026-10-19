# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest
from unittest import mock

import hwPortUtils
from winBindings import bthprops


class TestBluetoothDeviceInfo(unittest.TestCase):
	def test_cplCompatibilityAliasIsAvailable(self):
		self.assertTrue(hasattr(bthprops, "cpl"))

	def test_unavailableBluetoothApiRaisesOSError(self):
		with (
			mock.patch.object(
				hwPortUtils,
				"_BluetoothGetDeviceInfo",
				bthprops._unavailableBluetoothGetDeviceInfo,
			),
			self.assertRaisesRegex(OSError, "Bluetooth API is not available"),
		):
			hwPortUtils.getBluetoothDeviceInfo(0)
