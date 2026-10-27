# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the add-on filtering logic in the NVDA Log Viewer."""

import unittest

from gui.logViewer import LogViewer

SAMPLE_LOG = (
	"INFO - core.main (09:00:00.100) - MainThread (1234):\n"
	"NVDA started\n"
	"DEBUG - external:globalPlugins.myAddon.MyGlobalPlugin.event_gainFocus (09:00:01.200) - MainThread (1234):\n"
	"Got focus event\n"
	"with a second message line\n"
	"IO - inputCore.InputManager.executeGesture (09:00:02.300) - Thread-5 (5678):\n"
	"kb(desktop):tab\n"
	"WARNING - external:globalPlugins.otherAddon.foo (09:00:03.400) - MainThread (1234):\n"
	"Some warning from a different addon\n"
	"ERROR - external:addons.myAddon_7f3a.installTasks.onInstall (09:00:04.500) - MainThread (1234):\n"
	"Traceback (most recent call last):\n"
	"  ...\n"
)


class TestIterLogEntries(unittest.TestCase):
	"""Tests for LogViewer._iterLogEntries."""

	def test_splitsIntoOneEntryPerHeader(self):
		entries = list(LogViewer._iterLogEntries(SAMPLE_LOG))
		self.assertEqual(len(entries), 5)

	def test_codepathCapturedPerEntry(self):
		entries = list(LogViewer._iterLogEntries(SAMPLE_LOG))
		codepaths = [codepath for codepath, _entryText in entries]
		self.assertEqual(
			codepaths,
			[
				"core.main",
				"external:globalPlugins.myAddon.MyGlobalPlugin.event_gainFocus",
				"inputCore.InputManager.executeGesture",
				"external:globalPlugins.otherAddon.foo",
				"external:addons.myAddon_7f3a.installTasks.onInstall",
			],
		)

	def test_entryTextIncludesMessageLines(self):
		entries = list(LogViewer._iterLogEntries(SAMPLE_LOG))
		_codepath, entryText = entries[1]
		self.assertIn("Got focus event", entryText)
		self.assertIn("with a second message line", entryText)

	def test_textBeforeFirstHeaderDiscarded(self):
		entries = list(LogViewer._iterLogEntries("some preamble\n" + SAMPLE_LOG))
		self.assertEqual(len(entries), 5)
		self.assertNotIn("preamble", "".join(entryText for _codepath, entryText in entries))

	def test_emptyTextYieldsNoEntries(self):
		self.assertEqual(list(LogViewer._iterLogEntries("")), [])


class TestCodepathMatchesPrefixes(unittest.TestCase):
	"""Tests for LogViewer._codepathMatchesPrefixes."""

	def test_exactMatch(self):
		self.assertTrue(LogViewer._codepathMatchesPrefixes("globalPlugins.foo", {"globalPlugins.foo"}))

	def test_subModuleMatch(self):
		self.assertTrue(
			LogViewer._codepathMatchesPrefixes(
				"globalPlugins.foo.MyClass.myFunc",
				{"globalPlugins.foo"},
			),
		)

	def test_externalPrefixStripped(self):
		self.assertTrue(
			LogViewer._codepathMatchesPrefixes(
				"external:globalPlugins.foo.MyClass.myFunc",
				{"globalPlugins.foo"},
			),
		)

	def test_unrelatedModuleDoesNotMatch(self):
		self.assertFalse(LogViewer._codepathMatchesPrefixes("globalPlugins.other", {"globalPlugins.foo"}))

	def test_prefixOfUnrelatedModuleDoesNotMatch(self):
		"""e.g. "globalPlugins.foo" must not match "globalPlugins.fooBar"."""
		self.assertFalse(LogViewer._codepathMatchesPrefixes("globalPlugins.fooBar", {"globalPlugins.foo"}))

	def test_coreCodepathDoesNotMatchAddon(self):
		self.assertFalse(LogViewer._codepathMatchesPrefixes("core.main", {"globalPlugins.foo"}))


class TestFilterIntegration(unittest.TestCase):
	"""End-to-end test of splitting and filtering together, as used by LogViewer._render."""

	def test_filteringKeepsOnlyMatchingEntries(self):
		prefixes = {"globalPlugins.myAddon", "addons.myAddon_7f3a"}
		filteredText = "".join(
			entryText
			for codepath, entryText in LogViewer._iterLogEntries(SAMPLE_LOG)
			if LogViewer._codepathMatchesPrefixes(codepath, prefixes)
		)
		self.assertIn("myAddon.MyGlobalPlugin", filteredText)
		self.assertIn("installTasks.onInstall", filteredText)
		self.assertNotIn("otherAddon", filteredText)
		self.assertNotIn("core.main", filteredText)
		self.assertNotIn("inputCore", filteredText)
