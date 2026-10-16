# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for NVDAObjects.IAccessible.MSHTML."""

import unittest
from unittest.mock import Mock

import textInfos
from comtypes import COMError
from NVDAObjects.IAccessible.MSHTML import MSHTMLTextInfo


class TestMSHTMLTextInfoSelection(unittest.TestCase):
	def setUp(self) -> None:
		self.obj = Mock(HTMLNodeName="BODY", isContentEditable=False)
		self.obj.HTMLNode.uniqueNumber = 1
		self.obj.HTMLNode.document.activeElement.uniqueNumber = 1
		self.selectionRange = self.obj.HTMLNode.document.selection.createRange.return_value
		self.elementRange = self.obj.HTMLNode.createTextRange.return_value
		# #20860: Moving to the selection's bookmark fails for some text, such as "𝔓".
		self.elementRange.MoveToBookmark.side_effect = COMError(-2147024809, "Invalid argument", None)

	def test_bodyCaretUsesSelectionRange(self) -> None:
		info = MSHTMLTextInfo(self.obj, textInfos.POSITION_CARET)
		self.assertIs(info._rangeObj, self.selectionRange)
		self.selectionRange.collapse.assert_called_once()
		self.elementRange.MoveToBookmark.assert_not_called()

	def test_bodySelectionUsesSelectionRange(self) -> None:
		info = MSHTMLTextInfo(self.obj, textInfos.POSITION_SELECTION)
		self.assertIs(info._rangeObj, self.selectionRange)
		self.selectionRange.collapse.assert_not_called()
		self.elementRange.MoveToBookmark.assert_not_called()

	def test_inactiveBodyIsRejected(self) -> None:
		self.obj.HTMLNode.document.activeElement.uniqueNumber = 2
		with self.assertRaises(RuntimeError):
			MSHTMLTextInfo(self.obj, textInfos.POSITION_CARET)

	def test_otherElementsStillUseBookmark(self) -> None:
		self.obj.HTMLNodeName = "INPUT"
		self.elementRange.MoveToBookmark.side_effect = None
		info = MSHTMLTextInfo(self.obj, textInfos.POSITION_CARET)
		self.assertIs(info._rangeObj, self.elementRange)
		self.elementRange.MoveToBookmark.assert_called_once_with(
			self.selectionRange.GetBookmark.return_value,
		)
