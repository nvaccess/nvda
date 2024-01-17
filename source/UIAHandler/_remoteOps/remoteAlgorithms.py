# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

from __future__ import annotations
from collections.abc import Generator
import contextlib
from .midLevel import (
	remoteFunc,
	RemoteBool,
	RemoteUint,
	RemoteInt,
	RemoteArray,
	RemoteTextRange,
	RemoteVariant
)
import operator
from .highLevel import RemoteFuncAPI
from .lowLevel import (
	TextPatternRangeEndpoint,
	TextUnit,
)


@contextlib.contextmanager
@remoteFunc
def remote_unsignedRange(rfa: RemoteFuncAPI, start: RemoteUint, stop: RemoteUint, step: RemoteUint ) -> Generator[RemoteUint, None, None]:
	counter =start.copy()
	with rfa.whileBlock(lambda: counter < stop):
		yield counter
		counter += step

@contextlib.contextmanager
@remoteFunc
def remote_signedRange(rfa: RemoteFuncAPI, start: RemoteInt, stop: RemoteInt, step: RemoteInt) -> Generator[RemoteInt, None, None]:
	counter = rfa.newInt(start)
	with rfa.whileBlock(lambda: counter < stop):
		yield counter
		counter += step

@contextlib.contextmanager
@remoteFunc
def remote_forEachItemInArray(rfa: RemoteFuncAPI, array: RemoteArray) -> Generator[RemoteVariant, None, None]:
	with remote_unsignedRange(rfa, start=0, stop=array.size(), step=1) as index:
		yield array[index]

@contextlib.contextmanager
@remoteFunc
def remote_forEachUnitInTextRange(rfa: RemoteFuncAPI, textRange: RemoteTextRange, unit: RemoteInt) -> Generator[RemoteTextRange, None, None]:
	logicalTextRange = textRange.getLogicalAdapter(True)
	logicalTempRange = logicalTextRange.clone()
	logicalTempRange.end = logicalTempRange.start
	with rfa.whileBlock(lambda: logicalTempRange.start < logicalTextRange.end):
		logicalTempRange.end.moveByUnit(unit, 1)
		with rfa.ifBlock(logicalTempRange.end > logicalTextRange.end):
			logicalTempRange.end = logicalTextRange.end
		yield logicalTempRange.getTextRange()
		logicalTempRange.start = logicalTempRange.end
