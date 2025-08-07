# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited

"""Unit tests for the message dialog API."""

from copy import deepcopy
import unittest
from unittest.mock import ANY, MagicMock, Mock, PropertyMock, patch, sentinel

import wx
from gui.message import _Command, DefaultButtonSet, DialogType, EscapeCode, ReturnCode
from gui.message import (
	_messageBoxButtonStylesToMessageDialogButtons,
)
from parameterized import parameterized
from typing import Any, Iterable, NamedTuple
from concurrent.futures import ThreadPoolExecutor

from gui.message import Button
from gui.message import MessageDialog


NO_CALLBACK = (EscapeCode.NO_FALLBACK, None)


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


def mockDialogFactory(isBlocking: bool = False) -> MagicMock:
	"""Mock a dialog with certain properties set.

	:param isBlocking: Whether the mocked dialog is blocking.
	:return: A mock with the same API as :class:`MessageDialog`.
	"""
	mock = MagicMock(spec_set=MessageDialog)
	type(mock).isBlocking = PropertyMock(return_value=isBlocking)
	return mock


class AddDefaultButtonHelpersArgList(NamedTuple):
	func: str
	expectedButtons: Iterable[int]
	expectedHasFallback: bool = False
	expectedFallbackId: int = wx.ID_NONE


class MethodCall(NamedTuple):
	name: str
	args: tuple[Any, ...] = tuple()
	kwargs: dict[str, Any] = dict()


class FocusBlockingInstancesDialogs(NamedTuple):
	dialog: MagicMock
	expectedRaise: bool
	expectedSetFocus: bool


class SubsequentCallArgList(NamedTuple):
	label: str
	meth1: MethodCall
	meth2: MethodCall


class ExecuteCommandArgList(NamedTuple):
	label: str
	closesDialog: bool
	canCallClose: bool
	expectedCloseCalled: bool


class BlockingInstancesExistArgList(NamedTuple):
	label: str
	instances: tuple[MagicMock, ...]
	expectedBlockingInstancesExist: bool


class IsBlockingArgList(NamedTuple):
	label: str
	isModal: bool
	hasFallback: bool
	expectedIsBlocking: bool


class WxTestBase(unittest.TestCase):
	"""Base class for test cases which need wx to be initialised."""

	def setUp(self) -> None:
		self.app = wx.App()


