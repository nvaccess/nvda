# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2024 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Unit tests for the brailleTables module.
"""

import os.path
import unittest

import brailleTables


class TestBrailleTables(unittest.TestCase):
	"""Tests for braille table files and their existence."""

	def test_tableExistence(self):
		"""Tests whether all defined tables exist."""
		tables = brailleTables.listTables()
		for table in tables:
			self.assertTrue(
				os.path.isfile(os.path.join(brailleTables.TABLES_DIR, table.fileName)),
				msg=f"{table.displayName} table not found"
			)

	def test_renamedTableExistence(self):
		"""Tests whether all defined renamed tables are part of the actual list of tables."""
		tableNames = [table.fileName for table in brailleTables.listTables()]
		for name in brailleTables.RENAMED_TABLES.values():
			self.assertIn(name, tableNames)
