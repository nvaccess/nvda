#contentRecog/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Support for cloud-based content recognition.
"""

import os
import threading
import tempfile
import urllib
import json
import urllib2
import PIL.Image
import httpRequest
from . import ContentRecognizer, SimpleTextResult

class CloudRecognizer(ContentRecognizer):
	"""Base class for a content recognizer which operates on an image file
	and runs in a background thread.
	This is intended for use with cloud-based content recognition services.
	Subclasses should override the L{recogRequest} method.
	"""

	def recognize(self, pixels, imgInfo, onResult):
		img = PIL.Image.frombytes("RGBX", (imgInfo.recogWidth, imgInfo.recogHeight), pixels)
		self._fileName = tempfile.mktemp(prefix="nvda_cloundContentRecog_", suffix=".jpg")
		img.save(self._fileName)
		self._onResult = onResult
		t = threading.Thread(target=self._bgRecog)
		t.daemon = True
		t.start()

	def _bgRecog(self):
		try:
			result = self.recogRequest(self._fileName)
		except Exception as e:
			result = e
		finally:
			os.remove(self._fileName)
		if self._onResult:
			self._onResult(result)

	def cancel(self):
		self._onResult = None

	def recogRequest(self, fileName):
		"""Perform recognition.
		This should block until complete and then return the result.
		It is run in a background thread.
		@rtype: L{contentRecog.RecognitionResult}
		"""
		raise NotImplementedError

class CaptionBot(CloudRecognizer):
	"""Image recognition using Microsoft's CaptionBot (https://www.captionbot.ai/) service.
	"""
	# Based on the captionbot Python package by Tatiana Krikun: https://github.com/krikunts/captionbot
	BASE_URL = "https://www.captionbot.ai/api/"

	def _init(self):
		url = self.BASE_URL + "init"
		resp = urllib2.urlopen(url)
		self.conversationId = httpRequest.getJsonFromResponse(resp)

	def _upload(self, fileName):
		url = self.BASE_URL + "upload"
		with file(fileName, "rb") as fileObj:
			files = [("file", os.path.basename(fileName), fileObj)]
			resp = httpRequest.urlopenWithFiles(url, files)
			return httpRequest.getJsonFromResponse(resp)

	def _message(self, message):
		url = self.BASE_URL + "message"
		data = {
			"userMessage": message,
			"conversationId": self.conversationId,
			"waterMark": ""}
		httpRequest.urlopenWithJson(url, data)
		# The post request doesn't return anything.
		# We have to make a get request with the same data to obtain the response.
		getUrl = url + "?" + urllib.urlencode(data)
		resp = urllib2.urlopen(getUrl)
		# This is double JSON encoded.
		resp = httpRequest.getJsonFromResponse(resp)
		return json.loads(resp)

	def recogRequest(self, fileName):
		self._init()
		imgUrl = self._upload(fileName)
		resp = self._message(imgUrl)
		# resp["BotMessages"][0] is the URL, [1] is the caption.
		text = resp["BotMessages"][1]
		return SimpleTextResult(text)
