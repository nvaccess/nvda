# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022-2023 NV Access Limited, Leonard de Ruijter

"""Unit tests for the extension points in the braille module.
"""


import braille
from ..extensionPointTestHelpers import actionTester, deciderTester, filterTester
import unittest


class TestHandlerExtensionPoints(unittest.TestCase):
	"""A test for the several extension points on the braille handler."""

	def test_pre_writeCells(self):
		cells = [0] * braille.handler.displaySize
		braille.handler._rawText = " " * braille.handler.displaySize
		expectedKwargs = dict(
			cells=cells,
			rawText=braille.handler._rawText,
			currentCellCount=braille.handler.displaySize
		)

		with actionTester(self, braille.pre_writeCells, **expectedKwargs):
			braille.handler._writeCells(cells)

	def test_displaySizeChanged(self):
		expectedKwargs = dict(
			displaySize=braille.handler.displaySize
		)

		with actionTester(self, braille.displaySizeChanged, **expectedKwargs):
			# Change the attribute that is compared with the value coming from filter_displaySize
			braille.handler._displaySize = 0
			# The getter should now trigger the action.
			braille.handler._get_displaySize()

	def test_displayChanged(self):
		expectedKwargs = dict(
			isFallback=False,
			detected=None
		)

		with actionTester(self, braille.displayChanged, useAssertDictContainsSubset=True, **expectedKwargs):
			# Terminate the current noBraille instance to ensure that the action is triggered when choosing it again.
			braille.handler.display.terminate()
			braille.handler.display = None
			braille.handler.setDisplayByName("noBraille")

	def test_filter_displaySize(self):
		with filterTester(
			self,
			braille.filter_displaySize,
			braille.handler._displaySize,  # The currently cached display size
			20,   # The filter handler should change the display size to 40
		) as expectedOutput:
			self.assertEqual(braille.handler.displaySize, expectedOutput)

	def test_decide_enabled(self):
		with deciderTester(
			self,
			braille.decide_enabled,
			expectedDecision=False,
		) as expectedDecision:
			# Ensure that disabling braille by the decider doesn't try to call _handleEnabledDecisionFalse,
			# as that relies on wx.
			braille.handler._enabled = False
			self.assertEqual(braille.handler.enabled, expectedDecision)
