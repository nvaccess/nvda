# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for deferring focus ancestor events across browse mode document boundaries."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import api
import browseMode


class _Interceptor(browseMode.BrowseModeDocumentTreeInterceptor):
	def __init__(self, root):
		# Avoid constructing a virtual buffer; exercise the normal focusEntered handler.
		self.rootNVDAObject = root
		self._passThrough = False
		self._enteringFromOutside = False


class TestFocusEntered(unittest.TestCase):
	def setUp(self):
		self.root = object()
		self.interceptor = _Interceptor(self.root)
		self.ancestor = object()
		self.nextHandler = Mock()

	def _focusEntered(self, focusTreeInterceptor, ancestor=None):
		focus = SimpleNamespace(treeInterceptor=focusTreeInterceptor)
		with patch.object(api, "getFocusObject", return_value=focus):
			self.interceptor.event_focusEntered(
				self.ancestor if ancestor is None else ancestor,
				self.nextHandler,
			)

	def test_noFocusTreeInterceptor_callsNextHandler(self):
		self._focusEntered(None)
		self.nextHandler.assert_called_once_with()

	def test_otherTreeInterceptorInBrowseMode_callsNextHandler(self):
		self._focusEntered(SimpleNamespace(passThrough=False))
		self.nextHandler.assert_called_once_with()

	def test_otherTreeInterceptorInFocusMode_defersEvent(self):
		self._focusEntered(SimpleNamespace(passThrough=True))
		self.nextHandler.assert_not_called()

	def test_sameTreeInterceptor_defersEventInBothModes(self):
		for passThrough in (False, True):
			with self.subTest(passThrough=passThrough):
				self.interceptor._passThrough = passThrough
				self._focusEntered(self.interceptor)
				self.nextHandler.assert_not_called()

	def test_rootAncestor_marksEnteringFromOutsideWhenForwardingEvent(self):
		self._focusEntered(None, ancestor=self.root)
		self.assertTrue(self.interceptor._enteringFromOutside)
		self.nextHandler.assert_called_once_with()