class MDTestBase(WxTestBase):
	"""Base class for test cases needing a MessageDialog instance to work on."""

	def setUp(self) -> None:
		super().setUp()
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
		(
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
		),
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
			self.assertEqual(self.dialog.hasFallback, expectedHasFallback)
		with self.subTest(
			"Test whether getting the fallback action returns the expected action type and return code",
		):
			actualFallbackAction = self.dialog._getFallbackAction()
			if expectedHasFallback:
				self.assertIsNotNone(actualFallbackAction)
				self.assertEqual(actualFallbackAction.returnCode, expectedFallbackId)
			else:
				self.assertIsNone(actualFallbackAction)

	def test_addButtonWithDefaultFocus(self):
		"""Test adding a button with default focus."""
		self.dialog.addButton(
			Button(label="Custom", id=ReturnCode.CUSTOM_1, defaultFocus=True),
		)
		self.assertEqual(self.dialog.GetDefaultItem().GetId(), ReturnCode.CUSTOM_1)

	def test_addButtonWithFallbackAction(self):
		"""Test adding a button with fallback action."""
		self.dialog.addButton(
			Button(
				label="Custom",
				id=ReturnCode.CUSTOM_1,
				fallbackAction=True,
				closesDialog=True,
			),
		)
		command = self.dialog._getFallbackAction()
		self.assertEqual(command.returnCode, ReturnCode.CUSTOM_1)
		self.assertTrue(command.closesDialog)

	def test_addButtonWithNonClosingFallbackAction(self):
		"""Test adding a button with fallback action that does not close the dialog."""
		self.dialog.addButton(
			Button(
				label="Custom",
				id=ReturnCode.CUSTOM_1,
				fallbackAction=True,
				closesDialog=False,
			),
		)
		command = self.dialog._getFallbackAction()
		self.assertEqual(command.returnCode, ReturnCode.CUSTOM_1)
		self.assertTrue(command.closesDialog)

	@parameterized.expand(
		(
			SubsequentCallArgList(
				"buttons_same_id",
				meth1=MethodCall("addOkButton", kwargs={"callback": dummyCallback1}),
				meth2=MethodCall("addOkButton", kwargs={"callback": dummyCallback2}),
			),
			SubsequentCallArgList(
				"Button_then_ButtonSet_containing_same_id",
				meth1=MethodCall("addOkButton"),
				meth2=MethodCall("addOkCancelButtons"),
			),
			SubsequentCallArgList(
				"ButtonSet_then_Button_with_id_from_set",
				meth1=MethodCall("addOkCancelButtons"),
				meth2=MethodCall("addOkButton"),
			),
			SubsequentCallArgList(
				"ButtonSets_containing_same_id",
				meth1=MethodCall("addOkCancelButtons"),
				meth2=MethodCall("addYesNoCancelButtons"),
			),
		),
	)
	def test_subsequentAdd(self, _, func1: MethodCall, func2: MethodCall):
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

	def test_setButtonLabelNotAButton(self):
		"""Test that calling setButtonLabel with an id that does not refer to a wx.Button fails as expected."""
		messageControlId = self.dialog._messageControl.GetId()
		# This is not a case that should be encountered unless users tamper with internal state.
		self.dialog._commands[messageControlId] = _Command(
			closesDialog=True,
			callback=None,
			returnCode=ReturnCode.APPLY,
		)
		with self.assertRaises(TypeError):
			self.dialog.setButtonLabel(messageControlId, "test")

	def test_setButtonLabelsCountMismatch(self):
		with self.assertRaises(ValueError):
			"""Test that calling _setButtonLabels with a mismatched collection of IDs and labels fails as expected."""
			self.dialog._setButtonLabels((ReturnCode.APPLY, ReturnCode.CANCEL), ("Apply", "Cancel", "Ok"))

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
			SubsequentCallArgList(
				"noExistantIds",
				meth1=MethodCall("addYesNoButtons"),
				meth2=MethodCall("setOkCancelLabels", ("Test 1", "Test 2")),
			),
			SubsequentCallArgList(
				"ExistantAndNonexistantIds",
				meth1=MethodCall("addYesNoCancelButtons"),
				meth2=MethodCall("setOkCancelLabels", ("Test 1", "Test 2")),
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
		self.assertEqual(self.dialog._commands[ReturnCode.APPLY].returnCode, RETURN_CODE)
		self.assertEqual(self.dialog.GetEscapeId(), ReturnCode.APPLY)

	def test_addButtonsNonuniqueIds(self):
		"""Test that adding a set of buttons with non-unique IDs fails."""
		with self.assertRaises(KeyError):
			self.dialog.addButtons((*DefaultButtonSet.OK_CANCEL, *DefaultButtonSet.YES_NO_CANCEL))

	def test_setDefaultFocusGoodId(self):
		"""Test that setting the default focus works as expected."""
		self.dialog.addOkCancelButtons()
		self.dialog.setDefaultFocus(ReturnCode.CANCEL)
		self.assertEqual(self.dialog.GetDefaultItem().GetId(), ReturnCode.CANCEL)

	def test_setDefaultFocusBadId(self):
		"""Test that setting the default focus to an ID that doesn't exist in the dialog fails as expected."""
		self.dialog.addOkCancelButtons()
		with self.assertRaises(KeyError):
			self.dialog.setDefaultFocus(ReturnCode.APPLY)


class Test_MessageDialog_DefaultAction(MDTestBase):
	def test_defaultActionDefaultEscape_OkCancel(self):
		"""Test that when adding OK and Cancel buttons with default escape code, that the fallback action is cancel."""
		self.dialog.addOkButton(callback=dummyCallback1).addCancelButton(callback=dummyCallback2)
		command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(command.returnCode, ReturnCode.CANCEL)
			self.assertEqual(command.callback, dummyCallback2)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual(command, self.dialog._getFallbackActionOrFallback())

	def test_defaultActionDefaultEscape_CancelOk(self):
		"""Test that when adding cancel and ok buttons with default escape code, that the fallback action is cancel."""
		self.dialog.addCancelButton(callback=dummyCallback2).addOkButton(callback=dummyCallback1)
		command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(command.returnCode, ReturnCode.CANCEL)
			self.assertEqual(command.callback, dummyCallback2)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual(command, self.dialog._getFallbackActionOrFallback())

	def test_defaultActionDefaultEscape_OkClose(self):
		"""Test that when adding OK and Close buttons with default escape code, that the fallback action is OK."""
		self.dialog.addOkButton(callback=dummyCallback1).addCloseButton(callback=dummyCallback2)
		command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(command.returnCode, ReturnCode.OK)
			self.assertEqual(command.callback, dummyCallback1)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual(command, self.dialog._getFallbackActionOrFallback())

	def test_defaultActionDefaultEscape_CloseOk(self):
		"""Test that when adding Close and OK buttons with default escape code, that the fallback action is OK."""
		self.dialog.addCloseButton(callback=dummyCallback2).addOkButton(callback=dummyCallback1)
		command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(command.returnCode, ReturnCode.OK)
			self.assertEqual(command.callback, dummyCallback1)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual(command, self.dialog._getFallbackActionOrFallback())

	def test_setFallbackActionExistantAction(self):
		"""Test that setting the fallback action results in the correct action being returned from both getFallbackAction and getFallbackActionOrFallback."""
		self.dialog.addYesNoButtons()
		self.dialog.setFallbackAction(ReturnCode.YES)
		command = self.dialog._getFallbackAction()
		with self.subTest("Test getting the fallback action."):
			self.assertEqual(command.returnCode, ReturnCode.YES)
			self.assertIsNone(command.callback)
			self.assertTrue(command.closesDialog)
		with self.subTest(
			"Test getting the fallback action or fallback returns the same as getting the fallback action.",
		):
			self.assertEqual(command, self.dialog._getFallbackActionOrFallback())

	def test_setFallbackActionNonexistantAction(self):
		"""Test that setting the fallback action to an action that has not been set up results in KeyError, and that a fallback action is returned from getFallbackActionOrFallback."""
		self.dialog.addYesNoButtons()
		with self.subTest("Test getting the fallback action."):
			with self.assertRaises(KeyError):
				self.dialog.setFallbackAction(ReturnCode.APPLY)
		with self.subTest("Test getting the fallback fallback action."):
			self.assertIsNone(self.dialog._getFallbackAction())

	def test_setFallbackActionNonclosingAction(self):
		"""Check that setting the fallback action to an action that does not close the dialog fails with a ValueError."""
		self.dialog.addOkButton().addApplyButton(closesDialog=False)
		with self.subTest("Test setting the fallback action."):
			with self.assertRaises(ValueError):
				self.dialog.setFallbackAction(ReturnCode.APPLY)

	def test_getFallbackActionOrFallbackNoControls(self):
		"""Test that getFallbackActionOrFallback returns wx.ID_NONE and a close command with no callback when the dialog has no buttons."""
		command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(command.returnCode, EscapeCode.NO_FALLBACK)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionOrFallbackNoDefaultFocusClosingButton(self):
		"""Test that getFallbackActionOrFallback returns the first button when no fallback action or default focus is specified."""
		self.dialog.addApplyButton(closesDialog=False).addCloseButton()
		self.assertIsNone(self.dialog.GetDefaultItem())
		command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(command.returnCode, ReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionOrFallbackNoDefaultFocusNoClosingButton(self):
		"""Test that getFallbackActionOrFallback returns the first button when no fallback action or default focus is specified."""
		self.dialog.addApplyButton(closesDialog=False).addCloseButton(closesDialog=False)
		self.assertIsNone(self.dialog.GetDefaultItem())
		command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(command.returnCode, ReturnCode.APPLY)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionOrFallbackNoDefaultAction(self):
		"""Test that getFallbackActionOrFallback returns the default focus if one is specified but there is no fallback action."""
		self.dialog.addApplyButton().addCloseButton()
		self.dialog.setDefaultFocus(ReturnCode.CLOSE)
		self.assertEqual(self.dialog.GetDefaultItem().GetId(), ReturnCode.CLOSE)
		command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(command.returnCode, ReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionOrFallbackCustomDefaultAction(self):
		"""Test that getFallbackActionOrFallback returns the custom defaultAction if set."""
		self.dialog.addApplyButton().addCloseButton()
		self.dialog.setFallbackAction(ReturnCode.CLOSE)
		command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(command.returnCode, ReturnCode.CLOSE)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionOrFallbackEscapeIdNotACommand(self):
		"""Test that calling _getFallbackActionOrFallback on a dialog whose EscapeId is not a command falls back to returning the default focus."""
		self.dialog.addOkCancelButtons()
		super(MessageDialog, self.dialog).SetEscapeId(ReturnCode.CLOSE)
		command = self.dialog._getFallbackActionOrFallback()
		self.assertEqual(command.returnCode, ReturnCode.OK)
		self.assertIsNotNone(command)
		self.assertTrue(command.closesDialog)

	def test_getFallbackActionEscapeCode_None(self):
		"""Test that setting EscapeCode to None causes _getFallbackAction to return None."""
		self.dialog.addOkCancelButtons()
		self.dialog.SetEscapeId(EscapeCode.NO_FALLBACK)
		self.assertIsNone(self.dialog._getFallbackAction())


class Test_MessageDialog_Threading(WxTestBase):
	def test_newOnNonmain(self):
		"""Test that creating a MessageDialog on a non GUI thread fails."""
		with ThreadPoolExecutor(max_workers=1) as tpe:
			with self.assertRaises(RuntimeError):
				tpe.submit(MessageDialog.__new__, MessageDialog).result()

	def test_initOnNonMain(self):
		"""Test that initializing a MessageDialog on a non-GUI thread fails."""
		dlg = MessageDialog.__new__(MessageDialog)
		with ThreadPoolExecutor(max_workers=1) as tpe:
			with self.assertRaises(RuntimeError):
				tpe.submit(dlg.__init__, None, "Test").result()

	def test_showOnNonMain(self):
		"""Test that showing a MessageDialog on a non-GUI thread fails."""
		dlg = MessageDialog(None, "Test")
		with ThreadPoolExecutor(max_workers=1) as tpe:
			with self.assertRaises(RuntimeError):
				tpe.submit(dlg.Show).result()

	def test_showModalOnNonMain(self):
		"""Test that showing a MessageDialog modally on a non-GUI thread fails."""
		dlg = MessageDialog(None, "Test")
		with ThreadPoolExecutor(max_workers=1) as tpe:
			with self.assertRaises(RuntimeError):
				tpe.submit(dlg.ShowModal).result()


@patch.object(wx.Dialog, "Show")
class Test_MessageDialog_Show(MDTestBase):
	def test_showNoButtons(self, mocked_show: MagicMock):
		"""Test that showing a MessageDialog with no buttons fails."""
		with self.assertRaises(RuntimeError):
			self.dialog.Show()
		mocked_show.assert_not_called()

	def test_show(self, mocked_show: MagicMock):
		"""Test that showing a MessageDialog works as expected."""
		self.dialog.addOkButton()
		self.dialog.Show()
		mocked_show.assert_called_once()


@patch("gui.mainFrame")
@patch.object(wx.Dialog, "ShowModal")
class Test_MessageDialog_ShowModal(MDTestBase):
	def test_showModalNoButtons(self, mocked_showModal: MagicMock, _):
		"""Test that showing a MessageDialog modally with no buttons fails."""
		with self.assertRaises(RuntimeError):
			self.dialog.ShowModal()
		mocked_showModal.assert_not_called()

	def test_showModal(self, mocked_showModal: MagicMock, _):
		"""Test that showing a MessageDialog works as expected."""
		self.dialog.addOkButton()
		with patch("gui.message._messageBoxCounter") as mocked_messageBoxCounter:
			mocked_messageBoxCounter.__iadd__.return_value = (
				mocked_messageBoxCounter.__isub__.return_value
			) = mocked_messageBoxCounter
			self.dialog.ShowModal()
			mocked_showModal.assert_called_once()
			mocked_messageBoxCounter.__iadd__.assert_called_once()
			mocked_messageBoxCounter.__isub__.assert_called_once()


class Test_MessageDialog_EventHandlers(MDTestBase):
	def test_onShowEventDefaultFocus(self):
		"""Test that _onShowEvent correctly focuses the default focus."""
		self.dialog.addOkButton().addCancelButton(defaultFocus=True)
		evt = wx.ShowEvent(self.dialog.GetId(), True)
		with patch.object(wx.Window, "SetFocus") as mocked_setFocus:
			self.dialog._onShowEvent(evt)
			mocked_setFocus.assert_called_once()

	def test_onCloseEventNonVetoable(self):
		evt = wx.CloseEvent(wx.wxEVT_CLOSE_WINDOW, self.dialog.GetId())
		"""Test that a non-vetoable close event is executed."""
		evt.SetCanVeto(False)
		self.dialog._instances.append(self.dialog)
		with (
			patch.object(wx.Dialog, "Destroy") as mocked_destroy,
			patch.object(
				self.dialog,
				"_executeCommand",
				wraps=self.dialog._executeCommand,
			) as mocked_executeCommand,
		):
			self.dialog._onCloseEvent(evt)
			mocked_destroy.assert_called_once()
			mocked_executeCommand.assert_called_once_with(ANY, _canCallClose=False)
			self.assertNotIn(self.dialog, MessageDialog._instances)

	def test_onCloseEventNoFallbackAction(self):
		"""Test that a vetoable call to close is vetoed if there is no fallback action."""
		self.dialog.addYesNoButtons()
		self.dialog.SetEscapeId(EscapeCode.NO_FALLBACK)
		evt = wx.CloseEvent(wx.wxEVT_CLOSE_WINDOW, self.dialog.GetId())
		MessageDialog._instances.append(self.dialog)
		with (
			patch.object(wx.Dialog, "DestroyLater") as mocked_destroyLater,
			patch.object(
				self.dialog,
				"_executeCommand",
			) as mocked_executeCommand,
		):
			self.dialog._onCloseEvent(evt)
			mocked_destroyLater.assert_not_called()
			mocked_executeCommand.assert_not_called()
			self.assertTrue(evt.GetVeto())
			self.assertIn(self.dialog, MessageDialog._instances)

	def test_onCloseEventFallbackAction(self):
		"""Test that _onCloseEvent works properly when there is an there is a fallback action."""
		self.dialog.addOkCancelButtons()
		evt = wx.CloseEvent(wx.wxEVT_CLOSE_WINDOW, self.dialog.GetId())
		MessageDialog._instances.append(self.dialog)
		with (
			patch.object(wx.Dialog, "DestroyLater") as mocked_destroyLater,
			patch.object(
				self.dialog,
				"_executeCommand",
				wraps=self.dialog._executeCommand,
			) as mocked_executeCommand,
		):
			self.dialog._onCloseEvent(evt)
			mocked_destroyLater.assert_called_once()
			mocked_executeCommand.assert_called_once_with(ANY, _canCallClose=False)
			self.assertNotIn(self.dialog, MessageDialog._instances)

	@parameterized.expand(
		(
			ExecuteCommandArgList(
				label="closableCanCallClose",
				closesDialog=True,
				canCallClose=True,
				expectedCloseCalled=True,
			),
			ExecuteCommandArgList(
				label="ClosableCannotCallClose",
				closesDialog=True,
				canCallClose=False,
				expectedCloseCalled=False,
			),
			ExecuteCommandArgList(
				label="UnclosableCanCallClose",
				closesDialog=False,
				canCallClose=True,
				expectedCloseCalled=False,
			),
			ExecuteCommandArgList(
				label="UnclosableCannotCallClose",
				closesDialog=False,
				canCallClose=False,
				expectedCloseCalled=False,
			),
		),
	)
	def test_executeCommand(self, _, closesDialog: bool, canCallClose: bool, expectedCloseCalled: bool):
		"""Test that _executeCommand performs as expected in a number of situations."""
		returnCode = sentinel.return_code
		callback = Mock()
		command = _Command(callback=callback, closesDialog=closesDialog, returnCode=returnCode)
		with (
			patch.object(self.dialog, "Close") as mocked_close,
			patch.object(
				self.dialog,
				"SetReturnCode",
			) as mocked_setReturnCode,
		):
			self.dialog._executeCommand(command, _canCallClose=canCallClose)
			callback.assert_called_once()
			if expectedCloseCalled:
				mocked_setReturnCode.assert_called_with(returnCode)
				mocked_close.assert_called_once()
			else:
				mocked_setReturnCode.assert_not_called()
				mocked_close.assert_not_called()


class Test_MessageDialog_Blocking(MDTestBase):
	def tearDown(self) -> None:
		MessageDialog._instances.clear()
		super().tearDown()

	@parameterized.expand(
		(
			BlockingInstancesExistArgList(
				label="noInstances",
				instances=tuple(),
				expectedBlockingInstancesExist=False,
			),
			BlockingInstancesExistArgList(
				label="nonBlockingInstance",
				instances=(mockDialogFactory(isBlocking=False),),
				expectedBlockingInstancesExist=False,
			),
			BlockingInstancesExistArgList(
				label="blockingInstance",
				instances=(mockDialogFactory(isBlocking=True),),
				expectedBlockingInstancesExist=True,
			),
			BlockingInstancesExistArgList(
				label="onlyBlockingInstances",
				instances=(mockDialogFactory(isBlocking=True), mockDialogFactory(isBlocking=True)),
				expectedBlockingInstancesExist=True,
			),
			BlockingInstancesExistArgList(
				label="onlyNonblockingInstances",
				instances=(mockDialogFactory(isBlocking=False), mockDialogFactory(isBlocking=False)),
				expectedBlockingInstancesExist=False,
			),
			BlockingInstancesExistArgList(
				label="blockingFirstNonBlockingSecond",
				instances=(mockDialogFactory(isBlocking=True), mockDialogFactory(isBlocking=False)),
				expectedBlockingInstancesExist=True,
			),
			BlockingInstancesExistArgList(
				label="nonblockingFirstblockingSecond",
				instances=(mockDialogFactory(isBlocking=False), mockDialogFactory(isBlocking=True)),
				expectedBlockingInstancesExist=True,
			),
		),
	)
	def test_blockingInstancesExist(
		self,
		_,
		instances: tuple[MagicMock, ...],
		expectedBlockingInstancesExist: bool,
	):
		"""Test that blockingInstancesExist is correct in a number of situations."""
		MessageDialog._instances.extend(instances)
		self.assertEqual(MessageDialog.blockingInstancesExist(), expectedBlockingInstancesExist)

	@parameterized.expand(
		(
			IsBlockingArgList(
				label="modalWithFallback",
				isModal=True,
				hasFallback=True,
				expectedIsBlocking=True,
			),
			IsBlockingArgList(
				label="ModalWithoutFallback",
				isModal=True,
				hasFallback=False,
				expectedIsBlocking=True,
			),
			IsBlockingArgList(
				label="ModelessWithFallback",
				isModal=False,
				hasFallback=True,
				expectedIsBlocking=False,
			),
			IsBlockingArgList(
				label="ModelessWithoutFallback",
				isModal=False,
				hasFallback=False,
				expectedIsBlocking=True,
			),
		),
	)
	def test_isBlocking(self, _, isModal: bool, hasFallback: bool, expectedIsBlocking: bool):
		"""Test that isBlocking works correctly in a number of situations."""
		with (
			patch.object(self.dialog, "IsModal", return_value=isModal),
			patch.object(
				type(self.dialog),
				"hasFallback",
				new_callable=PropertyMock,
				return_value=hasFallback,
			),
		):
			self.assertEqual(self.dialog.isBlocking, expectedIsBlocking)

	@parameterized.expand(
		(
			(
				"oneNonblockingDialog",
				(
					FocusBlockingInstancesDialogs(
						mockDialogFactory(False),
						expectedRaise=False,
						expectedSetFocus=False,
					),
				),
			),
			(
				"oneBlockingDialog",
				(
					FocusBlockingInstancesDialogs(
						mockDialogFactory(True),
						expectedRaise=True,
						expectedSetFocus=True,
					),
				),
			),
			(
				"blockingThenNonblocking",
				(
					FocusBlockingInstancesDialogs(
						mockDialogFactory(True),
						expectedRaise=True,
						expectedSetFocus=True,
					),
					FocusBlockingInstancesDialogs(
						mockDialogFactory(False),
						expectedRaise=False,
						expectedSetFocus=False,
					),
				),
			),
			(
				"nonblockingThenBlocking",
				(
					FocusBlockingInstancesDialogs(
						mockDialogFactory(False),
						expectedRaise=False,
						expectedSetFocus=False,
					),
					FocusBlockingInstancesDialogs(
						mockDialogFactory(True),
						expectedRaise=True,
						expectedSetFocus=True,
					),
				),
			),
			(
				"blockingThenBlocking",
				(
					FocusBlockingInstancesDialogs(
						mockDialogFactory(True),
						expectedRaise=True,
						expectedSetFocus=False,
					),
					FocusBlockingInstancesDialogs(
						mockDialogFactory(True),
						expectedRaise=True,
						expectedSetFocus=True,
					),
				),
			),
		),
	)
	def test_focusBlockingInstances(self, _, dialogs: tuple[FocusBlockingInstancesDialogs, ...]):
		"""Test that focusBlockingInstances works as expected in a number of situations."""
		MessageDialog._instances.extend(dialog.dialog for dialog in dialogs)
		MessageDialog.focusBlockingInstances()
		for dialog, expectedRaise, expectedSetFocus in dialogs:
			if expectedRaise:
				dialog.Raise.assert_called_once()
			else:
				dialog.Raise.assert_not_called()
			if expectedSetFocus:
				dialog.SetFocus.assert_called_once()
			else:
				dialog.SetFocus.assert_not_called()

	def test_closeNonblockingInstances(self):
		"""Test that closing non-blocking instances works in a number of situations."""
		bd1, bd2 = mockDialogFactory(True), mockDialogFactory(True)
		nd1, nd2, nd3 = mockDialogFactory(False), mockDialogFactory(False), mockDialogFactory(False)
		MessageDialog._instances.extend((nd1, bd1, nd2, bd2, nd3))
		MessageDialog.closeInstances()
		bd1.Close.assert_not_called()
		bd2.Close.assert_not_called()
		nd1.Close.assert_called()
		nd2.Close.assert_called()
		nd3.Close.assert_called()


class Test_MessageBoxShim(unittest.TestCase):
	def test_messageBoxButtonStylesToMessageDialogButtons(self):
		"""Test that mapping from style flags to Buttons works as expected."""
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
						(button.id for button in _messageBoxButtonStylesToMessageDialogButtons(input)),
					)
