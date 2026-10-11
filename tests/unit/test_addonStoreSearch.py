# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Cary-rowen
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for add-on store search ranking."""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from gui.addonStoreGui.viewModels.addonList import AddonListItemVM


def _makeListItem(searchableText: str) -> AddonListItemVM:
	return AddonListItemVM(
		SimpleNamespace(
			listItemVMId="test-addon-stable",
			displayName="Test add-on",
			description=searchableText,
			addonId="testAddon",
		),
	)


class TestFuzzySearchRank(unittest.TestCase):
	def test_singleCharacterExactMatch_preservesExactSearch(self):
		self.assertEqual(_makeListItem("contains 剪").searchRank("剪"), 0.99)

	def test_singleCharacterNonMatch_skipsFuzzySearch(self):
		listItem = _makeListItem("unrelated add-on metadata")
		with patch("gui.addonStoreGui.viewModels.addonList.find_near_matches") as findNearMatches:
			self.assertEqual(listItem.searchRank("剪"), 0.0)
		findNearMatches.assert_not_called()

	def test_oneEditMatch_preservesExistingSequenceMatcherRank(self):
		self.assertEqual(_makeListItem("abxd").searchRank("abcd"), 0.75)
		self.assertEqual(_makeListItem("ac").searchRank("ab"), 0.5)

	def test_noMatch_returnsZero(self):
		self.assertEqual(_makeListItem("wxyz").searchRank("abcd"), 0.0)
