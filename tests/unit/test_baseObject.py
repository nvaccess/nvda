#tests/unit/test_braille.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Babbage B.V.

"""Unit tests for the baseObject module, its classes and their derivatives."""

import unittest
from baseObject import ScriptableObject
from objectProvider import PlaceholderNVDAObject
import controlTypes
from config import conf
import api
import globalVars
from scriptHandler import script

class NVDAObjectWithDecoratedScript(PlaceholderNVDAObject):
	"""An object with a decorated script."""

	@script(gestures=["kb:a"])
	def script_a(self, gesture):
		return

class NVDAObjectWithGestureMap(PlaceholderNVDAObject):
	"""An object with a script that is bound to a gesture in a gesture map."""

	def script_b(self, gesture):
		return

	__gestures = {
		"kb:b": "b"
	}

class NVDAObjectWithDecoratedScriptAndGestureMap(PlaceholderNVDAObject):
	"""An object with a decorated script
	and a script that is bound to a gesture in a gesture map.
	"""

	@script(gestures=["kb:c"])
	def script_c(self, gesture):
		return

	def script_d(self, gesture):
		return

	__gestures = {
		"kb:d": "d",
	}

class SubclassedNVDAObjectWithDecoratedScriptAndGestureMap(
	NVDAObjectWithDecoratedScript,
	NVDAObjectWithGestureMap,
	NVDAObjectWithDecoratedScriptAndGestureMap
):

	@script(gestures=["kb:e"])
	def script_e(self, gesture):
		return

	def script_f(self, gesture):
		return

	__gestures = {
		"kb:f": "f",
	}

class TestScriptableObject(unittest.TestCase):
	"""A test that verifies whether scripts are properly bound to associated gestures."""

	def test_decoratedScript(self):
		obj = NVDAObjectWithDecoratedScript()
		self.assertIn("kb:a", obj._gestureMap)

	def test_gestureMap(self):
		obj = NVDAObjectWithGestureMap()
		self.assertIn("kb:b", obj._gestureMap)

	def test_decoratedScriptAndGestureMap(self):
		obj = NVDAObjectWithDecoratedScriptAndGestureMap()
		self.assertIn("kb:c", obj._gestureMap)
		self.assertIn("kb:d", obj._gestureMap)

	def test_decoratedScriptsAndGestureMapsIfSubclassed(self):
		obj = SubclassedNVDAObjectWithDecoratedScriptAndGestureMap()
		for key in ("a", "b", "c", "d", "e", "f"):
			self.assertIn("kb:%s" % key, obj._gestureMap)
