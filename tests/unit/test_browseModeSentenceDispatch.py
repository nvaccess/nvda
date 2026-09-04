# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for browse mode alt+up/down sentence-vs-collapse/expand dispatch.

Covers ``BrowseModeDocumentTreeInterceptor._isExpandableControlAtCaret``, the discriminator
that decides whether ``alt+upArrow``/``alt+downArrow`` should collapse/expand a control or
navigate by sentence, and ``getAlternativeScript``, which swaps the script accordingly.
"""

import unittest
from types import SimpleNamespace

import browseMode
from controlTypes import Role, State

from .objectProvider import NVDAObjectWithRole


class _Interceptor(browseMode.BrowseModeDocumentTreeInterceptor):
	"""An interceptor carrying only the two objects the discriminator reads.

	``super().__init__`` is skipped so that no virtual buffer is constructed.
	"""

	def __init__(self, focusable: NVDAObjectWithRole | None, root: NVDAObjectWithRole):
		self.currentFocusableNVDAObject = focusable
		self.rootNVDAObject = root
		self._passThrough = False


def _obj(role: Role, *states: State) -> NVDAObjectWithRole:
	obj = NVDAObjectWithRole(role=role)
	obj.states = frozenset(states)
	return obj


class TestIsExpandableControlAtCaret(unittest.TestCase):
	def setUp(self):
		self.root = _obj(Role.DOCUMENT)

	def test_dispatch(self):
		cases = (
			("plain content, focusable is the root", self.root, False),
			("no focusable object", None, False),
			("combo box", _obj(Role.COMBOBOX), True),
			("slider", _obj(Role.SLIDER), True),
			("button offering autocompletion", _obj(Role.BUTTON, State.AUTOCOMPLETE), True),
			("collapsed button", _obj(Role.BUTTON, State.COLLAPSED), True),
			("expanded button", _obj(Role.BUTTON, State.EXPANDED), True),
			("button with a popup", _obj(Role.BUTTON, State.HASPOPUP), True),
			("button opening a list", _obj(Role.BUTTON, State.HASPOPUP_LIST), True),
			("button opening a dialog", _obj(Role.BUTTON, State.HASPOPUP_DIALOG), True),
			("button opening a grid", _obj(Role.BUTTON, State.HASPOPUP_GRID), True),
			("button opening a tree", _obj(Role.BUTTON, State.HASPOPUP_TREE), True),
			("plain link", _obj(Role.LINK), False),
			("plain button", _obj(Role.BUTTON), False),
		)
		for description, focusable, expected in cases:
			with self.subTest(description):
				interceptor = _Interceptor(focusable, self.root)
				self.assertEqual(interceptor._isExpandableControlAtCaret(), expected)


class TestGetAlternativeScript(unittest.TestCase):
	def setUp(self):
		self.root = _obj(Role.DOCUMENT)
		self.gesture = SimpleNamespace(isCharacter=False)

	def test_expandableControl_swapsToCollapseOrExpand(self):
		interceptor = _Interceptor(_obj(Role.COMBOBOX), self.root)
		for script in (
			interceptor.script_moveBySentence_back,
			interceptor.script_moveBySentence_forward,
		):
			with self.subTest(script.__name__):
				self.assertEqual(
					interceptor.getAlternativeScript(self.gesture, script),
					interceptor.script_collapseOrExpandControl,
				)

	def test_plainContent_keepsSentenceScript(self):
		interceptor = _Interceptor(self.root, self.root)
		script = interceptor.script_moveBySentence_forward
		self.assertEqual(interceptor.getAlternativeScript(self.gesture, script), script)

	def test_otherScript_isUntouched(self):
		interceptor = _Interceptor(_obj(Role.COMBOBOX), self.root)
		script = interceptor.script_collapseOrExpandControl
		self.assertEqual(interceptor.getAlternativeScript(self.gesture, script), script)
