#tests/unit/test_baseObject.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Babbage B.V.

"""Unit tests for the baseObject module, its classes and their derivatives."""

import unittest
from baseObject import ScriptableObject
from objectProvider import *

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
