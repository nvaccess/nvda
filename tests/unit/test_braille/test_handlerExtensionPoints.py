# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022-2025 NV Access Limited, Leonard de Ruijter

"""Unit tests for the extension points in the braille module."""

import braille
from ..extensionPointTestHelpers import actionTester, deciderTester, filterTester
import unittest
from braille.display import DisplayDimensions
from braille.extensions import (
	decide_enabled,
	displayChanged,
	displaySizeChanged,
	filter_displayDimensions,
	filter_displaySize,
	pre_writeCells,
)


class TestHandlerExtensionPoints(unittest.TestCase):
	"""A test for the several extension points on the braille handler."""

	def test_pre_writeCells(self):
		cells = [0] * braille.getHandler().displaySize
		braille.getHandler()._rawText = " " * braille.getHandler().displaySize
		expectedKwargs = dict(
			cells=cells,
			rawText=braille.getHandler()._rawText,
			currentCellCount=braille.getHandler().displaySize,
		)

		with actionTester(self, pre_writeCells, **expectedKwargs):
			braille.getHandler()._writeCells(cells)

	def test_displaySizeChanged(self):
		expectedKwargs = dict(
			displaySize=braille.getHandler().displaySize,
			numRows=1,
			numCols=braille.getHandler().displaySize,
		)

		with actionTester(self, displaySizeChanged, **expectedKwargs):
			# Change the internal cache of the display size to trigger the action when getting the display size.
			braille.getHandler()._displayDimensions = DisplayDimensions(1, 0)
			# The getter should now trigger the action.
			braille.getHandler()._get_displaySize()

	def test_displayChanged(self):
		expectedKwargs = dict(
			isFallback=False,
			detected=None,
		)

		with actionTester(self, displayChanged, useAssertDictContainsSubset=True, **expectedKwargs):
			# Terminate the current noBraille instance to ensure that the action is triggered when choosing it again.
			braille.getHandler().display.terminate()
			braille.getHandler().display = None
			braille.getHandler().setDisplayByName("noBraille")

	def test_filter_displayDimensions(self):
		cachedDisplayDimensions = braille.getHandler().displayDimensions
		with filterTester(
			self,
			filter_displayDimensions,
			cachedDisplayDimensions,
			DisplayDimensions(5, 20),
		) as expectedOutput:
			self.assertEqual(braille.getHandler().displayDimensions, expectedOutput)
			self.assertEqual(
				braille.getHandler().displayDimensions.displaySize,
				expectedOutput.numRows * expectedOutput.numCols,
			)

	def test_filter_displaySize(self):
		cachedDisplaySize = braille.getHandler().displaySize
		with filterTester(
			self,
			filter_displaySize,
			cachedDisplaySize,  # The currently cached display size
			20,  # The filter handler should change the display size to 20
		) as expectedOutput:
			self.assertEqual(braille.getHandler().displaySize, expectedOutput)
			self.assertEqual(braille.getHandler().displayDimensions.numCols, expectedOutput)
			self.assertEqual(braille.getHandler().displayDimensions.numRows, 1)

	def test_decide_enabled(self):
		with deciderTester(
			self,
			decide_enabled,
			expectedDecision=False,
		) as expectedDecision:
			# Ensure that disabling braille by the decider doesn't try to call _handleEnabledDecisionFalse,
			# as that relies on wx.
			braille.getHandler()._enabled = False
			self.assertEqual(braille.getHandler().enabled, expectedDecision)
