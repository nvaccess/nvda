# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import typing

if typing.TYPE_CHECKING:
	import controlTypes
	from NVDAObjects import NVDAObject


class AnnotationTarget:
	@property
	def role(self) -> "controlTypes.Role":
		raise NotImplementedError

	@property
	def targetObject(self) -> "NVDAObject":
		raise NotImplementedError

	@property
	def summary(self) -> str:
		raise NotImplementedError


class AnnotationOrigin:
	""" Annotation relation information.
	Each origin may have many annotation targets.
	Targets can have different roles.
	This class encapsulates the relation.
	"""
	def __init__(self, originObj: "NVDAObject"):
		self._originObj: "NVDAObject" = originObj

	def __bool__(self):
		"""Performant implementation required to test for annotations
		"""
		raise NotImplementedError

	@property
	def targets(self) -> typing.Iterable[AnnotationTarget]:
		raise NotImplementedError

	@property
	def roles(self) -> typing.Iterable["controlTypes.Role"]:
		raise NotImplementedError

	@property
	def summaries(self) -> typing.Iterable["str"]:
		raise NotImplementedError
