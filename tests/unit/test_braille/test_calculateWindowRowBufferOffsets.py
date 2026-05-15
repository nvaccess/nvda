# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2026 NV Access Limited, Noelia Ruiz Martínez, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the _calculateWindowRowBufferOffsets function in the braille module."""

import unittest

import braille
import config
from config.featureFlag import FeatureFlag
from config.featureFlagEnums import BrailleTextWrapFlag


def _getDisplayDimensions(dimensions: braille.DisplayDimensions) -> braille.DisplayDimensions:
	"""Used to build a braille handler with particular dimensions."""
	return braille.DisplayDimensions(
		numRows=2,
		numCols=20,
	)


def _setTextWrap(mode: BrailleTextWrapFlag) -> None:
	"""Write a `BrailleTextWrapFlag` value to the config as a `FeatureFlag`.

	`behaviorOfDefault` is only meaningful when `mode` is `DEFAULT`; for any explicit value,
	we pick an arbitrary non-DEFAULT member to satisfy the `FeatureFlag` constructor assertions.
	"""
	behaviorOfDefault = (
		BrailleTextWrapFlag.AT_WORD_BOUNDARIES
		if mode != BrailleTextWrapFlag.AT_WORD_BOUNDARIES
		else BrailleTextWrapFlag.MARK_WORD_CUTS
	)
	config.conf["braille"]["textWrap"] = FeatureFlag(mode, behaviorOfDefault)


class TestCalculate(unittest.TestCase):
	def setUp(self):
		braille.filter_displayDimensions.register(_getDisplayDimensions)

	def tearDown(self):
		braille.filter_displayDimensions.unregister(_getDisplayDimensions)
		_setTextWrap(BrailleTextWrapFlag.NONE)

	def test_noCells(self):
		"""Check that, if list of braille cells is empty, offsets will be (0, 0)."""
		braille.handler.buffer.brailleCells = []
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 0)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)

	def test_firstPosition(self):
		"""Checks that first offset is equal to start parameter."""
		braille.handler.buffer.brailleCells = [1] * braille.handler.displaySize
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 20), (20, 40)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)
		braille.handler.buffer._calculateWindowRowBufferOffsets(1)
		expectedOffsets = [(1, 21), (21, 40)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)

	def test_end(self):
		"""Check that last row offset won't be greater than length of list of braille cells."""
		braille.handler.buffer.brailleCells = [1] * (braille.handler.displaySize - 10)
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 20), (20, 30)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)
		braille.handler.buffer.brailleCells = [1] * braille.handler.displaySize
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 20), (20, 40)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)

	def test_textWrapFirstRowWithSpace(self):
		"""Check that the first row will be truncated if it contains a space, only if text wrap is set to word boundaries."""
		_setTextWrap(BrailleTextWrapFlag.AT_WORD_BOUNDARIES)
		cells = [1] * (braille.handler.displayDimensions.numCols - 5)
		cells.append(0)
		cells.extend([1] * (braille.handler.displayDimensions.numCols + 4))
		braille.handler.buffer.brailleCells = cells
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 16), (16, 35)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)
		_setTextWrap(BrailleTextWrapFlag.NONE)
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 20), (20, 40)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)

	def test_textWrapSecondRowStartsWithSpace(self):
		"""Check that the first row won't be truncated if the next row starts with a space, even if text wrap is not NONE."""
		_setTextWrap(BrailleTextWrapFlag.AT_WORD_BOUNDARIES)
		cells = [1] * braille.handler.displayDimensions.numCols
		cells.append(0)
		cells.extend([1] * (braille.handler.displayDimensions.numCols - 1))
		braille.handler.buffer.brailleCells = cells
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 20), (20, 40)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)
		_setTextWrap(BrailleTextWrapFlag.NONE)
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)

	def test_none_hardCutsAtDisplayEdge(self):
		"""NONE wraps at the raw display edge with no continuation marker, even mid-word."""
		_setTextWrap(BrailleTextWrapFlag.NONE)
		# 25 consecutive non-zero cells: no space anywhere in the first row.
		braille.handler.buffer.brailleCells = [1] * 25
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, [(0, 20), (20, 25)])
		self.assertEqual(braille.handler.buffer._continuationRows, [])

	def test_markWordCuts_oneCellEarlierAndMarksRow(self):
		"""MARK_WORD_CUTS cuts one cell earlier than NONE and records the row in _continuationRows."""
		_setTextWrap(BrailleTextWrapFlag.MARK_WORD_CUTS)
		braille.handler.buffer.brailleCells = [1] * 25
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		# With MARK_WORD_CUTS, the end is pulled back by 1 to leave room for the marker.
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets[0], (0, 19))
		self.assertIn(0, braille.handler.buffer._continuationRows)

	def test_markWordCuts_cleanRowHasNoMarker(self):
		"""MARK_WORD_CUTS does not mark a row that ends naturally at a space."""
		_setTextWrap(BrailleTextWrapFlag.MARK_WORD_CUTS)
		# Row of 20 cells where cell 19 is a space (0): no mid-word cut.
		cells = [1] * 19 + [0] + [1] * 10
		braille.handler.buffer.brailleCells = cells
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		self.assertNotIn(0, braille.handler.buffer._continuationRows)

	def test_atWordBoundaries_noSpaceInWindowMarksCut(self):
		"""AT_WORD_BOUNDARIES with no whitespace in the window hard-cuts AND marks the row."""
		_setTextWrap(BrailleTextWrapFlag.AT_WORD_BOUNDARIES)
		# No zero anywhere in row 0; the `rindex` call raises and falls through.
		braille.handler.buffer.brailleCells = [1] * 25
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets[0], (0, 19))
		self.assertIn(0, braille.handler.buffer._continuationRows)
