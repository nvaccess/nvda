# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for the ART logging indirection, :mod:`_art._log`."""

import unittest

from _art import _log
from logHandler import Logger


class TestWarningLevels(unittest.TestCase):
	"""
	``_art._log`` duplicates NVDA's ``DEBUGWARNING`` because the host cannot import it.
	This test is the coupling that catches the copy drifting from NVDA's own.
	If further levels are copied, cases should be added for them, too.
	"""

	def test_debugWarningMatchesNVDA(self):
		self.assertEqual(_log._DEBUGWARNING_LEVEL, Logger.DEBUGWARNING)
