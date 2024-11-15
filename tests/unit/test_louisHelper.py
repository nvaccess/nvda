# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited, Leonard de Ruijter

"""Unit tests for the louisHelper module."""

import os.path
import unittest

import brailleTables
import louisHelper
import NVDAState


class TestResolvingInternal(unittest.TestCase):
	"""Tests for internal braille table resolving using our custom resolver."""

	def test_tableResolvingInternal(self):
		"""Test whether our custom braille table resolver can resolve all defined tables."""
		tables = brailleTables.listTables()
		for table in tables:
			self.assertEqual(
				list(louisHelper._resolveTableInner(tables=[table.fileName])),
				[os.path.join(brailleTables.TABLES_DIR, table.fileName)],
			)

	def test_internalTableIncludedInternal(self):
		"""Test the case for resolving a particular internal table."""
		base = brailleTables.getTable("en-us-comp8-ext.utb")
		basePath = os.path.join(brailleTables.TABLES_DIR, base.fileName)
		fileNameToTest = "latinLetterDef8Dots.uti"
		self.assertEqual(
			list(louisHelper._resolveTableInner(tables=[fileNameToTest], base=basePath)),
			[os.path.join(brailleTables.TABLES_DIR, fileNameToTest)],
		)

	def test_unknownInternalTable(self):
		"""Test the case where a table does not exist, regardless of base."""
		fileNameToTest = "random.uti"
		with self.assertRaises(LookupError):
			list(louisHelper._resolveTableInner(tables=[fileNameToTest]))

	def test_internalTableIncludedUnknown(self):
		"""Test the case where an included table does not exist."""
		base = brailleTables.getTable("en-us-comp8-ext.utb")
		basePath = os.path.join(brailleTables.TABLES_DIR, base.fileName)
		fileNameToTest = "random.uti"
		with self.assertRaises(LookupError):
			list(louisHelper._resolveTableInner(tables=[fileNameToTest], base=basePath))


class TestResolvingCustom(unittest.TestCase):
	"""Tests for custom braille table resolving using our custom resolver."""

	tableDir: str

	def setUp(self):
		self.tablesDir = os.path.join(NVDAState.WritePaths.configDir, "brailleTables")
		self.assertTrue(os.path.exists(self.tablesDir))
		brailleTables._tablesDirs["tests"] = self.tablesDir
		brailleTables.addTable(
			fileName="en-us-comp8-ext.utb",
			displayName="English (U.S.) 8 dot computer braille override",
			source="tests",
		)
		brailleTables.addTable(fileName="test.utb", displayName="Test table", source="tests")

	def tearDown(self) -> None:
		# Cleanup our modifications to the brailleTables internals.
		brailleTables._tablesDirs.clear()
		brailleTables._tables.clear()

	def test_customTableOverridingExistingTable(self):
		table = brailleTables.getTable("en-us-comp8-ext.utb")
		self.assertEqual(
			list(louisHelper._resolveTableInner(tables=[table.fileName])),
			[os.path.join(self.tablesDir, table.fileName)],
		)

	def test_customTableNew(self):
		table = brailleTables.getTable("test.utb")
		self.assertEqual(
			list(louisHelper._resolveTableInner(tables=[table.fileName])),
			[os.path.join(self.tablesDir, table.fileName)],
		)

	def test_customTableIncludedCustom(self):
		"""Test the case where a custom table includes another table that is also implicitly replaced."""
		base = brailleTables.getTable("en-us-comp8-ext.utb")
		basePath = os.path.join(self.tablesDir, base.fileName)
		fileNameToTest = "latinLetterDef8Dots.uti"
		self.assertEqual(
			list(louisHelper._resolveTableInner(tables=[fileNameToTest], base=basePath)),
			[os.path.join(self.tablesDir, fileNameToTest)],
		)

	def test_internalTableIncludedCustom(self):
		"""Test the case where an internal table includes another table
		that is bundled as part of a new or replaced table.
		In this case, even though the include has a replacement in an add-on or the scratchpad,
		the built-in table should use the built-in include.
		"""
		base = brailleTables.getTable("nl-comp8.utb")
		basePath = os.path.join(brailleTables.TABLES_DIR, base.fileName)
		fileNameToTest = "latinLetterDef8Dots.uti"
		# Ensure the replacement is available
		self.assertTrue(os.path.exists(os.path.join(self.tablesDir, fileNameToTest)))
		# Perform the test of the resolver
		self.assertEqual(
			list(louisHelper._resolveTableInner(tables=[fileNameToTest], base=basePath)),
			[os.path.join(brailleTables.TABLES_DIR, fileNameToTest)],
		)

	def test_customTableIncludedInternal(self):
		"""Test the case where a custom table includes another table that is bundled internally."""
		base = brailleTables.getTable("test.utb")
		basePath = os.path.join(self.tablesDir, base.fileName)
		fileNameToTest = "braille-patterns.cti"
		self.assertEqual(
			list(louisHelper._resolveTableInner(tables=[fileNameToTest], base=basePath)),
			[os.path.join(brailleTables.TABLES_DIR, fileNameToTest)],
		)

	def test_customTableIncludedUnknown(self):
		"""Test the case where an included table does not exist."""
		base = brailleTables.getTable("test.utb")
		basePath = os.path.join(brailleTables.TABLES_DIR, base.fileName)
		fileNameToTest = "random.uti"
		with self.assertRaises(LookupError):
			list(louisHelper._resolveTableInner(tables=[fileNameToTest], base=basePath))

	def test_unknownTableIncludedInternal(self):
		"""Test the case for resolving a table when the base folder does not exist.
		Note that the resolver should always try to resolve from the default directory,
		so this shouldn't raise an error.
		"""
		basePath = os.path.join("ran", "dom")
		fileNameToTest = "braille-patterns.cti"
		self.assertEqual(
			list(louisHelper._resolveTableInner(tables=[fileNameToTest], base=basePath)),
			[os.path.join(brailleTables.TABLES_DIR, fileNameToTest)],
		)
