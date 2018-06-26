#tests/unit/test_baseObject.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Babbage B.V.

"""Unit tests for the baseObject module, its classes and their derivatives."""

import unittest
from baseObject import ScriptableObject
from objectProvider import PlaceholderNVDAObject
from scriptHandler import script

class NVDAObjectWithDecoratedScript(PlaceholderNVDAObject):
	"""An object with a decorated script."""

	@script(gestures=["kb:a"])
	def script_alpha(self, gesture):
		return

class NVDAObjectWithGesturesDictionary(PlaceholderNVDAObject):
	"""An object with a script that is bound to a gesture in a L{__gestures} dictionary."""

	def script_bravo(self, gesture):
		return

	__gestures = {
		"kb:b": "bravo"
	}

class NVDAObjectWithDecoratedScriptAndGesturesDictionary(PlaceholderNVDAObject):
	"""An object with a decorated script
	and a script that is bound to a gesture in a L{__gestures} dictionary.
	"""

	@script(gestures=["kb:c"])
	def script_charlie(self, gesture):
		return

	def script_delta(self, gesture):
		return

	__gestures = {
		"kb:d": "delta",
	}

class SubclassedNVDAObjectWithDecoratedScriptAndGesturesDictionary(
	NVDAObjectWithDecoratedScript,
	NVDAObjectWithGesturesDictionary,
	NVDAObjectWithDecoratedScriptAndGesturesDictionary
):
	"""An object with decorated scripts and L{__gestures} dictionaries, based on subclassing."""

	@script(gestures=["kb:e"])
	def script_echo(self, gesture):
		return

	def script_foxtrot(self, gesture):
		return

	__gestures = {
		"kb:f": "foxtrot",
	}

class DynamicNVDAObjectWithDecoratedScriptAndGesturesDictionary(PlaceholderNVDAObject):
	"""An object with decorated scripts and L{__gestures} dictionaries,
	using the chooseOverlayClasses logic to construct a dynamic object."""

	def findOverlayClasses(self, clsList):
		clsList.extend([
			NVDAObjectWithDecoratedScript,
			NVDAObjectWithGesturesDictionary,
			NVDAObjectWithDecoratedScriptAndGesturesDictionary
		])

	@script(gestures=["kb:g"])
	def script_golf(self, gesture):
		return

	def script_hotel(self, gesture):
		return

	__gestures = {
		"kb:h": "hotel",
	}

class TestScriptableObject(unittest.TestCase):
	"""A test that verifies whether scripts are properly bound to associated gestures."""

	def test_decoratedScript(self):
		obj = NVDAObjectWithDecoratedScript()
		self.assertIn("kb:a", obj._gestureMap)

	def test_gesturesDictionary(self):
		obj = NVDAObjectWithGesturesDictionary()
		self.assertIn("kb:b", obj._gestureMap)

	def test_decoratedScriptAndGesturesDictionary(self):
		obj = NVDAObjectWithDecoratedScriptAndGesturesDictionary()
		self.assertIn("kb:c", obj._gestureMap)
		self.assertIn("kb:d", obj._gestureMap)

	def test_decoratedScriptsAndGestureDictionariesIfSubclassed(self):
		obj = SubclassedNVDAObjectWithDecoratedScriptAndGesturesDictionary()
		for key in ("a", "b", "c", "d", "e", "f"):
			self.assertIn("kb:%s" % key, obj._gestureMap)

	def test_decoratedScriptsAndGestureDictionariesIfDynamic(self):
		obj = DynamicNVDAObjectWithDecoratedScriptAndGesturesDictionary()
		for key in ("a", "b", "c", "d", "g", "h"):
			self.assertIn("kb:%s" % key, obj._gestureMap)
