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

	def test_selForward(self):
		cm = CursorManager(text="abc") # Caret at "a"
		cm.script_selectCharacter_forward(None)
		self.assertEqual(cm.selectionOffsets, (0, 1)) # "a" selected

	def test_selBackward(self):
		"""Same as test_selForward, but with reversed direction.
		"""
		cm = CursorManager(text="abc", selection=(1, 1)) # Caret at "b"
		cm.script_selectCharacter_back(None)
		self.assertEqual(cm.selectionOffsets, (0, 1)) # "a" selected

	def test_selForwardThenUnsel(self):
		"""Depends on behavior tested by test_selForward.
		"""
		cm = CursorManager(text="abc") # Caret at "a"
		cm.script_selectCharacter_forward(None) # "a" selected
		cm.script_selectCharacter_back(None) # "a" unselected
		self.assertEqual(cm.selectionOffsets, (0, 0)) # Caret at "a", no selection

	def test_selBackwardThenUnsel(self):
		"""Depends on behavior tested by test_selBackward.
		Same as test_selForwardThenUnsel, but with reversed directions.
		"""
		cm = CursorManager(text="abc", selection=(1, 1)) # Caret at "b"
		cm.script_selectCharacter_back(None) # "a" selected
		cm.script_selectCharacter_forward(None) # "a" unselected
		self.assertEqual(cm.selectionOffsets, (1, 1)) # Caret at "b", no selection

	def test_selForwardTwice(self):
		"""Depends on behavior tested in test_selForward.
		"""
		cm = CursorManager(text="abc") # Caret at "a"
		cm.script_selectCharacter_forward(None) # "a" selected
		cm.script_selectCharacter_forward(None) # "b" selected
		self.assertEqual(cm.selectionOffsets, (0, 2)) # "ab" selected

	def test_selBackwardTwice(self):
		"""Depends on behavior tested in test_selBackward.
		Same as test_selForwardTwice, but with reversed directions.
		"""
		cm = CursorManager(text="abc", selection=(2, 2)) # Caret at "c"
		cm.script_selectCharacter_back(None) # "b" selected
		cm.script_selectCharacter_back(None) # "a" selected
		self.assertEqual(cm.selectionOffsets, (0, 2)) # "ab" selected

	def test_selForwardThenUnselThenSelBackward(self):
		"""Test selecting forward, then unselecting and selecting backward.
		Depends on behavior tested by test_selForwardThenUnsel.
		"""
		cm = CursorManager(text="abc", selection=(1, 1)) # Caret at "b"
		cm.script_selectCharacter_forward(None) # "b" selected
		cm.script_selectCharacter_back(None) # "b" unselected, caret at "b"
		cm.script_selectCharacter_back(None)
		self.assertEqual(cm.selectionOffsets, (0, 1)) # "a" selected

	def test_selBackwardThenUnselThenSelForward(self):
		"""Test selecting backward, then unselecting and selecting forward.
		Depends on behavior tested by test_selBackwardThenUnsel.
		Same as test_selForwardThenUnselThenSelBackward, but with reversed directions.
		"""
		cm = CursorManager(text="abc", selection=(1, 1)) # Caret at "b"
		cm.script_selectCharacter_back(None) # "a" selected
		cm.script_selectCharacter_forward(None) # "a" unselected, caret at "b"
		cm.script_selectCharacter_forward(None)
		self.assertEqual(cm.selectionOffsets, (1, 2)) # "b" selected

	def test_selForwardThenSelBackward(self):
		"""Test selecting forward, then selecting backward without unselecting.
		Depends on behavior tested by test_selForward.
		"""
		cm = CursorManager(text="abc", selection=(1, 1)) # Caret at "b"
		cm.script_selectCharacter_forward(None) # "b" selected
		cm.script_selectWord_back(None) # "b" unselected, "a" selected
		self.assertEqual(cm.selectionOffsets, (0, 1)) # "a" selected

	def test_selBackwardThenSelForward(self):
		"""Test selecting backward, then selecting forward without unselecting.
		Same as test_selForwardThenSelBackward, but with reversed directions.
		"""
		cm = CursorManager(text="abc", selection=(2, 2)) # Caret at "c"
		cm.script_selectCharacter_back(None) # "b" selected
		cm.script_selectWord_forward(None) # "b" unselected, "c" selected
		self.assertEqual(cm.selectionOffsets, (2, 3)) # "c" selected

	def test_selForwardThenSelBackwardThenUnsel(self):
		"""Test selecting forward, then selecting backward without unselecting, then unselecting forward.
		Depends on behavior tested by test_selForwardThenSelBackward.
		"""
		cm = CursorManager(text="abc", selection=(1, 1)) # Caret at "b"
		cm.script_selectCharacter_forward(None) # "b" selected
		cm.script_selectWord_back(None) # "b" unselected, "a" selected
		cm.script_selectCharacter_forward(None) # "a" unselected
		self.assertEqual(cm.selectionOffsets, (1, 1)) # Caret at "b", no selection

	def test_selBackwardThenSelForwardThenUnsel(self):
		"""Test selecting backward, then selecting forward without unselecting, then unselecting backward.
		Same as test_selForwardThenSelBackwardThenUnsel, but with reversed directions.
		Depends on behavior tested by test_selBackwardThenSelForward.
		"""
		cm = CursorManager(text="abc", selection=(2, 2)) # Caret at "c"
		cm.script_selectCharacter_back(None) # "b" selected
		cm.script_selectWord_forward(None) # "b" unselected, "c" selected
		cm.script_selectCharacter_back(None) # "c" unselected
		self.assertEqual(cm.selectionOffsets, (2, 2)) # Caret at "c", no selection

	def test_selToBottom(self):
		cm = CursorManager(text="abc", selection=(1, 1)) # Caret at "b"
		cm.script_selectToBottomOfDocument(None)
		self.assertEqual(cm.selectionOffsets, (1, 3)) # "bc" selected

	def test_selToTop(self):
		cm = CursorManager(text="abc", selection=(2, 2)) # Caret at "c"
		cm.script_selectToTopOfDocument(None)
		self.assertEqual(cm.selectionOffsets, (0, 2)) # "ab" selected

	def test_selToEndOfLine(self):
		cm = CursorManager(text="ab\ncd", selection=(1, 1)) # Caret at "b"
		cm.script_selectToEndOfLine(None)
		self.assertEqual(cm.selectionOffsets, (1, 3)) # "b\n" selected

	def test_selToBeginningOfLine(self):
		cm = CursorManager(text="ab\ncd", selection=(4, 4)) # Caret at "d"
		cm.script_selectToBeginningOfLine(None)
		self.assertEqual(cm.selectionOffsets, (3, 4)) # "c" selected

	def test_selToBeginningOfLineAtBeginning(self):
		"""Test selecting to the beginning of the line when the caret is already at the beginning of the line.
		In this case, nothing should happen.
		"""
		cm = CursorManager(text="ab\ncd", selection=(3, 3)) # Caret at "c"
		cm.script_selectToBeginningOfLine(None)
		self.assertEqual(cm.selectionOffsets, (3, 3)) # No selection

	def test_selForwardThenSelToBeginningOfLine(self):
		"""Depends on behavior tested by test_selForward.
		"""
		cm = CursorManager(text="ab\ncd", selection=(3, 3)) # Caret at "c"
		cm.script_selectCharacter_forward(None) # "c" selected
		cm.script_selectToBeginningOfLine(None) # "c" unselected
		self.assertEqual(cm.selectionOffsets, (3, 3)) # Caret at "c", no selection

	def test_selToEndThenBeginningOfLine(self):
		"""Test for #5746.
		Depends on behavior tested in test_selToEndOfLine and test_selToBeginningOfLine.
		"""
		cm = CursorManager(text="ab") # Caret at "a"
		cm.script_selectToEndOfLine(None)
		cm.script_selectToBeginningOfLine(None)
		self.assertEqual(cm.selectionOffsets, (0, 0)) # Caret at "a", no selection

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

	def test_selectAllFromMiddle(self):
		self._selectAllTest(1) # Caret at "b"

	def test_selectAllFromEnd(self):
		self._selectAllTest(2) # Caret at "c"
