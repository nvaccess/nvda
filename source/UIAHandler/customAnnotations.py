# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021-2022 NV Access Limited, Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
This module provides helpers and a common format to define UIA custom annotation types.
The common custom annotation types are defined here.
Custom annotation types specific to an application should be defined within a NVDAObjects/UIA
submodule specific to that application, E.G. 'NVDAObjects/UIA/excel.py'

UIA originally had hard coded 'static' ID's for annotation types.
For an example see 'AnnotationType_SpellingError' in
`source/comInterfaces/_944DE083_8FB8_45CF_BCB7_C477ACB2F897_0_1_0.py`
imported via `UIAutomationClient.py`.
When a new annotation type was added the UIA spec had to be updated.
Now a mechanism is in place to allow applications to register "custom annotation types".
This relies on both the UIA server application and the UIA client application sharing a known
GUID for the annotation type.
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

import winVersion


@dataclasses.dataclass
class CustomAnnotationTypeInfo:
	"""Holds information about a CustomAnnotationType
	This makes it easy to define custom annotation types to be loaded.
	"""

	guid: GUID
	_registeredAnnotations: ClassVar[Dict[GUID, int]] = dict()

	def _registerCustomAnnotation(self) -> int:
		"""Registers the annotation with a given GUID.

		A GUID uniquely identifies a custom annotation, but the UIA system relies on integer IDs.
		Any application (clients or providers) can register a custom annotation type, subsequent applications
		will get the same id for a given GUID.
		Registering custom annotations is only supported on Windows 11 and above.
		For any lesser version, id will be 0.

		"""
		if winVersion.getWinVer() >= winVersion.WIN11:
			import NVDAHelper

			return NVDAHelper.localLib.registerUIAAnnotationType(
				byref(self.guid),
			)
		return 0

	@property
	def id(self) -> int:
		"""Return an ID for a given annotation registering it first if necessary.

		Id's of all registered annotations are cached when requested for the first time
		to prevent unnecessary work by repeatedly interacting with UIA .
		"""
		try:
			annotationId = self._registeredAnnotations[self.guid]
		except KeyError:
			annotationId = self._registerCustomAnnotation()
			self._registeredAnnotations[self.guid] = annotationId
		return annotationId


class CustomAnnotationTypesCommon:
	"""UIA 'custom annotation types' common to all applications.
	Once registered, all subsequent registrations will return the same ID value.
	"""

	def __init__(self):
		# Registration of Custom annotation types used across multiple applications or frameworks should go here.
		self.microsoftWord_resolvedComment = CustomAnnotationTypeInfo(
			guid=GUID("{A015030C-5B44-4EAC-B0CC-21BA35DE6D07}"),
		)
		self.microsoftWord_draftComment = CustomAnnotationTypeInfo(
			guid=GUID("{26BAEBC6-591E-4116-BBCF-E9A7996CD169}"),
		)
		self.microsoftWord_bookmark = CustomAnnotationTypeInfo(
			guid=GUID("{25330951-A372-4DB9-A88A-85137AD008D2}"),
		)
