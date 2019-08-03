#tests/unit/test_scriptHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Unit tests for the scriptHandler module."""

import unittest
from scriptHandler import *
from inputCore import SCRCAT_MISC
from sayAllHandler import CURSOR_CARET

class TestScriptDecorator(unittest.TestCase):
	"""A test that verifies the functionality of the L{scriptHandler.script} decorator."""

	def test_scriptdecoration(self):
		@script(
			description="description",
			category=SCRCAT_MISC,
			gesture="kb:a",
			gestures=["kb:b", "kb:c"],
			canPropagate=True,
			bypassInputHelp=True,
			resumeSayAllMode=CURSOR_CARET
		)
		def script_test(self, gesture):
			return

		self.assertEqual(script_test.__doc__, "description")
		self.assertEqual(script_test.category, SCRCAT_MISC)
		self.assertCountEqual(script_test.gestures, ["kb:a", "kb:b", "kb:c"])
		self.assertTrue(script_test.canPropagate)
		self.assertTrue(script_test.bypassInputHelp)
		self.assertEqual(script_test.resumeSayAllMode, CURSOR_CARET)
