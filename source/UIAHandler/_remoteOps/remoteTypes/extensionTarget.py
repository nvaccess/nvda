# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited


from __future__ import annotations
from typing import (
	Iterable,
	Generic,
)
from ctypes import (
	c_ulong,
)
from comtypes import (
	GUID,
)
from .. import instructions
from ..remoteFuncWrapper import (
	remoteMethod,
	remoteMethod_mutable,
)
from . import (
	LocalTypeVar,
	RemoteBaseObject,
	RemoteVariant,
	RemoteBool,
	RemoteGuid,
)


class RemoteExtensionTarget(RemoteBaseObject[LocalTypeVar], Generic[LocalTypeVar]):
	"""
	Represents a remote object that supports UI Automation custom extensions.
	Including checking for the existence of extensions and
	calling extensions.
	"""

	def _generateInitInstructions(self) -> Iterable[instructions.InstructionBase]:
		yield instructions.NewNull(
			result=self,
		)

	@remoteMethod
	def isNull(self):
		variant = RemoteVariant(self.rob, self.operandId)
		return variant.isNull()

	@remoteMethod
	def isExtensionSupported(self, extensionId: RemoteGuid | GUID) -> RemoteBool:
		result = RemoteBool(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.IsExtensionSupported(
				result=result,
				target=self,
				extensionId=RemoteGuid.ensureRemote(self.rob, extensionId),
			),
		)
		return result

	@remoteMethod_mutable
	def callExtension(
		self,
		extensionId: RemoteGuid | GUID,
		*params: RemoteBaseObject | int | float | str,
	) -> None:
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.CallExtension(
				target=self,
				extensionId=RemoteGuid.ensureRemote(self.rob, extensionId),
				argCount=c_ulong(len(params)),
				arguments=[RemoteBaseObject.ensureRemote(self.rob, param) for param in params],
			),
		)
