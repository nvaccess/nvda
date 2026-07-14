# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021-2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt


from typing import (
	Any,
	Generator,
	cast,
)
from comtypes import GUID
from comInterfaces import UIAutomationClient as UIA
import winVersion
from logHandler import log
from ._remoteOps import remoteAlgorithms
from ._remoteOps.remoteTypes import (
	RemoteElement,
	RemoteExtensionTarget,
	RemoteInt,
)
from ._remoteOps import operation
from ._remoteOps import remoteAPI
from ._remoteOps.lowLevel import (
	TextUnit,
	TextPatternRangeEndpoint,
	AttributeId,
	StyleId,
)


_isSupported: bool = False


def isSupported() -> bool:
	"""
	Returns whether UIA remote operations are supported on this version of Windows.
	"""
	return _isSupported


def initialize(doRemote: bool, UIAClient: UIA.IUIAutomation):
	"""
	Initializes UI Automation remote operations.
	The following parameters are deprecated and ignored:
	@param doRemote: true if code should be executed remotely, or false for locally.
	@param UIAClient: the current instance of the UI Automation client library running in NVDA.
	"""
	global _isSupported
	_isSupported = winVersion.getWinVer() >= winVersion.WIN11
	return True


def terminate():
	"""Terminates UIA remote operations support."""
	global _isSupported
	_isSupported = False


def _msWord_remote_getExtendedTextRangePattern(
	ra: remoteAPI.RemoteAPI,
	remoteDocElement: RemoteElement,
) -> RemoteExtensionTarget:
	guid_msWord_extendedTextRangePattern = GUID("{93514122-FF04-4B2C-A4AD-4AB04587C129}")
	remoteResult = ra.newVariant()
	extendedTextRangeIsSupported = remoteDocElement.isExtensionSupported(
		guid_msWord_extendedTextRangePattern,
	)
	with ra.ifBlock(extendedTextRangeIsSupported.inverse()):
		ra.logRuntimeMessage("docElement does not support extendedTextRangePattern")
		ra.Return(None)
	ra.logRuntimeMessage("docElement supports extendedTextRangePattern")
	ra.logRuntimeMessage("doing callExtension for extendedTextRangePattern")
	remoteDocElement.callExtension(
		guid_msWord_extendedTextRangePattern,
		remoteResult,
	)
	with ra.ifBlock(remoteResult.isNull()):
		ra.logRuntimeMessage("extendedTextRangePattern is null")
		ra.Return(None)
	ra.logRuntimeMessage("got extendedTextRangePattern")
	return remoteResult.asType(RemoteExtensionTarget)


def msWord_getCustomAttributeValue(
	docElement: UIA.IUIAutomationElement,
	textRange: UIA.IUIAutomationTextRange,
	customAttribID: int,
) -> Any | None:
	guid_msWord_getCustomAttributeValue = GUID("{081ACA91-32F2-46F0-9FB9-017038BC45F8}")
	op = operation.Operation()

	@op.buildFunction
	def code(ra: remoteAPI.RemoteAPI):
		remoteDocElement = ra.newElement(docElement)
		remoteTextRange = ra.newTextRange(textRange)
		remoteCustomAttribValue = ra.newVariant()
		remoteExtendedTextRangePattern = _msWord_remote_getExtendedTextRangePattern(
			ra,
			remoteDocElement,
		)
		customAttributeValueIsSupported = remoteExtendedTextRangePattern.isExtensionSupported(
			guid_msWord_getCustomAttributeValue,
		)
		with ra.ifBlock(customAttributeValueIsSupported.inverse()):
			ra.logRuntimeMessage("extendedTextRangePattern does not support getCustomAttributeValue")
			ra.Return(None)
		ra.logRuntimeMessage("extendedTextRangePattern supports getCustomAttributeValue")
		ra.logRuntimeMessage("doing callExtension for getCustomAttributeValue")
		remoteExtendedTextRangePattern.callExtension(
			guid_msWord_getCustomAttributeValue,
			remoteTextRange,
			customAttribID,
			remoteCustomAttribValue,
		)
		ra.logRuntimeMessage("got customAttribValue of ", remoteCustomAttribValue)
		ra.Return(remoteCustomAttribValue)

	customAttribValue = op.execute()
	if customAttribValue is None:
		log.debugWarning("Custom attribute value not available")
		return None
	return customAttribValue


