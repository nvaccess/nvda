# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021-2022 NV Access Limited


from typing import Optional, Any
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

def collectHeadingsInTextRange(
	textRange: UIA.IUIAutomationTextRange
) -> list[tuple[int, str, UIA.IUIAutomationElement]]:
	headings = []
	count = 10
	while count > 0:
		count -= 1
		levels: list[int]
		labels: list[str]
		ranges: list[UIA.IUIAutomationTextRange]
		try:
			levels, labels, ranges = highLevel.execute(
				remoteAlgorithms.remote_collectAllHeadingsInTextRange,
				textRange,
				remoteLogging=False,
				dumpInstructions=True
			)
		except highLevel.InstructionLimitExceededException as e:
			levels, labels, ranges = e.results
		else:
			count = 0
		for heading in zip(levels, labels, ranges):
			headings.append(heading)
	return headings
