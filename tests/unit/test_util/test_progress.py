# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the utils._progress module."""

import unittest
from typing import Self

from utils._progress import ProgressStep, ProgressTracker


class _Steps(ProgressStep):
	FIRST = 1
	SECOND = 2

	@property
	def _displayStringLabels(self) -> dict[Self, str]:
		return {_Steps.FIRST: "First", _Steps.SECOND: "Second"}

	@property
	def _startPercentages(self) -> dict[Self, int]:
		return {_Steps.FIRST: 0, _Steps.SECOND: 20}


class Test_ProgressStep(unittest.TestCase):
	def test_startPercentage(self):
		self.assertEqual(_Steps.SECOND.startPercentage, 20)


class Test_ProgressTracker(unittest.TestCase):
	def setUp(self) -> None:
		self._reports: list[tuple[ProgressStep, int]] = []
		self._tracker = ProgressTracker(
			_Steps,
			lambda step, percentage: self._reports.append((step, percentage)),
		)

	def test_startStep_reportsStartOfStep(self):
		self._tracker.startStep(_Steps.FIRST)
		self._tracker.startStep(_Steps.SECOND)
		self.assertEqual(self._reports, [(_Steps.FIRST, 0), (_Steps.SECOND, 20)])

	def test_stepProgress_endsAtStartOfNextStep(self):
		self._tracker.startStep(_Steps.FIRST)
		self._tracker.stepProgress(1, 2)
		self._tracker.stepProgress(2, 2)
		self.assertEqual(self._reports, [(_Steps.FIRST, 0), (_Steps.FIRST, 10), (_Steps.FIRST, 20)])

	def test_stepProgress_ofLastStep_endsAtHundred(self):
		self._tracker.startStep(_Steps.SECOND)
		self._tracker.stepProgress(1, 2)
		self._tracker.stepProgress(2, 2)
		self.assertEqual(self._reports, [(_Steps.SECOND, 20), (_Steps.SECOND, 60), (_Steps.SECOND, 100)])

	def test_unchangedReports_areSkipped(self):
		self._tracker.startStep(_Steps.SECOND)
		for done in range(1, 6):
			self._tracker.stepProgress(done, 1000)
		self.assertEqual(self._reports, [(_Steps.SECOND, 20)])

	def test_percentage_neverDecreases(self):
		self._tracker.startStep(_Steps.SECOND)
		self._tracker.stepProgress(1, 2)
		self._tracker.startStep(_Steps.FIRST)
		self.assertEqual(self._reports, [(_Steps.SECOND, 20), (_Steps.SECOND, 60), (_Steps.FIRST, 60)])

	def test_stepProgress_withoutTotal_completesStep(self):
		self._tracker.startStep(_Steps.FIRST)
		self._tracker.stepProgress(0, 0)
		self.assertEqual(self._reports, [(_Steps.FIRST, 0), (_Steps.FIRST, 20)])

	def test_stepProgress_beyondTotal_staysWithinStep(self):
		self._tracker.startStep(_Steps.FIRST)
		self._tracker.stepProgress(3, 2)
		self.assertEqual(self._reports, [(_Steps.FIRST, 0), (_Steps.FIRST, 20)])

	def test_withoutCallback_reportsNothing(self):
		tracker = ProgressTracker(_Steps, None)
		tracker.startStep(_Steps.FIRST)
		tracker.stepProgress(1, 1)
