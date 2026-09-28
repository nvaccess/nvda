# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited

"""Unit tests for system utilities."""

import unittest
from unittest.mock import patch

import systemUtils
import winKernel


class TestPreventSystemIdle(unittest.TestCase):
	def setUp(self) -> None:
		systemUtils._persistentSystemIdlePreventionRequests = 0

	@patch("systemUtils.winBindings.kernel32.SetThreadExecutionState")
	def test_overlappingPersistentRequests(self, setThreadExecutionState) -> None:
		systemUtils.preventSystemIdle(preventDisplayTurningOff=True, persistent=True)
		systemUtils.preventSystemIdle(preventDisplayTurningOff=True, persistent=True)
		setThreadExecutionState.reset_mock()

		systemUtils.resetThreadExecutionState()
		setThreadExecutionState.assert_not_called()

		systemUtils.resetThreadExecutionState()
		setThreadExecutionState.assert_called_once_with(winKernel.ES_CONTINUOUS)
