# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited, American Printing House for the Blind

"""Unit tests for Java Access Bridge"""

import unittest
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
		htmlStr = "<html><body><p>Some <b>bold</b> text.</p></body></html>"
		expected = "   Some  bold  text.   "
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
		AccessibleKeystroke.SHIFT: "shift"
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
		AccessibleKeystroke.SHIFT: "shift"
	}
]
BASIC_SHORTCUT_KEYS = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
FKEY_SHORTCUTS = [chr(x) for x in range(1, 25)]


class TestJavaAccessBridgeShortcutKeys(unittest.TestCase):
	def testBasicShortcut(self):
		for c in BASIC_SHORTCUT_KEYS:
			for modifierCombination in MODIFIER_COMBINATIONS:
				modifiers = 0
				modLabels = []
				for m, l in modifierCombination.items():
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
				for m, l in modifierCombination.items():
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
				for m, l in modifierCombination.items():
					modifiers |= m
					modLabels.append(l)
				with self.subTest(controlCode=c, label=v, modifiers=modifiers, modLabels=modLabels):
					expected = modLabels + [v]
					self.assertListEqual(expected, JABHandler._getKeyLabels(modifiers, chr(c)))
