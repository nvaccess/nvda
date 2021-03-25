# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited, Joseph Lee

"""Unit tests for the Windows version module."""

import unittest
import sys
import winVersion


class TestWinVersion(unittest.TestCase):

	def test_getWinVer(self):
		# Test a 3-tuple consisting of version major, minor, build.
		# sys.getwindowsversion() internally returns a named tuple, so comparing tuples is possible.
		currentWinVer = winVersion.getWinVer()
		winVerPython = sys.getwindowsversion()
		self.assertTupleEqual(
			(currentWinVer.major, currentWinVer.minor, currentWinVer.build),
			winVerPython[:3]
		)

	def test_getWinVerFromNonExistentRelease(self):
		# Test the fact that there is no Windows 10 2003 (2004 exists, however).
		with self.assertRaises(AttributeError):
			may2020Update = winVersion.WIN10_2003  # NOQA: F841

	def test_moreRecentWinVer(self):
		# Specifically to test operators.
		minimumWinVer = winVersion.WIN7_SP1
		audioDuckingAvailable = winVersion.WIN8
		self.assertGreaterEqual(
			audioDuckingAvailable, minimumWinVer
		)
