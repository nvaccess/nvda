# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Cary-rowen
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for .NET Framework WinForms UIA combo boxes."""

from unittest import TestCase
from unittest.mock import Mock, patch

import api
import eventHandler
from NVDAObjects.UIA import ListItem, UIA, _NetFrameworkWinFormsComboBox
from winBindings import user32


class _TestNetFrameworkWinFormsComboBox(_NetFrameworkWinFormsComboBox):
	processID: int = 1
	windowHandle: int = 100


class _ComboLBoxListItem(ListItem):
	processID: int = 1
	windowClassName: str = "ComboLBox"
	windowHandle: int = 200


class _OtherProcessComboLBoxListItem(_ComboLBoxListItem):
	processID: int = 2


class _OtherWindowClassListItem(_ComboLBoxListItem):
	windowClassName: str = "OtherWindowClass"


class TestNetFrameworkWinFormsComboBox(TestCase):
	def setUp(self) -> None:
		self.comboBox: _TestNetFrameworkWinFormsComboBox = object.__new__(
			_TestNetFrameworkWinFormsComboBox,
		)
		self.comboBox.event_valueChange = Mock()

	def test_initOverlayClassRequestsElementSelectedEvents(self) -> None:
		with patch.object(eventHandler, "requestEvents", autospec=True) as requestEvents:
			self.comboBox.initOverlayClass()
		requestEvents.assert_called_once_with(
			"UIA_elementSelected",
			processId=1,
			windowClassName="ComboLBox",
		)

	def test_elementSelectedForwardsValueChange(self) -> None:
		listItem = object.__new__(_ComboLBoxListItem)
		comboBoxInfo = user32.COMBOBOXINFO(hwndList=listItem.windowHandle)
		with (
			patch.object(api, "getFocusObject", return_value=self.comboBox),
			patch.object(user32, "COMBOBOXINFO", return_value=comboBoxInfo),
			patch.object(user32, "GetComboBoxInfo", return_value=True) as getComboBoxInfo,
			patch.object(UIA, "event_UIA_elementSelected", autospec=True) as baseHandler,
		):
			listItem.event_UIA_elementSelected()
		baseHandler.assert_called_once_with(listItem)
		getComboBoxInfo.assert_called_once()
		self.assertEqual(self.comboBox.windowHandle, getComboBoxInfo.call_args.args[0])
		self.comboBox.event_valueChange.assert_called_once_with()

	def test_elementSelectedFromAnotherComboBoxDoesNotForwardValueChange(self) -> None:
		listItem = object.__new__(_ComboLBoxListItem)
		comboBoxInfo = user32.COMBOBOXINFO(hwndList=listItem.windowHandle + 1)
		with (
			patch.object(api, "getFocusObject", return_value=self.comboBox),
			patch.object(user32, "COMBOBOXINFO", return_value=comboBoxInfo),
			patch.object(user32, "GetComboBoxInfo", return_value=True),
			patch.object(UIA, "event_UIA_elementSelected", autospec=True) as baseHandler,
		):
			listItem.event_UIA_elementSelected()
		baseHandler.assert_called_once_with(listItem)
		self.comboBox.event_valueChange.assert_not_called()

	def test_unrelatedElementSelectedDoesNotForwardValueChange(self) -> None:
		for listItemClass, focus in (
			(_OtherProcessComboLBoxListItem, self.comboBox),
			(_OtherWindowClassListItem, self.comboBox),
			(_ComboLBoxListItem, Mock(processID=1)),
		):
			with self.subTest(listItemClass=listItemClass, focus=focus):
				focus.event_valueChange.reset_mock()
				listItem = object.__new__(listItemClass)
				with (
					patch.object(api, "getFocusObject", return_value=focus),
					patch.object(UIA, "event_UIA_elementSelected", autospec=True) as baseHandler,
				):
					listItem.event_UIA_elementSelected()
				baseHandler.assert_called_once_with(listItem)
				focus.event_valueChange.assert_not_called()
