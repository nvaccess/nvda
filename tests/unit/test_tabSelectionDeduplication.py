# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Sanjeev Chaodhari
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for deduplication of selection events on focused ARIA tabs and controls."""

import unittest
from unittest.mock import Mock, patch

import api
import braille
from NVDAObjects.IAccessible.ia2Web import Ia2Web

from .objectProvider import PlaceholderNVDAObject


class TestTabSelectionDeduplication(unittest.TestCase):
	def test_event_selection_on_focused_object_does_not_report_focus(self):
		"""When event_selection fires on the currently focused object, focus should not be re-reported."""
		tab = PlaceholderNVDAObject()
		tab.reportFocus = Mock()
		tab.event_stateChange = Mock()

		with patch.object(api, "getFocusObject", return_value=tab):
			tab.event_selection()

		tab.reportFocus.assert_not_called()
		tab.event_stateChange.assert_called_once()

	def test_event_selection_on_controlled_descendant_reports_focus(self):
		"""When event_selection fires on a descendant of a control controlled by focus, focus is reported."""
		focus = PlaceholderNVDAObject()
		container = PlaceholderNVDAObject()
		item = PlaceholderNVDAObject()
		item.reportFocus = Mock()
		item.event_stateChange = Mock()

		with (
			patch.object(api, "getFocusObject", return_value=focus),
			patch.object(PlaceholderNVDAObject, "controllerFor", new=[container]),
			patch.object(PlaceholderNVDAObject, "isDescendantOf", return_value=True),
			patch.object(braille.handler, "message"),
		):
			item.event_selection()

		item.reportFocus.assert_called_once()

	def test_isDescendantOf_passes_candidate_unique_id_to_ancestor_accChild(self):
		"""isDescendantOf must query the candidate descendant's IA2UniqueID against the ancestor."""
		descendant = Mock(spec=Ia2Web)
		descendant.windowHandle = 1234
		descendant.IA2UniqueID = 999

		ancestor = Mock(spec=Ia2Web)
		ancestor.windowHandle = 1234
		ancestor.IA2UniqueID = 111
		ancestor.IAccessibleObject = Mock()
		ancestor.IAccessibleObject.accChild = Mock(return_value=Mock())

		result = Ia2Web.isDescendantOf(descendant, ancestor)
		ancestor.IAccessibleObject.accChild.assert_called_once_with(999)
		self.assertTrue(result)
