# -*- coding: UTF-8 -*-

#textUtils.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Babbage B.V.

"""
Classes and utilities to deal with strings.
"""

from six import text_type
import encodings
import sys
try:
	from collections import Sequence # Python 2.7 import
except ImportError:
	from collections.abc import Sequence # Python 3 import

byteTypes = (bytes, bytearray)
defaultStringEncoding = "utf_16_le" if sys.version_info.major == 2 else "utf_32_le"

class EncodingAwareString(Sequence, text_type):
	u"""
	Magic string object that holds a string in both its decoded and its UTF-x encoded form.
	The indexes and length of the resulting objects are based on the byte size of the given encoding.

	First, an instance is created:

	>> string = EncodingAwareString(u'\U0001f609', encoding="utf_32_le")

	Then, the length of the string can be fetched:

	>>> len(string)
	1

	And the object can be indexed and sliced:

	>>> string[0]
	EncodingAwareString(u'\U0001f609')

	This example string behaves exactly the same as a Python 3 string, where 1 index is 1 code point.
	Therefore, the following happens on Python 3:

	>>> len(string.decoded)
	1

	However, on Python 2, the result differs:

	>>> len(string.decoded)
	2

	This is because Python 2 on Windows uses a 2 byte encoding to store the string.
	The oposite is accomplished with an instance like this:

	>> string = EncodingAwareString(u"\U0001f609", encoding="utf_16_le")
	>>> len(string)
	2
	"""

	__slots__=("bytesPerIndex", "encoded", "encoding", "errors")
	_encodingToBytes = {
		"utf_8": 1,
		"utf_16_le": 2,
		"utf_32_le": 4,
	}

	def __new__(cls, value, encoding, errors="replace"):
		encoding = encodings.normalize_encoding(encoding)
		if encoding not in cls._encodingToBytes:
			raise ValueError("Encoding %s not supported. Supported values are %s" % (
				encoding,
				", ".join(cls._encodingToBytes)
			))
		if isinstance(value, byteTypes):
			obj = super(EncodingAwareString, cls).__new__(cls, value, encoding, errors)
			obj.encoded = value
		else:
			obj = super(EncodingAwareString, cls).__new__(cls, value)
			obj.encoded = obj.encode(encoding, errors)
		obj.encoding = encoding
		obj.bytesPerIndex = cls._encodingToBytes[obj.encoding]
		obj.errors = errors
		return obj

	@property
	def decoded(self):
		return text_type(self)

	def __repr__(self):
		return "{}({})".format(self.__class__.__name__, repr(self.decoded))

	def __add__(self, value):
		return EncodingAwareString(super(EncodingAwareString, self).__add__(value), self.encoding, self.errors)

	def __radd__(self, value):
		return EncodingAwareString(super(EncodingAwareString, self).__radd__(value), self.encoding, self.errors)

	def __mul__(self, value):
		return EncodingAwareString(super(EncodingAwareString, self).__mul__(value), self.encoding, self.errors)

	def __rmul__(self, value):
		return EncodingAwareString(super(EncodingAwareString, self).__rmul__(value), self.encoding, self.errors)

	def __mod__(self, args):
		return EncodingAwareString(super(EncodingAwareString, self).__mod__(args), self.encoding, self.errors)

	def __rmod__(self, args):
		return EncodingAwareString(super(EncodingAwareString, self).__rmod__(args), self.encoding, self.errors)

	def __len__(self):
		return len(self.encoded) // self.bytesPerIndex

	def __getitem__(self, key):
		if self.bytesPerIndex == 1 and sys.version_info.major == 2:
			newKey = key
		elif isinstance(key, int):
			if key >= len(self):
				raise IndexError("%s index out of range" % EncodingAwareString.__name__)
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
				return EncodingAwareString("".join(self[i] for i in keys), self.encoding, self.errors)
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
		return EncodingAwareString(self.encoded[newKey], self.encoding, self.errors)

	def __contains__(self, char):
		if isinstance(char, byteTypes):
			return char in self.encoded
		return super(EncodingAwareString, self).__contains__(char)

	def count(self, sub, start=0, end=sys.maxsize):
		if isinstance(sub, text_type):
			sub = sub.encode(self.encoding, self.errors)
		if isinstance(sub, byteTypes):
			start *= self.bytesPerIndex
			end = min(end * self.bytesPerIndex, sys.maxsize)
			return self.encoded.count(sub, start, end) / self.bytesPerIndex
		return super(EncodingAwareString, self).count(sub, start, end)

	def format(self, *args, **kwargs):
		return EncodingAwareString(super(EncodingAwareString, self).format(*args, **kwargs), self.encoding, self.errors)


	def find(self, sub, start=0, end=sys.maxsize):
		if isinstance(sub, text_type):
			sub = sub.encode(self.encoding, self.errors)
		if isinstance(sub, byteTypes):
			start *= self.bytesPerIndex
			end = min(end * self.bytesPerIndex, sys.maxsize)
			return self.encoded.find(sub, start, end) / self.bytesPerIndex
		return super(EncodingAwareString, self).find(sub, start, end)

	def index(self, sub, start=0, end=sys.maxsize):
		if isinstance(sub, text_type):
			sub = sub.encode(self.encoding, self.errors)
		if isinstance(sub, byteTypes):
			start *= self.bytesPerIndex
			end = min(end * self.bytesPerIndex, sys.maxsize)
			return self.encoded.index(sub, start, end) / self.bytesPerIndex
		return super(EncodingAwareString, self).index(sub, start, end)

	def join(self, seq):
		return EncodingAwareString(super(EncodingAwareString, self).join(seq), self.encoding, self.errors)

	def lstrip(self, chars=None):
		if isinstance(chars, byteTypes):
			return EncodingAwareString(self.encoded.lstrip(chars), self.encoding, self.errors)
		return EncodingAwareString(self.decoded.lstrip(chars), self.encoding, self.errors)

	def rfind(self, sub, start=0, end=sys.maxsize):
		if isinstance(sub, text_type):
			sub = sub.encode(self.encoding, self.errors)
		if isinstance(sub, byteTypes):
			start *= self.bytesPerIndex
			end = min(end * self.bytesPerIndex, sys.maxsize)
			return self.encoded.rfind(sub, start, end) / self.bytesPerIndex
		return super(EncodingAwareString, self).rrfind(sub, start, end)

	def rindex(self, sub, start=0, end=sys.maxsize):
		if isinstance(sub, text_type):
			sub = sub.encode(self.encoding, self.errors)
		if isinstance(sub, byteTypes):
			start *= self.bytesPerIndex
			end = min(end * self.bytesPerIndex, sys.maxsize)
			return self.encoded.rindex(sub, start, end) / self.bytesPerIndex
		return super(EncodingAwareString, self).rindex(sub, start, end)

	def rstrip(self, chars=None):
		if isinstance(chars, byteTypes):
			return EncodingAwareString(self.encoded.strip(chars), self.encoding, self.errors)
		return EncodingAwareString(self.decoded.strip(chars), self.encoding, self.errors)

	def strip(self, chars=None):
		if isinstance(chars, byteTypes):
			return EncodingAwareString(self.encoded.strip(chars), self.encoding, self.errors)
		return EncodingAwareString(self.decoded.strip(chars), self.encoding, self.errors)

def getEncodingAwareString(value, encoding, errors="replace"):
	"""Creates a string that is encoding aware if necessary.
	On python 2, UTF_16_le will result in an unicode object,
	as it uses UCS-2/UTF-16 internally.
	On python 3, UTF_32_le will result in a str object,
	as 1 index corresponds to 1 code point.
	Other encodings will result in a L{EncodeAwareString} object.
	"""
	encoding = encodings.normalize_encoding(encoding)
	if encoding == defaultStringEncoding:
		stringType = text_type
	else:
		stringType = EncodingAwareString
	if isinstance(value, byteTypes):
		return stringType(value, encoding, errors)
	elif encoding == defaultStringEncoding:
		return stringType(value)
	else:
		return EncodingAwareString(value, encoding, errors)

