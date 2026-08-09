# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest

import aria


class TestLocalizedRoleDescription(unittest.TestCase):
	def test_knownDescription(self):
		for roleDescription, localizedRoleDescription in aria.localizedRoleDescriptions.items():
			with self.subTest(roleDescription=roleDescription):
				self.assertEqual(
					aria.getLocalizedRoleDescription(roleDescription),
					localizedRoleDescription,
				)

	def test_unknownDescription(self):
		self.assertEqual(aria.getLocalizedRoleDescription("pizza"), "pizza")
