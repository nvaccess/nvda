# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for browse mode alt+up/down sentence-vs-collapse/expand dispatch.

Covers ``BrowseModeDocumentTreeInterceptor._isExpandableControlAtCaret``, the discriminator
that decides whether ``alt+upArrow``/``alt+downArrow`` should collapse/expand a control or
navigate by sentence.  The method is exercised against a duck-typed ``self``, which avoids
constructing a tree interceptor and its virtual buffer.
"""

import unittest

import browseMode
import controlTypes


class _FakeObject:
	"""A minimal stand-in for an NVDAObject with just a role and states."""

	def __init__(self, role=controlTypes.Role.UNKNOWN, states=frozenset()):
		self.role = role
		self.states = states


class _FakeInterceptor:
	"""A duck-typed ``self`` exposing only what ``_isExpandableControlAtCaret`` reads."""

	ALWAYS_SWITCH_TO_PASS_THROUGH_ROLES = (
		browseMode.BrowseModeDocumentTreeInterceptor.ALWAYS_SWITCH_TO_PASS_THROUGH_ROLES
	)
	_EXPAND_OR_POPUP_STATES = browseMode.BrowseModeDocumentTreeInterceptor._EXPAND_OR_POPUP_STATES
	_isExpandableControlAtCaret = browseMode.BrowseModeDocumentTreeInterceptor._isExpandableControlAtCaret

	def __init__(self, focusable, root):
		self.currentFocusableNVDAObject = focusable
		self.rootNVDAObject = root


def _check(focusable, root):
	return _FakeInterceptor(focusable, root)._isExpandableControlAtCaret()


class TestIsExpandableControlAtCaret(unittest.TestCase):
	def setUp(self):
		# Plain document content: the focusable-node lookup yields the root object.
		self.root = _FakeObject(role=controlTypes.Role.DOCUMENT)

	def test_plainContent_isRoot(self):
		"""On plain content the focusable object is the root, so sentence nav is used."""
		self.assertFalse(_check(self.root, self.root))

	def test_none(self):
		"""A missing focusable object falls through to sentence nav rather than erroring."""
		self.assertFalse(_check(None, self.root))

	def test_comboBoxRole(self):
		"""A combo box keeps collapse/expand regardless of its states."""
		obj = _FakeObject(role=controlTypes.Role.COMBOBOX)
		self.assertTrue(_check(obj, self.root))

	def test_arrowConsumingRole(self):
		"""Other arrow-key-consuming roles (e.g. slider) keep collapse/expand."""
		obj = _FakeObject(role=controlTypes.Role.SLIDER)
		self.assertTrue(_check(obj, self.root))

	def test_autocompleteStateWithoutCollapsed(self):
		"""An editable/autocomplete combo box is caught by AUTOCOMPLETE even without COLLAPSED."""
		obj = _FakeObject(
			role=controlTypes.Role.EDITABLETEXT,
			states={controlTypes.State.EDITABLE, controlTypes.State.AUTOCOMPLETE},
		)
		self.assertTrue(_check(obj, self.root))

	def test_collapsedState(self):
		"""A collapsed control keeps collapse/expand."""
		obj = _FakeObject(role=controlTypes.Role.BUTTON, states={controlTypes.State.COLLAPSED})
		self.assertTrue(_check(obj, self.root))

	def test_hasPopupState(self):
		"""A menu/disclosure button (HASPOPUP) keeps collapse/expand."""
		obj = _FakeObject(role=controlTypes.Role.BUTTON, states={controlTypes.State.HASPOPUP})
		self.assertTrue(_check(obj, self.root))

	def test_plainLink_navigatesBySentence(self):
		"""A focusable link with no relevant role/state falls through to sentence nav."""
		obj = _FakeObject(role=controlTypes.Role.LINK)
		self.assertFalse(_check(obj, self.root))

	def test_plainButton_navigatesBySentence(self):
		"""A plain button (no popup/expand state) falls through to sentence nav."""
		obj = _FakeObject(role=controlTypes.Role.BUTTON)
		self.assertFalse(_check(obj, self.root))
