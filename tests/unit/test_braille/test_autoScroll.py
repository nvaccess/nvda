# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited

"""Unit tests for braille automatic scrolling."""

import unittest
from unittest.mock import Mock, patch

from braille.brailleHandler import BrailleHandler


class TestAutoScroll(unittest.TestCase):
	@patch("braille.brailleHandler.systemUtils")
	@patch("braille.brailleHandler.wx.CallLater")
	def test_preventsSystemIdleUntilDisabled(self, callLater: Mock, systemUtils: Mock) -> None:
		handler = Mock()
		handler.enabled = True
		handler._autoScrollCallLater = None

		BrailleHandler.autoScroll(handler, enable=True)

		systemUtils.preventSystemIdle.assert_called_once_with(persistent=True)

		handler.enabled = False
		BrailleHandler.autoScroll(handler, enable=False)

		callLater.return_value.Stop.assert_called_once_with()
		systemUtils.resetThreadExecutionState.assert_called_once_with()
