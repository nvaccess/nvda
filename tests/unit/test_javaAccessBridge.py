# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022-2026 NV Access Limited, American Printing House for the Blind

"""Unit tests for Java Access Bridge"""

import queue
import unittest
from unittest.mock import call, MagicMock, patch

from NVDAObjects import JAB
import JABHandler
from JABHandler import AccessibleKeystroke


class TestJavaAccessBridge(unittest.TestCase):
	def test_plainTextNotModified(self):
		plainText = "Some plain text with no HTML tags."
		self.assertEqual(plainText, JAB._processHtml(plainText))

	def test_plainTextWithTagsNotModified(self):
		plainText = "<p>some <b>text</b>.</p>"
		self.assertEqual(plainText, JAB._processHtml(plainText))

	def test_regexNotModified(self):
		regexStr = "(<image[^>\\n]*)\\n([^>]*>)"
		self.assertEqual(regexStr, JAB._processHtml(regexStr))

	def test_htmlStringHasTagsRemoved(self):
		htmlStr = "<html><body><p>Some <b>bold</b> <i>text</i>.</p></body></html>"
		expected = "Some bold text ."
		self.assertEqual(expected, JAB._processHtml(htmlStr))


MODIFIER_COMBINATIONS = [
	{},
	{AccessibleKeystroke.ALT: "alt"},
	{AccessibleKeystroke.SHIFT: "shift"},
	{AccessibleKeystroke.CONTROL: "control"},
	{AccessibleKeystroke.CONTROL: "control", AccessibleKeystroke.SHIFT: "shift"},
	{
		AccessibleKeystroke.ALT: "alt",
		AccessibleKeystroke.CONTROL: "control",
		AccessibleKeystroke.SHIFT: "shift",
	},
	{AccessibleKeystroke.ALT: "alt", AccessibleKeystroke.SHIFT: "shift"},
	{AccessibleKeystroke.ALT: "alt", AccessibleKeystroke.CONTROL: "control"},
	{AccessibleKeystroke.ALT_GRAPH: "altgraph"},
	{AccessibleKeystroke.META: "meta"},
	{AccessibleKeystroke.BUTTON1: "button1"},
	{AccessibleKeystroke.BUTTON2: "button2"},
	{AccessibleKeystroke.BUTTON3: "button3"},
	{
		AccessibleKeystroke.BUTTON3: "button3",
		AccessibleKeystroke.BUTTON2: "button2",
		AccessibleKeystroke.BUTTON1: "button1",
		AccessibleKeystroke.ALT_GRAPH: "altgraph",
		AccessibleKeystroke.ALT: "alt",
		AccessibleKeystroke.META: "meta",
		AccessibleKeystroke.CONTROL: "control",
		AccessibleKeystroke.SHIFT: "shift",
	},
]
BASIC_SHORTCUT_KEYS = [chr(x) for x in range(ord("A"), ord("Z") + 1)]
FKEY_SHORTCUTS = [chr(x) for x in range(1, 25)]


class TestJavaAccessBridgeShortcutKeys(unittest.TestCase):
	def testBasicShortcut(self):
		for c in BASIC_SHORTCUT_KEYS:
			for modifierCombination in MODIFIER_COMBINATIONS:
				modifiers = 0
				modLabels = []
				for m, l in modifierCombination.items():  # noqa: E741
					modifiers |= m
					modLabels.append(l)
				with self.subTest(character=c, modifiers=modifiers, modLabels=modLabels):
					expected = modLabels + [c]
					self.assertListEqual(expected, JABHandler._getKeyLabels(modifiers, c))

	def testFKeyShortcut(self):
		for c in FKEY_SHORTCUTS:
			for modifierCombination in MODIFIER_COMBINATIONS:
				modifiers = AccessibleKeystroke.FKEY
				modLabels = []
				for m, l in modifierCombination.items():  # noqa: E741
					modifiers |= m
					modLabels.append(l)
				with self.subTest(fkey=ord(c), modifiers=modifiers, modLabels=modLabels):
					expected = modLabels + ["F{}".format(ord(c))]
					self.assertListEqual(expected, JABHandler._getKeyLabels(modifiers, c))

	def testControlCodeShortcut(self):
		for c, v in JABHandler.JABKeyControlCodesToLabels.items():
			for modifierCombination in MODIFIER_COMBINATIONS:
				modifiers = AccessibleKeystroke.CONTROLCODE
				modLabels = []
				for m, l in modifierCombination.items():  # noqa: E741
					modifiers |= m
					modLabels.append(l)
				with self.subTest(controlCode=c, label=v, modifiers=modifiers, modLabels=modLabels):
					expected = modLabels + [v]
					self.assertListEqual(expected, JABHandler._getKeyLabels(modifiers, chr(c)))


