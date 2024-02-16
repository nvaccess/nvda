# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021-2022 NV Access Limited


from typing import Optional, Any
from comtypes import GUID
from comInterfaces import UIAutomationClient as UIA
from ._remoteOps import remoteAlgorithms
from ._remoteOps.remoteAPI import (
	RemoteExtensionTarget,
	RemoteInt
)
from ._remoteOps.operation import Operation
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
	ro = Operation()
	remoteDocElement = ro.importElement(docElement)
	remoteTextRange = ro.importTextRange(textRange)
	with ro.buildContext() as ra:
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
				with ra.elseBlock():
					ra.logRuntimeMessage("extendedTextRangePattern does not support getCustomAttributeValue")
		with ra.elseBlock():
			ra.logRuntimeMessage("docElement does not support extendedTextRangePattern")
		ra.logRuntimeMessage("msWord_getCustomAttributeValue end")
	ro.addToResults(remoteCustomAttribValue)
	ro.execute()
	if remoteCustomAttribValue.isLocalValueAvailable:
		return remoteCustomAttribValue.localValue


def collectAllHeadingsInTextRange(
	textRange: UIA.IUIAutomationTextRange
) -> list[tuple[int, str, UIA.IUIAutomationElement]]:
	headings = []
	ro = Operation(enableLogging=True)
	remoteTextRange = ro.importTextRange(textRange)
	with ro.buildContext() as ra:
		levels = ra.newArray()
		labels = ra.newArray()
		ranges = ra.newArray()
		with remoteAlgorithms.remote_forEachUnitInTextRange(
			ra, remoteTextRange, TextUnit.Paragraph
		) as paragraphRange:
			val = paragraphRange.getAttributeValue(AttributeId.StyleId)
			with ra.ifBlock(val.isInt()):
				intVal = val.asType(RemoteInt)
				with ra.ifBlock((intVal >= StyleId.Heading1) & (intVal <= StyleId.Heading9)):
					level = (intVal - StyleId.Heading1) + 1
					label = paragraphRange.getText(-1)
					levels.append(level)
					labels.append(label)
					ranges.append(paragraphRange)
	ro.addToResults(levels, labels, ranges)
	for done in ro.executeUntilSuccess():
		localLevels = levels.localValue
		localLabels = labels.localValue
		localRanges = [r.QueryInterface(UIA.IUIAutomationTextRange) for r in ranges.localValue]
		headings.extend(zip(localLevels, localLabels, localRanges))
	return headings


def findFirstHeadingInTextRange(
	textRange: UIA.IUIAutomationTextRange,
	wantedLevel: int | None = None,
	reverse: bool = False
) -> tuple[int, str, UIA.IUIAutomationElement] | None:
	ro = Operation(enableLogging=True)
	with ro.buildContext() as ra:
		remoteTextRange = ra.newTextRange(textRange, static=True)
		remoteWantedLevel = ra.newInt(wantedLevel or 0)
		foundLevel = ra.newInt(0)
		foundLabel = ra.newString("")
		foundParagraphRange = ra.newTextRange()
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
						foundLevel.set(level)
						foundLabel.set(paragraphRange.getText(-1))
						foundParagraphRange.set(paragraphRange)
						ra.breakLoop()
	ro.addToResults(foundLevel, foundLabel, foundParagraphRange)
	for done in ro.executeUntilSuccess():
		if done:
			localFoundParagraphRange = foundParagraphRange.localValue
			if not localFoundParagraphRange:
				return None
			localFoundLevel = foundLevel.localValue
			localFoundLabel = foundLabel.localValue
			return (
				localFoundLevel,
				localFoundLabel,
				localFoundParagraphRange
			)
