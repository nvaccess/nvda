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

class TestMove(unittest.TestCase):

	def test_nextChar(self):
		cm = CursorManager(text="abc") # Caret at "a"
		cm.script_moveByCharacter_forward(None)
		self.assertEqual(cm.selectionOffsets, (1, 1)) # Caret at "b"

	def test_prevChar(self):
		cm = CursorManager(text="abc", selection=(1, 1)) # Caret at "b"
		cm.script_moveByCharacter_back(None)
		self.assertEqual(cm.selectionOffsets, (0, 0)) # Caret at "a"

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

	def test_selectBackwardThenSelForward(self):
		"""Test selecting backward, then selecting forward without unselecting.
		Same as test_selectForwardThenSelBackward, but with reversed directions.
		"""
		cm = CursorManager(text="abc", selection=(2, 2)) # Caret at "c"
		cm.script_selectCharacter_back(None) # "b" selected
		cm.script_selectWord_forward(None) # "b" unselected, "c" selected
		self.assertEqual(cm.selectionOffsets, (2, 3)) # "c" selected

	def test_selectToBottom(self):
		cm = CursorManager(text="abc", selection=(1, 1)) # Caret at "b"
		cm.script_selectToBottomOfDocument(None)
		self.assertEqual(cm.selectionOffsets, (1, 3)) # "bc" selected

	def test_selectToTop(self):
		cm = CursorManager(text="abc", selection=(2, 2)) # Caret at "c"
		cm.script_selectToTopOfDocument(None)
		self.assertEqual(cm.selectionOffsets, (0, 2)) # "ab" selected

	def test_selectToEndOfLine(self):
		cm = CursorManager(text="ab\ncd", selection=(1, 1)) # Caret at "b"
		cm.script_selectToEndOfLine(None)
		self.assertEqual(cm.selectionOffsets, (1, 3)) # "b\n" selected

	def test_selectToBeginningOfLine(self):
		cm = CursorManager(text="ab\ncd", selection=(4, 4)) # Caret at "d"
		cm.script_selectToBeginningOfLine(None)
		self.assertEqual(cm.selectionOffsets, (3, 4)) # "c" selected

	def test_selectToBeginningOfLineAtBeginning(self):
		"""Test selecting to the beginning of the line when the caret is already at the beginning of the line.
		In this case, nothing should happen.
		"""
		cm = CursorManager(text="ab\ncd", selection=(3, 3)) # Caret at "c"
		cm.script_selectToBeginningOfLine(None)
		self.assertEqual(cm.selectionOffsets, (3, 3)) # No selection

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
