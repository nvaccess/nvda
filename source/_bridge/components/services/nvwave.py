import typing
import rpyc
import nvwave


class WavePlayerService(rpyc.Service):

	def __init__(self, channels: int, samplesPerSec: int, bitsPerSample: int, outputDevice: str | None = None, wantDucking: bool = True):
		self._player = nvwave.WavePlayer(channels=channels, samplesPerSec=samplesPerSec, bitsPerSample=bitsPerSample, outputDevice=outputDevice, wantDucking=wantDucking)

	def exposed_setVolume(self, *, all: float | None= None, left: float | None= None, right: float | None= None):
		self._player.setVolume(all=all, left=left, right=right)

	def exposed_feed(self, data: bytes, size: typing.Optional[int] = None, onDone: typing.Optional[typing.Callable] = None) -> None:
		if onDone:
			onDone = rpyc.async_(onDone)
		self._player.feed(data, size=size, onDone=onDone)

	def exposed_pause(self, switch: bool):
		self._player.pause(switch)

	def exposed_stop(self):
		self._player.stop()

	def exposed_close(self):
		self._player.close()
