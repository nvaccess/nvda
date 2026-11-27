# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Akash Kakkar
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import unittest
from unittest import mock

import bdDetect
import braille.display.driver
from brailleDisplayDrivers import hims


class TestWinUsbFallback(unittest.TestCase):
	def test_unavailableWinUsbContinuesAfterBulkFailure(self):
		port = "customPort"
		with (
			mock.patch.object(braille.display.driver.BrailleDisplayDriver, "__init__", return_value=None),
			mock.patch.object(
				hims.BrailleDisplayDriver,
				"_getTryPorts",
				return_value=[(bdDetect.ProtocolType.CUSTOM, "", port, {})],
			),
			mock.patch.object(hims.hwIo, "Bulk", side_effect=OSError),
			mock.patch.object(hims, "WINUSB_AVAILABLE", False),
			mock.patch.object(hims, "_WinUsbBulk") as winUsbBulk,
			self.assertRaisesRegex(RuntimeError, "No Hims display found"),
		):
			hims.BrailleDisplayDriver()

		winUsbBulk.assert_not_called()
