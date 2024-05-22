# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited, Leonard de Ruijter

"""Unit tests for the move system caret when routing review cursor braille setting.
"""

import config
import braille
import textInfos
import api
import controlTypes
from ..textProvider import CursorManager
import unittest
import time
from config.featureFlagEnums import ReviewRoutingMovesSystemCaretFlag


class CursorManagerTextInfo(CursorManager.TextInfo):

	def updateCaret(self):
		super().updateCaret()
		self.obj.caretLastUpdateTime = time.time()

	def activate(self):
		self.obj.lastActivateTime = time.time()


class CursorManager(CursorManager):
	caretLastUpdateTime: float = 0.0
	lastActivateTime: float = 0.0
	TextInfo = CursorManagerTextInfo


class TestReviewRoutingMovesSystemCaretInNavigableText(unittest.TestCase):
	"""A test for the move system caret when routing review cursor braille setting
	when operating in navigable text with object review.
	"""

	cm: CursorManager

	def setUp(self):
		# Set tethering to review.
		braille.handler.setTether(braille.TetherTo.REVIEW.value)
		cmText = "the quick brown fox jumps over the lazy dog"
		cm = self.cm = CursorManager(text=cmText)
		cm.role = controlTypes.Role.EDITABLETEXT
		caret = self.caret = cm.makeTextInfo(textInfos.POSITION_CARET)
		api.setReviewPosition(caret)
		braille.handler.handleReviewMove()

	def test_moveCaret_never_moveReviewAndActivate(self):
		"""Test that routing action on a cell will move the review cursor when routing changes the position,
		whereas it should activate the current position when the review cursor is already at that position.
		The caret should never move.
		"""
		config.conf["braille"]["reviewRoutingMovesSystemCaret"] = ReviewRoutingMovesSystemCaretFlag.NEVER.name
		curTime = time.time()
		braille.handler.routeTo(3)  # Route to the fourth cell
		self.assertLess(self.cm.lastActivateTime, curTime)
		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
		self.assertEquals(caret, self.caret)
		expectedReview = self.caret.copy()
		expectedReview.move(textInfos.UNIT_CHARACTER, 3)
		self.assertEquals(expectedReview, api.getReviewPosition())
		braille.handler.routeTo(4)  # Route to the fifth cell
		# Object still not activated as no second routing press on same cell.
		self.assertLess(self.cm.lastActivateTime, curTime)
		# The caret shouldn't have been moved either
		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
		self.assertEquals(caret, self.caret)
		# move expected review from cell 4 to 5
		expectedReview.move(textInfos.UNIT_CHARACTER, 1)
		self.assertEquals(expectedReview, api.getReviewPosition())
		# Route a second time to activate the object under the cell
		braille.handler.routeTo(4)
		self.assertGreaterEqual(self.cm.lastActivateTime, curTime)
		# While the object is now activated, caret should have been steady.
		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
		self.assertEquals(caret, self.caret)

	def test_moveCaret_never_instantActivate(self):
		"""Test that routing action on a cell will activate the current position
		when the review cursor is already at that position.
		This test ensures that this behavior will work, even when it is the first routing action in a sequence.
		The caret should never move.
		"""
		config.conf["braille"]["reviewRoutingMovesSystemCaret"] = ReviewRoutingMovesSystemCaretFlag.NEVER.name
		curTime = time.time()
		review = self.caret.copy()
		review.move(textInfos.UNIT_CHARACTER, 3)
		api.setReviewPosition(review)
		# Route to the fourth cell to activate the object under the cell,
		# since the review cursor is already on that cell.
		braille.handler.routeTo(3)
		self.assertGreaterEqual(self.cm.lastActivateTime, curTime)
		# While the object is now activated, caret should have been steady.
		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
		self.assertEquals(caret, self.caret)

	def test_moveCaret_always_moveReviewAndActivate(self):
		"""Test that routing action on a cell will move the review cursor when routing changes the position,
		whereas it should activate the current position when the review cursor is already at that position.
		The caret should always move when routing.
		"""
		config.conf["braille"]["reviewRoutingMovesSystemCaret"] = ReviewRoutingMovesSystemCaretFlag.ALWAYS.name
		curTime = time.time()
		braille.handler.routeTo(3)  # Route to the fourth cell
		self.assertLess(self.cm.lastActivateTime, curTime)
		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
		expectedReview = self.caret.copy()
		expectedReview.move(textInfos.UNIT_CHARACTER, 3)
		self.assertEquals(expectedReview, api.getReviewPosition())
		self.assertEquals(caret, expectedReview)
		braille.handler.routeTo(4)  # Route to the fifth cell
		# Object still not activated as no second routing press on same cell.
		self.assertLess(self.cm.lastActivateTime, curTime)
		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
		# move expected review from cell 4 to 5
		expectedReview.move(textInfos.UNIT_CHARACTER, 1)
		self.assertEquals(expectedReview, api.getReviewPosition())
		self.assertEquals(caret, expectedReview)
		# Route a second time to activate the object under the cell
		braille.handler.routeTo(4)
		self.assertGreaterEqual(self.cm.lastActivateTime, curTime)
		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
		self.assertEquals(caret, expectedReview)

	def test_moveCaret_always_instantActivate(self):
		"""Test that routing action on a cell will activate the current position
		when the review cursor is already at that position.
		This test ensures that this behavior will work, even when it is the first routing action in a sequence.
		The caret should also have been moved even though routing didn't touch the review cursor position.
		"""
		config.conf["braille"]["reviewRoutingMovesSystemCaret"] = ReviewRoutingMovesSystemCaretFlag.ALWAYS.name
		curTime = time.time()
		review = self.caret.copy()
		review.move(textInfos.UNIT_CHARACTER, 3)
		api.setReviewPosition(review)
		self.assertNotEqual(self.caret, review)
		# Route to the fourth cell to activate the object under the cell,
		# since the review cursor is already on that cell.
		braille.handler.routeTo(3)
		self.assertGreaterEqual(self.cm.lastActivateTime, curTime)
		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
		self.assertEquals(caret, review)
