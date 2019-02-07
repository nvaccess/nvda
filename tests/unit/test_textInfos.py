# -*- coding: UTF-8 -*-
#tests/unit/test_textInfos.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Babbage B.V.

"""Unit tests for the textInfos module, its submodules and classes."""

import unittest
from .textProvider import BasicTextProvider
import textInfos
from textInfos.offsets import Offsets

class TestCharacterOffsets(unittest.TestCase):
	"""
	Tests for textInfos.offsets.OffsetsTextInfo for its ability to deal with
	UTF-16 surrogate characters (i.e. whether a surrogate pair is treated as one character).
	"""

	def test_nonSurrogateForward(self):
		obj = BasicTextProvider(text="abc")
		ti = obj.makeTextInfo(Offsets(0, 0))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at a
		self.assertEqual(ti.offsets, (0, 1)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at b
		self.assertEqual(ti.offsets, (1, 2)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at c
		self.assertEqual(ti.offsets, (2, 3)) # One offset

	def test_nonSurrogateBackward(self):
		obj = BasicTextProvider(text="abc")
		ti = obj.makeTextInfo(Offsets(2, 2))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at c
		self.assertEqual(ti.offsets, (2, 3)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at b
		self.assertEqual(ti.offsets, (1, 2)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at a
		self.assertEqual(ti.offsets, (0, 1)) # One offset

	def test_surrogatePairsForward(self):
		obj = BasicTextProvider(text=u"\ud83e\udd26\ud83d\ude0a\ud83d\udc4d") # 🤦😊👍
		ti = obj.makeTextInfo(Offsets(0, 0))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🤦
		self.assertEqual(ti.offsets, (0, 2)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 😊
		self.assertEqual(ti.offsets, (2, 4)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 👍
		self.assertEqual(ti.offsets, (4, 6)) # Two offsets

	def test_surrogatePairsBackward(self):
		obj = BasicTextProvider(text=u"\ud83e\udd26\ud83d\ude0a\ud83d\udc4d") # 🤦😊👍
		ti = obj.makeTextInfo(Offsets(5, 5))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 👍
		self.assertEqual(ti.offsets, (4, 6)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 😊
		self.assertEqual(ti.offsets, (2, 4)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🤦
		self.assertEqual(ti.offsets, (0, 2)) # Two offsets

	def test_mixedSurrogatePairsAndNonSurrogatesForward(self):
		obj = BasicTextProvider(text=u"a\ud83e\udd26b") # a🤦b
		ti = obj.makeTextInfo(Offsets(0, 0))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at a
		self.assertEqual(ti.offsets, (0, 1)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🤦
		self.assertEqual(ti.offsets, (1, 3)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at c
		self.assertEqual(ti.offsets, (3, 4)) # One offset

	def test_mixedSurrogatePairsAndNonSurrogatesBackward(self):
		obj = BasicTextProvider(text=u"a\ud83e\udd26b") # a🤦b
		ti = obj.makeTextInfo(Offsets(3, 3))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at c
		self.assertEqual(ti.offsets, (3, 4)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🤦
		self.assertEqual(ti.offsets, (1, 3)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at a
		self.assertEqual(ti.offsets, (0, 1)) # One offset

	def test_mixedSurrogatePairsNonSurrogatesAndSingleSurrogatesForward(self):
		"""
		Tests surrogate pairs, non surrogates as well as
		single surrogate characters (i.e. incomplete pairs)
		"""
		obj = BasicTextProvider(text=u"a\ud83e\ud83e\udd26\udd26b")
		ti = obj.makeTextInfo(Offsets(0, 0))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at a
		self.assertEqual(ti.offsets, (0, 1)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🠀
		self.assertEqual(ti.offsets, (1, 2)) # Leading surrogate without a trailing surrogate
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🤦
		self.assertEqual(ti.offsets, (2, 4)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 񙠀
		self.assertEqual(ti.offsets, (4, 5)) # Trailing surrogate without a leading surrogate.
		ti.move(textInfos.UNIT_CHARACTER, 1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at c
		self.assertEqual(ti.offsets, (5, 6)) # One offset

	def test_mixedSurrogatePairsNonSurrogatesAndSingleSurrogatesBackward(self):
		obj = BasicTextProvider(text=u"a\ud83e\ud83e\udd26\udd26b")
		ti = obj.makeTextInfo(Offsets(5, 5))
		ti.expand(textInfos.UNIT_CHARACTER) # Range at c
		self.assertEqual(ti.offsets, (5, 6)) # One offset
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 񙠀
		self.assertEqual(ti.offsets, (4, 5)) # Trailing surrogate without a leading surrogate.
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🤦
		self.assertEqual(ti.offsets, (2, 4)) # Two offsets
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at 🠀
		self.assertEqual(ti.offsets, (1, 2)) # Leading surrogate without a trailing surrogate
		ti.move(textInfos.UNIT_CHARACTER, -1)
		ti.expand(textInfos.UNIT_CHARACTER) # Range at a
		self.assertEqual(ti.offsets, (0, 1)) # One offset

def createCaretAtEndTextProvider(text):
	"""Helper function to create a text provider that has its virtual caret positioned at the end of the text."""
	return BasicTextProvider(text=text, selection=(len(text),len(text)))

class TestFindWordBeforeCaret_result(unittest.TestCase):

	def test_wordSeparatorSpace(self):
		tp = createCaretAtEndTextProvider(text="The ")
		caret = tp.caret
		self.assertTrue(caret.findWordBeforeCaret(" "))
		# Note: the space is part of the word itself, in which is differs from other word separators
		self.assertEqual(caret.text, "The ")

	def test_wordSeparatorDot(self):
		tp = createCaretAtEndTextProvider(text="The.")
		caret = tp.caret
		self.assertTrue(caret.findWordBeforeCaret("."))
		self.assertEqual(caret.text, "The")

	def test_wordSeparatorComma(self):
		tp = createCaretAtEndTextProvider(text="The,")
		caret = tp.caret
		self.assertTrue(caret.findWordBeforeCaret(","))
		self.assertEqual(caret.text, "The")

	def test_invalidWordSeparator(self):
		"""An alphanumeric character is not considered a word separator in all cases."""
		tp = createCaretAtEndTextProvider(text="The")
		self.assertFalse(tp.caret.findWordBeforeCaret("e"))

	def test_layoutUSInternational(self):
		"""
		The US Internationa keyboard layout has several word separator characters (i.e. ' ` ") that aren't send to the application directly.
		Typing "'e" results in "é", etc.
		Typing "'t" results in "'t", but both characters are sent at once.
		This means that, typing "'t" results in word echo triggered on "'", but the caret is already behind "t".
		Note that uniscribe and many other implementations do not treat "'" as word separator in "won't"
		"""
		tp = createCaretAtEndTextProvider(text="Won't")
		caret = tp.caret
		self.assertTrue(caret.findWordBeforeCaret("'"))
		# The word before the caret is won, 
		self.assertEqual(caret.text, "Won")

class TestFindWordBeforeCaret_exceptions(unittest.TestCase):
	"""
	L{findWordBeforeCaret} raises an exepsion if no suitable word could be found,
	in which case the word echo system falls back to the buffer based system.
	"""

	def test_textInfoNotInitializedAtCaret(self):
		tp = BasicTextProvider(text="")
		# Using the selection instead of the caret should fail
		self.assertRaises(RuntimeError, tp.selection.findWordBeforeCaret)

	def test_noWordBeforeCaret(self):
		tp = BasicTextProvider(text="")
		self.assertRaises(LookupError, tp.caret.findWordBeforeCaret)

	def test_onlySpaces(self):
		tp = createCaretAtEndTextProvider(text="     ")
		self.assertRaises(LookupError, tp.caret.findWordBeforeCaret)
