# tests/unit/test_baseObject.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Unit tests for the baseObject module, its classes and their derivatives."""

import unittest
from baseObject import AutoPropertyObject
from .objectProvider import PlaceholderNVDAObject
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
		"kb:b": "bravo",
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
	NVDAObjectWithDecoratedScriptAndGesturesDictionary,
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
		clsList.extend(
			[
				NVDAObjectWithDecoratedScript,
				NVDAObjectWithGesturesDictionary,
				NVDAObjectWithDecoratedScriptAndGesturesDictionary,
			],
		)

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


class AutoPropertyObjectWithAbstractProperty(AutoPropertyObject):
	_abstract_x = True

	def _get_x(self):
		return True

	def _set_x(self, value):
		self._attribute = value


class SubclassedAutoPropertyObjectWithAbstractProperty(AutoPropertyObjectWithAbstractProperty):
	pass


class SubclassedAutoPropertyObjectWithImplementedProperty(AutoPropertyObjectWithAbstractProperty):
	def _get_x(self):
		return True


class SubclassedAutoPropertyObjectWithOverriddenClassProperty(AutoPropertyObjectWithAbstractProperty):
	x = True


class TestAbstractAutoPropertyObjects(unittest.TestCase):
	"""A test that verifies whether abstract properties are properly identified as such.
	It also makes sure that abstract properties can be overridden on subclasses.
	"""

	def test_abstractProperty(self):
		self.assertRaisesRegex(
			TypeError,
			"^Can't instantiate abstract class AutoPropertyObjectWithAbstractProperty with abstract method x",
			AutoPropertyObjectWithAbstractProperty,
		)

	def test_subclassedAbstractProperty(self):
		self.assertRaisesRegex(
			TypeError,
			"^Can't instantiate abstract class SubclassedAutoPropertyObjectWithAbstractProperty "
			"with abstract method x",
			SubclassedAutoPropertyObjectWithAbstractProperty,
		)

	def test_implementedProperty(self):
		self.assertTrue(SubclassedAutoPropertyObjectWithImplementedProperty().x)

	def test_overriddenClassProperty(self):
		self.assertTrue(SubclassedAutoPropertyObjectWithOverriddenClassProperty().x)


class AutoPropertyObjectWithClassProperty(AutoPropertyObject):
	@classmethod
	def _get_x(cls):
		return True


class TestAutoClassProperties(unittest.TestCase):
	"""A test that verifies whether automatic class properties work as expected."""

	def test_classProperty(self):
		cls = AutoPropertyObjectWithClassProperty
		self.assertIsInstance(cls.x, bool)
		self.assertIsInstance(cls().x, bool)
