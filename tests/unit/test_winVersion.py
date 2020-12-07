#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2020 NV Access Limited, Joseph Lee

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