def msWord_textRange_moveBySentence(
	docElement: UIA.IUIAutomationElement,
	textRange: UIA.IUIAutomationTextRange,
	unitCount: int,
) -> tuple[UIA.IUIAutomationTextRange, int] | None:
	"""
	Move a UI Automation text range by unitCount sentences using the Word-specific UIA
	extended text range pattern, if available.
	A degenerate range stays degenerate on success, matching the ITextRangeProvider::Move contract.
	On par with ITextRangeProvider::Move, hitting a document boundary is not a failure: the range
	is moved as far as possible and the actual number of sentences moved is returned, which may be
	less than requested, or 0.
	Returns None only if the operation fails or the extension is not supported.
	"""
	if not isSupported():
		return None

	guid_msWord_moveBySentence = GUID("{F39655AC-133A-435B-A318-C197F0D3D203}")
	op = operation.Operation()

	@op.buildFunction
	def code(ra: remoteAPI.RemoteAPI):
		remoteDocElement = ra.newElement(docElement)
		remoteTextRange = ra.newTextRange(textRange)

		remoteExtendedTextRangePattern = _msWord_remote_getExtendedTextRangePattern(
			ra,
			remoteDocElement,
		)

		moveBySentenceSupported = remoteExtendedTextRangePattern.isExtensionSupported(
			guid_msWord_moveBySentence,
		)
		with ra.ifBlock(moveBySentenceSupported.inverse()):
			ra.logRuntimeMessage("extendedTextRangePattern does not support MoveBySentence")
			ra.Return(None)

		moveCount = ra.newInt(unitCount)
		actualMoved = ra.newInt(0)
		ra.logRuntimeMessage("doing callExtension for MoveBySentence")
		remoteExtendedTextRangePattern.callExtension(
			guid_msWord_moveBySentence,
			remoteTextRange,
			moveCount,
			actualMoved,
		)
		ra.Return(remoteTextRange, actualMoved)

	return op.execute()


def msWord_textRange_moveEndpointBySentence(
	docElement: UIA.IUIAutomationElement,
	textRange: UIA.IUIAutomationTextRange,
	endpoint: int,
	unitCount: int,
) -> tuple[UIA.IUIAutomationTextRange, int] | None:
	"""
	Move one endpoint of a UI Automation text range by unitCount sentences using the
	Word-specific UIA extended text range pattern, if available.
	:param endpoint: a TextPatternRangeEndpoint value indicating which endpoint to move.
	On par with ITextRangeProvider::MoveEndpointByUnit, hitting a document boundary is not a
	failure: the endpoint is moved as far as possible and the actual number of sentences moved
	is returned, which may be less than requested, or 0.
	Returns None only if the operation fails or the extension is not supported.
	"""
	if not isSupported():
		return None

	guid_msWord_moveEndpointBySentence = GUID("{368E89A2-1BC2-4402-8C58-33C63ECFFA3B}")
	remoteEndpointConst = TextPatternRangeEndpoint(endpoint)
	op = operation.Operation()

	@op.buildFunction
	def code(ra: remoteAPI.RemoteAPI):
		remoteDocElement = ra.newElement(docElement)
		remoteTextRange = ra.newTextRange(textRange)

		remoteExtendedTextRangePattern = _msWord_remote_getExtendedTextRangePattern(
			ra,
			remoteDocElement,
		)

		moveEndpointBySentenceSupported = remoteExtendedTextRangePattern.isExtensionSupported(
			guid_msWord_moveEndpointBySentence,
		)
		with ra.ifBlock(moveEndpointBySentenceSupported.inverse()):
			ra.logRuntimeMessage(
				"extendedTextRangePattern does not support MoveEndpointBySentence",
			)
			ra.Return(None)

		remoteEndpoint = ra.newInt(remoteEndpointConst)
		moveCount = ra.newInt(unitCount)
		actualMoved = ra.newInt(0)
		ra.logRuntimeMessage("doing callExtension for MoveEndpointBySentence")
		remoteExtendedTextRangePattern.callExtension(
			guid_msWord_moveEndpointBySentence,
			remoteTextRange,
			remoteEndpoint,
			moveCount,
			actualMoved,
		)
		ra.Return(remoteTextRange, actualMoved)

	return op.execute()


