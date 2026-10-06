# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for browse mode alt+up/down sentence-vs-collapse/expand dispatch.

Covers ``BrowseModeDocumentTreeInterceptor._isExpandableControlAtCaret``, the discriminator
that reads the control fields at the caret to decide whether ``alt+upArrow``/``alt+downArrow``
should collapse/expand a control or navigate by sentence, and ``getAlternativeScript``,
which swaps the script accordingly.
"""

import unittest
from types import SimpleNamespace

import browseMode
import textInfos
from controlTypes import Role, State


class _CaretTextInfo:
	"""A text info at the caret that yields a fixed field list."""

	def __init__(self, fields: list[textInfos.FieldCommand | str]):
		self._fields = fields
		self.expandedUnit: str | None = None

	def expand(self, unit: str) -> None:
		self.expandedUnit = unit

	def getTextWithFields(self, formatConfig: dict | None = None) -> list[textInfos.FieldCommand | str]:
		return self._fields


class _Interceptor(browseMode.BrowseModeDocumentTreeInterceptor):
	"""An interceptor whose caret text info is the only thing the discriminator reads.

	``super().__init__`` is skipped so that no virtual buffer is constructed.
	"""

	def __init__(self, fields: list[textInfos.FieldCommand | str]):
		self._fields = fields
		self._passThrough = False
		self.textInfo: _CaretTextInfo | None = None

	def makeTextInfo(self, position) -> _CaretTextInfo:
		assert position == textInfos.POSITION_CARET
		self.textInfo = _CaretTextInfo(self._fields)
		return self.textInfo


def _control(role: Role, *states: State) -> textInfos.ControlField:
	return textInfos.ControlField(role=role, states=set(states))


_DOCUMENT = _control(Role.DOCUMENT, State.FOCUSABLE, State.FOCUSED, State.READONLY)


def _fields(*controls: textInfos.ControlField) -> list[textInfos.FieldCommand | str]:
	"""Build the field list for one character at the caret, nested in the given controls, outermost first."""
	return [
		*(textInfos.FieldCommand("controlStart", control) for control in controls),
		"x",
		*(textInfos.FieldCommand("controlEnd", None) for _ in controls),
	]


class TestIsExpandableControlAtCaret(unittest.TestCase):
	def test_expandsToCharacter(self):
		interceptor = _Interceptor(_fields(_DOCUMENT))
		interceptor._isExpandableControlAtCaret()
		self.assertEqual(interceptor.textInfo.expandedUnit, textInfos.UNIT_CHARACTER)

	def test_dispatch(self):
		cases = (
			("plain content in the document", _fields(_DOCUMENT), False),
			("plain content in a section", _fields(_DOCUMENT, _control(Role.SECTION)), False),
			("no focusable control at all", _fields(_control(Role.SECTION)), False),
			("combo box", _fields(_DOCUMENT, _control(Role.COMBOBOX, State.FOCUSABLE)), True),
			("combo box that is not focusable", _fields(_DOCUMENT, _control(Role.COMBOBOX)), False),
			("slider", _fields(_DOCUMENT, _control(Role.SLIDER, State.FOCUSABLE)), True),
			(
				"button offering autocompletion",
				_fields(_DOCUMENT, _control(Role.BUTTON, State.FOCUSABLE, State.AUTOCOMPLETE)),
				True,
			),
			(
				"collapsed button",
				_fields(_DOCUMENT, _control(Role.BUTTON, State.FOCUSABLE, State.COLLAPSED)),
				True,
			),
			(
				"expanded button",
				_fields(_DOCUMENT, _control(Role.BUTTON, State.FOCUSABLE, State.EXPANDED)),
				True,
			),
			(
				"button with a popup",
				_fields(_DOCUMENT, _control(Role.BUTTON, State.FOCUSABLE, State.HASPOPUP)),
				True,
			),
			(
				"button opening a list",
				_fields(_DOCUMENT, _control(Role.BUTTON, State.FOCUSABLE, State.HASPOPUP_LIST)),
				True,
			),
			(
				"button opening a dialog",
				_fields(_DOCUMENT, _control(Role.BUTTON, State.FOCUSABLE, State.HASPOPUP_DIALOG)),
				True,
			),
			(
				"button opening a grid",
				_fields(_DOCUMENT, _control(Role.BUTTON, State.FOCUSABLE, State.HASPOPUP_GRID)),
				True,
			),
			(
				"button opening a tree",
				_fields(_DOCUMENT, _control(Role.BUTTON, State.FOCUSABLE, State.HASPOPUP_TREE)),
				True,
			),
			("plain link", _fields(_DOCUMENT, _control(Role.LINK, State.FOCUSABLE)), False),
			("plain button", _fields(_DOCUMENT, _control(Role.BUTTON, State.FOCUSABLE)), False),
			(
				"combo box inside a link",
				_fields(
					_DOCUMENT,
					_control(Role.LINK, State.FOCUSABLE),
					_control(Role.COMBOBOX, State.FOCUSABLE),
				),
				True,
			),
			(
				"span inside a link",
				_fields(_DOCUMENT, _control(Role.LINK, State.FOCUSABLE), _control(Role.SECTION)),
				False,
			),
		)
		for description, fields, expected in cases:
			with self.subTest(description):
				interceptor = _Interceptor(fields)
				self.assertEqual(interceptor._isExpandableControlAtCaret(), expected)


class TestGetAlternativeScript(unittest.TestCase):
	def setUp(self):
		self.gesture = SimpleNamespace(isCharacter=False)
		self.comboBoxFields = _fields(_DOCUMENT, _control(Role.COMBOBOX, State.FOCUSABLE))

	def test_expandableControl_swapsToCollapseOrExpand(self):
		interceptor = _Interceptor(self.comboBoxFields)
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
		interceptor = _Interceptor(_fields(_DOCUMENT))
		script = interceptor.script_moveBySentence_forward
		self.assertEqual(interceptor.getAlternativeScript(self.gesture, script), script)

	def test_otherScript_isUntouched(self):
		interceptor = _Interceptor(self.comboBoxFields)
		script = interceptor.script_collapseOrExpandControl
		self.assertEqual(interceptor.getAlternativeScript(self.gesture, script), script)
