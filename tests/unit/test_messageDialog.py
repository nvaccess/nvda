# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""Unit tests for the message dialog API."""

from copy import deepcopy
import unittest
from unittest.mock import MagicMock, patch

import wx
from gui.messageDialog import (
	DefaultButtonSet,
	MessageDialog,
	Button,
	EscapeCode,
	ReturnCode,
	DialogType,
	_MessageBoxButtonStylesToMessageDialogButtons,
)
from parameterized import parameterized
from typing import Any, Iterable, NamedTuple


NO_CALLBACK = (EscapeCode.NONE, None)


def dummyCallback1(*a):
	pass


def dummyCallback2(*a):
	pass


def getDialogState(dialog: MessageDialog):
	"""Capture internal state of a :class:`gui.messageDialog.MessageDialog` for later analysis.

	Currently this only captures state relevant to adding buttons.
	Further tests wishing to use this dialog should be sure to add any state potentially modified by the functions under test.

	As this is currently only used to ensure internal state does not change between calls, the order of return should be considered arbitrary.
	"""
	return (
		{id: dialog.FindWindow(id).GetLabel() for id in dialog.GetMainButtonIds()},
		deepcopy(dialog._commands),
		item.GetId() if (item := dialog.GetDefaultItem()) is not None else None,
		dialog.GetEscapeId(),
		dialog._isLayoutFullyRealized,
	)


class AddDefaultButtonHelpersArgList(NamedTuple):
	func: str
	expectedButtons: Iterable[int]
	expectedHasFallback: bool = False
	expectedFallbackId: int = wx.ID_NONE


class MethodCall(NamedTuple):
	name: str
	args: tuple[Any, ...] = tuple()
	kwargs: dict[str, Any] = dict()


class MDTestBase(unittest.TestCase):
	"""Base class for test cases testing MessageDialog. Handles wx initialisation."""

	def setUp(self) -> None:
		self.app = wx.App()
		self.dialog = MessageDialog(None, "Test dialog", buttons=None)


@patch.object(wx.ArtProvider, "GetIconBundle")
class Test_MessageDialog_Icons(MDTestBase):
	"""Test that message dialog icons are set correctly."""

	@parameterized.expand(((DialogType.ERROR,), (DialogType.WARNING,)))
	def test_setIconWithTypeWithIcon(self, mocked_GetIconBundle: MagicMock, type: DialogType):
		"""Test that setting the dialog's icons has an effect when the dialog's type has icons."""
		mocked_GetIconBundle.return_value = wx.IconBundle()
		self.dialog._setIcon(type)
		mocked_GetIconBundle.assert_called_once()

	@parameterized.expand(((DialogType.STANDARD,),))
	def test_setIconWithTypeWithoutIcon(self, mocked_GetIconBundle: MagicMock, type: DialogType):
		"""Test that setting the dialog's icons doesn't have an effect when the dialog's type doesn't have icons."""
		type = DialogType.STANDARD
		self.dialog._setIcon(type)
		mocked_GetIconBundle.assert_not_called()


@patch("winsound.MessageBeep")
class Test_MessageDialog_Sounds(MDTestBase):
	"""Test that message dialog sounds are set and played correctly."""

	@parameterized.expand(((DialogType.ERROR,), (DialogType.WARNING,)))
	def test_playSoundWithTypeWithSound(self, mocked_MessageBeep: MagicMock, type: DialogType):
		"""Test that sounds are played for message dialogs whose type has an associated sound."""
		self.dialog._setSound(type)
		self.dialog._playSound()
		mocked_MessageBeep.assert_called_once()

	@parameterized.expand(((DialogType.STANDARD,),))
	def test_playSoundWithTypeWithoutSound(self, mocked_MessageBeep: MagicMock, type: DialogType):
		"""Test that no sounds are played for message dialogs whose type has an associated sound."""
		self.dialog._setSound(type)
		self.dialog._playSound()
		mocked_MessageBeep.assert_not_called()


