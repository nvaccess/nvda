# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2023 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Unit tests for the BrailleDisplayGesture classes in the braille module.
"""


import braille
import unittest


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
			('No braille', 'noModel: noKey1+noKey2')
		)

	def test_identifierWithoutModel(self):
		self.assertEqual(
			braille.BrailleDisplayGesture.getDisplayTextForIdentifier('br(noBraille):noKey1+noKey2'),
			('No braille', 'noKey1+noKey2')
		)
