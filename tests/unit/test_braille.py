#tests/unit/test_braille.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited, Babbage B.V.

"""Unit tests for the braille module.
"""

import unittest
import braille
from . import PlaceholderNVDAObject
import controlTypes
import api
from config import conf
import api
import globalVars

class NVDAObjectWithRole(PlaceholderNVDAObject):
	"""An object that accepts a role as one of its construction parameters.
	The name of the object will be set with the associated role label.
	This class is used to quickly create objects for a fake focus ancestry."""

	def __init__(self, role=controlTypes.ROLE_UNKNOWN,**kwargs):
		super(NVDAObjectWithRole,self).__init__(**kwargs)
		self.role=role

	def _get_name(self):
		return controlTypes.roleLabels.get(self.role,controlTypes.ROLE_UNKNOWN)

class TestFocusContextPresentation(unittest.TestCase):
	"""A test for the different focus context presentation options."""

	@property
	def regionsWithPositions(self):
		return list(braille.handler.buffer.regionsWithPositions)

	def setUp(self):
		"""Set up a fake focus object and give it some ancestry."""
		self.obj=NVDAObjectWithRole(role=controlTypes.ROLE_LISTITEM)
		# Create and set a fake desktop object
		self.fakeDesktopObj=NVDAObjectWithRole(role=controlTypes.ROLE_WINDOW)
		api.setDesktopObject(self.fakeDesktopObj)
		# Forcefully create a fake focus ancestry
		globalVars.focusAncestors=[api.getDesktopObject(),NVDAObjectWithRole(role=controlTypes.ROLE_DIALOG),NVDAObjectWithRole(role=controlTypes.ROLE_LIST)]
		braille.handler.handleGainFocus(self.obj)
		# Make sure that we are testing with three regions
		self.assertEqual(len(self.regionsWithPositions),3)

	def test_fillDisplay(self):
		"""Test for the case where both the focus object and its ancestors should be visible on a 40 cell display."""
		conf['braille']['focusContextPresentation']="fill"
		# Since we set the presentation mode, simulate another gainFocus so the regions will be updated properly
		braille.handler.handleGainFocus(self.obj)
		# WindowEndPos should be retrieved before we attempt to get the start position
		# This is because getting windowEndPos can update windowStartPos
		# Both the focus object and its parent should fit on the display
		# Thus, the window end position is equal to the end position of the 3rd region
		self.assertEqual(braille.handler.buffer.windowEndPos,self.regionsWithPositions[2][2])
		# The start position should be 0 now
		self.assertEqual(braille.handler.buffer.windowStartPos,0)

	def test_scrollOnly(self):
		"""Test for the case where the focus object should be visible hard left on a display."""
		conf['braille']['focusContextPresentation']="scroll"
		braille.handler.handleGainFocus(self.obj)
		# Only the focus object should be visible on the display
		# This means that the window end position is equal to the end position of the 3rd region
		self.assertEqual(braille.handler.buffer.windowEndPos,self.regionsWithPositions[2][2])
		# This also means that the window start position is equal to the start position of the 3rd region
		self.assertEqual(braille.handler.buffer.windowStartPos,self.regionsWithPositions[2][1])

	def test_hybrid(self):
		"""Test for the case where the focus object as well as ancestry differences should be visible on the display"""
		conf['braille']['focusContextPresentation']="hybrid"
		# Clean up the cached ancestry regions
		braille.invalidateCachedFocusAncestors(0)
		# Regenerate the regions
		braille.handler.handleGainFocus(self.obj)
		# Both the focus object and its parents should be visible, equivalent to always fill display
		self.assertEqual(braille.handler.buffer.windowEndPos,self.regionsWithPositions[2][2])
		self.assertEqual(braille.handler.buffer.windowStartPos,0)
		# Do another focus to simulate a new focus object with equal ancestry
		braille.handler.handleGainFocus(self.obj)
		# Only the focus object should be visible now, equivalent to scroll only
		self.assertEqual(braille.handler.buffer.windowEndPos,self.regionsWithPositions[2][2])
		self.assertEqual(braille.handler.buffer.windowStartPos,self.regionsWithPositions[2][1])
		# Clean up the cached focus ancestors
		braille.invalidateCachedFocusAncestors(2)
		# Do another focus to simulate a new focus object with different ancestry
		braille.handler.handleGainFocus(self.obj)
		# The list and the list item should be visible
		# This still means that the window end position is equal to the end position of the 3rd region
		self.assertEqual(braille.handler.buffer.windowEndPos,self.regionsWithPositions[2][2])
		# The window start position is equal to the start position of the 2nd region
		self.assertEqual(braille.handler.buffer.windowStartPos,self.regionsWithPositions[1][1])
