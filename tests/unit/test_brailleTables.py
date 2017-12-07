#tests/unit/test_brailleTables.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited, Babbage B.V.

"""Unit tests for the brailleTables module.
"""

import unittest
import brailleTables
import os.path

class TestFBrailleTables(unittest.TestCase):
	"""Tests for braille table files and their existence."""

	def test_tableExistence(self):
		"""Tests whether all defined tables exist."""
		tables = brailleTables.listTables()
		for table in tables:
			self.assertTrue(
				os.path.isfile(os.path.join(brailleTables.TABLES_DIR, table.fileName)),
				msg="{table} table not found".format(table=table.displayName)
			)