# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the NVDA Highlighter vision enhancement provider."""

import unittest
from unittest.mock import patch

from exceptions import LocationUnavailableError
from locationHelper import RectLTRB
from vision.constants import Context
from visionEnhancementProviders import NVDAHighlighter


class TestUpdateContextRect(unittest.TestCase):
	def setUp(self):
		# Avoid __init__, which starts the highlighter window thread.
		self.highlighter = NVDAHighlighter.NVDAHighlighter.__new__(NVDAHighlighter.NVDAHighlighter)
		self.highlighter.contextToRectMap = {Context.REVIEW: RectLTRB(10, 20, 30, 40)}
		patcher = patch.object(NVDAHighlighter.NVDAHighlighter, "enabledContexts", (Context.REVIEW,))
		patcher.start()
		self.addCleanup(patcher.stop)

	def test_unavailableLocationClearsHighlight(self):
		"""#20860: An unavailable location clears the highlight instead of raising."""
		with patch.object(NVDAHighlighter, "getContextRect", side_effect=LocationUnavailableError()):
			self.highlighter.updateContextRect(Context.REVIEW)
		self.assertIsNone(self.highlighter.contextToRectMap[Context.REVIEW])
