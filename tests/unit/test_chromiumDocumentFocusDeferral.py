# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for deferring focus on a Chromium document after the focused element was removed."""

from types import SimpleNamespace  # noqa: I001
from typing import cast
import unittest
from unittest.mock import Mock, PropertyMock, patch

from comtypes import COMError
from comtypes.hresult import E_FAIL

import IAccessibleHandler
import eventHandler
from comInterfaces import IAccessible2Lib as IA2
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.IAccessible import chromium, ia2Web

_WINDOW = 1
_OTHER_WINDOW = 2


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


def _getDelay(oldFocus) -> int:
	document = cast(chromium.Document, SimpleNamespace(windowHandle=_WINDOW))
	with patch.object(eventHandler, "lastQueuedFocusObject", oldFocus):
		return chromium.Document._get_focusEventDelay(document)


class TestChromiumDocumentFocusEventDelay(unittest.TestCase):
	def test_defunctOldFocusInSameWindow_defers(self):
		oldFocus = _makeOldFocus(ia2States=IA2.IA2_STATE_DEFUNCT)
		self.assertEqual(chromium.FOCUS_DELAY_AFTER_FOCUSED_NODE_REMOVED_MS, _getDelay(oldFocus))

	def test_oldFocusRaisingCOMError_defers(self):
		oldFocus = _makeOldFocus(statesError=True)
		self.assertEqual(chromium.FOCUS_DELAY_AFTER_FOCUSED_NODE_REMOVED_MS, _getDelay(oldFocus))

	def test_liveOldFocus_doesNotDefer(self):
		self.assertEqual(0, _getDelay(_makeOldFocus()))

	def test_defunctOldFocusInOtherWindow_doesNotDefer(self):
		oldFocus = _makeOldFocus(ia2States=IA2.IA2_STATE_DEFUNCT, windowHandle=_OTHER_WINDOW)
		self.assertEqual(0, _getDelay(oldFocus))

	def test_defunctOldDocument_doesNotDefer(self):
		oldFocus = _makeOldFocus(ia2States=IA2.IA2_STATE_DEFUNCT, cls=ia2Web.Document)
		self.assertEqual(0, _getDelay(oldFocus))

	def test_noOldFocus_doesNotDefer(self):
		self.assertEqual(0, _getDelay(None))


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
		obj = _makeFocusTarget(delay=150)
		self.assertTrue(IAccessibleHandler.processFocusNVDAEvent(obj))
		queueEvent.assert_not_called()
		callLater.assert_called_once_with(
			150,
			IAccessibleHandler._processDeferredFocusNVDAEvent,
			obj,
			self.oldFocus,
		)

	def test_force_ignoresDelay(self, callLater: Mock, queueEvent: Mock):
		obj = _makeFocusTarget(delay=150)
		self.assertTrue(IAccessibleHandler.processFocusNVDAEvent(obj, force=True))
		queueEvent.assert_called_once_with("gainFocus", obj)
		callLater.assert_not_called()

	def test_deferred_focusUnchanged_queues(self, callLater: Mock, queueEvent: Mock):
		obj = _makeFocusTarget(delay=150)
		IAccessibleHandler._processDeferredFocusNVDAEvent(obj, self.oldFocus)
		queueEvent.assert_called_once_with("gainFocus", obj)

	def test_deferred_focusMoved_drops(self, callLater: Mock, queueEvent: Mock):
		obj = _makeFocusTarget(delay=150)
		with patch.object(eventHandler, "lastQueuedFocusObject", Mock(spec=IAccessible)):
			IAccessibleHandler._processDeferredFocusNVDAEvent(obj, self.oldFocus)
		queueEvent.assert_not_called()

	def test_deferred_noLongerFocused_drops(self, callLater: Mock, queueEvent: Mock):
		obj = _makeFocusTarget(delay=150, allowFocus=False)
		IAccessibleHandler._processDeferredFocusNVDAEvent(obj, self.oldFocus)
		queueEvent.assert_not_called()
