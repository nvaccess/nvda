# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the deferral of the full-screen magnifier's colour filter.

The filter is rate limited, so a call can run after the magnifier has stopped. By then the
screen curtain may own the full-screen colour effect, and reapplying the filter would reveal
the screen.
"""

from unittest.mock import patch

from _magnifier import commands
from _magnifier.fullscreenMagnifier import FullScreenMagnifier
from _magnifier.utils.filterHandler import FilterMatrix
from _magnifier.utils.types import Filter

from tests.unit.test_magnifier.test_magnifier import _TestMagnifier
from tests.unit.test_util.test_debounce import _FakeCallLater, _FakeClock


class TestFilterDeferral(_TestMagnifier):
	def setUp(self):
		super().setUp()
		self.clock = _FakeClock()
		self.callLater = _FakeCallLater()
		for patcher in (
			patch("utils.debounce.monotonic", new=self.clock.monotonic),
			patch("utils.debounce.wx.CallLater", new=self.callLater),
		):
			patcher.start()
			self.addCleanup(patcher.stop)
		self.fullscreenMagnifier = FullScreenMagnifier()
		self.fullscreenMagnifier.filterType = Filter.INVERTED
		self.addCleanup(setattr, self.fullscreenMagnifier, "_isActive", False)

	def _filterCallCount(self) -> int:
		calls = self.mock_mag_fs.MagSetFullscreenColorEffect.call_args_list
		return [call.args[0] for call in calls].count(FilterMatrix.INVERTED.value)

	def _deferAFilterCall(self) -> None:
		"""Leave exactly one delayed _applyFilter call pending."""
		self.clock.now = 0.0
		self.fullscreenMagnifier._applyFilter()
		self.clock.now = 0.05
		self.fullscreenMagnifier._applyFilter()

	def testDeferredFilterIsDroppedAfterStop(self):
		self.fullscreenMagnifier._startMagnifier()
		self._deferAFilterCall()
		countBeforeStop = self._filterCallCount()
		self.fullscreenMagnifier._stopMagnifier()
		self.clock.now = 0.5
		self.callLater.runPending()
		self.assertEqual(countBeforeStop, self._filterCallCount())

	def testFilterIsNotAppliedWhileInactive(self):
		"""A deferred call that outlived the stop must do nothing, even if it is not cancelled."""
		self.fullscreenMagnifier._startMagnifier()
		self.fullscreenMagnifier._stopMagnifier()
		countAfterStop = self._filterCallCount()
		self.clock.now = 10.0
		self.fullscreenMagnifier._applyFilter()
		self.assertEqual(countAfterStop, self._filterCallCount())

	def testPendingCallIsCancelledOnStop(self):
		self.fullscreenMagnifier._startMagnifier()
		self._deferAFilterCall()
		self.assertTrue(self.callLater.handles)
		self.fullscreenMagnifier._stopMagnifier()
		self.assertTrue(all(handle._stopped for handle in self.callLater.handles))

	def testDeferredFilterStillAppliesWhileActive(self):
		self.fullscreenMagnifier._startMagnifier()
		self._deferAFilterCall()
		countBeforeFiring = self._filterCallCount()
		self.clock.now = 0.5
		self.callLater.runPending()
		self.assertEqual(countBeforeFiring + 1, self._filterCallCount())

	def testStartMagnifierStillAppliesTheFilter(self):
		self.fullscreenMagnifier._startMagnifier()
		self.assertTrue(self.fullscreenMagnifier._isActive)
		self.assertGreaterEqual(self._filterCallCount(), 1)

	def testToggleFilterAppliesOnce(self):
		"""A single filter change must not leave a second, deferred application queued."""
		self.fullscreenMagnifier._startMagnifier()
		self.clock.now = 10.0
		self.fullscreenMagnifier.filterType = Filter.NORMAL
		self.clock.now = 20.0
		self.callLater.handles.clear()
		with (
			patch("_magnifier.commands.getMagnifier", return_value=self.fullscreenMagnifier),
			patch("_magnifier.commands.magnifierIsActiveVerify", return_value=True),
			patch("_magnifier.commands.setFilter"),
			patch("_magnifier.commands.ui.message"),
		):
			commands.toggleFilter()
		self.assertEqual(Filter.GRAYSCALE, self.fullscreenMagnifier.filterType)
		self.assertEqual([], self.callLater.handles)
