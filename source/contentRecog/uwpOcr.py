#contentRecog/uwpOcr.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Recognition of text using the UWP OCR engine included in Windows 10.
"""

import ctypes
import json
import NVDAHelper
from . import ContentRecognizer, LinesWordsResult
import config

uwpOcr_Callback = ctypes.CFUNCTYPE(None, ctypes.c_wchar_p)

def getLanguages():
	"""Return the available recognition languages.
	@return: A list of language codes suitable to be passed to L{UwpOcr}'s constructor.
		These need to be normalized with L{languageHandler.normalizeLanguage}
		for use as NVDA language codes.
	@rtype: list of unicode
	"""
	dll = NVDAHelper.getHelperLocalWin10Dll()
	dll.uwpOcr_getLanguages.restype = NVDAHelper.bstrReturn
	langs = dll.uwpOcr_getLanguages()
	return langs.split(";")[:-1]

class UwpOcr(ContentRecognizer):

	def getResizeFactor(self, width, height):
		# UWP OCR performs poorly with small images, so increase their size.
		if width < 100 or height < 100:
			return 4
		return 1

	def __init__(self, language=None):
		"""
		@param language: The language code of the desired recognition language,
			C{None} to use the user's configured default.
		"""
		if language:
			self.language = language
		else:
			self.language = config.conf["uwpOcr"]["language"]
		self._dll = NVDAHelper.getHelperLocalWin10Dll()

	def recognize(self, pixels, width, height, coordConv, onResult):
		self._onResult = onResult
		@uwpOcr_Callback
		def callback(result):
			# If self._onResult is None, recognition was cancelled.
			if self._onResult:
				if result:
					data = json.loads(result)
					self._onResult(LinesWordsResult(data, coordConv))
				else:
					self._onResult(RuntimeError("UWP OCR failed"))
			self._dll.uwpOcr_terminate(self._handle)
			self._callback = None
			self._handle = None
		self._callback = callback
		self._handle = self._dll.uwpOcr_initialize(self.language, callback)
		if not self._handle:
			onResult(RuntimeError("UWP OCR initialization failed"))
			return
		self._dll.uwpOcr_recognize(self._handle, pixels, width, height)

	def cancel(self):
		self._onResult = None
