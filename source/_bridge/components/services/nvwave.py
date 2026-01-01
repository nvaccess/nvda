# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import typing
import rpyc
import nvwave
from logHandler import log
from _bridge.base import Service


@rpyc.service
class WavePlayerService(Service):
	"""Wraps a local WavePlayer, exposing its methods for remote access.
	When accessed remotely, this service must be wrapped in a `_bridge.components.proxies.nvwave.WavePlayerProxy` which will handle any deserialization and provide the same interface as a local SynthDriver.
	Arguments and return types on the methods here are an internal detail and not thoroughly documented, as they should not be used directly.
	:ivar _player: The WavePlayer instance being wrapped.
	"""

	_player: nvwave.WavePlayer

	def __init__(
		self,
		childProcess,
		channels: int,
		samplesPerSec: int,
		bitsPerSample: int,
		outputDevice: str,
		wantDucking: bool = True,
	):
		super().__init__(childProcess)
		self._player = nvwave.WavePlayer(
			channels=channels,
			samplesPerSec=samplesPerSec,
			bitsPerSample=bitsPerSample,
			outputDevice=outputDevice,
			wantDucking=wantDucking,
		)
		log.debug("WavePlayer instance created")

	@Service.exposed
	def createWavePlayerFeederServiceConnection(self) -> tuple[int, int]:
		"""Create and return a WavePlayerFeeder service to feed audio data to this WavePlayer over RPYC."""
		feederService = WavePlayerFeederService(self._childProcess, self._player)
		return self._createDependentConnection(feederService, name="WavePlayerFeeder for WavePlayer")

	@Service.exposed
	def setVolume(self, *, all: float | None = None, left: float | None = None, right: float | None = None):
		self._player.setVolume(all=all, left=left, right=right)

	@Service.exposed
	def pause(self, switch: bool):
		self._player.pause(switch)

	@Service.exposed
	def stop(self):
		self._player.stop()

	@Service.exposed
	def close(self):
		self._player.close()

	def terminate(self):
		log.debug("Deleting WavePlayer instance")
		del self._player
		super().terminate()


@rpyc.service
class WavePlayerFeederService(Service):
	"""A helper service to feed audio data to a WavePlayer over RPYC.
	Used internally by WavePlayerProxy.
	"""

	_player: nvwave.WavePlayer

	def __init__(self, childProcess, player: nvwave.WavePlayer):
		super().__init__(childProcess)
		self._player = player

	@Service.exposed
	def feed(
		self, data: bytes, size: typing.Optional[int] = None, onDone: typing.Optional[typing.Callable] = None
	) -> None:
		if onDone:

			def localOnDone():
				log.debug("WavePlayerFeeder feed onDone callback start")
				onDone()
				log.debug("WavePlayerFeeder feed onDone callback end")
		else:
			localOnDone = None
		self._player.feed(data, size=size, onDone=onDone)

	def terminate(self):
		log.debug("Deleting WavePlayer instance")
		del self._player
		super().terminate()