class Test_MessageDialog_Buttons(MDTestBase):
	@parameterized.expand(
		[
			AddDefaultButtonHelpersArgList(
				func="addOkButton",
				expectedButtons=(wx.ID_OK,),
				expectedHasFallback=True,
				expectedFallbackId=wx.ID_OK,
			),
			AddDefaultButtonHelpersArgList(
				func="addCancelButton",
				expectedButtons=(wx.ID_CANCEL,),
				expectedHasFallback=True,
				expectedFallbackId=wx.ID_CANCEL,
			),
			AddDefaultButtonHelpersArgList(func="addYesButton", expectedButtons=(wx.ID_YES,)),
			AddDefaultButtonHelpersArgList(func="addNoButton", expectedButtons=(wx.ID_NO,)),
			AddDefaultButtonHelpersArgList(func="addSaveButton", expectedButtons=(wx.ID_SAVE,)),
			AddDefaultButtonHelpersArgList(func="addApplyButton", expectedButtons=(wx.ID_APPLY,)),
			AddDefaultButtonHelpersArgList(func="addCloseButton", expectedButtons=(wx.ID_CLOSE,)),
			AddDefaultButtonHelpersArgList(func="addHelpButton", expectedButtons=(wx.ID_HELP,)),
			AddDefaultButtonHelpersArgList(
				func="addOkCancelButtons",
				expectedButtons=(wx.ID_OK, wx.ID_CANCEL),
				expectedHasFallback=True,
				expectedFallbackId=wx.ID_CANCEL,
			),
			AddDefaultButtonHelpersArgList(func="addYesNoButtons", expectedButtons=(wx.ID_YES, wx.ID_NO)),
			AddDefaultButtonHelpersArgList(
				func="addYesNoCancelButtons",
				expectedButtons=(wx.ID_YES, wx.ID_NO, wx.ID_CANCEL),
				expectedHasFallback=True,
				expectedFallbackId=wx.ID_CANCEL,
			),
			AddDefaultButtonHelpersArgList(
				func="addSaveNoCancelButtons",
				expectedButtons=(wx.ID_SAVE, wx.ID_NO, wx.ID_CANCEL),
				expectedHasFallback=True,
				expectedFallbackId=wx.ID_CANCEL,
			),
		],
	)
	def test_addDefaultButtonHelpers(
		self,
		func: str,
		expectedButtons: Iterable[int],
		expectedHasFallback: bool,
		expectedFallbackId: int,
	):
		"""Test the various /add*buttons?/ functions."""
		getattr(self.dialog, func)()
		with self.subTest("Test all expected buttons are in main buttons"):
			self.assertCountEqual(self.dialog.GetMainButtonIds(), expectedButtons)
		for id in expectedButtons:
			with self.subTest("Check that all buttons have the expected type", id=id):
				self.assertIsInstance(self.dialog.FindWindowById(id), wx.Button)
		with self.subTest("Test whether the fallback status is as expected."):
			self.assertEqual(self.dialog.hasDefaultAction, expectedHasFallback)
		with self.subTest("Test whether getting the fallback action returns the expected id and action type"):
			actualFallbackId, actualFallbackAction = self.dialog._getFallbackAction()
			self.assertEqual(actualFallbackId, expectedFallbackId)
			if expectedHasFallback:
				self.assertIsNotNone(actualFallbackAction)
			else:
				self.assertIsNone(actualFallbackAction)

	def test_addButton_with_defaultFocus(self):
		"""Test adding a button with default focus."""
		self.dialog.addButton(
			Button(label="Custom", id=ReturnCode.CUSTOM_1, defaultFocus=True),
		)
		self.assertEqual(self.dialog.GetDefaultItem().GetId(), ReturnCode.CUSTOM_1)

	def test_addButton_with_fallbackAction(self):
		"""Test adding a button with fallback action."""
		self.dialog.addButton(
			Button(
				label="Custom",
				id=ReturnCode.CUSTOM_1,
				fallbackAction=True,
				closesDialog=True,
			),
		)
		id, command = self.dialog._getFallbackAction()
		self.assertEqual(id, ReturnCode.CUSTOM_1)
		self.assertTrue(command.closesDialog)

	def test_addButton_with_non_closing_fallbackAction(self):
		"""Test adding a button with fallback action that does not close the dialog."""
		self.dialog.addButton(
			Button(
				label="Custom",
				id=ReturnCode.CUSTOM_1,
				fallbackAction=True,
				closesDialog=False,
			),
		)
		id, command = self.dialog._getFallbackAction()
		self.assertEqual(id, ReturnCode.CUSTOM_1)
		self.assertTrue(command.closesDialog)

	@parameterized.expand(
		(
			(
				"buttons_same_id",
				MethodCall("addOkButton", kwargs={"callback": dummyCallback1}),
				MethodCall("addOkButton", kwargs={"callback": dummyCallback2}),
			),
			(
				"Button_then_ButtonSet_containing_same_id",
				MethodCall("addOkButton"),
				MethodCall("addOkCancelButtons"),
			),
			(
				"ButtonSet_then_Button_with_id_from_set",
				MethodCall("addOkCancelButtons"),
				MethodCall("addOkButton"),
			),
			(
				"ButtonSets_containing_same_id",
				MethodCall("addOkCancelButtons"),
				MethodCall("addYesNoCancelButtons"),
			),
		),
	)
	def test_subsequent_add(self, _, func1: MethodCall, func2: MethodCall):
		"""Test that adding buttons that already exist in the dialog fails."""
		getattr(self.dialog, func1.name)(*func1.args, **func1.kwargs)
		oldState = getDialogState(self.dialog)
		with self.subTest("Test calling second function raises."):
			self.assertRaises(KeyError, getattr(self.dialog, func2.name), *func2.args, **func2.kwargs)
		with self.subTest("Check state hasn't changed."):
			self.assertEqual(oldState, getDialogState(self.dialog))

	def test_setButtonLabelExistantId(self):
		"""Test that setting the label of a button works."""
		NEW_LABEL = "test"
		self.dialog.addOkButton()
		self.dialog.setButtonLabel(ReturnCode.OK, NEW_LABEL)
		self.assertEqual(self.dialog.FindWindow(ReturnCode.OK).GetLabel(), NEW_LABEL)

	def test_setButtonLabelNonexistantId(self):
		"""Test that setting the label of a button that does not exist in the dialog fails."""
		self.dialog.addOkButton()
		oldState = getDialogState(self.dialog)
		self.assertRaises(KeyError, self.dialog.setButtonLabel, ReturnCode.CANCEL, "test")
		self.assertEqual(oldState, getDialogState(self.dialog))

	def test_setButtonLabelsExistantIds(self):
		"""Test that setting multiple button labels at once works."""
		NEW_YES_LABEL, NEW_NO_LABEL, NEW_CANCEL_LABEL = "test 1", "test 2", "test 3"
		self.dialog.addYesNoCancelButtons()
		self.dialog.setYesNoCancelLabels(NEW_YES_LABEL, NEW_NO_LABEL, NEW_CANCEL_LABEL)
		self.assertEqual(self.dialog.FindWindow(ReturnCode.YES).GetLabel(), NEW_YES_LABEL)
		self.assertEqual(self.dialog.FindWindow(ReturnCode.NO).GetLabel(), NEW_NO_LABEL)
		self.assertEqual(self.dialog.FindWindow(ReturnCode.CANCEL).GetLabel(), NEW_CANCEL_LABEL)

	def test_setSomeButtonLabels(self):
		"""Test that setting the labels of a subset of the existant buttons in the dialog works."""
		NEW_YES_LABEL, NEW_NO_LABEL = "test 1", "test 2"
		self.dialog.addYesNoCancelButtons()
		OLD_CANCEL_LABEL = self.dialog.FindWindow(ReturnCode.CANCEL).GetLabel()
		self.dialog.setYesNoLabels(NEW_YES_LABEL, NEW_NO_LABEL)
		self.assertEqual(self.dialog.FindWindow(ReturnCode.YES).GetLabel(), NEW_YES_LABEL)
		self.assertEqual(self.dialog.FindWindow(ReturnCode.NO).GetLabel(), NEW_NO_LABEL)
		self.assertEqual(self.dialog.FindWindow(ReturnCode.CANCEL).GetLabel(), OLD_CANCEL_LABEL)

	@parameterized.expand(
		(
			(
				"noExistantIds",
				MethodCall("addYesNoButtons"),
				MethodCall("setOkCancelLabels", ("Test 1", "Test 2")),
			),
			(
				"ExistantAndNonexistantIds",
				MethodCall("addYesNoCancelButtons"),
				MethodCall("setOkCancelLabels", ("Test 1", "Test 2")),
			),
		),
	)
	def test_setButtonLabelsBadIds(self, _, setupFunc: MethodCall, setLabelFunc: MethodCall):
		"""Test that attempting to set button labels with IDs that don't appear in the dialog fails and does not alter the dialog."""
		getattr(self.dialog, setupFunc.name)(*setupFunc.args, **setupFunc.kwargs)
		oldState = getDialogState(self.dialog)
		with self.subTest("Test that the operation raises."):
			self.assertRaises(
				KeyError,
				getattr(self.dialog, setLabelFunc.name),
				*setLabelFunc.args,
				**setLabelFunc.kwargs,
			)
		with self.subTest("Check state hasn't changed."):
			self.assertEqual(oldState, getDialogState(self.dialog))

	def test_addButtonFromButtonWithOverrides(self):
		"""Test adding a button from a :class:`Button` with overrides for its properties."""
		LABEL = "test"
		CALLBACK = dummyCallback1
		DEFAULT_FOCUS = FALLBACK_ACTION = CLOSES_DIALOG = True
		RETURN_CODE = 1
		self.dialog.addYesButton().addApplyButton(
			label=LABEL,
			callback=CALLBACK,
			defaultFocus=DEFAULT_FOCUS,
			fallbackAction=FALLBACK_ACTION,
			closesDialog=CLOSES_DIALOG,
			returnCode=RETURN_CODE,
		)
		self.assertEqual(self.dialog.FindWindow(ReturnCode.APPLY).GetLabel(), LABEL)
		self.assertEqual(self.dialog._commands[ReturnCode.APPLY].callback, CALLBACK)
		self.assertEqual(self.dialog._commands[ReturnCode.APPLY].closesDialog, CLOSES_DIALOG)
		self.assertEqual(self.dialog._commands[ReturnCode.APPLY].ReturnCode, RETURN_CODE)
		self.assertEqual(self.dialog.GetEscapeId(), ReturnCode.APPLY)

	def test_addButtonsNonuniqueIds(self):
		"""Test that adding a set of buttons with non-unique IDs fails."""
		with self.assertRaises(KeyError):
			self.dialog.addButtons((*DefaultButtonSet.OK_CANCEL, *DefaultButtonSet.YES_NO_CANCEL))

	def test_setDefaultFocus_goodId(self):
		self.dialog.addOkCancelButtons()
		self.dialog.setDefaultFocus(ReturnCode.CANCEL)
		self.assertEqual(self.dialog.GetDefaultItem().GetId(), ReturnCode.CANCEL)

	def test_setDefaultFocus_badId(self):
		self.dialog.addOkCancelButtons()
		with self.assertRaises(KeyError):
			self.dialog.setDefaultFocus(ReturnCode.APPLY)


