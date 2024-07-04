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
from .. import lowLevel
from .. import instructions
from .. import builder
from ..remoteFuncWrapper import (
	remoteMethod,
	remoteMethod_mutable,
)
from . import (
	RemoteVariant,
	RemoteBool,
	RemoteInt,
	RemoteIntEnum,
	RemoteString,
	RemoteExtensionTarget,
	RemoteElement,
)


class RemoteTextRange(RemoteExtensionTarget[POINTER(UIA.IUIAutomationTextRange)]):
	"""
	Represents a remote UI Automation text range.
	"""

	LocalType = POINTER(UIA.IUIAutomationTextRange)

	def _initOperand(self, initialValue: None = None, const: bool = False):
		if initialValue is not None:
			raise TypeError("Cannot initialize RemoteTextRange with an initial value.")
		return super()._initOperand()

	@property
	def localValue(self) -> UIA.IUIAutomationTextRange:
		value = super().localValue
		if value is None:
			return POINTER(UIA.IUIAutomationTextRange)()
		return cast(UIA.IUIAutomationTextRange, value.QueryInterface(UIA.IUIAutomationTextRange))

	@remoteMethod
	def clone(self) -> RemoteTextRange:
		result = RemoteTextRange(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeClone(
				result=result,
				target=self,
			),
		)
		return result

	@remoteMethod
	def getEnclosingElement(self) -> RemoteElement:
		result = RemoteElement(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeGetEnclosingElement(
				result=result,
				target=self,
			),
		)
		return result

	@remoteMethod
	def getText(self, maxLength: RemoteInt | int) -> RemoteString:
		result = RemoteString(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeGetText(
				result=result,
				target=self,
				maxLength=RemoteInt.ensureRemote(self.rob, maxLength),
			),
		)
		return result

	@remoteMethod_mutable
	def expandToEnclosingUnit(self, unit: RemoteIntEnum[lowLevel.TextUnit] | lowLevel.TextUnit):
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeExpandToEnclosingUnit(
				target=self,
				unit=RemoteIntEnum.ensureRemote(self.rob, unit),
			),
		)

	@remoteMethod_mutable
	def moveEndpointByUnit(
		self,
		endpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint,
		unit: RemoteIntEnum[lowLevel.TextUnit] | lowLevel.TextUnit,
		count: RemoteInt | int,
	) -> RemoteInt:
		result = RemoteInt(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeMoveEndpointByUnit(
				result=result,
				target=self,
				endpoint=RemoteIntEnum.ensureRemote(self.rob, endpoint),
				unit=RemoteIntEnum.ensureRemote(self.rob, unit),
				count=RemoteInt.ensureRemote(self.rob, count),
			),
		)
		return result

	@remoteMethod_mutable
	def moveEndpointByRange(
		self,
		srcEndpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint,
		otherRange: RemoteTextRange,
		otherEndpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint,
	):
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeMoveEndpointByRange(
				target=self,
				srcEndpoint=RemoteIntEnum.ensureRemote(self.rob, srcEndpoint),
				otherRange=otherRange,
				otherEndpoint=RemoteIntEnum.ensureRemote(self.rob, otherEndpoint),
			),
		)

	@remoteMethod
	def getAttributeValue(
		self,
		attributeId: RemoteIntEnum[lowLevel.AttributeId] | lowLevel.AttributeId,
	) -> RemoteVariant:
		result = RemoteVariant(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeGetAttributeValue(
				result=result,
				target=self,
				attributeId=RemoteIntEnum.ensureRemote(self.rob, attributeId),
			),
		)
		return result

	@remoteMethod
	def compareEndpoints(
		self,
		thisEndpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint,
		otherRange: RemoteTextRange,
		otherEndpoint: RemoteIntEnum[lowLevel.TextPatternRangeEndpoint] | lowLevel.TextPatternRangeEndpoint,
	) -> RemoteInt:
		result = RemoteInt(self.rob, self.rob.requestNewOperandId())
		self.rob.getDefaultInstructionList().addInstruction(
			instructions.TextRangeCompareEndpoints(
				result=result,
				target=self,
				thisEndpoint=RemoteIntEnum.ensureRemote(self.rob, thisEndpoint),
				otherRange=otherRange,
				otherEndpoint=RemoteIntEnum.ensureRemote(self.rob, otherEndpoint),
			),
		)
		return result

	def getLogicalAdapter(self, reverse: bool = False) -> RemoteTextRangeLogicalAdapter:
		obj = RemoteTextRangeLogicalAdapter(self.rob, self, reverse=reverse)
		return obj


