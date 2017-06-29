#tests/unit/test_controlTypes.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited, Babbage B.V.

"""Unit tests for the controlTypes module.
"""

import unittest
from controlTypes import *
from . import PlaceholderNVDAObject

class TestProcessStates(unittest.TestCase):
	obj = PlaceholderNVDAObject()
	obj.role = ROLE_CHECKBOX
	obj.states = set((STATE_FOCUSABLE, STATE_INVALID_ENTRY, STATE_FOCUSED, STATE_REQUIRED))

	def test_positiveStates(self):
		self.assertEqual(processPositiveStates(self.obj.role, self.obj.states, REASON_FOCUS, self.obj.states), set([STATE_INVALID_ENTRY, STATE_REQUIRED]))

	def test_negativeStates(self):
		self.assertEqual(processNegativeStates(self.obj.role, self.obj.states, REASON_FOCUS, self.obj.states), set([STATE_CHECKED]))

class TestStateOrder(unittest.TestCase):

	def test_positiveMergedStatesOutput(self):
		obj = PlaceholderNVDAObject()
		obj.role = ROLE_CHECKBOX
		obj.states = set((STATE_CHECKED, STATE_FOCUSABLE, STATE_FOCUSED, STATE_SELECTED, STATE_SELECTABLE))
		self.assertEqual(processAndLabelStates(obj.role, obj.states, REASON_FOCUS, obj.states, None), [stateLabels[STATE_SELECTED],stateLabels[STATE_CHECKED]])

	def test_negativeMergedStatesOutput(self):
		obj = PlaceholderNVDAObject()
		obj.role = ROLE_CHECKBOX
		obj.states = set((STATE_FOCUSABLE, STATE_FOCUSED, STATE_SELECTED, STATE_SELECTABLE))
		self.assertEqual(processAndLabelStates(obj.role, obj.states, REASON_FOCUS, obj.states, None), [stateLabels[STATE_SELECTED],negativeStateLabels[STATE_CHECKED]])
