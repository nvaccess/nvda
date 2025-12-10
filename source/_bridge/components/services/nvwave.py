# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import typing
import rpyc
import nvwave


@rpyc.service
class WavePlayerService:
	""" Wraps a local WavePlayer, exposing its methods for remote access.
	When accessed remotely, this service must be wrapped in a `_bridge.components.proxies.nvwave.WavePlayerProxy` which will handle any deserialization and provide the same interface as a local SynthDriver.
	Arguments and return types on the methods here are an internal detail and not thoroughly documented, as they should not be used directly.
	:ivar _player: The WavePlayer instance being wrapped.
	"""
	_player: nvwave.WavePlayer

	def __init__(self, channels: int, samplesPerSec: int, bitsPerSample: int, outputDevice: str, wantDucking: bool = True):
		self._player = nvwave.WavePlayer(channels=channels, samplesPerSec=samplesPerSec, bitsPerSample=bitsPerSample, outputDevice=outputDevice, wantDucking=wantDucking)

	@rpyc.exposed
	def setVolume(self, *, all: float | None= None, left: float | None= None, right: float | None= None):
		self._player.setVolume(all=all, left=left, right=right)

	@rpyc.exposed
	def feed(self, data: bytes, size: typing.Optional[int] = None, onDone: typing.Optional[typing.Callable] = None) -> None:
		if onDone:
			onDone = rpyc.async_(onDone)
		self._player.feed(data, size=size, onDone=onDone)

	@rpyc.exposed
	def pause(self, switch: bool):
		self._player.pause(switch)

	@rpyc.exposed
	def stop(self):
		self._player.stop()

	@rpyc.exposed
	def close(self):
		self._player.close()