def msWord_textRange_expandToEnclosingSentence(
	docElement: UIA.IUIAutomationElement,
	textRange: UIA.IUIAutomationTextRange,
) -> UIA.IUIAutomationTextRange | None:
	"""
	Expand a UI Automation text range to its enclosing sentence using the Word-specific UIA
	extended text range pattern, if available.
	If the range is collapsed at the very end of the document, it is returned unchanged:
	Word's ExpandToEnclosingSentence extension otherwise wraps around and expands the first
	sentence in the document instead of leaving the range where it is.
	Returns None if the operation fails or the extension is not supported.
	"""
	if not isSupported():
		return None

	guid_msWord_expandToEnclosingSentence = GUID("{98FE8B34-F317-459A-9627-21123EA95BEA}")
	op = operation.Operation()

	@op.buildFunction
	def code(ra: remoteAPI.RemoteAPI):
		remoteDocElement = ra.newElement(docElement)
		remoteTextRange = ra.newTextRange(textRange)

		isCollapsed = (
			remoteTextRange.compareEndpoints(
				TextPatternRangeEndpoint.End,
				remoteTextRange,
				TextPatternRangeEndpoint.Start,
			)
			== 0
		)
		with ra.ifBlock(isCollapsed):
			endTestRange = remoteTextRange.clone()
			charsAvailable = endTestRange.moveEndpointByUnit(
				TextPatternRangeEndpoint.End,
				TextUnit.Character,
				1,
			)
			with ra.ifBlock(charsAvailable == 0):
				ra.logRuntimeMessage(
					"Collapsed range is at the end of the document; "
					"not expanding to sentence to avoid wraparound",
				)
				ra.Return(remoteTextRange)

		remoteExtendedTextRangePattern = _msWord_remote_getExtendedTextRangePattern(
			ra,
			remoteDocElement,
		)

		expandSupported = remoteExtendedTextRangePattern.isExtensionSupported(
			guid_msWord_expandToEnclosingSentence,
		)
		with ra.ifBlock(expandSupported.inverse()):
			ra.logRuntimeMessage(
				"extendedTextRangePattern does not support ExpandToEnclosingSentence",
			)
			ra.Return(None)

		ra.logRuntimeMessage("doing callExtension for ExpandToEnclosingSentence")
		remoteExtendedTextRangePattern.callExtension(
			guid_msWord_expandToEnclosingSentence,
			remoteTextRange,
		)
		ra.Return(remoteTextRange)

	return op.execute()


def collectAllHeadingsInTextRange(
	textRange: UIA.IUIAutomationTextRange,
) -> Generator[tuple[int, str, UIA.IUIAutomationElement], None, None]:
	op = operation.Operation()

	@op.buildIterableFunction
	def code(ra: remoteAPI.RemoteAPI):
		remoteTextRange = ra.newTextRange(textRange, static=True)
		with remoteAlgorithms.remote_forEachUnitInTextRange(
			ra,
			remoteTextRange,
			TextUnit.Paragraph,
		) as paragraphRange:
			val = paragraphRange.getAttributeValue(AttributeId.StyleId)
			with ra.ifBlock(val.isInt()):
				intVal = val.asType(RemoteInt)
				with ra.ifBlock((intVal >= StyleId.Heading1) & (intVal <= StyleId.Heading9)):
					level = (intVal - StyleId.Heading1) + 1
					label = paragraphRange.getText(-1)
					ra.Yield(level, label, paragraphRange)

	for level, label, paragraphRange in op.iterExecute(maxTries=20):
		yield level, label, paragraphRange


def findFirstHeadingInTextRange(
	textRange: UIA.IUIAutomationTextRange,
	wantedLevel: int | None = None,
	reverse: bool = False,
) -> tuple[int, str, UIA.IUIAutomationElement] | None:
	op = operation.Operation()

	@op.buildFunction
	def code(ra: remoteAPI.RemoteAPI):
		remoteTextRange = ra.newTextRange(textRange, static=True)
		remoteWantedLevel = ra.newInt(wantedLevel or 0)
		executionCount = ra.newInt(0, static=True)
		executionCount += 1
		ra.logRuntimeMessage("executionCount is ", executionCount)
		with ra.ifBlock(executionCount == 1):
			ra.logRuntimeMessage("Doing initial move")
			remoteTextRange.getLogicalAdapter(reverse).start.moveByUnit(TextUnit.Paragraph, 1)
		with remoteAlgorithms.remote_forEachUnitInTextRange(
			ra,
			remoteTextRange,
			TextUnit.Paragraph,
			reverse=reverse,
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
		level, label, paragraphRange = op.execute(maxTries=20)
	except operation.NoReturnException:
		return None
	return (
		cast(int, level),
		cast(str, label),
		cast(UIA.IUIAutomationTextRange, paragraphRange),
	)
