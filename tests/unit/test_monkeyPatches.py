# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

import certifi
import certifi.core
from monkeyPatches import certifiMonkeyPatches


class TestCertifiMonkeyPatches(unittest.TestCase):
	def setUp(self):
		self._originalCertifiWhere = certifi.where
		self._originalCertifiContents = certifi.contents
		self._originalCertifiCoreWhere = certifi.core.where
		self._originalCertifiCoreContents = certifi.core.contents

	def tearDown(self):
		certifi.where = self._originalCertifiWhere
		certifi.contents = self._originalCertifiContents
		certifi.core.where = self._originalCertifiCoreWhere
		certifi.core.contents = self._originalCertifiCoreContents

	def test_applyDoesNothingWhenNotFrozen(self):
		with patch.object(sys, "frozen", new=None, create=True):
			certifiMonkeyPatches.apply()

		self.assertIs(certifi.where, self._originalCertifiWhere)
		self.assertIs(certifi.core.where, self._originalCertifiCoreWhere)

	def test_applyUsesBundledCaCertInFrozenBuild(self):
		with tempfile.TemporaryDirectory() as tempDir:
			bundledCertPath = os.path.join(tempDir, "cacert.pem")
			with open(bundledCertPath, "w", encoding="ascii") as certFile:
				certFile.write("TEST CERT")
			fakeExecutablePath = os.path.join(tempDir, "nvda_noUIAccess.exe")

			with (
				patch.object(sys, "frozen", new="windows_exe", create=True),
				patch.object(sys, "executable", new=fakeExecutablePath),
			):
				certifiMonkeyPatches.apply()

			self.assertEqual(certifi.where(), bundledCertPath)
			self.assertEqual(certifi.core.where(), bundledCertPath)
			self.assertEqual(certifi.contents(), "TEST CERT")
			self.assertEqual(certifi.core.contents(), "TEST CERT")
