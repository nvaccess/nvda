# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""Language handler service for ART - provides language/locale functionality to add-ons."""

import languageHandler
import Pyro5.api

from .base import BaseService


@Pyro5.api.expose
class LanguageHandlerService(BaseService):
	"""Provides language and locale functionality for add-ons running in ART."""

	def __init__(self):
		super().__init__("LanguageHandlerService")

	def getLanguage(self) -> str:
		"""Get the current NVDA language."""
		try:
			return languageHandler.getLanguage()
		except Exception:
			self._log_error("getLanguage")
			return "en"

	def getLanguageDescription(self, language: str) -> str:
		"""Get a human-readable description of a language code."""
		try:
			desc = languageHandler.getLanguageDescription(language)
			return desc if desc else ""
		except Exception:
			self._log_error("getLanguageDescription", language)
			return ""

	def normalizeLanguage(self, lang: str) -> str:
		"""Normalize a language-dialect string to standard form."""
		try:
			normalized = languageHandler.normalizeLanguage(lang)
			return normalized if normalized else ""
		except Exception:
			self._log_error("normalizeLanguage", lang)
			return ""

	def getAvailableLanguages(self, presentational: bool = False) -> list:
		"""Get list of available languages."""
		try:
			# Convert list of tuples to list of lists for JSON serialization
			langs = languageHandler.getAvailableLanguages(presentational)
			return [[code, desc] for code, desc in langs]
		except Exception:
			self._log_error("getAvailableLanguages")
			return []

	def getWindowsLanguage(self) -> str:
		"""Get the locale name of the user's configured language in Windows."""
		try:
			return languageHandler.getWindowsLanguage()
		except Exception:
			self._log_error("getWindowsLanguage")
			return "en"

	def localeNameToWindowsLCID(self, localeName: str) -> int:
		"""Retrieves the Windows locale identifier (LCID) for the given locale name."""
		try:
			return languageHandler.localeNameToWindowsLCID(localeName)
		except Exception:
			self._log_error("localeNameToWindowsLCID", localeName)
			return 0

	def windowsLCIDToLocaleName(self, lcid: int) -> str:
		"""Gets a normalized locale from a Windows LCID."""
		try:
			localeName = languageHandler.windowsLCIDToLocaleName(lcid)
			return localeName if localeName else ""
		except Exception:
			self._log_error("windowsLCIDToLocaleName", str(lcid))
			return ""

	def stripLocaleFromLangCode(self, langWithOptionalLocale: str) -> str:
		"""Get the lang code eg "en" for "en-au"."""
		try:
			stripped = languageHandler.stripLocaleFromLangCode(langWithOptionalLocale)
			return stripped if stripped else ""
		except Exception:
			self._log_error("stripLocaleFromLangCode", langWithOptionalLocale)
			return ""
