# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2021 NV Access Limited, Babbage B.V.

"""Unit tests for the controlTypes module.
"""
import enum
import unittest
import controlTypes
from . import PlaceholderNVDAObject
from controlTypes.processAndLabelStates import _processNegativeStates, _processPositiveStates


class TestLabels(unittest.TestCase):
	_noDisplayStringRoles = {
	}
	_noDisplayStringStates = {
		# HAS_ARIA_DETAILS is not used internally to NVDA, only exists for backwards
		# compatibility of the add-on API
		controlTypes.State.HAS_ARIA_DETAILS,
		controlTypes.State.INDETERMINATE,
	}
	_noNegDisplayStringStates = {
		# HAS_ARIA_DETAILS is not used internally to NVDA, only exists for backwards
		# compatibility of the add-on API
		controlTypes.State.HAS_ARIA_DETAILS,
		controlTypes.State.INDETERMINATE,
	}

	def test_role_displayString(self):
		"""Test to check whether every role has its own display string
		Roles without display strings should be explicitly listed in _noDisplayStringRoles, these
		will be checked to ensure a KeyError is raised if displayString is accessed.
		"""
		rolesExpectingDisplayString = set(controlTypes.Role).difference(self._noDisplayStringRoles)
		for role in rolesExpectingDisplayString:
			self.assertTrue(role.displayString)

		for role in self._noDisplayStringRoles:
			with self.assertRaises(KeyError):
				role.displayString

	def test_state_displayString(self):
		"""Test to check whether every state has its own display string
		States without display strings should be explicitly listed in _noDisplayStringStates, these
		will be checked to ensure a KeyError is raised if displayString is accessed.
		"""
		statesExpectingDisplayString = set(controlTypes.State).difference(self._noDisplayStringStates)
		for state in statesExpectingDisplayString:
			self.assertTrue(state.displayString)

		for state in self._noDisplayStringStates:
			with self.assertRaises(KeyError):
				state.displayString

	def test_state_negativeDisplayString(self):
		"""Test to check whether every state has its own negative display string
		States without negative display strings should be explicitly listed in _noNegDisplayStringStates, these
		will be checked to ensure a KeyError is raised if negativeDisplayString is accessed.
		"""
		statesExpectingNegDispString = set(controlTypes.State).difference(self._noNegDisplayStringStates)
		for state in statesExpectingNegDispString:
			self.assertTrue(state.negativeDisplayString)

		for state in self._noNegDisplayStringStates:
			with self.assertRaises(KeyError):
				state.negativeDisplayString


class TestProcessStates(unittest.TestCase):

	def setUp(self):
		self.obj = PlaceholderNVDAObject()
		self.obj.role = controlTypes.Role.CHECKBOX
		self.obj.states = {
			controlTypes.State.FOCUSABLE,
			controlTypes.State.INVALID_ENTRY,
			controlTypes.State.FOCUSED,
			controlTypes.State.REQUIRED
		}

	def test_positiveStates(self):
		self.assertSetEqual(
			_processPositiveStates(
				self.obj.role,
				self.obj.states,
				controlTypes.OutputReason.FOCUS,
				self.obj.states
			),
			{controlTypes.State.INVALID_ENTRY, controlTypes.State.REQUIRED}
		)

	def test_negativeStates(self):
		self.assertSetEqual(
			_processNegativeStates(
				self.obj.role,
				self.obj.states,
				controlTypes.OutputReason.FOCUS,
				None
			),
			{controlTypes.State.CHECKED}
		)

class TestStateOrder(unittest.TestCase):

	def test_positiveMergedStatesOutput(self):
		obj = PlaceholderNVDAObject()
		obj.role = controlTypes.Role.CHECKBOX
		obj.states = {
			controlTypes.State.CHECKED,
			controlTypes.State.FOCUSABLE,
			controlTypes.State.FOCUSED,
			controlTypes.State.SELECTED,
			controlTypes.State.SELECTABLE
		}
		self.assertEqual(
			controlTypes.processAndLabelStates(
				obj.role,
				obj.states,
				controlTypes.OutputReason.FOCUS,
				obj.states,
				None
			),
			[controlTypes.State.CHECKED.displayString]
		)

	def test_negativeMergedStatesOutput(self):
		obj = PlaceholderNVDAObject()
		obj.role = controlTypes.Role.CHECKBOX
		obj.states = {
			controlTypes.State.FOCUSABLE,
			controlTypes.State.FOCUSED,
			controlTypes.State.SELECTED,
			controlTypes.State.SELECTABLE
		}
		self.assertEqual(
			controlTypes.processAndLabelStates(
				obj.role,
				obj.states,
				controlTypes.OutputReason.FOCUS,
				obj.states,
				None
			),
			[controlTypes.State.CHECKED.negativeDisplayString]
		)


class TestBackCompat(unittest.TestCase):

	def test_statesValues(self):
		class oldStates(enum.IntEnum):
			# Copied from commit d4586a5d907dd4dec761d3234147fa5fd6186b37
			UNAVAILABLE = 0x1
			FOCUSED = 0x2
			SELECTED = 0x4
			BUSY = 0x8
			PRESSED = 0x10
			CHECKED = 0x20
			HALFCHECKED = 0x40
			READONLY = 0x80
			EXPANDED = 0x100
			COLLAPSED = 0x200
			INVISIBLE = 0x400
			VISITED = 0x800
			LINKED = 0x1000
			HASPOPUP = 0x2000
			PROTECTED = 0x4000
			REQUIRED = 0x8000
			DEFUNCT = 0x10000
			INVALID_ENTRY = 0x20000
			MODAL = 0x40000
			AUTOCOMPLETE = 0x80000
			MULTILINE = 0x100000
			ICONIFIED = 0x200000
			OFFSCREEN = 0x400000
			SELECTABLE = 0x800000
			FOCUSABLE = 0x1000000
			CLICKABLE = 0x2000000
			EDITABLE = 0x4000000
			CHECKABLE = 0x8000000
			DRAGGABLE = 0x10000000
			DRAGGING = 0x20000000
			DROPTARGET = 0x40000000
			SORTED = 0x80000000
			SORTED_ASCENDING = 0x100000000
			SORTED_DESCENDING = 0x200000000
			HASLONGDESC = 0x400000000
			PINNED = 0x800000000
			HASFORMULA = 0x1000000000  # Mostly for spreadsheets
			HASCOMMENT = 0x2000000000
			OBSCURED = 0x4000000000
			CROPPED = 0x8000000000
			OVERFLOWING = 0x10000000000
			UNLOCKED = 0x20000000000
			HAS_ARIA_DETAILS = 0x40000000000
			HASNOTE = 0x80000000000
		for old in oldStates:
			new = controlTypes.State[old.name]
			self.assertEqual(new.value, old.value, msg=f"Value not equal: {new.name}")
			self.assertEqual(new, old.value, msg=f"Can't treat as integer: {new.name}")
			self.assertEqual(
				controlTypes.State(old.value),
				old.value,
				msg=f"Can't construct from integer value: {new.name}"
			)
