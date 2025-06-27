# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""LanguageHandler module proxy for add-ons running in ART."""

from typing import List, Optional, Tuple
from .base import ServiceProxyMixin


class _LanguageHandlerProxy(ServiceProxyMixin):
	"""Internal proxy class for languageHandler service."""
	_service_env_var = "NVDA_ART_LANGUAGE_SERVICE_URI"


def getLanguage() -> str:
	"""Get the current NVDA language.
	
	@return: The current language code (e.g., "en", "es", "fr_FR")
	"""
	result = _LanguageHandlerProxy._call_service("getLanguage")
	return result if result is not None else "en"


def getLanguageDescription(language: str) -> Optional[str]:
	"""Get a human-readable description of a language code.
	
	@param language: Language code (e.g., "en", "es", "fr_FR")
	@return: Localized language description or None if not found
	"""
	return _LanguageHandlerProxy._call_service("getLanguageDescription", language)


def normalizeLanguage(lang: str) -> Optional[str]:
	"""Normalize a language-dialect string to standard form.
	
	Converts any dash to underline, and makes sure that language is lowercase 
	and dialect is uppercase.
	
	@param lang: Language code to normalize
	@return: Normalized language code or None if invalid
	"""
	return _LanguageHandlerProxy._call_service("normalizeLanguage", lang)


def getAvailableLanguages(presentational: bool = False) -> List[Tuple[str, str]]:
	"""Get list of available languages.
	
	@param presentational: Whether this is meant to be shown alphabetically by language description
	@return: List of (language_code, description) tuples
	"""
	result = _LanguageHandlerProxy._call_service("getAvailableLanguages", presentational)
	return result if result is not None else []


def getWindowsLanguage() -> str:
	"""Get the locale name of the user's configured language in Windows.
	
	@return: Windows language code
	"""
	result = _LanguageHandlerProxy._call_service("getWindowsLanguage")
	return result if result is not None else "en"


def localeNameToWindowsLCID(localeName: str) -> int:
	"""Retrieves the Windows locale identifier (LCID) for the given locale name.
	
	@param localeName: a string of 2letterLanguage_2letterCountry or just language
	@return: a Windows LCID or 0 if it could not be retrieved
	"""
	result = _LanguageHandlerProxy._call_service("localeNameToWindowsLCID", localeName)
	return result if result is not None else 0


def windowsLCIDToLocaleName(lcid: int) -> Optional[str]:
	"""Gets a normalized locale from a Windows LCID.
	
	@param lcid: Windows locale identifier
	@return: Locale name or None if not found
	"""
	return _LanguageHandlerProxy._call_service("windowsLCIDToLocaleName", lcid)


def stripLocaleFromLangCode(langWithOptionalLocale: str) -> str:
	"""Get the lang code eg "en" for "en-au" or "chr" for "chr-US-Qaaa-x-west".
	
	@param langWithOptionalLocale: may already be language only, or include locale specifier
	(e.g. "en" or "en-au").
	@return: The language only part, before the first dash.
	"""
	result = _LanguageHandlerProxy._call_service("stripLocaleFromLangCode", langWithOptionalLocale)
	return result if result is not None else ""


# Constants that add-ons might use
LCID_NONE = 0


def setGlobalTranslation(translations) -> None:
	"""Install translation functions globally.
	
	This function installs the gettext translation functions into the builtins
	namespace, making them available globally throughout the process.
	This matches the behavior of NVDA core's languageHandler.setLanguage().
	
	@param translations: A gettext translation object with gettext, ngettext, 
		pgettext, and npgettext methods
	"""
	import builtins
	
	# Install translation functions into builtins
	# This matches what trans.install(names=["pgettext", "npgettext", "ngettext"]) does
	builtins._ = translations.gettext
	builtins.gettext = translations.gettext
	builtins.ngettext = translations.ngettext
	builtins.pgettext = translations.pgettext
	builtins.npgettext = translations.npgettext
