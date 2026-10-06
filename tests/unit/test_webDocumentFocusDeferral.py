# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, eilatc
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for deferring focus on a web document after the focused element in it was removed."""

from types import SimpleNamespace  # noqa: I001
from typing import cast
import unittest
from unittest.mock import Mock, PropertyMock, patch

from comtypes import COMError
from comtypes.hresult import E_FAIL

import IAccessibleHandler
import eventHandler
import oleacc
from comInterfaces import IAccessible2Lib as IA2
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.IAccessible import ia2Web

_WINDOW = 1
_OTHER_WINDOW = 2
_DELAY = ia2Web.FOCUS_DELAY_AFTER_FOCUS_REMOVED_MS


def _makeOldFocus(
	*,
	ia2States: int = 0,
	statesError: bool = False,
	windowHandle: int = _WINDOW,
	cls: type = IAccessible,
) -> Mock:
	ia2Obj = Mock(spec=IA2.IAccessible2)
	if statesError:
		type(ia2Obj).states = PropertyMock(side_effect=COMError(E_FAIL, "Object removed", None))
	else:
		type(ia2Obj).states = PropertyMock(return_value=ia2States)
	return Mock(spec=cls, IAccessibleObject=ia2Obj, windowHandle=windowHandle)


def _removedOldFocus(**kwargs) -> Mock:
	return _makeOldFocus(ia2States=IA2.IA2_STATE_DEFUNCT, **kwargs)


class TestWebDocumentFocusEventDelay(unittest.TestCase):
	def _getDelay(
		self,
		oldFocus,
		*,
		role: int = oleacc.ROLE_SYSTEM_DOCUMENT,
		isFocusAncestor: bool = True,
		flagEnabled: bool = True,
	) -> int:
		document = cast(
			ia2Web.Document,
			SimpleNamespace(IAccessibleRole=role, windowHandle=_WINDOW),
		)
		ancestors = [document] if isFocusAncestor else []
		fakeConfig = SimpleNamespace(
			conf={"virtualBuffers": {"delayDocumentFocusAfterFocusRemoved": flagEnabled}},
		)
		with (
			patch.object(eventHandler, "lastQueuedFocusObject", oldFocus),
			patch.object(ia2Web.api, "getFocusAncestors", return_value=ancestors),
			patch.object(ia2Web, "config", fakeConfig),
		):
			return ia2Web.Document._get_focusEventDelay(document)

	def test_removedFocusInThisDocument_defers(self):
		self.assertEqual(_DELAY, self._getDelay(_removedOldFocus()))

	def test_oldFocusRaisingCOMError_defers(self):
		self.assertEqual(_DELAY, self._getDelay(_makeOldFocus(statesError=True)))

	def test_liveOldFocus_doesNotDefer(self):
		self.assertEqual(0, self._getDelay(_makeOldFocus()))

	def test_noOldFocus_doesNotDefer(self):
		self.assertEqual(0, self._getDelay(None))

	def test_oldFocusInOtherWindow_doesNotDefer(self):
		self.assertEqual(0, self._getDelay(_removedOldFocus(windowHandle=_OTHER_WINDOW)))

	def test_oldFocusWasADocument_doesNotDefer(self):
		self.assertEqual(0, self._getDelay(_removedOldFocus(cls=ia2Web.Document)))

	def test_documentNotAnAncestorOfOldFocus_doesNotDefer(self):
		"""For example, a new document gaining focus after a full page load."""
		self.assertEqual(0, self._getDelay(_removedOldFocus(), isFocusAncestor=False))

	def test_applicationRole_doesNotDefer(self):
		self.assertEqual(0, self._getDelay(_removedOldFocus(), role=oleacc.ROLE_SYSTEM_APPLICATION))

	def test_dialogRole_doesNotDefer(self):
		self.assertEqual(0, self._getDelay(_removedOldFocus(), role=oleacc.ROLE_SYSTEM_DIALOG))

	def test_featureFlagDisabled_doesNotDefer(self):
		self.assertEqual(0, self._getDelay(_removedOldFocus(), flagEnabled=False))


def _makeFocusTarget(*, delay: int, allowFocus: bool = True) -> Mock:
	return Mock(spec=IAccessible, focusEventDelay=delay, shouldAllowIAccessibleFocusEvent=allowFocus)


@patch.object(eventHandler, "queueEvent")
@patch.object(IAccessibleHandler.core, "callLater")
class TestProcessFocusNVDAEvent(unittest.TestCase):
	def setUp(self):
		self.oldFocus = Mock(spec=IAccessible)
		self.oldFocus.isDuplicateIAccessibleEvent.return_value = False
		patcher = patch.object(eventHandler, "lastQueuedFocusObject", self.oldFocus)
		patcher.start()
		self.addCleanup(patcher.stop)

	def test_noDelay_queuesImmediately(self, callLater: Mock, queueEvent: Mock):
		obj = _makeFocusTarget(delay=0)
		self.assertTrue(IAccessibleHandler.processFocusNVDAEvent(obj))
		queueEvent.assert_called_once_with("gainFocus", obj)
		callLater.assert_not_called()

	def test_delay_defersInsteadOfQueuing(self, callLater: Mock, queueEvent: Mock):
		obj = _makeFocusTarget(delay=_DELAY)
		self.assertTrue(IAccessibleHandler.processFocusNVDAEvent(obj))
		queueEvent.assert_not_called()
		callLater.assert_called_once_with(
			_DELAY,
			IAccessibleHandler._processDeferredFocusNVDAEvent,
			obj,
			self.oldFocus,
		)

	def test_force_ignoresDelay(self, callLater: Mock, queueEvent: Mock):
		obj = _makeFocusTarget(delay=_DELAY)
		self.assertTrue(IAccessibleHandler.processFocusNVDAEvent(obj, force=True))
		queueEvent.assert_called_once_with("gainFocus", obj)
		callLater.assert_not_called()

	def test_deferred_focusUnchanged_queues(self, callLater: Mock, queueEvent: Mock):
		obj = _makeFocusTarget(delay=_DELAY)
		IAccessibleHandler._processDeferredFocusNVDAEvent(obj, self.oldFocus)
		queueEvent.assert_called_once_with("gainFocus", obj)

	def test_deferred_focusMoved_drops(self, callLater: Mock, queueEvent: Mock):
		obj = _makeFocusTarget(delay=_DELAY)
		eventHandler.lastQueuedFocusObject = Mock(spec=IAccessible)
		IAccessibleHandler._processDeferredFocusNVDAEvent(obj, self.oldFocus)
		queueEvent.assert_not_called()

	def test_deferred_noLongerFocused_drops(self, callLater: Mock, queueEvent: Mock):
		obj = _makeFocusTarget(delay=_DELAY, allowFocus=False)
		IAccessibleHandler._processDeferredFocusNVDAEvent(obj, self.oldFocus)
		queueEvent.assert_not_called()

	def test_secondDocumentFocusDuringDelay_queuesOnlyOnce(self, callLater: Mock, queueEvent: Mock):
		def fakeQueueEvent(eventName, obj):
			eventHandler.lastQueuedFocusObject = obj

		queueEvent.side_effect = fakeQueueEvent
		first = _makeFocusTarget(delay=_DELAY)
		second = _makeFocusTarget(delay=_DELAY)
		IAccessibleHandler.processFocusNVDAEvent(first)
		IAccessibleHandler.processFocusNVDAEvent(second)
		self.assertEqual(2, callLater.call_count)
		# Run the deferred callbacks in the order they were scheduled.
		for call in callLater.call_args_list:
			_delay, callback, *args = call.args
			callback(*args)
		queueEvent.assert_called_once_with("gainFocus", first)
