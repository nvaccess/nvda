#tests/unit/objectProvider.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited, Babbage B.V.

"""Fake object provider implementation for testing of code which uses NVDAObjects.
"""

from NVDAObjects import NVDAObject
import controlTypes

class PlaceholderNVDAObject(NVDAObject):
	processID = None # Must be implemented to instantiate.

class NVDAObjectWithRole(PlaceholderNVDAObject):
	"""An object that accepts a role as one of its construction parameters.
	The name of the object will be set with the associated role label.
	This class can be used to quickly create objects for a fake focus ancestry."""

	def __init__(self, role=controlTypes.Role.UNKNOWN,**kwargs):
		super(NVDAObjectWithRole,self).__init__(**kwargs)
		self.role=role

	# Type information for autoproperty _get_name
	# the translated display string for the role, or unknown
	name: str

	def _get_name(self) -> str:
		try:
			role = controlTypes.Role(self.role)
			role.displayString
		except ValueError:
			role = controlTypes.Role.UNKNOWN
		return role.displayString
