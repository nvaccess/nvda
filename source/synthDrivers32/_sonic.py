# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2025 NV Access Limited, gexgd0419

from ctypes import CDLL, POINTER, Array, c_float, c_int, c_short, c_ubyte, c_void_p, cdll
import os
from typing import TYPE_CHECKING
from logHandler import log

if TYPE_CHECKING:
	from ctypes import _Pointer

	c_float_p = _Pointer[c_float]
	c_short_p = _Pointer[c_short]
	c_ubyte_p = _Pointer[c_ubyte]
else:
	c_float_p = POINTER(c_float)
	c_short_p = POINTER(c_short)
	c_ubyte_p = POINTER(c_ubyte)

sonicLib: CDLL | None = None


class SonicStreamP(c_void_p):
	pass


def initialize():
	"""Initialize the Sonic DLL.
	The sonic.dll file should be in the synthDrivers directory.
	This can be called more than once."""
	global sonicLib
	if sonicLib:
		return
	log.debug("Initializing Sonic library")
	sonicLib = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), "sonic.dll"))
	sonicLib.sonicCreateStream.restype = SonicStreamP
	sonicLib.sonicCreateStream.argtypes = [c_int, c_int]
	sonicLib.sonicDestroyStream.restype = None
	sonicLib.sonicDestroyStream.argtypes = [SonicStreamP]
	sonicLib.sonicWriteFloatToStream.restype = c_int
	sonicLib.sonicWriteFloatToStream.argtypes = [SonicStreamP, c_void_p, c_int]
	sonicLib.sonicWriteShortToStream.restype = c_int
	sonicLib.sonicWriteShortToStream.argtypes = [SonicStreamP, c_void_p, c_int]
	sonicLib.sonicWriteUnsignedCharToStream.restype = c_int
	sonicLib.sonicWriteUnsignedCharToStream.argtypes = [SonicStreamP, c_void_p, c_int]
	sonicLib.sonicReadFloatFromStream.restype = c_int
	sonicLib.sonicReadFloatFromStream.argtypes = [SonicStreamP, c_void_p, c_int]
	sonicLib.sonicReadShortFromStream.restype = c_int
	sonicLib.sonicReadShortFromStream.argtypes = [SonicStreamP, c_void_p, c_int]
	sonicLib.sonicReadUnsignedCharFromStream.restype = c_int
	sonicLib.sonicReadUnsignedCharFromStream.argtypes = [SonicStreamP, c_void_p, c_int]
	sonicLib.sonicFlushStream.restype = c_int
	sonicLib.sonicFlushStream.argtypes = [SonicStreamP]
	sonicLib.sonicSamplesAvailable.restype = c_int
	sonicLib.sonicSamplesAvailable.argtypes = [SonicStreamP]
	sonicLib.sonicGetSpeed.restype = c_float
	sonicLib.sonicGetSpeed.argtypes = [SonicStreamP]
	sonicLib.sonicSetSpeed.restype = None
	sonicLib.sonicSetSpeed.argtypes = [SonicStreamP, c_float]
	sonicLib.sonicGetPitch.restype = c_float
	sonicLib.sonicGetPitch.argtypes = [SonicStreamP]
	sonicLib.sonicSetPitch.restype = None
	sonicLib.sonicSetPitch.argtypes = [SonicStreamP, c_float]
	sonicLib.sonicGetRate.restype = c_float
	sonicLib.sonicGetRate.argtypes = [SonicStreamP]
	sonicLib.sonicSetRate.restype = None
	sonicLib.sonicSetRate.argtypes = [SonicStreamP, c_float]
	sonicLib.sonicGetVolume.restype = c_float
	sonicLib.sonicGetVolume.argtypes = [SonicStreamP]
	sonicLib.sonicSetVolume.restype = None
	sonicLib.sonicSetVolume.argtypes = [SonicStreamP, c_float]
	sonicLib.sonicGetQuality.restype = c_int
	sonicLib.sonicGetQuality.argtypes = [SonicStreamP]
	sonicLib.sonicSetQuality.restype = None
	sonicLib.sonicSetQuality.argtypes = [SonicStreamP, c_int]
	sonicLib.sonicGetSampleRate.restype = c_int
	sonicLib.sonicGetSampleRate.argtypes = [SonicStreamP]
	sonicLib.sonicSetSampleRate.restype = None
	sonicLib.sonicSetSampleRate.argtypes = [SonicStreamP, c_int]
	sonicLib.sonicGetNumChannels.restype = c_int
	sonicLib.sonicGetNumChannels.argtypes = [SonicStreamP]
	sonicLib.sonicSetNumChannels.restype = None
	sonicLib.sonicSetNumChannels.argtypes = [SonicStreamP, c_int]


