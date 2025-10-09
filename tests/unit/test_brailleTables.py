# tests/unit/test_brailleTables.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Unit tests for the brailleTables module."""

import unittest
import brailleTables
import louis
import louisHelper
import os.path


class TestBrailleTables(unittest.TestCase):
	"""Tests for braille table files and their existence."""

	def test_tableExistence(self):
		"""Tests whether all defined tables exist."""
		tables = brailleTables.listTables()
		for table in tables:
			with self.subTest(table=table.fileName):
				self.assertTrue(
					os.path.isfile(os.path.join(brailleTables.TABLES_DIR, table.fileName)),
					msg="{table} table not found".format(table=table.displayName),
				)

	def test_renamedTableExistence(self):
		"""Tests whether all defined renamed tables are part of the actual list of tables."""
		tableNames = [table.fileName for table in brailleTables.listTables()]
		for name in brailleTables.RENAMED_TABLES.values():
			with self.subTest(name=name):
				self.assertIn(name, tableNames)


class TestTranslate(unittest.TestCase):
	"""Ensures that all tables can be used for translation."""

	def test_translate(self):
		"""Tests whether all tables can be used for translation."""
		tables = brailleTables.listTables()
		for table in tables:
			if not table.output:
				continue
			with self.subTest(table=table.fileName):
				try:
					louisHelper.translate([table.fileName, "braille-patterns.cti"], "test")
				except Exception as e:
					self.fail(f"Translation failed for {table.displayName}: {e}")

	def test_backtranslate(self):
		"""Tests whether all tables can be used for back-translation."""
		tables = brailleTables.listTables()
		for table in tables:
			if not table.input:
				continue
			with self.subTest(table=table.fileName):
				try:
					louis.backTranslate([table.fileName, "braille-patterns.cti"], "⠞⠑⠎⠞")
				except Exception as e:
					self.fail(f"Back-translation failed for {table.displayName}: {e}")