class _RemoteTextRangeEndpoint(builder._RemoteBase):
	def __init__(
		self,
		rob: builder.RemoteOperationBuilder,
		textRangeLA: RemoteTextRangeLogicalAdapter,
		isStart: bool,
	):
		super().__init__(rob)
		self._la = textRangeLA
		self._endpoint = (
			lowLevel.TextPatternRangeEndpoint.Start
			if isStart ^ self.isReversed
			else lowLevel.TextPatternRangeEndpoint.End
		)

	@property
	def textRange(self: _RemoteTextRangeEndpoint) -> RemoteTextRange:
		return self._la.textRange

	@property
	def isReversed(self: _RemoteTextRangeEndpoint) -> bool:
		return self._la.isReversed

	@property
	def endpoint(self: _RemoteTextRangeEndpoint) -> lowLevel.TextPatternRangeEndpoint:
		return self._endpoint

	def compareWith(self, other: _RemoteTextRangeEndpoint) -> RemoteInt:
		res = self.textRange.compareEndpoints(self.endpoint, other.textRange, other.endpoint)
		if self.isReversed:
			res *= -1
		return res

	def moveTo(self, other: _RemoteTextRangeEndpoint):
		self.textRange.moveEndpointByRange(self.endpoint, other.textRange, other.endpoint)

	def moveByUnit(
		self,
		unit: RemoteIntEnum[lowLevel.TextUnit] | lowLevel.TextUnit,
		count: RemoteInt | int,
	) -> RemoteInt:
		realCount = (count * -1) if self.isReversed else count
		res = self.textRange.moveEndpointByUnit(self.endpoint, unit, realCount)
		return res

	def __lt__(self, other: _RemoteTextRangeEndpoint) -> RemoteBool:
		return self.compareWith(other).__lt__(0)

	def __le__(self, other: _RemoteTextRangeEndpoint) -> RemoteBool:
		return self.compareWith(other).__le__(0)

	def __gt__(self, other: _RemoteTextRangeEndpoint) -> RemoteBool:
		return self.compareWith(other).__gt__(0)

	def __ge__(self, other: _RemoteTextRangeEndpoint) -> RemoteBool:
		return self.compareWith(other).__ge__(0)

	def __eq__(self, other: _RemoteTextRangeEndpoint) -> RemoteBool:
		return self.compareWith(other) == 0

	def __ne__(self, other: _RemoteTextRangeEndpoint) -> RemoteBool:
		return (self == other).inverse()


class RemoteTextRangeLogicalAdapter(builder._RemoteBase):
	def __init__(
		self,
		rob: builder.RemoteOperationBuilder,
		textRange: RemoteTextRange,
		reverse: bool = False,
	):
		super().__init__(rob)
		self._textRange = textRange
		self._isReversed = reverse

	@property
	def textRange(self) -> RemoteTextRange:
		return self._textRange

	@property
	def isReversed(self) -> bool:
		return self._isReversed

	@property
	def start(self) -> _RemoteTextRangeEndpoint:
		obj = _RemoteTextRangeEndpoint(self.rob, self, isStart=True)
		return obj

	@start.setter
	def start(self, value: _RemoteTextRangeEndpoint):
		self.start.moveTo(value)

	@property
	def end(self) -> _RemoteTextRangeEndpoint:
		obj = _RemoteTextRangeEndpoint(self.rob, self, isStart=False)
		return obj

	@end.setter
	def end(self, value: _RemoteTextRangeEndpoint):
		self.end.moveTo(value)

	def clone(self):
		return self.textRange.clone().getLogicalAdapter(self.isReversed)