class SonicStream:
	"""
	Audio stream that wraps the Sonic library to process audio,
	which is optimised for speeding up speech by high factors.
	Audio data are stored internally as 16-bit integers.
	"""

	def __init__(self, sampleRate: int, channels: int):
		self.stream: SonicStreamP = sonicLib.sonicCreateStream(sampleRate, channels)
		if not self.stream:
			raise MemoryError()

	def __del__(self):
		sonicLib.sonicDestroyStream(self.stream)

	def writeFloat(self, data: c_float_p, numSamples: int) -> None:
		"""Write 32-bit floating point data to be processed into the stream,
		where each sample must be between -1 and 1.
		:param data: A pointer to 32-bit floating point wave data.
		:param numSamples: The number of samples.
			Multiply this by channel count to get the total number of values.
		:raises MemoryError: If memory allocation failed."""
		if not sonicLib.sonicWriteFloatToStream(self.stream, data, numSamples):
			raise MemoryError()

	def writeShort(self, data: c_short_p, numSamples: int) -> None:
		"""Write 16-bit integer data to be processed into the stream.
		:param data: A pointer to 16-bit integer wave data.
		:param numSamples: The number of samples.
			Multiply this by channel count to get the total number of values.
		:raises MemoryError: If memory allocation failed."""
		if not sonicLib.sonicWriteShortToStream(self.stream, data, numSamples):
			raise MemoryError()

	def writeUnsignedChar(self, data: c_ubyte_p, numSamples: int) -> None:
		"""Write 8-bit unsigned integer data to be processed into the stream.
		:param data: A pointer to 8-bit integer wave data.
		:param numSamples: The number of samples.
			Multiply this by channel count to get the total number of values.
		:raises MemoryError: If memory allocation failed."""
		if not sonicLib.sonicWriteUnsignedCharToStream(self.stream, data, numSamples):
			raise MemoryError()

	def readFloat(self) -> Array[c_float]:
		"""Read processed data from the stream as 32-bit floating point data."""
		samples = self.samplesAvailable
		arrayLength = samples * self.channels
		buffer = (c_float * arrayLength)()
		sonicLib.sonicReadFloatFromStream(self.stream, buffer, samples)
		return buffer

	def readShort(self) -> Array[c_short]:
		"""Read processed data from the stream as 16-bit integer data."""
		samples = self.samplesAvailable
		arrayLength = samples * self.channels
		buffer = (c_short * arrayLength)()
		sonicLib.sonicReadShortFromStream(self.stream, buffer, samples)
		return buffer

	def readUnsignedChar(self) -> Array[c_ubyte]:
		"""Read processed data from the stream as 8-bit unsigned integer data."""
		samples = self.samplesAvailable
		arrayLength = samples * self.channels
		buffer = (c_ubyte * arrayLength)()
		sonicLib.sonicReadUnsignedCharFromStream(self.stream, buffer, samples)
		return buffer

	def flush(self) -> None:
		"""Force the sonic stream to generate output using whatever data it currently has.
		No extra delay will be added to the output, but flushing in the middle of words could introduce distortion.
		This is usually done when data writing is completed.
		:raises MemoryError: If memory allocation failed."""
		if not sonicLib.sonicFlushStream(self.stream):
			raise MemoryError()

	@property
	def samplesAvailable(self) -> int:
		return sonicLib.sonicSamplesAvailable(self.stream)

	@property
	def speed(self) -> float:
		return sonicLib.sonicGetSpeed(self.stream)

	@speed.setter
	def speed(self, value: float):
		sonicLib.sonicSetSpeed(self.stream, value)

	@property
	def pitch(self) -> float:
		return sonicLib.sonicGetPitch(self.stream)

	@pitch.setter
	def pitch(self, value: float):
		sonicLib.sonicSetPitch(self.stream, value)

	@property
	def rate(self) -> float:
		"""This scales pitch and speed at the same time."""
		return sonicLib.sonicGetRate(self.stream)

	@rate.setter
	def rate(self, value: float):
		sonicLib.sonicSetRate(self.stream, value)

	@property
	def volume(self) -> float:
		"""The scaling factor of the stream."""
		return sonicLib.sonicGetVolume(self.stream)

	@volume.setter
	def volume(self, value: float):
		sonicLib.sonicSetVolume(self.stream, value)

	@property
	def quality(self) -> int:
		"""Default 0 is virtually as good as 1, but very much faster."""
		return sonicLib.sonicGetQuality(self.stream)

	@quality.setter
	def quality(self, value: int):
		sonicLib.sonicSetQuality(self.stream, value)

	@property
	def sampleRate(self) -> int:
		return sonicLib.sonicGetSampleRate(self.stream)

	@sampleRate.setter
	def sampleRate(self, value: int):
		sonicLib.sonicSetSampleRate(self.stream, value)

	@property
	def channels(self) -> int:
		return sonicLib.sonicGetNumChannels(self.stream)

	@channels.setter
	def channels(self, value: int):
		sonicLib.sonicSetNumChannels(self.stream, value)
