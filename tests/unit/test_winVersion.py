# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 NV Access Limited, Joseph Lee

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

	def test_specificWinVer(self):
		# Try detecting Windows 8.1 or later.
		win81 = winVersion.WinVersion(release="8.1")
		self.assertTupleEqual(
			(win81.major, win81.minor, win81.build),
			(6, 3, 9600)
		)

	def test_getWinVerFromVersionText(self):
		winTenInitial = winVersion.getWinVerFromVersionText("10.0.10240")
		self.assertTupleEqual(
			(winTenInitial.major, winTenInitial.minor, winTenInitial.build),
			(10, 0, 10240)
		)

	def test_moreRecentWinVer(self):
		# Specificlaly to test operators.
		minimumWinVer = winVersion.WinVersion(
			major=6,
			minor=1,
			build=7601
		)
		self.assertGreaterEqual(
			winVersion.getWinVer(), minimumWinVer
		)

	def test_isWin10(self):
		# Say "False" if tested on anything other than Windows 10.
		currentWinVer = winVersion.getWinVer()
		if currentWinVer.major == 10:
			self.assertTrue(currentWinVer.isWin10())
		else:
			self.assertFalse(currentWinVer.isWin10())

	@unittest.skipIf(
			sys.getwindowsversion().major != 10,
			"requires Windows 10"
	)
	def test_isWin10NonexistentRelease(self):
		# Test the fact that there is no Version 2003 (Version 2004 exists, however).
		self.assertRaises(
			ValueError,
			winVersion.getWinVer().isWin10,
			release="2003"
		)
