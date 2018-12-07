#textUtils.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Babbage B.V.

from six import text_type
import encodings

class DuoString(text_type):
	"""
	Magic string object that holds a string in both its decoded and encoded forms.
	"""
	__slots__=("bytesPerIndex", "encoded", "encoding", "errors")
	_encodingToBytes = {
		"utf_8": 1,
		"utf_16_le": 2,
		"utf_32_le": 4,
	}

	def __new__(cls, value="", encoding="utf_16_le", errors="surrogatepass"):
		if isinstance(value, (bytes, bytearray)):
			obj = super(DuoString, cls).__new__(cls, value, encoding, errors)
			obj.encoded = value
		else:
			obj = super(DuoString, cls).__new__(cls, value)
			obj.encoded = obj.encode(encoding, errors)
		obj.encoding = encodings.normalize_encoding(encoding)
		obj.bytesPerIndex = cls._encodingToBytes[obj.encoding]
		obj.errors = errors
		return obj

	@property
	def decoded(self):
		return text_type(self)

	def __repr__(self):
		return "{}({})".format(self.__class__.__name__, self.decoded)

	def __add__(self, value):
		if isinstance(value, (bytes, bytearray)):
			return DuoString(self.encoded + value, self.encoding, self.errors)
		return DuoString(self.decoded + value, self.encoding, self.errors)

	def __radd__(self, value):
		if isinstance(value, (bytes, bytearray)):
			return DuoString(value + self.encoded, self.encoding, self.errors)
		return DuoString(value + self.decoded, self.encoding, self.errors)

	def __len__(self):
		return len(self.encoded) // self.bytesPerIndex

	def __getitem__(self, key):
		if self.bytesPerIndex == 1:
			newKey = key
		elif isinstance(key, int):
			if key >= len(self):
				raise IndexError("%s index out of range" % self.__class__.__name__)
			start = key * self.bytesPerIndex
			stop = start + self.bytesPerIndex
			newKey = slice(start, stop)
		elif isinstance(key, slice):
			if key.step and key.step > 1:
				start = key.start or 0
				if key.stop is None:
					stop = len(self) - 1
				else:
					stop = min(key.stop, len(self) - 1)
				step = key.step
				keys = range(start, stop, step)
				return DuoString("".join(self[i] for i in keys), self.encoding, self.errors)
			start = key.start
			if start is not None:
				start *= self.bytesPerIndex
			stop = key.stop
			if stop is not None:
				stop *= self.bytesPerIndex
			step = key.step
			newKey = slice(start, stop, step)
		else:
			return NotImplemented
		return DuoString(self.encoded[newKey], self.encoding, self.errors)
