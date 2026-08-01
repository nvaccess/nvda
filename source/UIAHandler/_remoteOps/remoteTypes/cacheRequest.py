# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt


from __future__ import annotations
from typing import (
	Iterable,
)
from .. import lowLevel
from .. import instructions
from ..remoteFuncWrapper import (
	remoteMethod_mutable,
)
from . import (
	RemoteBaseObject,
	RemoteIntEnum,
)


class RemoteCacheRequest(RemoteBaseObject):
	"""
	Represents a remote UIA cache request.
	Properties and patterns can be added to it,
	after which it can populate the cache of a remote UI Automation element.
	"""

	_IsTypeInstruction = instructions.IsCacheRequest

	def _generateInitInstructions(self) -> Iterable[instructions.InstructionBase]:
		yield instructions.NewCacheRequest(result=self)

	@remoteMethod_mutable
	def addProperty(self, propertyId: RemoteIntEnum[lowLevel.PropertyId] | lowLevel.PropertyId):
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.CacheRequestAddProperty(
				target=self,
				propertyId=RemoteIntEnum.ensureRemote(self.rob, propertyId),
			),
		)

	@remoteMethod_mutable
	def addPattern(self, patternId: RemoteIntEnum[lowLevel.PatternId] | lowLevel.PatternId):
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.CacheRequestAddPattern(
				target=self,
				patternId=RemoteIntEnum.ensureRemote(self.rob, patternId),
			),
		)
