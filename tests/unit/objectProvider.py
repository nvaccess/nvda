#tests/unit/objectProvider.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited, Babbage B.V.

"""Fake object provider implementation for testing of code which uses NVDAObjects.
"""

from NVDAObjects import NVDAObject
import controlTypes
from scriptHandler import script

class PlaceholderNVDAObject(NVDAObject):
	processID = None # Must be implemented to instantiate.

class NVDAObjectWithRole(PlaceholderNVDAObject):
	"""An object that accepts a role as one of its construction parameters.
	The name of the object will be set with the associated role label.
	This class can be used to quickly create objects for a fake focus ancestry."""

	def __init__(self, role=controlTypes.ROLE_UNKNOWN,**kwargs):
		super(NVDAObjectWithRole,self).__init__(**kwargs)
		self.role=role

	def _get_name(self):
		return controlTypes.roleLabels.get(self.role,controlTypes.ROLE_UNKNOWN)

class NVDAObjectWithDecoratedScript(PlaceholderNVDAObject):
	"""An object with a decorated script."""

	@script(gestures=["kb:a"])
	def script_a(self, gesture):
		return

class NVDAObjectWithGesturesDictionary(PlaceholderNVDAObject):
	"""An object with a script that is bound to a gesture in a L{__gestures} dictionary."""

	def script_b(self, gesture):
		return

	__gestures = {
		"kb:b": "b"
	}

class NVDAObjectWithDecoratedScriptAndGesturesDictionary(PlaceholderNVDAObject):
	"""An object with a decorated script
	and a script that is bound to a gesture in a L{__gestures} dictionary.
	"""

	@script(gestures=["kb:c"])
	def script_c(self, gesture):
		return

	def script_d(self, gesture):
		return

	__gestures = {
		"kb:d": "d",
	}

class SubclassedNVDAObjectWithDecoratedScriptAndGesturesDictionary(
	NVDAObjectWithDecoratedScript,
	NVDAObjectWithGesturesDictionary,
	NVDAObjectWithDecoratedScriptAndGesturesDictionary
):
	"""An object with decorated scripts and L{__gestures} dictionaries, based on subclassing."""

	@script(gestures=["kb:e"])
	def script_e(self, gesture):
		return

	def script_f(self, gesture):
		return

	__gestures = {
		"kb:f": "f",
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
	def script_g(self, gesture):
		return

	def script_h(self, gesture):
		return

	__gestures = {
		"kb:h": "h",
	}