class TestInternalQueueFunction(unittest.TestCase):
	"""Tests for :func:`JABHandler.internalQueueFunction` eviction behaviour.

	These tests focus on the queue-full / eviction / retry-fail paths where
	JOBJECT64 handle leaks would otherwise occur when JAB events are produced
	faster than the main thread can consume them.
	"""

	@staticmethod
	def _placeholderHandler(vmID, accContext):
		"""Stand-in for a handler following the ``(vmID, accContext, ...)`` contract."""

	def test_normalEnqueue_doesNotReleaseHandle(self):
		"""A successful enqueue must not release the handle or touch bridgeDll."""
		fakeQueue = queue.Queue(3)
		with (
			patch.object(JABHandler, "bridgeDll") as mockBridgeDll,
			patch.object(JABHandler, "core") as mockCore,
			patch.object(JABHandler, "internalFunctionQueue", fakeQueue),
		):
			JABHandler.internalQueueFunction(self._placeholderHandler, 1, 100)
		mockBridgeDll.releaseJavaObject.assert_not_called()
		mockCore.requestPump.assert_called_once()
		self.assertEqual(fakeQueue.qsize(), 1)

	def test_fullQueue_evictsOldestAndReleasesItsHandle(self):
		"""When the queue is full, the oldest event's handle must be released."""
		fakeQueue = queue.Queue(3)
		with (
			patch.object(JABHandler, "bridgeDll") as mockBridgeDll,
			patch.object(JABHandler, "core") as mockCore,
			patch.object(JABHandler, "internalFunctionQueue", fakeQueue),
		):
			# Fill the queue to capacity.
			JABHandler.internalQueueFunction(self._placeholderHandler, 1, 100)
			JABHandler.internalQueueFunction(self._placeholderHandler, 1, 101)
			JABHandler.internalQueueFunction(self._placeholderHandler, 1, 102)
			self.assertEqual(mockBridgeDll.releaseJavaObject.call_count, 0)
			# One more — oldest (vmID=1, accContext=100) must be evicted and released.
			JABHandler.internalQueueFunction(self._placeholderHandler, 1, 9999)
		mockBridgeDll.releaseJavaObject.assert_called_once_with(1, 100)
		self.assertEqual(fakeQueue.qsize(), 3)
		self.assertEqual(mockCore.requestPump.call_count, 4)

	def test_fullQueue_withEnterJavaWindowHelper_skipsRelease(self):
		"""If the evicted event is enterJavaWindow_helper, no handle is released."""
		fakeQueue = queue.Queue(3)
		with (
			patch.object(JABHandler, "bridgeDll") as mockBridgeDll,
			patch.object(JABHandler, "core"),
			patch.object(JABHandler, "internalFunctionQueue", fakeQueue),
		):
			# Fill the queue with enterJavaWindow_helper calls (single-arg, no JOBJECT64).
			JABHandler.internalQueueFunction(JABHandler.enterJavaWindow_helper, 500)
			JABHandler.internalQueueFunction(JABHandler.enterJavaWindow_helper, 501)
			JABHandler.internalQueueFunction(JABHandler.enterJavaWindow_helper, 502)
			# Add a normal event — oldest is enterJavaWindow_helper → release must be skipped.
			JABHandler.internalQueueFunction(self._placeholderHandler, 1, 9999)
		mockBridgeDll.releaseJavaObject.assert_not_called()

	def test_evictionGuardsAgainstShortArgs(self):
		"""If an evicted non-enterJavaWindow_helper handler happens to carry fewer
		than two args, the guard must prevent a release attempt.

		This is defensive coverage: all current handlers follow the
		``(vmID, accContext, ...)`` contract, but the guard should still protect
		future additions from silent leaks or index errors.
		"""

		def shortArgsHandler(singleArg):
			pass

		fakeQueue = MagicMock()
		fakeQueue.put_nowait.side_effect = [queue.Full, None]
		fakeQueue.get_nowait.return_value = (shortArgsHandler, (42,), {})
		with (
			patch.object(JABHandler, "bridgeDll") as mockBridgeDll,
			patch.object(JABHandler, "core"),
			patch.object(JABHandler, "internalFunctionQueue", fakeQueue),
		):
			JABHandler.internalQueueFunction(self._placeholderHandler, 1, 9999)
		mockBridgeDll.releaseJavaObject.assert_not_called()

	def test_retryFullAfterEviction_releasesNewEventHandle(self):
		"""If the retry put_nowait also raises queue.Full, the new event's handle must be released."""
		fakeQueue = MagicMock()
		fakeQueue.put_nowait.side_effect = queue.Full
		fakeQueue.get_nowait.return_value = (self._placeholderHandler, (1, 100), {})
		with (
			patch.object(JABHandler, "bridgeDll") as mockBridgeDll,
			patch.object(JABHandler, "core") as mockCore,
			patch.object(JABHandler, "internalFunctionQueue", fakeQueue),
		):
			JABHandler.internalQueueFunction(self._placeholderHandler, 1, 9999)
		# Both handles released: evicted oldest (1, 100) and dropped new (1, 9999).
		self.assertEqual(
			mockBridgeDll.releaseJavaObject.call_args_list,
			[call(1, 100), call(1, 9999)],
		)
		# Early return before requestPump.
		mockCore.requestPump.assert_not_called()

	def test_emptyQueueDuringEviction_handlesGracefully(self):
		"""If get_nowait raises Empty and retry put_nowait still fails, only new handle is released."""
		fakeQueue = MagicMock()
		fakeQueue.put_nowait.side_effect = queue.Full
		fakeQueue.get_nowait.side_effect = queue.Empty
		with (
			patch.object(JABHandler, "bridgeDll") as mockBridgeDll,
			patch.object(JABHandler, "core") as mockCore,
			patch.object(JABHandler, "internalFunctionQueue", fakeQueue),
		):
			JABHandler.internalQueueFunction(self._placeholderHandler, 1, 9999)
		mockBridgeDll.releaseJavaObject.assert_called_once_with(1, 9999)
		mockCore.requestPump.assert_not_called()
