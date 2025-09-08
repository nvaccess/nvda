# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2017-2021 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Recognition of text using the UWP OCR engine included in Windows 10 and later."""

import json
import NVDAHelper
from NVDAHelper.localWin10 import (
	uwpOcr_getLanguages,
	uwpOcr_initialize,
	uwpOcr_recognize,
	uwpOcr_terminate,
	uwpOcr_Callback as _uwpOcr_Callback,
)
from . import ContentRecognizer, LinesWordsResult
import config
import languageHandler
from utils import _deprecate

__getattr__ = _deprecate.handleDeprecations(
	_deprecate.MovedSymbol("uwpOcr_Callback", "NVDAHelper.localWin10"),
)


def getLanguages():
	"""Return the available recognition languages.
	@return: A list of language codes suitable to be passed to L{UwpOcr}'s constructor.
		These need to be normalized with L{languageHandler.normalizeLanguage}
		for use as NVDA language codes.
	@rtype: list of str
	"""
	langs = uwpOcr_getLanguages()
	return langs.split(";")[:-1]


def getInitialLanguage():
	"""Get the language to use the first time UWP OCR is used.
	The NVDA interface language is used if a matching OCR language is available.
	Otherwise, this falls back to the first available language.
	"""
	nvdaLang = languageHandler.getLanguage()
	ocrLangs = getLanguages()
	return _getInitialLanguage(nvdaLang, ocrLangs)


def _getInitialLanguage(nvdaLang, ocrLangs):
	# Try the full language code.
	for lang in ocrLangs:
		normLang = languageHandler.normalizeLanguage(lang)
		if nvdaLang == normLang:
			return lang
	# Try the language code without country.
	nvdaLangPrimary = nvdaLang.split("_", 1)[0]
	for lang in ocrLangs:
		# Don't need to normalize here because the primary code is
		# the same when normalized.
		if lang.startswith(nvdaLangPrimary):
			return lang
	# Fall back to the first OCR language.
	if len(ocrLangs) >= 1:
		return ocrLangs[0]
	raise LookupError("No UWP OCR languages installed")


def getConfigLanguage():
	"""Get the user's configured OCR language.
	If no language has been configured, choose an initial language
	and update the configuration.
	"""
	lang = config.conf["uwpOcr"]["language"]
	if lang:
		return lang
	initial = getInitialLanguage()
	config.conf["uwpOcr"]["language"] = initial
	return initial


class UwpOcr(ContentRecognizer):
	@classmethod
	def _get_allowAutoRefresh(cls) -> bool:
		return config.conf["uwpOcr"]["autoRefresh"]

	@classmethod
	def _get_autoRefreshInterval(cls) -> int:
		return config.conf["uwpOcr"]["autoRefreshInterval"]

	def getResizeFactor(self, width, height):
		# UWP OCR performs poorly with small images, so increase their size.
		if width < 100 or height < 100:
			return 4
		return 1

	def __init__(self, language=None):
		"""
		@param language: The language code of the desired recognition language,
			C{None} to use the user's configured language.
		"""
		if language:
			self.language = language
		else:
			self.language = getConfigLanguage()
		self._dll = NVDAHelper.getHelperLocalWin10Dll()

	def recognize(self, pixels, imgInfo, onResult):
		self._onResult = onResult

		@_uwpOcr_Callback
		def callback(result):
			# If self._onResult is None, recognition was cancelled.
			if self._onResult:
				if result:
					data = json.loads(result)
					self._onResult(LinesWordsResult(data, imgInfo))
				else:
					self._onResult(RuntimeError("UWP OCR failed"))
			uwpOcr_terminate(self._handle)
			self._callback = None
			self._handle = None

		self._callback = callback
		self._handle = uwpOcr_initialize(self.language, callback)
		if not self._handle:
			onResult(RuntimeError("UWP OCR initialization failed"))
			return
		uwpOcr_recognize(self._handle, pixels, imgInfo.recogWidth, imgInfo.recogHeight)

	def cancel(self):
		self._onResult = None