class Test_MessageDialog_DefaultAction(MDTestBase):
	def test_defaultAction_defaultEscape_OkCancel(self):
		"""Test that when adding OK and Cancel buttons with default escape code, that the fallback action is cancel."""
		self.dialog.addOkButton(callback=dummyCallback1).addCancelButton(callback=dummyCallback2)
		id, command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(id, ReturnCode.CANCEL)
			self.assertEqual(command.callback, dummyCallback2)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual((id, command), self.dialog._getFallbackActionOrFallback())

	def test_defaultAction_defaultEscape_CancelOk(self):
		"""Test that when adding cancel and ok buttons with default escape code, that the fallback action is cancel."""
		self.dialog.addCancelButton(callback=dummyCallback2).addOkButton(callback=dummyCallback1)
		id, command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(id, ReturnCode.CANCEL)
			self.assertEqual(command.callback, dummyCallback2)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual((id, command), self.dialog._getFallbackActionOrFallback())

	def test_defaultAction_defaultEscape_OkClose(self):
		"""Test that when adding OK and Close buttons with default escape code, that the fallback action is OK."""
		self.dialog.addOkButton(callback=dummyCallback1).addCloseButton(callback=dummyCallback2)
		id, command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(id, ReturnCode.OK)
			self.assertEqual(command.callback, dummyCallback1)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual((id, command), self.dialog._getFallbackActionOrFallback())

	def test_defaultAction_defaultEscape_CloseOk(self):
		"""Test that when adding Close and OK buttons with default escape code, that the fallback action is OK."""
		self.dialog.addCloseButton(callback=dummyCallback2).addOkButton(callback=dummyCallback1)
		id, command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(id, ReturnCode.OK)
			self.assertEqual(command.callback, dummyCallback1)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual((id, command), self.dialog._getFallbackActionOrFallback())

	def test_setDefaultAction_existant_action(self):
		"""Test that setting the fallback action results in the correct action being returned from both getFallbackAction and getFallbackActionOrFallback."""
		self.dialog.addYesNoButtons()
		self.dialog.setDefaultAction(ReturnCode.YES)
		id, command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(id, ReturnCode.YES)
			self.assertIsNone(command.callback)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual((id, command), self.dialog._getFallbackActionOrFallback())

	def test_setDefaultAction_nonexistant_action(self):
		"""Test that setting the fallback action to an action that has not been set up results in KeyError, and that a fallback action is returned from getFallbackActionOrFallback."""
		self.dialog.addYesNoButtons()
		with self.subTest("Test getting the fallback action."):
			with self.assertRaises(KeyError):
				self.dialog.setDefaultAction(ReturnCode.APPLY)
		with self.subTest("Test getting the fallback fallback action."):
			self.assertEqual(self.dialog._getFallbackAction(), NO_CALLBACK)

	def test_setDefaultAction_nonclosing_action(self):
		"""Check that setting the fallback action to an action that does not close the dialog fails with a ValueError."""
		self.dialog.addOkButton().addApplyButton(closesDialog=False)
		with self.subTest("Test getting the fallback action."):
			with self.assertRaises(ValueError):
				self.dialog.setDefaultAction(ReturnCode.APPLY)

	def test_getFallbackActionOrFallback_no_controls(self):
		"""Test that getFallbackActionOrFallback returns wx.ID_NONE and a close command with no callback when the dialog has no buttons."""
		id, command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(id, EscapeCode.NONE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionOrFallback_no_defaultFocus_closing_button(self):
		"""Test that getFallbackActionOrFallback returns the first button when no fallback action or default focus is specified."""
		self.dialog.addApplyButton(closesDialog=False).addCloseButton()
		self.assertIsNone(self.dialog.GetDefaultItem())
		id, command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(id, ReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionOrFallback_no_defaultFocus_no_closing_button(self):
		"""Test that getFallbackActionOrFallback returns the first button when no fallback action or default focus is specified."""
		self.dialog.addApplyButton(closesDialog=False).addCloseButton(closesDialog=False)
		self.assertIsNone(self.dialog.GetDefaultItem())
		id, command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(id, ReturnCode.APPLY)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionOrFallback_no_defaultAction(self):
		"""Test that getFallbackActionOrFallback returns the default focus if one is specified but there is no fallback action."""
		self.dialog.addApplyButton().addCloseButton()
		self.dialog.setDefaultFocus(ReturnCode.CLOSE)
		self.assertEqual(self.dialog.GetDefaultItem().GetId(), ReturnCode.CLOSE)
		id, command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(id, ReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionOrFallback_custom_defaultAction(self):
		"""Test that getFallbackActionOrFallback returns the custom defaultAction if set."""
		self.dialog.addApplyButton().addCloseButton()
		self.dialog.setDefaultAction(ReturnCode.CLOSE)
		id, command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(id, ReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)


class Test_MessageBoxShim(unittest.TestCase):
	def test_messageBoxButtonStylesToMessageDialogButtons(self):
		YES, NO, OK, CANCEL, HELP = wx.YES, wx.NO, wx.OK, wx.CANCEL, wx.HELP
		outputToInputsMap = {
			(ReturnCode.OK,): (OK, 0),
			(ReturnCode.OK, ReturnCode.CANCEL): (OK | CANCEL, CANCEL),
			(ReturnCode.OK, ReturnCode.HELP): (OK | HELP, HELP),
			(ReturnCode.OK, ReturnCode.CANCEL, ReturnCode.HELP): (OK | CANCEL | HELP, CANCEL | HELP),
			(ReturnCode.YES, ReturnCode.NO): (YES | NO, YES, NO, YES | OK, NO | OK, YES | NO | OK),
			(ReturnCode.YES, ReturnCode.NO, ReturnCode.CANCEL): (
				YES | NO | CANCEL,
				YES | CANCEL,
				NO | CANCEL,
				YES | OK | CANCEL,
				NO | OK | CANCEL,
				YES | NO | OK | CANCEL,
			),
			(ReturnCode.YES, ReturnCode.NO, ReturnCode.HELP): (
				YES | NO | HELP,
				YES | HELP,
				NO | HELP,
				YES | OK | HELP,
				NO | OK | HELP,
				YES | NO | OK | HELP,
			),
			(ReturnCode.YES, ReturnCode.NO, ReturnCode.CANCEL, ReturnCode.HELP): (
				YES | NO | CANCEL | HELP,
				YES | CANCEL | HELP,
				NO | CANCEL | HELP,
				YES | OK | CANCEL | HELP,
				NO | OK | CANCEL | HELP,
				YES | NO | OK | CANCEL | HELP,
			),
		}
		for expectedOutput, inputs in outputToInputsMap.items():
			for input in inputs:
				with self.subTest(flags=input):
					self.assertCountEqual(
						expectedOutput,
						(button.id for button in _MessageBoxButtonStylesToMessageDialogButtons(input)),
					)
