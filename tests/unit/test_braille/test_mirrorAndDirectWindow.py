# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Pneuma Solutions
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for braille.BrailleMirror, braille.DirectBrailleWindow, braille.registerMirror, braille.unregisterMirror, and braille.injectGesture."""

import unittest
from unittest.mock import MagicMock, patch

import braille
import inputCore


class _CountingMirror(braille.BrailleMirror):
	"""A mirror that records every display() call."""

	def __init__(self, numCells_: int = 0) -> None:
		self._numCells_ = numCells_
		self.received: list[list[int]] = []

	def display(self, cells: list[int]) -> None:
		self.received.append(list(cells))

	def numCells(self) -> int:
		return self._numCells_


class TestBrailleMirrorRegistration(unittest.TestCase):
	"""Test register/unregisterMirror lifecycle."""

	def tearDown(self) -> None:
		# Ensure no mirrors leak between tests.
		for m in list(braille._registeredMirrors):
			braille.unregisterMirror(m)

	def test_registerAddsToList(self):
		m = _CountingMirror()
		braille.registerMirror(m)
		self.assertIn(m, braille._registeredMirrors)

	def test_unregisterRemovesFromList(self):
		m = _CountingMirror()
		braille.registerMirror(m)
		braille.unregisterMirror(m)
		self.assertNotIn(m, braille._registeredMirrors)

	def test_unregisterNonRegisteredIsSafe(self):
		m = _CountingMirror()
		# Should not raise.
		braille.unregisterMirror(m)

	def test_extensionPointsHookedOnFirstRegister(self):
		self.assertFalse(braille._registeredMirrors)
		m = _CountingMirror()
		braille.registerMirror(m)
		# The shared handler should now be registered.
		self.assertIn(braille._mirrorPreWriteCells, list(braille.pre_writeCells.handlers))

	def test_extensionPointsUnhookedAfterLastUnregister(self):
		m = _CountingMirror()
		braille.registerMirror(m)
		braille.unregisterMirror(m)
		self.assertNotIn(braille._mirrorPreWriteCells, list(braille.pre_writeCells.handlers))

	def test_multipleRegistrationsKeepHandlerOnce(self):
		m1 = _CountingMirror()
		m2 = _CountingMirror()
		braille.registerMirror(m1)
		braille.registerMirror(m2)
		# The shared pre_writeCells handler should be registered exactly once.
		self.assertEqual(list(braille.pre_writeCells.handlers).count(braille._mirrorPreWriteCells), 1)
		braille.unregisterMirror(m1)
		braille.unregisterMirror(m2)


class TestBrailleMirrorDisplay(unittest.TestCase):
	def tearDown(self) -> None:
		for m in list(braille._registeredMirrors):
			braille.unregisterMirror(m)

	def test_mirrorReceivesCellsOnWriteCells(self):
		m = _CountingMirror()
		braille.registerMirror(m)
		cells = [0] * braille.handler.displaySize
		braille.handler._writeCells(cells)
		self.assertEqual(len(m.received), 1)
		self.assertEqual(m.received[0], cells)

	def test_multipleMirrorsAllReceiveCells(self):
		m1 = _CountingMirror()
		m2 = _CountingMirror()
		braille.registerMirror(m1)
		braille.registerMirror(m2)
		cells = [1] * braille.handler.displaySize
		braille.handler._writeCells(cells)
		self.assertEqual(len(m1.received), 1)
		self.assertEqual(len(m2.received), 1)

	def test_unregisteredMirrorReceivesNothing(self):
		m = _CountingMirror()
		braille.registerMirror(m)
		braille.unregisterMirror(m)
		braille.handler._writeCells([0] * braille.handler.displaySize)
		self.assertEqual(m.received, [])


class TestBrailleMirrorNumCells(unittest.TestCase):
	def tearDown(self) -> None:
		for m in list(braille._registeredMirrors):
			braille.unregisterMirror(m)

	def test_numCellsZeroHasNoEffect(self):
		"""A mirror with numCells()==0 should not shrink the display width."""
		m = _CountingMirror(numCells_=0)
		braille.registerMirror(m)
		original = braille.handler.displayDimensions
		# Apply the mirror filter manually.
		result = braille._mirrorFilterDisplayDimensions(original)
		self.assertEqual(result, original)

	def test_numCellsShrinksCap(self):
		"""A mirror reporting fewer cells should cap numCols."""
		displayCols = braille.handler.displayDimensions.numCols
		cap = max(1, displayCols - 4)
		m = _CountingMirror(numCells_=cap)
		braille.registerMirror(m)
		original = braille.handler.displayDimensions
		result = braille._mirrorFilterDisplayDimensions(original)
		self.assertEqual(result.numCols, cap)

	def test_numCellsLargerThanDisplayHasNoEffect(self):
		"""A mirror reporting more cells than the display should not widen it."""
		displayCols = braille.handler.displayDimensions.numCols
		m = _CountingMirror(numCells_=displayCols + 100)
		braille.registerMirror(m)
		original = braille.handler.displayDimensions
		result = braille._mirrorFilterDisplayDimensions(original)
		self.assertEqual(result.numCols, displayCols)

	def test_smallestMirrorWins(self):
		"""When multiple mirrors are registered, the smallest positive numCells wins."""
		displayCols = braille.handler.displayDimensions.numCols
		small = max(1, displayCols - 10)
		big = max(1, displayCols - 5)
		m1 = _CountingMirror(numCells_=big)
		m2 = _CountingMirror(numCells_=small)
		braille.registerMirror(m1)
		braille.registerMirror(m2)
		original = braille.handler.displayDimensions
		result = braille._mirrorFilterDisplayDimensions(original)
		self.assertEqual(result.numCols, small)


class TestInjectGesture(unittest.TestCase):
	def test_injectGestureCallsExecuteGesture(self):
		gesture = MagicMock(spec=braille.BrailleDisplayGesture)
		mock_manager = MagicMock()
		with patch.object(inputCore, "manager", mock_manager):
			braille.injectGesture(gesture)
		mock_manager.executeGesture.assert_called_once_with(gesture)

	def test_injectGestureSwallowsNoInputGestureAction(self):
		gesture = MagicMock(spec=braille.BrailleDisplayGesture)
		mock_manager = MagicMock()
		mock_manager.executeGesture.side_effect = inputCore.NoInputGestureAction
		with patch.object(inputCore, "manager", mock_manager):
			# Should not raise.
			braille.injectGesture(gesture)


class TestDirectBrailleWindow(unittest.TestCase):
	"""Tests for DirectBrailleWindow using a mock foreground-window check."""

	FAKE_HWND = 0xDEADBEEF

	def setUp(self) -> None:
		self._win = braille.DirectBrailleWindow(hwnd=self.FAKE_HWND, numCells=0)

	def tearDown(self) -> None:
		self._win.deactivate()

	def _patch_foreground(self, is_fg: bool):
		return patch.object(self._win, "_isForeground", return_value=is_fg)

	def test_activateRegistersDecideEnabled(self):
		self._win.activate()
		self.assertIn(self._win._handleDecideEnabled, list(braille.decide_enabled.handlers))

	def test_deactivateUnregistersDecideEnabled(self):
		self._win.activate()
		self._win.deactivate()
		self.assertNotIn(self._win._handleDecideEnabled, list(braille.decide_enabled.handlers))

	def test_doubleActivateIsNoop(self):
		self._win.activate()
		self._win.activate()
		count = list(braille.decide_enabled.handlers).count(self._win._handleDecideEnabled)
		self.assertEqual(count, 1)
		self._win.deactivate()

	def test_doubleDeactivateIsNoop(self):
		self._win.activate()
		self._win.deactivate()
		# Second deactivate should not raise.
		self._win.deactivate()

	def test_handleDecideEnabledReturnsFalseWhenForeground(self):
		with self._patch_foreground(True):
			self.assertFalse(self._win._handleDecideEnabled())

	def test_handleDecideEnabledReturnsTrueWhenNotForeground(self):
		with self._patch_foreground(False):
			self.assertTrue(self._win._handleDecideEnabled())

	def test_gestureInterceptedWhenForeground(self):
		gesture = MagicMock(spec=braille.BrailleDisplayGesture)
		self._win.onGesture = MagicMock()
		with self._patch_foreground(True):
			result = self._win._handleDecideExecuteGesture(gesture)
		self.assertFalse(result)
		self._win.onGesture.assert_called_once_with(gesture)

	def test_gesturePassedThroughWhenNotForeground(self):
		gesture = MagicMock(spec=braille.BrailleDisplayGesture)
		self._win.onGesture = MagicMock()
		with self._patch_foreground(False):
			result = self._win._handleDecideExecuteGesture(gesture)
		self.assertTrue(result)
		self._win.onGesture.assert_not_called()

	def test_nonBrailleGestureAlwaysPassedThrough(self):
		gesture = MagicMock()  # Not a BrailleDisplayGesture
		with self._patch_foreground(True):
			result = self._win._handleDecideExecuteGesture(gesture)
		self.assertTrue(result)

	def test_numCellsZeroSkipsFilter(self):
		win = braille.DirectBrailleWindow(hwnd=self.FAKE_HWND, numCells=0)
		dims = braille.handler.displayDimensions
		with patch.object(win, "_isForeground", return_value=True):
			result = win._handleFilterDisplayDimensions(dims)
		self.assertEqual(result, dims)

	def test_numCellsCapsWhenForeground(self):
		displayCols = braille.handler.displayDimensions.numCols
		cap = max(1, displayCols - 4)
		win = braille.DirectBrailleWindow(hwnd=self.FAKE_HWND, numCells=cap)
		dims = braille.handler.displayDimensions
		with patch.object(win, "_isForeground", return_value=True):
			result = win._handleFilterDisplayDimensions(dims)
		self.assertEqual(result.numCols, cap)

	def test_numCellsIgnoredWhenNotForeground(self):
		displayCols = braille.handler.displayDimensions.numCols
		win = braille.DirectBrailleWindow(hwnd=self.FAKE_HWND, numCells=max(1, displayCols - 4))
		dims = braille.handler.displayDimensions
		with patch.object(win, "_isForeground", return_value=False):
			result = win._handleFilterDisplayDimensions(dims)
		self.assertEqual(result, dims)

	def test_numCellsLargerThanDisplayHasNoEffect(self):
		displayCols = braille.handler.displayDimensions.numCols
		win = braille.DirectBrailleWindow(hwnd=self.FAKE_HWND, numCells=displayCols + 100)
		dims = braille.handler.displayDimensions
		with patch.object(win, "_isForeground", return_value=True):
			result = win._handleFilterDisplayDimensions(dims)
		self.assertEqual(result.numCols, displayCols)

	def test_filterRegisteredWhenNumCellsPositive(self):
		win = braille.DirectBrailleWindow(hwnd=self.FAKE_HWND, numCells=20)
		win.activate()
		self.assertIn(win._handleFilterDisplayDimensions, list(braille.filter_displayDimensions.handlers))
		win.deactivate()

	def test_filterNotRegisteredWhenNumCellsZero(self):
		win = braille.DirectBrailleWindow(hwnd=self.FAKE_HWND, numCells=0)
		win.activate()
		self.assertNotIn(win._handleFilterDisplayDimensions, list(braille.filter_displayDimensions.handlers))
		win.deactivate()
