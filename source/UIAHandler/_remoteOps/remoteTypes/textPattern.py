# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited


from __future__ import annotations
from typing import (
	cast,
)
from ctypes import (
	POINTER,
)
from UIAHandler import UIA
from .. import instructions
from ..remoteFuncWrapper import (
	remoteMethod,
)
from . import (
	RemoteExtensionTarget,
)


class RemoteTextPattern(RemoteExtensionTarget[POINTER(UIA.IUIAutomationTextPattern)]):
	"""
	Represents a remote UI Automation text pattern.
	"""

	LocalType = POINTER(UIA.IUIAutomationTextPattern)

	def _initOperand(self, initialValue: None = None, const: bool = False):
		if initialValue is not None:
			raise TypeError("Cannot initialize RemoteTextRange with an initial value.")
		return super()._initOperand()

	@property
	def localValue(self) -> UIA.IUIAutomationTextPattern:
		value = super().localValue
		if value is None:
			return POINTER(UIA.IUIAutomationTextPattern)()
		return cast(UIA.IUIAutomationTextPattern, value.QueryInterface(UIA.IUIAutomationTextPattern))

	@remoteMethod
	def rangeFromChild(self, child: RemoteElement) -> RemoteTextRange:
		result = RemoteTextRange(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextPatternRangeFromChild(
				result=result,
				target=self,
				child=child,
			),
		)
		return result

from .element import RemoteElement
from .textRange import RemoteTextRange
