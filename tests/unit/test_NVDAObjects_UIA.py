# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Cary-rowen
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for NVDAObjects.UIA."""

import unittest
from unittest.mock import Mock, patch

import api
import controlTypes
import eventHandler
from NVDAObjects.UIA import ListItem, MenuItem, UIA, _NetFrameworkWinFormsComboBox
import oleacc
import UIAHandler
from winBindings import user32


class TestMenuItemDescription(unittest.TestCase):
	def test_legacyDescriptionFallback(self) -> None:
		menuItem = object.__new__(MenuItem)
		menuItem.name = "Name"
		menuItem.UIAElement = Mock(
			cachedFrameworkID="WinForm",
			cachedProviderDescription=(
				"managed:System.Windows.Forms.ToolStripMenuItem+ToolStripMenuItemAccessibleObject, "
				"System.Windows.Forms, Version=4.0.0.0"
			),
		)
		notSupportedValue = object()
		testCases = (
			("UIA description", "Legacy description", "UIA description", False),
			("", "Legacy description", "Legacy description", True),
			("Name", "Legacy description", "Legacy description", True),
			("Name", "Name", None, True),
			("Name", notSupportedValue, None, True),
		)
		for uiaDescription, legacyDescription, expectedDescription, shouldReadLegacyDescription in testCases:
			with (
				self.subTest(
					uiaDescription=uiaDescription,
					legacyDescription=legacyDescription,
				),
				patch.object(UIA, "_get_description", return_value=uiaDescription),
				patch.object(
					MenuItem,
					"_getUIACacheablePropertyValue_handlesCOMErrors",
					return_value=legacyDescription,
				) as getLegacyDescription,
			):
				self.assertEqual(expectedDescription, menuItem._get_description())
				if shouldReadLegacyDescription:
					getLegacyDescription.assert_called_once()
				else:
					getLegacyDescription.assert_not_called()

	def test_legacyDescriptionFallbackIsLimitedToNetFrameworkWinFormsToolStripMenuItems(self) -> None:
		menuItem = object.__new__(MenuItem)
		menuItem.name = "Name"
		for frameworkID, providerDescription in (
			(
				"WPF",
				"managed:System.Windows.Forms.ToolStripMenuItem+ToolStripMenuItemAccessibleObject, "
				"System.Windows.Forms, Version=4.0.0.0",
			),
			(
				"WinForm",
				"managed:System.Windows.Forms.ToolStripMenuItem+ToolStripMenuItemAccessibleObject, "
				"System.Windows.Forms, Version=8.0.0.0",
			),
			("WinForm", "System.Windows.Forms.Button, System.Windows.Forms, Version=4.0.0.0"),
		):
			with (
				self.subTest(frameworkID=frameworkID, providerDescription=providerDescription),
				patch.object(UIA, "_get_description", return_value=""),
				patch.object(
					MenuItem,
					"_getUIACacheablePropertyValue_handlesCOMErrors",
					return_value="Legacy description",
				) as getLegacyDescription,
			):
				menuItem.UIAElement = Mock(
					cachedFrameworkID=frameworkID,
					cachedProviderDescription=providerDescription,
				)
				self.assertEqual("", menuItem._get_description())
				getLegacyDescription.assert_not_called()


class TestMenuItemStates(unittest.TestCase):
	def test_legacyCheckedStateFallback(self) -> None:
		menuItem = object.__new__(MenuItem)
		testCases = (
			(
				set(),
				oleacc.STATE_SYSTEM_CHECKED,
				{controlTypes.State.CHECKABLE, controlTypes.State.CHECKED},
				True,
			),
			(set(), 0, set(), True),
			(
				{controlTypes.State.CHECKABLE},
				oleacc.STATE_SYSTEM_CHECKED,
				{controlTypes.State.CHECKABLE},
				False,
			),
		)
		for uiaStates, legacyState, expectedStates, shouldReadLegacyState in testCases:
			with (
				self.subTest(
					uiaStates=uiaStates,
					legacyState=legacyState,
				),
				patch.object(UIA, "_get_states", return_value=uiaStates.copy()),
				patch.object(
					MenuItem,
					"_getUIACacheablePropertyValue_handlesCOMErrors",
					return_value=legacyState,
				) as getLegacyState,
			):
				self.assertEqual(expectedStates, menuItem._get_states())
				if shouldReadLegacyState:
					getLegacyState.assert_called_once_with(
						UIAHandler.UIA_LegacyIAccessibleStatePropertyId,
						True,
					)
				else:
					getLegacyState.assert_not_called()


class _TestNetFrameworkWinFormsComboBox(_NetFrameworkWinFormsComboBox):
	processID: int = 1
	windowHandle: int = 100


class _ComboLBoxListItem(ListItem):
	processID: int = 1
	windowClassName: str = "ComboLBox"
	windowHandle: int = 200


class TestNetFrameworkWinFormsComboBox(unittest.TestCase):
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
			patch.object(UIA, "event_UIA_elementSelected", autospec=True),
		):
			listItem.event_UIA_elementSelected()
		self.comboBox.event_valueChange.assert_not_called()

	def test_elementSelectedWithUnrelatedFocusDoesNotForwardValueChange(self) -> None:
		listItem = object.__new__(_ComboLBoxListItem)
		focus = Mock(processID=1)
		with (
			patch.object(api, "getFocusObject", return_value=focus),
			patch.object(UIA, "event_UIA_elementSelected", autospec=True),
		):
			listItem.event_UIA_elementSelected()
		focus.event_valueChange.assert_not_called()
