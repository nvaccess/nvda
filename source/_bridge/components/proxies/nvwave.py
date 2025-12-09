import typing
import ctypes
import rpyc
from logHandler import log
from ...base import Proxy


class WavePlayerProxy(Proxy):

	def __init__(self, remoteService, channels: int, samplesPerSec: int, bitsPerSample: int, outputDevice: str | None = None, wantDucking: bool = True):
		self._player = remoteService(channels=channels, samplesPerSec=samplesPerSec, bitsPerSample=bitsPerSample, outputDevice=outputDevice, wantDucking=wantDucking)

	def setVolume(self, *, all: float | None= None, left: float | None= None, right: float | None= None):
		self._player.setVolume(all=all, left=left, right=right)

	def feed(self, data: bytes, size: typing.Optional[int] = None, onDone: typing.Optional[typing.Callable] = None) -> None:
		if isinstance(data, (ctypes.c_void_p, ctypes.Array)):
			data = ctypes.string_at(data, size)
		self._player.feed(data, size=size, onDone=onDone)

	def pause(self, switch: bool):
		self._player.pause(switch)

	def stop(self):
		self._player.stop()

	def close(self):
		self._player.close()
