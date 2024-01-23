# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021-2022 NV Access Limited


from typing import Optional, Any
from logHandler import log
from comInterfaces import UIAutomationClient as UIA
from ._remoteOps import highLevel
from ._remoteOps import remoteAlgorithms




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
	customAttribValue = highLevel.execute(
		remoteAlgorithms._remote_msWord_getCustomAttributeValue,
		docElement, textRange, customAttribID,
		remoteLogging=False,
		dumpInstructions=False
	)
	return customAttribValue

def collectAllHeadingsInTextRange(
	textRange: UIA.IUIAutomationTextRange
) -> list[tuple[int, str, UIA.IUIAutomationElement]]:
	headings = []
	count = 0
	while count < 20:
		count += 1
		levels: list[int] = []
		labels: list[str] = []
		ranges: list[UIA.IUIAutomationTextRange] = []
		try:
			levels, labels, ranges = highLevel.execute(
				remoteAlgorithms.remote_collectAllHeadingsInTextRange,
				textRange,
				remoteLogging=False,
				dumpInstructions=True
			)
		except highLevel.InstructionLimitExceededException as e:
			log.warning(f"{e}\n{count=}")
			levels, labels, ranges = e.results
		else:
			count = 20
		textRanges = []
		for index, punk in enumerate(ranges):
			subrange = punk.QueryInterface(UIA.IUIAutomationTextRange)
			textRanges.append(subrange)
		for heading in zip(levels, labels, textRanges):
			headings.append(heading)
	return headings

def findFirstHeadingInTextRange(
	textRange: UIA.IUIAutomationTextRange, wantedLevel: int | None = None, reverse: bool = False
) -> tuple[int, str, UIA.IUIAutomationElement] | None:
	count = 0
	while count < 20:
		count += 1
		try:
			level, label, subrange = highLevel.execute(
				remoteAlgorithms.remote_findFirstHeadingInTextRange,
				textRange,
				wantedLevel or 0,
				reverse,
				remoteLogging=False,
				dumpInstructions=True
			)
		except highLevel.InstructionLimitExceededException as e:
			log.warning(f"{e}\n{count=}")
			continue
		except Exception:
			log.error("Could not execute remote function", exc_info=True)
			raise
		else:
			if level == 0:
				return None
			subrange = subrange.QueryInterface(UIA.IUIAutomationTextRange)
			return level, label, subrange
