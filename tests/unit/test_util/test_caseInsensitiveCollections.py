# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited.

"""Unit tests for the caseInsensitiveCollections submodule."""

import unittest

from utils.caseInsensitiveCollections import CaseInsensitiveSet


class Test_CaseInsensitiveSet(unittest.TestCase):
	"""Tests should cover all expected uses of an instantiated CaseInsensitiveSet"""

	def test_caseInsensitiveInit(self):
		self.assertSetEqual(CaseInsensitiveSet({"foo", "FOO"}), CaseInsensitiveSet({"foo"}))

	def test_caseInsensitiveAdd(self):
		base = CaseInsensitiveSet({"foo"})
		base.add("FOO")
		self.assertSetEqual(base, CaseInsensitiveSet({"foo"}))

	def test_caseInsensitiveDiscard(self):
		base = CaseInsensitiveSet({"foo"})
		base.discard("FOO")
		self.assertSetEqual(base, CaseInsensitiveSet())

	def test_caseInsensitiveRemove(self):
		base = CaseInsensitiveSet({"foo"})
		base.remove("FOO")
		self.assertSetEqual(base, CaseInsensitiveSet())

	def test_caseInsensitiveIn(self):
		self.assertIn("FOO", CaseInsensitiveSet({"foo"}))

	def test_caseInsensitiveSubtract(self):
		base = CaseInsensitiveSet({"foo", "bar", "lorem"})
		base -= CaseInsensitiveSet({"foo", "BAR"})
		self.assertSetEqual(base, CaseInsensitiveSet({"lorem"}))

	def test_caseInsensitiveAddSet(self):
		base = CaseInsensitiveSet({"foo", "bar"})
		base |= CaseInsensitiveSet({"lorem", "BAR"})
		self.assertSetEqual(base, CaseInsensitiveSet({"foo", "bar", "lorem"}))
