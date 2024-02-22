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
def remote_forEachUnitInTextRange(
	ra: RemoteAPI,
	textRange: RemoteTextRange,
	unit: RemoteIntEnum[TextUnit] | TextUnit,
	reverse: bool = False
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
