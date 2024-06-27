# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021-2022 NV Access Limited, Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
This module provides helpers and a common format to define UIA custom properties.
The common custom properties are defined here.
Custom properties specific to an application should be defined within a NVDAObjects/UIA
submodule specific to that application, E.G. 'NVDAObjects/UIA/excel.py'

UIA originally had hard coded 'static' ID's for properties.
For an example see 'UIA_SelectionPatternId' in
`source/comInterfaces/_944DE083_8FB8_45CF_BCB7_C477ACB2F897_0_1_0.py`
imported via `UIAutomationClient.py`.
When a new property was added the UIA spec had to be updated.
Now a mechanism is in place to allow applications to register "custom properties".
This relies on both the UIA server application and the UIA client application sharing a known
GUID for the property.
"""

import dataclasses
from typing import (
	ClassVar,
	Dict,
)

from comtypes import (
	GUID,
	byref,
)
from .constants import (
	UIAutomationType,
)


@dataclasses.dataclass
class CustomPropertyInfo:
	"""Holds information about a CustomProperty
	This makes it easy to define custom properties to be loaded.
	"""
	guid: GUID
	programmaticName: str
	uiaType: UIAutomationType
	_registeredProperties: ClassVar[Dict[GUID, int]] = dict()

	def _registerCustomProperty(self) -> int:
		""" Registers a custom property with a given id.

		UIA will return the id to use when given the GUID.
		Any application can be first to register a custom property, subsequent applications
		will be given the same id.
		"""
		import NVDAHelper
		return NVDAHelper.localLib.registerUIAProperty(
			byref(self.guid),
			self.programmaticName,
			self.uiaType
		)

	@property
	def id(self) -> int:
		"""Return the integer id of the given property registering it first if necessary.

		Id's of all registered properties are cached when requested for the first time
		to prevent unnecessary work by repeatedly interacting with UIA.
		"""
		try:
			propertyId = self._registeredProperties[self.guid]
		except KeyError:
			propertyId = self._registerCustomProperty()
			self._registeredProperties[self.guid] = propertyId
		return propertyId


class CustomPropertiesCommon:
	"""UIA 'custom properties' common to all applications.
	Once registered, all subsequent registrations will return the same ID value.
		"""

	def __init__(self):

		self.itemIndex = CustomPropertyInfo(
			guid=GUID("{92A053DA-2969-4021-BF27-514CFC2E4A69}"),
			programmaticName="ItemIndex",
			uiaType=UIAutomationType.INT,
		)

		self.itemCount = CustomPropertyInfo(
			guid=GUID("{ABBF5C45-5CCC-47b7-BB4E-87CB87BBD162}"),
			programmaticName="ItemCount",
			uiaType=UIAutomationType.INT,
		)

		# A property for fetching raw MathML from an equation node in Microsoft Word.
		# Available in MS Word build 14326 and higher.
		self.word_mathml = CustomPropertyInfo(
			guid=GUID("{FA170AB3-3229-4E7C-827F-DD05EE0481D9}"),
			programmaticName="Word.MathML",
			uiaType=UIAutomationType.STRING,
		)
