# tests/unit/test_sentenceNavigation.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited
""" Unit tests for sentence navigation."""

import unittest
from .textProvider import BasicTextProvider
from textInfos.offsets import Offsets
from documentNavigation import sentenceNavigation


class TestSentenceNavigation(unittest.TestCase):
	def runTestImpl(self, text: str, expected: str, direction: int = 0):
		caretOffset = text.index("^")
		text = text.replace("^", "")
		expected = expected.replace("^", "")
		obj = BasicTextProvider(text=text)
		info = obj.makeTextInfo(Offsets(caretOffset, caretOffset))
		context = sentenceNavigation.SentenceContext(info)
		result = context.moveSentence(direction)
		resultText = result.text
		self.assertEqual(resultText, expected)

	def test_simple(self):
		self.runTestImpl(
			"Hello. ^My name is John Smith. Good bye!",
			"My name is John Smith. ",
		)
		self.runTestImpl(
			"Hello. My name is Jo^hn Smith. Good bye!",
			"My name is John Smith. ",
		)
		self.runTestImpl(
			"Hello. My name is John Smith.^ Good bye!",
			"My name is John Smith. ",
		)
		self.runTestImpl(
			"Hello.^ My name is John Smith. Good bye!",
			"Hello. ",
		)
		self.runTestImpl(
			"Hello. My name is John Smith. ^Good bye!",
			"Good bye!",
		)
		self.runTestImpl(
			"Hello. ^My name is John Smith. Good bye!",
			"My name is John Smith. ",
		)

	def test_wiki(self):
		self.runTestImpl(
			"The Greek god of blacksmiths, Hephaestus, created several different humanoid automata in various myths. "
			"In Homer's Iliad, ^Hephaestus created golden handmaidens and imbued them with human-like voices.[1] "
			"Another Greek myth details how Hephaestus crafted a giant bronze automaton named Talos.[2]",
			"In Homer's Iliad, ^Hephaestus created golden handmaidens and imbued them with human-like voices.[1] "
		)

	def test_reconstructAcrossParagraphs(self):
		self.runTestImpl(
			"""
				lorem ipsum. One must be
				careful of books, and
				what is inside them, for
				words have the power to
				^change us.
			""",
			"""One must be
				careful of books, and
				what is inside them, for
				words have the power to
				change us.\n""",
		)

	def test_nonBreakingPrefixes(self):
		self.runTestImpl(
			"^J. R. R. Tolkien",
			"J. R. R. Tolkien",
		)
		self.runTestImpl(
			"^I enjoy playing various sports, i.e., basketball, soccer, and tennis, etc. Lorem ipsum.",
			"I enjoy playing various sports, i.e., basketball, soccer, and tennis, etc. ",
		)

	def test_doubleNewLine(self):
		self.runTestImpl(
			"""^This is a

			test.""",
			"""This is a\n\n""",
		)

	def test_exclamationQuestionMarks(self):
		self.runTestImpl(
			"What’s in a name? That ^which we call a rose By any other name would smell as sweet! Lorem ipsum.",
			"That which we call a rose By any other name would smell as sweet! ",
		)

	def test_negative(self):
		self.runTestImpl(
			"^A. b.b 5.0 42. test,. test.... Lorem ipsum",
			"A. b.b 5.0 42. test,. test.... Lorem ipsum",
		)

	def test_quote(self):
		self.runTestImpl(
			'^"So we beat on, boats against the current, borne back ceaselessly into the past." Lorem ipsum',
			'"So we beat on, boats against the current, borne back ceaselessly into the past." ',
		)

	def test_movement(self):
		gatsby = [
			"Gatsby believed in the green light, the orgastic future that year by year recedes before us. ",
			"So we beat on, boats against the current, borne back ceaselessly into the past. ",
			"I am still a little afraid of missing something if I forget that, as my father snobbishly "
			"suggested, and I snobbishly repeat, a sense of the fundamental decencies is parcelled out unequally "
			"at birth. "
		]
		greatGatsby = gatsby[0] + "^" + gatsby[1] + gatsby[2]
		for direction in [-1, 0, 1]:
			self.runTestImpl(
				greatGatsby,
				gatsby[1 + direction],
				direction=direction,
			)
