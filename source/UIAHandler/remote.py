# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021-2022 NV Access Limited


from typing import (
	Optional,
	Any,
	Generator,
	cast
)
from comtypes import GUID
from comInterfaces import UIAutomationClient as UIA
from ._remoteOps import remoteAlgorithms
from ._remoteOps.remoteAPI import (
	RemoteExtensionTarget,
	RemoteInt
)
from ._remoteOps import operation
from ._remoteOps import remoteAPI
from ._remoteOps.lowLevel import (
	TextUnit,
	AttributeId,
	StyleId
)


_dll = None


def initialize(doRemote: bool, UIAClient: UIA.IUIAutomation):
	"""
	Initializes UI Automation remote operations.
	@param doRemote: true if code should be executed remotely, or false for locally.
	@param UIAClient: the current instance of the UI Automation client library running in NVDA.
	"""
	return True


def msWord_getCustomAttributeValue(
	docElement: UIA.IUIAutomationElement,
	textRange: UIA.IUIAutomationTextRange,
	customAttribID: int
) -> Optional[Any]:
	guid_msWord_extendedTextRangePattern = GUID("{93514122-FF04-4B2C-A4AD-4AB04587C129}")
	guid_msWord_getCustomAttributeValue = GUID("{081ACA91-32F2-46F0-9FB9-017038BC45F8}")
	op = operation.Operation()

	@op.buildFunction
	def code(ra: remoteAPI.RemoteAPI):
		remoteDocElement = ra.newElement(docElement)
		remoteTextRange = ra.newTextRange(textRange)
		remoteCustomAttribValue = ra.newVariant()
		with ra.ifBlock(remoteDocElement.isExtensionSupported(guid_msWord_extendedTextRangePattern)):
			ra.logRuntimeMessage("docElement supports extendedTextRangePattern")
			remoteResult = ra.newVariant()
			ra.logRuntimeMessage("doing callExtension for extendedTextRangePattern")
			remoteDocElement.callExtension(
				guid_msWord_extendedTextRangePattern,
				remoteResult
			)
			with ra.ifBlock(remoteResult.isNull()):
				ra.logRuntimeMessage("extendedTextRangePattern is null")
				ra.halt()
			with ra.elseBlock():
				ra.logRuntimeMessage("got extendedTextRangePattern ")
				remoteExtendedTextRangePattern = remoteResult.asType(RemoteExtensionTarget)
				with ra.ifBlock(
					remoteExtendedTextRangePattern.isExtensionSupported(guid_msWord_getCustomAttributeValue)
				):
					ra.logRuntimeMessage("extendedTextRangePattern supports getCustomAttributeValue")
					ra.logRuntimeMessage("doing callExtension for getCustomAttributeValue")
					remoteExtendedTextRangePattern.callExtension(
						guid_msWord_getCustomAttributeValue,
						remoteTextRange,
						customAttribID,
						remoteCustomAttribValue
					)
					ra.logRuntimeMessage("got customAttribValue of ", remoteCustomAttribValue.stringify())
					ra.Return(remoteCustomAttribValue)
				with ra.elseBlock():
					ra.logRuntimeMessage("extendedTextRangePattern does not support getCustomAttributeValue")
		with ra.elseBlock():
			ra.logRuntimeMessage("docElement does not support extendedTextRangePattern")
		ra.logRuntimeMessage("msWord_getCustomAttributeValue end")

	customAttribValue = op.execute()
	return customAttribValue

def collectAllHeadingsInTextRange(
	textRange: UIA.IUIAutomationTextRange
) -> Generator[tuple[int, str, UIA.IUIAutomationElement], None, None]:
	op = operation.Operation(enableLogging=True)

	@op.buildIterableFunction
	def code(ra: remoteAPI.RemoteAPI):
		remoteTextRange = ra.newTextRange(textRange, static=True)
		with remoteAlgorithms.remote_forEachUnitInTextRange(
			ra, remoteTextRange, TextUnit.Paragraph
		) as paragraphRange:
			val = paragraphRange.getAttributeValue(AttributeId.StyleId)
			with ra.ifBlock(val.isInt()):
				intVal = val.asType(RemoteInt)
				with ra.ifBlock((intVal >= StyleId.Heading1) & (intVal <= StyleId.Heading9)):
					level = (intVal - StyleId.Heading1) + 1
					label = paragraphRange.getText(-1)
					ra.Yield(level, label, paragraphRange)

	for level, label, paragraphRange in op.iterExecuteUntilSuccess():
		yield level, label, paragraphRange.QueryInterface(UIA.IUIAutomationTextRange)


def findFirstHeadingInTextRange(
	textRange: UIA.IUIAutomationTextRange,
	wantedLevel: int | None = None,
	reverse: bool = False
) -> tuple[int, str, UIA.IUIAutomationElement] | None:
	op = operation.Operation(enableLogging=True)

	@op.buildFunction
	def code(ra: remoteAPI.RemoteAPI):
		remoteTextRange = ra.newTextRange(textRange, static=True)
		remoteWantedLevel = ra.newInt(wantedLevel or 0)
		remoteTextRange.getLogicalAdapter(reverse).start.moveByUnit(TextUnit.Paragraph, 1)
		with remoteAlgorithms.remote_forEachUnitInTextRange(
			ra, remoteTextRange, TextUnit.Paragraph, reverse=reverse
		) as paragraphRange:
			val = paragraphRange.getAttributeValue(AttributeId.StyleId)
			with ra.ifBlock(val.isInt()):
				intVal = val.asType(RemoteInt)
				with ra.ifBlock((intVal >= StyleId.Heading1) & (intVal <= StyleId.Heading9)):
					level = (intVal - StyleId.Heading1) + 1
					with ra.ifBlock((remoteWantedLevel == 0) | (level == remoteWantedLevel)):
						ra.logRuntimeMessage("found heading at level ", level)
						label = paragraphRange.getText(-1)
						ra.Return(level, label, paragraphRange)

	try:
		level, label, paragraphRange = op.executeUntilSuccess()
	except operation.NoReturnException:
		return None
	return (
		cast(int, level),
		cast(str, label),
		cast(UIA.IUIAutomationTextRange, paragraphRange.QueryInterface(UIA.IUIAutomationTextRange))
	)
