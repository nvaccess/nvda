# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Ryan McCleary
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Internal types for identifying MathML nodes."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from locationHelper import RectLTRB


MathMlNodePath = tuple[int, ...]
SyntheticMathMlNodeId = str


@dataclass(frozen=True)
class MathMlNodeInfo:
	path: MathMlNodePath
	tag: str


@dataclass(frozen=True)
class MathMlNodeRectInfo:
	path: MathMlNodePath
	tag: str
	rect: "RectLTRB"
