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

	@property
	def decoded(self):
		return text_type(self)

	def __new__(cls, value="", encoding="utf-8", errors="strict"):
		if isinstance(value, (bytes, bytearray)):
			obj = super(DuoString, cls).__new__(cls, value, encoding. errors)
			obj.encoded = value
		else:
			obj = super(DuoString, cls).__new__(cls, value)
			obj.encoded = obj.encode(encoding, errors)
		obj.encoding = encodings.normalize_encoding(encoding)
		obj.bytesPerIndex = cls._encodingToBytes[obj.encoding]
		obj.errors = errors
		return obj

	def __len__(self):
		return len(self.encoded) / self.bytesPerIndex

	def __getitem__(self, key):
		if isinstance(key, int):
			start = key * self.bytesPerIndex
			stop = start + self.bytesPerIndex
			step = None
		elif isinstance(key, slice):
			start = key.start
			if start is not None:
				start *= self.bytesPerIndex
			stop = key.stop
			if stop is not None:
				stop *= self.bytesPerIndex
			step = key.step
		else:
			return NotImplemented
		key = slice(start, stop, step)
		item = self.encoded[key].decode(self.encoding, self.errors)
		return item
