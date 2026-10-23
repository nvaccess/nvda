# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Recipient popup event ordering and lifecycle regression tests."""

import unittest
from unittest.mock import Mock, call, patch

import controlTypes
from appModules import outlook
from comtypes import COMError
from NVDAObjects import NVDAObject
from NVDAObjects.UIA import UIA


class _RecipientUIA:
	"""Replace native UIA object construction while retaining cached element data."""

	def __init__(
		self,
		windowHandle: int,
		UIAElement: outlook.UIAHandler.IUIAutomationElement,
		initialUIACachedPropertyIDs: set[int],
	) -> None:
		self.windowHandle: int = windowHandle
		self.UIAElement: outlook.UIAHandler.IUIAutomationElement = UIAElement
		self.initialUIACachedPropertyIDs: set[int] = initialUIACachedPropertyIDs


class TestAutoComplete(unittest.TestCase):
	"""Exercise the actual layout, UIA selection and state-change entry points."""

	def setUp(self) -> None:
		self.app: outlook.AppModule = object.__new__(outlook.AppModule)
		self.app._lastAutoCompleteAnnouncement = None
		self.focus: Mock = Mock(spec=outlook.ContactEditField, appModule=self.app, windowHandle=20, value="c")
		self.popup: Mock = Mock(cachedIsOffscreen=False, cachedIsEnabled=True)
		self.selected: Mock = Mock(cachedName="Recipient A", cachedIsOffscreen=False, cachedIsEnabled=True)
		self.selected.getCachedPropertyValue.return_value = True
		self.popup.findFirstBuildCache.return_value = self.selected
		self.handler: Mock = Mock()
		self.handler.clientObject.createTreeWalker.return_value.normalizeElementBuildCache.return_value = (
			self.popup
		)
		self.list: Mock = Mock(
			spec=outlook.AutoCompleteList, appModule=self.app, windowHandle=10, UIAElement=Mock()
		)
		self.list.role = controlTypes.Role.LIST
		self.item: Mock = Mock(spec=_RecipientUIA, appModule=self.app, windowHandle=10)
		self.item.role = controlTypes.Role.LISTITEM
		self.item.UIAElement = Mock()
		self.item.UIAElement.buildUpdatedCache.return_value = self.selected
		self.item.event_selection = Mock(
			side_effect=lambda: outlook.AutoCompleteListItem.event_selection(self.item)
		)
		self.message: Mock = self.enterContext(patch.object(outlook.ui, "message"))
		self.navigator: Mock = self.enterContext(patch.object(outlook.api, "setNavigatorObject"))
		self.vision: Mock = self.enterContext(patch.object(outlook.vision, "handler", Mock()))
		self.enterContext(patch.object(outlook.speech, "cancelSpeech"))
		self.enterContext(patch.object(outlook.api, "getFocusObject", return_value=self.focus))
		self.enterContext(patch.object(outlook.UIAHandler, "handler", self.handler))
		self.enterContext(patch.object(outlook, "UIA", _RecipientUIA))
		self.enterContext(patch.object(outlook.winUser, "getAncestor", side_effect=self._getRoot))
		self.foreground: Mock = self.enterContext(
			patch.object(outlook.winUser, "getForegroundWindow", return_value=200)
		)
		self.owner: Mock = self.enterContext(patch.object(outlook.winUser, "getWindow", return_value=200))
		self.visible: Mock = self.enterContext(
			patch.object(outlook.winUser, "isWindowVisible", return_value=True)
		)
		self.enabled: Mock = self.enterContext(
			patch.object(outlook.winUser, "isWindowEnabled", return_value=True)
		)

	@staticmethod
	def _getRoot(window: int, relation: int) -> int:
		return {10: 100, 20: 200}.get(window, window)

	def _layout(self) -> None:
		self.list.treeInterceptor = None
		self.list.event_UIA_layoutInvalidated = Mock(
			side_effect=lambda: outlook.AutoCompleteList.event_UIA_layoutInvalidated(self.list)
		)
		with patch.object(outlook.eventHandler.globalPluginHandler, "runningPlugins", []):
			outlook.eventHandler._EventExecuter("UIA_layoutInvalidated", self.list, {})

	def _selection(self) -> None:
		# UIA's normal dispatch must reach the overlay's selection override.
		UIA.event_UIA_elementSelected(self.item)

	def test_firstLayoutWithoutSelectionEvent(self) -> None:
		self._layout()
		self.message.assert_called_once_with("Recipient A")
		self.assertIs(self.navigator.call_args.args[0].UIAElement, self.selected)
		self.vision.handleGainFocus.assert_called_once_with(self.navigator.call_args.args[0])
		self.popup.findFirstBuildCache.assert_called_once()
		self.popup.findAll.assert_not_called()

	def test_layoutAndSelectionOrdering(self) -> None:
		events: tuple[str, ...]
		for events in (("layout", "layout", "selection"), ("selection", "layout")):
			with self.subTest(events=events):
				self.app._resetAutoCompleteAnnouncement()
				self.message.reset_mock()
				event: str
				for event in events:
					self._layout() if event == "layout" else self._selection()
				self.message.assert_called_once_with("Recipient A")

	def test_recreatedObjectAndInputRefinement(self) -> None:
		self._layout()
		self.list = Mock(
			spec=outlook.AutoCompleteList, appModule=self.app, windowHandle=10, UIAElement=Mock()
		)
		self.list.role = controlTypes.Role.LIST
		self.selected = Mock(cachedName="Recipient A", cachedIsOffscreen=False, cachedIsEnabled=True)
		self.selected.getCachedPropertyValue.return_value = True
		self.popup.findFirstBuildCache.return_value = self.selected
		self.focus.value = "ch"
		self._layout()
		self.message.assert_called_once_with("Recipient A")

	def test_changedRecipientAndReturn(self) -> None:
		name: str
		for name in ("Recipient A", "Recipient B", "Recipient A"):
			self.selected.cachedName = name
			self._layout()
		self.assertEqual(
			[call("Recipient A"), call("Recipient B"), call("Recipient A")], self.message.call_args_list
		)

	def test_emptyAndUnusableSelection(self) -> None:
		self.popup.findFirstBuildCache.return_value = None
		self._layout()
		self.popup.findFirstBuildCache.return_value = self.selected
		attribute: str
		value: bool
		for attribute, value in (("cachedIsOffscreen", True), ("cachedIsEnabled", False)):
			with self.subTest(attribute=attribute):
				setattr(self.selected, attribute, value)
				self._layout()
				setattr(self.selected, attribute, not value)
		self.selected.getCachedPropertyValue.return_value = False
		self._layout()
		self.message.assert_not_called()

	def test_parentNameFallbackAndMissingName(self) -> None:
		self.selected.cachedName = ""
		self.handler.baseTreeWalker.getParentElementBuildCache.return_value = Mock(
			cachedName="Parent recipient"
		)
		self._layout()
		self.message.assert_called_once_with("Parent recipient")
		self.message.reset_mock()
		self.handler.baseTreeWalker.getParentElementBuildCache.return_value = None
		self._layout()
		self.message.assert_not_called()

	def test_closedProvider(self) -> None:
		self.popup.findFirstBuildCache.side_effect = COMError(-2147220991, "Popup closed", None)
		self._layout()
		self.message.assert_not_called()

	def test_wrongFocusAndStalePopup(self) -> None:
		self.focus.appModule = Mock()
		self._layout()
		self.focus.appModule = self.app
		self.owner.return_value = 300
		self._layout()
		self.owner.return_value = 200
		self.visible.return_value = False
		self._layout()
		self.visible.return_value = True
		self.enabled.return_value = False
		self._layout()
		self.enabled.return_value = True
		self.foreground.return_value = 300
		self._layout()
		self.message.assert_not_called()

	def test_hiddenAndDisabledList(self) -> None:
		self.popup.cachedIsOffscreen = True
		self._layout()
		self.popup.cachedIsOffscreen = False
		self.popup.cachedIsEnabled = False
		self._layout()
		self.message.assert_not_called()

	def test_deselectionDoesNotReset(self) -> None:
		self._layout()
		self.item.UIAElement.buildUpdatedCache.return_value = Mock()
		self.item.UIAElement.buildUpdatedCache.return_value.getCachedPropertyValue.return_value = False
		outlook.AutoCompleteListItem.event_stateChange(self.item)
		self._layout()
		self.message.assert_called_once_with("Recipient A")

	def test_popupHideAndAcceptanceReset(self) -> None:
		self._layout()
		nextHandler: Mock = Mock()
		outlook.AppModule.event_hide(self.app, Mock(windowHandle=10), nextHandler)
		self._layout()
		self.message.assert_called_once()
		outlook.AppModule.event_hide(
			self.app, Mock(windowHandle=100, windowClassName="Net UI Tool Window"), nextHandler
		)
		self._layout()
		self.assertEqual(2, self.message.call_count)
		self.assertEqual(2, nextHandler.call_count)

	def test_escapeClearingAndFocusReset(self) -> None:
		self._layout()
		outlook.ContactEditField.script_hide(self.focus, Mock())
		self._layout()
		valueChange: Mock
		with patch.object(NVDAObject, "event_valueChange") as valueChange:
			# Typing with the same selection must preserve suppression.
			outlook.ContactEditField.event_valueChange(self.focus)
			self._layout()
			self.assertEqual(2, self.message.call_count)
			self.focus.value = ""
			outlook.ContactEditField.event_valueChange(self.focus)
			self.focus.value = "c"
			self._layout()
			self.assertEqual(3, self.message.call_count)
			self.assertEqual(2, valueChange.call_count)
		loseFocus: Mock
		with patch.object(NVDAObject, "event_loseFocus") as loseFocus:
			outlook.ContactEditField.event_loseFocus(self.focus)
			loseFocus.assert_called_once()
		self._layout()
		self.app.event_appModule_loseFocus()
		self._layout()
		self.assertEqual(5, self.message.call_count)

	def test_msaaAnnouncementIsUnchanged(self) -> None:
		item: Mock = Mock(spec=outlook.AutoCompleteListItem)
		item.states = {controlTypes.State.SELECTED}
		item.name = "MSAA recipient"
		self.focus.role = controlTypes.Role.EDITABLETEXT
		outlook.AutoCompleteListItem.event_stateChange(item)
		self.message.assert_called_once_with("MSAA recipient")
		self.navigator.assert_called_once_with(item)

	def test_hideRegistrationIsProcessAndClassScoped(self) -> None:
		self.app.processID = 42
		requestEvents: Mock
		with (
			patch.object(outlook.appModuleHandler.AppModule, "__init__"),
			patch.object(outlook.eventHandler, "requestEvents") as requestEvents,
		):
			outlook.AppModule.__init__(self.app, 42, "outlook")
			requestEvents.assert_any_call("hide", processId=42, windowClassName="Net UI Tool Window")
			self.assertEqual(2, requestEvents.call_count)

	def test_listOverlayIsRestrictedToRecipientLists(self) -> None:
		obj: Mock = Mock(spec=_RecipientUIA, role=controlTypes.Role.LIST, windowClassName="NetUIHWND")
		obj.UIAElement = Mock(cachedClassName="NetUIListView", cachedAutomationId="idAutoCompleteList")
		classes: list[type[NVDAObject]] = []
		self.app.chooseNVDAObjectOverlayClasses(obj, classes)
		self.assertEqual([outlook.AutoCompleteList], classes)
		classes.clear()
		obj.UIAElement.cachedAutomationId = "OtherList"
		self.app.chooseNVDAObjectOverlayClasses(obj, classes)
		self.assertEqual([], classes)

	def test_selectionAndStateChangeShareSuppression(self) -> None:
		self._selection()
		outlook.AutoCompleteListItem.event_stateChange(self.item)
		self.message.assert_called_once_with("Recipient A")

	def test_anotherFieldCannotResetCurrentPopup(self) -> None:
		self._layout()
		self.app._resetAutoCompleteAnnouncement(30)
		self._layout()
		self.message.assert_called_once()

	def test_msaaSelectionDelegatesToBase(self) -> None:
		# A real overlay instance is required for super() delegation.
		item: outlook.AutoCompleteListItem = object.__new__(outlook.AutoCompleteListItem)
		selection: Mock
		with patch.object(outlook.Window, "event_selection") as selection:
			outlook.AutoCompleteListItem.event_selection(item)
			selection.assert_called_once()

	def test_emptyOrNonRecipientFocus(self) -> None:
		self.focus.value = ""
		self._layout()
		with patch.object(outlook.api, "getFocusObject", return_value=Mock(spec=NVDAObject)):
			self._layout()
		self.message.assert_not_called()

	def test_itemEventIgnoresHiddenOrDisabledSender(self) -> None:
		item: Mock = Mock(cachedIsOffscreen=True, cachedIsEnabled=True)
		item.getCachedPropertyValue.return_value = True
		self.item.UIAElement.buildUpdatedCache.return_value = item
		self._selection()
		item.cachedIsOffscreen = False
		item.cachedIsEnabled = False
		self._selection()
		self.message.assert_not_called()

	def test_popupHostAllowsHideButRecipientChildrenKeepUIA(self) -> None:
		with patch.object(outlook.winUser, "getClassName", return_value="Net UI Tool Window"):
			self.assertTrue(self.app.isBadUIAWindow(100))
		with patch.object(outlook.winUser, "getClassName", side_effect=["NetUIHWND", "Net UI Tool Window"]):
			self.app.productVersion = "16.0"
			self.assertFalse(self.app.isBadUIAWindow(10))

	def test_unavailableRecipientObject(self) -> None:
		with patch.object(_RecipientUIA, "__new__", return_value=None):
			self._layout()
		self.message.assert_not_called()
		self.assertIsNone(self.app._lastAutoCompleteAnnouncement)
