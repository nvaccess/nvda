# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for deciding whether braille input is going into a text object."""

import unittest
from unittest.mock import Mock, patch

from braille.input.inputHandler import BrailleInputHandler
from compoundDocuments import CompoundDocument
from editableText import EditableText


def _currentFocusIsTextObj(focusObj) -> bool:
	with patch("api.getFocusObject", return_value=focusObj):
		# The getter doesn't use any instance state, so avoid constructing a full handler.
		return BrailleInputHandler._get_currentFocusIsTextObj(None)


class TestCurrentFocusIsTextObj(unittest.TestCase):
	def test_navigableTextWithoutTreeInterceptor(self):
		"""An edit field such as Notepad is a text object."""
		focusObj = Mock(_hasNavigableText=True, treeInterceptor=None)
		self.assertTrue(_currentFocusIsTextObj(focusObj))

	def test_nonNavigableTextWithoutTreeInterceptor(self):
		"""A button or list item is not a text object."""
		focusObj = Mock(_hasNavigableText=False, treeInterceptor=None)
		self.assertFalse(_currentFocusIsTextObj(focusObj))

	def test_browseModeIsNotTextObj(self):
		"""In browse mode, typed braille shouldn't be treated as text input."""
		treeInterceptor = Mock(passThrough=False)
		focusObj = Mock(_hasNavigableText=True, treeInterceptor=treeInterceptor)
		self.assertFalse(_currentFocusIsTextObj(focusObj))

	def test_focusModeIsTextObj(self):
		"""In focus mode, an editable field in a browse mode document is a text object."""
		treeInterceptor = Mock(passThrough=True)
		focusObj = Mock(_hasNavigableText=True, treeInterceptor=treeInterceptor)
		self.assertTrue(_currentFocusIsTextObj(focusObj))

	def test_editableTreeInterceptorIsTextObj(self):
		"""LibreOffice Writer uses a compound document tree interceptor which never uses pass through.
		Contracted braille input should still work there (#21141).
		"""
		treeInterceptor = Mock(spec=CompoundDocument, passThrough=False)
		self.assertIsInstance(treeInterceptor, EditableText)
		# The result shouldn't depend on whether the focused object inside the document reports navigable text.
		for hasNavigableText in (True, False):
			with self.subTest(hasNavigableText=hasNavigableText):
				focusObj = Mock(_hasNavigableText=hasNavigableText, treeInterceptor=treeInterceptor)
				self.assertTrue(_currentFocusIsTextObj(focusObj))
