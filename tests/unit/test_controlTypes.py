#tests/unit/test_controlTypes.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017-2019 NV Access Limited, Babbage B.V.

"""Unit tests for the controlTypes module.
"""

import unittest
import controlTypes
from . import PlaceholderNVDAObject

class TestLabels(unittest.TestCase):

	def test_roleLabels(self):
		"""Test to check whether every role has its own label in controlTypes.roleLabels"""
		for name, const in vars(controlTypes).items():
			if name.startswith("ROLE_"):
				self.assertIsNotNone(controlTypes.roleLabels.get(const),msg="{name} has no label".format(name=name))

	def test_positiveStateLabels(self):
		"""Test to check whether every state has its own label in controlTypes.stateLabels"""
		for name, const in vars(controlTypes).items():
			if name.startswith("STATE_"):
				self.assertIsNotNone(controlTypes.stateLabels.get(const),msg="{name} has no label".format(name=name))

class TestProcessStates(unittest.TestCase):

	def setUp(self):
		self.obj = PlaceholderNVDAObject()
		self.obj.role = controlTypes.ROLE_CHECKBOX
		self.obj.states = {
			controlTypes.STATE_FOCUSABLE,
			controlTypes.STATE_INVALID_ENTRY,
			controlTypes.STATE_FOCUSED,
			controlTypes.STATE_REQUIRED
		}

	def test_positiveStates(self):
		self.assertSetEqual(
			controlTypes.processPositiveStates(
				self.obj.role,
				self.obj.states,
				controlTypes.REASON_FOCUS,
				self.obj.states
			),
			{controlTypes.STATE_INVALID_ENTRY, controlTypes.STATE_REQUIRED}
		)

	def test_negativeStates(self):
		self.assertSetEqual(
			controlTypes.processNegativeStates(
				self.obj.role,
				self.obj.states,
				controlTypes.REASON_FOCUS,
				None
			),
			{controlTypes.STATE_CHECKED}
		)

class TestStateOrder(unittest.TestCase):

	def test_positiveMergedStatesOutput(self):
		obj = PlaceholderNVDAObject()
		obj.role = controlTypes.ROLE_CHECKBOX
		obj.states = {
			controlTypes.STATE_CHECKED,
			controlTypes.STATE_FOCUSABLE,
			controlTypes.STATE_FOCUSED,
			controlTypes.STATE_SELECTED,
			controlTypes.STATE_SELECTABLE
		}
		self.assertEqual(
			controlTypes.processAndLabelStates(
				obj.role,
				obj.states,
				controlTypes.REASON_FOCUS,
				obj.states,
				None
			),
			[controlTypes.stateLabels[controlTypes.STATE_CHECKED]]
		)

	def test_negativeMergedStatesOutput(self):
		obj = PlaceholderNVDAObject()
		obj.role = controlTypes.ROLE_CHECKBOX
		obj.states = {
			controlTypes.STATE_FOCUSABLE,
			controlTypes.STATE_FOCUSED,
			controlTypes.STATE_SELECTED,
			controlTypes.STATE_SELECTABLE
		}
		self.assertEqual(
			controlTypes.processAndLabelStates(
				obj.role,
				obj.states,
				controlTypes.REASON_FOCUS,
				obj.states,
				None
			),
			[controlTypes.negativeStateLabels[controlTypes.STATE_CHECKED]]
		)
