# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

from __future__ import annotations
import typing
from collections.abc import Generator
from comtypes import GUID
from .remoteFuncWrapper import (
	remoteFunc,
	remoteContextManager
)
from .remoteAPI import (
	RemoteAPI,
	RemoteUint,
	RemoteInt,
	RemoteIntEnum,
	RemoteString,
	RemoteArray,
	RemoteExtensionTarget,
	RemoteElement,
	RemoteTextRange,
	RemoteVariant
)
from .lowLevel import (
	TextUnit,
	AttributeId,
	StyleId
)


@remoteContextManager
def remote_unsignedRange(
	ra: RemoteAPI,
	start: RemoteUint | int,
	stop: RemoteUint | int,
	step: RemoteUint | int = 1
) -> typing.Generator[RemoteUint, None, None]:
	counter = ra.newUint(start)
	with ra.whileBlock(lambda: counter < stop):
		yield counter
		counter += step

@remoteContextManager
def remote_signedRange(
	ra: RemoteAPI,
	start: RemoteInt | int,
	stop: RemoteInt | int,
	step: RemoteInt | int = 1
) -> Generator[RemoteInt, None, None]:
	counter = ra.newInt(start)
	with ra.whileBlock(lambda: counter < stop):
		yield counter
		counter += step


@remoteContextManager
def remote_forEachItemInArray(ra: RemoteAPI, array: RemoteArray) -> Generator[RemoteVariant, None, None]:
	with remote_unsignedRange(ra, 0, array.size()) as index:
		yield array[index]


@remoteContextManager
def remote_forEachUnitInTextRange(
	ra: RemoteAPI,
	textRange: RemoteTextRange,
	unit: RemoteIntEnum[TextUnit] | TextUnit,
	reverse: bool =False
) -> Generator[RemoteTextRange, None, None]:
	logicalTextRange = textRange.getLogicalAdapter(reverse)
	logicalTempRange = logicalTextRange.clone()
	logicalTempRange.end = logicalTempRange.start
	with ra.whileBlock(lambda: logicalTempRange.end < logicalTextRange.end):
		unitsMoved = logicalTempRange.end.moveByUnit(unit, 1)
		endDelta = logicalTempRange.end.compareWith(logicalTextRange.end)
		with ra.ifBlock((unitsMoved == 0) | (endDelta > 0)):
			logicalTempRange.end = logicalTextRange.end
		yield logicalTempRange.textRange
		logicalTextRange.start = logicalTempRange.end
		with ra.ifBlock((unitsMoved == 0) | (endDelta >= 0)):
			ra.breakLoop()
		logicalTempRange.start = logicalTempRange.end


@remoteContextManager
def remote_forEachParagraphWithHeadingStyle(
	ra: RemoteAPI,
	textRange: RemoteTextRange,
	skipFirstUnit: bool =False,
	reverse: bool =False
) -> Generator[tuple[RemoteTextRange, RemoteInt], None, None]:
	if skipFirstUnit:
		logicalTextRange = textRange.getLogicalAdapter(reverse)
		logicalTextRange.start.moveByUnit(TextUnit.Paragraph, 1)
	with remote_forEachUnitInTextRange(ra, textRange, TextUnit.Paragraph, reverse=reverse) as paragraphRange:
		val = paragraphRange.getAttributeValue(AttributeId.StyleId)
		with ra.ifBlock(val.isInt()):
			intVal = val.asType(RemoteInt)
			with ra.ifBlock((intVal >= StyleId.Heading1) & (intVal <= StyleId.Heading9)):
				level = (intVal - StyleId.Heading1) + 1
				yield paragraphRange, level


@remoteFunc
def remote_collectAllHeadingsInTextRange(
	ra: RemoteAPI,
	textRange: RemoteTextRange
) -> tuple[RemoteArray, RemoteArray, RemoteArray]:
	levels = ra.newArray()
	labels = ra.newArray()
	ranges = ra.newArray()
	with remote_forEachParagraphWithHeadingStyle(ra, textRange) as (paragraphRange, level):
		levels.append(level)
		labels.append(paragraphRange.getText(-1))
		ranges.append(paragraphRange)
	return levels, labels, ranges


@remoteFunc
def remote_findFirstHeadingInTextRange(
	ra: RemoteAPI,
	textRange: RemoteTextRange,
	wantedLevel: RemoteInt | int = 0,
	reverse: bool =False
) -> tuple[RemoteInt, RemoteString, RemoteTextRange]:
	foundLevel = ra.newInt(0)
	foundLabel = ra.newString("")
	foundRange = ra.newNullTextRange()
	with remote_forEachParagraphWithHeadingStyle(
		ra, textRange, skipFirstUnit=True, reverse=reverse
	) as (paragraphRange, level):
		with ra.ifBlock((wantedLevel <= 0) | (level == wantedLevel)):
			label = paragraphRange.getText(-1)
			foundLevel.set(level)
			foundLabel.set(label)
			foundRange.set(paragraphRange)
			ra.breakLoop()
	return foundLevel, foundLabel, foundRange


@remoteFunc
def _remote_msWord_getCustomAttributeValue(
	ra: RemoteAPI,
	remote_docElement: RemoteElement,
	remote_textRange: RemoteTextRange,
	remote_customAttribID: RemoteInt | int
) -> RemoteVariant:
	guid_msWord_extendedTextRangePattern = GUID("{93514122-FF04-4B2C-A4AD-4AB04587C129}")
	guid_msWord_getCustomAttributeValue = GUID("{081ACA91-32F2-46F0-9FB9-017038BC45F8}")
	remote_customAttribValue = ra.newVariant()
	with ra.ifBlock(remote_docElement.isExtensionSupported(guid_msWord_extendedTextRangePattern)):
		ra.logRuntimeMessage("docElement supports extendedTextRangePattern")
		resultObj = ra.newVariant()
		ra.logRuntimeMessage("doing callExtension for extendedTextRangePattern")
		remote_docElement.callExtension(
			guid_msWord_extendedTextRangePattern,
			resultObj
		)
		with ra.ifBlock(resultObj.isNull()):
			ra.logRuntimeMessage("extendedTextRangePattern is null")
			ra.halt()
		with ra.elseBlock():
			ra.logRuntimeMessage("got extendedTextRangePattern ")
			remote_extendedTextRangePattern = resultObj.asType(RemoteExtensionTarget)
			with ra.ifBlock(
				remote_extendedTextRangePattern.isExtensionSupported(guid_msWord_getCustomAttributeValue)
			):
				ra.logRuntimeMessage("extendedTextRangePattern supports getCustomAttributeValue")
				ra.logRuntimeMessage("doing callExtension for getCustomAttributeValue")
				remote_extendedTextRangePattern.callExtension(
					guid_msWord_getCustomAttributeValue,
					remote_textRange,
					remote_customAttribID,
					remote_customAttribValue
				)
				ra.logRuntimeMessage("got customAttribValue of ", remote_customAttribValue.stringify())
			with ra.elseBlock():
				ra.logRuntimeMessage("extendedTextRangePattern does not support getCustomAttributeValue")
	with ra.elseBlock():
		ra.logRuntimeMessage("docElement does not support extendedTextRangePattern")
	ra.logRuntimeMessage("msWord_getCustomAttributeValue end")
	return remote_customAttribValue
