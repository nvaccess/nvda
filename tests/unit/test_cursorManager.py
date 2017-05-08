#tests/unit/test_cursorManager.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited

"""Unit tests for the cursorManager module.
"""

import unittest
import cursorManager
from .textProvider import BasicTextProvider

class CursorManager(cursorManager.CursorManager, BasicTextProvider):
	"""CursorManager which navigates within a provided string of text.
	"""

class SkipBlanksCursorManager(cursorManager.CursorManager, BasicTextProvider):
	"""CursorManager which navigates within a provided string of text, but skips blank lines.
	"""

	def _shouldSkipBlankLines(self, info):
		return True

class TestMove(unittest.TestCase):
	#Don't use tripple quote for multiline, because crlf makes each new line two offsets.
	multiline = "abc\n123\ndef\n\n456"

	def test_nextChar(self):
		cm = CursorManager(text="abc") # Caret at "a"
		cm.script_moveByCharacter_forward(None)
		self.assertEqual(cm.selectionOffsets, (1, 1)) # Caret at "b"

	def test_prevChar(self):
		cm = CursorManager(text="abc", selection=(1, 1)) # Caret at "b"
		cm.script_moveByCharacter_back(None)
		self.assertEqual(cm.selectionOffsets, (0, 0)) # Caret at "a"

	def test_nextLine(self):
		cm = CursorManager(text=self.multiline) # Caret at "a"
		cm.script_moveByLine_forward(None)
		self.assertEqual(cm.selectionOffsets, (4, 4)) # Caret at "1"

	def test_nextLineNoBlankSkipping(self):
		cm = CursorManager(text=self.multiline, selection=(8, 8)) # Caret at "d"
		cm.script_moveByLine_forward(None)
		self.assertEqual(cm.selectionOffsets, (12, 12)) # Caret at "\n"

	def test_nextLineBlankSkipping(self):
		cm = SkipBlanksCursorManager(text=self.multiline, selection = (8, 8)) # Caret at "d"
		cm.script_moveByLine_forward(None)
		self.assertEqual(cm.selectionOffsets, (13, 13)) # Caret at "4"

	def test_prevLine(self):
		cm = CursorManager(text=self.multiline, selection=(4, 4)) # Caret at "1"
		cm.script_moveByLine_back(None)
		self.assertEqual(cm.selectionOffsets, (0, 0)) # Caret at "a"

	def test_PrevLineNoBlankSkipping(self):
		cm = CursorManager(text=self.multiline, selection=(13, 13)) # Caret at "4"
		cm.script_moveByLine_back(None)
		self.assertEqual(cm.selectionOffsets, (12, 12)) # Caret at "\n"

	def test_prevLineBlankSkipping(self):
		cm = SkipBlanksCursorManager(text=self.multiline, selection = (13, 13)) # Caret at "4"
		cm.script_moveByLine_back(None)
		self.assertEqual(cm.selectionOffsets, (8, 8)) # Caret at "4"


class TestSelection(unittest.TestCase):

	def test_selectNextChar(self):
		cm = CursorManager(text="abc") # Caret at "a"
		cm.script_selectCharacter_forward(None)
		self.assertEqual(cm.selectionOffsets, (0, 1)) # "a" selected

	def test_selectPrevChar(self):
		cm = CursorManager(text="abc", selection=(1, 1)) # Caret at "b"
		cm.script_selectCharacter_back(None)
		self.assertEqual(cm.selectionOffsets, (0, 1)) # "a" selected

	def test_unselectPrevChar(self):
		"""Depends on behavior tested by test_selectNextChar.
		"""
		cm = CursorManager(text="abc") # Caret at "a"
		cm.script_selectCharacter_forward(None) # "a" selected
		cm.script_selectCharacter_back(None) # "a" unselected
		self.assertEqual(cm.selectionOffsets, (0, 0)) # Caret at "a", no selection

	def test_selForwardThenUnselThenSelBackward(self):
		"""Test selecting forward, then unselecting and selecting backward.
		Depends on behavior tested by test_unselectPrevChar.
		"""
		cm = CursorManager(text="abc", selection=(1, 1)) # Caret at "b"
		cm.script_selectCharacter_forward(None) # "b" selected
		cm.script_selectCharacter_back(None) # "b" unselected, caret at "b"
		cm.script_selectCharacter_back(None)
		self.assertEqual(cm.selectionOffsets, (0, 1)) # "a" selected

	def test_selectForwardThenSelBackward(self):
		"""Test selecting forward, then selecting backward without unselecting.
		Depends on behavior tested by test_selectNextChar.
		"""
		cm = CursorManager(text="abc", selection=(1, 1)) # Caret at "b"
		cm.script_selectCharacter_forward(None) # "b" selected
		cm.script_selectWord_back(None) # "b" unselected, "a" selected
		self.assertEqual(cm.selectionOffsets, (0, 1)) # "a" selected

class TestSelectAll(unittest.TestCase):
	"""Tests the select all command starting from different caret positions.
	"""

	def _selectAllTest(self, caret):
		"""Tests select all with the caret at the given offset.
		"""
		cm = CursorManager(text="abc", selection=(caret, caret))
		cm.script_selectAll(None)
		self.assertEqual(cm.selectionOffsets, (0, 3)) # "abc" selected

	def test_selectAllFromStart(self):
		self._selectAllTest(0) # Caret at "a"
