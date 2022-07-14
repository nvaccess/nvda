# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	List,
)
from typing_extensions import (
	Protocol,
)

from comInterfaces.UIAutomationClient import IUIAutomationTextRange


class _IUIAutomationTextRangeT(Protocol):
	# Based on IUIAutomationTextRange
	# https://docs.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange

	def findText(self) -> "IUIAutomationTextRangeT":
		...

	def clone(self) -> "IUIAutomationTextRangeT":
		...

	def MoveEndpointByRange(
			self,
			source: int,
			rangeObject: "IUIAutomationTextRangeT",
			target: int
	) -> None:
		...

	def CompareEndpoints(
			self,
			source: int,
			rangeObject: "IUIAutomationTextRangeT",
			target: int
	) -> int:
		...

	def compare(self, other: "IUIAutomationTextRangeT") -> bool:
		...

	def getText(self, index: int) -> str:
		...

	def Select(self) -> None:
		...

	def MoveEndpointByUnit(self, endPoint: int, unit: int, direction: int) -> None:
		...

	def Move(self, unit: int, direction: int) -> None:
		...

	def ExpandToEnclosingUnit(self, unit: int) -> None:
		...

	def GetBoundingRectangles(self) -> List:
		...


class IUIAutomationTextRangeT(type(IUIAutomationTextRange), _IUIAutomationTextRangeT):
	pass
