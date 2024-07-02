# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2010-2024 NV Access Limited, World Light Information Limited,
# Hong Kong Blind Union, Babbage B.V., Julien Cochuyt, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import codecs
import os.path
from .data import LocaleDataMap
from logHandler import log
import globalVars


class CharacterDescriptions:
	"""
	Represents a map of characters to one or more descriptions (examples) for that character.
	The data is loaded from a file from the requested locale.
	"""

	def __init__(self, locale: str):
		"""
		@param locale: The characterDescriptions.dic file will be found by using this locale.
		"""
		self._entries: dict[str, list[str]] = {}
		fileName = os.path.join(globalVars.appDir, "locale", locale, "characterDescriptions.dic")
		if not os.path.isfile(fileName):
			raise LookupError(fileName)
		with codecs.open(fileName, "r", "utf_8_sig", errors="replace") as f:
			for line in f:
				if line.isspace() or line.startswith("#"):
					continue
				line = line.rstrip("\r\n")
				temp = line.split("\t")
				if len(temp) > 1:
					key = temp.pop(0)
					self._entries[key] = temp
				else:
					log.warning("can't parse line '%s'" % line)
			log.debug("Loaded %d entries." % len(self._entries))

	def getCharacterDescription(self, character: str) -> list[str] | None:
		"""
		Looks up the given character and returns a list containing all the description strings found.
		"""
		return self._entries.get(character)


_charDescLocaleDataMap: LocaleDataMap[CharacterDescriptions] = LocaleDataMap(CharacterDescriptions)


def getCharacterDescription(locale: str, character: str) -> list[str] | None:
	"""
	Finds a description or examples for the given character, which makes sense in the given locale.
	@param locale: the locale (language[_COUNTRY]) the description should be for.
	@param character: the character to fetch the description for.
	@return: the found description for the given character
	"""
	try:
		l = _charDescLocaleDataMap.fetchLocaleData(locale)  # noqa: E741
	except LookupError:
		if not locale.startswith("en"):
			return getCharacterDescription("en", character)
		raise LookupError("en")
	desc = l.getCharacterDescription(character)
	if not desc and not locale.startswith("en"):
		desc = getCharacterDescription("en", character)
	return desc
