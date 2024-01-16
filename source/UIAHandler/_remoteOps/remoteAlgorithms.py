# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

import contextlib
from .midLevel import (
	remoteFunc,
	RemoteUint,
	RemoteInt,
	RemoteArray
)
from .highLevel import RemoteFuncAPI


@contextlib.contextmanager
@remoteFunc
def unsignedRangeBlock(rfa: RemoteFuncAPI, start: RemoteUint, stop: RemoteUint, step: RemoteUint = RemoteUint(1, const=True)):
	counter =start.copy()
	with rfa.whileBlock(lambda: counter < stop):
		yield counter
		counter += step

@contextlib.contextmanager
@remoteFunc
def signedRangeBlock(rfa: RemoteFuncAPI, start: RemoteInt, stop: RemoteInt, step: RemoteInt = RemoteInt(1, const=True)):
	counter = rfa.newInt(start)
	with rfa.whileBlock(lambda: counter < stop):
		yield counter
		counter += step

@contextlib.contextmanager
@remoteFunc
def forEachBlock(rfa: RemoteFuncAPI, array: RemoteArray):
	with unsignedRangeBlock(rfa, RemoteUint(0, const=True), array.size()) as index:
		yield array[index]
