#tests/unit/test_braille.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017-2019 NV Access Limited, Babbage B.V.

"""Unit tests for the braille module.
"""

import unittest
import braille
from .objectProvider import PlaceholderNVDAObject, NVDAObjectWithRole
import controlTypes
from config import conf
import api
import globalVars

class TestFocusContextPresentation(unittest.TestCase):
	"""A test for the different focus context presentation options."""

	@property
	def regionsWithPositions(self):
		return list(braille.handler.buffer.regionsWithPositions)

	def setUp(self):
		"""Set up a fake focus object and give it some ancestry."""
		self.obj=NVDAObjectWithRole(role=controlTypes.Role.LISTITEM)
		# Forcefully create a fake focus ancestry
		# Note that the braille code excludes the desktop object when getting regions for focus ancestry
		# The resulting focus object including ancestry will look like: "dialog dlg list lst list item"
		globalVars.focusAncestors=[api.getDesktopObject(),NVDAObjectWithRole(role=controlTypes.Role.DIALOG),NVDAObjectWithRole(role=controlTypes.Role.LIST)]
		braille.handler.handleGainFocus(self.obj)
		# Make sure that we are testing with three regions
		self.assertEqual(len(self.regionsWithPositions),3)

	def test_fillDisplay(self):
		"""Test for the case where both the focus object and all its ancestors should be visible on a 40 cell display."""
		conf['braille']['focusContextPresentation']=braille.CONTEXTPRES_FILL
		# Since we set the presentation mode, simulate another gainFocus so the regions will be updated properly
		braille.handler.handleGainFocus(self.obj)
		# WindowEndPos should be retrieved before we attempt to get the start position
		# This is because getting windowEndPos can update windowStartPos
		# Both the focus object and its ancestors should fit on the display
		# Thus, the window end position is equal to the end position of the 3rd region
		self.assertEqual(braille.handler.buffer.windowEndPos,self.regionsWithPositions[2].end)
		# The start position should be 0 now
		self.assertEqual(braille.handler.buffer.windowStartPos,0)

	def test_scrollOnly(self):
		"""Test for the case where the focus object should be visible hard left on a display."""
		conf['braille']['focusContextPresentation']=braille.CONTEXTPRES_SCROLL
		braille.handler.handleGainFocus(self.obj)
		# Only the focus object should be visible on the display
		# This means that the window end position is equal to the end position of the 3rd region
		self.assertEqual(braille.handler.buffer.windowEndPos,self.regionsWithPositions[2].end)
		# This also means that the window start position is equal to the start position of the 3rd region
		self.assertEqual(braille.handler.buffer.windowStartPos,self.regionsWithPositions[2].start)
		# Scroll the braille window back
		braille.handler.scrollBack()
		# Both the focus object and its parents should be visible
		self.assertEqual(braille.handler.buffer.windowEndPos,self.regionsWithPositions[2].end)
		self.assertEqual(braille.handler.buffer.windowStartPos,0)

	def test_changedContext(self):
		"""Test for the case where the focus object as well as ancestry differences should be visible on the display"""
		conf['braille']['focusContextPresentation']=braille.CONTEXTPRES_CHANGEDCONTEXT
		# Clean up the cached ancestry regions
		braille.invalidateCachedFocusAncestors(0)
		# Regenerate the regions
		braille.handler.handleGainFocus(self.obj)
		# Both the focus object and its parents should be visible, equivalent to always fill display
		self.assertEqual(braille.handler.buffer.windowEndPos,self.regionsWithPositions[2].end)
		self.assertEqual(braille.handler.buffer.windowStartPos,0)
		# Do another focus to simulate a new focus object with equal ancestry
		braille.handler.handleGainFocus(self.obj)
		# Only the focus object should be visible now, equivalent to scroll only
		self.assertEqual(braille.handler.buffer.windowEndPos,self.regionsWithPositions[2].end)
		self.assertEqual(braille.handler.buffer.windowStartPos,self.regionsWithPositions[2].start)
		# Scroll the braille window back
		braille.handler.scrollBack()
		# Both the focus object and its parents should be visible
		self.assertEqual(braille.handler.buffer.windowEndPos,self.regionsWithPositions[2].end)
		self.assertEqual(braille.handler.buffer.windowStartPos,0)
		# Clean up the cached focus ancestors
		# specifically, the desktop object (ancestor 0) has no associated region
		# We will keep the region for the dialog (ancestor 1) and consider the list (ancestor 2) as new for this test
		braille.invalidateCachedFocusAncestors(2)
		# Do another focus to simulate a new focus object with different ancestry
		braille.handler.handleGainFocus(self.obj)
		# The list and the list item should be visible
		# This still means that the window end position is equal to the end position of the 3rd region
		self.assertEqual(braille.handler.buffer.windowEndPos,self.regionsWithPositions[2].end)
		# The window start position is equal to the start position of the 2nd region
		self.assertEqual(braille.handler.buffer.windowStartPos,self.regionsWithPositions[1].start)

class TestDisplayTextForGestureIdentifier(unittest.TestCase):
	"""A test for the regular expression code that handles display gesture identifiers."""

	def test_regex(self):
		regex = braille.BrailleDisplayGesture.ID_PARTS_REGEX
		self.assertEqual(
			regex.match('br(noBraille.noModel):noKey1+noKey2').groups(),
			('noBraille', 'noModel', 'noKey1+noKey2')
		)
		self.assertEqual(
			regex.match('br(noBraille):noKey1+noKey2').groups(),
			('noBraille', None, 'noKey1+noKey2')
		)
		# Also try a string which doesn't match the pattern
		self.assertEqual(
			regex.match('br[noBraille.noModel]:noKey1+noKey2'),
			None
		)

	def test_identifierWithModel(self):
		self.assertEqual(
			braille.BrailleDisplayGesture.getDisplayTextForIdentifier('br(noBraille.noModel):noKey1+noKey2'),
			(u'No braille', 'noModel: noKey1+noKey2')
		)

	def test_identifierWithoutModel(self):
		self.assertEqual(
			braille.BrailleDisplayGesture.getDisplayTextForIdentifier('br(noBraille):noKey1+noKey2'),
			(u'No braille', 'noKey1+noKey2')
		)
