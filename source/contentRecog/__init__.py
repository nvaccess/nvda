#contentRecog/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Framework for recognition of content; OCR, image recognition, etc.
When authors don't provide sufficient information for a screen reader user to determine the content of something,
various tools can be used to attempt to recognize the content from an image.
Some examples are optical character recognition (OCR) to recognize text in an image
and the Microsoft Cognitive Services Computer Vision and Google Cloud Vision APIs to describe images.
Recognizers take an image and produce text.
They are implemented using the L{ContentRecognizer} class.
"""

from collections import namedtuple
import textInfos.offsets

class ContentRecognizer(object):
	"""Implementation of a content recognizer.
	"""

	def getResizeFactor(self, width, height):
		"""Return the factor by which an image must be resized
		before it is passed to this recognizer.
		@param width: The width of the image in pixels.
		@type width: int
		@param height: The height of the image in pixels.
		@type height: int
		@return: The resize factor, C{1} for no resizing.
		@rtype: int or float
		"""
		return 1

	def recognize(self, pixels, width, height, coordConverter, onResult):
		"""Asynchronously recognize content from an image.
		This method should not block.
		Only one recognition can be performed at a time.
		@param pixels: The pixels of the image as a two dimensional array of RGBQUADs.
			For example, to get the red value for the coordinate (1, 2):
			pixels[2][1].rgbRed
			This can be treated as raw bytes in BGRA8 format;
			i.e. four bytes per pixel in the order blue, green, red, alpha.
			However, the alpha channel should be ignored.
		@type pixels: Two dimensional array (y then x) of L{winGDI.RGBQUAD}
		@param width: The width of the image in pixels.
		@type width: int
		@param height: The height of the image in pixels.
		@type height: int
		@param coordConverter: The converter to convert coordinates
			in the supplied image to screen coordinates.
			This should be used when returning coordinates to NVDA.
		@type coordConverter: L{ResultCoordConverter}
		@param onResult: A callable which takes a L{RecognitionResult} (or an exception on failure) as its only argument.
		@type onResult: callable
		"""
		raise NotImplementedError

	def cancel(self):
		"""Cancel the recognition in progress (if any).
		"""
		raise NotImplementedError

class ResultCoordConverter(object):
	"""Converts coordinates in a recognition result to screen coordinates.
	An image captured for recognition can begin at any point on the screen.
	However, the image is cropped when passed to the recognizer.
	Also, some recognizers need the image to be resized prior to recognition.
	This converter converts coordinates in the recognized image
	to screen coordinates suitable to be returned to NVDA;
	e.g. in order to route the mouse.
	"""

	def __init__(self, left, top, resizeFactor):
		"""
		@param left: The x screen coordinate of the upper-left corner of the image.
		@type left: int
		@param top: The y screen coordinate of the upper-left corner of the image.
		@type top: int
		@param resizeFactor: The factor by which the image was resized for recognition.
		@type resizeFactor: int or float
		"""
		self.left = left
		self.top = top
		self.resizeFactor = resizeFactor

	def convertX(self, x):
		"""Convert an x coordinate in the result to an x coordinate on the screen.
		"""
		return self.left + int(x / self.resizeFactor)

	def convertY(self, y):
		"""Convert an x coordinate in the result to an x coordinate on the screen.
		"""
		return self.top + int(y / self.resizeFactor)

class RecognitionResult(object):
	"""Provides access to the result of recognition by a recognizer.
	The result is textual, but to facilitate navigation by word, line, etc.
	and to allow for retrieval of screen coordinates within the text,
	L{TextInfo} objects are used.
	Callers use the L{makeTextInfo} method to create a L{TextInfo}.
	Most implementers should use one of the subclasses provided in this module.
	"""

	def makeTextInfo(self, obj, position):
		"""Make a TextInfo within the recognition result text at the requested position.
		@param obj: The object to return for the C{obj} property of the TextInfo.
			The TextInfo itself doesn't use this, but NVDA requires it to set the review object, etc.
		@param position: The requested position; one of the C{textInfos.POSITION_*} constants.
		@return: The TextInfo at the requested position in the result.
		@rtype: L{textInfos.TextInfo}
		"""
		raise NotImplementedError

# Used by LinesWordsResult.
LwrWord = namedtuple("LwrWord", ("offset", "left", "top"))

class LinesWordsResult(RecognitionResult):
	"""A L{RecognizerResult} which can create TextInfos based on a simple lines/words data structure.
	The data structure is a list of lines, wherein each line is a list of words,
	wherein each word is a dict containing the keys x, y, width, height and text.
	Several OCR engines produce output in a format which can be easily converted to this.
	"""

	def __init__(self, data, coordConverter):
		"""Constructor.
		@param data: The lines/words data structure. For example:
			[
				[
					{"x": 106, "y": 91, "width": 11, "height": 9, "text": "Word1"},
					{"x": 117, "y": 91, "width": 11, "height": 9, "text": "Word2"}
				],
				[
					{"x": 106, "y": 105, "width": 11, "height": 9, "text": "Word3"},
					{"x": 117, "y": 105, "width": 11, "height": 9, "text": "Word4"}
				]
			]
		@type data: list of lists of dicts
		@param coordConverter: The converter to convert coordinates
			in the supplied image to screen coordinates.
			This should be used when returning coordinates to NVDA.
		@type coordConverter: L{ResultCoordConverter}
		"""
		self.data = data
		self.coordConverter = coordConverter
		self._textList = []
		self.textLen = 0
		#: End offsets for each line.
		self.lines = []
		#: Start offsets and screen coordinates for each word.
		self.words = []
		self._parseData()
		self.text = "".join(self._textList)

	def _parseData(self):
		for line in self.data:
			firstWordOfLine = True
			for word in line:
				if firstWordOfLine:
					firstWordOfLine = False
				else:
					# Separate with a space.
					self._textList.append(" ")
					self.textLen += 1
				self.words.append(LwrWord(self.textLen,
					self.coordConverter.convertX(word["x"]),
					self.coordConverter.convertY(word["y"])))
				text = word["text"]
				self._textList.append(text)
				self.textLen += len(text)
			# End with new line.
			self._textList.append("\n")
			self.textLen += 1
			self.lines.append(self.textLen)

	def makeTextInfo(self, obj, position):
		return LwrTextInfo(obj, position, self)

class LwrTextInfo(textInfos.offsets.OffsetsTextInfo):
	"""TextInfo used by L{LinesWordsResult}.
	This should only be instantiated by L{LinesWordsResult}.
	"""

	def __init__(self, obj, position, result):
		self.result = result
		super(LwrTextInfo, self).__init__(obj, position)

	def copy(self):
		return self.__class__(self.obj, self.bookmark, self.result)

	def _getTextRange(self, start, end):
		return self.result.text[start:end]

	def _getStoryLength(self):
		return self.result.textLen

	def _getLineOffsets(self, offset):
		start = 0
		for end in self.result.lines:
			if end > offset:
				return (start, end)
			start = end
		# offset is too big. Fail gracefully by returning the last line.
		return (start, self.result.textLen)

	def _getWordOffsets(self, offset):
		start = 0
		for word in self.result.words:
			if word.offset > offset:
				return (start, word.offset)
			start = word.offset
		# offset is in the last word (or offset is too big).
		return (start, self.result.textLen)

	def _getPointFromOffset(self, offset):
		word = None
		for nextWord in self.result.words:
			if nextWord.offset > offset:
				# Stop! We need the word before this.
				break
			word = nextWord
		return textInfos.Point(word.left, word.top)

class SimpleTextResult(RecognitionResult):
	"""A L{RecognitionResult} which presents a simple text string.
	NVDA calculates words and lines itself based on the text;
	e.g. a new line character breaks a line.
	Routing the mouse, etc. cannot be supported.
	This should only be used if the recognizer only returns text
	and no coordinate information.
	"""

	def __init__(self, text):
		self.text = text

	def makeTextInfo(self, obj, position):
		return SimpleResultTextInfo(obj, position, self)

class SimpleResultTextInfo(textInfos.offsets.OffsetsTextInfo):
	"""TextInfo used by L{SimpleTextResult}.
	This should only be instantiated by L{SimpleTextResult}.
	"""

	def __init__(self, obj, position, result):
		self.result = result
		super(SimpleResultTextInfo, self).__init__(obj, position)

	def copy(self):
		return self.__class__(self.obj, self.bookmark, self.result)

	def _getStoryText(self):
		return self.result.text

	def _getStoryLength(self):
		return len(self.result.text)

	def _getStoryText(self):
		return self.result.text
