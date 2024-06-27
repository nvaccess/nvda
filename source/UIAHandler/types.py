# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	List,
	Protocol,
)

from comInterfaces.UIAutomationClient import IUIAutomationTextRange


class _IUIAutomationTextRangeT(Protocol):
	# Based on IUIAutomationTextRange
	# https://docs.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange
	# Currently incomplete.

	def clone(self) -> "IUIAutomationTextRangeT":
		...

	def compare(self, other: "IUIAutomationTextRangeT") -> bool:
		...

	def CompareEndpoints(
			self,
			source: int,
			rangeObject: "IUIAutomationTextRangeT",
			target: int
	) -> int:
		...

	def ExpandToEnclosingUnit(self, unit: int) -> None:
		...

	def findText(self) -> "IUIAutomationTextRangeT":
		...

	def GetBoundingRectangles(self) -> List:
		...

	def getText(self, index: int) -> str:
		...

	def Move(self, unit: int, direction: int) -> None:
		...

	def MoveEndpointByRange(
			self,
			source: int,
			rangeObject: "IUIAutomationTextRangeT",
			target: int
	) -> None:
		...

	def MoveEndpointByUnit(self, endPoint: int, unit: int, direction: int) -> None:
		...

	def Select(self) -> None:
		...


class IUIAutomationTextRangeT(type(IUIAutomationTextRange), _IUIAutomationTextRangeT):
	pass
