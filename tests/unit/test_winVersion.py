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
			# Flake8 F841: local variable name is assigned to but never used
			may2020Update = winVersion.WIN10_2003  # NOQA: F841

	def test_moreRecentWinVer(self):
		# Specifically to test operators.
		minimumWinVer = winVersion.WIN7_SP1
		audioDuckingAvailable = winVersion.WIN8
		self.assertGreaterEqual(
			audioDuckingAvailable, minimumWinVer
		)

	def test_winVerReleaseName(self):
		# Test the fact that later Windows releases provide version information in a consistent manner,
		# specifically, via Windows Registry on Windows 10 1511 and later.
		# Test with Windows Server 2016 (client release name: Windows 10 1607).
		server2016 = winVersion.WIN10_1607
		self.assertIn(
			"Windows 10 1607", repr(server2016)
		)
