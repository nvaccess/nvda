# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

from __future__ import annotations
from typing import ContextManager, Any
from collections.abc import Generator
from comtypes import GUID
from .midLevel import (
	remoteFunc,
	remoteContextManager,
	RemoteUint,
	RemoteInt,
	RemoteArray,
	RemoteExtensionTarget,
	RemoteElement,
	RemoteTextRange,
	RemoteVariant
)
from .highLevel import RemoteFuncAPI
from .lowLevel import (
	TextUnit,
	AttributeId,
	StyleId
)


@remoteContextManager
def remote_unsignedRange(rfa: RemoteFuncAPI, start: RemoteUint, stop: RemoteUint, step: RemoteUint ):
	counter =start.copy()
	with rfa.whileBlock(lambda: counter < stop):
		yield counter
		counter += step

@remoteContextManager
def remote_signedRange(rfa: RemoteFuncAPI, start: RemoteInt, stop: RemoteInt, step: RemoteInt) -> Generator[RemoteInt, None, None]:
	counter = rfa.newInt(start)
	with rfa.whileBlock(lambda: counter < stop):
		yield counter
		counter += step

@remoteContextManager
def remote_forEachItemInArray(rfa: RemoteFuncAPI, array: RemoteArray) -> Generator[RemoteVariant, None, None]:
	with remote_unsignedRange(rfa, RemoteUint(0, const=True), array.size(), RemoteUint(1, const=True)) as index:
		yield array[index]

@remoteContextManager
def remote_forEachUnitInTextRange(rfa: RemoteFuncAPI, textRange: RemoteTextRange, unit: RemoteInt, reverse=False ) -> Generator[RemoteTextRange, None, None]:
	logicalTextRange = textRange.getLogicalAdapter(reverse)
	logicalTempRange = logicalTextRange.clone()
	logicalTempRange.end = logicalTempRange.start
	with rfa.whileBlock(lambda: logicalTempRange.end < logicalTextRange.end):
		unitsMoved = logicalTempRange.end.moveByUnit(unit, 1)
		endDelta = logicalTempRange.end.compareWith(logicalTextRange.end)
		with rfa.ifBlock((unitsMoved == 0) | (endDelta > 0)):
			logicalTempRange.end = logicalTextRange.end
		yield logicalTempRange.textRange
		logicalTextRange.start = logicalTempRange.end
		with rfa.ifBlock((unitsMoved == 0) | (endDelta >= 0)):
			rfa.breakLoop()
		logicalTempRange.start = logicalTempRange.end

@remoteContextManager
def remote_forEachParagraphWithHeadingStyle(rfa: RemoteFuncAPI, textRange: RemoteTextRange, reverse=False) -> Generator[tuple[RemoteTextRange, RemoteInt], None, None]:
	with remote_forEachUnitInTextRange(rfa, textRange, TextUnit.Paragraph, reverse=reverse) as paragraphRange:
		val = paragraphRange.getAttributeValue(AttributeId.StyleId)
		with rfa.ifBlock(val.isType(RemoteInt)):
			intVal = val.asType(RemoteInt)
			with rfa.ifBlock((intVal >= StyleId.Heading1) & (intVal <= StyleId.Heading9)):
				level = (intVal - StyleId.Heading1) + 1 
				yield paragraphRange, level

@remoteFunc
def remote_collectAllHeadingsInTextRange(rfa: RemoteFuncAPI, textRange: RemoteTextRange) -> tuple[RemoteArray, RemoteArray, RemoteArray]:
	levels = rfa.newArray()
	labels = rfa.newArray()
	ranges = rfa.newArray()
	with remote_forEachParagraphWithHeadingStyle(rfa, textRange, False) as (paragraphRange, level):
		levels.append(level)
		labels.append(paragraphRange.getText(-1))
		ranges.append(paragraphRange)
	return levels, labels, ranges

@remoteFunc
def _remote_msWord_getCustomAttributeValue(
	rfa: RemoteFuncAPI,
	remote_docElement: RemoteElement,
	remote_textRange: RemoteTextRange,
	remote_customAttribID: RemoteInt
):
	guid_msWord_extendedTextRangePattern = GUID("{93514122-FF04-4B2C-A4AD-4AB04587C129}")
	guid_msWord_getCustomAttributeValue = GUID("{081ACA91-32F2-46F0-9FB9-017038BC45F8}")
	remote_customAttribValue = RemoteVariant()
	with rfa.ifBlock(remote_docElement.isExtensionSupported(guid_msWord_extendedTextRangePattern)):
		rfa.logRuntimeMessage("docElement supports extendedTextRangePattern")
		resultObj = RemoteVariant()
		rfa.logRuntimeMessage("doing callExtension for extendedTextRangePattern")
		remote_docElement.callExtension(
			guid_msWord_extendedTextRangePattern,
			resultObj
		)
		with rfa.ifBlock(resultObj.isNull()):
			rfa.logRuntimeMessage("extendedTextRangePattern is null")
			rfa.halt()
		with rfa.elseBlock():
			rfa.logRuntimeMessage("got extendedTextRangePattern ")
			remote_extendedTextRangePattern = resultObj.asType(RemoteExtensionTarget)
			with rfa.ifBlock(
				remote_extendedTextRangePattern.isExtensionSupported(guid_msWord_getCustomAttributeValue)
			):
				rfa.logRuntimeMessage("extendedTextRangePattern supports getCustomAttributeValue")
				rfa.logRuntimeMessage("doing callExtension for getCustomAttributeValue")
				remote_extendedTextRangePattern.callExtension(
					guid_msWord_getCustomAttributeValue,
					remote_textRange,
					remote_customAttribID,
					remote_customAttribValue
				)
				rfa.logRuntimeMessage("got customAttribValue of ", remote_customAttribValue.stringify())
			with rfa.elseBlock():
				rfa.logRuntimeMessage("extendedTextRangePattern does not support getCustomAttributeValue")
	with rfa.elseBlock():
		rfa.logRuntimeMessage("docElement does not support extendedTextRangePattern")
	rfa.logRuntimeMessage("msWord_getCustomAttributeValue end")
	return remote_customAttribValue
