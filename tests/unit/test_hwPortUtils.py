# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Akash Kakkar
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import unittest
from unittest import mock

import hwPortUtils
from winBindings import bthprops
from winBindings._utils import _makeUnavailable


class TestBluetoothDeviceInfo(unittest.TestCase):
	def test_cplCompatibilityAliasIsAvailable(self):
		self.assertTrue(hasattr(bthprops, "cpl"))

	def test_unavailableBluetoothApiRaisesOSError(self):
		with (
			mock.patch.object(
				hwPortUtils,
				"_BluetoothGetDeviceInfo",
				_makeUnavailable("BluetoothGetDeviceInfo", "The Bluetooth API is not available", None),
			),
			self.assertRaisesRegex(OSError, "Bluetooth API is not available"),
		):
			hwPortUtils.getBluetoothDeviceInfo(0)
