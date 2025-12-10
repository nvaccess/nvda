# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations
import typing
import ctypes
from ...base import Proxy
if typing.TYPE_CHECKING:
	from ..services.nvwave import WavePlayerService


class WavePlayerProxy(Proxy):
	""" Wraps a remote WavePlayerService, providing the same interface as a local WavePlayer. """
	_player: WavePlayerService

	def __init__(self, remoteService, channels: int, samplesPerSec: int, bitsPerSample: int, outputDevice: str | None = None, wantDucking: bool = True):
		self._player = remoteService(channels=channels, samplesPerSec=samplesPerSec, bitsPerSample=bitsPerSample, outputDevice=outputDevice, wantDucking=wantDucking)

	def setVolume(self, *, all: float | None= None, left: float | None= None, right: float | None= None):
		self._player.setVolume(all=all, left=left, right=right)

	def feed(self, data: bytes, size: typing.Optional[int] = None, onDone: typing.Optional[typing.Callable] = None) -> None:
		if isinstance(data, ctypes.Array):
			if size is None:
				size = ctypes.sizeof(data)
			else:
				size = min(size, ctypes.sizeof(data))
			data = ctypes.string_at(data, size)
		elif isinstance(data, ctypes.c_void_p):
			if size is None:
				raise ValueError("Size must be provided when feeding from a ctypes pointer")
			data = ctypes.string_at(data, size)
		self._player.feed(data, size=size, onDone=onDone)

	def pause(self, switch: bool):
		self._player.pause(switch)

	def stop(self):
		self._player.stop()

	def close(self):
		self._player.close()
