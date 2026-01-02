# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations
from functools import cached_property
import typing
import ctypes
from ...base import Proxy

if typing.TYPE_CHECKING:
	from ..services.nvwave import WavePlayerService
from logHandler import log
from _bridge.components.services.nvwave import WavePlayerFeederService


class WavePlayerProxy(Proxy):
	"""Wraps a remote WavePlayerService, providing the same interface as a local WavePlayer."""

	def __init__(
		self,
		remoteServiceFactory: typing.Callable[..., WavePlayerService],
		channels: int,
		samplesPerSec: int,
		bitsPerSample: int,
		outputDevice: str | None = None,
		wantDucking: bool = True,
	):
		remoteService = remoteServiceFactory(
			channels=channels,
			samplesPerSec=samplesPerSec,
			bitsPerSample=bitsPerSample,
			outputDevice=outputDevice,
			wantDucking=wantDucking,
		)
		super().__init__(remoteService)

	@cached_property
	def _remoteFeederService(self) -> WavePlayerFeederService:
		log.debug("Creating WavePlayerFeeder service connection for WavePlayerProxy")
		r_handle, w_handle = self._remoteService.createWavePlayerFeederServiceConnection()
		feederService = self._connectToDependentServiceOverPipes(
			r_handle,
			w_handle,
			name="WavePlayerFeeder for WavePlayer on Proxy",
		)
		return feederService

	def setVolume(self, *, all: float | None = None, left: float | None = None, right: float | None = None):
		# log.debug("setVolume start")
		self._remoteService.setVolume(all=all, left=left, right=right)
		# log.debug("setVolume end")

	def feed(
		self,
		data: bytes,
		size: typing.Optional[int] = None,
		onDone: typing.Optional[typing.Callable] = None,
	) -> None:
		log.debug("feed start")
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
		log.debug("Calling remote feed")
		self._remoteFeederService.feed(data, size=size, onDone=onDone)
		log.debug("feed end")

	def idle(self):
		self._remoteFeederService.idle()

	def pause(self, switch: bool):
		# log.debug("pause start")
		self._remoteService.pause(switch)
		# log.debug("pause end")

	def stop(self):
		# log.debug("stop start")
		self._remoteService.stop()
		# log.debug("stop end")

	def close(self):
		# log.debug("close start")
		self._remoteService.close()
			# log.debug("close end")
