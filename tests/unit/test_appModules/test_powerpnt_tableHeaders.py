# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for the header cells of PowerPoint tables."""

import unittest
from types import SimpleNamespace
from typing import Any

import controlTypes
from appModules import powerpnt


def _object[T](cls: type[T], **attrs: Any) -> T:
	obj = object.__new__(cls)
	obj._propertyCache = {}
	obj.__dict__.update(attrs)
	return obj


class TestTableHeaders(unittest.TestCase):
	def setUp(self) -> None:
		self.texts = {
			(1, 1): "Animal",
			(1, 2): "Sound ",
			(2, 1): " Dog",
			(2, 2): "Woof",
		}
		self.ppTable = SimpleNamespace(
			firstRow=True,
			firstCol=True,
			cell=lambda row, column: SimpleNamespace(
				shape=SimpleNamespace(
					textFrame=SimpleNamespace(textRange=SimpleNamespace(text=self.texts[row, column])),
				),
			),
		)
		self.table = SimpleNamespace(ppTable=self.ppTable)

	def _cell(self, row: int, column: int) -> powerpnt.TableCell:
		return _object(powerpnt.TableCell, table=self.table, rowNumber=row, columnNumber=column)

	def test_rolesFollowTheHeaderRowAndFirstColumnOptions(self) -> None:
		self.assertEqual(self._cell(1, 2).role, controlTypes.Role.TABLECOLUMNHEADER)
		self.assertEqual(self._cell(2, 1).role, controlTypes.Role.TABLEROWHEADER)
		self.assertEqual(self._cell(2, 2).role, controlTypes.Role.TABLECELL)

	def test_cornerCellIsAColumnHeader(self) -> None:
		self.assertEqual(self._cell(1, 1).role, controlTypes.Role.TABLECOLUMNHEADER)

	def test_cellsAreOrdinaryWhenTheOptionsAreOff(self) -> None:
		self.ppTable.firstRow = False
		self.ppTable.firstCol = False
		for row, column in self.texts:
			with self.subTest(row=row, column=column):
				cell = self._cell(row, column)
				self.assertEqual(cell.role, controlTypes.Role.TABLECELL)
				self.assertIsNone(cell.rowHeaderText)
				self.assertIsNone(cell.columnHeaderText)

	def test_headerTextComesFromTheFirstRowAndColumn(self) -> None:
		cell = self._cell(2, 2)
		self.assertEqual(cell.rowHeaderText, "Dog")
		self.assertEqual(cell.columnHeaderText, "Sound")

	def test_headerCellsHaveNoHeaderOfTheirOwnKind(self) -> None:
		self.assertIsNone(self._cell(1, 2).columnHeaderText)
		self.assertIsNone(self._cell(2, 1).rowHeaderText)

	def test_onlyTheEnabledOptionProvidesHeaderText(self) -> None:
		self.ppTable.firstRow = False
		cell = self._cell(2, 2)
		self.assertIsNone(cell.columnHeaderText)
		self.assertEqual(cell.rowHeaderText, "Dog")
